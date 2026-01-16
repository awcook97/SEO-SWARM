import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import inputs_from_schema


class InputsFromSchemaTests(unittest.TestCase):
    def test_parse_schema(self):
        data = {
            "name": "Guilded Plumbing",
            "url": "https://example.com",
            "telephone": "(555) 111-2222",
            "description": "Plumbing in Guthrie",
            "address": {
                "streetAddress": "123 Main St",
                "addressLocality": "Guthrie",
                "addressRegion": "OK",
                "postalCode": "73044",
                "addressCountry": "US",
            },
            "geo": {"latitude": "35.0", "longitude": "-97.0"},
        }
        profile = inputs_from_schema.parse_schema(data)
        self.assertEqual(profile.name, "Guilded Plumbing")
        self.assertEqual(profile.address["city"], "Guthrie")
        self.assertEqual(profile.geo["lat"], "35.0")

    def test_render_inputs(self):
        profile = inputs_from_schema.SchemaProfile(
            name="Test",
            url="https://example.com",
            telephone="(555) 111-2222",
            description="Test desc",
            address={"line1": "123 Main", "city": "Town", "region": "TX", "postal": "77001", "country": "US"},
            geo={"lat": "1.0", "lng": "2.0"},
        )
        content = inputs_from_schema.render_inputs(profile)
        self.assertIn("Approved business facts", content)
        self.assertIn("Geo latitude", content)

    def test_load_schema_missing(self):
        with self.assertRaises(SystemExit):
            inputs_from_schema.load_schema(Path("missing.json"))


if __name__ == "__main__":
    unittest.main()
