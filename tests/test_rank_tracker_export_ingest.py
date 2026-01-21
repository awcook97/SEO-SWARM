import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import rank_tracker_export_ingest


class RankTrackerExportIngestTests(unittest.TestCase):
    def test_normalize_rows(self):
        csv_content = "\n".join(
            [
                "Keyword,Current Rank,Previous Rank,Best Rank,URL,Notes",
                "heater repair,3,5,1,https://example.com/heater,steady",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "rank.csv"
            path.write_text(csv_content, encoding="utf-8")
            headers, rows = rank_tracker_export_ingest.load_csv(path)
            mapping = rank_tracker_export_ingest.map_headers(headers)
            normalized = rank_tracker_export_ingest.normalize_rows(rows, mapping)

        self.assertEqual(normalized[0]["keyword"], "heater repair")
        self.assertEqual(normalized[0]["current_rank"], "3")
        self.assertEqual(normalized[0]["previous_rank"], "5")
        self.assertEqual(normalized[0]["target_url"], "https://example.com/heater")


if __name__ == "__main__":
    unittest.main()
