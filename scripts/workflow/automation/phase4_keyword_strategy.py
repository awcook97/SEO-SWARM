#!/usr/bin/env python3
"""Phase 4: Keyword Strategy + 12-Month Content Plan."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .base import ProgramRunner
from .io_utils import pick_value, read_csv
from .metrics_utils import to_int
from .report_templates import render_list, render_section, render_table


@dataclass
class KeywordImporter:
    rows: list[dict[str, str]]
    volume_min: int = 0

    @classmethod
    def import_csv(cls, path: Path) -> "KeywordImporter":
        return cls(read_csv(path))

    def set_volume_min(self, volume: int) -> None:
        self.volume_min = volume

    def get_rows(self) -> list[dict[str, str]]:
        return self.rows

    def get_keywords(self) -> list[str]:
        keywords = [pick_value(row, ("keyword", "query")) for row in self._filtered_rows()]
        return [keyword for keyword in keywords if keyword]

    def get_top_keywords(self, limit: int = 20) -> list[dict[str, str]]:
        rows = sorted(self._filtered_rows(), key=self._volume_key, reverse=True)
        return rows[:limit]

    def _filtered_rows(self) -> list[dict[str, str]]:
        return [row for row in self.rows if self._volume_key(row) >= self.volume_min]

    def _volume_key(self, row: dict[str, str]) -> int:
        return to_int(pick_value(row, ("volume", "search_volume")))


class ClusterBuilder:
    def __init__(self) -> None:
        self.keywords: list[str] = []

    def set_keywords(self, keywords: list[str]) -> None:
        self.keywords = keywords

    def build_clusters(self) -> dict[str, list[str]]:
        clusters: dict[str, list[str]] = {}
        for keyword in self.keywords:
            key = self._cluster_key(keyword)
            clusters.setdefault(key, []).append(keyword)
        return clusters

    def get_priority_clusters(self, clusters: dict[str, list[str]]) -> list[dict[str, Any]]:
        items = [{"cluster": key, "count": len(values)} for key, values in clusters.items()]
        return sorted(items, key=lambda item: item["count"], reverse=True)

    def get_cluster_keywords(self, clusters: dict[str, list[str]], key: str) -> list[str]:
        return clusters.get(key, [])

    def _cluster_key(self, keyword: str) -> str:
        tokens = keyword.split()
        return " ".join(tokens[:2]).lower() if tokens else "misc"


class ContentCalendar:
    def __init__(self) -> None:
        self.clusters: dict[str, list[str]] = {}

    def set_clusters(self, clusters: dict[str, list[str]]) -> None:
        self.clusters = clusters

    def build_12_month_plan(self) -> list[dict[str, Any]]:
        keys = list(self.clusters.keys())
        return [self._build_month_plan(i + 1, keys) for i in range(12)]

    def get_month(self, plan: list[dict[str, Any]], month: int) -> dict[str, Any]:
        if month < 1 or month > len(plan):
            raise SystemExit("Month must be between 1 and 12")
        return plan[month - 1]

    def _build_month_plan(self, month: int, keys: list[str]) -> dict[str, Any]:
        index = (month - 1) % len(keys) if keys else 0
        cluster = keys[index] if keys else "misc"
        return {"month": month, "focus": cluster, "topics": self.clusters.get(cluster, [])[:5]}


class KpiPlanner:
    def __init__(self) -> None:
        self.clusters: dict[str, list[str]] = {}

    def set_clusters(self, clusters: dict[str, list[str]]) -> None:
        self.clusters = clusters

    def get_targets(self) -> dict[str, int]:
        return {key: max(1, len(values) // 2) for key, values in self.clusters.items()}

    def get_monthly_targets(self) -> list[dict[str, Any]]:
        targets = self.get_targets()
        return [{"cluster": key, "target": value} for key, value in targets.items()]

    def get_total_target(self) -> int:
        return sum(self.get_targets().values())


class KeywordStrategyProgram(ProgramRunner):
    def execute(self) -> dict[str, Any]:
        importer = self._load_keywords()
        clustered = self._build_clusters(importer)
        plan = self._build_calendar(clustered)
        kpis = self._build_kpis(clustered)
        return self._build_payload(importer, clustered, plan, kpis)

    def _load_keywords(self) -> KeywordImporter:
        importer = KeywordImporter.import_csv(self.inputs.require_path("keywords_csv"))
        importer.set_volume_min(10)
        return importer

    def _build_clusters(self, importer: KeywordImporter) -> dict[str, list[str]]:
        clusters = ClusterBuilder()
        clusters.set_keywords(importer.get_keywords())
        return clusters.build_clusters()

    def _build_calendar(self, clustered: dict[str, list[str]]) -> list[dict[str, Any]]:
        calendar = ContentCalendar()
        calendar.set_clusters(clustered)
        return calendar.build_12_month_plan()

    def _build_kpis(self, clustered: dict[str, list[str]]) -> KpiPlanner:
        kpis = KpiPlanner()
        kpis.set_clusters(clustered)
        return kpis

    def _build_payload(
        self,
        importer: KeywordImporter,
        clustered: dict[str, list[str]],
        plan: list[dict[str, Any]],
        kpis: KpiPlanner,
    ) -> dict[str, Any]:
        clusters = ClusterBuilder()
        return {
            "top_keywords": importer.get_top_keywords(),
            "clusters": clusters.get_priority_clusters(clustered),
            "calendar": plan,
            "kpi_targets": kpis.get_monthly_targets(),
            "total_target": kpis.get_total_target(),
        }

    def render_report(self, data: dict[str, Any]) -> str:
        report = [self._build_header()]
        report.extend(self._build_sections(data))
        return "\n".join(report).strip() + "\n"

    def _build_header(self) -> str:
        return f"# Keyword Strategy Plan - {self.config.client_name}\n"

    def _build_sections(self, data: dict[str, Any]) -> list[str]:
        return [
            self._build_summary(data),
            self._build_clusters(data),
            self._build_calendar(data),
            self._build_kpis(data),
        ]

    def report_basename(self) -> str:
        return "keyword-strategy-plan"

    def _build_summary(self, data: dict[str, Any]) -> str:
        rows = [["Total KPI Target", str(data["total_target"])]]
        return render_section("Strategy Summary", render_table(["Metric", "Value"], rows))

    def _build_clusters(self, data: dict[str, Any]) -> str:
        rows = [[item["cluster"], str(item["count"])] for item in data["clusters"]]
        return render_section("Keyword Clusters", render_table(["Cluster", "Count"], rows))

    def _build_calendar(self, data: dict[str, Any]) -> str:
        items = [f"Month {item['month']}: {item['focus']}" for item in data["calendar"]]
        return render_section("12-Month Content Calendar", render_list(items))

    def _build_kpis(self, data: dict[str, Any]) -> str:
        rows = [[item["cluster"], str(item["target"])] for item in data["kpi_targets"]]
        return render_section("KPI Targets", render_table(["Cluster", "Target"], rows))
