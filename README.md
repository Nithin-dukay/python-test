# Python Web Automation & Connectivity Testing Suite

A comprehensive Python toolkit for web automation, browser testing, and network connectivity verification. This project includes Selenium-based browser automation scripts, connectivity checkers for popular websites, and a simple Flask web server.

## 🚀 Features

- **Selenium Browser Automation**: Automated web browser control with Chrome and Firefox support
- **Connectivity Testing**: Comprehensive network connectivity checks for Google and Bing
- **Flask Web Server**: Simple "Hello World" web application with health check endpoint
- **Headless Testing**: Support for headless browser operations for CI/CD environments
- **Multi-Method Verification**: DNS resolution, socket connections, and HTTP request testing

## 📋 Prerequisites

- Python 3.7 or higher
- Chrome or Firefox browser installed
- ChromeDriver or GeckoDriver (for Selenium automation)

## 🔧 Installation

1. **Clone the repository** (or download the project files)

```bash
git clone <repository-url>
cd <project-directory>
```

2. **Install pip** (if not already installed)

```bash
python3 -m ensurepip --upgrade
```

3. **Install required dependencies**

```bash
pip install -r requirements.txt
```

4. **Install WebDriver** (for Selenium)

For Chrome:
```bash
# Download ChromeDriver from https://chromedriver.chromium.org/
# Or use webdriver-manager (already in requirements.txt)
```

For Firefox:
```bash
# Download GeckoDriver from https://github.com/mozilla/geckodriver/releases
```

## 📦 Dependencies

- `selenium>=4.0.0` - Web browser automation
- `webdriver-manager>=3.8.0` - Automatic WebDriver management
- `flask>=2.0.0` - Web application framework
- `requests>=2.25.0` - HTTP library for connectivity testing

## 🎯 Usage

### 1. Selenium Browser Automation

Open a browser and navigate to a website:

```bash
# Navigate to Google (default)
python3 selenium_browser.py

# Navigate to a custom URL
python3 selenium_browser.py https://www.example.com
```

### 2. Headless Browser Testing

Run Selenium tests in headless mode (no GUI):

```bash
python3 test_selenium.py
```

### 3. Connectivity Checkers

Check if Google is accessible:

```bash
python3 check_google.py
```

Check if Bing is accessible:

```bash
python3 check_bing.py
```

These scripts perform three types of checks:
- DNS resolution
- Socket connection
- HTTP request

### 4. Flask Web Server

Start the Flask development server:

```bash
python3 app.py
```

The server will start on `http://0.0.0.0:5000`

Available endpoints:
- `/` - Serves the index.html page
- `/health` - Health check endpoint (returns JSON status)

## 📁 Project Structure

```
.
├── app.py                      # Flask web server
├── selenium_browser.py         # Main Selenium automation script
├── selenium_browser_enhanced.py # Enhanced browser automation
├── test_selenium.py            # Selenium headless tests
├── check_google.py             # Google connectivity checker
├── check_google_simple.py      # Simplified Google checker
├── check_bing.py               # Bing connectivity checker
├── check_bing_simple.py        # Simplified Bing checker
├── requirements.txt            # Python dependencies
├── index.html                  # Web server homepage
└── README.md                   # This file
```

## 🧪 Testing

### Test Selenium Installation

```bash
python3 test_selenium.py
```

Expected output:
```
=== Selenium Functionality Test ===
Testing Selenium functionality in headless mode...
✅ Chrome driver setup successful!
✅ Page loaded successfully!
🎉 All tests passed! Selenium is working correctly.
```

### Test Network Connectivity

```bash
python3 check_google.py
```

Expected output:
```
🌐 GOOGLE.COM CONNECTIVITY CHECKER
✅ SUCCESS: DNS resolution successful!
✅ SUCCESS: Socket connection to google.com established!
✅ SUCCESS: Google.com is UP!
🎉 OVERALL STATUS: Google.com is FULLY ACCESSIBLE
```

## 🐛 Troubleshooting

### Selenium WebDriver Issues

If you encounter WebDriver errors:

1. Ensure Chrome/Firefox is installed
2. Download the appropriate WebDriver for your browser version
3. Add WebDriver to your system PATH
4. Or use `webdriver-manager` for automatic management

### Connection Timeout Issues

If connectivity checks fail:

1. Verify your internet connection
2. Check firewall settings
3. Ensure DNS is properly configured
4. Try increasing the timeout value in the scripts

### Flask Server Issues

If the Flask server won't start:

1. Check if port 5000 is already in use
2. Try running on a different port: `app.run(port=8080)`
3. Ensure Flask is properly installed: `pip install flask`

## 🔒 Security Notes

- The Flask server runs in debug mode by default (for development only)
- For production deployment, disable debug mode and use a production WSGI server
- Be cautious when running browser automation scripts with untrusted URLs

## 📝 License

This project is provided as-is for educational and testing purposes. Feel free to modify and distribute according to your needs.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Note**: This project is designed for testing and educational purposes. Always ensure you have proper authorization before running automated tests against websites.
