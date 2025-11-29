#!/usr/bin/env python3
"""
Unit Tests for Web Scraper Utility
This module contains comprehensive tests for the web_scraper module.
"""

import unittest
import json
import os
import time
from unittest.mock import Mock, patch, MagicMock
from web_scraper import WebScraper


class TestWebScraper(unittest.TestCase):
    """Test cases for WebScraper class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scraper = WebScraper(timeout=5, rate_limit=0.1)
        
        # Sample HTML for testing
        self.sample_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Page</title>
            <meta name="description" content="A test page">
            <meta property="og:title" content="Test OG Title">
        </head>
        <body>
            <h1>Welcome to Test Page</h1>
            <p>This is a test paragraph with some text.</p>
            <a href="/relative-link">Relative Link</a>
            <a href="https://example.com/absolute">Absolute Link</a>
            <img src="/image1.jpg" alt="Image 1">
            <img src="https://example.com/image2.png" alt="Image 2">
            <script>console.log('test');</script>
            <style>.test { color: red; }</style>
        </body>
        </html>
        """
    
    def tearDown(self):
        """Clean up after tests"""
        self.scraper.close()
        
        # Remove test output files
        test_files = ['test_output.json', 'scraped_data.json']
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
    
    def test_initialization(self):
        """Test WebScraper initialization"""
        self.assertEqual(self.scraper.timeout, 5)
        self.assertEqual(self.scraper.rate_limit, 0.1)
        self.assertIsNotNone(self.scraper.session)
    
    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        start_time = time.time()
        
        # Make two consecutive calls
        self.scraper._apply_rate_limit()
        self.scraper._apply_rate_limit()
        
        elapsed_time = time.time() - start_time
        
        # Should take at least rate_limit seconds
        self.assertGreaterEqual(elapsed_time, self.scraper.rate_limit)
    
    def test_extract_text(self):
        """Test text extraction from HTML"""
        text = self.scraper.extract_text(self.sample_html)
        
        self.assertIn("Welcome to Test Page", text)
        self.assertIn("This is a test paragraph", text)
        # Script and style content should be removed
        self.assertNotIn("console.log", text)
        self.assertNotIn("color: red", text)
    
    def test_extract_links(self):
        """Test link extraction from HTML"""
        base_url = "https://example.com"
        links = self.scraper.extract_links(self.sample_html, base_url)
        
        self.assertEqual(len(links), 2)
        
        # Check relative link conversion
        relative_link = next(l for l in links if l['href'] == '/relative-link')
        self.assertEqual(relative_link['absolute_url'], 'https://example.com/relative-link')
        
        # Check absolute link
        absolute_link = next(l for l in links if 'absolute' in l['href'])
        self.assertEqual(absolute_link['absolute_url'], 'https://example.com/absolute')
    
    def test_extract_images(self):
        """Test image extraction from HTML"""
        base_url = "https://example.com"
        images = self.scraper.extract_images(self.sample_html, base_url)
        
        self.assertEqual(len(images), 2)
        
        # Check image attributes
        img1 = images[0]
        self.assertEqual(img1['src'], '/image1.jpg')
        self.assertEqual(img1['alt'], 'Image 1')
        self.assertEqual(img1['absolute_url'], 'https://example.com/image1.jpg')
        
        img2 = images[1]
        self.assertEqual(img2['src'], 'https://example.com/image2.png')
        self.assertEqual(img2['alt'], 'Image 2')
    
    def test_extract_metadata(self):
        """Test metadata extraction from HTML"""
        metadata = self.scraper.extract_metadata(self.sample_html)
        
        self.assertEqual(metadata['title'], 'Test Page')
        self.assertEqual(metadata['description'], 'A test page')
        self.assertEqual(metadata['og:title'], 'Test OG Title')
    
    @patch('web_scraper.requests.Session.get')
    def test_fetch_page_success(self, mock_get):
        """Test successful page fetching"""
        mock_response = Mock()
        mock_response.text = self.sample_html
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        html = self.scraper.fetch_page('https://example.com')
        
        self.assertEqual(html, self.sample_html)
        mock_get.assert_called_once()
    
    @patch('requests.Session.get')
    def test_fetch_page_failure(self, mock_get):
        """Test page fetching failure"""
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        
        html = self.scraper.fetch_page('https://example.com')
        
        self.assertIsNone(html)
    
    def test_save_to_json(self):
        """Test saving data to JSON file"""
        test_data = {
            'url': 'https://example.com',
            'title': 'Test Page',
            'links': [{'text': 'Link', 'href': '/link'}]
        }
        
        filename = 'test_output.json'
        self.scraper.save_to_json(test_data, filename)
        
        # Verify file was created
        self.assertTrue(os.path.exists(filename))
        
        # Verify content
        with open(filename, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data['url'], test_data['url'])
        self.assertEqual(loaded_data['title'], test_data['title'])
    
    @patch('web_scraper.WebScraper.fetch_page')
    def test_scrape_page_with_requests(self, mock_fetch):
        """Test complete page scraping with requests method"""
        mock_fetch.return_value = self.sample_html
        
        result = self.scraper.scrape_page('https://example.com', use_selenium=False)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['url'], 'https://example.com')
        self.assertEqual(result['method'], 'requests')
        self.assertEqual(result['metadata']['title'], 'Test Page')
        self.assertEqual(result['statistics']['link_count'], 2)
        self.assertEqual(result['statistics']['image_count'], 2)
        self.assertGreater(result['statistics']['text_length'], 0)
    
    @patch('web_scraper.WebScraper.fetch_page')
    def test_scrape_page_failure(self, mock_fetch):
        """Test scraping failure handling"""
        mock_fetch.return_value = None
        
        result = self.scraper.scrape_page('https://example.com')
        
        self.assertIsNone(result)
    
    def test_extract_text_empty_html(self):
        """Test text extraction from empty HTML"""
        text = self.scraper.extract_text("")
        self.assertEqual(text, "")
    
    def test_extract_links_no_links(self):
        """Test link extraction when no links present"""
        html = "<html><body><p>No links here</p></body></html>"
        links = self.scraper.extract_links(html, "https://example.com")
        self.assertEqual(len(links), 0)
    
    def test_extract_images_no_images(self):
        """Test image extraction when no images present"""
        html = "<html><body><p>No images here</p></body></html>"
        images = self.scraper.extract_images(html, "https://example.com")
        self.assertEqual(len(images), 0)


class TestWebScraperIntegration(unittest.TestCase):
    """Integration tests for WebScraper"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scraper = WebScraper(timeout=10, rate_limit=0.5)
    
    def tearDown(self):
        """Clean up after tests"""
        self.scraper.close()
    
    def test_scrape_real_page(self):
        """Test scraping a real page (httpbin.org)"""
        # Using httpbin.org as it's a reliable test endpoint
        url = "https://httpbin.org/html"
        
        result = self.scraper.scrape_page(url, use_selenium=False)
        
        if result:  # Only assert if connection was successful
            self.assertEqual(result['url'], url)
            self.assertEqual(result['method'], 'requests')
            self.assertIn('metadata', result)
            self.assertIn('text', result)
            self.assertIn('links', result)
            self.assertIn('statistics', result)
            self.assertGreater(result['statistics']['text_length'], 0)


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 RUNNING WEB SCRAPER TESTS")
    print("=" * 60)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestWebScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestWebScraperIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit_code = run_tests()
    exit(exit_code)
