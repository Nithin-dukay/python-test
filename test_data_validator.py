"""
Comprehensive tests for the data_validator module.
"""

import pytest
from data_validator import Validator, Schema, ValidationError, validate_value


class TestValidator:
    """Test cases for the Validator class"""
    
    def test_required_field_missing(self):
        """Test that required fields raise error when None"""
        validator = Validator().required().string()
        with pytest.raises(ValidationError, match="is required"):
            validator.validate(None)
    
    def test_optional_field_allows_none(self):
        """Test that optional fields allow None"""
        validator = Validator().optional().string()
        assert validator.validate(None) is True
    
    def test_string_validation_success(self):
        """Test successful string validation"""
        validator = Validator().string()
        assert validator.validate("hello") is True
    
    def test_string_validation_failure(self):
        """Test string validation with non-string"""
        validator = Validator().string()
        with pytest.raises(ValidationError, match="must be a string"):
            validator.validate(123)
    
    def test_integer_validation_success(self):
        """Test successful integer validation"""
        validator = Validator().integer()
        assert validator.validate(42) is True
    
    def test_integer_validation_failure(self):
        """Test integer validation with non-integer"""
        validator = Validator().integer()
        with pytest.raises(ValidationError, match="must be an integer"):
            validator.validate("42")
    
    def test_integer_validation_rejects_boolean(self):
        """Test that integer validation rejects booleans"""
        validator = Validator().integer()
        with pytest.raises(ValidationError, match="must be an integer"):
            validator.validate(True)
    
    def test_float_validation_success(self):
        """Test successful float validation"""
        validator = Validator().float_type()
        assert validator.validate(3.14) is True
        assert validator.validate(42) is True
    
    def test_float_validation_failure(self):
        """Test float validation with non-numeric"""
        validator = Validator().float_type()
        with pytest.raises(ValidationError, match="must be a float"):
            validator.validate("3.14")
    
    def test_boolean_validation_success(self):
        """Test successful boolean validation"""
        validator = Validator().boolean()
        assert validator.validate(True) is True
        assert validator.validate(False) is True
    
    def test_boolean_validation_failure(self):
        """Test boolean validation with non-boolean"""
        validator = Validator().boolean()
        with pytest.raises(ValidationError, match="must be a boolean"):
            validator.validate(1)
    
    def test_list_validation_success(self):
        """Test successful list validation"""
        validator = Validator().list_type()
        assert validator.validate([1, 2, 3]) is True
    
    def test_list_validation_failure(self):
        """Test list validation with non-list"""
        validator = Validator().list_type()
        with pytest.raises(ValidationError, match="must be a list"):
            validator.validate((1, 2, 3))
    
    def test_dict_validation_success(self):
        """Test successful dictionary validation"""
        validator = Validator().dict_type()
        assert validator.validate({"key": "value"}) is True
    
    def test_dict_validation_failure(self):
        """Test dictionary validation with non-dict"""
        validator = Validator().dict_type()
        with pytest.raises(ValidationError, match="must be a dictionary"):
            validator.validate([1, 2, 3])
    
    def test_min_length_string_success(self):
        """Test minimum length validation for strings"""
        validator = Validator().string().min_length(3)
        assert validator.validate("hello") is True
    
    def test_min_length_string_failure(self):
        """Test minimum length validation failure"""
        validator = Validator().string().min_length(5)
        with pytest.raises(ValidationError, match="must have at least 5"):
            validator.validate("hi")
    
    def test_max_length_string_success(self):
        """Test maximum length validation for strings"""
        validator = Validator().string().max_length(10)
        assert validator.validate("hello") is True
    
    def test_max_length_string_failure(self):
        """Test maximum length validation failure"""
        validator = Validator().string().max_length(3)
        with pytest.raises(ValidationError, match="must have at most 3"):
            validator.validate("hello")
    
    def test_min_length_list_success(self):
        """Test minimum length validation for lists"""
        validator = Validator().list_type().min_length(2)
        assert validator.validate([1, 2, 3]) is True
    
    def test_min_length_list_failure(self):
        """Test minimum length validation failure for lists"""
        validator = Validator().list_type().min_length(5)
        with pytest.raises(ValidationError, match="must have at least 5"):
            validator.validate([1, 2])
    
    def test_min_value_success(self):
        """Test minimum value validation"""
        validator = Validator().integer().min_value(0)
        assert validator.validate(10) is True
    
    def test_min_value_failure(self):
        """Test minimum value validation failure"""
        validator = Validator().integer().min_value(10)
        with pytest.raises(ValidationError, match="must be at least 10"):
            validator.validate(5)
    
    def test_max_value_success(self):
        """Test maximum value validation"""
        validator = Validator().integer().max_value(100)
        assert validator.validate(50) is True
    
    def test_max_value_failure(self):
        """Test maximum value validation failure"""
        validator = Validator().integer().max_value(10)
        with pytest.raises(ValidationError, match="must be at most 10"):
            validator.validate(20)
    
    def test_email_validation_success(self):
        """Test successful email validation"""
        validator = Validator().email()
        assert validator.validate("user@example.com") is True
        assert validator.validate("test.user+tag@domain.co.uk") is True
    
    def test_email_validation_failure(self):
        """Test email validation with invalid emails"""
        validator = Validator().email()
        with pytest.raises(ValidationError, match="must be a valid email"):
            validator.validate("invalid-email")
        with pytest.raises(ValidationError, match="must be a valid email"):
            validator.validate("@example.com")
        with pytest.raises(ValidationError, match="must be a valid email"):
            validator.validate("user@")
    
    def test_url_validation_success(self):
        """Test successful URL validation"""
        validator = Validator().url()
        assert validator.validate("http://example.com") is True
        assert validator.validate("https://www.example.com/path") is True
        assert validator.validate("http://localhost:8080") is True
    
    def test_url_validation_failure(self):
        """Test URL validation with invalid URLs"""
        validator = Validator().url()
        with pytest.raises(ValidationError, match="must be a valid URL"):
            validator.validate("not-a-url")
        with pytest.raises(ValidationError, match="must be a valid URL"):
            validator.validate("ftp://example.com")
    
    def test_regex_validation_success(self):
        """Test successful regex validation"""
        validator = Validator().regex(r'^\d{3}-\d{3}-\d{4}$')
        assert validator.validate("123-456-7890") is True
    
    def test_regex_validation_failure(self):
        """Test regex validation failure"""
        validator = Validator().regex(r'^\d{3}-\d{3}-\d{4}$')
        with pytest.raises(ValidationError, match="does not match required pattern"):
            validator.validate("123-456-789")
    
    def test_date_format_validation_success(self):
        """Test successful date format validation"""
        validator = Validator().date_format('%Y-%m-%d')
        assert validator.validate("2023-12-25") is True
    
    def test_date_format_validation_failure(self):
        """Test date format validation failure"""
        validator = Validator().date_format('%Y-%m-%d')
        with pytest.raises(ValidationError, match="must be a valid date"):
            validator.validate("25-12-2023")
    
    def test_one_of_validation_success(self):
        """Test successful one_of validation"""
        validator = Validator().one_of(['red', 'green', 'blue'])
        assert validator.validate('red') is True
    
    def test_one_of_validation_failure(self):
        """Test one_of validation failure"""
        validator = Validator().one_of(['red', 'green', 'blue'])
        with pytest.raises(ValidationError, match="must be one of"):
            validator.validate('yellow')
    
    def test_custom_validation_success(self):
        """Test successful custom validation"""
        validator = Validator().custom(lambda x: x > 0, "must be positive")
        assert validator.validate(5) is True
    
    def test_custom_validation_failure(self):
        """Test custom validation failure"""
        validator = Validator().custom(lambda x: x > 0, "must be positive")
        with pytest.raises(ValidationError, match="must be positive"):
            validator.validate(-5)
    
    def test_chained_validations(self):
        """Test multiple chained validations"""
        validator = Validator().required().string().min_length(3).max_length(10)
        assert validator.validate("hello") is True
        
        with pytest.raises(ValidationError):
            validator.validate("hi")
        
        with pytest.raises(ValidationError):
            validator.validate("this is too long")
    
    def test_field_name_in_error_message(self):
        """Test that field name appears in error messages"""
        validator = Validator().set_field_name("username").required().string()
        with pytest.raises(ValidationError, match="Field 'username'"):
            validator.validate(None)


class TestSchema:
    """Test cases for the Schema class"""
    
    def test_schema_validation_success(self):
        """Test successful schema validation"""
        schema = Schema({
            'name': Validator().required().string(),
            'age': Validator().required().integer().min_value(0)
        })
        
        data = {'name': 'John', 'age': 30}
        assert schema.validate(data) == data
    
    def test_schema_validation_failure(self):
        """Test schema validation with invalid data"""
        schema = Schema({
            'name': Validator().required().string(),
            'age': Validator().required().integer()
        })
        
        with pytest.raises(ValidationError):
            schema.validate({'name': 'John', 'age': 'thirty'})
    
    def test_schema_missing_required_field(self):
        """Test schema validation with missing required field"""
        schema = Schema({
            'name': Validator().required().string(),
            'email': Validator().required().email()
        })
        
        with pytest.raises(ValidationError, match="is required"):
            schema.validate({'name': 'John'})
    
    def test_schema_optional_field(self):
        """Test schema with optional fields"""
        schema = Schema({
            'name': Validator().required().string(),
            'nickname': Validator().optional().string()
        })
        
        data = {'name': 'John'}
        assert schema.validate(data) == data
    
    def test_schema_complex_validation(self):
        """Test schema with complex validation rules"""
        schema = Schema({
            'username': Validator().required().string().min_length(3).max_length(20),
            'email': Validator().required().email(),
            'age': Validator().required().integer().min_value(18).max_value(120),
            'website': Validator().optional().url()
        })
        
        data = {
            'username': 'johndoe',
            'email': 'john@example.com',
            'age': 25,
            'website': 'https://johndoe.com'
        }
        assert schema.validate(data) == data
    
    def test_schema_multiple_errors(self):
        """Test that schema collects multiple validation errors"""
        schema = Schema({
            'name': Validator().required().string(),
            'age': Validator().required().integer()
        })
        
        with pytest.raises(ValidationError) as exc_info:
            schema.validate({'name': 123, 'age': 'thirty'})
        
        error_message = str(exc_info.value)
        assert 'name' in error_message
        assert 'age' in error_message
    
    def test_schema_validate_many_success(self):
        """Test validating multiple items successfully"""
        schema = Schema({
            'name': Validator().required().string(),
            'age': Validator().required().integer()
        })
        
        data_list = [
            {'name': 'John', 'age': 30},
            {'name': 'Jane', 'age': 25}
        ]
        
        result = schema.validate_many(data_list)
        assert result == data_list
    
    def test_schema_validate_many_failure(self):
        """Test validating multiple items with errors"""
        schema = Schema({
            'name': Validator().required().string(),
            'age': Validator().required().integer()
        })
        
        data_list = [
            {'name': 'John', 'age': 30},
            {'name': 'Jane', 'age': 'twenty-five'}
        ]
        
        with pytest.raises(ValidationError, match="Item 1"):
            schema.validate_many(data_list)
    
    def test_schema_non_dict_input(self):
        """Test schema validation with non-dictionary input"""
        schema = Schema({
            'name': Validator().required().string()
        })
        
        with pytest.raises(ValidationError, match="must be a dictionary"):
            schema.validate("not a dict")
    
    def test_schema_validate_many_non_list_input(self):
        """Test validate_many with non-list input"""
        schema = Schema({
            'name': Validator().required().string()
        })
        
        with pytest.raises(ValidationError, match="must be a list"):
            schema.validate_many({'name': 'John'})


class TestValidateValue:
    """Test cases for the validate_value convenience function"""
    
    def test_validate_value_success(self):
        """Test validate_value with valid data"""
        validator = Validator().string().min_length(3)
        assert validate_value("hello", validator) is True
    
    def test_validate_value_failure(self):
        """Test validate_value with invalid data"""
        validator = Validator().string().min_length(5)
        with pytest.raises(ValidationError):
            validate_value("hi", validator)


class TestEdgeCases:
    """Test edge cases and special scenarios"""
    
    def test_empty_string_validation(self):
        """Test validation with empty string"""
        validator = Validator().string()
        assert validator.validate("") is True
    
    def test_empty_list_validation(self):
        """Test validation with empty list"""
        validator = Validator().list_type()
        assert validator.validate([]) is True
    
    def test_empty_dict_validation(self):
        """Test validation with empty dictionary"""
        validator = Validator().dict_type()
        assert validator.validate({}) is True
    
    def test_zero_value_validation(self):
        """Test validation with zero"""
        validator = Validator().integer().min_value(0)
        assert validator.validate(0) is True
    
    def test_negative_number_validation(self):
        """Test validation with negative numbers"""
        validator = Validator().integer().min_value(-100).max_value(-1)
        assert validator.validate(-50) is True
    
    def test_unicode_string_validation(self):
        """Test validation with unicode strings"""
        validator = Validator().string().min_length(2)
        assert validator.validate("你好") is True
    
    def test_special_characters_in_email(self):
        """Test email validation with special characters"""
        validator = Validator().email()
        assert validator.validate("user+tag@example.com") is True
        assert validator.validate("user.name@example.com") is True
    
    def test_localhost_url_validation(self):
        """Test URL validation with localhost"""
        validator = Validator().url()
        assert validator.validate("http://localhost") is True
        assert validator.validate("http://localhost:3000") is True
    
    def test_ip_address_url_validation(self):
        """Test URL validation with IP addresses"""
        validator = Validator().url()
        assert validator.validate("http://192.168.1.1") is True
        assert validator.validate("http://127.0.0.1:8080") is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
