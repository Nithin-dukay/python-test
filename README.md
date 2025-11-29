# Python Web Automation & Connectivity Testing Toolkit

A comprehensive Python toolkit for web browser automation using Selenium and network connectivity testing. This project provides multiple utilities for automated web browsing, website status checking, and a simple Flask web server.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Selenium Browser Automation](#selenium-browser-automation)
  - [Website Connectivity Checkers](#website-connectivity-checkers)
  - [Flask Web Server](#flask-web-server)
- [Scripts Overview](#scripts-overview)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Selenium Browser Automation**: Automated web browser control with Chrome and Firefox support
- **Automatic WebDriver Management**: Uses webdriver-manager for hassle-free driver setup
- **Connectivity Testing**: Comprehensive network connectivity checks (DNS, Socket, HTTP)
- **Multiple Testing Modes**: Both headless and GUI browser modes
- **Flask Web Server**: Simple "Hello World" web application
- **Cross-Platform Support**: Works on Linux, macOS, and Windows

## 📁 Project Structure

```
.
├── app.py                          # Flask web server application
├── selenium_browser.py             # Basic Selenium browser automation
├── selenium_browser_enhanced.py    # Enhanced Selenium with auto driver management
├── test_selenium.py                # Selenium functionality tests (headless)
├── check_google.py                 # Comprehensive Google.com connectivity checker
├── check_google_simple.py          # Simple Google.com status checker
├── check_bing.py                   # Comprehensive Bing.com connectivity checker
├── check_bing_simple.py            # Simple Bing.com status checker
├── requirements.txt                # Python dependencies
├── index.html                      # HTML page for Flask server
└── README.md                       # This file
```

## 📦 Requirements

### System Requirements
- Python 3.7 or higher
- Chrome or Firefox browser installed
- Internet connection (for connectivity tests)

### Python Dependencies
- `selenium>=4.0.0` - Web browser automation
- `webdriver-manager>=3.8.0` - Automatic WebDriver management
- `flask>=2.0.0` - Web framework
- `requests>=2.25.0` - HTTP library

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Python Dependencies
```bash
# Install pip if not already installed
python3 -m ensurepip --upgrade

# Install required packages
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
# Test Selenium installation
python3 test_selenium.py

# Test connectivity checker
python3 check_google_simple.py
```

## 💻 Usage

### Selenium Browser Automation

#### Basic Browser Automation
Opens a browser and navigates to a URL (default: Google):
```bash
# Navigate to default URL (Google)
python3 selenium_browser.py

# Navigate to custom URL
python3 selenium_browser.py https://www.example.com
```

#### Enhanced Browser Automation (Recommended)
Uses webdriver-manager for automatic driver management:
```bash
# Navigate to default URL
python3 selenium_browser_enhanced.py

# Navigate to custom URL
python3 selenium_browser_enhanced.py https://www.github.com
```

#### Headless Testing
Run Selenium tests in headless mode (no GUI):
```bash
python3 test_selenium.py
```

**Note**: To enable headless mode in other scripts, uncomment the headless argument in the script:
```python
chrome_options.add_argument("--headless")
```

### Website Connectivity Checkers

#### Comprehensive Connectivity Check
Performs DNS, Socket, and HTTP connectivity tests:

```bash
# Check Google.com
python3 check_google.py

# Check Bing.com
python3 check_bing.py
```

**Output includes**:
- DNS resolution status and IP address
- Socket connection status and timing
- HTTP request status and response time
- Comprehensive summary report

#### Simple Status Check
Quick website availability check:

```bash
# Quick Google.com check
python3 check_google_simple.py

# Quick Bing.com check
python3 check_bing_simple.py
```

### Flask Web Server

Start the Flask development server:
```bash
python3 app.py
```

The server will start on `http://0.0.0.0:5000`

**Available endpoints**:
- `/` - Serves the index.html page
- `/health` - Health check endpoint (returns JSON status)

Access the server:
```bash
# In a browser
http://localhost:5000

# Using curl
curl http://localhost:5000/health
```

## 📚 Scripts Overview

### Browser Automation Scripts

| Script | Description | Features |
|--------|-------------|----------|
| `selenium_browser.py` | Basic Selenium automation | Manual driver setup, Chrome/Firefox support |
| `selenium_browser_enhanced.py` | Enhanced automation | Auto driver management, better error handling |
| `test_selenium.py` | Headless testing | Automated tests in headless mode |

### Connectivity Testing Scripts

| Script | Description | Use Case |
|--------|-------------|----------|
| `check_google.py` | Comprehensive Google check | Full diagnostics (DNS, Socket, HTTP) |
| `check_google_simple.py` | Simple Google check | Quick availability check |
| `check_bing.py` | Comprehensive Bing check | Full diagnostics (DNS, Socket, HTTP) |
| `check_bing_simple.py` | Simple Bing check | Quick availability check |

### Web Server

| Script | Description | Port |
|--------|-------------|------|
| `app.py` | Flask web server | 5000 |

## ⚙️ Configuration

### Selenium Configuration

**Timeout Settings**: Modify timeout values in scripts:
```python
self.timeout = 10  # seconds
```

**Browser Options**: Customize Chrome options:
```python
chrome_options.add_argument("--headless")        # Headless mode
chrome_options.add_argument("--no-sandbox")      # Disable sandbox
chrome_options.add_argument("--disable-gpu")     # Disable GPU
chrome_options.add_argument("--window-size=1920,1080")  # Window size
```

### Flask Configuration

**Host and Port**: Modify in `app.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

**Debug Mode**: Set `debug=False` for production

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
   ```bash
   git fork <repository-url>
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Include error handling
   - Test your changes thoroughly

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Ensure all tests pass

### Code Style Guidelines

- Follow [PEP 8](https://pep8.org/) Python style guide
- Use meaningful variable and function names
- Add comments for complex logic
- Include docstrings for all functions and classes
- Keep functions focused and concise

### Reporting Issues

- Use the issue tracker to report bugs
- Include Python version, OS, and error messages
- Provide steps to reproduce the issue
- Suggest potential solutions if possible

## 📄 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🔧 Troubleshooting

### Common Issues

**1. WebDriver not found**
```bash
# Solution: Use the enhanced version with webdriver-manager
python3 selenium_browser_enhanced.py
```

**2. Chrome/Firefox not installed**
```bash
# Install Chrome on Ubuntu/Debian
sudo apt-get install google-chrome-stable

# Install Firefox on Ubuntu/Debian
sudo apt-get install firefox
```

**3. Permission denied errors**
```bash
# Make scripts executable
chmod +x *.py
```

**4. Module not found errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**5. Connection timeout issues**
- Check your internet connection
- Verify firewall settings
- Try increasing timeout values in scripts

## 📞 Support

For questions, issues, or suggestions:
- Open an issue in the repository
- Check existing issues for solutions
- Review the troubleshooting section

## 🎯 Future Enhancements

- [ ] Add support for Edge and Safari browsers
- [ ] Implement screenshot capture functionality
- [ ] Add more comprehensive test suites
- [ ] Create Docker container for easy deployment
- [ ] Add CI/CD pipeline configuration
- [ ] Implement logging functionality
- [ ] Add configuration file support (YAML/JSON)
- [ ] Create REST API for connectivity checks

---

**Made with ❤️ using Python, Selenium, and Flask**
