# Project Metadata

## 🧑‍💻 Languages & Frameworks
- Primary Language: Python
- Languages Used: Python, HTML, CSS, Shell
- Frameworks: Flask
- Frontend: HTML5 with Tailwind CSS (CDN)

## 🔧 Tooling & Build System
- Package Manager: pip
- Runtime: Python 3.10
- Dependencies: Flask 3.1.1, requests

## 📁 Code Structure & Modules
- Entry Point: `app.py`
- Static Files: `index.html`
- Configuration: `requirements.txt`
- Utility Scripts: 
  - `check_google.py`, `check_google_simple.py`
  - `check_bing.py`, `check_bing_simple.py`
  - `check_facebook_simple.py`

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

## 📦 Dependencies
- Flask: 3.1.1
- requests: 2.32.3
- Blinker: 1.9.0
- Click: 8.2.1
- Werkzeug: 3.1.3
- Jinja2: 3.1.6
- ItsDangerous: 2.2.0
- MarkupSafe: 3.0.2

## 🔧 Utility Scripts
- Website Status Checkers:
  - Google.com connectivity checker (comprehensive and simple versions)
  - Bing.com connectivity checker (comprehensive and simple versions)
  - Facebook.com connectivity checker (simple version)
- Features: DNS resolution, socket connectivity, HTTP status checks
- Output: Colored status messages with timestamps and response times

## 🚀 Deployment
- Server Host: 0.0.0.0 (all interfaces)
- Application Type: Web server
- Entry Command: `python3 app.py`

## 📄 Project Files
- `app.py` - Flask web server
- `index.html` - Hello world page with modern styling
- `requirements.txt` - Python dependencies
- `check_google.py` - Comprehensive Google connectivity checker
- `check_google_simple.py` - Simple Google status checker
- `check_bing.py` - Comprehensive Bing connectivity checker
- `check_bing_simple.py` - Simple Bing status checker
- `check_facebook_simple.py` - Simple Facebook status checker

## 🔄 Version Control
- Repository: Nithin-dukay/python-test
- Branch: main
- Recent Commits: 
  - Hello world page implementation with Flask server
  - Google.com connectivity checker scripts
  - Bing.com connectivity checker scripts
  - Facebook.com connectivity checker script

## 🧪 Testing & Functionality
- All connectivity checkers tested and verified working
- Flask server tested with browser launch
- Scripts made executable with proper shebang lines
- Error handling implemented for network connectivity issues