from flask import Flask, render_template, send_from_directory, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the weather app page"""
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'Weather app is running!'}

@app.route('/api/weather/<city>')
def get_weather(city):
    """Fetch weather data for a given city"""
    try:
        # Use wttr.in API - no API key required
        url = f'https://wttr.in/{city}?format=j1'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
            return jsonify({
                'error': 'City not found',
                'message': f'Could not find weather data for "{city}"'
            }), 404
        
        if response.status_code != 200:
            return jsonify({
                'error': 'API error',
                'message': 'Failed to fetch weather data'
            }), 500
        
        data = response.json()
        
        # Extract relevant weather information
        current = data['current_condition'][0]
        location = data['nearest_area'][0]
        
        weather_data = {
            'city': location['areaName'][0]['value'],
            'country': location['country'][0]['value'],
            'region': location.get('region', [{}])[0].get('value', ''),
            'temperature_c': current['temp_C'],
            'temperature_f': current['temp_F'],
            'feels_like_c': current['FeelsLikeC'],
            'feels_like_f': current['FeelsLikeF'],
            'condition': current['weatherDesc'][0]['value'],
            'humidity': current['humidity'],
            'wind_speed_kmph': current['windspeedKmph'],
            'wind_speed_mph': current['windspeedMiles'],
            'wind_direction': current['winddir16Point'],
            'pressure': current['pressure'],
            'visibility': current['visibility'],
            'uv_index': current['uvIndex'],
            'weather_icon': current['weatherCode']
        }
        
        return jsonify(weather_data)
    
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Timeout',
            'message': 'Request timed out. Please try again.'
        }), 504
    
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Network error',
            'message': 'Failed to connect to weather service'
        }), 503
    
    except (KeyError, IndexError) as e:
        return jsonify({
            'error': 'Data error',
            'message': 'Failed to parse weather data'
        }), 500
    
    except Exception as e:
        return jsonify({
            'error': 'Server error',
            'message': 'An unexpected error occurred'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
