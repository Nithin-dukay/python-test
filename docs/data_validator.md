# Data Validator Documentation

A comprehensive data validation library for Python that provides schema-based validation, type checking, and custom validators for common data formats.

## Features

- **Type Validation**: String, integer, float, boolean, list, and dictionary types
- **Length Validation**: Min/max length for strings and lists
- **Range Validation**: Min/max values for numbers
- **Format Validation**: Email, URL, date formats, and custom regex patterns
- **Schema Validation**: Validate complex nested data structures
- **Chainable API**: Build complex validation rules with a fluent interface
- **Clear Error Messages**: Descriptive error messages with field names
- **Custom Validators**: Add your own validation logic

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Validation

```python
from data_validator import Validator, ValidationError

# Simple string validation
validator = Validator().string().min_length(3)
validator.validate("hello")  # Returns True

# Integer with range validation
validator = Validator().integer().min_value(0).max_value(100)
validator.validate(50)  # Returns True
```

### Schema Validation

```python
from data_validator import Schema, Validator

# Define a schema
user_schema = Schema({
    'username': Validator().required().string().min_length(3).max_length(20),
    'email': Validator().required().email(),
    'age': Validator().required().integer().min_value(18).max_value(120),
    'website': Validator().optional().url()
})

# Validate data
user_data = {
    'username': 'johndoe',
    'email': 'john@example.com',
    'age': 25,
    'website': 'https://johndoe.com'
}

validated_data = user_schema.validate(user_data)
```

## API Reference

### Validator Class

The `Validator` class provides a chainable interface for building validation rules.

#### Field Requirements

- **`required()`**: Mark field as required (cannot be None)
- **`optional()`**: Mark field as optional (allows None)

```python
# Required field
Validator().required().string()

# Optional field
Validator().optional().email()
```

#### Type Validators

- **`string()`**: Validate that value is a string
- **`integer()`**: Validate that value is an integer
- **`float_type()`**: Validate that value is a float or int
- **`boolean()`**: Validate that value is a boolean
- **`list_type()`**: Validate that value is a list
- **`dict_type()`**: Validate that value is a dictionary

```python
# Type validation examples
Validator().string().validate("hello")
Validator().integer().validate(42)
Validator().boolean().validate(True)
Validator().list_type().validate([1, 2, 3])
```

#### Length Validators

- **`min_length(length: int)`**: Minimum length for strings or lists
- **`max_length(length: int)`**: Maximum length for strings or lists

```python
# String length validation
Validator().string().min_length(3).max_length(50)

# List length validation
Validator().list_type().min_length(1).max_length(10)
```

#### Range Validators

- **`min_value(min_val: Union[int, float])`**: Minimum value for numbers
- **`max_value(max_val: Union[int, float])`**: Maximum value for numbers

```python
# Age validation
Validator().integer().min_value(0).max_value(150)

# Price validation
Validator().float_type().min_value(0.01).max_value(9999.99)
```

#### Format Validators

- **`email()`**: Validate email format
- **`url()`**: Validate URL format (http/https)
- **`date_format(format_str: str)`**: Validate date string format
- **`regex(pattern: str)`**: Validate against custom regex pattern

```python
# Email validation
Validator().email().validate("user@example.com")

# URL validation
Validator().url().validate("https://example.com")

# Date validation
Validator().date_format('%Y-%m-%d').validate("2023-12-25")

# Phone number validation
Validator().regex(r'^\d{3}-\d{3}-\d{4}$').validate("123-456-7890")
```

#### Choice Validators

- **`one_of(allowed_values: List[Any])`**: Validate that value is one of allowed values

```python
# Status validation
Validator().one_of(['active', 'inactive', 'pending'])
```

#### Custom Validators

- **`custom(validator_func: Callable, error_message: str)`**: Add custom validation logic

```python
# Custom validation
def is_even(x):
    return x % 2 == 0

Validator().integer().custom(is_even, "must be an even number")
```

### Schema Class

The `Schema` class validates dictionaries against a defined schema.

#### Methods

- **`validate(data: Dict[str, Any])`**: Validate a single dictionary
- **`validate_many(data_list: List[Dict[str, Any]])`**: Validate multiple dictionaries

```python
# Define schema
schema = Schema({
    'name': Validator().required().string(),
    'age': Validator().required().integer()
})

# Validate single item
schema.validate({'name': 'John', 'age': 30})

# Validate multiple items
schema.validate_many([
    {'name': 'John', 'age': 30},
    {'name': 'Jane', 'age': 25}
])
```

### ValidationError

Custom exception raised when validation fails. Contains descriptive error messages.

```python
from data_validator import ValidationError

try:
    validator = Validator().required().email()
    validator.validate("invalid-email")
except ValidationError as e:
    print(f"Validation failed: {e}")
```

## Usage Examples

### User Registration Validation

```python
from data_validator import Schema, Validator

registration_schema = Schema({
    'username': Validator().required().string().min_length(3).max_length(20),
    'email': Validator().required().email(),
    'password': Validator().required().string().min_length(8),
    'age': Validator().required().integer().min_value(13),
    'terms_accepted': Validator().required().boolean()
})

# Validate registration data
try:
    user_data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'securepass123',
        'age': 25,
        'terms_accepted': True
    }
    validated = registration_schema.validate(user_data)
    print("Registration data is valid!")
except ValidationError as e:
    print(f"Validation error: {e}")
```

### API Request Validation

```python
from data_validator import Schema, Validator

api_request_schema = Schema({
    'endpoint': Validator().required().url(),
    'method': Validator().required().one_of(['GET', 'POST', 'PUT', 'DELETE']),
    'headers': Validator().optional().dict_type(),
    'timeout': Validator().optional().integer().min_value(1).max_value(300)
})

# Validate API request
request_data = {
    'endpoint': 'https://api.example.com/users',
    'method': 'POST',
    'headers': {'Content-Type': 'application/json'},
    'timeout': 30
}

validated = api_request_schema.validate(request_data)
```

### Product Data Validation

```python
from data_validator import Schema, Validator

product_schema = Schema({
    'sku': Validator().required().regex(r'^[A-Z]{3}-\d{6}$'),
    'name': Validator().required().string().min_length(1).max_length(100),
    'price': Validator().required().float_type().min_value(0.01),
    'quantity': Validator().required().integer().min_value(0),
    'categories': Validator().required().list_type().min_length(1),
    'description': Validator().optional().string().max_length(500)
})

# Validate product data
product = {
    'sku': 'ABC-123456',
    'name': 'Widget',
    'price': 29.99,
    'quantity': 100,
    'categories': ['electronics', 'gadgets']
}

validated = product_schema.validate(product)
```

### Bulk Data Validation

```python
from data_validator import Schema, Validator

contact_schema = Schema({
    'name': Validator().required().string(),
    'email': Validator().required().email(),
    'phone': Validator().optional().regex(r'^\d{3}-\d{3}-\d{4}$')
})

# Validate multiple contacts
contacts = [
    {'name': 'John Doe', 'email': 'john@example.com', 'phone': '123-456-7890'},
    {'name': 'Jane Smith', 'email': 'jane@example.com'},
    {'name': 'Bob Johnson', 'email': 'bob@example.com', 'phone': '987-654-3210'}
]

try:
    validated_contacts = contact_schema.validate_many(contacts)
    print(f"All {len(validated_contacts)} contacts are valid!")
except ValidationError as e:
    print(f"Validation error: {e}")
```

## Error Handling

The library provides clear, descriptive error messages:

```python
from data_validator import Validator, ValidationError

validator = Validator().set_field_name('age').required().integer().min_value(18)

try:
    validator.validate(15)
except ValidationError as e:
    print(e)  # Output: Field 'age' must be at least 18
```

Multiple errors in schema validation are combined:

```python
schema = Schema({
    'name': Validator().required().string(),
    'age': Validator().required().integer()
})

try:
    schema.validate({'name': 123, 'age': 'thirty'})
except ValidationError as e:
    print(e)  # Output: Field 'name' must be a string; Field 'age' must be an integer
```

## Best Practices

1. **Define schemas once**: Create schema objects once and reuse them
2. **Use descriptive field names**: Field names appear in error messages
3. **Chain validators logically**: Order validators from general to specific
4. **Handle ValidationError**: Always catch and handle validation errors appropriately
5. **Use optional() for nullable fields**: Explicitly mark fields that can be None
6. **Combine with type hints**: Use Python type hints alongside validators for better IDE support

## Testing

Run the test suite:

```bash
pytest test_data_validator.py -v
```

Run with coverage:

```bash
pytest test_data_validator.py --cov=data_validator --cov-report=html
```

## License

This project is part of the python-test repository.
