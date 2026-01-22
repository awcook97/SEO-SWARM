# Review response templates

## Purpose

Provide templated responses for reviews, covering both positive feedback and issues.

## Inputs

- `data/outputs/<client>/reports/review-templates-input.json`
- Review export (CSV/JSON) via `scripts/ingest/review_export_ingest.py`

## Command

```bash
python scripts/generators/review_response_templates.py --client-slug <client>
```

Scaffold an input file with `--scaffold`, then fill in actual reviews and issue flags.

To generate the input from an export:

```bash
python scripts/ingest/review_export_ingest.py --client-slug <client> --input path/to/reviews.csv
```

## Outputs

- `data/outputs/<client>/reports/review-response-templates.md`
- `data/outputs/<client>/reports/review-response-templates.json`

## Notes

- Templates surface tone guidance and highlight approved issues/next steps.
- Use the JSON for automation or CRM push to the review response owner.
