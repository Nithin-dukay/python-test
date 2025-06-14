#!/usr/bin/env python3
"""
Simple Bing.com Status Checker
A lightweight script to quickly check if bing.com is accessible.
"""

import requests
import sys

def check_bing_simple():
    """Simple check if bing.com is accessible"""
    try:
        print("Checking bing.com status...")
        response = requests.get("https://www.bing.com", timeout=5)
        
        if response.status_code == 200:
            print("✅ Bing.com is UP and accessible!")
            return True
        else:
            print(f"⚠️ Bing.com returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Bing.com is DOWN or unreachable!")
        return False
    except requests.exceptions.Timeout:
        print("❌ Connection to bing.com timed out!")
        return False
    except Exception as e:
        print(f"❌ Error checking bing.com: {str(e)}")
        return False

if __name__ == "__main__":
    is_up = check_bing_simple()
    sys.exit(0 if is_up else 1)
