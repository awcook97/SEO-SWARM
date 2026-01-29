import tempfile
import unittest
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.generators import article_cache_to_markdown


ARTICLE_HTML_SAMPLE = """
<!DOCTYPE html>
<html>
<head>
    <title>HVAC Maintenance Tips for Winter | Denver HVAC Blog</title>
    <meta name="description" content="Learn essential HVAC maintenance tips for winter months.">
    <meta name="author" content="John Smith">
    <link rel="canonical" href="https://example.com/blog/hvac-maintenance-tips">
    <meta property="og:type" content="article">
    <meta property="og:title" content="HVAC Maintenance Tips for Winter">
    <meta property="og:description" content="Keep your HVAC system running smoothly.">
    <meta property="og:image" content="https://example.com/images/hvac.jpg">
    <meta property="article:published_time" content="2024-01-15T10:00:00Z">
    <meta property="article:modified_time" content="2024-01-20T14:30:00Z">
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "author": {
            "@type": "Person",
            "name": "John Smith"
        }
    }
    </script>
</head>
<body>
    <article>
        <h1>HVAC Maintenance Tips for Winter</h1>
        <p>Winter is coming and your HVAC system needs proper maintenance to keep your home comfortable.</p>
        <h2>Why Winter Maintenance Matters</h2>
        <p>Regular maintenance can prevent costly repairs and improve energy efficiency during the cold months.</p>
        <h2>Essential Maintenance Tasks</h2>
        <p>Here are the key tasks you should complete before winter arrives to ensure optimal performance.</p>
        <h3>Change Your Air Filter</h3>
        <p>A clean air filter is crucial for proper airflow and system efficiency throughout the heating season.</p>
        <img src="https://example.com/images/filter.jpg" alt="Air filter">
        <a href="/services/maintenance">Learn about our maintenance services</a>
        <a href="/contact">Contact us for help</a>
    </article>
</body>
</html>
"""


class ArticleCacheToMarkdownTests(unittest.TestCase):
    def test_is_article_page(self):
        self.assertTrue(article_cache_to_markdown.is_article_page("https://example.com/blog/post-1"))
        self.assertTrue(article_cache_to_markdown.is_article_page("https://example.com/article/news"))
        self.assertTrue(article_cache_to_markdown.is_article_page("https://example.com/resources/guide"))
        self.assertFalse(article_cache_to_markdown.is_article_page("https://example.com/services/hvac"))
        self.assertFalse(article_cache_to_markdown.is_article_page("https://example.com/about"))

    def test_parse_html(self):
        article = article_cache_to_markdown.parse_html(
            ARTICLE_HTML_SAMPLE, "https://example.com/blog/hvac-maintenance-tips"
        )
        
        self.assertEqual(article.url, "https://example.com/blog/hvac-maintenance-tips")
        self.assertEqual(article.title, "HVAC Maintenance Tips for Winter | Denver HVAC Blog")
        self.assertEqual(article.h1, "HVAC Maintenance Tips for Winter")
        self.assertEqual(article.meta_description, "Learn essential HVAC maintenance tips for winter months.")
        self.assertEqual(article.canonical_url, "https://example.com/blog/hvac-maintenance-tips")
        self.assertEqual(article.og_type, "article")
        self.assertEqual(article.og_title, "HVAC Maintenance Tips for Winter")
        self.assertEqual(article.published_date, "2024-01-15T10:00:00Z")
        self.assertEqual(article.modified_date, "2024-01-20T14:30:00Z")
        self.assertEqual(article.author, "John Smith")
        self.assertIn("BlogPosting", article.schema_types)
        self.assertGreater(len(article.content_paragraphs), 0)
        self.assertIn("Why Winter Maintenance Matters", article.headings)
        self.assertGreater(len(article.images), 0)
        self.assertGreater(len(article.internal_links), 0)
        self.assertGreater(len(article.full_content), 0)

    def test_render_markdown(self):
        article = article_cache_to_markdown.parse_html(
            ARTICLE_HTML_SAMPLE, "https://example.com/blog/hvac-maintenance-tips"
        )
        markdown = article_cache_to_markdown.render_markdown(article)
        
        self.assertIn("# HVAC Maintenance Tips for Winter", markdown)
        self.assertIn("**Source:** https://example.com/blog/hvac-maintenance-tips", markdown)
        self.assertIn("**Author:** John Smith", markdown)
        self.assertIn("**Published:** 2024-01-15T10:00:00Z", markdown)
        self.assertIn("## Metadata", markdown)
        self.assertIn("## Why Winter Maintenance Matters", markdown)
        self.assertIn("### Change Your Air Filter", markdown)
        self.assertIn("Winter is coming", markdown)

    def test_load_cache(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            index_path = Path(tmpdir) / "index.json"
            html_path = Path(tmpdir) / "page1.html"
            html_path.write_text("<html></html>", encoding="utf-8")
            
            index_data = {
                "https://example.com/blog/post": {
                    "path": str(html_path),
                    "fetched_at": "2024-01-01T00:00:00Z"
                }
            }
            index_path.write_text(article_cache_to_markdown.json.dumps(index_data), encoding="utf-8")
            
            cache = article_cache_to_markdown.load_cache(index_path)
            
            self.assertIn("https://example.com/blog/post", cache)
            self.assertEqual(cache["https://example.com/blog/post"], html_path)


if __name__ == "__main__":
    unittest.main()
