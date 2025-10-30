# Weather Report App

A modern, responsive weather application built with Python Flask and vanilla JavaScript. Get real-time weather information for any city worldwide.

## Features

- 🌍 **Global Weather Data**: Search for weather in any city worldwide
- 🌡️ **Temperature Units**: Toggle between Celsius and Fahrenheit
- 📊 **Comprehensive Data**: View temperature, humidity, wind speed, pressure, and visibility
- 🎨 **Modern UI**: Clean, responsive design with gradient backgrounds
- ⚡ **Real-time Updates**: Instant weather data from wttr.in API
- 🔍 **Error Handling**: Graceful error messages for invalid cities
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## Technology Stack

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Weather API**: wttr.in (no API key required)
- **Fonts**: Google Fonts (Inter)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python3 app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

### Get Weather Data
```
GET /api/weather/<city>
```

**Example Request:**
```bash
curl http://localhost:5000/api/weather/London
```

**Example Response:**
```json
{
  "city": "London",
  "country": "United Kingdom",
  "region": "City of London Greater London",
  "temperature_c": "12",
  "temperature_f": "54",
  "feels_like_c": "10",
  "feels_like_f": "50",
  "condition": "Partly cloudy",
  "humidity": "77",
  "wind_speed_kmph": "26",
  "wind_speed_mph": "16",
  "wind_direction": "S",
  "pressure": "1004",
  "visibility": "10",
  "uv_index": "0"
}
```

### Health Check
```
GET /health
```

**Example Response:**
```json
{
  "status": "healthy",
  "message": "Weather app is running!"
}
```

## Testing

Run the automated test suite:
```bash
python3 test_weather_app.py
```

The test suite validates:
- Health endpoint functionality
- Valid city weather data retrieval
- Error handling for invalid cities
- Special character handling

## Usage

1. **Search for a City**: Enter any city name in the search box
2. **View Weather**: Weather data loads automatically
3. **Toggle Units**: Click °C or °F buttons to switch temperature units
4. **Try Different Cities**: Search for multiple cities to compare weather

## Features in Detail

### Weather Information Displayed
- Current temperature (with feels-like temperature)
- Weather condition (e.g., Partly cloudy, Rainy)
- Humidity percentage
- Wind speed and direction
- Atmospheric pressure
- Visibility distance
- UV index

### User Interface
- Gradient purple background for visual appeal
- Card-based layout with rounded corners
- Smooth animations and transitions
- Loading indicators during data fetch
- Error messages for invalid inputs
- Responsive grid layout for weather details

## Error Handling

The app handles various error scenarios:
- **Invalid City**: Shows "City not found" message
- **Network Errors**: Displays connection error message
- **API Timeouts**: Graceful timeout handling
- **Empty Input**: Prompts user to enter a city name

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development

### Project Structure
```
/vercel/sandbox/
├── app.py                    # Flask backend application
├── index.html                # Frontend UI
├── requirements.txt          # Python dependencies
├── test_weather_app.py       # Automated test suite
└── WEATHER_APP_README.md     # This file
```

### Adding New Features

To extend the app:
1. Modify `app.py` for backend changes
2. Update `index.html` for UI changes
3. Add tests to `test_weather_app.py`

## API Rate Limits

The wttr.in API is free and doesn't require an API key. However, be mindful of rate limits for production use.

## License

This project is open source and available for educational purposes.

## Credits

- Weather data provided by [wttr.in](https://wttr.in)
- Fonts by [Google Fonts](https://fonts.google.com)

---

**Enjoy checking the weather! 🌤️**
