# Review response templates

## Purpose

Provide templated responses for reviews, covering both positive feedback and issues.

## Inputs

- `outputs/<client>/reports/review-templates-input.json`

## Command

```bash
python scripts/review_response_templates.py --client-slug <client>
```

Scaffold an input file with `--scaffold`, then fill in actual reviews and issue flags.

## Outputs

- `outputs/<client>/reports/review-response-templates.md`
- `outputs/<client>/reports/review-response-templates.json`

## Notes

- Templates surface tone guidance and highlight approved issues/next steps.
- Use the JSON for automation or CRM push to the review response owner.
