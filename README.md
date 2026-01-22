# SEO-SWARM

SEO-SWARM is a local SEO production workspace that turns structured inputs into reports, briefs, and draft-ready assets. It combines a step-by-step workflow, reusable templates, and automation scripts that write everything into `data/outputs/<client>/`.

Use it to:
- scaffold a client workspace
- collect and validate inputs
- generate briefs, audits, and compliance checks
- preview outputs in a web UI

## What this repo contains

- Workflow rules and roles: @docs/client-templates/swarm-roles.md
- Content templates: @docs/client-templates/webpage-templates.md, @docs/client-templates/article-templates.md
- Measurement system: @docs/seo/measurement-spec.md + intake/reporting templates
  - @docs/seo/measurement-intake-template.md
  - @docs/seo/measurement-reporting-template.md
- End-to-end execution flow: @docs/seo/swarm-execution-workflow.md
- Automation scripts grouped by category:
  - @scripts/workflow/ (scaffolding and viewers)
  - @scripts/generators/ (reports and briefs)
  - @scripts/ingest/ (input ingestion and exports)
  - @scripts/validation/ (linting and validation)

## Quick start (fast path)

1) Read the roles and guardrails: @docs/client-templates/swarm-roles.md
2) Scaffold a client workspace:
   - `python scripts/workflow/swarm_workflow.py --client "Client Name" --slug client-slug`
   - Optional: add `--site-url https://example.com` to crawl and cache the site HTML.
3) Fill approved facts in `data/outputs/<client>/inputs.md`
   - Template: @docs/seo/inputs-template.md
4) Run generators for briefs and reports (see below)
5) Open the outputs viewer to browse and QA generated files:
   - `python3 scripts/workflow/outputs_viewer.py`
   - or `./outputs_viewer.sh`

## Use the app to its full potential

- Treat `data/outputs/<client>/inputs.md` as the single source of truth. All downstream scripts reference it or derived JSONs.
- Run the workflow in order (intake -> mapping -> briefs -> metadata -> compliance). See @docs/seo/swarm-execution-workflow.md.
- Use the outputs viewer to QA HTML and JSON outputs quickly without digging through folders.
- Keep input exports (GSC, GBP, GA4, rank tracker, crawl data) in `data/outputs/<client>/reports/` and ingest them via @scripts/ingest/.
- Validate schema HTML via @docs/seo/schema-approval-workflow.md before shipping.

## Onboard a new client (end-to-end)

1) Create the client folder:
   - `python scripts/workflow/swarm_workflow.py --client "Client Name" --slug client-slug`
   - Optional: add `--site-url https://example.com` to crawl and cache the site HTML.
2) Fill in `data/outputs/<client>/inputs.md` with approved facts (NAP, services, hours, proof points).
   - Template: @docs/seo/inputs-template.md
3) Capture measurement inputs:
   - Use @docs/seo/measurement-intake-template.md
   - Optional generator: `python scripts/generators/measurement_intake_generator.py --client-slug client-slug --scaffold`
4) Run a crawl cache if needed (see @scripts/generators/service_brief_generator.py requirements).
5) Generate service briefs and supporting reports.
6) Produce content briefs and draft pages/articles using templates.

## Swarm workflow (recommended order)

1) **Intake + validation**
   - Approved inputs in `data/outputs/<client>/inputs.md` (see @docs/seo/inputs-template.md)
   - Measurement intake per @docs/seo/measurement-intake-template.md
2) **Strategy + mapping**
   - Keyword map + KPI targets:
     `python scripts/generators/keyword_map_kpi.py --client-slug client-slug --scaffold`
3) **Content production**
   - Generate service briefs:
     `python scripts/generators/service_brief_generator.py --client-slug client-slug`
   - Summarize briefs:
     `python scripts/generators/brief_summary_report.py --client-slug client-slug`
   - Generate content briefs:
     `python scripts/generators/content_brief_generator.py --client-slug client-slug --scaffold`
4) **On-page + metadata**
   - Metadata + internal link map:
     `python scripts/generators/metadata_internal_link_map.py --client-slug client-slug`
   - Internal link validation:
     `python scripts/validation/internal_link_validator.py --client-slug client-slug`
5) **Compliance**
   - Draft compliance lint:
     `python scripts/validation/draft_compliance_lint.py --client-slug client-slug`
6) **Local asset updates**
   - GBP update checklist:
     `python scripts/generators/gbp_update_checklist.py --client-slug client-slug`
   - Citation update log:
     `python scripts/generators/citation_update_log.py --client-slug client-slug --scaffold`
   - Local link outreach log:
     `python scripts/generators/local_link_outreach.py --client-slug client-slug --scaffold`
   - Review response templates:
     `python scripts/generators/review_response_templates.py --client-slug client-slug --scaffold`
   - Review export ingest:
     `python scripts/ingest/review_export_ingest.py --client-slug client-slug --input path/to/reviews.csv`
7) **Technical audit**
   - `python scripts/generators/technical_seo_audit_scaffold.py --client-slug client-slug`

## Automation scripts (outputs)

All scripts write under `data/outputs/<client>/reports/` unless noted. Use the outputs viewer to browse and QA results quickly.

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
