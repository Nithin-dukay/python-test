#!/usr/bin/env python3
"""
Google.com Connectivity Checker
This script checks if google.com is accessible using multiple methods.
"""

import requests
import socket
import time
import sys
from urllib.parse import urlparse

class GoogleConnectivityChecker:
    def __init__(self):
        self.url = "https://www.google.com"
        self.timeout = 10
        
    def check_http_connectivity(self):
        """Check connectivity using HTTP request"""
        try:
            print("🔍 Checking HTTP connectivity to google.com...")
            response = requests.get(self.url, timeout=self.timeout)
            
            if response.status_code == 200:
                print(f"✅ SUCCESS: Google.com is UP!")
                print(f"   Status Code: {response.status_code}")
                print(f"   Response Time: {response.elapsed.total_seconds():.2f} seconds")
                return True
            else:
                print(f"⚠️  WARNING: Google.com responded with status code: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ ERROR: Connection failed - No internet connection or DNS issues")
            return False
        except requests.exceptions.Timeout:
            print(f"❌ ERROR: Request timed out after {self.timeout} seconds")
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ ERROR: Request failed - {str(e)}")
            return False
    
    def check_socket_connectivity(self):
        """Check connectivity using socket connection"""
        try:
            print("🔍 Checking socket connectivity to google.com...")
            
            # Get IP address of google.com
            host = "www.google.com"
            port = 80
            
            # Create socket and connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            start_time = time.time()
            result = sock.connect_ex((host, port))
            end_time = time.time()
            
            sock.close()
            
            if result == 0:
                print(f"✅ SUCCESS: Socket connection to google.com established!")
                print(f"   Connection Time: {(end_time - start_time):.2f} seconds")
                return True
            else:
                print(f"❌ ERROR: Socket connection failed with error code: {result}")
                return False
                
        except socket.gaierror:
            print("❌ ERROR: DNS resolution failed - Cannot resolve google.com")
            return False
        except socket.timeout:
            print(f"❌ ERROR: Socket connection timed out after {self.timeout} seconds")
            return False
        except Exception as e:
            print(f"❌ ERROR: Socket connection failed - {str(e)}")
            return False
    
    def check_dns_resolution(self):
        """Check if google.com can be resolved via DNS"""
        try:
            print("🔍 Checking DNS resolution for google.com...")
            
            ip_address = socket.gethostbyname("www.google.com")
            print(f"✅ SUCCESS: DNS resolution successful!")
            print(f"   IP Address: {ip_address}")
            return True
            
        except socket.gaierror:
            print("❌ ERROR: DNS resolution failed")
            return False
        except Exception as e:
            print(f"❌ ERROR: DNS check failed - {str(e)}")
            return False
    
    def run_comprehensive_check(self):
        """Run all connectivity checks"""
        print("=" * 60)
        print("🌐 GOOGLE.COM CONNECTIVITY CHECKER")
        print("=" * 60)
        print(f"Target: {self.url}")
        print(f"Timeout: {self.timeout} seconds")
        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        results = []
        
        # DNS Check
        dns_result = self.check_dns_resolution()
        results.append(("DNS Resolution", dns_result))
        print()
        
        # Socket Check
        socket_result = self.check_socket_connectivity()
        results.append(("Socket Connection", socket_result))
        print()
        
        # HTTP Check
        http_result = self.check_http_connectivity()
        results.append(("HTTP Request", http_result))
        print()
        
        # Summary
        print("=" * 60)
        print("📊 SUMMARY REPORT")
        print("=" * 60)
        
        all_passed = True
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name:<20}: {status}")
            if not result:
                all_passed = False
        
        print("-" * 60)
        if all_passed:
            print("🎉 OVERALL STATUS: Google.com is FULLY ACCESSIBLE")
            return 0
        else:
            print("⚠️  OVERALL STATUS: Google.com has CONNECTIVITY ISSUES")
            return 1

def main():
    """Main function to run the connectivity checker"""
    try:
        checker = GoogleConnectivityChecker()
        exit_code = checker.run_comprehensive_check()
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Check interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
