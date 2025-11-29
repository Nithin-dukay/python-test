# Weather Info App 🌤️

A comprehensive Flask-based web application that provides real-time weather information for cities worldwide using the OpenWeatherMap API.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)
- [Performance & Caching](#performance--caching)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- 🌡️ **Real-time Weather Data**: Current temperature with feels-like information
- 💨 **Wind Information**: Wind speed and direction details
- 💧 **Humidity & Pressure**: Atmospheric pressure and humidity levels
- 🌅 **Sunrise & Sunset**: Accurate sunrise and sunset times
- 👁️ **Visibility**: Current visibility conditions
- 🔄 **Unit Conversion**: Toggle between Celsius and Fahrenheit
- 📱 **Responsive Design**: Works seamlessly on all devices
- ⚡ **Fast & Cached**: Optimized performance with data caching
- 🔌 **RESTful API**: JSON API endpoint for developers
- 🎨 **Modern UI**: Beautiful, intuitive interface with Bootstrap 5
- 🔍 **Input Validation**: Comprehensive input sanitization and validation
- 📊 **Detailed Weather Cards**: Organized display of weather metrics
- 🌍 **Global Coverage**: Search weather for any city worldwide

## 🎬 Demo

### Home Page
The home page features a clean search interface with popular city shortcuts.

### Weather Display
Detailed weather information with:
- Current temperature and conditions
- Feels-like temperature
- High/Low temperatures
- Humidity and pressure
- Wind speed and direction
- Sunrise and sunset times
- Visibility and cloudiness

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 3.0+**: Web framework
- **Flask-Caching**: Response caching for performance
- **Requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management

### Frontend
- **HTML5 & CSS3**: Structure and styling
- **Bootstrap 5**: Responsive UI framework
- **JavaScript (ES6+)**: Client-side interactivity
- **Google Fonts**: Typography (Inter font family)

### API
- **OpenWeatherMap API**: Weather data provider

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)
- A web browser (Chrome, Firefox, Safari, etc.)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Get OpenWeatherMap API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to API Keys section
4. Generate a new API key (free tier allows 60 calls/minute)

### 2. Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
cp .env.example .env
```

Edit the `.env` file and add your API key:

```env
# OpenWeatherMap API Configuration
OPENWEATHERMAP_API_KEY=your_actual_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here

# Cache Configuration (in seconds)
CACHE_DEFAULT_TIMEOUT=600
```

**Important**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

## 🏃 Running the Application

### Development Mode

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📡 API Documentation

### Get Weather Data (JSON)

**Endpoint**: `/api/weather/<city>`

**Method**: `GET`

**Parameters**:
- `city` (string, required): Name of the city

**Example Request**:
```bash
curl http://localhost:5000/api/weather/London
```

**Success Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "city": "London",
    "country": "GB",
    "temp_celsius": 15.5,
    "temp_fahrenheit": 59.9,
    "feels_like_celsius": 14.2,
    "feels_like_fahrenheit": 57.6,
    "temp_min_celsius": 13.0,
    "temp_max_celsius": 17.0,
    "humidity": 72,
    "pressure": 1013,
    "wind_speed": 5.5,
    "wind_direction": "NW",
    "wind_deg": 315,
    "description": "Partly cloudy",
    "main": "Clouds",
    "icon": "02d",
    "icon_url": "https://openweathermap.org/img/wn/02d@2x.png",
    "sunrise": "06:45 AM",
    "sunset": "08:30 PM",
    "visibility": 10.0,
    "cloudiness": 40,
    "timestamp": "2025-11-29 12:00:00"
  }
}
```

**Error Response** (404 Not Found):
```json
{
  "success": false,
  "error": "City 'InvalidCity' not found. Please check the spelling and try again."
}
```

**Error Response** (400 Bad Request):
```json
{
  "success": false,
  "error": "Invalid city name"
}
```

### Health Check

**Endpoint**: `/health`

**Method**: `GET`

**Response**:
```json
{
  "status": "healthy",
  "message": "Weather Info App is running!",
  "api_configured": true
}
```

## 📁 Project Structure

```
weather-info-app/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
├── templates/                 # HTML templates
│   ├── base.html             # Base template with navigation
│   ├── index.html            # Home page with search form
│   ├── weather.html          # Weather display page
│   ├── about.html            # About page
│   ├── 404.html              # 404 error page
│   └── 500.html              # 500 error page
└── static/                    # Static assets
    ├── css/
    │   └── style.css         # Custom styles
    └── js/
        └── main.js           # JavaScript functionality
```

## 💡 Usage Examples

### Search for Weather

1. Open the application in your browser: `http://localhost:5000`
2. Enter a city name in the search box (e.g., "London", "New York", "Tokyo")
3. Click "Search" or press Enter
4. View detailed weather information

### Toggle Temperature Units

On the weather display page, click the "Switch to °F" button to toggle between Celsius and Fahrenheit.

### Use Popular Cities

Click any of the popular city buttons on the home page for quick access to weather information.

### API Integration

Use the JSON API endpoint in your applications:

```python
import requests

response = requests.get('http://localhost:5000/api/weather/Paris')
data = response.json()

if data['success']:
    weather = data['data']
    print(f"Temperature in {weather['city']}: {weather['temp_celsius']}°C")
```

## 🛡️ Error Handling

The application includes comprehensive error handling for:

- **Invalid City Names**: Validates input and provides helpful error messages
- **API Connection Errors**: Handles network timeouts and connection issues
- **Rate Limit Exceeded**: Manages API rate limits gracefully
- **Missing API Key**: Alerts users if API key is not configured
- **404 Errors**: Custom 404 page for non-existent routes
- **500 Errors**: Custom 500 page for server errors

## ⚡ Performance & Caching

### Caching Strategy

Weather data is cached for **10 minutes** (600 seconds) per city to:
- Reduce API calls and stay within rate limits
- Improve response times
- Minimize server load

### Cache Configuration

Modify cache timeout in `.env`:

```env
CACHE_DEFAULT_TIMEOUT=600  # 10 minutes in seconds
```

### Cache Behavior

- First request for a city fetches fresh data from API
- Subsequent requests within 10 minutes use cached data
- Cache automatically expires after timeout
- Each city has its own cache entry

## 🔒 Security Features

- **Input Validation**: All user inputs are validated and sanitized
- **Environment Variables**: Sensitive data stored in `.env` file
- **HTTPS Ready**: Can be deployed with SSL/TLS certificates
- **No Data Storage**: No personal information is collected or stored
- **Rate Limiting**: Built-in protection against API abuse

## 🐛 Troubleshooting

### API Key Not Working

1. Verify your API key is correct in `.env`
2. Check if the API key is activated (may take a few minutes after creation)
3. Ensure you haven't exceeded the free tier limits (60 calls/minute)

### City Not Found

1. Check the spelling of the city name
2. Try using the full city name
3. Some cities may require country codes (e.g., "Paris, FR")

### Application Won't Start

1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check if port 5000 is available
3. Verify Python version is 3.8 or higher: `python --version`

### Caching Issues

Clear the cache by restarting the application or modifying the cache timeout.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for providing the weather API
- [Bootstrap](https://getbootstrap.com/) for the UI framework
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Google Fonts](https://fonts.google.com/) for the Inter font family

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [API Documentation](#api-documentation)
3. Open an issue on GitHub

## 🚀 Future Enhancements

Potential features for future versions:

- [ ] 5-day weather forecast
- [ ] Weather maps and radar
- [ ] Historical weather data
- [ ] Weather alerts and notifications
- [ ] User accounts and saved locations
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Weather comparison between cities
- [ ] Export weather data (PDF, CSV)
- [ ] Mobile app (React Native/Flutter)

---

**Made with ❤️ using Flask and OpenWeatherMap API**
