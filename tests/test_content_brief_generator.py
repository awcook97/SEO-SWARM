import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import content_brief_generator


SERVICE_BRIEF_SAMPLE = """
# Service Brief: Sample Service

## Source
- URL: https://example.com/sample
- Page title: Sample Service
- Meta description: Sample meta description.
- H1: Sample H1
- Pricing mentions: $100, $200

## Page structure
- H2/H3 headings: Intro, Process, FAQs

## Signals
### Value props (extracted)
- Value prop one.

### Proof points (extracted)
- Proof point one.

### CTAs (extracted)
- Call now

## Internal links (sampled)
- https://example.com/contact

## Schema types (detected)
- Service

## FAQs (extracted)
- Q: What is the service?
  A: It is a sample.
"""


class ContentBriefGeneratorTests(unittest.TestCase):
    def test_parse_service_brief(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.md"
            path.write_text(SERVICE_BRIEF_SAMPLE, encoding="utf-8")

            snapshot = content_brief_generator.parse_service_brief(path)

            self.assertEqual(snapshot.url, "https://example.com/sample")
            self.assertEqual(snapshot.h1, "Sample H1")
            self.assertIn("Intro", snapshot.headings)
            self.assertIn("Value prop one.", snapshot.value_props)
            self.assertIn("Proof point one.", snapshot.proof_points)
            self.assertIn("Call now", snapshot.ctas)
            self.assertIn("Service", snapshot.schema_types)
            self.assertEqual(len(snapshot.faqs), 1)

    def test_scaffold_input(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            briefs_dir = base / "briefs"
            briefs_dir.mkdir()
            (briefs_dir / "one.md").write_text("# Brief", encoding="utf-8")

            output_path = base / "content-brief-input.json"
            content_brief_generator.scaffold_input(briefs_dir, output_path)

            data = content_brief_generator.load_input(output_path)
            self.assertEqual(len(data["briefs"]), 1)
            self.assertEqual(data["briefs"][0]["service_brief"], "one")


if __name__ == "__main__":
    unittest.main()
