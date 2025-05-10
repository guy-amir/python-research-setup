"""
Test cases for python-research-setup core functionality.
"""
import pytest
from python-research-setup.core import hello_world


def test_hello_world():
    """Test that hello_world returns the expected greeting."""
    result = hello_world()
    assert f"Hello from python-research-setup!" in result
