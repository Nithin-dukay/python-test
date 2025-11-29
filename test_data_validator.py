#!/usr/bin/env python3
"""
Unit Tests for Data Validator Module
Comprehensive test suite for all validation functions
"""

import pytest
from data_validator import DataValidator, ValidationResult, ValidationError


class TestEmailValidation:
    """Test cases for email validation"""
    
    def test_valid_emails(self):
        """Test valid email addresses"""
        valid_emails = [
            "user@example.com",
            "test.user@example.com",
            "user+tag@example.co.uk",
            "user_name@example-domain.com",
            "123@example.com",
            "a@b.co",
        ]
        
        for email in valid_emails:
            result = DataValidator.validate_email(email)
            assert result.is_valid, f"Expected {email} to be valid"
            assert result.value == email
            assert result.error_message == ""
    
    def test_invalid_emails(self):
        """Test invalid email addresses"""
        invalid_emails = [
            "invalid.email",
            "@example.com",
            "user@",
            "user @example.com",
            "user@example",
            "",
            "user..name@example.com",
            "a" * 65 + "@example.com",  # Local part too long
        ]
        
        for email in invalid_emails:
            result = DataValidator.validate_email(email)
            assert not result.is_valid, f"Expected {email} to be invalid"
            assert result.error_message != ""
    
    def test_email_edge_cases(self):
        """Test edge cases for email validation"""
        # None input
        result = DataValidator.validate_email(None)
        assert not result.is_valid
        
        # Non-string input
        result = DataValidator.validate_email(123)
        assert not result.is_valid
        
        # Email too long
        long_email = "a" * 250 + "@example.com"
        result = DataValidator.validate_email(long_email)
        assert not result.is_valid
    
    def test_email_metadata(self):
        """Test email validation metadata"""
        result = DataValidator.validate_email("user@example.com")
        assert result.is_valid
        assert "local_part" in result.metadata
        assert "domain" in result.metadata
        assert result.metadata["local_part"] == "user"
        assert result.metadata["domain"] == "example.com"


class TestPhoneValidation:
    """Test cases for phone number validation"""
    
    def test_valid_phones(self):
        """Test valid phone numbers"""
        valid_phones = [
            "+1-555-123-4567",
            "+44 20 7946 0958",
            "+91 98765 43210",
            "1234567",
            "+1 (555) 123-4567",
            "555-123-4567",
        ]
        
        for phone in valid_phones:
            result = DataValidator.validate_phone(phone)
            assert result.is_valid, f"Expected {phone} to be valid"
            assert result.value == phone
    
    def test_invalid_phones(self):
        """Test invalid phone numbers"""
        invalid_phones = [
            "123",  # Too short
            "12345678901234567",  # Too long
            "abc-def-ghij",
            "",
            "+++123456789",
        ]
        
        for phone in invalid_phones:
            result = DataValidator.validate_phone(phone)
            assert not result.is_valid, f"Expected {phone} to be invalid"
    
    def test_phone_country_code(self):
        """Test phone validation with country code"""
        result = DataValidator.validate_phone("+1-555-123-4567", country_code="+1")
        assert result.is_valid
        
        result = DataValidator.validate_phone("555-123-4567", country_code="+1")
        assert not result.is_valid
    
    def test_phone_metadata(self):
        """Test phone validation metadata"""
        result = DataValidator.validate_phone("+1-555-123-4567")
        assert result.is_valid
        assert "digits" in result.metadata
        assert "length" in result.metadata
        assert result.metadata["digits"] == "15551234567"


class TestURLValidation:
    """Test cases for URL validation"""
    
    def test_valid_urls(self):
        """Test valid URLs"""
        valid_urls = [
            "https://www.example.com",
            "http://example.com",
            "https://example.com/path/to/page",
            "http://localhost:8080",
            "https://sub.domain.example.com",
            "ftp://files.example.com",
        ]
        
        for url in valid_urls:
            result = DataValidator.validate_url(url)
            assert result.is_valid, f"Expected {url} to be valid"
    
    def test_invalid_urls(self):
        """Test invalid URLs"""
        invalid_urls = [
            "invalid-url",
            "www.example.com",  # Missing protocol
            "http://",
            "",
            "javascript:alert('xss')",
        ]
        
        for url in invalid_urls:
            result = DataValidator.validate_url(url)
            assert not result.is_valid, f"Expected {url} to be invalid"
    
    def test_url_https_requirement(self):
        """Test URL HTTPS requirement"""
        result = DataValidator.validate_url("http://example.com", require_https=True)
        assert not result.is_valid
        
        result = DataValidator.validate_url("https://example.com", require_https=True)
        assert result.is_valid
    
    def test_url_metadata(self):
        """Test URL validation metadata"""
        result = DataValidator.validate_url("https://www.example.com/path")
        assert result.is_valid
        assert result.metadata["scheme"] == "https"
        assert result.metadata["domain"] == "www.example.com"
        assert result.metadata["path"] == "/path"
        assert result.metadata["is_secure"] is True


class TestDateValidation:
    """Test cases for date validation"""
    
    def test_valid_dates(self):
        """Test valid date strings"""
        valid_dates = [
            "2024-12-31",
            "31/12/2024",
            "12/31/2024",
            "2024/12/31",
            "31-12-2024",
            "December 31, 2024",
            "31 December 2024",
        ]
        
        for date in valid_dates:
            result = DataValidator.validate_date(date)
            assert result.is_valid, f"Expected {date} to be valid"
    
    def test_invalid_dates(self):
        """Test invalid date strings"""
        invalid_dates = [
            "invalid-date",
            "32/13/2024",  # Invalid day/month
            "2024-13-01",  # Invalid month
            "",
            "not a date",
        ]
        
        for date in invalid_dates:
            result = DataValidator.validate_date(date)
            assert not result.is_valid, f"Expected {date} to be invalid"
    
    def test_date_with_format(self):
        """Test date validation with specific format"""
        result = DataValidator.validate_date("2024-12-31", date_format="%Y-%m-%d")
        assert result.is_valid
        
        result = DataValidator.validate_date("31/12/2024", date_format="%Y-%m-%d")
        assert not result.is_valid
    
    def test_date_metadata(self):
        """Test date validation metadata"""
        result = DataValidator.validate_date("2024-12-31")
        assert result.is_valid
        assert "parsed_date" in result.metadata
        assert "format" in result.metadata
        assert "iso_format" in result.metadata


class TestCreditCardValidation:
    """Test cases for credit card validation"""
    
    def test_valid_credit_cards(self):
        """Test valid credit card numbers"""
        valid_cards = [
            "4532015112830366",  # Visa
            "5425233430109903",  # Mastercard
            "374245455400126",   # American Express
            "6011111111111117",  # Discover
            "4532-0151-1283-0366",  # With dashes
            "4532 0151 1283 0366",  # With spaces
        ]
        
        for card in valid_cards:
            result = DataValidator.validate_credit_card(card)
            assert result.is_valid, f"Expected {card} to be valid"
    
    def test_invalid_credit_cards(self):
        """Test invalid credit card numbers"""
        invalid_cards = [
            "1234567890123456",  # Invalid Luhn
            "123",  # Too short
            "12345678901234567890",  # Too long
            "abcd-efgh-ijkl-mnop",
            "",
        ]
        
        for card in invalid_cards:
            result = DataValidator.validate_credit_card(card)
            assert not result.is_valid, f"Expected {card} to be invalid"
    
    def test_credit_card_types(self):
        """Test credit card type detection"""
        # Visa
        result = DataValidator.validate_credit_card("4532015112830366")
        assert result.is_valid
        assert result.metadata["card_type"] == "Visa"
        
        # Mastercard
        result = DataValidator.validate_credit_card("5425233430109903")
        assert result.is_valid
        assert result.metadata["card_type"] == "Mastercard"
        
        # American Express
        result = DataValidator.validate_credit_card("374245455400126")
        assert result.is_valid
        assert result.metadata["card_type"] == "American Express"
    
    def test_credit_card_metadata(self):
        """Test credit card validation metadata"""
        result = DataValidator.validate_credit_card("4532015112830366")
        assert result.is_valid
        assert "card_type" in result.metadata
        assert "length" in result.metadata
        assert "masked" in result.metadata
        assert result.metadata["masked"].endswith("0366")


class TestIPAddressValidation:
    """Test cases for IP address validation"""
    
    def test_valid_ipv4(self):
        """Test valid IPv4 addresses"""
        valid_ips = [
            "192.168.1.1",
            "10.0.0.1",
            "172.16.0.1",
            "8.8.8.8",
            "127.0.0.1",
        ]
        
        for ip in valid_ips:
            result = DataValidator.validate_ip_address(ip)
            assert result.is_valid, f"Expected {ip} to be valid"
            assert result.metadata["version"] == 4
    
    def test_valid_ipv6(self):
        """Test valid IPv6 addresses"""
        valid_ips = [
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            "2001:db8:85a3::8a2e:370:7334",
            "::1",
            "fe80::1",
        ]
        
        for ip in valid_ips:
            result = DataValidator.validate_ip_address(ip)
            assert result.is_valid, f"Expected {ip} to be valid"
            assert result.metadata["version"] == 6
    
    def test_invalid_ips(self):
        """Test invalid IP addresses"""
        invalid_ips = [
            "256.256.256.256",
            "192.168.1",
            "invalid.ip",
            "",
            "gggg::1",
        ]
        
        for ip in invalid_ips:
            result = DataValidator.validate_ip_address(ip)
            assert not result.is_valid, f"Expected {ip} to be invalid"
    
    def test_ip_version_check(self):
        """Test IP version validation"""
        result = DataValidator.validate_ip_address("192.168.1.1", version=4)
        assert result.is_valid
        
        result = DataValidator.validate_ip_address("192.168.1.1", version=6)
        assert not result.is_valid
        
        result = DataValidator.validate_ip_address("::1", version=6)
        assert result.is_valid
    
    def test_ip_metadata(self):
        """Test IP address validation metadata"""
        result = DataValidator.validate_ip_address("192.168.1.1")
        assert result.is_valid
        assert "version" in result.metadata
        assert "is_private" in result.metadata
        assert "is_loopback" in result.metadata
        assert result.metadata["is_private"] is True


class TestValidationResult:
    """Test cases for ValidationResult class"""
    
    def test_validation_result_bool(self):
        """Test ValidationResult boolean conversion"""
        valid_result = ValidationResult(True, "test")
        assert bool(valid_result) is True
        
        invalid_result = ValidationResult(False, "test", "error")
        assert bool(invalid_result) is False
    
    def test_validation_result_repr(self):
        """Test ValidationResult string representation"""
        result = ValidationResult(True, "test")
        repr_str = repr(result)
        assert "✅ VALID" in repr_str
        
        result = ValidationResult(False, "test", "error")
        repr_str = repr(result)
        assert "❌ INVALID" in repr_str


def test_validator_instance():
    """Test DataValidator instantiation"""
    validator = DataValidator()
    assert validator is not None
    assert hasattr(validator, 'validate_email')
    assert hasattr(validator, 'validate_phone')
    assert hasattr(validator, 'validate_url')
    assert hasattr(validator, 'validate_date')
    assert hasattr(validator, 'validate_credit_card')
    assert hasattr(validator, 'validate_ip_address')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
