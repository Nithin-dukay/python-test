# Selenium Web Browser Automation

This repository contains Python scripts that demonstrate how to use Selenium to open and control web browsers.

## Files

- `selenium_browser.py` - Basic Selenium script that opens a web browser
- `selenium_browser_enhanced.py` - Enhanced version with automatic driver management
- `requirements.txt` - Python dependencies

## Installation

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

2. Make sure you have either Chrome or Firefox browser installed on your system.

## Usage

### Basic Script
```bash
python selenium_browser.py
```

Or with a custom URL:
```bash
python selenium_browser.py https://www.example.com
```

### Enhanced Script (Recommended)
```bash
python selenium_browser_enhanced.py
```

Or with a custom URL:
```bash
python selenium_browser_enhanced.py https://www.example.com
```

## Features

- Automatic browser detection (Chrome first, then Firefox)
- Automatic WebDriver management (enhanced version)
- Error handling and cleanup
- Customizable URL navigation
- Basic page interaction demonstrations

## Requirements

- Python 3.6+
- Selenium 4.0+
- Chrome or Firefox browser
- Internet connection (for downloading drivers automatically)

## Notes

- The enhanced script uses `webdriver-manager` to automatically download and manage browser drivers
- Both scripts will keep the browser open for 10 seconds to demonstrate functionality
- To run in headless mode (without GUI), uncomment the headless option in the scripts
