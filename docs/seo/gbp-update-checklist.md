# GBP update checklist generator

## Purpose

Generate a Google Business Profile update checklist and posting plan from
approved inputs. Use this to ensure GBP fields stay consistent with the
approved NAP, services, and profile details.

## Inputs

- `outputs/<client-slug>/inputs.md` with approved NAP, hours, service areas,
  profile details, and service list.

## Command

```bash
python scripts/gbp_update_checklist.py --client-slug <client-slug>
```

## Outputs

- `outputs/<client-slug>/reports/gbp-update-checklist.md`
- `outputs/<client-slug>/reports/gbp-update-checklist.json`

## Notes

- Missing approvals are listed under the risk flags section.
- Fill in cadence, offers, CTAs, assets, and UTMs before publishing posts.
