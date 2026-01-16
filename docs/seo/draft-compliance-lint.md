# Draft compliance lint

## Purpose

Scan draft markdown files for placeholders and risky claims before publishing.

## Inputs

- Drafts under `outputs/<client>/pages/*.md` and `outputs/<client>/articles/*.md`.

## Command

```bash
python scripts/draft_compliance_lint.py --client-slug <client>
```

Optional: limit to specific folders or files.

```bash
python scripts/draft_compliance_lint.py --client-slug <client> --paths pages articles
```

## Outputs

- `outputs/<client>/reports/draft-compliance-lint.md`
- `outputs/<client>/reports/draft-compliance-lint.json`

## Notes

- Placeholders like `[Primary Service]` must be replaced with approved inputs.
- Claims such as "best" or "#1" require verified sources.
