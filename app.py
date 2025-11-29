"""
Weather Fetching Application using Flask and OpenWeatherMap API
"""
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# OpenWeatherMap API configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'


def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius"""
    return round(kelvin - 273.15, 1)


def kelvin_to_fahrenheit(kelvin):
    """Convert Kelvin to Fahrenheit"""
    return round((kelvin - 273.15) * 9/5 + 32, 1)


def fetch_weather_data(city):
    """
    Fetch weather data from OpenWeatherMap API
    
    Args:
        city (str): City name to fetch weather for
        
    Returns:
        dict: Weather data or error information
    """
    if not API_KEY:
        return {
            'error': True,
            'message': 'API key not configured. Please set OPENWEATHER_API_KEY in .env file.'
        }
    
    try:
        params = {
            'q': city,
            'appid': API_KEY
        }
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process and format weather data
            weather_info = {
                'error': False,
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature_celsius': kelvin_to_celsius(data['main']['temp']),
                'temperature_fahrenheit': kelvin_to_fahrenheit(data['main']['temp']),
                'feels_like_celsius': kelvin_to_celsius(data['main']['feels_like']),
                'feels_like_fahrenheit': kelvin_to_fahrenheit(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_deg': data['wind'].get('deg', 0),
                'description': data['weather'][0]['description'].capitalize(),
                'main': data['weather'][0]['main'],
                'icon': data['weather'][0]['icon'],
                'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                'clouds': data['clouds']['all'],
                'timestamp': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
            }
            
            return weather_info
            
        elif response.status_code == 404:
            return {
                'error': True,
                'message': f'City "{city}" not found. Please check the spelling and try again.'
            }
        elif response.status_code == 401:
            return {
                'error': True,
                'message': 'Invalid API key. Please check your OPENWEATHER_API_KEY configuration.'
            }
        else:
            return {
                'error': True,
                'message': f'Error fetching weather data. Status code: {response.status_code}'
            }
            
    except requests.exceptions.Timeout:
        return {
            'error': True,
            'message': 'Request timed out. Please try again later.'
        }
    except requests.exceptions.ConnectionError:
        return {
            'error': True,
            'message': 'Connection error. Please check your internet connection.'
        }
    except Exception as e:
        return {
            'error': True,
            'message': f'An unexpected error occurred: {str(e)}'
        }


def fetch_forecast_data(city):
    """
    Fetch 5-day weather forecast from OpenWeatherMap API
    
    Args:
        city (str): City name to fetch forecast for
        
    Returns:
        list: List of forecast data for next 5 days
    """
    if not API_KEY:
        return []
    
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'cnt': 40  # 5 days * 8 (3-hour intervals)
        }
        
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            forecast_list = []
            
            # Get one forecast per day (at noon)
            for item in data['list'][::8][:5]:  # Every 8th item (24h), max 5 days
                forecast_list.append({
                    'date': datetime.fromtimestamp(item['dt']).strftime('%a, %b %d'),
                    'temp_celsius': kelvin_to_celsius(item['main']['temp']),
                    'temp_fahrenheit': kelvin_to_fahrenheit(item['main']['temp']),
                    'description': item['weather'][0]['description'].capitalize(),
                    'icon': item['weather'][0]['icon']
                })
            
            return forecast_list
        else:
            return []
            
    except Exception:
        return []


@app.route('/')
def index():
    """Home page with search form"""
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def weather():
    """Weather results page"""
    city = request.form.get('city', '').strip()
    
    if not city:
        return render_template('error.html', 
                             error_message='Please enter a city name.')
    
    weather_data = fetch_weather_data(city)
    
    if weather_data['error']:
        return render_template('error.html', 
                             error_message=weather_data['message'])
    
    # Fetch forecast data
    forecast_data = fetch_forecast_data(city)
    
    return render_template('weather.html', 
                         weather=weather_data,
                         forecast=forecast_data)


@app.route('/api/weather/<city>')
def api_weather(city):
    """API endpoint to fetch weather data programmatically"""
    if not city:
        return jsonify({
            'error': True,
            'message': 'City parameter is required'
        }), 400
    
    weather_data = fetch_weather_data(city)
    
    if weather_data['error']:
        return jsonify(weather_data), 404 if 'not found' in weather_data['message'] else 500
    
    return jsonify(weather_data), 200


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('error.html', 
                         error_message='Page not found.'), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return render_template('error.html', 
                         error_message='Internal server error. Please try again later.'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
