#!/usr/bin/env python3
"""
Populate inputs.md from cached site HTML (data/outputs/<client>/reports/site-cache).
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SOCIAL_DOMAINS = {
    "facebook.com": "Facebook",
    "instagram.com": "Instagram",
    "linkedin.com": "LinkedIn",
    "x.com": "X",
    "twitter.com": "X",
}


@dataclass
class InputsDraft:
    name: str = ""
    business_type: str = ""
    website: str = ""
    phone: str = ""
    email: str = ""
    address_line1: str = ""
    address_line2: str = ""
    city: str = ""
    state: str = ""
    postal_code: str = ""
    country: str = ""
    hours: dict[str, str] = field(default_factory=dict)
    areas_served: list[str] = field(default_factory=list)
    short_description: str = ""
    long_description: str = ""
    keywords: list[str] = field(default_factory=list)
    price_range: str = ""
    payment_forms: list[str] = field(default_factory=list)
    social: dict[str, str] = field(default_factory=dict)
    services: list[str] = field(default_factory=list)


def load_index(index_path: Path) -> dict[str, dict[str, str]]:
    if not index_path.exists():
        return {}
    return json.loads(index_path.read_text(encoding="utf-8"))


def pick_cache_paths(index: dict[str, dict[str, str]]) -> list[Path]:
    urls = list(index.keys())
    if not urls:
        return []

    def score_url(url: str) -> tuple[int, int]:
        parsed = urlparse(url)
        path = parsed.path or "/"
        parts = [p for p in path.split("/") if p]
        return (0 if path in {"/", ""} else 1, len(parts))

    urls.sort(key=score_url)
    picks = [urls[0]]

    for url in urls:
        if "contact" in url.lower():
            picks.append(url)
            break

    return [Path(index[url]["path"]) for url in picks if url in index]


def load_html(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def iter_jsonld_objects(raw: Any) -> list[dict[str, Any]]:
    objs: list[dict[str, Any]] = []
    if isinstance(raw, dict):
        if "@graph" in raw and isinstance(raw["@graph"], list):
            for item in raw["@graph"]:
                objs.extend(iter_jsonld_objects(item))
        else:
            objs.append(raw)
    elif isinstance(raw, list):
        for item in raw:
            objs.extend(iter_jsonld_objects(item))
    return objs


def extract_jsonld(soup: Any) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    for tag in soup.find_all("script"):
        if tag.get("type") != "application/ld+json":
            continue
        try:
            payload = json.loads(tag.string or "")
        except Exception:
            continue
        objects.extend(iter_jsonld_objects(payload))
    return objects


def normalize_phone(value: str) -> str:
    return value.replace("\n", " ").strip()


def normalize_hours(value: str) -> dict[str, str]:
    hours: dict[str, str] = {}
    if isinstance(value, list):
        for entry in value:
            if not isinstance(entry, dict):
                continue
            day = entry.get("dayOfWeek")
            if isinstance(day, list):
                days = day
            else:
                days = [day] if day else []
            opens = entry.get("opens", "")
            closes = entry.get("closes", "")
            for d in days:
                label = str(d).split("/")[-1] if d else ""
                if label:
                    hours[label] = f"{opens} - {closes}".strip(" -")
    elif isinstance(value, str):
        hours["Note"] = value
    return hours


def extract_from_jsonld(objects: list[dict[str, Any]], draft: InputsDraft) -> None:
    for obj in objects:
        types = obj.get("@type")
        if isinstance(types, list):
            type_list = [t for t in types if isinstance(t, str)]
        elif isinstance(types, str):
            type_list = [types]
        else:
            type_list = []

        if any(t in {"LocalBusiness", "Organization"} for t in type_list):
            draft.name = draft.name or str(obj.get("name", "")).strip()
            draft.business_type = draft.business_type or next(
                (t for t in type_list if t not in {"LocalBusiness", "Organization"}), ""
            )
            draft.website = draft.website or str(obj.get("url", "")).strip()
            draft.phone = draft.phone or normalize_phone(str(obj.get("telephone", "")).strip())
            draft.email = draft.email or str(obj.get("email", "")).strip()
            description = str(obj.get("description", "")).strip()
            if description:
                draft.short_description = draft.short_description or description
                draft.long_description = draft.long_description or description

            address = obj.get("address") or {}
            if isinstance(address, dict):
                draft.address_line1 = draft.address_line1 or str(address.get("streetAddress", "")).strip()
                draft.city = draft.city or str(address.get("addressLocality", "")).strip()
                draft.state = draft.state or str(address.get("addressRegion", "")).strip()
                draft.postal_code = draft.postal_code or str(address.get("postalCode", "")).strip()
                draft.country = draft.country or str(address.get("addressCountry", "")).strip()

            area = obj.get("areaServed")
            if area and not draft.areas_served:
                if isinstance(area, list):
                    draft.areas_served = [str(a) for a in area if a]
                else:
                    draft.areas_served = [str(area)]

            hours = obj.get("openingHoursSpecification") or obj.get("openingHours")
            if hours and not draft.hours:
                draft.hours = normalize_hours(hours)

            same_as = obj.get("sameAs")
            if isinstance(same_as, list):
                for link in same_as:
                    if not isinstance(link, str):
                        continue
                    for domain, label in SOCIAL_DOMAINS.items():
                        if domain in link and label not in draft.social:
                            draft.social[label] = link

        if "makesOffer" in obj and not draft.services:
            offers = obj.get("makesOffer")
            names: list[str] = []
            if isinstance(offers, list):
                for offer in offers:
                    if isinstance(offer, dict):
                        item = offer.get("itemOffered", offer)
                        if isinstance(item, dict):
                            name = item.get("name")
                            if isinstance(name, str):
                                names.append(name)
            draft.services = names


def extract_from_html(soup: Any, draft: InputsDraft) -> None:
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    draft.name = draft.name or title

    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        desc = meta_desc["content"].strip()
        draft.short_description = draft.short_description or desc
        draft.long_description = draft.long_description or desc

    for meta in soup.find_all("meta", attrs={"property": "og:site_name"}):
        if meta.get("content") and not draft.name:
            draft.name = meta["content"].strip()

    for link in soup.select("a[href^='tel:']"):
        number = link.get("href", "").replace("tel:", "").strip()
        if number and not draft.phone:
            draft.phone = number

    for link in soup.select("a[href^='mailto:']"):
        email = link.get("href", "").replace("mailto:", "").strip()
        if email and not draft.email:
            draft.email = email

    for link in soup.select("a[href]"):
        href = link.get("href", "")
        for domain, label in SOCIAL_DOMAINS.items():
            if domain in href and label not in draft.social:
                draft.social[label] = href


def merge_missing(target: InputsDraft, source: InputsDraft) -> None:
    for field_name in target.__dataclass_fields__:
        value = getattr(target, field_name)
        source_value = getattr(source, field_name)
        if isinstance(value, dict):
            if not value:
                setattr(target, field_name, source_value)
        elif isinstance(value, list):
            if not value:
                setattr(target, field_name, source_value)
        else:
            if not value:
                setattr(target, field_name, source_value)


def format_inputs_md(client_name: str, draft: InputsDraft) -> str:
    hours = {day: draft.hours.get(day, "") for day in [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]}
    social = {
        "Facebook": draft.social.get("Facebook", ""),
        "Instagram": draft.social.get("Instagram", ""),
        "LinkedIn": draft.social.get("LinkedIn", ""),
        "X": draft.social.get("X", ""),
    }
    areas = draft.areas_served or [""]
    services = draft.services or [""]
    keywords = draft.keywords or [""]
    payment = draft.payment_forms or [""]

    lines = [
        f"# {client_name} - inputs.md",
        "",
        "Auto-populated from cached site HTML. Review and correct before use.",
        "",
        "## Approved business facts",
        "",
        f"- Business name: {draft.name}",
        f"- Business type (schema.org subtype, optional): {draft.business_type}",
        f"- Website: {draft.website}",
        f"- Phone: {draft.phone}",
        f"- Email: {draft.email}",
        "- Address:",
        f"  - Line 1: {draft.address_line1}",
        f"  - Line 2: {draft.address_line2}",
        f"  - City: {draft.city}",
        f"  - State: {draft.state}",
        f"  - Postal code: {draft.postal_code}",
        f"  - Country: {draft.country}",
        "- Hours:",
        f"  - Monday: {hours['Monday']}",
        f"  - Tuesday: {hours['Tuesday']}",
        f"  - Wednesday: {hours['Wednesday']}",
        f"  - Thursday: {hours['Thursday']}",
        f"  - Friday: {hours['Friday']}",
        f"  - Saturday: {hours['Saturday']}",
        f"  - Sunday: {hours['Sunday']}",
        "- Areas served (verified list):",
    ]
    lines.extend([f"  - {item}" for item in areas])
    lines.extend(
        [
            "",
            "## Approved profile details",
            "",
            f"- Short description: {draft.short_description}",
            f"- Long description: {draft.long_description}",
            f"- Keywords (approved list): {', '.join([k for k in keywords if k])}",
            f"- Price range: {draft.price_range}",
            f"- Payment forms: {', '.join([p for p in payment if p])}",
            "- Social:",
            f"  - Facebook: {social['Facebook']}",
            f"  - Instagram: {social['Instagram']}",
            f"  - LinkedIn: {social['LinkedIn']}",
            f"  - X: {social['X']}",
            "",
            "## Approved service list (descriptions)",
            "",
        ]
    )
    lines.extend([f"- Service: {item}" for item in services])
    lines.extend(
        [
            "",
            "## Placeholder (needs approved inputs)",
            "",
            "- Geo latitude:",
            "- Geo longitude:",
            "- Proof points (with sources):",
            "",
        ]
    )
    return "\n".join(lines)


def should_overwrite(path: Path, force: bool) -> bool:
    if force:
        return True
    if not path.exists():
        return True
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return True
    lines = [line for line in content.splitlines() if line.strip()]
    if len(lines) <= 2 and "inputs.md" in lines[0].lower():
        return True
    if "Approved business facts" not in content and len(lines) < 5:
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Populate inputs.md from cached site HTML.")
    parser.add_argument("--client-slug", required=True, help="Client slug under data/outputs/")
    parser.add_argument("--client-name", help="Client display name (defaults to slug)")
    parser.add_argument("--base-dir", default="data/outputs", help="Base outputs directory")
    parser.add_argument("--force", action="store_true", help="Overwrite inputs.md even if non-empty")
    args = parser.parse_args()

    client_name = args.client_name or args.client_slug
    base_dir = Path(args.base_dir)
    cache_dir = base_dir / args.client_slug / "reports" / "site-cache"
    index_path = cache_dir / "index.json"
    index = load_index(index_path)
    if not index:
        raise SystemExit("No site cache index found. Run crawl_cache.py first.")

    try:
        from bs4 import BeautifulSoup  # type: ignore
    except Exception:
        raise SystemExit("BeautifulSoup is required. Install bs4 before running this script.")

    draft = InputsDraft()
    paths = pick_cache_paths(index)
    for path in paths:
        html = load_html(path)
        soup = BeautifulSoup(html, "html.parser")
        objects = extract_jsonld(soup)
        page_draft = InputsDraft()
        extract_from_jsonld(objects, page_draft)
        extract_from_html(soup, page_draft)
        merge_missing(draft, page_draft)

    if not draft.website and paths:
        for url in index.keys():
            parsed = urlparse(url)
            if parsed.path in {"", "/"}:
                draft.website = url
                break

    inputs_path = base_dir / args.client_slug / "inputs.md"
    if not should_overwrite(inputs_path, args.force):
        print(f"inputs.md already populated: {inputs_path}")
        return

    content = format_inputs_md(client_name, draft)
    inputs_path.write_text(content, encoding="utf-8")
    print(f"Wrote inputs.md to {inputs_path}")


if __name__ == "__main__":
    main()
