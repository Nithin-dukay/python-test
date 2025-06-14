# Project Metadata

## 🧑‍💻 Languages & Frameworks
- Primary Language: Python
- Languages Used: Python, HTML, CSS, Shell
- Frameworks: Flask, Selenium WebDriver

## 🔧 Tooling & Build System
- Package Manager: pip
- Virtual Environment: system python
- Runtime: Python 3.10

## 📁 Code Structure & Modules
- Modules: Root directory structure with various test files
- Entry Points: 
  - `selenium_browser.py` - Basic Selenium automation
  - `selenium_browser_enhanced.py` - Enhanced Selenium with auto driver management
  - `test_selenium.py` - Selenium functionality testing
  - `app.py` - Flask web server
  - `check_google.py` - Google connectivity checker (comprehensive)
  - `check_google_simple.py` - Google connectivity checker (simple)
  - `check_bing.py` - Bing connectivity checker (comprehensive)
  - `check_bing_simple.py` - Bing connectivity checker (simple)
  - `check_facebook_simple.py` - Facebook connectivity checker

## 🌐 Web Application
- Server Framework: Flask
- Host Configuration: 0.0.0.0
- Default Port: 5000
- Routes:
  - `/` - Serves hello world page
  - `/health` - Health check endpoint

## 🎨 Frontend & Styling
- CSS Framework: Tailwind CSS (via CDN)
- Design: Responsive design with gradient background
- Features: Interactive hover effects, modern styling
- Static Files: `index.html` - Hello world page

## 🧪 Testing & Automation
- Testing Framework: Custom test scripts
- Browser Automation: Selenium WebDriver
- Supported Browsers: Chrome (headless), Firefox
- WebDriver Management: Automatic driver detection and setup
- Network Connectivity Testing: Multiple website status checkers

## 📦 Dependencies
- Core Dependencies: selenium, webdriver-manager, flask, requests
- Browser Support: Chrome WebDriver, Firefox GeckoDriver
- Automation Features: Headless mode, error handling, cleanup
- Web Framework: Flask 3.1.1 with dependencies (Blinker, Click, Werkzeug, Jinja2, ItsDangerous, MarkupSafe)

## 🔗 Network Monitoring
- Website Status Checkers: Google, Bing, Facebook
- Connectivity Tests: DNS resolution, socket connection, HTTP requests
- Response Metrics: Status codes, response times, connection times

## 📄 Documentation
- README Files: `README_selenium.md` - Selenium usage documentation
- Requirements: `requirements.txt` - Python package dependencies

## 🚀 Deployment
- Server Host: 0.0.0.0 (all interfaces)
- Application Type: Web server with network monitoring tools
- Entry Command: `python3 app.py`

## 🔄 Version Control
- Repository: Git-based
- Branch: main
- Remote: GitHub (Nithin-dukay/python-test)
- Commit Pattern: Descriptive commits with feature summaries
- Recent Activity: Added Flask hello world page, network connectivity checkers for multiple websites