import unittest
from pathlib import Path

from scripts.service_brief_generator import parse_html


class ServiceBriefGeneratorTests(unittest.TestCase):
    def test_parse_html_extracts_core_fields(self):
        html = Path("tests/fixtures/service_page.html").read_text(encoding="utf-8")
        brief = parse_html(html, "https://example.com/air-duct-services")

        self.assertIn("Front Range Air Duct Services", brief.title)
        self.assertEqual(brief.h1, "Front Range Air Duct Services")
        self.assertIn("Begin at $169", brief.meta_description)
        self.assertEqual(brief.canonical_url, "https://example.com/air-duct-services")
        self.assertIn("Front Range Air Duct Services", brief.og_title)
        self.assertIn("Front Range Air Duct Services", brief.twitter_title)
        self.assertIn("$169", brief.pricing_mentions)
        self.assertTrue(brief.value_props)
        self.assertTrue(brief.faqs)
        self.assertTrue(brief.cta_links)
        question, answer = brief.faqs[0]
        self.assertTrue(question.endswith("?"))
        self.assertTrue(len(answer) > 0)


if __name__ == "__main__":
    unittest.main()
