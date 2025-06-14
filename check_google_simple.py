#!/usr/bin/env python3
"""
Simple Google.com Status Checker
A lightweight script to quickly check if google.com is accessible.
"""

import requests
import sys

def check_google_simple():
    """Simple check if google.com is accessible"""
    try:
        print("Checking google.com status...")
        response = requests.get("https://www.google.com", timeout=5)
        
        if response.status_code == 200:
            print("✅ Google.com is UP and accessible!")
            return True
        else:
            print(f"⚠️ Google.com returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Google.com is DOWN or unreachable!")
        return False
    except requests.exceptions.Timeout:
        print("❌ Connection to google.com timed out!")
        return False
    except Exception as e:
        print(f"❌ Error checking google.com: {str(e)}")
        return False

if __name__ == "__main__":
    is_up = check_google_simple()
    sys.exit(0 if is_up else 1)
