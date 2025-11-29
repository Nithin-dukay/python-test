from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_caching import Cache
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure caching
cache_timeout = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 600))
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = cache_timeout
cache = Cache(app)

# OpenWeatherMap API configuration
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'


def validate_city_name(city):
    """Validate and sanitize city name input."""
    if not city or not isinstance(city, str):
        return None
    
    # Remove extra whitespace and limit length
    city = city.strip()[:100]
    
    # Check if city name contains only valid characters
    if not city or not all(c.isalnum() or c.isspace() or c in '-,.' for c in city):
        return None
    
    return city


def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    return round(kelvin - 273.15, 1)


def kelvin_to_fahrenheit(kelvin):
    """Convert Kelvin to Fahrenheit."""
    return round((kelvin - 273.15) * 9/5 + 32, 1)


def get_wind_direction(degrees):
    """Convert wind direction degrees to compass direction."""
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    index = round(degrees / 22.5) % 16
    return directions[index]


def format_timestamp(timestamp):
    """Format Unix timestamp to readable time."""
    return datetime.fromtimestamp(timestamp).strftime('%I:%M %p')


@cache.memoize(timeout=cache_timeout)
def fetch_weather_data(city):
    """
    Fetch weather data from OpenWeatherMap API.
    Results are cached to reduce API calls.
    """
    if not API_KEY:
        logger.error("OpenWeatherMap API key not configured")
        return None, "API key not configured. Please set OPENWEATHERMAP_API_KEY in .env file"
    
    try:
        params = {
            'q': city,
            'appid': API_KEY
        }
        
        logger.info(f"Fetching weather data for city: {city}")
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            logger.info(f"Successfully fetched weather data for {city}")
            return response.json(), None
        elif response.status_code == 404:
            logger.warning(f"City not found: {city}")
            return None, f"City '{city}' not found. Please check the spelling and try again."
        elif response.status_code == 401:
            logger.error("Invalid API key")
            return None, "Invalid API key. Please check your configuration."
        elif response.status_code == 429:
            logger.error("API rate limit exceeded")
            return None, "Too many requests. Please try again later."
        else:
            logger.error(f"API error: {response.status_code}")
            return None, f"Error fetching weather data (Status: {response.status_code})"
    
    except requests.exceptions.Timeout:
        logger.error("Request timeout")
        return None, "Request timeout. Please try again."
    except requests.exceptions.ConnectionError:
        logger.error("Connection error")
        return None, "Connection error. Please check your internet connection."
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None, "An unexpected error occurred. Please try again."


def process_weather_data(data):
    """Process raw weather data into a formatted dictionary."""
    if not data:
        return None
    
    try:
        processed = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temp_celsius': kelvin_to_celsius(data['main']['temp']),
            'temp_fahrenheit': kelvin_to_fahrenheit(data['main']['temp']),
            'feels_like_celsius': kelvin_to_celsius(data['main']['feels_like']),
            'feels_like_fahrenheit': kelvin_to_fahrenheit(data['main']['feels_like']),
            'temp_min_celsius': kelvin_to_celsius(data['main']['temp_min']),
            'temp_max_celsius': kelvin_to_celsius(data['main']['temp_max']),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': round(data['wind']['speed'], 1),
            'wind_direction': get_wind_direction(data['wind'].get('deg', 0)),
            'wind_deg': data['wind'].get('deg', 0),
            'description': data['weather'][0]['description'].capitalize(),
            'main': data['weather'][0]['main'],
            'icon': data['weather'][0]['icon'],
            'icon_url': f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
            'sunrise': format_timestamp(data['sys']['sunrise']),
            'sunset': format_timestamp(data['sys']['sunset']),
            'visibility': data.get('visibility', 0) / 1000,  # Convert to km
            'cloudiness': data['clouds']['all'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return processed
    except (KeyError, TypeError) as e:
        logger.error(f"Error processing weather data: {str(e)}")
        return None


@app.route('/')
def index():
    """Render the home page with search form."""
    return render_template('index.html')


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    """Display weather information for a city."""
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
    else:
        city = request.args.get('city', '').strip()
    
    # Validate city name
    city = validate_city_name(city)
    if not city:
        flash('Please enter a valid city name', 'error')
        return redirect(url_for('index'))
    
    # Fetch weather data
    data, error = fetch_weather_data(city)
    
    if error:
        flash(error, 'error')
        return redirect(url_for('index'))
    
    # Process weather data
    weather_info = process_weather_data(data)
    
    if not weather_info:
        flash('Error processing weather data. Please try again.', 'error')
        return redirect(url_for('index'))
    
    return render_template('weather.html', weather=weather_info)


@app.route('/api/weather/<city>')
def api_weather(city):
    """API endpoint to get weather data in JSON format."""
    # Validate city name
    city = validate_city_name(city)
    if not city:
        return jsonify({
            'success': False,
            'error': 'Invalid city name'
        }), 400
    
    # Fetch weather data
    data, error = fetch_weather_data(city)
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        }), 404 if 'not found' in error.lower() else 500
    
    # Process weather data
    weather_info = process_weather_data(data)
    
    if not weather_info:
        return jsonify({
            'success': False,
            'error': 'Error processing weather data'
        }), 500
    
    return jsonify({
        'success': True,
        'data': weather_info
    })


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Weather Info App is running!',
        'api_configured': API_KEY is not None
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {str(error)}")
    return render_template('500.html'), 500


if __name__ == '__main__':
    if not API_KEY:
        logger.warning("⚠️  OPENWEATHERMAP_API_KEY not set! Please configure it in .env file")
        logger.warning("Get your free API key from: https://openweathermap.org/api")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
