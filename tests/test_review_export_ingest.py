import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import review_export_ingest


class ReviewExportIngestTests(unittest.TestCase):
    def test_build_reviews_from_csv(self):
        csv_content = "\n".join(
            [
                "Reviewer,Rating,Platform,Date,Summary,Issues",
                "Jamie,5,Google,2026-01-02,Quick response,",
                "Riley,2,Yelp,2026-01-03,Long wait,late arrival;billing",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "reviews.csv"
            path.write_text(csv_content, encoding="utf-8")
            rows = review_export_ingest.load_csv(path)
            reviews = review_export_ingest.build_reviews(rows)

        self.assertEqual(len(reviews), 2)
        self.assertEqual(reviews[0]["reviewer"], "Jamie")
        self.assertEqual(reviews[0]["rating"], 5)
        self.assertEqual(reviews[1]["issues"], ["late arrival", "billing"])


if __name__ == "__main__":
    unittest.main()
