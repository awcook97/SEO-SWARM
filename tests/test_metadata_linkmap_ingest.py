import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import metadata_linkmap_ingest


class MetadataLinkmapIngestTests(unittest.TestCase):
    def test_build_pages(self):
        csv_content = "\n".join(
            [
                "Type,Slug,Service,Related Services,Internal Links,Include FAQ Schema",
                "service-page,air-duct,Air Duct Services,Dryer Vent Services,Blog|/blog|supporting,true",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "pages.csv"
            path.write_text(csv_content, encoding="utf-8")
            rows = metadata_linkmap_ingest.load_csv(path)
            pages = metadata_linkmap_ingest.build_pages(rows)

        self.assertEqual(pages[0]["service"], "Air Duct Services")
        self.assertTrue(pages[0]["include_faq_schema"])
        self.assertEqual(pages[0]["internal_links"][0]["url"], "/blog")


if __name__ == "__main__":
    unittest.main()
