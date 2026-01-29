# Article generator

Generate markdown articles from content briefs based on article templates.

## Purpose

Turn content briefs and approved inputs into draft-ready markdown articles for both:
- Service-area landing articles (localized service content)
- Topical service guides (educational evergreen content)

Articles follow the templates defined in `@docs/client-templates/article-templates.md`.

## Usage

### Scaffold input file

```bash
python scripts/generators/article_generator.py --client-slug <client> --scaffold
```

Creates `data/outputs/<client>/reports/article-input.json` with template structure.

### Generate articles

```bash
python scripts/generators/article_generator.py --client-slug <client>
```

Reads `data/outputs/<client>/reports/article-input.json` and generates:
- `data/outputs/<client>/articles/*.md` (one markdown file per article)
- `data/outputs/<client>/reports/articles.json` (summary JSON)

## Input JSON format

Store at: `data/outputs/<client>/reports/article-input.json`

```json
{
  "client": {
    "name": "Client Name",
    "website": "https://example.com",
    "phone": "(555) 123-4567",
    "hours": "Monday-Friday 8am-5pm"
  },
  "articles": [
    {
      "id": "hvac-repair-denver",
      "type": "service-area-landing",
      "service": "HVAC Repair",
      "city": "Denver",
      "primary_keyword": "hvac repair denver",
      "secondary_keywords": ["furnace repair", "ac repair"],
      "target_url": "/hvac-repair-denver",
      "content_brief": "hvac-repair-brief",
      "proof_points": [
        "Licensed and insured",
        "24/7 emergency service"
      ],
      "service_areas": ["Downtown", "Capitol Hill"],
      "internal_links": {
        "service_page": "/services/hvac-repair",
        "contact_page": "/contact"
      },
      "notes": "Focus on emergency capabilities"
    },
    {
      "id": "hvac-maintenance-guide",
      "type": "topical-guide",
      "topic": "HVAC Maintenance",
      "primary_keyword": "hvac maintenance tips",
      "secondary_keywords": ["furnace maintenance"],
      "target_url": "/hvac-maintenance-guide",
      "content_brief": "maintenance-brief",
      "internal_links": {
        "service_page": "/services/maintenance",
        "contact_page": "/contact"
      },
      "notes": "Educational content for homeowners"
    }
  ]
}
```

## Article types

### service-area-landing

Localized service content targeting a specific city or area. Includes:
- Title + intro with local context
- Service scope
- Local considerations and service areas
- Common local issues
- Why choose us (proof points)
- FAQs
- Call to action
- Metadata: LocalBusiness, Service, FAQPage schema

### topical-guide

Evergreen educational content. Includes:
- Title + intro
- Key takeaways
- Core concept explanation
- Step-by-step guide
- Common mistakes
- When to call a professional
- FAQs
- Call to action
- Metadata: Article, FAQPage schema

## Content brief integration

If you specify a `content_brief` field pointing to an existing content brief (in `data/outputs/<client>/reports/content-briefs/`), the generator will:
- Extract service, city, topic, keywords
- Pull FAQs for inclusion
- Use proof points if available

If no content brief is specified, the generator uses only the data in the article input JSON.

## Outputs

Generated articles contain:
- Structured markdown following templates
- Placeholder text for manual editing (marked with `[...]`)
- Metadata section with title tag, meta description, schema types
- Internal link recommendations

## Workflow

1. Generate or have content briefs available (optional)
2. Scaffold article input: `--scaffold`
3. Fill in article-input.json with approved data
4. Generate articles
5. Review and edit markdown files to:
   - Replace placeholders with approved content
   - Verify all facts against approved inputs
   - Add actual FAQ questions and answers
   - Complete local considerations and proof points
6. Validate with draft compliance lint before publishing

## Notes

- All business facts (NAP, hours, proof points) must come from approved inputs
- Articles are starting points requiring manual review and completion
- Use article templates (`@docs/client-templates/article-templates.md`) as the source of truth for structure
- Schema types noted in metadata must be implemented separately
