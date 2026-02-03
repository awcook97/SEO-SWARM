#!/usr/bin/env python3
"""Phase 3: Compliance Risk Audit + Remediation Plan."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .base import ProgramRunner
from .report_templates import render_list, render_section, render_table


@dataclass
class ComplianceScanner:
    policy_phrases: list[str]

    @classmethod
    def from_policy(cls, path: Path) -> "ComplianceScanner":
        phrases = cls._extract_phrases(path.read_text(encoding="utf-8"))
        return cls(phrases)

    def import_markdown(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def get_claims(self, text: str) -> list[str]:
        sentences = self._split_sentences(text)
        return [s for s in sentences if self._looks_like_claim(s)]

    def get_disallowed_claims(self, claims: list[str]) -> list[str]:
        return [claim for claim in claims if not self._is_allowed(claim)]

    def get_allowed_claims(self, claims: list[str]) -> list[str]:
        return [claim for claim in claims if self._is_allowed(claim)]

    @staticmethod
    def _extract_phrases(text: str) -> list[str]:
        phrases = []
        for line in text.splitlines():
            cleaned = line.strip().lstrip("-*").strip()
            if cleaned:
                phrases.append(cleaned.lower())
        return phrases

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        return [s.strip() for s in re.split(r"[.!?]\s+", text) if s.strip()]

    @staticmethod
    def _looks_like_claim(sentence: str) -> bool:
        return any(token in sentence.lower() for token in ("guarantee", "best", "only", "%"))

    def _is_allowed(self, claim: str) -> bool:
        return any(phrase in claim.lower() for phrase in self.policy_phrases)


class RiskScorer:
    def __init__(self) -> None:
        self.claims: list[str] = []
        self.scored: list[dict[str, Any]] = []

    def set_claims(self, claims: list[str]) -> None:
        self.claims = claims

    def score_claims(self) -> list[dict[str, Any]]:
        self.scored = [self._score_claim(claim) for claim in self.claims]
        return self.scored

    def get_high_risk(self) -> list[dict[str, Any]]:
        return [item for item in self._ensure_scored() if item["risk"] == "high"]

    def get_medium_risk(self) -> list[dict[str, Any]]:
        return [item for item in self._ensure_scored() if item["risk"] == "medium"]

    def get_low_risk(self) -> list[dict[str, Any]]:
        return [item for item in self._ensure_scored() if item["risk"] == "low"]

    def split_by_risk(self, scored: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        return {
            "high": [item for item in scored if item["risk"] == "high"],
            "medium": [item for item in scored if item["risk"] == "medium"],
            "low": [item for item in scored if item["risk"] == "low"],
        }

    def _score_claim(self, claim: str) -> dict[str, Any]:
        score = 1
        if "%" in claim:
            score += 1
        if "guarantee" in claim.lower():
            score += 2
        risk = "high" if score >= 3 else "medium" if score == 2 else "low"
        return {"claim": claim, "risk": risk, "score": score}

    def _ensure_scored(self) -> list[dict[str, Any]]:
        return self.scored if self.scored else self.score_claims()


class RemediationPlanner:
    def __init__(self) -> None:
        self.risks: list[dict[str, Any]] = []

    def set_risks(self, risks: list[dict[str, Any]]) -> None:
        self.risks = risks

    def get_fixes(self) -> list[dict[str, str]]:
        return [{"claim": r["claim"], "fix": "Rewrite to match approved language"} for r in self.risks]

    def get_alternative_phrasing(self) -> list[str]:
        return ["Describe outcomes without guarantees", "Reference testimonials instead of claims"]

    def build_checklist(self) -> list[str]:
        return [f"Update: {r['claim']}" for r in self.risks]

    def get_owner_tasks(self) -> list[dict[str, str]]:
        return [{"owner": "Compliance", "task": f"Review: {r['claim']}"} for r in self.risks]


class ComplianceRiskProgram(ProgramRunner):
    def execute(self) -> dict[str, Any]:
        scanner = ComplianceScanner.from_policy(self.inputs.require_path("policy_md"))
        content = scanner.import_markdown(self.inputs.require_path("content_md"))
        claims = scanner.get_claims(content)
        disallowed = scanner.get_disallowed_claims(claims)

        scorer = RiskScorer()
        scorer.set_claims(disallowed)
        scored = scorer.score_claims()
        buckets = scorer.split_by_risk(scored)

        planner = RemediationPlanner()
        planner.set_risks(scored)

        return {
            "claims": claims,
            "disallowed": disallowed,
            "high": buckets["high"],
            "medium": buckets["medium"],
            "low": buckets["low"],
            "fixes": planner.get_fixes(),
            "alternatives": planner.get_alternative_phrasing(),
            "checklist": planner.build_checklist(),
        }

    def render_report(self, data: dict[str, Any]) -> str:
        sections = [f"# Compliance Risk Report - {self.config.client_name}\n"]
        sections.append(self._build_summary(data))
        sections.append(self._build_risk_section("High Risk Claims", data["high"]))
        sections.append(self._build_risk_section("Medium Risk Claims", data["medium"]))
        sections.append(self._build_risk_section("Low Risk Claims", data["low"]))
        sections.append(render_section("Remediation Checklist", render_list(data["checklist"])))
        sections.append(render_section("Approved Alternatives", render_list(data["alternatives"])))
        return "\n".join(sections).strip() + "\n"

    def report_basename(self) -> str:
        return "compliance-risk-report"

    def _build_summary(self, data: dict[str, Any]) -> str:
        rows = [
            ["Claims Found", str(len(data["claims"]))],
            ["Disallowed", str(len(data["disallowed"]))],
        ]
        return render_section("Compliance Summary", render_table(["Metric", "Count"], rows))

    def _build_risk_section(self, title: str, items: list[dict[str, Any]]) -> str:
        rows = [[item["claim"], item["risk"], str(item["score"])] for item in items]
        table = render_table(["Claim", "Risk", "Score"], rows)
        return render_section(title, table)
