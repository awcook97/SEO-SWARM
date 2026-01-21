import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import crawl_export_ingest


class CrawlExportIngestTests(unittest.TestCase):
    def test_normalize_rows(self):
        csv_content = "\n".join(
            [
                "URL,Status Code,Title,H1,Word Count",
                "https://example.com,200,Home,Welcome,120",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "crawl.csv"
            path.write_text(csv_content, encoding="utf-8")
            rows = crawl_export_ingest.normalize_rows(crawl_export_ingest.load_csv(path))

        self.assertEqual(rows[0]["status_code"], 200)
        self.assertEqual(rows[0]["word_count"], 120)


if __name__ == "__main__":
    unittest.main()
