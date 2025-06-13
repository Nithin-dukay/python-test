#!/usr/bin/env python3
"""
Enhanced Selenium Web Browser Automation Script
This script uses webdriver-manager for automatic driver management and demonstrates 
how to use Selenium to open a web browser and navigate to a webpage.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time
import sys

def setup_chrome_driver():
    """
    Set up Chrome WebDriver with automatic driver management
    """
    try:
        chrome_options = ChromeOptions()
        
        # Add options for better compatibility
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Uncomment the line below to run in headless mode (without GUI)
        # chrome_options.add_argument("--headless")
        
        # Use webdriver-manager to automatically download and manage ChromeDriver
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        return None

def setup_firefox_driver():
    """
    Set up Firefox WebDriver with automatic driver management
    """
    try:
        firefox_options = FirefoxOptions()
        
        # Uncomment the line below to run in headless mode
        # firefox_options.add_argument("--headless")
        
        # Use webdriver-manager to automatically download and manage GeckoDriver
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        return driver
    except Exception as e:
        print(f"Error setting up Firefox driver: {e}")
        return None

def open_browser_and_navigate(url="https://www.google.com"):
    """
    Open a web browser and navigate to the specified URL
    
    Args:
        url (str): The URL to navigate to (default: Google)
    """
    driver = None
    
    try:
        print("Attempting to open Chrome browser...")
        driver = setup_chrome_driver()
        
        if driver is None:
            print("Chrome failed, trying Firefox...")
            driver = setup_firefox_driver()
        
        if driver is None:
            print("Both Chrome and Firefox failed. Please ensure you have a supported browser installed.")
            return False
        
        print(f"Browser opened successfully! Navigating to: {url}")
        
        # Navigate to the specified URL
        driver.get(url)
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print(f"Successfully loaded: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        
        # Demonstrate some basic interactions
        print("\nPerforming basic page interactions...")
        
        # Get page source length
        page_source_length = len(driver.page_source)
        print(f"Page source length: {page_source_length} characters")
        
        # Get window size
        window_size = driver.get_window_size()
        print(f"Window size: {window_size['width']}x{window_size['height']}")
        
        # Keep the browser open for 10 seconds to demonstrate
        print("\nBrowser will remain open for 10 seconds...")
        time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
        
    finally:
        # Clean up - close the browser
        if driver:
            print("Closing browser...")
            driver.quit()

def main():
    """
    Main function to run the browser automation
    """
    print("=== Enhanced Selenium Web Browser Automation ===")
    print("This script will open a web browser and navigate to a webpage.")
    print("Using webdriver-manager for automatic driver management.")
    print()
    
    # Default URL
    default_url = "https://www.google.com"
    
    # Check if a custom URL was provided as command line argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"Using custom URL: {url}")
    else:
        url = default_url
        print(f"Using default URL: {url}")
    
    print()
    
    # Run the browser automation
    success = open_browser_and_navigate(url)
    
    if success:
        print("✅ Browser automation completed successfully!")
    else:
        print("❌ Browser automation failed!")
        print("Make sure you have:")
        print("1. Selenium installed: pip install selenium")
        print("2. webdriver-manager installed: pip install webdriver-manager")
        print("3. Chrome or Firefox browser installed")

if __name__ == "__main__":
    main()
