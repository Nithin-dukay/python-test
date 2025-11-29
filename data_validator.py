"""
Data Validator Utility

A comprehensive data validation library for Python that provides schema-based
validation, type checking, and custom validators for common data formats.

Example:
    from data_validator import Validator, Schema
    
    schema = Schema({
        'name': Validator().required().string().min_length(2),
        'email': Validator().required().email(),
        'age': Validator().required().integer().min_value(0).max_value(150)
    })
    
    result = schema.validate({'name': 'John', 'email': 'john@example.com', 'age': 30})
"""

import re
from typing import Any, Callable, Dict, List, Optional, Union
from datetime import datetime


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class Validator:
    """
    A chainable validator class that allows building complex validation rules.
    """
    
    def __init__(self):
        self.rules: List[Callable] = []
        self.field_name: Optional[str] = None
        self.is_required: bool = False
        self.allow_none: bool = False
    
    def set_field_name(self, name: str) -> 'Validator':
        """Set the field name for better error messages"""
        self.field_name = name
        return self
    
    def required(self) -> 'Validator':
        """Mark field as required"""
        self.is_required = True
        return self
    
    def optional(self) -> 'Validator':
        """Mark field as optional (allows None)"""
        self.allow_none = True
        return self
    
    def string(self) -> 'Validator':
        """Validate that value is a string"""
        def validate(value):
            if not isinstance(value, str):
                raise ValidationError(f"{self._field_prefix()}must be a string, got {type(value).__name__}")
        self.rules.append(validate)
        return self
    
    def integer(self) -> 'Validator':
        """Validate that value is an integer"""
        def validate(value):
            if not isinstance(value, int) or isinstance(value, bool):
                raise ValidationError(f"{self._field_prefix()}must be an integer, got {type(value).__name__}")
        self.rules.append(validate)
        return self
    
    def float_type(self) -> 'Validator':
        """Validate that value is a float"""
        def validate(value):
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ValidationError(f"{self._field_prefix()}must be a float, got {type(value).__name__}")
        self.rules.append(validate)
        return self
    
    def boolean(self) -> 'Validator':
        """Validate that value is a boolean"""
        def validate(value):
            if not isinstance(value, bool):
                raise ValidationError(f"{self._field_prefix()}must be a boolean, got {type(value).__name__}")
        self.rules.append(validate)
        return self
    
    def list_type(self) -> 'Validator':
        """Validate that value is a list"""
        def validate(value):
            if not isinstance(value, list):
                raise ValidationError(f"{self._field_prefix()}must be a list, got {type(value).__name__}")
        self.rules.append(validate)
        return self
    
    def dict_type(self) -> 'Validator':
        """Validate that value is a dictionary"""
        def validate(value):
            if not isinstance(value, dict):
                raise ValidationError(f"{self._field_prefix()}must be a dictionary, got {type(value).__name__}")
        self.rules.append(validate)
        return self
    
    def min_length(self, length: int) -> 'Validator':
        """Validate minimum length for strings or lists"""
        def validate(value):
            if len(value) < length:
                raise ValidationError(f"{self._field_prefix()}must have at least {length} characters/items")
        self.rules.append(validate)
        return self
    
    def max_length(self, length: int) -> 'Validator':
        """Validate maximum length for strings or lists"""
        def validate(value):
            if len(value) > length:
                raise ValidationError(f"{self._field_prefix()}must have at most {length} characters/items")
        self.rules.append(validate)
        return self
    
    def min_value(self, min_val: Union[int, float]) -> 'Validator':
        """Validate minimum value for numbers"""
        def validate(value):
            if value < min_val:
                raise ValidationError(f"{self._field_prefix()}must be at least {min_val}")
        self.rules.append(validate)
        return self
    
    def max_value(self, max_val: Union[int, float]) -> 'Validator':
        """Validate maximum value for numbers"""
        def validate(value):
            if value > max_val:
                raise ValidationError(f"{self._field_prefix()}must be at most {max_val}")
        self.rules.append(validate)
        return self
    
    def email(self) -> 'Validator':
        """Validate email format"""
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        
        def validate(value):
            if not isinstance(value, str):
                raise ValidationError(f"{self._field_prefix()}must be a string")
            if not email_pattern.match(value):
                raise ValidationError(f"{self._field_prefix()}must be a valid email address")
        self.rules.append(validate)
        return self
    
    def url(self) -> 'Validator':
        """Validate URL format"""
        url_pattern = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        
        def validate(value):
            if not isinstance(value, str):
                raise ValidationError(f"{self._field_prefix()}must be a string")
            if not url_pattern.match(value):
                raise ValidationError(f"{self._field_prefix()}must be a valid URL")
        self.rules.append(validate)
        return self
    
    def regex(self, pattern: str) -> 'Validator':
        """Validate against a custom regex pattern"""
        compiled_pattern = re.compile(pattern)
        
        def validate(value):
            if not isinstance(value, str):
                raise ValidationError(f"{self._field_prefix()}must be a string")
            if not compiled_pattern.match(value):
                raise ValidationError(f"{self._field_prefix()}does not match required pattern")
        self.rules.append(validate)
        return self
    
    def date_format(self, format_str: str = '%Y-%m-%d') -> 'Validator':
        """Validate date string format"""
        def validate(value):
            if not isinstance(value, str):
                raise ValidationError(f"{self._field_prefix()}must be a string")
            try:
                datetime.strptime(value, format_str)
            except ValueError:
                raise ValidationError(f"{self._field_prefix()}must be a valid date in format {format_str}")
        self.rules.append(validate)
        return self
    
    def one_of(self, allowed_values: List[Any]) -> 'Validator':
        """Validate that value is one of the allowed values"""
        def validate(value):
            if value not in allowed_values:
                raise ValidationError(f"{self._field_prefix()}must be one of {allowed_values}")
        self.rules.append(validate)
        return self
    
    def custom(self, validator_func: Callable[[Any], bool], error_message: str = "validation failed") -> 'Validator':
        """Add a custom validation function"""
        def validate(value):
            if not validator_func(value):
                raise ValidationError(f"{self._field_prefix()}{error_message}")
        self.rules.append(validate)
        return self
    
    def validate(self, value: Any) -> bool:
        """
        Run all validation rules on the value.
        
        Args:
            value: The value to validate
            
        Returns:
            True if validation passes
            
        Raises:
            ValidationError: If validation fails
        """
        if value is None:
            if self.is_required:
                raise ValidationError(f"{self._field_prefix()}is required")
            if self.allow_none:
                return True
            if not self.rules:
                return True
        
        for rule in self.rules:
            rule(value)
        
        return True
    
    def _field_prefix(self) -> str:
        """Get field name prefix for error messages"""
        return f"Field '{self.field_name}' " if self.field_name else ""


class Schema:
    """
    Schema validator for dictionaries/JSON data.
    
    Example:
        schema = Schema({
            'name': Validator().required().string(),
            'age': Validator().required().integer().min_value(0)
        })
        
        schema.validate({'name': 'John', 'age': 30})
    """
    
    def __init__(self, schema: Dict[str, Validator]):
        self.schema = schema
        for field_name, validator in schema.items():
            validator.set_field_name(field_name)
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data against the schema.
        
        Args:
            data: Dictionary to validate
            
        Returns:
            The validated data
            
        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(data, dict):
            raise ValidationError("Data must be a dictionary")
        
        errors = []
        
        for field_name, validator in self.schema.items():
            try:
                value = data.get(field_name)
                validator.validate(value)
            except ValidationError as e:
                errors.append(str(e))
        
        if errors:
            raise ValidationError("; ".join(errors))
        
        return data
    
    def validate_many(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate multiple data items against the schema.
        
        Args:
            data_list: List of dictionaries to validate
            
        Returns:
            List of validated data
            
        Raises:
            ValidationError: If any validation fails
        """
        if not isinstance(data_list, list):
            raise ValidationError("Data must be a list")
        
        validated = []
        errors = []
        
        for idx, item in enumerate(data_list):
            try:
                validated.append(self.validate(item))
            except ValidationError as e:
                errors.append(f"Item {idx}: {str(e)}")
        
        if errors:
            raise ValidationError("; ".join(errors))
        
        return validated


def validate_value(value: Any, validator: Validator) -> bool:
    """
    Convenience function to validate a single value.
    
    Args:
        value: The value to validate
        validator: The validator to use
        
    Returns:
        True if validation passes
        
    Raises:
        ValidationError: If validation fails
    """
    return validator.validate(value)
