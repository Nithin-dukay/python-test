#!/usr/bin/env python3
"""
Test script for the Weather Report App
Tests the API endpoints and validates responses
"""

import requests
import sys

BASE_URL = "http://localhost:5000"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'
    print("✓ Health endpoint working")

def test_valid_city():
    """Test with valid city names"""
    print("\nTesting valid cities...")
    cities = ["London", "Paris", "Tokyo", "New York", "Sydney"]
    
    for city in cities:
        response = requests.get(f"{BASE_URL}/api/weather/{city}")
        assert response.status_code == 200
        data = response.json()
        assert 'city' in data
        assert 'temperature_c' in data
        assert 'temperature_f' in data
        assert 'condition' in data
        assert 'humidity' in data
        print(f"✓ {city}: {data['temperature_c']}°C, {data['condition']}")

def test_invalid_city():
    """Test with invalid city name"""
    print("\nTesting invalid city...")
    response = requests.get(f"{BASE_URL}/api/weather/InvalidCity12345")
    assert response.status_code == 404
    data = response.json()
    assert 'error' in data
    assert data['error'] == 'City not found'
    print("✓ Invalid city error handling working")

def test_special_characters():
    """Test with special characters in city name"""
    print("\nTesting special characters...")
    response = requests.get(f"{BASE_URL}/api/weather/São Paulo")
    # Should either work or return proper error
    assert response.status_code in [200, 404]
    print("✓ Special characters handled")

def main():
    """Run all tests"""
    print("=" * 50)
    print("Weather Report App - API Tests")
    print("=" * 50)
    
    try:
        test_health_endpoint()
        test_valid_city()
        test_invalid_city()
        test_special_characters()
        
        print("\n" + "=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
        return 0
    
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except requests.exceptions.ConnectionError:
        print("\n✗ Could not connect to server. Is it running?")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
