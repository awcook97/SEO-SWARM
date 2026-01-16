# Local link outreach log

## Purpose

Maintain a log of outreach targets for local partners, events, or publications, including status and ownership.

## Inputs

- `outputs/<client>/reports/local-link-input.json`
- Required fields: `organization`, `contact`, `priority`, `target_url`, `status`.

## Command

```bash
python scripts/local_link_outreach.py --client-slug <client>
```

Create a scaffold input with `--scaffold` and fill in approved partners before running.

## Outputs

- `outputs/<client>/reports/local-link-outreach.md`
- `outputs/<client>/reports/local-link-outreach.json`

## Notes

- The markdown report includes counts per status for quick triage.
- Use the JSON file to automate follow-ups or integrate with link tracking tools.
