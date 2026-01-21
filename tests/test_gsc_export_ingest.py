import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import gsc_export_ingest


class GscExportIngestTests(unittest.TestCase):
    def test_summary_totals(self):
        csv_content = "\n".join(
            [
                "Query,Page,Clicks,Impressions,CTR,Position",
                "plumber,/plumber,10,100,10%,3.2",
                "drain,/drain,5,50,10%,5.1",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "gsc.csv"
            path.write_text(csv_content, encoding="utf-8")
            rows = gsc_export_ingest.normalize_rows(gsc_export_ingest.load_csv(path))

        summary = gsc_export_ingest.build_summary(rows)
        self.assertEqual(summary["totals"]["clicks"], 15.0)
        self.assertEqual(summary["totals"]["impressions"], 150.0)
        self.assertEqual(summary["top_queries"][0]["name"], "plumber")


if __name__ == "__main__":
    unittest.main()
