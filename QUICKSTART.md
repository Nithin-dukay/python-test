# 🚀 Quick Start Guide

## Get Started in 3 Minutes!

### Step 1: Get Your Free API Key (1 minute)

1. Visit: https://www.weatherapi.com/signup.aspx
2. Sign up (no credit card required)
3. Copy your API key from the dashboard

### Step 2: Configure the App (30 seconds)

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and replace 'your_api_key_here' with your actual API key
# You can use any text editor: nano, vim, or just edit the file
```

Your `.env` file should look like:
```
WEATHER_API_KEY=abc123your_actual_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Step 3: Run the App (30 seconds)

**Option A: Web Interface**
```bash
python weather_app.py
```
Then open: http://127.0.0.1:5000

**Option B: Command Line**
```bash
python weather_cli.py London
```

## 🎯 Quick Examples

### Web Interface
```bash
# Start the server
python weather_app.py

# Open in browser: http://127.0.0.1:5000
# Search for: London, New York, Tokyo, Paris, Sydney
```

### CLI Examples
```bash
# Single word cities
python weather_cli.py London
python weather_cli.py Tokyo
python weather_cli.py Paris

# Multi-word cities (use quotes)
python weather_cli.py "New York"
python weather_cli.py "Los Angeles"
python weather_cli.py "San Francisco"

# Alternative syntax
python weather_cli.py --city London
```

### API Endpoint
```bash
# Get JSON weather data
curl http://127.0.0.1:5000/api/weather/London

# Pretty print with jq (if installed)
curl http://127.0.0.1:5000/api/weather/London | jq
```

## ✅ Verify Installation

Run the test suite to ensure everything works:
```bash
python test_weather_app.py
```

You should see:
```
🎉 ALL TESTS PASSED!
```

## 🆘 Troubleshooting

### "WEATHER_API_KEY not found"
- Make sure you created the `.env` file
- Check that your API key is in the file
- No spaces around the `=` sign

### "Invalid API key"
- Verify your API key is correct
- Check if it's active on weatherapi.com
- Make sure you copied the entire key

### "Module not found"
```bash
pip install -r requirements.txt
```

### Port 5000 already in use
Edit `weather_app.py` and change the port:
```python
app.run(host='0.0.0.0', port=5001, debug=Config.DEBUG)
```

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.

## 🎉 You're Ready!

That's it! You now have a fully functional weather application.

Try searching for your city and enjoy! 🌤️
