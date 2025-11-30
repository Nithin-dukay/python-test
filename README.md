# Python Test Suite

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

A comprehensive Python testing and automation toolkit featuring web connectivity checkers, Selenium browser automation, and a Flask web server for testing purposes.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [Web Connectivity Checkers](#web-connectivity-checkers)
  - [Selenium Browser Automation](#selenium-browser-automation)
  - [Flask Web Server](#flask-web-server)
- [Requirements](#requirements)
- [Running Tests](#running-tests)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🎯 Overview

This repository contains a collection of Python scripts designed for testing web connectivity, browser automation using Selenium, and a simple Flask web server. It's ideal for developers who need to:

- Test network connectivity to popular websites
- Automate browser interactions for testing
- Run a simple web server for development/testing
- Learn Selenium WebDriver basics

## ✨ Features

- **🌐 Web Connectivity Checkers**: Comprehensive connectivity testing for Google and Bing
  - DNS resolution checks
  - Socket connection testing
  - HTTP request validation
  - Detailed reporting with timestamps and metrics

- **🤖 Selenium Browser Automation**: Full-featured browser automation scripts
  - Chrome and Firefox support
  - Headless mode capability
  - Configurable options for different environments
  - Example scripts for learning and testing

- **🚀 Flask Web Server**: Lightweight web server for testing
  - Simple "Hello World" endpoint
  - Health check endpoint
  - Static file serving

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Chrome or Firefox browser (for Selenium scripts)
- ChromeDriver or GeckoDriver (for Selenium scripts)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/python-test.git
cd python-test
```

### Step 2: Install pip (if not already installed)

```bash
# On Amazon Linux 2023 / RHEL-based systems
sudo dnf install python3-pip -y

# On Debian/Ubuntu-based systems
sudo apt-get install python3-pip -y
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Browser Drivers (for Selenium)

**Option 1: Using webdriver-manager (Recommended)**

The project uses `webdriver-manager` which automatically downloads and manages browser drivers.

**Option 2: Manual Installation**

- **ChromeDriver**: Download from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
- **GeckoDriver**: Download from [GeckoDriver Releases](https://github.com/mozilla/geckodriver/releases)

Add the driver to your system PATH or place it in the project directory.

## 📁 Project Structure

```
python-test/
│
├── app.py                          # Flask web server application
├── requirements.txt                # Project dependencies
├── index.html                      # Static HTML file for Flask server
│
├── check_google.py                 # Comprehensive Google connectivity checker
├── check_google_simple.py          # Simplified Google connectivity checker
├── check_bing.py                   # Comprehensive Bing connectivity checker
├── check_bing_simple.py            # Simplified Bing connectivity checker
│
├── selenium_browser.py             # Selenium browser automation (GUI mode)
├── selenium_browser_enhanced.py    # Enhanced Selenium automation script
├── test_selenium.py                # Selenium functionality test (headless)
│
├── README.md                       # This file
├── README_selenium.md              # Selenium-specific documentation
│
└── *.txt                           # Various test files
```

## 🚀 Usage

### Web Connectivity Checkers

#### Check Google Connectivity

Run comprehensive connectivity tests for Google.com:

```bash
python3 check_google.py
```

Run simplified connectivity check:

```bash
python3 check_google_simple.py
```

#### Check Bing Connectivity

Run comprehensive connectivity tests for Bing.com:

```bash
python3 check_bing.py
```

Run simplified connectivity check:

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
Timestamp: 2025-11-30 12:00:00
------------------------------------------------------------
🔍 Checking DNS resolution for google.com...
✅ SUCCESS: DNS resolution successful!
   IP Address: 142.250.185.46
...
```

### Selenium Browser Automation

#### Basic Browser Automation (GUI Mode)

Open a browser and navigate to a URL:

```bash
# Navigate to default URL (Google)
python3 selenium_browser.py

# Navigate to custom URL
python3 selenium_browser.py https://www.example.com
```

#### Headless Browser Testing

Run Selenium tests in headless mode (no GUI):

```bash
python3 test_selenium.py
```

**Features:**
- Automatic Chrome driver setup
- Headless mode for CI/CD environments
- Element detection and interaction
- Page load verification

### Flask Web Server

Start the Flask development server:

```bash
python3 app.py
```

The server will start on `http://0.0.0.0:5000`

**Available Endpoints:**

- `GET /` - Serves the index.html page
- `GET /health` - Health check endpoint

**Test the server:**

```bash
# Test the main endpoint
curl http://localhost:5000/

# Test the health check
curl http://localhost:5000/health
```

## 📋 Requirements

All dependencies are listed in `requirements.txt`:

```
selenium>=4.0.0          # Browser automation framework
webdriver-manager>=3.8.0 # Automatic WebDriver management
flask>=2.0.0             # Web framework
requests>=2.25.0         # HTTP library
```

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **RAM**: Minimum 2GB (4GB recommended for Selenium)
- **Browser**: Chrome 90+ or Firefox 88+ (for Selenium scripts)

## 🧪 Running Tests

### Test Selenium Installation

Verify that Selenium is properly installed and configured:

```bash
python3 test_selenium.py
```

Expected output:
```
=== Selenium Functionality Test ===
Testing Selenium functionality in headless mode...
✅ Chrome driver setup successful!
Navigating to: https://httpbin.org/html
✅ Page loaded successfully!
...
🎉 All tests passed! Selenium is working correctly.
```

### Test Web Connectivity

Run all connectivity checkers:

```bash
# Test Google connectivity
python3 check_google.py

# Test Bing connectivity
python3 check_bing.py
```

### Test Flask Server

1. Start the server:
   ```bash
   python3 app.py
   ```

2. In another terminal, test the endpoints:
   ```bash
   curl http://localhost:5000/health
   ```

## ⚙️ Configuration

### Selenium Configuration

Edit the Chrome options in `selenium_browser.py` or `test_selenium.py`:

```python
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")  # Enable headless mode
chrome_options.add_argument("--window-size=1920,1080")
```

### Flask Configuration

Modify `app.py` to change server settings:

```python
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',    # Listen on all interfaces
        port=5000,          # Port number
        debug=True          # Enable debug mode
    )
```

### Connectivity Checker Configuration

Adjust timeout values in checker scripts:

```python
class GoogleConnectivityChecker:
    def __init__(self):
        self.url = "https://www.google.com"
        self.timeout = 10  # Adjust timeout in seconds
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/python-test.git
   cd python-test
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, documented code
   - Follow PEP 8 style guidelines
   - Add tests if applicable

4. **Test your changes**
   ```bash
   python3 test_selenium.py
   python3 check_google.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Describe your changes in detail

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists
2. Create a new issue with a clear title and description
3. Include steps to reproduce (for bugs)
4. Add relevant logs or screenshots

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 Python Test Suite Contributors

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

## 📞 Contact

### Project Maintainer

- **Name**: Python Test Suite Team
- **Email**: contact@pythontest.dev
- **GitHub**: [@pythontest](https://github.com/pythontest)

### Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/python-test/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/python-test/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/python-test/wiki)

### Community

- **Discord**: [Join our Discord server](https://discord.gg/pythontest)
- **Twitter**: [@pythontest](https://twitter.com/pythontest)
- **Stack Overflow**: Tag your questions with `python-test`

---

## 🙏 Acknowledgments

- [Selenium](https://www.selenium.dev/) - Browser automation framework
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Requests](https://requests.readthedocs.io/) - HTTP library
- All contributors who have helped improve this project

## 📚 Additional Resources

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/en/2.3.x/)
- [Python Requests Documentation](https://requests.readthedocs.io/en/latest/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

---

**Made with ❤️ by the Python Test Suite Team**

*Last Updated: November 30, 2025*
