#!/usr/bin/env python3
"""Generate JSON-LD schema scripts from cached HTML pages.

Reads outputs/<client>/reports/site-cache/index.json and writes one JSON-LD
<script> tag per page under outputs/<client>/gen-schema/website-tree/.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

try:
    from geopy.geocoders import Nominatim
except ImportError:  # optional dependency
    Nominatim = None


FAQ_QUESTION_RE = re.compile(r"\?$|^(how|what|when|where|why|do|does|is|can|should|will|are)\b", re.I)
INVALID_CHARREF_RE = re.compile(r"&#(?!\d+;|x[0-9a-fA-F]+;)")
PHONEISH_RE = re.compile(r"^\+?[\d\-\.\s\(\)]+$")
TIME_RANGE_RE = re.compile(
    r"(?P<start>\d{1,2})(?::(?P<start_min>\d{2}))?\s*(?P<start_ampm>AM|PM)\s*[-–—]\s*"
    r"(?P<end>\d{1,2})(?::(?P<end_min>\d{2}))?\s*(?P<end_ampm>AM|PM)",
    re.I,
)
HTML_EXTENSIONS = {".html", ".htm", ".php", ""}


@dataclass
class PageSignals:
    url: str
    canonical_url: str
    title: str
    h1: str
    meta_description: str
    og_title: str
    og_description: str
    og_image: str
    og_type: str
    twitter_title: str
    twitter_description: str
    twitter_image: str
    site_name: str
    lang: str
    published_time: str
    modified_time: str
    faqs: list[tuple[str, str]]


@dataclass
class ApprovedInputs:
    business_name: str = ""
    website: str = ""
    phone: str = ""
    email: str = ""
    address: dict[str, str] = field(default_factory=dict)
    hours: dict[str, str] = field(default_factory=dict)
    service_areas: list[str] = field(default_factory=list)
    short_description: str = ""
    long_description: str = ""
    keywords: list[str] = field(default_factory=list)
    price_range: str = ""
    payment_forms: list[str] = field(default_factory=list)
    social: dict[str, str] = field(default_factory=dict)
    services: list[dict[str, str]] = field(default_factory=list)


@dataclass
class EntityRegistry:
    website: dict[str, Any]
    organization: dict[str, Any] | None
    local_business: dict[str, Any] | None
    services: list[dict[str, str]] = field(default_factory=list)
    logo_url: str = ""
    geo: dict[str, Any] | None = None


def load_cache(index_path: Path) -> dict[str, Path]:
    data = json.loads(index_path.read_text(encoding="utf-8"))
    return {url: Path(meta["path"]) for url, meta in data.items()}


def clean_value(value: str) -> str:
    cleaned = value.strip()
    if cleaned.startswith("[") and cleaned.endswith("]"):
        return ""
    return cleaned


def split_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def sanitize_html(markup: str) -> str:
    return INVALID_CHARREF_RE.sub("&amp;#", markup)


def read_html(path: Path, url: str) -> str | None:
    raw = path.read_bytes()
    if b"\x00" in raw:
        print(f"skip non-text content (null bytes): {url} -> {path}", file=sys.stderr)
        return None
    text = raw.decode("utf-8", errors="replace")
    return sanitize_html(text)


def extract_logo_url(soup: BeautifulSoup, base_url: str, business_name: str) -> str:
    candidates: list[tuple[int, str]] = []
    business_name = business_name.lower()
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
        if not src:
            continue
        alt = " ".join(img.get("alt", "").split()).lower()
        classes = " ".join(img.get("class", [])).lower()
        ident = " ".join([alt, classes, (img.get("id") or "").lower()])
        score = 0
        if "logo" in ident or "logo" in src.lower():
            score += 2
        if business_name and business_name in alt:
            score += 2
        if score:
            candidates.append((score, src))
    if candidates:
        candidates.sort(key=lambda item: item[0], reverse=True)
        return ensure_absolute(candidates[0][1], base_url)
    meta_logo = soup.find("meta", property="og:logo")
    if meta_logo and meta_logo.get("content"):
        return ensure_absolute(meta_logo["content"], base_url)
    return ""


def normalize_site_url(url: str) -> str:
    if not url:
        return ""
    if not re.match(r"^https?://", url, re.I):
        url = f"https://{url}"
    parsed = urlparse(url)
    if not parsed.netloc:
        return url
    return f"{parsed.scheme}://{parsed.netloc}/"


def parse_inputs_md(inputs_path: Path) -> ApprovedInputs | None:
    if not inputs_path.exists():
        return None
    inputs = ApprovedInputs()
    current_block = ""
    in_services = False
    for raw in inputs_path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line:
            continue
        if line.startswith("## "):
            current_block = ""
            in_services = "Approved service list" in line
            continue
        if line.startswith("- Address:"):
            current_block = "address"
            continue
        if line.startswith("- Hours:"):
            current_block = "hours"
            continue
        if line.startswith("- Areas served"):
            current_block = "service_areas"
            continue
        if line.startswith("- Social:"):
            current_block = "social"
            continue
        if line.startswith("- Business name:"):
            inputs.business_name = clean_value(line.split(":", 1)[1])
        elif line.startswith("- Website:"):
            inputs.website = clean_value(line.split(":", 1)[1])
        elif line.startswith("- Phone:"):
            inputs.phone = clean_value(line.split(":", 1)[1])
        elif line.startswith("- Email:"):
            inputs.email = clean_value(line.split(":", 1)[1])
        elif line.startswith("- Short description:"):
            inputs.short_description = clean_value(line.split(":", 1)[1])
        elif line.startswith("- Long description:"):
            inputs.long_description = clean_value(line.split(":", 1)[1])
        elif line.startswith("- Keywords"):
            raw_value = clean_value(line.split(":", 1)[1])
            inputs.keywords = [item for item in split_list(raw_value) if item]
        elif line.startswith("- Price range:"):
            inputs.price_range = clean_value(line.split(":", 1)[1])
        elif line.startswith("- Payment forms:"):
            raw_value = clean_value(line.split(":", 1)[1])
            inputs.payment_forms = [item for item in split_list(raw_value) if item]
        elif line.startswith("  - ") and current_block in {"address", "hours", "service_areas", "social"}:
            entry = line[4:]
            if current_block == "service_areas":
                value = clean_value(entry)
                if value:
                    inputs.service_areas.append(value)
            else:
                if ":" not in entry:
                    continue
                key, value = entry.split(":", 1)
                value = clean_value(value)
                if not value:
                    continue
                if current_block == "address":
                    inputs.address[key.strip()] = value
                elif current_block == "hours":
                    inputs.hours[key.strip()] = value
                elif current_block == "social":
                    inputs.social[key.strip()] = value
        elif in_services and line.startswith("- "):
            entry = line[2:]
            if ":" not in entry:
                continue
            name, desc = entry.split(":", 1)
            name = clean_value(name)
            desc = clean_value(desc)
            if name:
                inputs.services.append({"name": name, "description": desc})
    return inputs


def load_gbp_inputs(base_dir: Path) -> ApprovedInputs | None:
    report_path = base_dir / "reports" / "gbp-update-checklist.json"
    if not report_path.exists():
        return None
    data = json.loads(report_path.read_text(encoding="utf-8"))
    raw_inputs = data.get("inputs", {})
    inputs = ApprovedInputs()
    inputs.business_name = clean_value(str(raw_inputs.get("business_name", "")))
    inputs.website = clean_value(str(raw_inputs.get("website", "")))
    inputs.phone = clean_value(str(raw_inputs.get("phone", "")))
    inputs.email = clean_value(str(raw_inputs.get("email", "")))
    inputs.address = {k: clean_value(str(v)) for k, v in raw_inputs.get("address", {}).items() if clean_value(str(v))}
    inputs.hours = {k: clean_value(str(v)) for k, v in raw_inputs.get("hours", {}).items() if clean_value(str(v))}
    inputs.service_areas = [clean_value(str(v)) for v in raw_inputs.get("service_areas", []) if clean_value(str(v))]
    inputs.short_description = clean_value(str(raw_inputs.get("short_description", "")))
    inputs.long_description = clean_value(str(raw_inputs.get("long_description", "")))
    inputs.keywords = [clean_value(str(v)) for v in raw_inputs.get("keywords", []) if clean_value(str(v))]
    inputs.price_range = clean_value(str(raw_inputs.get("price_range", "")))
    inputs.payment_forms = [clean_value(str(v)) for v in raw_inputs.get("payment_forms", []) if clean_value(str(v))]
    inputs.social = {k: clean_value(str(v)) for k, v in raw_inputs.get("social", {}).items() if clean_value(str(v))}
    inputs.services = [
        {"name": clean_value(str(svc.get("name", ""))), "description": clean_value(str(svc.get("description", "")))}
        for svc in raw_inputs.get("services", [])
        if clean_value(str(svc.get("name", "")))
    ]
    return inputs


def load_inputs(base_dir: Path) -> ApprovedInputs | None:
    return load_gbp_inputs(base_dir) or parse_inputs_md(base_dir / "inputs.md")


def to_24_hour(hour: int, minute: int, ampm: str) -> str:
    ampm = ampm.lower()
    hour = hour % 12
    if ampm == "pm":
        hour += 12
    return f"{hour:02d}:{minute:02d}"


def parse_opening_hours(hours: dict[str, str]) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for day, value in hours.items():
        if not value or value.lower().startswith("closed"):
            continue
        match = TIME_RANGE_RE.search(value)
        if not match:
            continue
        start = int(match.group("start"))
        start_min = int(match.group("start_min") or 0)
        end = int(match.group("end"))
        end_min = int(match.group("end_min") or 0)
        opens = to_24_hour(start, start_min, match.group("start_ampm"))
        closes = to_24_hour(end, end_min, match.group("end_ampm"))
        specs.append(
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": day,
                "opens": opens,
                "closes": closes,
            }
        )
    return specs


def format_street_address(address: dict[str, str]) -> str:
    line1 = address.get("Line 1", "")
    line2 = address.get("Line 2", "")
    return ", ".join([part for part in [line1, line2] if part])


def format_address_line(address: dict[str, str]) -> str:
    parts = [
        format_street_address(address),
        address.get("City", ""),
        address.get("State", ""),
        address.get("Postal code", ""),
        address.get("Country", ""),
    ]
    return ", ".join([part for part in parts if part])


def load_geo_cache(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_geo_cache(path: Path, cache: dict[str, dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def geocode_address(address: str) -> dict[str, Any] | None:
    if not Nominatim:
        return None
    geocoder = Nominatim(user_agent="codex-schema-generator", timeout=10)
    location = geocoder.geocode(address)
    if not location:
        return None
    try:
        lat = float(location.latitude)
        lon = float(location.longitude)
    except (TypeError, ValueError):
        return None
    return {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon}


def resolve_geo(
    inputs: ApprovedInputs | None,
    cache_path: Path,
    enable_geocode: bool,
) -> dict[str, Any] | None:
    if not inputs:
        return None
    address = inputs.address
    if not address:
        return None
    address_text = format_address_line(address)
    if not address_text:
        return None
    variants = [address_text]
    if address.get("Line 2"):
        line2 = address.get("Line 2")
        address_no_line2 = ", ".join(
            part
            for part in [
                address.get("Line 1", ""),
                address.get("City", ""),
                address.get("State", ""),
                address.get("Postal code", ""),
                address.get("Country", ""),
            ]
            if part
        )
        if address_no_line2 and address_no_line2 not in variants:
            variants.append(address_no_line2)
        if line2:
            address_with_unit = address_no_line2.replace(address.get("Line 1", ""), f"{address.get('Line 1', '')} Unit {line2}")
            if address_with_unit and address_with_unit not in variants:
                variants.append(address_with_unit)
    city_state = ", ".join(
        part
        for part in [
            address.get("City", ""),
            address.get("State", ""),
            address.get("Postal code", ""),
            address.get("Country", ""),
        ]
        if part
    )
    if city_state and city_state not in variants:
        variants.append(city_state)

    cache = load_geo_cache(cache_path)
    for variant in variants:
        if variant in cache:
            return cache[variant]
    if not enable_geocode:
        return None
    for variant in variants:
        geo = geocode_address(variant)
        if geo:
            cache[variant] = geo
            cache[address_text] = geo
            save_geo_cache(cache_path, cache)
            return geo
        print(f"geocode failed for: {variant}", file=sys.stderr)
    return None


def build_entity_registry(
    site_url: str,
    inputs: ApprovedInputs | None,
    logo_url: str,
    geo: dict[str, Any] | None,
) -> EntityRegistry:
    website_id = f"{site_url}#website" if site_url else "#website"
    org_id = f"{site_url}#organization" if site_url else "#organization"
    local_id = f"{site_url}#localbusiness" if site_url else "#localbusiness"

    org_name = inputs.business_name if inputs else ""
    website_name = org_name

    website: dict[str, Any] = {
        "@type": "WebSite",
        "@id": website_id,
        "url": site_url or None,
        "name": website_name or None,
        "description": (inputs.short_description if inputs and inputs.short_description else None),
        "publisher": {"@id": org_id} if org_name else None,
    }

    organization = None
    local_business = None
    services: list[dict[str, str]] = []
    postal_address = None
    if org_name:
        address = inputs.address if inputs else {}
        if address:
            postal_address = {
                "@type": "PostalAddress",
                "streetAddress": format_street_address(address),
                "addressLocality": address.get("City"),
                "addressRegion": address.get("State"),
                "postalCode": address.get("Postal code"),
                "addressCountry": address.get("Country"),
            }
        organization = {
            "@type": "Organization",
            "@id": org_id,
            "name": org_name,
            "url": site_url or None,
            "telephone": inputs.phone if inputs and inputs.phone else None,
            "email": inputs.email if inputs and inputs.email else None,
            "description": (inputs.long_description if inputs and inputs.long_description else None),
            "sameAs": list(inputs.social.values()) if inputs and inputs.social else None,
            "address": postal_address,
            "image": logo_url or None,
        }
        areas = [area for area in inputs.service_areas if area] if inputs else []
        if inputs:
            for svc in inputs.services:
                name = svc.get("name") or ""
                if not name:
                    continue
                services.append(
                    {
                        "name": name,
                        "description": svc.get("description") or "",
                    }
                )
        local_business = {
            "@type": ["HVACBusiness", "LocalBusiness"],
            "@id": local_id,
            "name": org_name,
            "url": site_url or None,
            "telephone": inputs.phone if inputs and inputs.phone else None,
            "priceRange": inputs.price_range if inputs and inputs.price_range else None,
            "paymentAccepted": inputs.payment_forms if inputs and inputs.payment_forms else None,
            "address": postal_address,
            "areaServed": areas if areas else None,
            "openingHoursSpecification": parse_opening_hours(inputs.hours) if inputs else None,
            "geo": geo,
            "sameAs": list(inputs.social.values()) if inputs and inputs.social else None,
            "description": (inputs.long_description if inputs and inputs.long_description else None),
            "parentOrganization": {"@id": org_id} if organization else None,
            "image": logo_url or None,
        }

    return EntityRegistry(
        website=website,
        organization=organization,
        local_business=local_business,
        services=services,
        logo_url=logo_url,
        geo=geo,
    )


def hydrate_registry_names(registry: EntityRegistry, fallback_name: str) -> None:
    if not fallback_name:
        return
    if not registry.website.get("name"):
        registry.website["name"] = fallback_name
    if registry.organization and not registry.organization.get("name"):
        registry.organization["name"] = fallback_name
    if registry.local_business and not registry.local_business.get("name"):
        registry.local_business["name"] = fallback_name


def normalize_title(text: str) -> str:
    return " ".join(text.split()).strip()


def is_title_candidate(value: str) -> bool:
    cleaned = normalize_title(value)
    if not cleaned:
        return False
    if cleaned.lower().startswith("tel:"):
        return False
    if PHONEISH_RE.fullmatch(cleaned):
        return False
    if not any(ch.isalpha() for ch in cleaned):
        return False
    return len(cleaned) >= 3


def slugify(value: str) -> str:
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in value)
    slug = "-".join(part for part in slug.split("-") if part)
    return slug


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(value)
    return out


def extract_meta_values(soup: BeautifulSoup) -> dict[str, str]:
    values: dict[str, str] = {}
    for tag in soup.find_all("meta"):
        content = tag.get("content", "").strip()
        if not content:
            continue
        prop = tag.get("property")
        name = tag.get("name")
        if prop and prop not in values:
            values[prop] = content
        if name and name not in values:
            values[name] = content
    return values


def extract_canonical(soup: BeautifulSoup) -> str:
    link = soup.find("link", rel="canonical")
    if link and link.get("href"):
        return link["href"].strip()
    return ""


def extract_h1(soup: BeautifulSoup) -> str:
    h1_tag = soup.find("h1")
    if h1_tag:
        return " ".join(h1_tag.stripped_strings)
    return ""


def extract_faqs(soup: BeautifulSoup) -> list[tuple[str, str]]:
    faqs: list[tuple[str, str]] = []
    for el in soup.find_all(["h2", "h3", "h4", "button", "summary", "p", "div"]):
        question = " ".join(el.stripped_strings)
        if not question.endswith("?"):
            continue
        if len(question) < 6 or len(question) > 200:
            continue
        if not FAQ_QUESTION_RE.search(question):
            continue
        answer = None
        sibling = el.find_next_sibling()
        if sibling:
            sib_text = " ".join(sibling.stripped_strings)
            if sib_text and len(sib_text) > 10:
                answer = sib_text
        if not answer:
            parent = el.parent
            if parent:
                found = False
                for child in parent.find_all(recursive=False):
                    if child == el:
                        found = True
                        continue
                    if found:
                        ctext = " ".join(child.stripped_strings)
                        if ctext and len(ctext) > 10:
                            answer = ctext
                            break
        if answer:
            faqs.append((question.strip(), answer.strip()))
    seen = set()
    deduped = []
    for question, answer in faqs:
        key = question.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append((question, answer))
    return deduped


def parse_page(html: str, url: str) -> PageSignals:
    soup = BeautifulSoup(html, "html.parser")
    title = normalize_title(soup.title.get_text()) if soup.title else ""
    h1 = normalize_title(extract_h1(soup))
    meta_values = extract_meta_values(soup)
    meta_description = meta_values.get("description", "")
    og_title = meta_values.get("og:title", "")
    og_description = meta_values.get("og:description", "")
    og_image = meta_values.get("og:image", "")
    og_type = meta_values.get("og:type", "")
    twitter_title = meta_values.get("twitter:title", "")
    twitter_description = meta_values.get("twitter:description", "")
    twitter_image = meta_values.get("twitter:image", "")
    site_name = meta_values.get("og:site_name", "")
    lang = soup.html.get("lang", "").strip() if soup.html else ""
    published_time = meta_values.get("article:published_time", "")
    modified_time = meta_values.get("article:modified_time", "") or meta_values.get("og:updated_time", "")
    canonical_url = extract_canonical(soup)
    return PageSignals(
        url=url,
        canonical_url=canonical_url,
        title=title,
        h1=h1,
        meta_description=meta_description,
        og_title=og_title,
        og_description=og_description,
        og_image=og_image,
        og_type=og_type,
        twitter_title=twitter_title,
        twitter_description=twitter_description,
        twitter_image=twitter_image,
        site_name=site_name,
        lang=lang,
        published_time=published_time,
        modified_time=modified_time,
        faqs=extract_faqs(soup),
    )


def build_breadcrumbs(page_url: str) -> list[dict[str, Any]]:
    parsed = urlparse(page_url)
    base = f"{parsed.scheme}://{parsed.netloc}/"
    segments = [seg for seg in parsed.path.split("/") if seg]
    items: list[dict[str, Any]] = []
    position = 1
    items.append(
        {
            "@type": "ListItem",
            "position": position,
            "name": "Home",
            "item": base,
        }
    )
    position += 1
    current = base
    for seg in segments:
        current = urljoin(current, f"{seg}/")
        name = seg.replace("-", " ").replace("_", " ").title()
        items.append(
            {
                "@type": "ListItem",
                "position": position,
                "name": name,
                "item": current,
            }
        )
        position += 1
    return items


def prune_empty(value: Any) -> Any:
    if isinstance(value, dict):
        cleaned = {k: prune_empty(v) for k, v in value.items()}
        return {k: v for k, v in cleaned.items() if v not in ("", None, [], {})}
    if isinstance(value, list):
        cleaned_list = [prune_empty(item) for item in value]
        return [item for item in cleaned_list if item not in ("", None, [], {})]
    return value


def ensure_absolute(url: str, base_url: str) -> str:
    if not url:
        return ""
    return urljoin(base_url, url)


def match_service_for_url(page_url: str, services: list[dict[str, str]]) -> dict[str, str] | None:
    path = urlparse(page_url).path.strip("/").lower()
    if path.endswith(".html"):
        path = path[:-5]
    best = None
    best_len = 0
    for svc in services:
        slug = slugify(svc.get("name", ""))
        if not slug:
            continue
        if slug in path and len(slug) > best_len:
            best = svc
            best_len = len(slug)
    return best


def build_offers(services: list[dict[str, str]]) -> list[dict[str, Any]]:
    offers: list[dict[str, Any]] = []
    for svc in services:
        name = svc.get("name") or ""
        if not name:
            continue
        offers.append(
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": name,
                    "description": svc.get("description") or None,
                },
            }
        )
    return offers


def choose_titles(signals: PageSignals) -> tuple[str, list[str]]:
    candidates = dedupe(
        [
            signals.title,
            signals.h1,
            signals.og_title,
            signals.twitter_title,
        ]
    )
    candidates = [value for value in candidates if is_title_candidate(value)]
    if not candidates:
        fallback = urlparse(signals.url).path.strip("/") or "Homepage"
        return fallback.replace("-", " ").title(), []
    primary = candidates[0]
    alternates = candidates[1:]
    return primary, alternates


def generate_schema(signals: PageSignals, registry: EntityRegistry) -> dict[str, Any]:
    raw_url = signals.canonical_url or signals.url
    parsed = urlparse(raw_url)
    page_url = parsed._replace(query="", fragment="").geturl()
    site_url = registry.website.get("url") or f"{parsed.scheme}://{parsed.netloc}/"
    page_id = page_url.rstrip("/") or page_url
    webpage_id = f"{page_id}#webpage"
    website_id = registry.website.get("@id") or f"{site_url}#website"
    org_id = None
    if registry.organization:
        org_id = registry.organization.get("@id")
    local_business_id = None
    if registry.local_business:
        local_business_id = registry.local_business.get("@id")
    primary_title, alternate_titles = choose_titles(signals)
    description = signals.meta_description or signals.og_description or signals.twitter_description
    image_url = ensure_absolute(signals.og_image or signals.twitter_image, page_url)
    image_id = f"{page_id}#primaryimage" if image_url else ""
    breadcrumbs = build_breadcrumbs(page_url)
    breadcrumb_id = f"{page_id}#breadcrumb"

    graph: list[dict[str, Any]] = []

    site_name = signals.site_name or primary_title
    hydrate_registry_names(registry, site_name)
    website = dict(registry.website)
    website["@id"] = website_id
    website["url"] = site_url
    site_alternates = dedupe(
        [signals.site_name] if signals.site_name and signals.site_name != website.get("name") else []
    )
    website["alternateName"] = site_alternates if site_alternates else None
    graph.append(website)

    if registry.organization:
        organization = dict(registry.organization)
        organization["@id"] = org_id
        organization["url"] = site_url
        graph.append(organization)

    if registry.local_business:
        local_business = dict(registry.local_business)
        local_business["@id"] = local_business_id
        local_business["url"] = site_url
        if registry.services:
            path = urlparse(page_url).path.strip("/").lower()
            if path.endswith(".html"):
                path = path[:-5]
            is_home = path in {"", "index", "home", "home-new"}
            matched = match_service_for_url(page_url, registry.services)
            if matched:
                local_business["makesOffer"] = build_offers([matched])
            elif is_home:
                local_business["makesOffer"] = build_offers(registry.services)
        graph.append(local_business)

    if image_url:
        graph.append(
            {
                "@type": "ImageObject",
                "@id": image_id,
                "url": image_url,
                "contentUrl": image_url,
                "caption": primary_title,
            }
        )

    graph.append(
        {
            "@type": "BreadcrumbList",
            "@id": breadcrumb_id,
            "itemListElement": breadcrumbs,
        }
    )

    webpage = {
        "@type": "WebPage",
        "@id": webpage_id,
        "url": page_url,
        "name": primary_title,
        "alternateName": alternate_titles if alternate_titles else None,
        "description": description,
        "inLanguage": signals.lang or None,
        "isPartOf": {"@id": website_id},
        "about": {"@id": local_business_id} if local_business_id else None,
        "primaryImageOfPage": {"@id": image_id} if image_id else None,
        "breadcrumb": {"@id": breadcrumb_id},
        "datePublished": signals.published_time or None,
        "dateModified": signals.modified_time or None,
    }
    graph.append(webpage)

    is_article = signals.og_type.lower() == "article" if signals.og_type else False
    if is_article:
        graph.append(
            {
                "@type": "Article",
                "@id": f"{page_id}#article",
                "headline": primary_title,
                "description": description,
                "datePublished": signals.published_time or None,
                "dateModified": signals.modified_time or None,
                "mainEntityOfPage": {"@id": webpage_id},
                "publisher": {"@id": org_id} if org_id else ({"@id": local_business_id} if local_business_id else None),
                "image": {"@id": image_id} if image_id else None,
            }
        )

    if signals.faqs:
        graph.append(
            {
                "@type": "FAQPage",
                "@id": f"{page_id}#faq",
                "url": page_url,
                "isPartOf": {"@id": website_id},
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {"@type": "Answer", "text": answer},
                    }
                    for question, answer in signals.faqs
                ],
            }
        )

    data = {
        "@context": "https://schema.org",
        "@graph": graph,
    }
    return prune_empty(data)


def output_path_for(url: str, out_dir: Path) -> Path:
    parsed = urlparse(url)._replace(query="", fragment="")
    path = parsed.path
    if not path or path.endswith("/"):
        relative = Path(path.lstrip("/")) / "index.html"
    else:
        relative = Path(path.lstrip("/"))
        if not relative.suffix:
            relative = relative.with_suffix(".html")
    return out_dir / relative


def render_script(schema: dict[str, Any]) -> str:
    payload = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
    return f'<script type="application/ld+json">\n{payload}\n</script>\n'


def should_skip_url(url: str) -> bool:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix and suffix not in HTML_EXTENSIONS:
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate JSON-LD schema scripts from cache.")
    parser.add_argument("--client-slug", required=True, help="Client slug under outputs/")
    parser.add_argument(
        "--output-dir",
        help="Optional output directory (default: outputs/<client>/gen-schema/website-tree)",
    )
    parser.add_argument(
        "--geocode",
        action="store_true",
        help="Enable geopy geocoding for LocalBusiness geo coordinates.",
    )
    args = parser.parse_args()

    client_dir = Path("outputs") / args.client_slug
    cache_dir = client_dir / "reports" / "site-cache"
    index_path = cache_dir / "index.json"
    if not index_path.exists():
        raise SystemExit(f"Cache index not found: {index_path}")

    out_dir = (
        Path(args.output_dir)
        if args.output_dir
        else Path("outputs") / args.client_slug / "gen-schema" / "website-tree"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    cache = load_cache(index_path)
    inputs = load_inputs(client_dir)
    seed_url = inputs.website if inputs else ""
    if not seed_url and cache:
        seed_url = next(iter(cache.keys()))
    site_url = normalize_site_url(seed_url)
    homepage_url = site_url or seed_url
    homepage_path = None
    if homepage_url:
        homepage_path = cache.get(homepage_url)
        if not homepage_path and homepage_url.endswith("/"):
            homepage_path = cache.get(homepage_url.rstrip("/"))
    logo_url = ""
    if homepage_path and homepage_path.exists():
        html = read_html(homepage_path, homepage_url)
        if html:
            soup = BeautifulSoup(html, "html.parser")
            logo_url = extract_logo_url(soup, homepage_url, inputs.business_name if inputs else "")
    geo = resolve_geo(
        inputs,
        client_dir / "reports" / "geocoded.json",
        enable_geocode=bool(args.geocode),
    )
    registry = build_entity_registry(site_url, inputs, logo_url, geo)
    for url, path in cache.items():
        if should_skip_url(url):
            print(f"skip non-html url: {url}", file=sys.stderr)
            continue
        if not path.exists():
            continue
        html = read_html(path, url)
        if not html:
            continue
        try:
            signals = parse_page(html, url)
        except Exception as exc:
            print(f"skip malformed html: {url} -> {path} ({exc})", file=sys.stderr)
            continue
        schema = generate_schema(signals, registry)
        out_path = output_path_for(signals.canonical_url or url, out_dir)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_script(schema), encoding="utf-8")
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
