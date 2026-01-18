#!/usr/bin/env python3
"""Validate JSON-LD against schema.org classes/properties."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


SCRIPT_RE = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>\s*(.*?)\s*</script>', re.S)


def to_schema_id(value: str) -> str:
    if value.startswith("schema:"):
        return value
    if value.startswith("http://schema.org/") or value.startswith("https://schema.org/"):
        return f"schema:{value.rsplit('/', 1)[-1]}"
    if ":" in value:
        return value
    return f"schema:{value}"


def load_jsonld(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    match = SCRIPT_RE.search(raw)
    if match:
        raw = match.group(1)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON-LD in {path}: {exc}") from exc


def load_schemaorg(path: Path) -> tuple[set[str], dict[str, set[str]], dict[str, set[str]], dict[str, set[str]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    classes: set[str] = set()
    properties: set[str] = set()
    parents: dict[str, set[str]] = defaultdict(set)
    domains: dict[str, set[str]] = defaultdict(set)
    ranges: dict[str, set[str]] = defaultdict(set)

    for node in data.get("@graph", []):
        node_id = node.get("@id")
        node_type = node.get("@type")
        if not node_id or not node_type:
            continue
        if node_type == "rdfs:Class":
            classes.add(node_id)
            sub = node.get("rdfs:subClassOf")
            if isinstance(sub, dict):
                parent = sub.get("@id")
                if parent:
                    parents[node_id].add(parent)
            elif isinstance(sub, list):
                for entry in sub:
                    if isinstance(entry, dict) and entry.get("@id"):
                        parents[node_id].add(entry["@id"])
        elif node_type == "rdf:Property":
            properties.add(node_id)
            domain = node.get("schema:domainIncludes")
            if isinstance(domain, dict):
                if domain.get("@id"):
                    domains[node_id].add(domain["@id"])
            elif isinstance(domain, list):
                for entry in domain:
                    if isinstance(entry, dict) and entry.get("@id"):
                        domains[node_id].add(entry["@id"])
            range_value = node.get("schema:rangeIncludes")
            if isinstance(range_value, dict):
                if range_value.get("@id"):
                    ranges[node_id].add(range_value["@id"])
            elif isinstance(range_value, list):
                for entry in range_value:
                    if isinstance(entry, dict) and entry.get("@id"):
                        ranges[node_id].add(entry["@id"])

    return classes, properties, parents, ranges, domains


def is_subclass(candidate: str, parent: str, parents: dict[str, set[str]]) -> bool:
    if candidate == parent:
        return True
    visited = set()
    stack = [candidate]
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        for ancestor in parents.get(current, set()):
            if ancestor == parent:
                return True
            stack.append(ancestor)
    return False


def is_range_match(value: Any, range_id: str, parents: dict[str, set[str]]) -> bool:
    if range_id in {"schema:Text", "schema:URL", "schema:Date", "schema:DateTime", "schema:Time", "schema:Duration"}:
        return isinstance(value, str)
    if range_id == "schema:Boolean":
        return isinstance(value, bool)
    if range_id == "schema:Integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if range_id == "schema:Number":
        return (isinstance(value, int) and not isinstance(value, bool)) or isinstance(value, float)
    if isinstance(value, dict):
        val_type = value.get("@type")
        if val_type:
            return is_subclass(to_schema_id(val_type), range_id, parents)
        if value.get("@id"):
            return True
    return False


def validate_graph(
    data: dict[str, Any],
    classes: set[str],
    properties: set[str],
    parents: dict[str, set[str]],
    ranges: dict[str, set[str]],
    domains: dict[str, set[str]],
    strict_range: bool,
) -> list[str]:
    errors: list[str] = []
    nodes = data.get("@graph")
    if nodes is None:
        nodes = [data]
    for node in nodes:
        if not isinstance(node, dict):
            errors.append("Top-level graph node is not an object.")
            continue
        node_types_raw = node.get("@type")
        if not node_types_raw:
            errors.append("Missing @type on graph node.")
            continue
        node_types = node_types_raw if isinstance(node_types_raw, list) else [node_types_raw]
        node_types = [to_schema_id(t) for t in node_types]
        for node_type in node_types:
            if node_type not in classes:
                errors.append(f"Unknown @type: {node_type}")

        for key, value in node.items():
            if key.startswith("@"):
                continue
            prop_id = to_schema_id(key)
            if prop_id not in properties:
                errors.append(f"Unknown property: {key}")
                continue
            domain_set = domains.get(prop_id)
            if domain_set:
                if not any(is_subclass(node_type, domain, parents) for node_type in node_types for domain in domain_set):
                    errors.append(f"Property '{key}' not in domain for {node_types_raw}")
            if strict_range:
                range_set = ranges.get(prop_id)
                if range_set:
                    values = value if isinstance(value, list) else [value]
                    for item in values:
                        if not any(is_range_match(item, range_id, parents) for range_id in range_set):
                            errors.append(f"Property '{key}' value fails rangeIncludes")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate JSON-LD against schema.org.")
    parser.add_argument("--schemaorg", default="downloaded_files/schemaorg-current-https.jsonld")
    parser.add_argument("--input", required=True, help="Path to JSON-LD file or HTML file containing JSON-LD.")
    parser.add_argument("--no-strict-range", action="store_true", help="Disable rangeIncludes checks.")
    args = parser.parse_args()

    schema_path = Path(args.schemaorg)
    if not schema_path.exists():
        raise SystemExit(f"schema.org file not found: {schema_path}")
    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    classes, properties, parents, ranges, domains = load_schemaorg(schema_path)
    data = load_jsonld(input_path)
    errors = validate_graph(
        data,
        classes,
        properties,
        parents,
        ranges,
        domains,
        strict_range=not args.no_strict_range,
    )
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        raise SystemExit(f"schema validation failed: {len(errors)} issue(s)")
    print("schema validation OK")


if __name__ == "__main__":
    main()
