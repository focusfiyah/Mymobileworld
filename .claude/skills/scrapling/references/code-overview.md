# Code overview

**Contents:** Basic Usage · Spiders · Advanced Parsing & Navigation · Async Session Management Examples

Upstream SKILL.md, moved here unchanged.

Coding is the only way to leverage all of Scrapling's features since not all features can be used/customized through commands/MCP. Here's a quick overview of how to code with scrapling.

### Basic Usage
HTTP requests with session support
```python
from scrapling.fetchers import Fetcher, FetcherSession

with FetcherSession(impersonate='chrome') as session:  # Use latest version of Chrome's TLS fingerprint
    page = session.get('https://quotes.toscrape.com/', stealthy_headers=True)
    quotes = page.css('.quote .text::text').getall()

# Or use one-off requests
page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()
```
Advanced stealth mode
```python
from scrapling.fetchers import StealthyFetcher, StealthySession

with StealthySession(headless=True, solve_cloudflare=True) as session:  # Keep the browser open until you finish
    page = session.fetch('https://nopecha.com/demo/cloudflare', google_search=False)
    data = page.css('#padded_content a').getall()

# Or use one-off request style, it opens the browser for this request, then closes it after finishing
page = StealthyFetcher.fetch('https://nopecha.com/demo/cloudflare')
data = page.css('#padded_content a').getall()
```
Full browser automation
```python
from scrapling.fetchers import DynamicFetcher, DynamicSession

with DynamicSession(headless=True, disable_resources=False, network_idle=True) as session:  # Keep the browser open until you finish
    page = session.fetch('https://quotes.toscrape.com/', load_dom=False)
    data = page.xpath('//span[@class="text"]/text()').getall()  # XPath selector if you prefer it

# Or use one-off request style, it opens the browser for this request, then closes it after finishing
page = DynamicFetcher.fetch('https://quotes.toscrape.com/')
data = page.css('.quote .text::text').getall()
```

### Spiders
Build full crawlers with concurrent requests, multiple session types, and pause/resume:
```python
from scrapling.spiders import Spider, Request, Response

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]
    concurrent_requests = 10
    robots_txt_obey = True  # Respect robots.txt rules
    
    async def parse(self, response: Response):
        for quote in response.css('.quote'):
            yield {
                "text": quote.css('.text::text').get(),
                "author": quote.css('.author::text').get(),
            }
            
        next_page = response.css('.next a')
        if next_page:
            yield response.follow(next_page[0].attrib['href'])

result = QuotesSpider().start()
print(f"Scraped {len(result.items)} quotes")
result.items.to_json("quotes.json")
```
Use multiple session types in a single spider:
```python
from scrapling.spiders import Spider, Request, Response
from scrapling.fetchers import FetcherSession, AsyncStealthySession

class MultiSessionSpider(Spider):
    name = "multi"
    start_urls = ["https://example.com/"]
    
    def configure_sessions(self, manager):
        manager.add("fast", FetcherSession(impersonate="chrome"))
        manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)
    
    async def parse(self, response: Response):
        for link in response.css('a::attr(href)').getall():
            # Route protected pages through the stealth session
            if "protected" in link:
                yield Request(link, sid="stealth")
            else:
                yield Request(link, sid="fast", callback=self.parse)  # explicit callback
```
Pause and resume long crawls with checkpoints by running the spider like this:
```python
QuotesSpider(crawldir="./crawl_data").start()
```
Press Ctrl+C to pause gracefully - progress is saved automatically. Later, when you start the spider again, pass the same `crawldir`, and it will resume from where it stopped.

While iterating on a spider's `parse()` logic, set `development_mode = True` on the spider class to cache responses to disk on the first run and replay them on subsequent runs - so you can re-run the spider as many times as you want without re-hitting the target servers. The cache lives in `.scrapling_cache/{spider.name}/` by default and can be overridden with `development_cache_dir`. Don't ship a spider with this enabled.

For rules-based crawls (follow links matching a regex), use `CrawlSpider` instead of writing the link-extraction loop yourself:
```python
from scrapling.spiders import CrawlSpider, CrawlRule, LinkExtractor

class BlogCrawler(CrawlSpider):
    name = "blog"
    start_urls = ["https://example.com"]

    def rules(self):
        return [
            CrawlRule(LinkExtractor(allow=r"/posts/"), callback=self.parse_post),
            CrawlRule(LinkExtractor(allow=r"/page/\d+/")),  # follow pagination, no callback
        ]

    async def parse_post(self, response):
        yield {"title": response.css("h1::text").get()}
```
For sitemap-driven crawls, use `SitemapSpider` with the same `rules()` API. It fetches `sitemap_urls`, descends into sitemap indexes, and dispatches each URL through your rules. Put a `robots.txt` URL directly in `sitemap_urls` and the spider extracts each `Sitemap:` directive from it automatically. See `references/spiders/generic-templates.md` for the full reference, including `LinkExtractor`'s allow/deny/restrict_css/canonicalize options.

For XML feeds (RSS, Atom, product feeds), use `XMLFeedSpider`: set `itertag` to the node name and override `parse_node(response, node)`, which receives each matching node as a namespace-stripped `lxml` element (`node.findtext("title")`). For CSV feeds, use `CSVFeedSpider`: override `parse_row(response, row)`, which receives each row as a dictionary, with `headers`/`delimiter`/`quotechar` for non-standard feeds. Both decompress gzipped feeds automatically. See `references/spiders/generic-templates.md`.

For Shopify-powered stores, subclass `ShopifySpider` and set `target_website` to the store's domain; it extracts every product variant through Shopify's JSON API without touching the HTML. See `references/spiders/platform-templates.md`.

### Advanced Parsing & Navigation
```python
from scrapling.fetchers import Fetcher

# Rich element selection and navigation
page = Fetcher.get('https://quotes.toscrape.com/')

# Get quotes with multiple selection methods
quotes = page.css('.quote')  # CSS selector
quotes = page.xpath('//div[@class="quote"]')  # XPath
quotes = page.find_all('div', {'class': 'quote'})  # BeautifulSoup-style
# Same as
quotes = page.find_all('div', class_='quote')
quotes = page.find_all(['div'], class_='quote')
quotes = page.find_all(class_='quote')  # and so on...
# Find element by text content
quotes = page.find_by_text('quote', tag='div')

# Advanced navigation
quote_text = page.css('.quote')[0].css('.text::text').get()
quote_text = page.css('.quote').css('.text::text').getall()  # Chained selectors
first_quote = page.css('.quote')[0]
author = first_quote.next_sibling.css('.author::text')
parent_container = first_quote.parent

# Element relationships and similarity
similar_elements = first_quote.find_similar()
below_elements = first_quote.below_elements()
```
You can use the parser right away if you don't want to fetch websites like below:
```python
from scrapling.parser import Selector

page = Selector("<html>...</html>")
```
And it works precisely the same way!
### Async Session Management Examples
```python
import asyncio
from scrapling.fetchers import FetcherSession, AsyncStealthySession, AsyncDynamicSession

async with FetcherSession(http3=True) as session:  # `FetcherSession` is context-aware and can work in both sync/async patterns
    page1 = session.get('https://quotes.toscrape.com/')
    page2 = session.get('https://quotes.toscrape.com/', impersonate='firefox135')

# Async session usage
async with AsyncStealthySession(max_pages=2) as session:
    tasks = []
    urls = ['https://example.com/page1', 'https://example.com/page2']

    for url in urls:
        task = session.fetch(url)
        tasks.append(task)

    print(session.get_pool_stats())  # Optional - The status of the browser tabs pool (busy/free/error)
    results = await asyncio.gather(*tasks)
    print(session.get_pool_stats())

# Capture XHR/fetch API calls during page load
async with AsyncDynamicSession(capture_xhr=r"https://api\.example\.com/.*") as session:
    page = await session.fetch('https://example.com')
    for xhr in page.captured_xhr:  # Each is a full Response object
        print(xhr.url, xhr.status, xhr.body)
```
