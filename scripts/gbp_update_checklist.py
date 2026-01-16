#!/usr/bin/env python3
"""Generate a GBP update checklist and posting plan from approved inputs."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class ApprovedInputs:
    business_name: str | None = None
    website: str | None = None
    phone: str | None = None
    email: str | None = None
    address: dict[str, str] = field(default_factory=dict)
    hours: dict[str, str] = field(default_factory=dict)
    service_areas: list[str] = field(default_factory=list)
    short_description: str | None = None
    long_description: str | None = None
    keywords: list[str] = field(default_factory=list)
    price_range: str | None = None
    payment_forms: list[str] = field(default_factory=list)
    social: dict[str, str] = field(default_factory=dict)
    services: list[dict[str, str]] = field(default_factory=list)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def split_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_inputs(path: Path) -> ApprovedInputs:
    inputs = ApprovedInputs()
    section = None
    active_block = None

    lines = path.read_text(encoding="utf-8").splitlines()
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            continue

        if stripped.startswith("## "):
            section = stripped[3:].strip()
            active_block = None
            continue
        if stripped.startswith("### "):
            active_block = None
            continue

        if not stripped.startswith("-"):
            continue

        indent = len(raw) - len(raw.lstrip())
        item = stripped.lstrip("-").strip()
        if indent >= 2 and active_block:
            if ":" in item:
                key, value = item.split(":", 1)
                key = key.strip()
                value = value.strip()
            else:
                key, value = item, ""
            if active_block == "address":
                inputs.address[key] = value
            elif active_block == "hours":
                inputs.hours[key] = value
            elif active_block == "service_areas":
                if item:
                    inputs.service_areas.append(item)
            elif active_block == "social":
                if key and value:
                    inputs.social[key] = value
            continue

        if section == "Approved service list (descriptions)":
            if ":" in item:
                name, desc = item.split(":", 1)
                inputs.services.append({"name": name.strip(), "description": desc.strip()})
            continue

        if ":" not in item:
            continue

        key, value = item.split(":", 1)
        key = key.strip()
        value = value.strip()

        if key == "Business name":
            inputs.business_name = value
        elif key == "Website":
            inputs.website = value
        elif key == "Phone":
            inputs.phone = value
        elif key == "Email":
            inputs.email = value
        elif key == "Address":
            active_block = "address"
        elif key == "Hours":
            active_block = "hours"
        elif key.lower().startswith("areas served"):
            active_block = "service_areas"
        elif key == "Short description":
            inputs.short_description = value
        elif key == "Long description":
            inputs.long_description = value
        elif key.startswith("Keywords"):
            inputs.keywords = split_list(value)
        elif key == "Price range":
            inputs.price_range = value
        elif key == "Payment forms":
            inputs.payment_forms = split_list(value)
        elif key == "Social":
            active_block = "social"

    return inputs


def missing_fields(inputs: ApprovedInputs) -> list[str]:
    missing: list[str] = []

    def require(value: str | None, label: str) -> None:
        if not value:
            missing.append(label)

    require(inputs.business_name, "Business name")
    require(inputs.website, "Website")
    require(inputs.phone, "Phone")
    require(inputs.address.get("Line 1"), "Address line 1")
    require(inputs.address.get("City"), "Address city")
    require(inputs.address.get("State"), "Address state")
    require(inputs.address.get("Postal code"), "Address postal code")
    require(inputs.address.get("Country"), "Address country")
    if not inputs.hours:
        missing.append("Hours")
    if not inputs.service_areas:
        missing.append("Service areas")
    require(inputs.short_description, "Short description")
    require(inputs.long_description, "Long description")
    if not inputs.keywords:
        missing.append("Keywords")
    require(inputs.price_range, "Price range")
    if not inputs.payment_forms:
        missing.append("Payment forms")
    if not inputs.services:
        missing.append("Services list")

    missing.append("Categories")
    missing.append("Attributes")
    missing.append("Photos/media list")
    missing.append("Posting cadence/offers")

    return missing


def rotate(values: list[str], idx: int, fallback: str) -> str:
    if not values:
        return fallback
    return values[idx % len(values)]


def build_post_plan(inputs: ApprovedInputs, count: int = 8) -> list[dict[str, str]]:
    areas = inputs.service_areas
    services = [svc["name"] for svc in inputs.services if svc.get("name")]

    rows = []
    for i in range(count):
        rows.append(
            {
                "post": f"Post {i + 1}",
                "date": "[set date]",
                "area": rotate(areas, i, "[add city/area]"),
                "service": rotate(services, i, "[add service]"),
                "cta": "[approved CTA]",
                "asset": "[approved asset]",
                "utm": "[utm]",
            }
        )
    return rows


def render_markdown(inputs: ApprovedInputs, missing: list[str], plan: list[dict[str, str]]) -> str:
    lines: list[str] = []
    lines.append("# GBP update checklist")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")

    lines.append("## Approved inputs snapshot")
    lines.append(f"- Business name: {inputs.business_name or '[missing]'}")
    lines.append(f"- Website: {inputs.website or '[missing]'}")
    lines.append(f"- Phone: {inputs.phone or '[missing]'}")
    lines.append(f"- Email: {inputs.email or '[missing]'}")
    address_parts = [
        inputs.address.get("Line 1"),
        inputs.address.get("Line 2"),
        inputs.address.get("City"),
        inputs.address.get("State"),
        inputs.address.get("Postal code"),
        inputs.address.get("Country"),
    ]
    addr = ", ".join([part for part in address_parts if part]) or "[missing]"
    lines.append(f"- Address: {addr}")

    if inputs.hours:
        lines.append("- Hours:")
        for day, hours in inputs.hours.items():
            lines.append(f"  - {day}: {hours}")
    else:
        lines.append("- Hours: [missing]")

    if inputs.service_areas:
        lines.append("- Service areas:")
        for area in inputs.service_areas:
            lines.append(f"  - {area}")
    else:
        lines.append("- Service areas: [missing]")

    lines.append(f"- Short description: {inputs.short_description or '[missing]'}")
    lines.append(f"- Long description: {inputs.long_description or '[missing]'}")
    lines.append(f"- Keywords: {', '.join(inputs.keywords) if inputs.keywords else '[missing]'}")
    lines.append(f"- Price range: {inputs.price_range or '[missing]'}")
    lines.append(
        f"- Payment forms: {', '.join(inputs.payment_forms) if inputs.payment_forms else '[missing]'}"
    )
    if inputs.services:
        lines.append("- Services:")
        for svc in inputs.services:
            lines.append(f"  - {svc['name']}: {svc['description']}")
    else:
        lines.append("- Services: [missing]")
    if inputs.social:
        lines.append("- Social:")
        for name, url in inputs.social.items():
            lines.append(f"  - {name}: {url}")
    else:
        lines.append("- Social: [missing]")
    lines.append("")

    lines.append("## GBP update checklist")
    checklist_items = [
        "Verify business name",
        "Verify phone number",
        "Verify website URL",
        "Verify address and service area settings",
        "Verify hours and holiday hours",
        "Update categories (primary/secondary)",
        "Update attributes",
        "Update services list",
        "Update short description",
        "Update long description",
        "Update keywords",
        "Update price range",
        "Update payment methods",
        "Update photos/media",
        "Update products/offers (if any)",
        "Update social and appointment links",
    ]
    for item in checklist_items:
        suffix = " (needs approval)" if any(item.lower().startswith(token) for token in ["update categories", "update attributes", "update photos", "update products/offers"]) else ""
        lines.append(f"- [ ] {item}{suffix}")
    lines.append("")

    lines.append("## GBP posting plan")
    lines.append("- Cadence: [add approved cadence]")
    lines.append("- Offers: [add approved offers]")
    lines.append("")
    lines.append("| Post | Date | City/Area | Service | CTA | Asset | UTM |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in plan:
        lines.append(
            f"| {row['post']} | {row['date']} | {row['area']} | {row['service']} | {row['cta']} | {row['asset']} | {row['utm']} |"
        )
    lines.append("")

    lines.append("## Risk flags")
    if missing:
        for field in missing:
            lines.append(f"- Missing approval: {field}")
    else:
        lines.append("- None detected based on inputs file.")
    lines.append("")

    return "\n".join(lines)


def build_payload(inputs: ApprovedInputs, missing: list[str], plan: list[dict[str, str]]) -> dict:
    return {
        "generated_at": now_iso(),
        "inputs": asdict(inputs),
        "missing_approvals": missing,
        "post_plan": plan,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate GBP update checklist from approved inputs.")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    parser.add_argument(
        "--inputs",
        default=None,
        help="Optional path to inputs.md (default: outputs/<client>/inputs.md)",
    )
    args = parser.parse_args()

    base_dir = Path("outputs") / args.client_slug
    inputs_path = Path(args.inputs) if args.inputs else base_dir / "inputs.md"
    if not inputs_path.exists():
        raise SystemExit(f"Inputs file not found: {inputs_path}")

    inputs = parse_inputs(inputs_path)
    missing = missing_fields(inputs)
    plan = build_post_plan(inputs)

    report_dir = base_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    md_path = report_dir / "gbp-update-checklist.md"
    json_path = report_dir / "gbp-update-checklist.json"

    md_path.write_text(render_markdown(inputs, missing, plan), encoding="utf-8")
    json_path.write_text(json.dumps(build_payload(inputs, missing, plan), indent=2), encoding="utf-8")

    print(f"wrote {md_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
