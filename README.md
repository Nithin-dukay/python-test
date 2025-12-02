# Web Automation & Connectivity Testing Toolkit

A comprehensive Python-based toolkit for web browser automation, connectivity testing, and simple web server deployment. This project includes Selenium-based browser automation scripts, network connectivity checkers for popular websites, and a Flask-based "Hello World" web server.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [Web Browser Automation](#web-browser-automation)
  - [Connectivity Checkers](#connectivity-checkers)
  - [Flask Web Server](#flask-web-server)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## ✨ Features

### 🌐 Web Browser Automation
- **Selenium-based automation** with support for Chrome and Firefox browsers
- **Automatic driver management** using webdriver-manager
- **Headless mode support** for CI/CD environments
- **Customizable browser options** for different use cases

### 🔍 Connectivity Testing
- **Comprehensive connectivity checks** using multiple methods:
  - DNS resolution testing
  - Socket-level connectivity
  - HTTP/HTTPS request validation
- **Simple and detailed checkers** for Google and Bing
- **Detailed reporting** with timestamps and response times

### 🚀 Web Server
- **Flask-based web server** serving a beautiful "Hello World" page
- **Health check endpoint** for monitoring
- **Modern UI** with Tailwind CSS

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+** (Python 3.8 or higher recommended)
- **pip** (Python package installer)
- **Chrome or Firefox browser** (for Selenium automation)
- **Internet connection** (for connectivity tests)

## 🔧 Installation

### 1. Clone or Download the Repository

```bash
cd /path/to/project
```

### 2. Install Python Dependencies

First, ensure pip is installed:

```bash
python3 -m ensurepip --upgrade
```

Then install the required packages:

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install selenium>=4.0.0
pip install webdriver-manager>=3.8.0
pip install flask>=2.0.0
pip install requests>=2.25.0
```

### 3. Verify Installation

Test your Selenium setup:

```bash
python3 test_selenium.py
```

## 📁 Project Structure

```
.
├── app.py                          # Flask web server application
├── index.html                      # Hello World web page
├── requirements.txt                # Python dependencies
│
├── selenium_browser.py             # Basic Selenium browser automation
├── selenium_browser_enhanced.py    # Enhanced Selenium with auto driver management
├── test_selenium.py                # Selenium functionality test (headless)
│
├── check_google.py                 # Comprehensive Google connectivity checker
├── check_google_simple.py          # Simple Google status checker
├── check_bing.py                   # Comprehensive Bing connectivity checker
├── check_bing_simple.py            # Simple Bing status checker
│
└── README.md                       # This file
```

## 🚀 Usage

### Web Browser Automation

#### Basic Selenium Browser (Manual Driver Setup)

Opens a browser and navigates to a URL (default: Google):

```bash
python3 selenium_browser.py
```

Navigate to a custom URL:

```bash
python3 selenium_browser.py https://www.example.com
```

#### Enhanced Selenium Browser (Automatic Driver Management)

**Recommended:** Uses webdriver-manager for automatic driver installation:

```bash
python3 selenium_browser_enhanced.py
```

Navigate to a custom URL:

```bash
python3 selenium_browser_enhanced.py https://www.github.com
```

**Features:**
- Automatically downloads and manages ChromeDriver/GeckoDriver
- Fallback to Firefox if Chrome is unavailable
- Displays page title, URL, and basic page information
- Browser stays open for 10 seconds for demonstration

#### Headless Testing

Test Selenium functionality without opening a visible browser:

```bash
python3 test_selenium.py
```

### Connectivity Checkers

#### Google Connectivity Checker

**Comprehensive Check** (DNS, Socket, HTTP):

```bash
python3 check_google.py
```

**Simple Check** (Quick HTTP-only test):

```bash
python3 check_google_simple.py
```

#### Bing Connectivity Checker

**Comprehensive Check** (DNS, Socket, HTTP):

```bash
python3 check_bing.py
```

**Simple Check** (Quick HTTP-only test):

```bash
python3 check_bing_simple.py
```

**Output Example:**
```
============================================================
🌐 GOOGLE.COM CONNECTIVITY CHECKER
============================================================
Target: https://www.google.com
Timeout: 10 seconds
Timestamp: 2025-12-02 10:30:45
------------------------------------------------------------
🔍 Checking DNS resolution for google.com...
✅ SUCCESS: DNS resolution successful!
   IP Address: 142.250.185.46

🔍 Checking socket connectivity to google.com...
✅ SUCCESS: Socket connection to google.com established!
   Connection Time: 0.15 seconds

🔍 Checking HTTP connectivity to google.com...
✅ SUCCESS: Google.com is UP!
   Status Code: 200
   Response Time: 0.23 seconds

============================================================
📊 SUMMARY REPORT
============================================================
DNS Resolution      : ✅ PASS
Socket Connection   : ✅ PASS
HTTP Request        : ✅ PASS
------------------------------------------------------------
🎉 OVERALL STATUS: Google.com is FULLY ACCESSIBLE
```

### Flask Web Server

Start the Flask development server:

```bash
python3 app.py
```

The server will start on `http://0.0.0.0:5000`

**Available Endpoints:**

- **`/`** - Serves the Hello World page
- **`/health`** - Health check endpoint (returns JSON status)

**Access the application:**

```bash
# In your browser
http://localhost:5000

# Health check
curl http://localhost:5000/health
```

**Expected Health Check Response:**
```json
{
  "status": "healthy",
  "message": "Hello World server is running!"
}
```

## 📚 Dependencies

All dependencies are listed in `requirements.txt`:

| Package | Version | Purpose |
|---------|---------|---------|
| `selenium` | ≥4.0.0 | Web browser automation framework |
| `webdriver-manager` | ≥3.8.0 | Automatic WebDriver management |
| `flask` | ≥2.0.0 | Web server framework |
| `requests` | ≥2.25.0 | HTTP library for connectivity tests |

## 🔧 Troubleshooting

### Selenium Issues

**Problem:** `selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH`

**Solution:** Use the enhanced version with webdriver-manager:
```bash
python3 selenium_browser_enhanced.py
```

Or manually install ChromeDriver:
```bash
# On Ubuntu/Debian
sudo apt-get install chromium-chromedriver

# On macOS
brew install chromedriver
```

**Problem:** Browser doesn't open in headless environment

**Solution:** Uncomment the headless mode in the scripts:
```python
chrome_options.add_argument("--headless")
```

### Connectivity Checker Issues

**Problem:** All connectivity tests fail

**Solution:** 
1. Check your internet connection
2. Verify DNS settings
3. Check if a firewall is blocking connections
4. Try the simple checker first to isolate the issue

### Flask Server Issues

**Problem:** `Address already in use`

**Solution:** Change the port in `app.py`:
```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

Or kill the process using port 5000:
```bash
# Find the process
lsof -i :5000

# Kill it
kill -9 <PID>
```

## 🎯 Use Cases

- **Web Scraping & Automation:** Use Selenium scripts as a foundation for web scraping projects
- **CI/CD Testing:** Run headless browser tests in continuous integration pipelines
- **Network Monitoring:** Use connectivity checkers to monitor website availability
- **Learning & Education:** Study web automation and network programming concepts
- **Prototyping:** Quick Flask server setup for testing frontend designs

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📄 License

This project is open source and available for educational and commercial use.

---

**Made with ❤️ using Python, Selenium, Flask, and Tailwind CSS**
