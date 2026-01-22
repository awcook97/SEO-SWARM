# inputs.md from schema

## Purpose

Generate `data/outputs/<client>/inputs.md` from a JSON-LD schema snippet.
This pulls business name, phone, URL, address, description, and geo when available.

## Command

```bash
python scripts/inputs_from_schema.py --schema path/to/schema.json --client-slug <client>
```

## Notes

- This only scaffolds what the schema includes.
- You must still add services, hours, proof points, and other approved inputs.
