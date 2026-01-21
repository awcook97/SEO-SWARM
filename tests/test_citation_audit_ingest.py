import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import citation_audit_ingest


class CitationAuditIngestTests(unittest.TestCase):
    def test_build_citations(self):
        csv_content = "\n".join(
            [
                "Platform,Listing URL,Status,Notes",
                "Yelp,https://yelp.com/biz/example,Needs update,Fix phone",
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "citations.csv"
            path.write_text(csv_content, encoding="utf-8")
            rows = citation_audit_ingest.load_csv(path)
            citations = citation_audit_ingest.build_citations(rows)

        self.assertEqual(citations[0]["platform"], "Yelp")
        self.assertEqual(citations[0]["status"], "Needs update")


if __name__ == "__main__":
    unittest.main()
