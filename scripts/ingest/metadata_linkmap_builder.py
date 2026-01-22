#!/usr/bin/env python3
"""
Build metadata-linkmap-input.json from inputs.md + service briefs summary.
Always overwrites the output file.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse


def load_inputs(path: Path) -> dict[str, object]:
    data: dict[str, object] = {
        "name": "",
        "website": "",
        "phone": "",
        "areas": [],
        "keywords": [],
        "services": [],
        "service_urls": {},
    }
    lines = [line.rstrip("\n") for line in path.read_text(encoding="utf-8").splitlines()]

    keywords: list[str] = []
    areas: list[str] = []
    services: list[str] = []
    service_urls: dict[str, str] = {}
    in_keywords = False
    in_areas = False
    in_services = False

    for line in lines:
        if line.startswith("- Business name:"):
            data["name"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Website:"):
            data["website"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Phone:"):
            data["phone"] = line.split(":", 1)[1].strip()

        if line.startswith("- Keywords"):
            in_keywords = True
            tail = line.split(":", 1)[1].strip()
            if tail.startswith("[") and tail.endswith("]"):
                content = tail.strip("[]")
                for item in content.split("\n"):
                    item = item.strip().strip(",")
                    if item:
                        keywords.append(item)
            continue
        if in_keywords:
            if line.strip().startswith("]"):
                in_keywords = False
                continue
            item = line.strip().strip(",")
            if item:
                keywords.append(item)

        if line.startswith("- Areas served"):
            in_areas = True
            continue
        if line.startswith("## ") and in_areas:
            in_areas = False
        if in_areas and line.startswith("  - "):
            area = line.replace("  - ", "", 1).strip()
            if area:
                areas.append(area)

        if line.startswith("## Approved service list"):
            in_services = True
            continue
        if line.startswith("## ") and in_services:
            in_services = False
        if in_services and line.startswith("- "):
            entry = line.replace("- ", "", 1).strip()
            if not entry:
                continue
            name, _, rest = entry.partition(":")
            name = name.strip()
            url_match = re.search(r"\((https?://[^)]+)\)", rest)
            url = url_match.group(1) if url_match else ""
            if name:
                services.append(name)
            if url:
                service_urls[name] = url

    data["keywords"] = keywords
    data["areas"] = areas
    data["services"] = services
    data["service_urls"] = service_urls
    return data


def load_service_summary(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_linkmap_payload(inputs: dict[str, object], summary: dict[str, object]) -> dict[str, object]:
    client_name = str(inputs.get("name") or "")
    website = str(inputs.get("website") or "")
    phone = str(inputs.get("phone") or "")
    services = list(inputs.get("services") or [])
    service_urls = dict(inputs.get("service_urls") or {})
    keywords = list(inputs.get("keywords") or [])
    areas = list(inputs.get("areas") or [])

    contact_url = ""
    service_hub_url = ""
    pages = summary.get("pages", []) if isinstance(summary.get("pages"), list) else []
    for page in pages:
        for link in page.get("internal_links", []) if isinstance(page, dict) else []:
            if not isinstance(link, str):
                continue
            if "/contact" in link and not contact_url:
                contact_url = urlparse(link).path or "/contact/"
            if "/services" in link and not service_hub_url:
                service_hub_url = urlparse(link).path or "/services/"
        if contact_url and service_hub_url:
            break

    area_links: list[str] = []
    slug_map = {page.get("slug"): page.get("url") for page in pages if isinstance(page, dict)}
    for area in areas:
        slug = area.lower().replace(" ", "-")
        url = slug_map.get(slug)
        if isinstance(url, str) and url:
            area_links.append(urlparse(url).path)
        else:
            area_links.append(f"/{slug}/")

    service_pages: dict[str, str] = {}
    for name in services:
        url = service_urls.get(name)
        if url:
            service_pages[name] = urlparse(url).path

    service_keyword_map: dict[str, str] = {}
    for service in services:
        s_low = service.lower()
        for kw in keywords:
            if kw.lower() in s_low or s_low in kw.lower():
                service_keyword_map[service] = kw
                break
        if service not in service_keyword_map and keywords:
            service_keyword_map[service] = keywords[0]

    pages_payload: list[dict[str, object]] = []
    for service in services:
        url = service_urls.get(service, "")
        slug = urlparse(url).path.strip("/").split("/")[-1] if url else service.lower().replace(" ", "-")
        related = [s for s in services if s != service]
        pages_payload.append(
            {
                "id": slug,
                "type": "service-page",
                "slug": slug,
                "service": service,
                "primary_keyword": service_keyword_map.get(service, service),
                "related_services": related,
                "service_area_links": area_links,
                "include_faq_schema": True,
                "internal_links": [
                    {"label": "Contact", "url": contact_url or "/contact/", "type": "contact"},
                    {"label": "Services", "url": service_hub_url or "/services/", "type": "hub"},
                ],
            }
        )

    return {
        "client": {
            "name": client_name,
            "phone": phone,
            "website": website,
        },
        "defaults": {
            "contact_url": contact_url or "/contact/",
            "service_hub_url": service_hub_url or "/services/",
            "service_pages": service_pages,
        },
        "pages": pages_payload,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build metadata-linkmap-input.json from inputs + briefs.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    args = parser.parse_args()

    base_dir = Path("data") / "outputs" / args.client_slug
    inputs_path = base_dir / "inputs.md"
    summary_path = base_dir / "reports" / "service-briefs-summary.json"
    output_path = base_dir / "reports" / "metadata-linkmap-input.json"

    if not inputs_path.exists():
        raise SystemExit(f"Missing inputs.md: {inputs_path}")

    inputs = load_inputs(inputs_path)
    summary = load_service_summary(summary_path)
    payload = build_linkmap_payload(inputs, summary)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
