# Measurement intake generation

## Purpose

Turn structured measurement inputs into a markdown intake sheet for swarms.

## Inputs

- `data/outputs/<client>/reports/measurement-intake-input.json`
- Include client profile, services, keywords, measurement cadence/tools, alerts, and service areas.

## Command

```bash
python scripts/measurement_intake_generator.py --client-slug <client>
```

Use `--scaffold` to generate an example input file you can edit.

## Outputs

- `data/outputs/<client>/reports/measurement-intake.md`
- `data/outputs/<client>/reports/measurement-intake.json`

## Notes

- This automates the front page of the measurement intake template and keeps the JSON for integrations.
