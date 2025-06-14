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
  - `app.py` - Flask web server
  - `selenium_browser.py` - Basic Selenium automation
  - `selenium_browser_enhanced.py` - Enhanced Selenium with auto driver management
  - `test_selenium.py` - Selenium functionality testing
  - `check_google.py` - Comprehensive Google connectivity checker
  - `check_google_simple.py` - Simple Google status checker
  - `check_bing.py` - Comprehensive Bing connectivity checker
  - `check_bing_simple.py` - Simple Bing status checker
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
- Network Testing: Website connectivity checkers for Google, Bing, Facebook

## 📦 Dependencies
- Core Dependencies: selenium, webdriver-manager, flask, requests
- Flask: 3.1.1 with full dependency stack (Blinker, Click, Werkzeug, Jinja2, ItsDangerous, MarkupSafe)
- Browser Support: Chrome WebDriver, Firefox GeckoDriver
- Automation Features: Headless mode, error handling, cleanup
- Network Libraries: requests for HTTP connectivity testing

## 🚀 Deployment
- Server Host: 0.0.0.0 (all interfaces)
- Application Type: Web server
- Entry Command: `python3 app.py`

## 📄 Documentation
- README Files: `README_selenium.md` - Selenium usage documentation
- Requirements: `requirements.txt` - Python package dependencies including Flask and requests

## 🔄 Version Control
- Repository: Git-based
- Branch: main
- Remote: GitHub (Nithin-dukay/python-test)
- Commit Pattern: Descriptive commits with feature summaries
- Recent Activity: Added Flask hello world page, Google/Bing/Facebook connectivity checkers

## 🛠 Utility Scripts
- Website Status Checkers:
  - Google.com connectivity (comprehensive and simple versions)
  - Bing.com connectivity (comprehensive and simple versions)  
  - Facebook.com connectivity (simple version)
- Features: DNS resolution testing, socket connectivity, HTTP status checks, response time measurement