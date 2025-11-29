#!/usr/bin/env python3
"""
Weather CLI - Command Line Interface for Weather Application
"""
import sys
import argparse
from weather_service import WeatherService, WeatherServiceError
from config import Config


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_colored(text, color):
    """Print colored text to terminal"""
    print(f"{color}{text}{Colors.END}")


def print_weather(weather_data, service):
    """
    Display weather data in a formatted way
    
    Args:
        weather_data: Dictionary containing weather information
        service: WeatherService instance for emoji generation
    """
    emoji = service.get_weather_emoji(weather_data['condition'], weather_data['is_day'])
    
    print("\n" + "=" * 60)
    print_colored(f"  {emoji}  Weather for {weather_data['city']}", Colors.BOLD + Colors.CYAN)
    
    if weather_data['region']:
        print(f"  {weather_data['region']}, {weather_data['country']}")
    else:
        print(f"  {weather_data['country']}")
    
    print(f"  Local Time: {weather_data['local_time']}")
    print("=" * 60)
    
    # Main weather info
    print_colored("\n🌡️  TEMPERATURE", Colors.BOLD + Colors.YELLOW)
    print(f"  Current: {weather_data['temperature_c']}°C ({weather_data['temperature_f']}°F)")
    print(f"  Feels Like: {weather_data['feels_like_c']}°C ({weather_data['feels_like_f']}°F)")
    
    print_colored(f"\n☁️  CONDITION", Colors.BOLD + Colors.BLUE)
    print(f"  {weather_data['condition']}")
    
    # Detailed info
    print_colored("\n📊 DETAILS", Colors.BOLD + Colors.GREEN)
    print(f"  💧 Humidity: {weather_data['humidity']}%")
    print(f"  💨 Wind Speed: {weather_data['wind_kph']} km/h ({weather_data['wind_mph']} mph)")
    print(f"  🧭 Wind Direction: {weather_data['wind_direction']}")
    print(f"  👁️  Visibility: {weather_data['visibility_km']} km ({weather_data['visibility_miles']} mi)")
    print(f"  🌡️  Pressure: {weather_data['pressure_mb']} mb")
    print(f"  🔆 UV Index: {weather_data['uv_index']}")
    
    print("\n" + "=" * 60 + "\n")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='Weather CLI - Get current weather information for any city',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s London
  %(prog)s "New York"
  %(prog)s Tokyo
  %(prog)s --city Paris

Get your free API key from: https://www.weatherapi.com/signup.aspx
Set it in .env file as: WEATHER_API_KEY=your_key_here
        """
    )
    
    parser.add_argument(
        'city',
        nargs='?',
        help='Name of the city to get weather for'
    )
    
    parser.add_argument(
        '-c', '--city',
        dest='city_flag',
        help='Name of the city (alternative way to specify)'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='Weather CLI v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Get city name from either positional or flag argument
    city = args.city or args.city_flag
    
    if not city:
        parser.print_help()
        print_colored("\n❌ Error: Please provide a city name", Colors.RED)
        sys.exit(1)
    
    try:
        # Validate configuration
        Config.validate()
        
        # Create weather service and fetch data
        print_colored(f"\n🔍 Fetching weather data for '{city}'...", Colors.CYAN)
        
        weather_service = WeatherService()
        weather_data = weather_service.get_weather(city)
        
        # Display results
        print_weather(weather_data, weather_service)
        
    except ValueError as e:
        print_colored(f"\n❌ Configuration Error: {e}", Colors.RED)
        print("\nPlease follow these steps:")
        print("1. Copy .env.example to .env")
        print("2. Get a free API key from: https://www.weatherapi.com/signup.aspx")
        print("3. Add your API key to .env file")
        sys.exit(1)
        
    except WeatherServiceError as e:
        print_colored(f"\n❌ Weather Service Error: {e}", Colors.RED)
        sys.exit(1)
        
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  Operation cancelled by user", Colors.YELLOW)
        sys.exit(0)
        
    except Exception as e:
        print_colored(f"\n❌ Unexpected Error: {e}", Colors.RED)
        sys.exit(1)


if __name__ == '__main__':
    main()
