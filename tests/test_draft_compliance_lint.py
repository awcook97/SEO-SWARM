import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import draft_compliance_lint


class DraftComplianceLintTests(unittest.TestCase):
    def test_lint_file_finds_issues(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "draft.md"
            path.write_text(
                """
# Draft
- Primary service: [Primary Service]
- TODO: fill this in
We are the best in town.
""",
                encoding="utf-8",
            )

            issues = draft_compliance_lint.lint_file(path)
            kinds = {issue.kind for issue in issues}
            self.assertIn("placeholder", kinds)
            self.assertIn("todo", kinds)
            self.assertIn("claim", kinds)

    def test_iter_markdown_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "one.md").write_text("# One", encoding="utf-8")
            (base / "two.txt").write_text("ignore", encoding="utf-8")

            files = draft_compliance_lint.iter_markdown_files([base])
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].name, "one.md")

    def test_schema_and_nap_checks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            inputs = base / "inputs.md"
            inputs.write_text(
                "\n- Business name: GeoNova\n- Phone: (555) 111-2222\n",
                encoding="utf-8",
            )

            draft = base / "service-page.md"
            draft.write_text("# Draft without schema", encoding="utf-8")

            nap = draft_compliance_lint.parse_nap(inputs)
            issues = draft_compliance_lint.lint_file(draft, nap)
            kinds = {issue.kind for issue in issues}
            self.assertIn("schema_missing", kinds)
            self.assertIn("nap_missing", kinds)


if __name__ == "__main__":
    unittest.main()
