# Release checklist (publish-ready)

Use this checklist before publishing the repo.

## Content readiness

- All placeholders in client drafts are filled with approved inputs.
- Schema is included on every page and article.
- Claims and proof points are source-verified.

## Repo hygiene

- `outputs/` is ignored and contains no committed client data.
- Root README is accurate and up to date.
- Measurement specs and templates are linked from @docs/seo/README.md.

## Workflow sanity

- `python scripts/swarm_workflow.py --help` runs without error.
- Task list has no TODOs or missing deps.

## Optional release steps

- Tag a release version.
- Add a LICENSE if publishing publicly.
