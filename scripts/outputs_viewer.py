#!/usr/bin/env python3
"""Simple outputs web viewer for data/outputs."""

from __future__ import annotations

import argparse
import contextlib
import json
import mimetypes
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


def resolve_repo_root() -> Path:
    cwd = Path.cwd()
    if (cwd / ".codex-swarm").exists():
        return cwd
    return Path(__file__).resolve().parent.parent


REPO_ROOT = resolve_repo_root()
VIEWER_HTML = REPO_ROOT / ".codex-swarm" / "viewer" / "outputs.html"


def safe_resolve(base: Path, rel: str) -> Path | None:
    target = (base / rel).resolve()
    if not str(target).startswith(str(base.resolve())):
        return None
    return target


def list_dir_entries(base: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    if not base.exists():
        return entries
    for item in sorted(base.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        entries.append(
            {
                "name": item.name,
                "is_dir": item.is_dir(),
                "size": item.stat().st_size if item.is_file() else 0,
                "modified": int(item.stat().st_mtime),
            }
        )
    return entries


def build_client_overview(client_dir: Path) -> list[dict[str, object]]:
    items = [
        ("Inputs", "inputs.md", "file"),
        ("Measurement Intake", "reports/measurement-intake.md", "file"),
        ("Keyword Map + KPI", "reports/keyword-map-kpi.md", "file"),
        ("Service Briefs Summary", "reports/service-briefs-summary.md", "file"),
        ("Content Briefs Index", "reports/content-briefs.json", "file"),
        ("Metadata + Link Map", "reports/metadata-internal-link-map.json", "file"),
        ("Internal Link Validation", "reports/internal-link-validation.md", "file"),
        ("Draft Compliance Lint", "reports/draft-compliance-lint.md", "file"),
        ("GBP Update Checklist", "reports/gbp-update-checklist.md", "file"),
        ("Technical SEO Audit", "reports/technical-seo-audit.md", "file"),
        ("Schema HTML", "gen-schema/website-tree", "dir"),
    ]
    overview: list[dict[str, object]] = []
    for label, rel_path, kind in items:
        target = safe_resolve(client_dir, rel_path)
        exists = bool(target and target.exists())
        is_dir = bool(target and target.is_dir())
        entry = {
            "label": label,
            "path": rel_path,
            "kind": kind,
            "exists": exists,
            "is_dir": is_dir,
            "bytes": target.stat().st_size if exists and target and target.is_file() else 0,
            "modified": int(target.stat().st_mtime) if exists and target else 0,
        }
        overview.append(entry)
    return overview


class OutputsHandler(BaseHTTPRequestHandler):
    server_version = "OutputsViewer/0.1"

    def log_message(self, fmt: str, *args: object) -> None:
        message = fmt % args if args else fmt
        sys.stderr.write(f"{self.address_string()} - - [{self.log_date_time_string()}] {message}\n")

    def _send_json(self, payload: dict[str, object], status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            return

    def _send_text(self, text: str, status: int = 200, content_type: str = "text/plain; charset=utf-8") -> None:
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_bytes(self, payload: bytes, status: int, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/index.html"}:
            if not VIEWER_HTML.exists():
                self._send_text("outputs.html not found", status=404)
                return
            self._send_text(VIEWER_HTML.read_text(encoding="utf-8"), content_type="text/html; charset=utf-8")
            return
        if parsed.path == "/api/health":
            self._send_json({"ok": True})
            return
        if parsed.path == "/api/clients":
            outputs_dir = self.server.outputs_dir  # type: ignore[attr-defined]
            clients = [
                {"slug": p.name, "has_reports": (p / "reports").exists()}
                for p in sorted(outputs_dir.iterdir(), key=lambda p: p.name.lower())
                if p.is_dir()
            ]
            self._send_json({"ok": True, "clients": clients})
            return
        if parsed.path == "/api/list":
            params = parse_qs(parsed.query)
            client = params.get("client", [""])[0].strip()
            rel_path = params.get("path", [""])[0].strip().lstrip("/")
            if not client:
                self._send_json({"error": "Missing client"}, status=400)
                return
            outputs_dir = self.server.outputs_dir  # type: ignore[attr-defined]
            client_dir = outputs_dir / client
            target = safe_resolve(client_dir, rel_path)
            if not target or not target.exists() or not target.is_dir():
                self._send_json({"error": "Directory not found"}, status=404)
                return
            self._send_json(
                {
                    "ok": True,
                    "client": client,
                    "path": rel_path,
                    "entries": list_dir_entries(target),
                }
            )
            return
        if parsed.path == "/api/overview":
            params = parse_qs(parsed.query)
            client = params.get("client", [""])[0].strip()
            if not client:
                self._send_json({"error": "Missing client"}, status=400)
                return
            outputs_dir = self.server.outputs_dir  # type: ignore[attr-defined]
            client_dir = outputs_dir / client
            if not client_dir.exists():
                self._send_json({"error": "Client not found"}, status=404)
                return
            self._send_json({"ok": True, "client": client, "overview": build_client_overview(client_dir)})
            return
        if parsed.path == "/api/file":
            params = parse_qs(parsed.query)
            client = params.get("client", [""])[0].strip()
            rel_path = params.get("path", [""])[0].strip().lstrip("/")
            if not client or not rel_path:
                self._send_json({"error": "Missing client or path"}, status=400)
                return
            outputs_dir = self.server.outputs_dir  # type: ignore[attr-defined]
            client_dir = outputs_dir / client
            target = safe_resolve(client_dir, rel_path)
            if not target or not target.exists() or not target.is_file():
                self._send_json({"error": "File not found"}, status=404)
                return
            max_bytes = 200_000
            raw = target.read_bytes()
            truncated = len(raw) > max_bytes
            if truncated:
                raw = raw[:max_bytes]
            try:
                content = raw.decode("utf-8")
            except UnicodeDecodeError:
                content = raw.decode("utf-8", errors="replace")
            self._send_json(
                {
                    "ok": True,
                    "client": client,
                    "path": rel_path,
                    "content": content,
                    "truncated": truncated,
                    "bytes": target.stat().st_size,
                }
            )
            return
        if parsed.path.startswith("/files/"):
            outputs_dir = self.server.outputs_dir  # type: ignore[attr-defined]
            rel = parsed.path.replace("/files/", "", 1)
            parts = rel.split("/", 1)
            if len(parts) != 2:
                self._send_text("Not found", status=404)
                return
            client, rel_path = parts[0], parts[1]
            client_dir = outputs_dir / client
            target = safe_resolve(client_dir, rel_path)
            if not target or not target.exists() or not target.is_file():
                self._send_text("Not found", status=404)
                return
            content_type, _ = mimetypes.guess_type(target.name)
            if content_type is None:
                content_type = "application/octet-stream"
            self._send_bytes(target.read_bytes(), status=200, content_type=content_type)
            return
        self._send_text("Not found", status=404)


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve a simple outputs viewer UI")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5181, help="Bind port (default: 5181)")
    parser.add_argument(
        "--outputs-dir",
        default="data/outputs",
        help="Outputs directory (default: data/outputs)",
    )
    args = parser.parse_args()

    outputs_dir = (REPO_ROOT / args.outputs_dir).resolve()
    if not outputs_dir.exists():
        print(f"Outputs directory not found: {outputs_dir}", file=sys.stderr)
        return 1

    addr = f"http://{args.host}:{args.port}"
    print(f"Serving outputs viewer at {addr} (Ctrl+C to stop)")
    httpd = ThreadingHTTPServer((args.host, args.port), OutputsHandler)
    httpd.outputs_dir = outputs_dir  # type: ignore[attr-defined]
    with contextlib.suppress(KeyboardInterrupt):
        httpd.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
