import unittest

from scripts import technical_seo_audit_scaffold


class TechnicalSeoAuditScaffoldTests(unittest.TestCase):
    def test_render_markdown_contains_sections(self):
        content = technical_seo_audit_scaffold.render_markdown("client-slug")
        self.assertIn("## Indexation", content)
        self.assertIn("## Structured data", content)


if __name__ == "__main__":
    unittest.main()
