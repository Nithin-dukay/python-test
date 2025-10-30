# Weather Report App - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Start the Server
```bash
python3 app.py
```

### Step 2: Open Your Browser
Navigate to: **http://localhost:5000**

### Step 3: Search for Weather
Type any city name and click "Search"!

---

## 📋 Quick Commands

### Start the Application
```bash
cd /vercel/sandbox
python3 app.py
```

### Run Tests
```bash
python3 test_weather_app.py
```

### Test API Directly
```bash
# Get weather for any city
curl http://localhost:5000/api/weather/London

# Check server health
curl http://localhost:5000/health
```

---

## 🌟 Features at a Glance

- **Search any city** worldwide
- **Toggle temperature** between °C and °F
- **View detailed weather** including:
  - Current temperature & feels-like
  - Weather conditions
  - Humidity
  - Wind speed & direction
  - Atmospheric pressure
  - Visibility

---

## 🎨 What You'll See

1. **Beautiful gradient background** (purple theme)
2. **Clean search interface** with instant results
3. **Comprehensive weather card** with all details
4. **Responsive design** that works on any device

---

## 🔧 Troubleshooting

**Server won't start?**
```bash
pip install -r requirements.txt
```

**Can't connect?**
- Make sure the server is running on port 5000
- Check if another service is using port 5000

**City not found?**
- Try different spelling
- Use English city names
- Check for typos

---

## 📚 More Information

- Full documentation: `WEATHER_APP_README.md`
- Project summary: `WEATHER_APP_SUMMARY.txt`
- Test suite: `test_weather_app.py`

---

**Enjoy your weather app! 🌤️☀️🌧️**
