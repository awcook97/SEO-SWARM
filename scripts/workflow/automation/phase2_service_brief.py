#!/usr/bin/env python3
"""Phase 2: Service Page Content Brief Auto-Generator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .base import ProgramConfig, ProgramInputs, ProgramRunner
from .io_utils import pick_value, read_csv
from .report_templates import render_list, render_section, render_table


@dataclass
class CrawlSnapshot:
    rows: list[dict[str, str]]
    service: str | None = None

    @classmethod
    def import_csv(cls, path: Path) -> "CrawlSnapshot":
        return cls(read_csv(path))

    def set_service(self, service: str) -> None:
        self.service = service.strip().lower()

    def get_pages(self) -> list[dict[str, str]]:
        return self.rows

    def get_page(self, url: str) -> dict[str, str] | None:
        if not url:
            return None
        for row in self.rows:
            if pick_value(row, ("url", "page")) == url:
                return row
        return None

    def get_pages_by_service(self) -> list[dict[str, str]]:
        if not self.service:
            return self.rows
        return [
            row
            for row in self.rows
            if self.service in pick_value(row, ("url", "page")).lower()
        ]

    def get_titles(self) -> list[str]:
        return [pick_value(row, ("title", "page_title")) for row in self.get_pages_by_service()]

    def get_meta_descriptions(self) -> list[str]:
        return [pick_value(row, ("meta_description", "description")) for row in self.get_pages_by_service()]


class ContentGapAnalyzer:
    def __init__(self) -> None:
        self.pages: list[dict[str, str]] = []

    def set_pages(self, pages: list[dict[str, str]]) -> None:
        self.pages = pages

    def get_missing_sections(self) -> list[str]:
        missing = []
        for section in ("pricing", "faqs", "service areas", "testimonials"):
            if not self._section_present(section):
                missing.append(section)
        return missing

    def get_thin_content_pages(self) -> list[dict[str, str]]:
        return [row for row in self.pages if self._word_count(row) < 300]

    def get_priority_gaps(self) -> list[str]:
        gaps = self.get_missing_sections()
        if self.get_thin_content_pages():
            gaps.append("expand thin pages")
        return gaps

    def _section_present(self, section: str) -> bool:
        for row in self.pages:
            body = pick_value(row, ("text", "body", "content"))
            if section in body.lower():
                return True
        return False

    def _word_count(self, row: dict[str, str]) -> int:
        body = pick_value(row, ("text", "body", "content"))
        return len(body.split()) if body else 0


class OutlineBuilder:
    def __init__(self) -> None:
        self.service = ""
        self.gaps: list[str] = []

    def set_service(self, service: str) -> None:
        self.service = service

    def set_gaps(self, gaps: list[str]) -> None:
        self.gaps = gaps

    def get_outline(self) -> list[str]:
        return [
            f"H1: {self.service} Services",
            "H2: Service Overview",
            "H2: Common Problems We Solve",
            "H2: Our Process",
            "H2: Pricing & Financing",
            "H2: FAQs",
        ]

    def get_required_sections(self) -> list[str]:
        base = ["overview", "benefits", "process", "pricing", "faqs", "service areas"]
        return sorted(set(base + self.gaps))

    def get_cta_notes(self) -> list[str]:
        return ["Add prominent phone CTA", "Include booking form above the fold"]


class SchemaChecklist:
    def __init__(self) -> None:
        self.service = ""

    def set_service(self, service: str) -> None:
        self.service = service

    def get_required_schema(self) -> list[str]:
        return ["Service", "LocalBusiness", "FAQPage"]

    def get_schema_notes(self) -> list[str]:
        return [f"Use '{self.service}' as the Service name", "Include areaServed and openingHours"]

    def get_localbusiness_types(self) -> list[str]:
        return ["LocalBusiness", "HomeAndConstructionBusiness", "ProfessionalService"]


class ServiceBriefProgram(ProgramRunner):
    def execute(self) -> dict[str, Any]:
        snapshot, service = self._load_snapshot()
        gaps = self._build_gaps(snapshot)
        outline = self._build_outline(service, gaps)
        schema = self._build_schema(service)
        return self._build_payload(snapshot, service, gaps, outline, schema)

    def _load_snapshot(self) -> tuple[CrawlSnapshot, str]:
        snapshot = CrawlSnapshot.import_csv(self.inputs.require_path("crawl_csv"))
        service = self.inputs.require_text("service")
        snapshot.set_service(service)
        return snapshot, service

    def _build_gaps(self, snapshot: CrawlSnapshot) -> ContentGapAnalyzer:
        gaps = ContentGapAnalyzer()
        gaps.set_pages(snapshot.get_pages_by_service())
        return gaps

    def _build_outline(self, service: str, gaps: ContentGapAnalyzer) -> OutlineBuilder:
        outline = OutlineBuilder()
        outline.set_service(service)
        outline.set_gaps(gaps.get_priority_gaps())
        return outline

    def _build_schema(self, service: str) -> SchemaChecklist:
        schema = SchemaChecklist()
        schema.set_service(service)
        return schema

    def _build_payload(
        self,
        snapshot: CrawlSnapshot,
        service: str,
        gaps: ContentGapAnalyzer,
        outline: OutlineBuilder,
        schema: SchemaChecklist,
    ) -> dict[str, Any]:
        return {
            "service": service,
            "pages": snapshot.get_pages_by_service(),
            "missing_sections": gaps.get_missing_sections(),
            "priority_gaps": gaps.get_priority_gaps(),
            "outline": outline.get_outline(),
            "required_sections": outline.get_required_sections(),
            "cta_notes": outline.get_cta_notes(),
            "schema": schema.get_required_schema(),
            "schema_notes": schema.get_schema_notes(),
        }

    def render_report(self, data: dict[str, Any]) -> str:
        report = [self._build_header(data)]
        report.extend(self._build_sections(data))
        return "\n".join(report).strip() + "\n"

    def _build_header(self, data: dict[str, Any]) -> str:
        return f"# Service Brief - {data['service']}\n"

    def _build_sections(self, data: dict[str, Any]) -> list[str]:
        return [
            self._build_overview(data),
            self._build_gaps(data),
            self._build_outline(data),
            self._build_required_sections(data),
            self._build_schema(data),
            self._build_cta(data),
        ]

    def report_basename(self) -> str:
        return "service-brief"

    def _build_overview(self, data: dict[str, Any]) -> str:
        body = render_table(
            ["Metric", "Value"],
            [["Pages found", str(len(data["pages"]))], ["Service", data["service"]]],
        )
        return render_section("Service Overview", body)

    def _build_gaps(self, data: dict[str, Any]) -> str:
        body = render_list(data["priority_gaps"])
        return render_section("Content Gaps", body)

    def _build_outline(self, data: dict[str, Any]) -> str:
        body = render_list(data["outline"])
        return render_section("Proposed Outline", body)

    def _build_required_sections(self, data: dict[str, Any]) -> str:
        body = render_list(data["required_sections"])
        return render_section("Required Sections", body)

    def _build_schema(self, data: dict[str, Any]) -> str:
        body = render_list(data["schema"] + data["schema_notes"])
        return render_section("Schema Requirements", body)

    def _build_cta(self, data: dict[str, Any]) -> str:
        return render_section("CTA Guidance", render_list(data["cta_notes"]))
