#!/usr/bin/env python3
"""Phase registry for orchestrator."""

from __future__ import annotations

from importlib import import_module
from typing import Callable

from .base import ProgramConfig, ProgramInputs, ProgramRunner


Builder = Callable[[ProgramConfig, ProgramInputs], ProgramRunner]


PHASE_CLASSES: dict[str, tuple[str, str]] = {
    "1": ("scripts.workflow.automation.phase1_monthly_performance", "MonthlyPerformanceProgram"),
    "2": ("scripts.workflow.automation.phase2_service_brief", "ServiceBriefProgram"),
    "3": ("scripts.workflow.automation.phase3_compliance_risk", "ComplianceRiskProgram"),
    "4": ("scripts.workflow.automation.phase4_keyword_strategy", "KeywordStrategyProgram"),
    "5": ("scripts.workflow.automation.phase5_measurement_intake", "MeasurementIntakeProgram"),
    "6": ("scripts.workflow.automation.phase6_gbp_optimization", "GBPOptimizationProgram"),
    "7": ("scripts.workflow.automation.phase7_citation_correction", "CitationCorrectionProgram"),
    "8": ("scripts.workflow.automation.phase8_internal_link", "InternalLinkProgram"),
}


def build_phase(phase_key: str, config: ProgramConfig, inputs: ProgramInputs) -> ProgramRunner:
    module_name, class_name = PHASE_CLASSES[phase_key]
    module = import_module(module_name)
    program_class = getattr(module, class_name)
    return program_class(config, inputs)


def make_builder(phase_key: str) -> Builder:
    def _builder(config: ProgramConfig, inputs: ProgramInputs) -> ProgramRunner:
        return build_phase(phase_key, config, inputs)

    return _builder


PHASE_BUILDERS: dict[str, Builder] = {key: make_builder(key) for key in PHASE_CLASSES}
