#!/usr/bin/env python3
"""
Comprehensive test script for Weather Application
Tests all components without requiring a real API key
"""
import sys
from weather_service import WeatherService, WeatherServiceError
from weather_app import app


def print_test(test_name, passed):
    """Print test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {test_name}")
    return passed


def test_weather_service():
    """Test weather service functionality"""
    print("\n" + "="*60)
    print("TESTING WEATHER SERVICE")
    print("="*60)
    
    all_passed = True
    
    # Test 1: Service initialization
    try:
        service = WeatherService(api_key='test_key')
        all_passed &= print_test("Service initialization", True)
    except Exception as e:
        all_passed &= print_test(f"Service initialization: {e}", False)
        return False
    
    # Test 2: Empty city validation
    try:
        service.get_weather('')
        all_passed &= print_test("Empty city validation", False)
    except WeatherServiceError as e:
        all_passed &= print_test("Empty city validation", "cannot be empty" in str(e))
    
    # Test 3: Whitespace city validation
    try:
        service.get_weather('   ')
        all_passed &= print_test("Whitespace city validation", False)
    except WeatherServiceError as e:
        all_passed &= print_test("Whitespace city validation", "cannot be empty" in str(e))
    
    # Test 4: Emoji generation - sunny day
    emoji = service.get_weather_emoji('Sunny', True)
    all_passed &= print_test("Emoji generation (sunny day)", emoji == '☀️')
    
    # Test 5: Emoji generation - clear night
    emoji = service.get_weather_emoji('Clear', False)
    all_passed &= print_test("Emoji generation (clear night)", emoji == '🌙')
    
    # Test 6: Emoji generation - rainy
    emoji = service.get_weather_emoji('Heavy rain', True)
    all_passed &= print_test("Emoji generation (heavy rain)", emoji == '🌧️')
    
    # Test 7: Emoji generation - cloudy
    emoji = service.get_weather_emoji('Partly cloudy', True)
    all_passed &= print_test("Emoji generation (partly cloudy)", emoji == '⛅')
    
    # Test 8: Emoji generation - snow
    emoji = service.get_weather_emoji('Snow', True)
    all_passed &= print_test("Emoji generation (snow)", emoji == '❄️')
    
    # Test 9: Emoji generation - thunderstorm
    emoji = service.get_weather_emoji('Thunderstorm', True)
    all_passed &= print_test("Emoji generation (thunderstorm)", emoji == '⛈️')
    
    return all_passed


def test_flask_app():
    """Test Flask application routes"""
    print("\n" + "="*60)
    print("TESTING FLASK APPLICATION")
    print("="*60)
    
    all_passed = True
    
    with app.test_client() as client:
        # Test 1: Home page
        response = client.get('/')
        all_passed &= print_test("Home page (GET /)", response.status_code == 200)
        all_passed &= print_test("Home page contains title", b'Weather App' in response.data)
        
        # Test 2: Weather page with empty city
        response = client.post('/weather', data={'city': ''})
        all_passed &= print_test("Empty city POST", response.status_code == 200)
        all_passed &= print_test("Empty city error message", b'Please enter a city name' in response.data)
        
        # Test 3: Weather page with GET and empty city
        response = client.get('/weather?city=')
        all_passed &= print_test("Empty city GET", response.status_code == 200)
        
        # Test 4: 404 error handling
        response = client.get('/nonexistent-page')
        all_passed &= print_test("404 error handling", response.status_code == 404)
        
        # Test 5: API endpoint with invalid city (will fail with demo key)
        response = client.get('/api/weather/InvalidCity123')
        all_passed &= print_test("API endpoint responds", response.status_code in [200, 400, 401])
        all_passed &= print_test("API returns JSON", response.content_type == 'application/json')
    
    return all_passed


def test_configuration():
    """Test configuration module"""
    print("\n" + "="*60)
    print("TESTING CONFIGURATION")
    print("="*60)
    
    all_passed = True
    
    from config import Config
    
    # Test 1: Config has required attributes
    all_passed &= print_test("Config has WEATHER_API_KEY", hasattr(Config, 'WEATHER_API_KEY'))
    all_passed &= print_test("Config has WEATHER_API_BASE_URL", hasattr(Config, 'WEATHER_API_BASE_URL'))
    all_passed &= print_test("Config has REQUEST_TIMEOUT", hasattr(Config, 'REQUEST_TIMEOUT'))
    all_passed &= print_test("Config has validate method", hasattr(Config, 'validate'))
    
    # Test 2: Config values are correct types
    all_passed &= print_test("API key is string", isinstance(Config.WEATHER_API_KEY, str))
    all_passed &= print_test("Base URL is string", isinstance(Config.WEATHER_API_BASE_URL, str))
    all_passed &= print_test("Timeout is integer", isinstance(Config.REQUEST_TIMEOUT, int))
    
    return all_passed


def test_templates():
    """Test that template files exist and are valid"""
    print("\n" + "="*60)
    print("TESTING TEMPLATES")
    print("="*60)
    
    all_passed = True
    
    import os
    
    # Test 1: Templates directory exists
    templates_dir = '/vercel/sandbox/templates'
    all_passed &= print_test("Templates directory exists", os.path.isdir(templates_dir))
    
    # Test 2: index.html exists
    index_path = os.path.join(templates_dir, 'index.html')
    all_passed &= print_test("index.html exists", os.path.isfile(index_path))
    
    # Test 3: weather.html exists
    weather_path = os.path.join(templates_dir, 'weather.html')
    all_passed &= print_test("weather.html exists", os.path.isfile(weather_path))
    
    # Test 4: Static CSS exists
    css_path = '/vercel/sandbox/static/css/style.css'
    all_passed &= print_test("style.css exists", os.path.isfile(css_path))
    
    # Test 5: Static JS exists
    js_path = '/vercel/sandbox/static/js/script.js'
    all_passed &= print_test("script.js exists", os.path.isfile(js_path))
    
    return all_passed


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("WEATHER APPLICATION - COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    results = {
        'Configuration': test_configuration(),
        'Weather Service': test_weather_service(),
        'Flask Application': test_flask_app(),
        'Templates & Static Files': test_templates()
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        print("\nThe weather application is ready to use!")
        print("\nNext steps:")
        print("1. Get a free API key from: https://www.weatherapi.com/signup.aspx")
        print("2. Update .env file with your API key")
        print("3. Run: python weather_app.py")
        print("4. Open: http://127.0.0.1:5000")
        print("\nOr use the CLI:")
        print("   python weather_cli.py London")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("="*60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
