# Citation update log

## Purpose

Track citation updates with statuses, owners, and action dates for each listing.

## Inputs

- `data/outputs/<client>/reports/citation-log-input.json`
- Each entry requires `platform`, `listing_url`, and `status`.

## Command

```bash
python scripts/generators/citation_update_log.py --client-slug <client>
```

Create a scaffold file via `--scaffold` and fill in approved listings before running.

## Outputs

- `data/outputs/<client>/reports/citation-update-log.md`
- `data/outputs/<client>/reports/citation-update-log.json`

## Notes

- The markdown output includes a status summary for quick review.
- Use the JSON for automation or integrations with citation trackers.
