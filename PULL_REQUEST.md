# Pull Request: Add Data Validation Utility

## Overview
This PR introduces a comprehensive data validation utility for Python that provides schema-based validation, type checking, and custom validators for common data formats.

## Feature Description
The data validator is a production-ready library that enables robust validation of user input, API requests, configuration data, and complex data structures. It features a chainable, fluent API that makes building complex validation rules intuitive and maintainable.

## What's Added

### Core Components

1. **`data_validator.py`** - Main validation library
   - `Validator` class with chainable validation rules
   - `Schema` class for validating complex data structures
   - `ValidationError` exception for clear error reporting
   - Support for required/optional fields
   - Type validators (string, integer, float, boolean, list, dict)
   - Length validators (min/max for strings and lists)
   - Range validators (min/max for numbers)
   - Format validators (email, URL, date, regex)
   - Choice validators (one_of)
   - Custom validation functions

2. **`test_data_validator.py`** - Comprehensive test suite
   - 60 unit tests covering all functionality
   - Tests for success and failure cases
   - Edge case testing (empty values, unicode, special characters)
   - Error message validation
   - 100% test pass rate

3. **`docs/data_validator.md`** - Complete documentation
   - Feature overview
   - Quick start guide
   - Complete API reference
   - Real-world usage examples
   - Error handling guide
   - Best practices

4. **`requirements.txt`** - Updated dependencies
   - Added pytest>=7.0.0 for testing

## Key Features

✅ **Chainable API** - Build complex validation rules with method chaining  
✅ **Type Safety** - Validate strings, integers, floats, booleans, lists, and dictionaries  
✅ **Format Validation** - Built-in validators for emails, URLs, dates, and regex patterns  
✅ **Schema Validation** - Validate complex nested data structures  
✅ **Clear Error Messages** - Descriptive errors with field names  
✅ **Custom Validators** - Extend with your own validation logic  
✅ **Bulk Validation** - Validate multiple items at once  
✅ **Well Tested** - 60 comprehensive unit tests  
✅ **Documented** - Complete documentation with examples  

## Usage Examples

### Basic Validation
```python
from data_validator import Validator

# String validation
validator = Validator().required().string().min_length(3)
validator.validate("hello")  # Returns True

# Email validation
validator = Validator().required().email()
validator.validate("user@example.com")  # Returns True
```

### Schema Validation
```python
from data_validator import Schema, Validator

# Define user schema
user_schema = Schema({
    'username': Validator().required().string().min_length(3).max_length(20),
    'email': Validator().required().email(),
    'age': Validator().required().integer().min_value(18).max_value(120),
    'website': Validator().optional().url()
})

# Validate user data
user_data = {
    'username': 'johndoe',
    'email': 'john@example.com',
    'age': 25,
    'website': 'https://johndoe.com'
}

validated = user_schema.validate(user_data)
```

## Testing

All tests pass successfully:

```bash
$ pytest test_data_validator.py -v
============================== 60 passed in 0.07s ==============================
```

Test coverage includes:
- Type validation (string, int, float, bool, list, dict)
- Length validation (min/max for strings and lists)
- Range validation (min/max for numbers)
- Format validation (email, URL, date, regex)
- Schema validation (single and bulk)
- Error handling and messages
- Edge cases (empty values, unicode, special characters)

## Use Cases

This validation utility is perfect for:

- **API Request Validation** - Validate incoming API requests before processing
- **User Input Validation** - Validate form data and user input
- **Configuration Validation** - Ensure configuration files have correct structure
- **Data Import Validation** - Validate data before importing into databases
- **Testing** - Create test fixtures with validated data
- **Data Pipelines** - Validate data at each stage of processing

## Breaking Changes

None - This is a new feature with no impact on existing code.

## Dependencies

- Added `pytest>=7.0.0` for testing (development dependency)
- No new runtime dependencies

## Checklist

- [x] Feature implemented and working
- [x] Comprehensive tests written (60 tests)
- [x] All tests passing (100% pass rate)
- [x] Documentation created
- [x] Code follows Python best practices and PEP 8
- [x] No breaking changes to existing code
- [x] Dependencies updated in requirements.txt

## Future Enhancements

Potential future improvements:
- Async validation support
- Nested schema validation
- Validation result caching
- Integration with popular frameworks (Flask, FastAPI, Django)
- JSON Schema export/import
- Performance optimizations for bulk validation

## Related Issues

None - This is a proactive feature addition to enhance the project's capabilities.

---

**Ready for Review** ✅

This PR is ready for review and merge. All tests pass, documentation is complete, and the feature is production-ready.
