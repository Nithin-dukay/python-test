"""
Weather Application - Flask Web Server
"""
from flask import Flask, render_template, request, jsonify
from weather_service import WeatherService, WeatherServiceError
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    """Home page with search form"""
    return render_template('index.html')


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    """Weather display page"""
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
    else:
        city = request.args.get('city', '').strip()
    
    if not city:
        return render_template('index.html', error="Please enter a city name")
    
    try:
        weather_service = WeatherService()
        weather_data = weather_service.get_weather(city)
        emoji = weather_service.get_weather_emoji(
            weather_data['condition'],
            weather_data['is_day']
        )
        weather_data['emoji'] = emoji
        
        return render_template('weather.html', weather=weather_data)
    
    except WeatherServiceError as e:
        return render_template('index.html', error=str(e))
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return render_template('index.html', error="An unexpected error occurred. Please try again.")


@app.route('/api/weather/<city>')
def api_weather(city):
    """JSON API endpoint for weather data"""
    try:
        weather_service = WeatherService()
        weather_data = weather_service.get_weather(city)
        emoji = weather_service.get_weather_emoji(
            weather_data['condition'],
            weather_data['is_day']
        )
        weather_data['emoji'] = emoji
        
        return jsonify({
            'success': True,
            'data': weather_data
        })
    
    except WeatherServiceError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'success': False,
            'error': "An unexpected error occurred"
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html', error="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('index.html', error="Internal server error"), 500


if __name__ == '__main__':
    try:
        Config.validate()
        print("=" * 60)
        print("🌤️  Weather Application Starting...")
        print("=" * 60)
        print(f"Server running at: http://127.0.0.1:5000")
        print(f"API endpoint: http://127.0.0.1:5000/api/weather/<city>")
        print("Press CTRL+C to quit")
        print("=" * 60)
        app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        exit(1)
