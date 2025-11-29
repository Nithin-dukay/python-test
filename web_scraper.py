#!/usr/bin/env python3
"""
Web Scraper Utility Module
This module provides comprehensive web scraping functionality using both
requests/BeautifulSoup and Selenium for dynamic content.
"""

import requests
import json
import time
import sys
import argparse
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Set
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class WebScraper:
    """
    A comprehensive web scraper that can extract various types of content
    from web pages using both static and dynamic scraping methods.
    """
    
    def __init__(self, timeout: int = 10, rate_limit: float = 1.0):
        """
        Initialize the WebScraper
        
        Args:
            timeout (int): Request timeout in seconds
            rate_limit (float): Minimum seconds between requests
        """
        self.timeout = timeout
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _apply_rate_limit(self):
        """Apply rate limiting between requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.rate_limit:
            time.sleep(self.rate_limit - time_since_last_request)
        
        self.last_request_time = time.time()
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from a URL using requests
        
        Args:
            url (str): The URL to fetch
            
        Returns:
            Optional[str]: HTML content or None if failed
        """
        try:
            self._apply_rate_limit()
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def fetch_page_dynamic(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from a URL using Selenium (for dynamic content)
        
        Args:
            url (str): The URL to fetch
            
        Returns:
            Optional[str]: HTML content or None if failed
        """
        driver = None
        try:
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            self._apply_rate_limit()
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, self.timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            return driver.page_source
            
        except Exception as e:
            print(f"Error fetching dynamic content from {url}: {e}")
            return None
        finally:
            if driver:
                driver.quit()
    
    def extract_text(self, html: str) -> str:
        """
        Extract all text content from HTML
        
        Args:
            html (str): HTML content
            
        Returns:
            str: Extracted text
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def extract_links(self, html: str, base_url: str) -> List[Dict[str, str]]:
        """
        Extract all links from HTML
        
        Args:
            html (str): HTML content
            base_url (str): Base URL for resolving relative links
            
        Returns:
            List[Dict[str, str]]: List of links with text and href
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True)
            absolute_url = urljoin(base_url, href)
            
            links.append({
                'text': text,
                'href': href,
                'absolute_url': absolute_url
            })
        
        return links
    
    def extract_images(self, html: str, base_url: str) -> List[Dict[str, str]]:
        """
        Extract all images from HTML
        
        Args:
            html (str): HTML content
            base_url (str): Base URL for resolving relative URLs
            
        Returns:
            List[Dict[str, str]]: List of images with src and alt text
        """
        soup = BeautifulSoup(html, 'html.parser')
        images = []
        
        for img in soup.find_all('img'):
            src = img.get('src', '')
            alt = img.get('alt', '')
            absolute_url = urljoin(base_url, src) if src else ''
            
            images.append({
                'src': src,
                'absolute_url': absolute_url,
                'alt': alt
            })
        
        return images
    
    def extract_metadata(self, html: str) -> Dict[str, str]:
        """
        Extract metadata from HTML (title, meta tags, etc.)
        
        Args:
            html (str): HTML content
            
        Returns:
            Dict[str, str]: Dictionary of metadata
        """
        soup = BeautifulSoup(html, 'html.parser')
        metadata = {}
        
        # Extract title
        title = soup.find('title')
        metadata['title'] = title.get_text(strip=True) if title else ''
        
        # Extract meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property', '')
            content = meta.get('content', '')
            
            if name and content:
                metadata[name] = content
        
        return metadata
    
    def scrape_page(self, url: str, use_selenium: bool = False) -> Optional[Dict]:
        """
        Scrape a complete page and extract all information
        
        Args:
            url (str): The URL to scrape
            use_selenium (bool): Whether to use Selenium for dynamic content
            
        Returns:
            Optional[Dict]: Dictionary containing all scraped data
        """
        print(f"Scraping: {url}")
        print(f"Method: {'Selenium (dynamic)' if use_selenium else 'Requests (static)'}")
        
        # Fetch HTML
        if use_selenium:
            html = self.fetch_page_dynamic(url)
        else:
            html = self.fetch_page(url)
        
        if not html:
            return None
        
        # Extract all information
        result = {
            'url': url,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'method': 'selenium' if use_selenium else 'requests',
            'metadata': self.extract_metadata(html),
            'text': self.extract_text(html),
            'links': self.extract_links(html, url),
            'images': self.extract_images(html, url),
            'statistics': {
                'text_length': len(self.extract_text(html)),
                'link_count': len(self.extract_links(html, url)),
                'image_count': len(self.extract_images(html, url))
            }
        }
        
        return result
    
    def save_to_json(self, data: Dict, filename: str):
        """
        Save scraped data to JSON file
        
        Args:
            data (Dict): Data to save
            filename (str): Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Data saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving to JSON: {e}")
    
    def close(self):
        """Close the session"""
        self.session.close()


def main():
    """Main function to run the web scraper from command line"""
    parser = argparse.ArgumentParser(
        description='Web Scraper Utility - Extract content from web pages',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://example.com
  %(prog)s https://example.com --selenium
  %(prog)s https://example.com --output result.json
  %(prog)s https://example.com --selenium --timeout 20
        """
    )
    
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('--selenium', action='store_true',
                        help='Use Selenium for dynamic content (default: requests)')
    parser.add_argument('--output', '-o', default='scraped_data.json',
                        help='Output JSON file (default: scraped_data.json)')
    parser.add_argument('--timeout', type=int, default=10,
                        help='Request timeout in seconds (default: 10)')
    parser.add_argument('--rate-limit', type=float, default=1.0,
                        help='Minimum seconds between requests (default: 1.0)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🕷️  WEB SCRAPER UTILITY")
    print("=" * 60)
    
    # Create scraper instance
    scraper = WebScraper(timeout=args.timeout, rate_limit=args.rate_limit)
    
    try:
        # Scrape the page
        result = scraper.scrape_page(args.url, use_selenium=args.selenium)
        
        if result:
            print("\n" + "=" * 60)
            print("📊 SCRAPING RESULTS")
            print("=" * 60)
            print(f"Title: {result['metadata'].get('title', 'N/A')}")
            print(f"Text Length: {result['statistics']['text_length']} characters")
            print(f"Links Found: {result['statistics']['link_count']}")
            print(f"Images Found: {result['statistics']['image_count']}")
            print()
            
            # Save to JSON
            scraper.save_to_json(result, args.output)
            
            print("\n🎉 Scraping completed successfully!")
            return 0
        else:
            print("\n❌ Scraping failed!")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Scraping interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        return 1
    finally:
        scraper.close()


if __name__ == "__main__":
    sys.exit(main())
