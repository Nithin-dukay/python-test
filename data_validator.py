#!/usr/bin/env python3
"""
Data Validator Module
This module provides comprehensive validation functions for common data types
including emails, phone numbers, URLs, dates, credit cards, and IP addresses.
"""

import re
import ipaddress
from datetime import datetime
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class ValidationResult:
    """
    Represents the result of a validation operation
    
    Attributes:
        is_valid (bool): Whether the validation passed
        value (Any): The validated value
        error_message (str): Error message if validation failed
        metadata (dict): Additional information about the validation
    """
    
    def __init__(self, is_valid: bool, value: Any = None, 
                 error_message: str = "", metadata: Optional[Dict] = None):
        self.is_valid = is_valid
        self.value = value
        self.error_message = error_message
        self.metadata = metadata or {}
    
    def __bool__(self):
        return self.is_valid
    
    def __repr__(self):
        status = "✅ VALID" if self.is_valid else "❌ INVALID"
        return f"ValidationResult({status}, value={self.value}, error={self.error_message})"


class DataValidator:
    """
    Main validator class providing various data validation methods
    """
    
    # Email regex pattern (RFC 5322 simplified)
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    # Phone number pattern (international format)
    PHONE_PATTERN = re.compile(
        r'^\+?[1-9]\d{0,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
    )
    
    # Supported date formats
    DATE_FORMATS = [
        '%Y-%m-%d',           # 2024-12-31
        '%d/%m/%Y',           # 31/12/2024
        '%m/%d/%Y',           # 12/31/2024
        '%Y/%m/%d',           # 2024/12/31
        '%d-%m-%Y',           # 31-12-2024
        '%m-%d-%Y',           # 12-31-2024
        '%B %d, %Y',          # December 31, 2024
        '%d %B %Y',           # 31 December 2024
        '%Y-%m-%d %H:%M:%S',  # 2024-12-31 23:59:59
    ]
    
    @staticmethod
    def validate_email(email: str) -> ValidationResult:
        """
        Validate an email address
        
        Args:
            email (str): Email address to validate
            
        Returns:
            ValidationResult: Validation result with details
        """
        if not email or not isinstance(email, str):
            return ValidationResult(
                False, 
                email, 
                "Email must be a non-empty string"
            )
        
        email = email.strip()
        
        if len(email) > 254:
            return ValidationResult(
                False, 
                email, 
                "Email address is too long (max 254 characters)"
            )
        
        if not DataValidator.EMAIL_PATTERN.match(email):
            return ValidationResult(
                False, 
                email, 
                "Invalid email format"
            )
        
        # Additional checks
        local_part, domain = email.rsplit('@', 1)
        
        if len(local_part) > 64:
            return ValidationResult(
                False, 
                email, 
                "Local part of email is too long (max 64 characters)"
            )
        
        if '..' in email:
            return ValidationResult(
                False, 
                email, 
                "Email cannot contain consecutive dots"
            )
        
        return ValidationResult(
            True, 
            email, 
            "",
            {"local_part": local_part, "domain": domain}
        )
    
    @staticmethod
    def validate_phone(phone: str, country_code: Optional[str] = None) -> ValidationResult:
        """
        Validate a phone number
        
        Args:
            phone (str): Phone number to validate
            country_code (str, optional): Expected country code (e.g., '+1', '+44')
            
        Returns:
            ValidationResult: Validation result with details
        """
        if not phone or not isinstance(phone, str):
            return ValidationResult(
                False, 
                phone, 
                "Phone number must be a non-empty string"
            )
        
        phone = phone.strip()
        
        # Remove common separators for length check
        digits_only = re.sub(r'[-.\s()+]', '', phone)
        
        if not digits_only.isdigit():
            return ValidationResult(
                False, 
                phone, 
                "Phone number contains invalid characters"
            )
        
        if len(digits_only) < 7 or len(digits_only) > 15:
            return ValidationResult(
                False, 
                phone, 
                "Phone number must be between 7 and 15 digits"
            )
        
        if not DataValidator.PHONE_PATTERN.match(phone):
            return ValidationResult(
                False, 
                phone, 
                "Invalid phone number format"
            )
        
        # Check country code if specified
        if country_code:
            if not phone.startswith(country_code):
                return ValidationResult(
                    False, 
                    phone, 
                    f"Phone number must start with country code {country_code}"
                )
        
        return ValidationResult(
            True, 
            phone, 
            "",
            {"digits": digits_only, "length": len(digits_only)}
        )
    
    @staticmethod
    def validate_url(url: str, require_https: bool = False) -> ValidationResult:
        """
        Validate a URL
        
        Args:
            url (str): URL to validate
            require_https (bool): Whether to require HTTPS protocol
            
        Returns:
            ValidationResult: Validation result with details
        """
        if not url or not isinstance(url, str):
            return ValidationResult(
                False, 
                url, 
                "URL must be a non-empty string"
            )
        
        url = url.strip()
        
        try:
            parsed = urlparse(url)
            
            # Check for scheme
            if not parsed.scheme:
                return ValidationResult(
                    False, 
                    url, 
                    "URL must include a protocol (http:// or https://)"
                )
            
            # Check for valid scheme
            if parsed.scheme not in ['http', 'https', 'ftp', 'ftps']:
                return ValidationResult(
                    False, 
                    url, 
                    f"Invalid URL scheme: {parsed.scheme}"
                )
            
            # Check HTTPS requirement
            if require_https and parsed.scheme != 'https':
                return ValidationResult(
                    False, 
                    url, 
                    "URL must use HTTPS protocol"
                )
            
            # Check for netloc (domain)
            if not parsed.netloc:
                return ValidationResult(
                    False, 
                    url, 
                    "URL must include a domain name"
                )
            
            # Basic domain validation
            # Extract hostname without port
            hostname = parsed.netloc.split(':')[0] if ':' in parsed.netloc else parsed.netloc
            if '.' not in hostname and hostname != 'localhost':
                return ValidationResult(
                    False, 
                    url, 
                    "Invalid domain name"
                )
            
            return ValidationResult(
                True, 
                url, 
                "",
                {
                    "scheme": parsed.scheme,
                    "domain": parsed.netloc,
                    "path": parsed.path,
                    "is_secure": parsed.scheme in ['https', 'ftps']
                }
            )
            
        except Exception as e:
            return ValidationResult(
                False, 
                url, 
                f"Invalid URL format: {str(e)}"
            )
    
    @staticmethod
    def validate_date(date_string: str, date_format: Optional[str] = None) -> ValidationResult:
        """
        Validate a date string
        
        Args:
            date_string (str): Date string to validate
            date_format (str, optional): Expected date format (strftime format)
            
        Returns:
            ValidationResult: Validation result with details
        """
        if not date_string or not isinstance(date_string, str):
            return ValidationResult(
                False, 
                date_string, 
                "Date must be a non-empty string"
            )
        
        date_string = date_string.strip()
        
        # If specific format provided, try only that format
        if date_format:
            try:
                parsed_date = datetime.strptime(date_string, date_format)
                return ValidationResult(
                    True, 
                    date_string, 
                    "",
                    {
                        "parsed_date": parsed_date,
                        "format": date_format,
                        "iso_format": parsed_date.isoformat()
                    }
                )
            except ValueError as e:
                return ValidationResult(
                    False, 
                    date_string, 
                    f"Date does not match format {date_format}: {str(e)}"
                )
        
        # Try all supported formats
        for fmt in DataValidator.DATE_FORMATS:
            try:
                parsed_date = datetime.strptime(date_string, fmt)
                return ValidationResult(
                    True, 
                    date_string, 
                    "",
                    {
                        "parsed_date": parsed_date,
                        "format": fmt,
                        "iso_format": parsed_date.isoformat()
                    }
                )
            except ValueError:
                continue
        
        return ValidationResult(
            False, 
            date_string, 
            f"Date format not recognized. Supported formats: {', '.join(DataValidator.DATE_FORMATS[:5])}..."
        )
    
    @staticmethod
    def validate_credit_card(card_number: str) -> ValidationResult:
        """
        Validate a credit card number using the Luhn algorithm
        
        Args:
            card_number (str): Credit card number to validate
            
        Returns:
            ValidationResult: Validation result with details
        """
        if not card_number or not isinstance(card_number, str):
            return ValidationResult(
                False, 
                card_number, 
                "Credit card number must be a non-empty string"
            )
        
        # Remove spaces and dashes
        card_number = re.sub(r'[-\s]', '', card_number)
        
        if not card_number.isdigit():
            return ValidationResult(
                False, 
                card_number, 
                "Credit card number must contain only digits"
            )
        
        if len(card_number) < 13 or len(card_number) > 19:
            return ValidationResult(
                False, 
                card_number, 
                "Credit card number must be between 13 and 19 digits"
            )
        
        # Luhn algorithm
        def luhn_check(number: str) -> bool:
            digits = [int(d) for d in number]
            checksum = 0
            
            # Process digits from right to left
            for i in range(len(digits) - 1, -1, -1):
                digit = digits[i]
                
                # Double every second digit from the right
                if (len(digits) - i) % 2 == 0:
                    digit *= 2
                    if digit > 9:
                        digit -= 9
                
                checksum += digit
            
            return checksum % 10 == 0
        
        if not luhn_check(card_number):
            return ValidationResult(
                False, 
                card_number, 
                "Invalid credit card number (failed Luhn check)"
            )
        
        # Identify card type
        card_type = "Unknown"
        if card_number.startswith('4'):
            card_type = "Visa"
        elif card_number.startswith(('51', '52', '53', '54', '55')):
            card_type = "Mastercard"
        elif card_number.startswith(('34', '37')):
            card_type = "American Express"
        elif card_number.startswith('6011') or card_number.startswith(('644', '645', '646', '647', '648', '649', '65')):
            card_type = "Discover"
        
        return ValidationResult(
            True, 
            card_number, 
            "",
            {
                "card_type": card_type,
                "length": len(card_number),
                "masked": f"{'*' * (len(card_number) - 4)}{card_number[-4:]}"
            }
        )
    
    @staticmethod
    def validate_ip_address(ip: str, version: Optional[int] = None) -> ValidationResult:
        """
        Validate an IP address (IPv4 or IPv6)
        
        Args:
            ip (str): IP address to validate
            version (int, optional): IP version to validate (4 or 6)
            
        Returns:
            ValidationResult: Validation result with details
        """
        if not ip or not isinstance(ip, str):
            return ValidationResult(
                False, 
                ip, 
                "IP address must be a non-empty string"
            )
        
        ip = ip.strip()
        
        try:
            # Try to parse as IP address
            ip_obj = ipaddress.ip_address(ip)
            
            # Check version if specified
            if version:
                if version not in [4, 6]:
                    return ValidationResult(
                        False, 
                        ip, 
                        "IP version must be 4 or 6"
                    )
                
                if ip_obj.version != version:
                    return ValidationResult(
                        False, 
                        ip, 
                        f"Expected IPv{version} but got IPv{ip_obj.version}"
                    )
            
            return ValidationResult(
                True, 
                ip, 
                "",
                {
                    "version": ip_obj.version,
                    "is_private": ip_obj.is_private,
                    "is_loopback": ip_obj.is_loopback,
                    "is_multicast": ip_obj.is_multicast,
                    "compressed": str(ip_obj)
                }
            )
            
        except ValueError as e:
            return ValidationResult(
                False, 
                ip, 
                f"Invalid IP address: {str(e)}"
            )


def main():
    """
    Demo function showing usage examples
    """
    print("=" * 60)
    print("🔍 DATA VALIDATOR - DEMO")
    print("=" * 60)
    
    validator = DataValidator()
    
    # Email validation
    print("\n📧 EMAIL VALIDATION:")
    emails = ["user@example.com", "invalid.email", "test@domain.co.uk"]
    for email in emails:
        result = validator.validate_email(email)
        print(f"  {email}: {result}")
    
    # Phone validation
    print("\n📱 PHONE VALIDATION:")
    phones = ["+1-555-123-4567", "123", "+44 20 7946 0958"]
    for phone in phones:
        result = validator.validate_phone(phone)
        print(f"  {phone}: {result}")
    
    # URL validation
    print("\n🌐 URL VALIDATION:")
    urls = ["https://www.example.com", "invalid-url", "http://localhost:8080"]
    for url in urls:
        result = validator.validate_url(url)
        print(f"  {url}: {result}")
    
    # Date validation
    print("\n📅 DATE VALIDATION:")
    dates = ["2024-12-31", "31/12/2024", "invalid-date"]
    for date in dates:
        result = validator.validate_date(date)
        print(f"  {date}: {result}")
    
    # Credit card validation
    print("\n💳 CREDIT CARD VALIDATION:")
    cards = ["4532015112830366", "1234567890123456"]
    for card in cards:
        result = validator.validate_credit_card(card)
        print(f"  {card}: {result}")
    
    # IP address validation
    print("\n🌍 IP ADDRESS VALIDATION:")
    ips = ["192.168.1.1", "2001:0db8:85a3:0000:0000:8a2e:0370:7334", "invalid.ip"]
    for ip in ips:
        result = validator.validate_ip_address(ip)
        print(f"  {ip}: {result}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
