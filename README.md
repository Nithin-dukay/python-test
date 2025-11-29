# Weather Fetching Application

A complete weather fetching application built with Flask and OpenWeatherMap API. Get real-time weather information for any city around the world with a beautiful, responsive interface.

## Features

- 🌡️ **Current Weather Data**: Temperature, humidity, wind speed, pressure, visibility
- 📅 **5-Day Forecast**: Weather predictions for the next 5 days
- 🎨 **Beautiful UI**: Clean, modern, and responsive design using Bootstrap 5
- 🔍 **City Search**: Search weather by city name with form validation
- 🌐 **RESTful API**: Programmatic access to weather data via API endpoint
- ⚠️ **Error Handling**: User-friendly error messages for invalid cities or API failures
- 📱 **Mobile Responsive**: Works seamlessly on all devices

## Screenshots

### Home Page
Clean search interface with gradient background and feature highlights.

### Weather Results
Detailed weather information with current conditions and 5-day forecast.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **API**: OpenWeatherMap API
- **Environment Management**: python-dotenv

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- OpenWeatherMap API key (free tier available)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get OpenWeatherMap API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your API key

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
OPENWEATHER_API_KEY=your_actual_api_key_here
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

## Usage

### Running the Application

Start the Flask development server:

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Enter a city name in the search box (e.g., "London", "New York", "Tokyo")
3. Click "Search" to view current weather and 5-day forecast
4. Use the "Back to Search" button to search for another city

### Using the API Endpoint

Get weather data programmatically:

```bash
# Get weather for a specific city
curl http://localhost:5000/api/weather/London

# Example response
{
  "error": false,
  "city": "London",
  "country": "GB",
  "temperature_celsius": 15.2,
  "temperature_fahrenheit": 59.4,
  "feels_like_celsius": 14.1,
  "feels_like_fahrenheit": 57.4,
  "humidity": 72,
  "pressure": 1013,
  "wind_speed": 3.5,
  "wind_deg": 230,
  "description": "Partly cloudy",
  "main": "Clouds",
  "icon": "02d",
  "visibility": 10.0,
  "clouds": 40,
  "timestamp": "2025-11-29 12:30:45",
  "sunrise": "07:45:12",
  "sunset": "16:23:45"
}
```

## Project Structure

```
weather-app/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # Project documentation
├── templates/             # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page with search form
│   ├── weather.html      # Weather results page
│   └── error.html        # Error page
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Custom styles
    └── js/               # JavaScript files (if needed)
```

## API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with search form |
| `/weather` | POST | Weather results page |
| `/api/weather/<city>` | GET | API endpoint for weather data |

## Features in Detail

### Current Weather Display
- Temperature in Celsius and Fahrenheit
- "Feels like" temperature
- Weather description with icon
- Humidity percentage
- Wind speed and direction
- Atmospheric pressure
- Visibility distance
- Cloud coverage percentage
- Sunrise and sunset times

### 5-Day Forecast
- Daily temperature predictions
- Weather conditions with icons
- Easy-to-read date format

### Error Handling
- Invalid city names
- Missing or invalid API key
- Network connection issues
- API rate limiting
- Server errors

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENWEATHER_API_KEY` | Your OpenWeatherMap API key | Yes |
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `FLASK_ENV` | Environment (development/production) | No |
| `FLASK_DEBUG` | Enable debug mode | No |

### API Rate Limits

Free tier OpenWeatherMap API limits:
- 60 calls per minute
- 1,000,000 calls per month

## Troubleshooting

### API Key Issues
- Ensure your API key is correctly set in `.env`
- Verify the API key is active (may take a few hours after creation)
- Check for any typos in the API key

### City Not Found
- Check spelling of city name
- Try using the full city name
- Some cities may require country code (e.g., "Paris,FR")

### Connection Errors
- Verify internet connection
- Check if OpenWeatherMap API is accessible
- Ensure firewall isn't blocking the connection

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

### Running in Production

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Weather data provided by [OpenWeatherMap](https://openweathermap.org/)
- UI framework: [Bootstrap 5](https://getbootstrap.com/)
- Icons and fonts: [Google Fonts](https://fonts.google.com/)

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Built with ❤️ using Flask and OpenWeatherMap API**
