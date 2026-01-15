import json
import unittest
from pathlib import Path

from scripts.internal_link_validator import validate_page


class InternalLinkValidatorTests(unittest.TestCase):
    def setUp(self):
        data = json.loads(Path("tests/fixtures/internal_link_map_output.json").read_text(encoding="utf-8"))
        self.pages = data["pages"]

    def test_service_page_passes(self):
        result = validate_page(self.pages[0])
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["issues"], [])

    def test_local_landing_missing_related_service(self):
        result = validate_page(self.pages[1])
        kinds = {issue["kind"] for issue in result["issues"]}
        self.assertIn("missing-target", kinds)
        self.assertIn("missing-required", kinds)
        self.assertEqual(result["status"], "fail")

    def test_topical_guide_placeholder_contact(self):
        result = validate_page(self.pages[2])
        kinds = {issue["kind"] for issue in result["issues"]}
        self.assertIn("placeholder-url", kinds)
        self.assertEqual(result["status"], "fail")


if __name__ == "__main__":
    unittest.main()
