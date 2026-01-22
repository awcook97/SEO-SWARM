# SEO-SWARM

This repository contains a reusable swarm workflow, templates, and measurement assets for local SEO content production.

## What is included

- Swarm roles and guardrails: @docs/client-templates/swarm-roles.md
- Webpage templates: @docs/client-templates/webpage-templates.md
- Article templates: @docs/client-templates/article-templates.md
- Measurement spec: @docs/seo/measurement-spec.md
- Measurement intake + reporting templates:
  - @docs/seo/measurement-intake-template.md
  - @docs/seo/measurement-reporting-template.md
- Swarm execution workflow: @docs/seo/swarm-execution-workflow.md
- Scaffold script: @scripts/swarm_workflow.py

## Quick start

1) Review the swarm roles and guardrails: @docs/client-templates/swarm-roles.md.
2) Use @scripts/swarm_workflow.py to scaffold a new client folder.
3) Populate `data/outputs/<client>/inputs.md` with approved inputs.
   - Template: @docs/seo/inputs-template.md
4) Run the core automation scripts (see below) and draft content from the templates.

Example scaffold:

```bash
python scripts/swarm_workflow.py --client "Example HVAC" --slug example-hvac
```

## Onboard a new client (end-to-end)

1) Create the client folder:
   - `python scripts/swarm_workflow.py --client "Client Name" --slug client-slug`
2) Fill in `data/outputs/<client>/inputs.md` with approved facts (NAP, services, hours, proof points).
   - Template: @docs/seo/inputs-template.md
3) Capture measurement inputs:
   - Use @docs/seo/measurement-intake-template.md
   - Optional generator: `python scripts/measurement_intake_generator.py --client-slug client-slug --scaffold`
4) Run a crawl cache if needed (see @scripts/service_brief_generator.py requirements).
5) Generate service briefs and supporting reports.
6) Produce content briefs and draft pages/articles using templates.

## Swarm workflow (recommended order)

1) **Intake + validation**
   - Approved inputs in `data/outputs/<client>/inputs.md` (see @docs/seo/inputs-template.md)
   - Measurement intake per @docs/seo/measurement-intake-template.md
2) **Strategy + mapping**
   - Keyword map + KPI targets:
     `python scripts/keyword_map_kpi.py --client-slug client-slug --scaffold`
3) **Content production**
   - Generate service briefs:
     `python scripts/service_brief_generator.py --client-slug client-slug`
   - Summarize briefs:
     `python scripts/brief_summary_report.py --client-slug client-slug`
   - Generate content briefs:
     `python scripts/content_brief_generator.py --client-slug client-slug --scaffold`
4) **On-page + metadata**
   - Metadata + internal link map:
     `python scripts/metadata_internal_link_map.py --client-slug client-slug`
   - Internal link validation:
     `python scripts/internal_link_validator.py --client-slug client-slug`
5) **Compliance**
   - Draft compliance lint:
     `python scripts/draft_compliance_lint.py --client-slug client-slug`
6) **Local asset updates**
   - GBP update checklist:
     `python scripts/gbp_update_checklist.py --client-slug client-slug`
   - Citation update log:
     `python scripts/citation_update_log.py --client-slug client-slug --scaffold`
   - Local link outreach log:
     `python scripts/local_link_outreach.py --client-slug client-slug --scaffold`
   - Review response templates:
     `python scripts/review_response_templates.py --client-slug client-slug --scaffold`
   - Review export ingest:
     `python scripts/review_export_ingest.py --client-slug client-slug --input path/to/reviews.csv`
7) **Technical audit**
   - `python scripts/technical_seo_audit_scaffold.py --client-slug client-slug`

## Automation scripts (outputs)

All scripts write under `data/outputs/<client>/reports/` unless noted.

- Service briefs: `service_brief_generator.py` -> `service-briefs/*.md`
- Brief summary: `brief_summary_report.py` -> `service-briefs-summary.md/.json`
- Content briefs: `content_brief_generator.py` -> `content-briefs/*.md` + `content-briefs.json`
- Metadata + internal link map: `metadata_internal_link_map.py` -> `metadata-internal-link-map.md/.json`
- Metadata linkmap ingest: `metadata_linkmap_ingest.py` -> `metadata-linkmap-input.json`
- Internal link validation: `internal_link_validator.py` -> report in `reports/`
- Measurement intake: `measurement_intake_generator.py` -> `measurement-intake.md/.json`
- Keyword map + KPI: `keyword_map_kpi.py` -> `keyword-map-kpi.md/.json`
- DataForSEO SERP fetch: `serp_dataforseo_fetch.py` -> `serp-export.json` + inputs
- GA4 export ingest: `ga4_export_ingest.py` -> `ga4-export.json` + `ga4-summary.json` (optional)
- Rank tracker export ingest: `rank_tracker_export_ingest.py` -> `rank-tracker-export.csv/.json`
- Draft compliance lint: `draft_compliance_lint.py` -> `draft-compliance-lint.md/.json`
- GBP checklist: `gbp_update_checklist.py` -> `gbp-update-checklist.md/.json`
- GBP export ingest: `gbp_export_ingest.py` -> `gbp-export.json` + `gbp-summary.json` (optional)
- Citation log: `citation_update_log.py` -> `citation-update-log.md/.json`
- Citation audit ingest: `citation_audit_ingest.py` -> `citation-log-input.json`
- Local link outreach log: `local_link_outreach.py` -> `local-link-outreach.md/.json`
- Review response templates: `review_response_templates.py` -> `review-response-templates.md/.json`
- GSC export ingest: `gsc_export_ingest.py` -> `gsc-export.json` + `gsc-summary.json` (optional)
- Review export ingest: `review_export_ingest.py` -> `review-templates-input.json`
- Technical SEO audit scaffold: `technical_seo_audit_scaffold.py` -> `technical-seo-audit.md/.json`
- Crawl export ingest: `crawl_export_ingest.py` -> `crawl-export.json` + `crawl-summary.json` (optional)

## Notes

- Client outputs are intentionally ignored from git (`data/outputs/` in `.gitignore`).
- Replace all placeholders with approved inputs before publishing.

## Environment

- Copy `.env.example` to `.env` and set `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD`, `DATAFORSEO_ENDPOINT` for SERP fetch automation.
