import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.generators import article_generator


CONTENT_BRIEF_SAMPLE = """
# Content brief: sample-brief

Generated: 2024-01-01T00:00:00+00:00

## Target page
- Type: service-page
- Service: Air Duct Cleaning
- City: Denver
- Topic: [topic]
- Primary keyword: air duct cleaning denver
- Secondary keywords: duct cleaning, hvac maintenance
- Target URL: /air-duct-cleaning
- Audience intent: book service
- Primary CTA: Call now

## Brief inputs
- Service brief source: air-duct-services
- Notes: Focus on preventive maintenance

## FAQs to include
- Q: How often should I clean my air ducts?
  A: Every 3-5 years is recommended.
- Q: What are signs my ducts need cleaning?
  A: Dust buildup and reduced airflow.
"""


class ArticleGeneratorTests(unittest.TestCase):
    def test_scaffold_input(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "article-input.json"
            article_generator.scaffold_input(output_path)

            data = article_generator.load_input(output_path)
            self.assertIn("client", data)
            self.assertIn("articles", data)
            self.assertEqual(len(data["articles"]), 2)
            self.assertEqual(data["articles"][0]["type"], "service-area-landing")
            self.assertEqual(data["articles"][1]["type"], "topical-guide")

    def test_load_brief(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            briefs_dir = Path(tmpdir)
            brief_path = briefs_dir / "sample-brief.md"
            brief_path.write_text(CONTENT_BRIEF_SAMPLE, encoding="utf-8")

            snapshot = article_generator.load_brief(briefs_dir, "sample-brief")

            self.assertIsNotNone(snapshot)
            self.assertEqual(snapshot.service, "Air Duct Cleaning")
            self.assertEqual(snapshot.city, "Denver")
            self.assertEqual(snapshot.primary_keyword, "air duct cleaning denver")
            self.assertIn("duct cleaning", snapshot.secondary_keywords)
            self.assertEqual(snapshot.target_url, "/air-duct-cleaning")
            self.assertEqual(snapshot.intent, "book service")
            self.assertEqual(snapshot.cta, "Call now")

    def test_render_service_area_article(self):
        entry = {
            "id": "test-article",
            "type": "service-area-landing",
            "service": "HVAC Repair",
            "city": "Denver",
            "primary_keyword": "hvac repair denver",
            "proof_points": ["Licensed and insured", "24/7 emergency service"],
            "service_areas": ["Downtown", "Capitol Hill"],
            "internal_links": {"service_page": "/hvac-repair", "contact_page": "/contact"},
        }
        client = {"name": "Test HVAC", "phone": "(555) 123-4567", "hours": "Mon-Fri 8am-5pm"}

        content = article_generator.render_service_area_article(entry, client, None)

        self.assertIn("HVAC Repair in Denver", content)
        self.assertIn("Test HVAC", content)
        self.assertIn("(555) 123-4567", content)
        self.assertIn("Licensed and insured", content)
        self.assertIn("24/7 emergency service", content)
        self.assertIn("Downtown", content)
        self.assertIn("Capitol Hill", content)
        self.assertIn("LocalBusiness", content)
        self.assertIn("FAQPage", content)

    def test_render_topical_guide(self):
        entry = {
            "id": "test-guide",
            "type": "topical-guide",
            "topic": "HVAC Maintenance",
            "primary_keyword": "hvac maintenance tips",
            "internal_links": {"service_page": "/maintenance", "contact_page": "/contact"},
        }
        client = {"name": "Test HVAC", "phone": "(555) 123-4567", "hours": "Mon-Fri 8am-5pm"}

        content = article_generator.render_topical_guide(entry, client, None)

        self.assertIn("HVAC Maintenance for Homeowners", content)
        self.assertIn("Test HVAC", content)
        self.assertIn("(555) 123-4567", content)
        self.assertIn("Key Takeaways", content)
        self.assertIn("Step-by-Step Guide", content)
        self.assertIn("Common Mistakes to Avoid", content)
        self.assertIn("When to Call a Professional", content)
        self.assertIn("Article", content)
        self.assertIn("FAQPage", content)


if __name__ == "__main__":
    unittest.main()
