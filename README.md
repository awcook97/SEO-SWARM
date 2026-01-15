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

## Usage

1) Collect approved inputs using @docs/seo/measurement-intake-template.md.
2) Produce content using the templates under @docs/client-templates/.
3) Use @scripts/swarm_workflow.py to scaffold a client output folder.

Example:

```bash
python scripts/swarm_workflow.py --client "Example HVAC" --slug example-hvac
```

## Notes

- Client outputs are intentionally ignored from git (`outputs/` in `.gitignore`).
- Replace all placeholders with approved inputs before publishing.
