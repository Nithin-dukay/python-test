# 🌤️ Weather Application - Usage Examples

## 📋 Table of Contents
1. [Web Interface Examples](#web-interface-examples)
2. [CLI Examples](#cli-examples)
3. [API Examples](#api-examples)
4. [Error Handling Examples](#error-handling-examples)

---

## 🌐 Web Interface Examples

### Starting the Web Server

```bash
# Start the Flask application
python weather_app.py

# You should see:
# ============================================================
# 🌤️  Weather Application Starting...
# ============================================================
# Server running at: http://127.0.0.1:5000
# API endpoint: http://127.0.0.1:5000/api/weather/<city>
# Press CTRL+C to quit
# ============================================================
```

### Using the Web Interface

1. **Open your browser**: Navigate to `http://127.0.0.1:5000`

2. **Search for a city**: 
   - Type "London" in the search box
   - Click "Search" or press Enter
   - View detailed weather information

3. **Quick search**: Click any example city button (London, New York, Tokyo, Paris, Sydney)

4. **Search another city**: Use the search form at the bottom of the results page

### What You'll See

**Home Page:**
- Clean, modern interface with gradient background
- Search input with placeholder text
- Quick search buttons for popular cities
- Responsive design that works on all devices

**Weather Results:**
- Large weather emoji (☀️, ☁️, 🌧️, etc.)
- Current temperature in °C and °F
- "Feels like" temperature
- Weather condition description
- Detailed information cards:
  - 💧 Humidity
  - 💨 Wind Speed
  - 🧭 Wind Direction
  - 🔆 UV Index
  - 👁️ Visibility
  - 🌡️ Pressure

---

## 💻 CLI Examples

### Basic Usage

```bash
# Search for weather in London
python weather_cli.py London

# Output:
# 🔍 Fetching weather data for 'London'...
# ============================================================
#   ☀️  Weather for London
#   England, United Kingdom
#   Local Time: 2024-01-15 14:30
# ============================================================
# 
# 🌡️  TEMPERATURE
#   Current: 15°C (59°F)
#   Feels Like: 13°C (55°F)
# 
# ☁️  CONDITION
#   Partly cloudy
# 
# 📊 DETAILS
#   💧 Humidity: 72%
#   💨 Wind Speed: 20 km/h (12 mph)
#   🧭 Wind Direction: SW
#   👁️  Visibility: 10 km (6 mi)
#   🌡️  Pressure: 1013 mb
#   🔆 UV Index: 3
# ============================================================
```

### Multi-Word Cities

```bash
# Use quotes for cities with spaces
python weather_cli.py "New York"
python weather_cli.py "Los Angeles"
python weather_cli.py "San Francisco"
python weather_cli.py "Buenos Aires"
```

### Alternative Syntax

```bash
# Using the --city flag
python weather_cli.py --city London
python weather_cli.py --city "New York"
python weather_cli.py -c Tokyo
```

### Help and Version

```bash
# Display help information
python weather_cli.py --help

# Display version
python weather_cli.py --version
# Output: Weather CLI v1.0.0
```

### Popular Cities Examples

```bash
# Major world cities
python weather_cli.py London        # United Kingdom
python weather_cli.py Paris         # France
python weather_cli.py Tokyo         # Japan
python weather_cli.py Sydney        # Australia
python weather_cli.py Dubai         # UAE
python weather_cli.py Mumbai        # India
python weather_cli.py "New York"    # USA
python weather_cli.py "Los Angeles" # USA
python weather_cli.py Toronto       # Canada
python weather_cli.py Berlin        # Germany
python weather_cli.py Rome          # Italy
python weather_cli.py Madrid        # Spain
python weather_cli.py Moscow        # Russia
python weather_cli.py Beijing       # China
python weather_cli.py Singapore     # Singapore
```

---

## 🔌 API Examples

### Basic API Request

```bash
# Get weather data as JSON
curl http://127.0.0.1:5000/api/weather/London

# Response:
{
  "success": true,
  "data": {
    "city": "London",
    "region": "City of London, Greater London",
    "country": "United Kingdom",
    "local_time": "2024-01-15 14:30",
    "temperature_c": 15,
    "temperature_f": 59,
    "feels_like_c": 13,
    "feels_like_f": 55,
    "humidity": 72,
    "wind_kph": 20,
    "wind_mph": 12,
    "wind_direction": "SW",
    "pressure_mb": 1013,
    "visibility_km": 10,
    "visibility_miles": 6,
    "uv_index": 3,
    "condition": "Partly cloudy",
    "condition_icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
    "is_day": true,
    "emoji": "⛅"
  }
}
```

### Pretty Print with jq

```bash
# Install jq if not available: sudo apt-get install jq
curl -s http://127.0.0.1:5000/api/weather/London | jq

# Extract specific fields
curl -s http://127.0.0.1:5000/api/weather/London | jq '.data.temperature_c'
curl -s http://127.0.0.1:5000/api/weather/London | jq '.data.condition'
```

### Using with Python

```python
import requests

# Fetch weather data
response = requests.get('http://127.0.0.1:5000/api/weather/London')
data = response.json()

if data['success']:
    weather = data['data']
    print(f"Temperature in {weather['city']}: {weather['temperature_c']}°C")
    print(f"Condition: {weather['condition']}")
else:
    print(f"Error: {data['error']}")
```

### Using with JavaScript

```javascript
// Fetch weather data
fetch('http://127.0.0.1:5000/api/weather/London')
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      const weather = data.data;
      console.log(`Temperature in ${weather.city}: ${weather.temperature_c}°C`);
      console.log(`Condition: ${weather.condition}`);
    } else {
      console.error(`Error: ${data.error}`);
    }
  });
```

### Multiple Cities

```bash
# Fetch weather for multiple cities
for city in London Paris Tokyo "New York"; do
  echo "Weather in $city:"
  curl -s "http://127.0.0.1:5000/api/weather/$city" | jq '.data.temperature_c'
  echo ""
done
```

---

## ⚠️ Error Handling Examples

### Empty City Name

**Web Interface:**
- Leave search box empty and click Search
- See error: "Please enter a city name"

**CLI:**
```bash
python weather_cli.py ""
# Output: ❌ Error: Please provide a city name
```

### Invalid City Name

**Web Interface:**
- Search for "InvalidCityName123"
- See error: "City not found: No matching location found"

**CLI:**
```bash
python weather_cli.py "InvalidCityName123"
# Output: ❌ Weather Service Error: City not found: No matching location found
```

**API:**
```bash
curl http://127.0.0.1:5000/api/weather/InvalidCity123
# Response:
{
  "success": false,
  "error": "City not found: No matching location found"
}
```

### Missing API Key

```bash
# Remove or rename .env file
mv .env .env.backup

# Try to run the app
python weather_app.py
# Output: ❌ Configuration Error: WEATHER_API_KEY not found...

# Restore .env file
mv .env.backup .env
```

### Invalid API Key

```bash
# Edit .env and set an invalid key
WEATHER_API_KEY=invalid_key_12345

# Try to fetch weather
python weather_cli.py London
# Output: ❌ Weather Service Error: Invalid API key. Please check your configuration
```

### Network Error Simulation

The application handles network errors gracefully:
- Connection timeouts (10 second timeout)
- Network unavailable
- DNS resolution failures

---

## 🎯 Real-World Scenarios

### Scenario 1: Check Weather Before Travel

```bash
# Check weather in destination city
python weather_cli.py "Paris"

# Compare with current location
python weather_cli.py "London"
```

### Scenario 2: Monitor Multiple Locations

```bash
# Create a simple monitoring script
for city in "New York" "London" "Tokyo" "Sydney"; do
  echo "=== $city ==="
  python weather_cli.py "$city" | grep "Current:"
  echo ""
done
```

### Scenario 3: Integration with Other Tools

```bash
# Save weather data to file
curl -s http://127.0.0.1:5000/api/weather/London > weather_london.json

# Process with jq
cat weather_london.json | jq '.data | {city, temp: .temperature_c, condition}'
```

### Scenario 4: Automated Weather Alerts

```python
# weather_alert.py
import requests

def check_weather_alert(city, temp_threshold):
    response = requests.get(f'http://127.0.0.1:5000/api/weather/{city}')
    data = response.json()
    
    if data['success']:
        temp = data['data']['temperature_c']
        if temp > temp_threshold:
            print(f"⚠️ Alert: Temperature in {city} is {temp}°C (threshold: {temp_threshold}°C)")
        else:
            print(f"✅ Temperature in {city} is normal: {temp}°C")

# Check if temperature exceeds 30°C
check_weather_alert('Dubai', 30)
```

---

## 📊 Testing Examples

### Run Comprehensive Tests

```bash
# Run all tests
python test_weather_app.py

# Expected output:
# ============================================================
# WEATHER APPLICATION - COMPREHENSIVE TEST SUITE
# ============================================================
# ...
# 🎉 ALL TESTS PASSED!
```

### Manual Testing Checklist

**Web Interface:**
- [ ] Home page loads correctly
- [ ] Search with valid city works
- [ ] Search with invalid city shows error
- [ ] Empty search shows error
- [ ] Quick search buttons work
- [ ] Responsive design on mobile
- [ ] Back button works
- [ ] Search again form works

**CLI:**
- [ ] Help command works
- [ ] Version command works
- [ ] Valid city search works
- [ ] Invalid city shows error
- [ ] Empty input shows error
- [ ] Multi-word cities work
- [ ] Colors display correctly

**API:**
- [ ] Valid city returns JSON
- [ ] Invalid city returns error
- [ ] Response format is correct
- [ ] HTTP status codes are appropriate

---

## 🎓 Learning Examples

### Example 1: Understanding the Response

```bash
# Get full weather data
curl -s http://127.0.0.1:5000/api/weather/London | jq

# Extract just temperature
curl -s http://127.0.0.1:5000/api/weather/London | jq '.data.temperature_c'

# Extract multiple fields
curl -s http://127.0.0.1:5000/api/weather/London | jq '{temp: .data.temperature_c, humidity: .data.humidity, wind: .data.wind_kph}'
```

### Example 2: Building on the API

```python
# Create a simple weather comparison tool
import requests

cities = ['London', 'Paris', 'Tokyo', 'New York']
base_url = 'http://127.0.0.1:5000/api/weather/'

print("City Temperature Comparison:")
print("-" * 40)

for city in cities:
    response = requests.get(f"{base_url}{city}")
    data = response.json()
    
    if data['success']:
        weather = data['data']
        print(f"{weather['city']:15} {weather['temperature_c']:5}°C  {weather['condition']}")
```

---

## 💡 Tips and Tricks

1. **Bookmark the web interface** for quick access
2. **Create shell aliases** for frequently checked cities:
   ```bash
   alias weather-london='python weather_cli.py London'
   alias weather-ny='python weather_cli.py "New York"'
   ```
3. **Use the API** to integrate with other applications
4. **Check multiple cities** by creating simple bash scripts
5. **Monitor weather changes** by scheduling periodic checks

---

**Need Help?** Check the [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md) for more information!
