#!/usr/bin/env python3
"""Phase 1: Monthly Performance Intelligence Report."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from .base import ProgramConfig, ProgramInputs, ProgramRunner
from .io_utils import pick_value, read_csv
from .metrics_utils import safe_div, sum_metric, to_float, to_int
from .report_templates import render_list, render_section, render_table


def parse_date(value: str) -> datetime | None:
    cleaned = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(cleaned)
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


@dataclass
class CsvReportBase:
    rows: list[dict[str, str]]
    date_range: tuple[datetime, datetime] | None = None

    @classmethod
    def import_csv(cls, path: Path) -> "CsvReportBase":
        return cls(read_csv(path))

    def set_date_range(self, start: str | None, end: str | None) -> None:
        if not start or not end:
            self.date_range = None
            return
        start_dt = parse_date(start)
        end_dt = parse_date(end)
        if start_dt and end_dt:
            self.date_range = (start_dt, end_dt)

    def filtered_rows(self) -> list[dict[str, str]]:
        if not self.date_range:
            return self.rows
        return [row for row in self.rows if self._row_in_range(row)]

    def _row_in_range(self, row: dict[str, str]) -> bool:
        value = pick_value(row, ("date", "day", "date_range"))
        if not value or not self.date_range:
            return True
        row_date = parse_date(value)
        if not row_date:
            return False
        start, end = self.date_range
        return start <= row_date <= end


class GA4Report(CsvReportBase):
    def get_sessions(self) -> int:
        return sum_metric(self.filtered_rows(), "sessions")

    def get_conversions(self) -> int:
        return sum_metric(self.filtered_rows(), "conversions")

    def get_users(self) -> int:
        return sum_metric(self.filtered_rows(), "users")

    def get_engaged_sessions(self) -> int:
        return sum_metric(self.filtered_rows(), "engaged_sessions")

    def get_top_pages(self, limit: int = 10) -> list[dict[str, Any]]:
        rows = self.filtered_rows()
        scored = [
            {"page": pick_value(row, ("page", "page_path")), "sessions": to_int(row.get("sessions", ""))}
            for row in rows
        ]
        ranked = sorted(scored, key=lambda item: item["sessions"], reverse=True)
        return [item for item in ranked if item["page"]][:limit]


class GBPReport(CsvReportBase):
    def get_profile_views(self) -> int:
        return sum_metric(self.filtered_rows(), "profile_views")

    def get_calls(self) -> int:
        return sum_metric(self.filtered_rows(), "calls")

    def get_directions(self) -> int:
        return sum_metric(self.filtered_rows(), "directions")

    def get_website_clicks(self) -> int:
        return sum_metric(self.filtered_rows(), "website_clicks")

    def get_total_actions(self) -> int:
        rows = self.filtered_rows()
        return self.get_calls() + self.get_directions() + sum_metric(rows, "website_clicks")


class RankTrackerReport(CsvReportBase):
    def get_avg_position(self) -> float:
        positions = [to_float(pick_value(row, ("position", "rank"))) for row in self.filtered_rows()]
        valid = [pos for pos in positions if pos > 0]
        return safe_div(sum(valid), len(valid))

    def get_top_movers(self, limit: int = 10) -> list[dict[str, Any]]:
        rows = self._score_changes(self.filtered_rows())
        ranked = sorted(rows, key=lambda item: abs(item["change"]), reverse=True)
        return ranked[:limit]

    def get_winners(self, limit: int = 10) -> list[dict[str, Any]]:
        rows = [row for row in self._score_changes(self.filtered_rows()) if row["change"] < 0]
        ranked = sorted(rows, key=lambda item: item["change"])
        return ranked[:limit]

    def get_losers(self, limit: int = 10) -> list[dict[str, Any]]:
        rows = [row for row in self._score_changes(self.filtered_rows()) if row["change"] > 0]
        ranked = sorted(rows, key=lambda item: item["change"], reverse=True)
        return ranked[:limit]

    def _score_changes(self, rows: Iterable[dict[str, str]]) -> list[dict[str, Any]]:
        scored: list[dict[str, Any]] = []
        for row in rows:
            scored.append(
                {
                    "keyword": pick_value(row, ("keyword", "query")),
                    "position": to_float(pick_value(row, ("position", "rank"))),
                    "change": to_float(pick_value(row, ("change", "delta"))),
                }
            )
        return scored


class KPISummary:
    def __init__(self) -> None:
        self.ga4: GA4Report | None = None
        self.gbp: GBPReport | None = None
        self.rank: RankTrackerReport | None = None

    def set_ga4(self, report: GA4Report) -> None:
        self.ga4 = report

    def set_gbp(self, report: GBPReport) -> None:
        self.gbp = report

    def set_rank(self, report: RankTrackerReport) -> None:
        self.rank = report

    def get_snapshot(self) -> dict[str, Any]:
        return {
            "sessions": self._get_ga4_value("sessions"),
            "conversions": self._get_ga4_value("conversions"),
            "users": self._get_ga4_value("users"),
            "gbp_actions": self._get_gbp_value("total_actions"),
            "avg_position": self._get_rank_value("avg_position"),
        }

    def _get_ga4_value(self, key: str) -> int:
        if not self.ga4:
            return 0
        return {
            "sessions": self.ga4.get_sessions,
            "conversions": self.ga4.get_conversions,
            "users": self.ga4.get_users,
        }[key]()

    def _get_gbp_value(self, key: str) -> int:
        if not self.gbp:
            return 0
        return {"total_actions": self.gbp.get_total_actions}[key]()

    def _get_rank_value(self, key: str) -> float:
        if not self.rank:
            return 0.0
        return {"avg_position": self.rank.get_avg_position}[key]()


class OpportunityFinder:
    def __init__(self) -> None:
        self.ga4: GA4Report | None = None
        self.gbp: GBPReport | None = None
        self.rank: RankTrackerReport | None = None

    def set_sources(self, ga4: GA4Report, gbp: GBPReport, rank: RankTrackerReport) -> None:
        self.ga4 = ga4
        self.gbp = gbp
        self.rank = rank

    def get_growth_opportunities(self) -> list[str]:
        if not self.ga4 or not self.rank:
            return []
        winners = self.rank.get_winners(5)
        pages = [item["page"] for item in self.ga4.get_top_pages(5)]
        target = self._first_page(pages)
        return [f"Double down on {winner['keyword']} targeting {target}" for winner in winners]

    def get_risk_flags(self) -> list[str]:
        if not self.rank:
            return []
        losers = self.rank.get_losers(5)
        return [f"Ranking drop: {item['keyword']} ({item['change']})" for item in losers]

    def get_recommendations(self) -> list[str]:
        actions = []
        if self.gbp:
            actions.append("Refresh GBP posts and images for visibility.")
        actions.extend(self.get_growth_opportunities())
        actions.extend(self.get_risk_flags())
        return actions

    def _first_page(self, pages: list[str]) -> str:
        return pages[0] if pages else "top landing page"


class MonthlyPerformanceProgram(ProgramRunner):
    def execute(self) -> dict[str, Any]:
        ga4, gbp, rank = self._load_sources()
        kpis = self._build_kpis(ga4, gbp, rank)
        opportunities = self._build_opportunities(ga4, gbp, rank)
        return self._build_payload(ga4, rank, kpis, opportunities)

    def _load_sources(self) -> tuple[GA4Report, GBPReport, RankTrackerReport]:
        ga4 = GA4Report.import_csv(self.inputs.require_path("ga4_csv"))
        gbp = GBPReport.import_csv(self.inputs.require_path("gbp_csv"))
        rank = RankTrackerReport.import_csv(self.inputs.require_path("rank_csv"))
        return ga4, gbp, rank

    def _build_kpis(self, ga4: GA4Report, gbp: GBPReport, rank: RankTrackerReport) -> KPISummary:
        kpis = KPISummary()
        kpis.set_ga4(ga4)
        kpis.set_gbp(gbp)
        kpis.set_rank(rank)
        return kpis

    def _build_opportunities(
        self, ga4: GA4Report, gbp: GBPReport, rank: RankTrackerReport
    ) -> OpportunityFinder:
        opportunities = OpportunityFinder()
        opportunities.set_sources(ga4, gbp, rank)
        return opportunities

    def _build_payload(
        self,
        ga4: GA4Report,
        rank: RankTrackerReport,
        kpis: KPISummary,
        opportunities: OpportunityFinder,
    ) -> dict[str, Any]:
        return {
            "kpis": kpis.get_snapshot(),
            "ga4_top_pages": ga4.get_top_pages(),
            "rank_winners": rank.get_winners(),
            "rank_losers": rank.get_losers(),
            "opportunities": opportunities.get_recommendations(),
        }

    def render_report(self, data: dict[str, Any]) -> str:
        report = [self._build_header()]
        report.append(render_section("Executive Summary", "Monthly KPI snapshot and movement."))
        report.append(self._build_kpi_section(data))
        report.append(self._build_top_pages_section(data))
        report.append(self._build_winners_section(data))
        report.append(self._build_losers_section(data))
        report.append(self._build_opportunities_section(data))
        return "\n".join(report).strip() + "\n"

    def _build_header(self) -> str:
        return f"# Monthly Performance Report - {self.config.client_name}\n"

    def _build_kpi_section(self, data: dict[str, Any]) -> str:
        kpis = data["kpis"]
        rows = [
            ["Sessions", str(kpis["sessions"])],
            ["Conversions", str(kpis["conversions"])],
            ["Users", str(kpis["users"])],
            ["GBP Actions", str(kpis["gbp_actions"])],
            ["Avg Position", f"{kpis['avg_position']:.2f}"],
        ]
        return render_section("KPI Snapshot", render_table(["Metric", "Value"], rows))

    def _build_top_pages_section(self, data: dict[str, Any]) -> str:
        rows = [[item["page"], str(item["sessions"])] for item in data["ga4_top_pages"]]
        return render_section("Top Pages", render_table(["Page", "Sessions"], rows))

    def _build_winners_section(self, data: dict[str, Any]) -> str:
        rows = [[item["keyword"], str(item["change"])] for item in data["rank_winners"]]
        return render_section("Ranking Winners", render_table(["Keyword", "Change"], rows))

    def _build_losers_section(self, data: dict[str, Any]) -> str:
        rows = [[item["keyword"], str(item["change"])] for item in data["rank_losers"]]
        return render_section("Ranking Losers", render_table(["Keyword", "Change"], rows))

    def _build_opportunities_section(self, data: dict[str, Any]) -> str:
        return render_section("Opportunities & Risks", render_list(data["opportunities"]))

    def report_basename(self) -> str:
        return "monthly-performance-report"
