# Swarm Automation Programs Plan

This plan defines the OOP architecture and implementation checklist for the 8 automation programs.

## Global Standards
- All functions must be ≤ 20 lines.
- Each phase has a runner script and a program class.
- Shared utilities live in `scripts/workflow/automation/`.
- Each phase includes a Markdown report and JSON output.

---

## Phase 0 - Framework + Orchestrator

### TODO
- [ ] Create shared OOP base classes and I/O utilities
- [ ] Create report templating helpers
- [ ] Create orchestrator with phase registry and config loader
- [ ] Create runner entrypoints for all 8 phases (wire later)

---

## Phase 1 - Monthly Performance Intelligence Report

### TODO
- [ ] Implement `GA4Report` class (import/get/set helpers)
- [ ] Implement `GBPReport` class (import/get/set helpers)
- [ ] Implement `RankTrackerReport` class (import/get/set helpers)
- [ ] Implement `KPISummary` class (set/get snapshot)
- [ ] Implement `OpportunityFinder` class (growth/risk/recommendations)
- [ ] Implement `MonthlyPerformanceProgram` runner
- [ ] Create Phase 1 CLI runner
- [ ] Add report template output

---

## Phase 2 - Service Page Content Brief Auto-Generator

### TODO
- [ ] Implement `CrawlSnapshot` class (import/get/set helpers)
- [ ] Implement `ContentGapAnalyzer` class (gap detection)
- [ ] Implement `OutlineBuilder` class (H1-H3 outline)
- [ ] Implement `SchemaChecklist` class (schema requirements)
- [ ] Implement `ServiceBriefProgram` runner
- [ ] Create Phase 2 CLI runner
- [ ] Add report template output

---

## Phase 3 - Compliance Risk Audit + Remediation Plan

### TODO
- [ ] Implement `ComplianceScanner` class (claims extraction)
- [ ] Implement `RiskScorer` class (risk buckets)
- [ ] Implement `RemediationPlanner` class (fix checklist)
- [ ] Implement `ComplianceRiskProgram` runner
- [ ] Create Phase 3 CLI runner
- [ ] Add report template output

---

## Phase 4 - Keyword Strategy + 12-Month Content Plan

### TODO
- [ ] Implement `KeywordImporter` class (import/filter)
- [ ] Implement `ClusterBuilder` class (cluster creation)
- [ ] Implement `ContentCalendar` class (12-month plan)
- [ ] Implement `KpiPlanner` class (targets)
- [ ] Implement `KeywordStrategyProgram` runner
- [ ] Create Phase 4 CLI runner
- [ ] Add report template output

---

## Phase 5 - Measurement Intake + KPI Dashboard Setup

### TODO
- [ ] Implement `IntakeForm` class (goal extraction)
- [ ] Implement `KPIMapper` class (kpi definitions)
- [ ] Implement `ReportTemplateBuilder` class (dashboard template)
- [ ] Implement `MeasurementIntakeProgram` runner
- [ ] Create Phase 5 CLI runner
- [ ] Add report template output

---

## Phase 6 - GBP Optimization + 4-Week Social Post Plan

### TODO
- [ ] Implement `GBPProfile` class (profile scoring)
- [ ] Implement `OptimizationChecklist` class (prioritized actions)
- [ ] Implement `SocialPostPlanner` class (calendar + variants)
- [ ] Implement `GBPOptimizationProgram` runner
- [ ] Create Phase 6 CLI runner
- [ ] Add report template output

---

## Phase 7 - Citation Audit + Correction Workflow

### TODO
- [ ] Implement `CitationAudit` class (audit parsing)
- [ ] Implement `CorrectionPrioritizer` class (ranking)
- [ ] Implement `UpdateLogBuilder` class (queue creation)
- [ ] Implement `CitationCorrectionProgram` runner
- [ ] Create Phase 7 CLI runner
- [ ] Add report template output

---

## Phase 8 - Internal Link Map + Content Cluster Builder

### TODO
- [ ] Implement `LinkMapIngest` class (link map parsing)
- [ ] Implement `ClusterAnalyzer` class (cluster build)
- [ ] Implement `LinkRecommendationEngine` class (tasks + anchors)
- [ ] Implement `InternalLinkProgram` runner
- [ ] Create Phase 8 CLI runner
- [ ] Add report template output
