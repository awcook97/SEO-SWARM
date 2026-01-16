import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import local_link_outreach


class LocalLinkOutreachTests(unittest.TestCase):
    def test_parse_and_render(self):
        data = {
            "client": {"name": "Test Client"},
            "targets": [
                {
                    "organization": "Library",
                    "contact": "info@library.example",
                    "priority": "high",
                    "target_url": "/community",
                    "status": "contacted",
                    "last_touch": "2026-01-02",
                    "notes": "Follow up next week.",
                }
            ],
        }
        targets = local_link_outreach.parse_targets(data)
        self.assertEqual(len(targets), 1)
        md = local_link_outreach.render_markdown(data["client"], targets)
        self.assertIn("Library", md)
        self.assertIn("Status counts", md)

    def test_scaffold_input(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "local-link-input.json"
            local_link_outreach.scaffold_input(path)
            data = local_link_outreach.load_input(path)
            targets = local_link_outreach.parse_targets(data)
            self.assertTrue(targets)


if __name__ == "__main__":
    unittest.main()
