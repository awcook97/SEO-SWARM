# Content brief workflow

This workflow produces consistent markdown content briefs using service brief inputs.
All business facts must come from approved inputs.

## 5-step brief workflow

1) Collect inputs
- Generate service briefs: `data/outputs/<client>/reports/service-briefs/*.md`.
- Prepare a brief input file (JSON) for the target pages.

2) Scaffold brief input (optional)

```bash
python scripts/generators/content_brief_generator.py --client-slug <client> --scaffold
```

Fill in `data/outputs/<client>/reports/content-brief-input.json` with keywords, targets,
CTAs, and notes.

3) Generate briefs

```bash
python scripts/generators/content_brief_generator.py --client-slug <client>
```

4) Review and edit
- Replace placeholders and confirm facts against approved inputs.
- Adjust required sections or FAQs before handing off to drafting.

5) Handoff
- Provide briefs to Content Planner or Copywriter along with templates.
- Keep briefs in markdown; convert to other formats only when needed.

## Input JSON format

Store the input file at: `data/outputs/<client>/reports/content-brief-input.json`.

```json
{
  "client": {
    "name": "Client Name",
    "website": "https://example.com",
    "phone": "(000) 000-0000"
  },
  "briefs": [
    {
      "id": "service-page-air-duct",
      "type": "service-page",
      "slug": "air-duct-services",
      "service": "Air Duct Services",
      "city": "Denver",
      "topic": null,
      "primary_keyword": "air duct services denver",
      "secondary_keywords": ["duct cleaning", "hvac maintenance"],
      "target_url": "/air-duct-services",
      "intent": "book service",
      "cta": "Call now",
      "service_brief": "air-duct-services",
      "notes": "Focus on preventive maintenance benefits."
    }
  ]
}
```

## Outputs

- `data/outputs/<client>/reports/content-briefs/<brief-id>.md`
- `data/outputs/<client>/reports/content-briefs.json`

## Notes

- The generator pulls headings, CTAs, schema types, and FAQs from service briefs.
- Missing fields remain as placeholders for manual completion.
- Markdown is the default; conversion to .docx can be handled later if needed.
