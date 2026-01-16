import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import review_response_templates


class ReviewResponseTemplatesTests(unittest.TestCase):
    def test_parse_and_render(self):
        data = {
            "client": {"name": "Client"},
            "reviews": [
                {
                    "reviewer": "Alex",
                    "rating": 4,
                    "platform": "Google",
                    "date": "2026-01-03",
                    "summary": "Great job",
                    "issues": [],
                }
            ],
        }
        entries = review_response_templates.parse_reviews(data)
        self.assertEqual(len(entries), 1)
        md = review_response_templates.render_markdown(data["client"], entries)
        self.assertIn("Review response templates", md)

    def test_scaffold_input(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "review-templates-input.json"
            review_response_templates.scaffold_input(path)
            data = review_response_templates.load_input(path)
            entries = review_response_templates.parse_reviews(data)
            self.assertTrue(entries)


if __name__ == "__main__":
    unittest.main()
