import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import citation_update_log


class CitationUpdateLogTests(unittest.TestCase):
    def test_parse_and_render(self):
        data = {
            "client": {"name": "Test Client"},
            "citations": [
                {
                    "platform": "Apple Maps",
                    "listing_url": "https://maps.apple.com/example",
                    "status": "Updated",
                    "action_date": "2026-01-01",
                    "owner": "Citations",
                    "notes": "Updated hours",
                }
            ],
        }
        entries = citation_update_log.parse_citations(data)
        self.assertEqual(len(entries), 1)
        md = citation_update_log.render_markdown(data["client"], entries)
        self.assertIn("Apple Maps", md)
        self.assertIn("Status summary", md)

    def test_scaffold_then_parse(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "citation-log-input.json"
            citation_update_log.scaffold_input(path)
            data = citation_update_log.load_input(path)
            entries = citation_update_log.parse_citations(data)
            self.assertTrue(entries)


if __name__ == "__main__":
    unittest.main()
