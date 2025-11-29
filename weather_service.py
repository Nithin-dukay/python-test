"""
Weather Service Module
Handles all weather API interactions and data processing
"""
import requests
from typing import Dict, Optional
from config import Config


class WeatherServiceError(Exception):
    """Custom exception for weather service errors"""
    pass


class WeatherService:
    """Service class for fetching and processing weather data"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize weather service
        
        Args:
            api_key: Weather API key (uses config if not provided)
        """
        self.api_key = api_key or Config.WEATHER_API_KEY
        self.base_url = Config.WEATHER_API_BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT
        
        if not self.api_key:
            raise WeatherServiceError(
                "API key is required. Please set WEATHER_API_KEY in .env file"
            )
    
    def get_weather(self, city: str) -> Dict:
        """
        Fetch current weather data for a city
        
        Args:
            city: Name of the city
            
        Returns:
            Dictionary containing weather data
            
        Raises:
            WeatherServiceError: If API request fails or city not found
        """
        if not city or not city.strip():
            raise WeatherServiceError("City name cannot be empty")
        
        city = city.strip()
        
        try:
            url = f"{self.base_url}/current.json"
            params = {
                'key': self.api_key,
                'q': city,
                'aqi': 'no'
            }
            
            response = requests.get(
                url,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._process_weather_data(data)
            elif response.status_code == 400:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Invalid city name')
                raise WeatherServiceError(f"City not found: {error_message}")
            elif response.status_code == 401:
                raise WeatherServiceError("Invalid API key. Please check your configuration")
            elif response.status_code == 403:
                raise WeatherServiceError("API key exceeded quota or disabled")
            else:
                raise WeatherServiceError(f"API error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            raise WeatherServiceError("Request timed out. Please try again")
        except requests.exceptions.ConnectionError:
            raise WeatherServiceError("Network error. Please check your internet connection")
        except requests.exceptions.RequestException as e:
            raise WeatherServiceError(f"Request failed: {str(e)}")
        except ValueError as e:
            raise WeatherServiceError(f"Invalid response format: {str(e)}")
    
    def _process_weather_data(self, data: Dict) -> Dict:
        """
        Process and format weather data from API response
        
        Args:
            data: Raw API response data
            
        Returns:
            Formatted weather data dictionary
        """
        try:
            location = data.get('location', {})
            current = data.get('current', {})
            condition = current.get('condition', {})
            
            return {
                'city': location.get('name', 'Unknown'),
                'region': location.get('region', ''),
                'country': location.get('country', ''),
                'local_time': location.get('localtime', ''),
                'temperature_c': current.get('temp_c', 0),
                'temperature_f': current.get('temp_f', 0),
                'feels_like_c': current.get('feelslike_c', 0),
                'feels_like_f': current.get('feelslike_f', 0),
                'humidity': current.get('humidity', 0),
                'wind_kph': current.get('wind_kph', 0),
                'wind_mph': current.get('wind_mph', 0),
                'wind_direction': current.get('wind_dir', ''),
                'pressure_mb': current.get('pressure_mb', 0),
                'visibility_km': current.get('vis_km', 0),
                'visibility_miles': current.get('vis_miles', 0),
                'uv_index': current.get('uv', 0),
                'condition': condition.get('text', 'Unknown'),
                'condition_icon': condition.get('icon', ''),
                'is_day': current.get('is_day', 1) == 1,
            }
        except (KeyError, TypeError) as e:
            raise WeatherServiceError(f"Error processing weather data: {str(e)}")
    
    def get_weather_emoji(self, condition: str, is_day: bool = True) -> str:
        """
        Get emoji representation of weather condition
        
        Args:
            condition: Weather condition text
            is_day: Whether it's daytime
            
        Returns:
            Emoji string
        """
        condition_lower = condition.lower()
        
        if 'sunny' in condition_lower or 'clear' in condition_lower:
            return '☀️' if is_day else '🌙'
        elif 'cloud' in condition_lower:
            if 'partly' in condition_lower:
                return '⛅'
            return '☁️'
        elif 'rain' in condition_lower or 'drizzle' in condition_lower:
            if 'heavy' in condition_lower:
                return '🌧️'
            return '🌦️'
        elif 'thunder' in condition_lower or 'storm' in condition_lower:
            return '⛈️'
        elif 'snow' in condition_lower:
            return '❄️'
        elif 'mist' in condition_lower or 'fog' in condition_lower:
            return '🌫️'
        elif 'wind' in condition_lower:
            return '💨'
        else:
            return '🌡️'
