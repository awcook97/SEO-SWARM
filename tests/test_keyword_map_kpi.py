import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import keyword_map_kpi


class KeywordMapKpiTests(unittest.TestCase):
    def test_scaffold_and_parse(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            input_path = base / "keyword-map-input.json"
            keyword_map_kpi.scaffold_input(input_path)

            data = keyword_map_kpi.load_input(input_path)
            self.assertIn("keywords", data)
            entries = keyword_map_kpi.parse_keywords(data["keywords"])
            self.assertTrue(entries)

    def test_parse_requires_keyword_and_target(self):
        with self.assertRaises(SystemExit):
            keyword_map_kpi.parse_keywords([{"keyword": "test"}])


if __name__ == "__main__":
    unittest.main()
