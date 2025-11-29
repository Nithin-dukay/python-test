# python-test

A Python testing and automation repository with web scraping, browser automation, and connectivity checking utilities.

## Features

### 🕷️ Web Scraper Utility
A comprehensive web scraping tool that extracts content from web pages using both static (requests) and dynamic (Selenium) methods.

**Capabilities:**
- Extract text content from web pages
- Extract all links with automatic URL resolution
- Extract images with metadata
- Extract page metadata (title, meta tags, Open Graph data)
- Support for both static and JavaScript-rendered pages
- Rate limiting to be respectful to servers
- JSON export functionality
- Comprehensive statistics

**Usage:**
```bash
# Basic scraping (static content)
python web_scraper.py https://example.com

# Scrape dynamic content with Selenium
python web_scraper.py https://example.com --selenium

# Custom output file
python web_scraper.py https://example.com --output my_data.json

# Custom timeout and rate limiting
python web_scraper.py https://example.com --timeout 20 --rate-limit 2.0
```

**Programmatic Usage:**
```python
from web_scraper import WebScraper

# Create scraper instance
scraper = WebScraper(timeout=10, rate_limit=1.0)

# Scrape a page
result = scraper.scrape_page('https://example.com', use_selenium=False)

# Save to JSON
scraper.save_to_json(result, 'output.json')

# Clean up
scraper.close()
```

### 🌐 Browser Automation
Selenium-based browser automation scripts for testing and web interaction.

- `selenium_browser.py` - Basic browser automation
- `selenium_browser_enhanced.py` - Enhanced version with webdriver-manager
- `test_selenium.py` - Headless browser testing

### 🔍 Connectivity Checkers
Tools to check website connectivity and availability.

- `check_google.py` - Comprehensive Google.com connectivity checker
- `check_bing.py` - Bing.com connectivity checker
- Simple versions available for quick checks

### 🌐 Flask Web Server
Simple Flask application serving a Hello World page.

```bash
python app.py
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Requirements

- Python 3.7+
- selenium >= 4.0.0
- webdriver-manager >= 3.8.0
- flask >= 2.0.0
- requests >= 2.25.0
- beautifulsoup4 >= 4.9.0

## Testing

Run the web scraper tests:
```bash
python test_web_scraper.py
```

Run Selenium tests:
```bash
python test_selenium.py
```

## Project Structure

```
python-test/
├── web_scraper.py              # Web scraping utility
├── test_web_scraper.py         # Web scraper tests
├── selenium_browser.py         # Browser automation
├── selenium_browser_enhanced.py # Enhanced browser automation
├── test_selenium.py            # Selenium tests
├── check_google.py             # Google connectivity checker
├── check_bing.py               # Bing connectivity checker
├── app.py                      # Flask web server
├── index.html                  # Hello World page
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License
