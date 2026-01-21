import unittest

from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import serp_dataforseo_fetch


class SerpDataForSeoFetchTests(unittest.TestCase):
    def test_build_tasks(self):
        payload = {
            "keywords": ["a", "b"],
            "location_name": "United States",
            "language_name": "English",
            "device": "desktop",
        }
        tasks = serp_dataforseo_fetch.build_tasks(payload)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]["keyword"], "a")
        self.assertEqual(tasks[0]["location_name"], "United States")

    def test_extract_items(self):
        response = {
            "tasks": [
                {
                    "data": {"keyword": "heater repair"},
                    "result": [
                        {
                            "items": [
                                {"type": "organic", "domain": "example.com", "url": "https://example.com"}
                            ]
                        }
                    ],
                }
            ]
        }
        items = serp_dataforseo_fetch.extract_items(response)
        self.assertEqual(items[0]["keyword"], "heater repair")
        self.assertEqual(items[0]["type"], "organic")


if __name__ == "__main__":
    unittest.main()
