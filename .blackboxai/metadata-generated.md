automation_tools:
- Selenium WebDriver
browser_automation:
  headless_mode: true
  supported_browsers:
  - Chrome
  - Firefox
  webdriver_management: webdriver_manager
dependencies:
  selenium: latest
  webdriver_manager: latest
frameworks:
- Selenium
git_workflow:
  branch: main
  commit_style: descriptive with feature lists
languages:
- Python
modules:
- selenium
- webdriver_manager
package_manager: pip
primary_language: Python
project_structure:
  automation_scripts:
  - selenium_browser.py
  - selenium_browser_enhanced.py
  documentation:
  - README_selenium.md
  requirements: requirements.txt
runtime_env: python3
testing:
  test_files:
  - test_selenium.py
  test_framework: custom
