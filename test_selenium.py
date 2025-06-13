#!/usr/bin/env python3
"""
Selenium Web Browser Test Script (Headless Mode)
This script tests the Selenium functionality in headless mode.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

def setup_chrome_driver_headless():
    """
    Set up Chrome WebDriver in headless mode for testing
    """
    chrome_options = Options()
    
    # Add options for better compatibility
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")  # Run in headless mode
    
    try:
        # Try to create the driver
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        return None

def test_browser_functionality():
    """
    Test basic browser functionality
    """
    driver = None
    
    try:
        print("Testing Selenium functionality in headless mode...")
        driver = setup_chrome_driver_headless()
        
        if driver is None:
            print("Failed to setup Chrome driver")
            return False
        
        print("✅ Chrome driver setup successful!")
        
        # Navigate to a test URL
        test_url = "https://httpbin.org/html"
        print(f"Navigating to: {test_url}")
        driver.get(test_url)
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print(f"✅ Page loaded successfully!")
        print(f"Page title: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        
        # Test finding an element
        try:
            h1_element = driver.find_element(By.TAG_NAME, "h1")
            print(f"✅ Found H1 element: {h1_element.text}")
        except Exception as e:
            print(f"Could not find H1 element: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
        
    finally:
        # Clean up - close the browser
        if driver:
            print("Closing browser...")
            driver.quit()

if __name__ == "__main__":
    print("=== Selenium Functionality Test ===")
    success = test_browser_functionality()
    
    if success:
        print("\n🎉 All tests passed! Selenium is working correctly.")
    else:
        print("\n❌ Tests failed. Please check your Selenium installation.")
