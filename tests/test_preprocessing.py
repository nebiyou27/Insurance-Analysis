# tests/test_preprocessing.py
import pytest

# Example function to test
def preprocess_data(data):
    if not data:
        raise ValueError("Data cannot be empty")
    return data.lower()

# Unit test
def test_preprocess_data():
    # Test for valid input
    assert preprocess_data("HELLO") == "hello"
    
    # Test for empty input
    with pytest.raises(ValueError):
        preprocess_data("")