# 🌤️ Weather Application

A complete Python-based weather application that fetches real-time weather data from WeatherAPI.com. Features both a beautiful web interface (Flask) and a command-line interface (CLI).

## ✨ Features

- 🔍 **Search by City**: Get weather for any city worldwide
- 🌡️ **Comprehensive Data**: Temperature, humidity, wind speed, visibility, UV index, and more
- 🎨 **Beautiful UI**: Modern, responsive web interface with gradient backgrounds
- 💻 **CLI Support**: Full-featured command-line interface with colored output
- 🔒 **Error Handling**: Graceful handling of invalid cities, API errors, and network issues
- 🌍 **Multiple Units**: Display temperature in both Celsius and Fahrenheit
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- 🎯 **JSON API**: RESTful API endpoint for programmatic access

## 📋 Requirements

- Python 3.7 or higher
- Free API key from [WeatherAPI.com](https://www.weatherapi.com/signup.aspx)

## 🚀 Quick Start

### 1. Install Dependencies

First, ensure pip is installed:

```bash
python3 -m ensurepip --upgrade
```

Then install required packages:

```bash
pip install -r requirements.txt
```

### 2. Get Your API Key

1. Visit [WeatherAPI.com](https://www.weatherapi.com/signup.aspx)
2. Sign up for a free account (no credit card required)
3. Copy your API key from the dashboard

### 3. Configure Environment

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
WEATHER_API_KEY=your_actual_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. Run the Application

#### Web Interface (Flask)

```bash
python weather_app.py
```

Then open your browser and navigate to:
- **Home Page**: http://127.0.0.1:5000
- **API Endpoint**: http://127.0.0.1:5000/api/weather/London

#### Command Line Interface

```bash
python weather_cli.py London
```

Or:

```bash
python weather_cli.py "New York"
```

Or:

```bash
./weather_cli.py Tokyo
```

## 📖 Usage Guide

### Web Interface

1. **Search for Weather**:
   - Enter a city name in the search box
   - Click "Search" or press Enter
   - View detailed weather information

2. **Quick Search**:
   - Click on any example city button for instant results

3. **Search Another City**:
   - Use the search form at the bottom of the results page

### Command Line Interface

**Basic Usage**:
```bash
python weather_cli.py <city_name>
```

**Examples**:
```bash
python weather_cli.py London
python weather_cli.py "New York"
python weather_cli.py Tokyo
python weather_cli.py --city Paris
```

**Help**:
```bash
python weather_cli.py --help
```

**Version**:
```bash
python weather_cli.py --version
```

### API Endpoint

**Get Weather Data (JSON)**:
```bash
curl http://127.0.0.1:5000/api/weather/London
```

**Response Format**:
```json
{
  "success": true,
  "data": {
    "city": "London",
    "country": "United Kingdom",
    "temperature_c": 15,
    "temperature_f": 59,
    "humidity": 72,
    "wind_kph": 20,
    "condition": "Partly cloudy",
    ...
  }
}
```

## 📁 Project Structure

```
weather-app/
├── weather_app.py           # Flask web application
├── weather_cli.py           # Command-line interface
├── weather_service.py       # Weather API service layer
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── templates/              # HTML templates
│   ├── index.html         # Home page
│   └── weather.html       # Weather results page
└── static/                # Static assets
    ├── css/
    │   └── style.css      # Stylesheet
    └── js/
        └── script.js      # JavaScript
```

## 🎨 Weather Data Displayed

- **Temperature**: Current temperature and "feels like" temperature
- **Condition**: Weather description with emoji representation
- **Humidity**: Relative humidity percentage
- **Wind**: Speed (km/h and mph) and direction
- **Visibility**: Distance in kilometers and miles
- **Pressure**: Atmospheric pressure in millibars
- **UV Index**: UV radiation level
- **Location**: City, region, and country
- **Local Time**: Current time in the searched location

## 🛠️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required
WEATHER_API_KEY=your_api_key_here

# Optional
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
```

### API Configuration

The application uses WeatherAPI.com with the following defaults:
- **Base URL**: http://api.weatherapi.com/v1
- **Timeout**: 10 seconds
- **Free Tier**: 1,000,000 calls/month

## 🔧 Error Handling

The application handles various error scenarios:

- ❌ **Invalid City**: "City not found" message
- ❌ **Empty Input**: "City name cannot be empty"
- ❌ **Network Error**: "Please check your internet connection"
- ❌ **API Error**: "Invalid API key" or "API quota exceeded"
- ❌ **Timeout**: "Request timed out. Please try again"
- ❌ **Missing Config**: "WEATHER_API_KEY not found"

## 🧪 Testing

### Test Valid Cities

```bash
# Web Interface
# Visit http://127.0.0.1:5000 and search for:
# - London
# - New York
# - Tokyo
# - Paris
# - Sydney

# CLI
python weather_cli.py London
python weather_cli.py "New York"
python weather_cli.py Tokyo
```

### Test Error Handling

```bash
# Invalid city
python weather_cli.py "InvalidCityName123"

# Empty input (web interface)
# Leave search box empty and submit

# API endpoint
curl http://127.0.0.1:5000/api/weather/InvalidCity
```

### Test API Endpoint

```bash
# Valid request
curl http://127.0.0.1:5000/api/weather/London

# Invalid request
curl http://127.0.0.1:5000/api/weather/
```

## 🚨 Troubleshooting

### "WEATHER_API_KEY not found"

**Solution**: Create a `.env` file and add your API key:
```bash
cp .env.example .env
# Edit .env and add your API key
```

### "Invalid API key"

**Solution**: 
1. Verify your API key is correct in `.env`
2. Check if your API key is active on WeatherAPI.com
3. Ensure there are no extra spaces in the `.env` file

### "Module not found" errors

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Port 5000 already in use

**Solution**: Change the port in `weather_app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=Config.DEBUG)
```

### CLI colors not showing

**Solution**: Some terminals don't support ANSI colors. The CLI will still work, just without colors.

## 📝 API Rate Limits

WeatherAPI.com free tier includes:
- ✅ 1,000,000 calls per month
- ✅ Current weather data
- ✅ No credit card required
- ✅ No time limit

## 🔐 Security Notes

- Never commit your `.env` file to version control
- Keep your API key private
- Use environment variables for sensitive data
- The `.gitignore` file is configured to exclude `.env`

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Weather data provided by [WeatherAPI.com](https://www.weatherapi.com)
- Built with Flask, Python, and modern web technologies

## 📞 Support

If you encounter any issues:
1. Check the Troubleshooting section above
2. Verify your API key is valid
3. Ensure all dependencies are installed
4. Check that Python 3.7+ is installed

---

**Made with ❤️ using Python and Flask**
