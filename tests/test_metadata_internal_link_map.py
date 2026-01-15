import json
import unittest
from pathlib import Path

from scripts.metadata_internal_link_map import build_page_entry, parse_client, parse_defaults


class MetadataInternalLinkMapTests(unittest.TestCase):
    def setUp(self):
        data = json.loads(Path("tests/fixtures/metadata_linkmap_input.json").read_text(encoding="utf-8"))
        self.client = parse_client(data)
        self.defaults = parse_defaults(data)
        self.pages = data["pages"]

    def test_service_page_metadata_and_links(self):
        entry = build_page_entry(self.pages[0], self.client, self.defaults)
        self.assertEqual(entry["metadata"]["title_tag"], "Air Duct Services | HighPoint HVAC")
        self.assertIn("Call (720) 277-6586", entry["metadata"]["meta_description"])
        self.assertIn("FAQPage", entry["metadata"]["schema_types"])
        link_urls = {link["url"] for link in entry["internal_links"]}
        self.assertIn("/services/dryer-vent", link_urls)
        self.assertIn("/service-areas/denver", link_urls)
        self.assertIn("/maintenance-plans", link_urls)

    def test_local_landing_metadata_includes_proof_point(self):
        entry = build_page_entry(self.pages[1], self.client, self.defaults)
        self.assertIn("Same-day availability", entry["metadata"]["meta_description"])
        self.assertEqual(entry["metadata"]["title_tag"], "Air Duct Services in Denver | HighPoint HVAC")
        link_urls = {link["url"] for link in entry["internal_links"]}
        self.assertIn("/services", link_urls)
        self.assertIn("/contact", link_urls)
        self.assertIn("/blog", link_urls)

    def test_topical_guide_defaults(self):
        entry = build_page_entry(self.pages[2], self.client, self.defaults)
        self.assertEqual(entry["metadata"]["title_tag"], "Air Duct Cleaning | HighPoint HVAC")
        link_urls = {link["url"] for link in entry["internal_links"]}
        self.assertIn("/services/air-duct", link_urls)
        self.assertIn("/contact", link_urls)


if __name__ == "__main__":
    unittest.main()
