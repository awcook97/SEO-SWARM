# SEO swarm execution workflow (reusable)

This workflow is client-agnostic and defines how the swarm executes end-to-end delivery. All facts must come from approved inputs.

## Inputs required to start

- Approved business facts (NAP, hours, service areas).
- Service list and priorities.
- Proof points with sources.
- Measurement inputs per @docs/seo/measurement-spec.md.

## Workflow stages

1) Intake and validation
- Collect measurement intake: @docs/seo/measurement-intake-template.md.
- Validate service areas and approved claims.

2) Strategy and planning
- Define keyword map and target URLs.
- Establish rank tracking cadence and competitor set.

3) Content production
- Use page templates: @docs/client-templates/webpage-templates.md (or client equivalents).
- Use article templates: @docs/client-templates/article-templates.md (or client equivalents).
- Enforce schema on every page (required).
- Generate metadata + internal link map (outputs/<client>/reports/metadata-internal-link-map.*).

4) Review and compliance
- Validate claims against sources.
- Confirm NAP consistency and service areas.
- Run internal link validation against the link map output.

5) Distribution and promotion
- Publish blog posts and landing pages.
- Schedule social posts.
- Send email to subscribers.

6) Measurement and iteration
- Produce rank tracking report.
- Run competitor analysis snapshot.
- Apply recommendations to the next cycle.

## Required outputs (per cycle)

- 1 service page draft.
- 1 local landing page draft.
- 1 topical article/blog post.
- 5 to 10 social posts.
- 1 email to subscribers.
- Metadata + internal link map report.
- Rank tracking report and competitor snapshot.

## Handoff checklist

- All placeholders resolved from approved inputs.
- Schema included for every page.
- Internal links validated.
- Measurement inputs captured for tracking.
