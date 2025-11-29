# python-test

A Python project with web automation, connectivity checking, and data validation utilities.

## Features

### 🔍 Data Validator
A comprehensive data validation utility that validates common data types with detailed error handling and metadata.

**Supported Validations:**
- ✉️ Email addresses (RFC 5322 compliant)
- 📱 Phone numbers (international formats)
- 🌐 URLs (HTTP/HTTPS/FTP)
- 📅 Dates (multiple formats)
- 💳 Credit cards (Luhn algorithm)
- 🌍 IP addresses (IPv4/IPv6)

### Installation

```bash
pip install -r requirements.txt
```

### Usage

#### Basic Usage

```python
from data_validator import DataValidator

validator = DataValidator()

# Validate email
result = validator.validate_email("user@example.com")
if result.is_valid:
    print(f"✅ Valid email: {result.value}")
    print(f"Domain: {result.metadata['domain']}")
else:
    print(f"❌ Invalid: {result.error_message}")
```

#### Email Validation

```python
# Valid emails
validator.validate_email("user@example.com")
validator.validate_email("test.user+tag@example.co.uk")

# Returns ValidationResult with metadata:
# - local_part: The part before @
# - domain: The domain name
```

#### Phone Number Validation

```python
# Validate phone numbers
validator.validate_phone("+1-555-123-4567")
validator.validate_phone("+44 20 7946 0958")

# With country code requirement
validator.validate_phone("+1-555-123-4567", country_code="+1")

# Returns metadata:
# - digits: Phone number with only digits
# - length: Number of digits
```

#### URL Validation

```python
# Validate URLs
validator.validate_url("https://www.example.com")
validator.validate_url("http://localhost:8080")

# Require HTTPS
validator.validate_url("https://secure.com", require_https=True)

# Returns metadata:
# - scheme: Protocol (http, https, ftp)
# - domain: Domain name
# - path: URL path
# - is_secure: Whether using secure protocol
```

#### Date Validation

```python
# Supports multiple formats
validator.validate_date("2024-12-31")
validator.validate_date("31/12/2024")
validator.validate_date("December 31, 2024")

# Specify exact format
validator.validate_date("2024-12-31", date_format="%Y-%m-%d")

# Returns metadata:
# - parsed_date: datetime object
# - format: Detected format
# - iso_format: ISO 8601 format
```

#### Credit Card Validation

```python
# Validates using Luhn algorithm
validator.validate_credit_card("4532015112830366")  # Visa
validator.validate_credit_card("5425233430109903")  # Mastercard

# Accepts various formats
validator.validate_credit_card("4532-0151-1283-0366")
validator.validate_credit_card("4532 0151 1283 0366")

# Returns metadata:
# - card_type: Visa, Mastercard, Amex, Discover
# - length: Number of digits
# - masked: Masked number (****0366)
```

#### IP Address Validation

```python
# IPv4 and IPv6
validator.validate_ip_address("192.168.1.1")
validator.validate_ip_address("2001:0db8:85a3::8a2e:370:7334")

# Specify version
validator.validate_ip_address("192.168.1.1", version=4)

# Returns metadata:
# - version: 4 or 6
# - is_private: Private IP range
# - is_loopback: Loopback address
# - is_multicast: Multicast address
```

#### ValidationResult Object

All validation methods return a `ValidationResult` object:

```python
result = validator.validate_email("user@example.com")

# Properties
result.is_valid      # bool: True if valid
result.value         # The validated value
result.error_message # Error message if invalid
result.metadata      # dict: Additional information

# Can be used as boolean
if result:
    print("Valid!")
```

#### Running the Demo

```bash
python data_validator.py
```

#### Running Tests

```bash
pytest test_data_validator.py -v
```

### Other Features

- **Flask Web Application**: Simple web server with health check endpoint
- **Selenium Browser Automation**: Web scraping and testing utilities
- **Connectivity Checkers**: Tools to verify network connectivity

### Running the Flask App

```bash
python app.py
```

Visit `http://localhost:5000` for the web interface or `http://localhost:5000/health` for the health check endpoint.
