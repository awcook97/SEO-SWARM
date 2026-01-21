import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import ga4_export_ingest


class Ga4ExportIngestTests(unittest.TestCase):
    def test_summary_totals(self):
        csv_content = "\n".join(
            [
                "Page path,Users,Sessions,Conversions,Session source",
                "/home,100,120,5,google",
                "/contact,50,60,2,google",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "ga4.csv"
            path.write_text(csv_content, encoding="utf-8")
            rows = ga4_export_ingest.normalize_rows(ga4_export_ingest.load_csv(path))

        summary = ga4_export_ingest.build_summary(rows)
        self.assertEqual(summary["totals"]["users"], 150.0)
        self.assertEqual(summary["totals"]["conversions"], 7.0)
        self.assertEqual(summary["top_pages"][0]["name"], "/home")


if __name__ == "__main__":
    unittest.main()
