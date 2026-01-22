#!/usr/bin/env python3
"""Scaffold data/outputs/<client>/inputs.md from JSON-LD schema."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SKIP_TYPES = {"WebSite", "WebPage", "BreadcrumbList", "ImageObject"}
SOCIAL_KEYS = {
    "facebook": "Facebook",
    "instagram": "Instagram",
    "linkedin": "LinkedIn",
    "twitter": "X",
    "x.com": "X",
    "youtube": "YouTube",
    "tiktok": "TikTok",
}


@dataclass
class SchemaProfile:
    name: str
    url: str
    telephone: str
    description: str
    address: dict[str, str]
    geo: dict[str, str]
    same_as: list[str]
    hours: list[str]
    areas_served: list[str]
    services: list[str]
    price_range: str
    payment_forms: list[str]
    keywords: list[str]


def load_schema(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Schema file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def extract_nodes(data: Any) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []

    def add(node: Any) -> None:
        if isinstance(node, dict):
            nodes.append(node)
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, dict):
                    nodes.append(item)

    if isinstance(data, dict):
        add(data)
        add(data.get("@graph"))
        add(data.get("mainEntity"))
        add(data.get("mainEntityOfPage"))
        add(data.get("about"))
        add(data.get("publisher"))
    elif isinstance(data, list):
        add(data)

    return nodes


def node_types(node: dict[str, Any]) -> list[str]:
    raw = node.get("@type")
    if isinstance(raw, list):
        return [str(item) for item in raw]
    if isinstance(raw, str):
        return [raw]
    return []


def node_score(node: dict[str, Any]) -> int:
    types = node_types(node)
    score = 0
    if "LocalBusiness" in types:
        score += 4
    if any(t.endswith("Business") for t in types):
        score += 3
    if "Organization" in types:
        score += 2
    if any(t not in SKIP_TYPES for t in types):
        score += 1
    if node.get("name"):
        score += 2
    if node.get("address"):
        score += 1
    if node.get("telephone") or node.get("telePhone"):
        score += 1
    if node.get("url"):
        score += 1
    return score


def pick_primary(nodes: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not nodes:
        return None
    return sorted(nodes, key=node_score, reverse=True)[0]


def first_value(nodes: list[dict[str, Any]], key: str) -> Any:
    for node in nodes:
        if key in node and node.get(key):
            return node.get(key)
    return None


def normalize_day(value: Any) -> str:
    if not value:
        return ""
    if isinstance(value, dict):
        value = value.get("@id") or value.get("name") or ""
    if isinstance(value, str) and "/" in value:
        return value.split("/")[-1]
    return str(value)


def extract_hours(node: dict[str, Any]) -> list[str]:
    hours: list[str] = []
    raw = node.get("openingHours")
    if isinstance(raw, list):
        hours.extend([str(item) for item in raw if item])
    elif isinstance(raw, str):
        hours.append(raw)

    specs = node.get("openingHoursSpecification")
    if isinstance(specs, dict):
        specs = [specs]
    if isinstance(specs, list):
        for spec in specs:
            if not isinstance(spec, dict):
                continue
            days = spec.get("dayOfWeek")
            if isinstance(days, list):
                day_names = [normalize_day(day) for day in days]
            else:
                day_names = [normalize_day(days)] if days else []
            opens = spec.get("opens", "")
            closes = spec.get("closes", "")
            if day_names and (opens or closes):
                for day in day_names:
                    hours.append(f"{day}: {opens}-{closes}".strip("-"))
    return hours


def extract_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return []


def extract_area_names(value: Any) -> list[str]:
    names: list[str] = []
    if isinstance(value, dict):
        name = value.get("name") or value.get("addressLocality")
        if name:
            names.append(str(name))
    elif isinstance(value, list):
        for item in value:
            names.extend(extract_area_names(item))
    elif isinstance(value, str):
        names.append(value)
    return names


def extract_services(value: Any) -> list[str]:
    services: list[str] = []
    if isinstance(value, dict):
        if value.get("name"):
            services.append(str(value["name"]))
        if value.get("itemOffered"):
            services.extend(extract_services(value.get("itemOffered")))
        if value.get("itemListElement"):
            services.extend(extract_services(value.get("itemListElement")))
    elif isinstance(value, list):
        for item in value:
            services.extend(extract_services(item))
    elif isinstance(value, str):
        services.append(value)
    return services


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def parse_schema(data: dict[str, Any]) -> SchemaProfile:
    nodes = extract_nodes(data)
    primary = pick_primary(nodes)
    if not primary:
        raise SystemExit("Schema did not contain any JSON-LD nodes")

    name = primary.get("name") or first_value(nodes, "name") or ""
    if not name:
        raise SystemExit("Schema is missing name across available nodes")

    url = primary.get("url") or first_value(nodes, "url") or ""
    telephone = primary.get("telephone") or primary.get("telePhone") or first_value(nodes, "telephone") or ""
    description = primary.get("description") or first_value(nodes, "description") or ""

    address = primary.get("address") or first_value(nodes, "address") or {}
    if not isinstance(address, dict):
        address = {}

    geo = primary.get("geo") or first_value(nodes, "geo") or {}
    if not isinstance(geo, dict):
        geo = {}

    same_as = extract_strings(primary.get("sameAs") or first_value(nodes, "sameAs") or [])

    hours = extract_hours(primary)
    if not hours:
        for node in nodes:
            hours = extract_hours(node)
            if hours:
                break

    areas = extract_area_names(primary.get("areaServed") or primary.get("serviceArea") or [])
    if not areas:
        for node in nodes:
            areas = extract_area_names(node.get("areaServed") or node.get("serviceArea") or [])
            if areas:
                break

    services: list[str] = []
    for node in nodes:
        for key in ("service", "makesOffer", "offers", "hasOfferCatalog"):
            services.extend(extract_services(node.get(key)))
    services = dedupe([s for s in services if s])

    price_range = str(primary.get("priceRange") or first_value(nodes, "priceRange") or "")
    payment = extract_strings(primary.get("paymentAccepted") or first_value(nodes, "paymentAccepted") or [])

    keywords_raw = primary.get("keywords") or first_value(nodes, "keywords") or []
    if isinstance(keywords_raw, str):
        keywords = [item.strip() for item in keywords_raw.split(",") if item.strip()]
    else:
        keywords = extract_strings(keywords_raw)

    return SchemaProfile(
        name=name,
        url=url,
        telephone=telephone,
        description=description,
        address={
            "line1": address.get("streetAddress", ""),
            "city": address.get("addressLocality", ""),
            "region": address.get("addressRegion", ""),
            "postal": address.get("postalCode", ""),
            "country": address.get("addressCountry", ""),
        },
        geo={
            "lat": str(geo.get("latitude", "")),
            "lng": str(geo.get("longitude", "")),
        },
        same_as=dedupe([s for s in same_as if s]),
        hours=dedupe([h for h in hours if h]),
        areas_served=dedupe([a for a in areas if a]),
        services=dedupe([s for s in services if s]),
        price_range=price_range,
        payment_forms=dedupe([p for p in payment if p]),
        keywords=dedupe([k for k in keywords if k]),
    )


def social_lines(same_as: list[str]) -> list[str]:
    lines: list[str] = []
    remaining = list(same_as)
    for key, label in SOCIAL_KEYS.items():
        for url in list(remaining):
            if key in url:
                lines.append(f"  - {label}: {url}")
                remaining.remove(url)
                break
    for url in remaining:
        lines.append(f"  - Other: {url}")
    return lines


def render_inputs(profile: SchemaProfile) -> str:
    lines: list[str] = []
    lines.append(f"# {profile.name} - Approved Inputs + Placeholders")
    lines.append("")
    lines.append("## Approved business facts")
    lines.append(f"- Business name: {profile.name}")
    lines.append(f"- Website: {profile.url or '[add website]'}")
    lines.append(f"- Phone: {profile.telephone or '[add phone]'}")
    lines.append("- Email: [add email]")
    lines.append("- Address:")
    lines.append(f"  - Line 1: {profile.address.get('line1') or '[add line 1]'}")
    lines.append("  - Line 2: [add line 2]")
    lines.append(f"  - City: {profile.address.get('city') or '[add city]'}")
    lines.append(f"  - State: {profile.address.get('region') or '[add state]'}")
    lines.append(f"  - Postal code: {profile.address.get('postal') or '[add postal]'}")
    lines.append(f"  - Country: {profile.address.get('country') or '[add country]'}")
    lines.append("- Hours:")
    if profile.hours:
        for hour in profile.hours:
            lines.append(f"  - {hour}")
    else:
        lines.append("  - Monday: [add]")
        lines.append("  - Tuesday: [add]")
        lines.append("  - Wednesday: [add]")
        lines.append("  - Thursday: [add]")
        lines.append("  - Friday: [add]")
        lines.append("  - Saturday: [add]")
        lines.append("  - Sunday: [add]")
    lines.append("- Areas served (verified list):")
    if profile.areas_served:
        for area in profile.areas_served:
            lines.append(f"  - {area}")
    else:
        lines.append("  - [add area]")
    lines.append("")

    lines.append("## Approved profile details")
    lines.append(f"- Short description: {profile.description or '[add short description]'}")
    lines.append("- Long description: [add long description]")
    if profile.keywords:
        lines.append(f"- Keywords (approved list): {', '.join(profile.keywords)}")
    else:
        lines.append("- Keywords (approved list): [add keywords]")
    lines.append(f"- Price range: {profile.price_range or '[add]'}")
    if profile.payment_forms:
        lines.append(f"- Payment forms: {', '.join(profile.payment_forms)}")
    else:
        lines.append("- Payment forms: [add]")
    lines.append("- Social:")
    if profile.same_as:
        lines.extend(social_lines(profile.same_as))
    else:
        lines.append("  - Facebook: [add]")
        lines.append("  - Instagram: [add]")
    lines.append("")

    lines.append("## Approved service list (descriptions)")
    if profile.services:
        for service in profile.services:
            lines.append(f"- {service}: [Description]")
    else:
        lines.append("- [Service]: [Description]")
    lines.append("")

    lines.append("## Placeholder (needs approved inputs)")
    lines.append(f"- Geo latitude: {profile.geo.get('lat') or '[add]'}")
    lines.append(f"- Geo longitude: {profile.geo.get('lng') or '[add]'}")
    lines.append("- Proof points (with sources): [add]")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold inputs.md from JSON-LD schema.")
    parser.add_argument("--schema", required=True, help="Path to JSON-LD schema file")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    args = parser.parse_args()

    schema_data = load_schema(Path(args.schema))
    profile = parse_schema(schema_data)

    out_dir = Path("data") / "outputs" / args.client_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "inputs.md"
    out_path.write_text(render_inputs(profile), encoding="utf-8")

    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
