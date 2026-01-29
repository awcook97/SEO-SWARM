# Article cache to markdown

Extract blog/article pages from the site cache and convert them to markdown format.

## Purpose

Reads cached HTML from `data/outputs/<client>/reports/site-cache/` and extracts article/blog pages, converting them to structured markdown files. This is useful for:
- Reviewing existing blog content
- Creating content inventories
- Extracting article metadata and structure
- Analyzing competitor blog posts (if cached)

## Usage

```bash
python scripts/generators/article_cache_to_markdown.py --client-slug <client>
```

## Prerequisites

The site must be cached first using the crawl workflow:

```bash
python scripts/workflow/swarm_workflow.py --client "Client Name" --slug client-slug --site-url https://example.com
```

Or via the site audit runner:

```bash
python scripts/workflow/site_audit_runner.py --client "Client Name" --slug client-slug --site-url https://example.com --crawl-only
```

## How it works

The tool:
1. Reads the cache index at `data/outputs/<client>/reports/site-cache/index.json`
2. Identifies article pages by URL patterns: `/blog`, `/article`, `/post`, `/news`, `/resources`
3. Extracts article metadata and content from each HTML page
4. Converts to structured markdown format
5. Outputs to `data/outputs/<client>/articles/*.md`

## What gets extracted

For each article page, the tool extracts:

- **Metadata**: Title, meta description, canonical URL, Open Graph data
- **Author and dates**: Published date, modified date, author name
- **Full article content**: Complete article text with proper heading hierarchy preserved
- **Headings**: H2-H6 headings rendered with proper markdown levels
- **Paragraphs**: All article paragraphs in order
- **Lists**: Bulleted and numbered lists with all items
- **Blockquotes**: Quoted text formatted as markdown quotes
- **Code blocks**: Preformatted code sections
- **Images**: All images from the article
- **Internal links**: All internal links from the article content
- **Schema types**: JSON-LD structured data types (BlogPosting, Article, etc.)

## Output format

Each article is saved as a markdown file with the full content and proper structure:

```markdown
# Article Title

**Source:** https://example.com/blog/article-url
**Author:** Author Name
**Published:** 2024-01-15T10:00:00Z
**Modified:** 2024-01-20T14:30:00Z

---

Full article content with proper headings...

## Section Heading

Content paragraphs...

### Subsection

More content...

- List items
- Properly formatted

> Blockquotes preserved

---

## Metadata
- Page title, meta description, canonical URL
- Open Graph metadata
- Schema types

## Images
- List of image URLs

## Internal Links
- List of internal links
```

## Article identification

Pages are identified as articles if their URL contains:
- `/blog`
- `/article`
- `/post`
- `/news`
- `/resources`

If no articles are found, the tool will notify you and suggest checking URL patterns.

## Notes

- The cache stores service pages by default; blog pages may be excluded depending on crawl settings
- Output markdown files use URL slugs as filenames (e.g., `blog-hvac-tips.md`)
- Complete article content is extracted with full text and proper structure
- All timestamps are preserved from the original HTML metadata
- Internal links are relative URLs as found in the source HTML

## Related tools

- `service_brief_generator.py`: Extracts service pages from cache to markdown
- `inputs_from_site_cache.py`: Populates inputs.md from cached site data
- `crawl_cache.py`: Caches site HTML for offline processing
