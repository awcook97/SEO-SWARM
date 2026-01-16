#!/usr/bin/env python3
"""Scaffold outputs/<client>/inputs.md from JSON-LD schema."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class SchemaProfile:
    name: str
    url: str
    telephone: str
    description: str
    address: dict[str, str]
    geo: dict[str, str]


def load_schema(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Schema file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def parse_schema(data: dict[str, Any]) -> SchemaProfile:
    name = data.get("name", "")
    url = data.get("url", "")
    telephone = data.get("telephone", data.get("telePhone", ""))
    description = data.get("description", "")
    address = data.get("address") or {}
    geo = data.get("geo") or {}

    if not name:
        raise SystemExit("Schema is missing name")

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
    )


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
    lines.append("  - Monday: [add]")
    lines.append("  - Tuesday: [add]")
    lines.append("  - Wednesday: [add]")
    lines.append("  - Thursday: [add]")
    lines.append("  - Friday: [add]")
    lines.append("  - Saturday: [add]")
    lines.append("  - Sunday: [add]")
    lines.append("- Areas served (verified list):")
    lines.append("  - [add area]")
    lines.append("")

    lines.append("## Approved profile details")
    lines.append(f"- Short description: {profile.description or '[add short description]'}")
    lines.append("- Long description: [add long description]")
    lines.append("- Keywords (approved list): [add keywords]")
    lines.append("- Price range: [add]")
    lines.append("- Payment forms: [add]")
    lines.append("- Social:")
    lines.append("  - Facebook: [add]")
    lines.append("  - Instagram: [add]")
    lines.append("")

    lines.append("## Approved service list (descriptions)")
    lines.append("- [Service]: [Description]")
    lines.append("")

    lines.append("## Placeholder (needs approved inputs)")
    lines.append("- Geo latitude: {lat}".format(lat=profile.geo.get("lat") or "[add]"))
    lines.append("- Geo longitude: {lng}".format(lng=profile.geo.get("lng") or "[add]"))
    lines.append("- Proof points (with sources): [add]")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold inputs.md from JSON-LD schema.")
    parser.add_argument("--schema", required=True, help="Path to JSON-LD schema file")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    args = parser.parse_args()

    schema_data = load_schema(Path(args.schema))
    profile = parse_schema(schema_data)

    out_dir = Path("outputs") / args.client_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "inputs.md"
    out_path.write_text(render_inputs(profile), encoding="utf-8")

    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
