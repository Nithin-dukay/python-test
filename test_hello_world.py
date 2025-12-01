#!/usr/bin/env python3
"""
Simple Hello World Test
"""

def hello_world():
    """Returns a greeting message"""
    return "Hello World"


def test_hello_world():
    """Test the hello_world function"""
    result = hello_world()
    assert result == "Hello World", f"Expected 'Hello World', got '{result}'"
    print("✓ Test passed: hello_world() returns 'Hello World'")


def test_hello_world_type():
    """Test that hello_world returns a string"""
    result = hello_world()
    assert isinstance(result, str), f"Expected string, got {type(result)}"
    print("✓ Test passed: hello_world() returns a string")


def test_hello_world_length():
    """Test the length of the greeting"""
    result = hello_world()
    assert len(result) == 11, f"Expected length 11, got {len(result)}"
    print("✓ Test passed: hello_world() has correct length")


if __name__ == "__main__":
    print("Running Hello World Tests...\n")

    try:
        test_hello_world()
        test_hello_world_type()
        test_hello_world_length()
        print("\n✓ All tests passed!")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        exit(1)
