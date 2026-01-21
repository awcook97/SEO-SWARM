import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import gbp_export_ingest


class GbpExportIngestTests(unittest.TestCase):
    def test_normalize_rows(self):
        csv_content = "\n".join(
            [
                "Date,Views,Searches,Calls,Website clicks",
                "2026-01-01,100,200,5,10",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "gbp.csv"
            path.write_text(csv_content, encoding="utf-8")
            _, rows = gbp_export_ingest.load_csv(path)
            normalized = gbp_export_ingest.normalize_rows(rows)

        self.assertEqual(normalized[0]["views"], 100.0)
        self.assertEqual(normalized[0]["calls"], 5.0)


if __name__ == "__main__":
    unittest.main()
