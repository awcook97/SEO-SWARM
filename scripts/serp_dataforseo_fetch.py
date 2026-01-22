#!/usr/bin/env python3
"""Fetch SERP data from DataForSEO and build input JSONs for reporting."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_ENV_PATH = Path(".env")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


def read_input(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def scaffold_input(path: Path) -> None:
    payload = {
        "client": {"name": "Client Name", "period": "2026-01", "prepared_by": "Analyst Name"},
        "keywords": ["service keyword", "city keyword"],
        "location_name": "United States",
        "language_name": "English",
        "device": "desktop",
        "depth": 10,
        "feature_targets": ["Local Pack", "FAQ"],
        "recommended_angles": ["Service comparison", "Pricing transparency"],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_tasks(payload: dict[str, Any]) -> list[dict[str, Any]]:
    keywords = payload.get("keywords") or []
    if not keywords:
        raise SystemExit("Input JSON must include a non-empty 'keywords' list.")
    task_template: dict[str, Any] = {}
    for key in ("location_name", "location_code", "language_name", "language_code", "device", "os", "depth"):
        if payload.get(key) is not None:
            task_template[key] = payload[key]
    tasks = []
    for keyword in keywords:
        task = dict(task_template)
        task["keyword"] = keyword
        tasks.append(task)
    return tasks


def build_auth_header(login: str, password: str) -> str:
    token = base64.b64encode(f"{login}:{password}".encode("utf-8")).decode("utf-8")
    return f"Basic {token}"


def call_api(endpoint: str, login: str, password: str, tasks: list[dict[str, Any]]) -> dict[str, Any]:
    body = json.dumps(tasks).encode("utf-8")
    request = Request(endpoint, data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    request.add_header("Authorization", build_auth_header(login, password))
    try:
        with urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace") if exc.fp else str(exc)
        raise SystemExit(f"DataForSEO API error: {exc.code} {detail}") from exc
    except URLError as exc:
        raise SystemExit(f"DataForSEO request failed: {exc}") from exc


def extract_items(response: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for task in response.get("tasks", []):
        data = task.get("data", {})
        keyword = data.get("keyword")
        for result in task.get("result", []) or []:
            result_keyword = result.get("keyword") or keyword
            for item in result.get("items", []) or []:
                items.append({"keyword": result_keyword, **item})
    return items


def summarize_features(items: list[dict[str, Any]]) -> list[str]:
    features: dict[str, int] = {}
    for item in items:
        feature = item.get("type")
        if not feature:
            continue
        features[feature] = features.get(feature, 0) + 1
    lines = [f"{name}: {count}" for name, count in sorted(features.items())]
    return lines


def build_serp_insights_input(payload: dict[str, Any], items: list[dict[str, Any]]) -> dict[str, Any]:
    client = payload.get("client", {})
    return {
        "client": {
            "name": client.get("name", "[Client]"),
            "period": client.get("period", "[Period]"),
            "prepared_by": client.get("prepared_by", "[Analyst]"),
            "data_sources": ["DataForSEO SERP API"],
            "exported_at": now_iso(),
        },
        "serp_patterns": summarize_features(items) or ["[No SERP features detected]"],
        "competitor_gaps": payload.get("competitor_gaps", []) or [],
        "feature_targets": payload.get("feature_targets", []) or [],
        "recommended_angles": payload.get("recommended_angles", []) or [],
        "notes": ["Generated from DataForSEO SERP export."],
    }


def build_competitor_snapshot_input(payload: dict[str, Any], items: list[dict[str, Any]]) -> dict[str, Any]:
    client = payload.get("client", {})
    competitors: dict[str, dict[str, Any]] = {}
    for item in items:
        if item.get("type") != "organic":
            continue
        domain = item.get("domain") or ""
        url = item.get("url") or ""
        keyword = item.get("keyword") or ""
        if not domain:
            continue
        entry = competitors.setdefault(
            domain,
            {
                "name": domain,
                "domain": domain,
                "primary_services": [],
                "top_pages": [],
                "serp_features": [],
                "notes": "Source: DataForSEO SERP API",
            },
        )
        if url:
            entry["top_pages"].append({"keyword": keyword, "url": url})
    return {
        "client": {
            "name": client.get("name", "[Client]"),
            "period": client.get("period", "[Period]"),
            "prepared_by": client.get("prepared_by", "[Analyst]"),
            "data_sources": ["DataForSEO SERP API"],
            "exported_at": now_iso(),
        },
        "competitors": list(competitors.values()),
        "gaps": {
            "content": payload.get("gap_content", []) or [],
            "service_areas": payload.get("gap_service_areas", []) or [],
            "serp_features": payload.get("gap_serp_features", []) or [],
            "reviews": payload.get("gap_reviews", []) or [],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch SERP data from DataForSEO and build inputs.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument(
        "--input",
        default=None,
        help="Input JSON path (default: data/outputs/<client>/reports/serp-fetch-input.json)",
    )
    parser.add_argument(
        "--endpoint",
        default=None,
        help="DataForSEO endpoint URL (overrides DATAFORSEO_ENDPOINT env var)",
    )
    parser.add_argument("--scaffold", action="store_true", help="Create a scaffold input file if missing.")
    parser.add_argument(
        "--env",
        default=str(DEFAULT_ENV_PATH),
        help="Path to .env file (default: .env)",
    )
    args = parser.parse_args()

    load_env(Path(args.env))

    login = os.environ.get("DATAFORSEO_LOGIN")
    password = os.environ.get("DATAFORSEO_PASSWORD")
    endpoint = args.endpoint or os.environ.get("DATAFORSEO_ENDPOINT")

    if not login or not password:
        raise SystemExit("DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD must be set (in env or .env).")
    if not endpoint:
        raise SystemExit("DataForSEO endpoint missing. Set DATAFORSEO_ENDPOINT or pass --endpoint.")

    base_dir = Path("data") / "outputs" / args.client_slug
    report_dir = base_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input) if args.input else report_dir / "serp-fetch-input.json"
    if not input_path.exists():
        if args.scaffold:
            scaffold_input(input_path)
            print(f"wrote scaffold input to {input_path}")
            return
        raise SystemExit(f"Input file not found: {input_path}. Use --scaffold to create one.")

    payload = read_input(input_path)
    tasks = build_tasks(payload)
    response = call_api(endpoint, login, password, tasks)

    raw_path = report_dir / "serp-export.json"
    raw_path.write_text(json.dumps({"generated_at": now_iso(), "response": response}, indent=2), encoding="utf-8")

    items = extract_items(response)
    serp_input = build_serp_insights_input(payload, items)
    comp_input = build_competitor_snapshot_input(payload, items)

    serp_path = report_dir / "serp-insights-input.json"
    comp_path = report_dir / "competitor-snapshot-input.json"
    serp_path.write_text(json.dumps(serp_input, indent=2), encoding="utf-8")
    comp_path.write_text(json.dumps(comp_input, indent=2), encoding="utf-8")

    print(f"wrote {raw_path}")
    print(f"wrote {serp_path}")
    print(f"wrote {comp_path}")


if __name__ == "__main__":
    main()
