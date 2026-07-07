"""
Test configuration and fixtures for the text transformer package.
"""

from unittest.mock import Mock

import pytest

from text_transformer.transformer import TextTransformer, TransformationType


@pytest.fixture
def transformer() -> TextTransformer:
    """Create a TextTransformer instance for testing."""
    return TextTransformer()


@pytest.fixture
def mock_protocol() -> Mock:
    """Create a mock transformer that satisfies the TextTransformerProtocol."""
    mock = Mock()
    mock.available_operations = list(TransformationType)
    mock.transform = Mock(side_effect=lambda text, op: text.upper() if op == TransformationType.UPPERCASE else text.lower())
    mock.get_all_operation_names = Mock(return_value=["Uppercase", "Lowercase", "Capitalize", "Title"])
    mock.get_operation_from_name = Mock(side_effect=lambda name: TransformationType.UPPERCASE if name == "Uppercase" else None)
    return mock


@pytest.fixture
def sample_text() -> str:
    """Sample text for testing."""
    return "hello world"


@pytest.fixture
def sample_text_mixed() -> str:
    """Sample text with mixed case for testing."""
    return "HeLLo WoRLD"
