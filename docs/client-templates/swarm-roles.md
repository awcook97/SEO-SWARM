# Local SEO swarm roles (client-agnostic)

This file defines the agent roles, responsibilities, and handoffs for a local SEO swarm supporting a single client. All facts about the business or market must come from approved inputs (owner notes, CRM, GBP, GA4/GSC, call logs, or verified citations). Do not invent external facts.

## Role roster

| Role | Mission | Inputs | Outputs |
| --- | --- | --- | --- |
| Orchestrator | Owns roadmap, prioritization, and handoffs. | Business goals, sprint scope, constraints. | Sprint plan, task assignments, acceptance criteria. |
| Local SEO Strategist | Translates goals into local SEO strategy and KPIs. | Orchestrator plan, baseline metrics, target areas. | Target keywords, service-area map, KPI targets. |
| Service Researcher | Gathers service details and differentiators. | Owner notes, technician notes, job logs. | Service briefs, FAQs, proof points with sources. |
| Competitor and SERP Analyst | Reviews local SERP patterns without fabricating data. | Approved SERP exports, citation audit data. | SERP insights, feature targets, gap list. |
| GBP Optimizer | Improves Google Business Profile content and structure. | GBP access, photos, services list. | GBP updates plan, posting calendar, attribute fixes. |
| On-Page SEO Specialist | Defines on-page structure and metadata. | Target keywords, service briefs. | Page outlines, title/meta, internal link map. |
| Technical SEO Auditor | Finds crawl, index, and performance risks. | Crawl exports, Core Web Vitals, sitemaps. | Audit report, prioritized fixes, regression checks. |
| Content Planner | Builds content calendar and template requirements. | Strategy, service briefs, SERP insights. | Content roadmap, template requirements, briefs. |
| Copywriter | Drafts pages and articles from briefs. | Outlines, FAQs, proof points. | Drafts with citations to approved inputs. |
| Editor and Compliance | Ensures clarity, compliance, and consistency. | Drafts, brand guidelines. | Edited drafts, risk flags, style alignment. |
| Citation Manager | Maintains listings and NAP consistency. | NAP source of truth, audit list. | Citation cleanup plan, updates log. |
| Analytics and Reporting | Measures performance and reports impact. | GA4/GSC exports, call tracking. | Monthly report, insights, next-step suggestions. |
| Review and Reputation | Guides review generation and responses. | Review inbox, owner approvals. | Response templates, outreach plan, escalation list. |
| Local Link Builder | Pursues local partnerships and mentions. | Target list, community calendar. | Outreach plan, tracked placements. |

## Role playbooks (ready-to-run)

These are “fill in the blanks” briefs for running the roles above. They are written to map cleanly to specialist Codex agents (optional) while still being usable for humans.

### Local SEO Strategist

Mission: turn approved business inputs into a keyword→URL plan and measurable KPIs.

Inputs required:

- Approved NAP, hours, service areas
- Service list + service priority order
- Approved claims/proof points with sources
- Measurement intake fields from `docs/seo/measurement-intake-template.md`

Outputs (per cycle):

- Keyword map: primary/secondary/branded keywords → target URL
- Service-area plan: which cities get location pages this cycle
- SERP feature targets: local pack/maps/FAQ/reviews/sitelinks
- KPI targets + cadence (weekly/monthly)

Agent profile (optional): `LOCAL_SEO_STRATEGIST` (see `.codex-swarm/agents/LOCAL_SEO_STRATEGIST.json`)

### Competitor and SERP Analyst

Mission: summarize SERP patterns and competitor gaps from approved exports without fabricating data.

Inputs required:

- Approved SERP exports/screenshots/URLs + timestamps
- Approved competitor set (domains)
- Keyword list + target locations

Outputs (per cycle):

- SERP pattern notes (local pack presence, common page types, FAQ usage)
- Competitor gap list (services, cities, FAQs, offers) backed by sources
- Recommended content angles (non-claims) for the next cycle

Agent profile (optional): `SERP_ANALYST` (see `.codex-swarm/agents/SERP_ANALYST.json`)

### GBP Optimizer

Mission: keep the Google Business Profile complete, accurate, and active.

Inputs required:

- Approved NAP/hours/services/categories/attributes
- Approved photos/media list
- Approved posting cadence and offers (if any)

Outputs (per cycle):

- GBP update checklist (fields to update + approvals required)
- GBP post plan (dates, city/service rotation, UTMs)
- Risk flags (unverified claims, inconsistent NAP)

Agent profile (optional): `GBP_OPTIMIZER` (see `.codex-swarm/agents/GBP_OPTIMIZER.json`)

### Content Planner

Mission: convert strategy + insights into a concrete set of content briefs.

Inputs required:

- Keyword map + target URLs
- Service briefs + approved FAQs/proof points
- SERP insights + feature targets

Outputs (per cycle):

- 1 service page brief
- 1 city/local landing brief
- 1 topical blog brief
- 14/30 day social plan brief (if in scope)

Agent profile (optional): `CONTENT_PLANNER_SEO` (see `.codex-swarm/agents/CONTENT_PLANNER_SEO.json`)

### Copywriter

Mission: draft pages and articles using templates, adding schema sections and internal links.

Inputs required:

- Page/article briefs
- Approved proof points + sources
- Approved NAP/service area list
- Template(s): `docs/client-templates/webpage-templates.md`, `docs/client-templates/article-templates.md`

Outputs (per cycle):

- Drafts with placeholders clearly marked when sources are missing
- Schema blocks included (LocalBusiness/Service/FAQPage/Article as relevant)

Agent profile (optional): `COPYWRITER_SEO` (see `.codex-swarm/agents/COPYWRITER_SEO.json`)

### Editor and Compliance

Mission: remove risk and tighten language; ensure NAP consistency; ensure claims are source-backed.

Inputs required:

- Drafts + source list
- Brand voice guidance (if any)
- Compliance constraints (no unverified superlatives, safety claims, etc.)

Outputs (per cycle):

- Edited drafts
- Risk log: any remaining placeholders, missing sources, or compliance issues

Agent profile (optional): `COMPLIANCE_EDITOR` (see `.codex-swarm/agents/COMPLIANCE_EDITOR.json`)

### Analytics and Reporting

Mission: produce a measurement snapshot and recommendations without inventing results.

Inputs required:

- Approved exports: rank tracker, GA4, GSC, GBP, call tracking (as available) + timestamps
- Keyword map + target URLs

Outputs (per cycle):

- Rank tracking summary + CSV link/attachment note
- Competitor snapshot + recommended next actions
- “What we’re doing next” plan tied to service priorities

Agent profile (optional): `ANALYTICS_REPORTING` (see `.codex-swarm/agents/ANALYTICS_REPORTING.json`)

## Handoff flow

1. Orchestrator sets sprint scope and acceptance criteria.
2. Local SEO Strategist sets target areas, services, and KPIs.
3. Service Researcher and Competitor and SERP Analyst supply briefs and insights.
4. Content Planner produces outlines and assigns Copywriter.
5. On-Page SEO Specialist adds metadata and internal link targets.
6. Editor and Compliance reviews drafts and flags risks.
7. GBP Optimizer and Citation Manager update local assets.
8. Technical SEO Auditor validates technical requirements.
9. Analytics and Reporting closes the loop with performance notes.

## Role guardrails

- Every claim must be traceable to approved inputs.
- No medical, legal, or safety claims beyond verified sources.
- Avoid location targeting without a verified service area list.
- Maintain consistent NAP data across all outputs.

## Required artifacts by role

- Orchestrator: sprint plan, acceptance criteria, handoff notes.
- Strategist: keyword map, service-area targets, KPIs.
- Service Researcher: service briefs with sources.
- SERP Analyst: insight summary and gap list.
- Content Planner: content roadmap and briefs.
- Copywriter: draft pages and articles.
- Editor and Compliance: final edits, risk log.
- On-Page SEO Specialist: metadata and internal links.
- GBP Optimizer: GBP update plan and posting schedule.
- Citation Manager: citation update log.
- Technical SEO Auditor: audit and fix list.
- Analytics and Reporting: monthly report and recommendations.
- Review and Reputation: response templates and escalation rules.
- Local Link Builder: outreach targets and tracking log.
