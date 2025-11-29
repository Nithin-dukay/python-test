# Python Test App

A comprehensive Python application featuring a Flask web server, connectivity checkers, Selenium browser automation, and a unified CLI interface with configuration management and structured logging.

## Features

- **Flask Web Application**: Simple "Hello World" web server with health check endpoint
- **Connectivity Checkers**: Tools to verify connectivity to Google, Bing, or custom URLs
- **Selenium Automation**: Browser automation scripts for testing web applications
- **Unified CLI Interface**: Command-line interface to access all features
- **Configuration Management**: YAML-based configuration with environment variable overrides
- **Structured Logging**: Colored console output and rotating file logs
- **Comprehensive Test Suite**: Unit tests with pytest and code coverage

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd python-test
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Using the CLI

The application provides a unified CLI interface for all features:

```bash
# Show help
python cli.py --help

# Show version
python cli.py version

# Run Flask web application
python cli.py run-app

# Check connectivity (simple)
python cli.py check-connectivity --simple

# Check connectivity to custom target
python cli.py check-connectivity --target https://example.com

# Run Selenium test
python cli.py test-selenium --url https://www.google.com

# Run Selenium in headless mode
python cli.py test-selenium --headless
```

### Configuration Management

```bash
# Show current configuration
python cli.py config show

# Get a configuration value
python cli.py config get app.port

# Set a configuration value
python cli.py config set app.port 8080

# Use custom config file
python cli.py --config custom_config.yaml version
```

### Logging Options

```bash
# Enable verbose logging (DEBUG level)
python cli.py --verbose run-app

# Set specific log level
python cli.py --log-level WARNING check-connectivity
```

## Configuration

The application uses a YAML configuration file (`config.yaml`) with the following structure:

```yaml
app:
  name: Python Test App
  version: 1.0.0
  host: 0.0.0.0
  port: 5000
  debug: true

logging:
  level: INFO
  directory: logs
  max_file_size_mb: 10
  backup_count: 5

connectivity:
  timeout: 10
  targets:
    - https://www.google.com
    - https://www.bing.com

selenium:
  headless: false
  window_size: 1920x1080
  timeout: 10
```

### Environment Variable Overrides

You can override configuration values using environment variables:

- `APP_PORT`: Override application port
- `APP_HOST`: Override application host
- `APP_DEBUG`: Override debug mode (true/false)
- `LOG_LEVEL`: Override log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_DIR`: Override log directory

Example:
```bash
export APP_PORT=8080
export LOG_LEVEL=DEBUG
python cli.py run-app
```

## Running Tests

Run the test suite with pytest:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov --cov-report=html

# Run specific test file
pytest tests/test_config_manager.py

# Run with verbose output
pytest -v
```

## Project Structure

```
python-test/
├── app.py                      # Flask web application
├── cli.py                      # Unified CLI interface
├── config.yaml                 # Configuration file
├── config_manager.py           # Configuration management module
├── logger.py                   # Logging module
├── check_google.py             # Google connectivity checker
├── check_bing.py               # Bing connectivity checker
├── selenium_browser.py         # Selenium automation script
├── requirements.txt            # Python dependencies
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   ├── test_cli.py            # CLI tests
│   ├── test_config_manager.py # Config manager tests
│   └── test_logger.py         # Logger tests
└── logs/                       # Log files (created automatically)
```

## CLI Commands Reference

### Main Commands

- `run-app`: Start the Flask web application
  - Options: `--host`, `--port`, `--debug/--no-debug`

- `check-connectivity`: Check connectivity to websites
  - Options: `--target`, `--timeout`, `--simple`

- `test-selenium`: Run Selenium browser automation test
  - Options: `--url`, `--headless/--no-headless`, `--timeout`

- `config`: Manage application configuration
  - Subcommands: `show`, `get <key>`, `set <key> <value>`

- `version`: Show application version

### Global Options

- `--config`, `-c`: Path to configuration file (default: config.yaml)
- `--verbose`, `-v`: Enable verbose output (DEBUG level)
- `--log-level`, `-l`: Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Logging

The application uses structured logging with:

- **Console Output**: Colored logs for easy reading
- **File Logging**: Rotating log files (10MB max, 5 backups)
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

Log files are stored in the `logs/` directory by default.

## Development

### Adding New Features

1. Create a new module for your feature
2. Add configuration options to `config.yaml`
3. Add CLI commands in `cli.py`
4. Write tests in `tests/`
5. Update documentation

### Code Style

This project follows PEP 8 style guidelines. Use tools like `black` and `flake8` for code formatting and linting.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
