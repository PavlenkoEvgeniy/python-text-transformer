"""
Unit tests for the core text transformation logic.

These tests cover all transformation operations and verify the
TextTransformer class behaves correctly in various scenarios.
"""

import pytest

from text_transformer.transformer import TextTransformer, TransformationType


class TestTextTransformer:
    """Test suite for TextTransformer class."""

    def test_initialization(self, transformer: TextTransformer) -> None:
        """Test that the transformer initializes with all operations available."""
        assert len(transformer.available_operations) == 4
        assert TransformationType.UPPERCASE in transformer.available_operations
        assert TransformationType.LOWERCASE in transformer.available_operations
        assert TransformationType.CAPITALIZE in transformer.available_operations
        assert TransformationType.TITLE in transformer.available_operations

    # --- Uppercase Tests ---

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("hello", "HELLO"),
            ("Hello", "HELLO"),
            ("HELLO", "HELLO"),
            ("hello world", "HELLO WORLD"),
            ("", ""),
            ("a", "A"),
            ("123 abc", "123 ABC"),
        ],
    )
    def test_uppercase_transformation(
        self, transformer: TextTransformer, input_text: str, expected: str
    ) -> None:
        """Test uppercase transformation with various inputs."""
        result = transformer.transform(input_text, TransformationType.UPPERCASE)
        assert result == expected

    # --- Lowercase Tests ---

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("hello", "hello"),
            ("Hello", "hello"),
            ("HELLO", "hello"),
            ("HELLO WORLD", "hello world"),
            ("", ""),
            ("A", "a"),
            ("123 ABC", "123 abc"),
        ],
    )
    def test_lowercase_transformation(
        self, transformer: TextTransformer, input_text: str, expected: str
    ) -> None:
        """Test lowercase transformation with various inputs."""
        result = transformer.transform(input_text, TransformationType.LOWERCASE)
        assert result == expected

    # --- Capitalize Tests ---

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("hello", "Hello"),
            ("Hello", "Hello"),
            ("HELLO", "Hello"),
            ("hello world", "Hello world"),
            ("", ""),
            ("a", "A"),
            ("123 abc", "123 abc"),
        ],
    )
    def test_capitalize_transformation(
        self, transformer: TextTransformer, input_text: str, expected: str
    ) -> None:
        """Test capitalize transformation with various inputs."""
        result = transformer.transform(input_text, TransformationType.CAPITALIZE)
        assert result == expected

    # --- Title Tests ---

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("hello", "Hello"),
            ("Hello", "Hello"),
            ("HELLO", "Hello"),
            ("hello world", "Hello World"),
            ("hello WORLD", "Hello World"),
            ("", ""),
            ("a", "A"),
            ("123 abc", "123 Abc"),
        ],
    )
    def test_title_transformation(
        self, transformer: TextTransformer, input_text: str, expected: str
    ) -> None:
        """Test title transformation with various inputs."""
        result = transformer.transform(input_text, TransformationType.TITLE)
        assert result == expected

    # --- Edge Case Tests ---

    def test_empty_string(self, transformer: TextTransformer) -> None:
        """Test transformation of empty string returns empty string."""
        result = transformer.transform("", TransformationType.UPPERCASE)
        assert result == ""

    def test_whitespace_only(self, transformer: TextTransformer) -> None:
        """Test transformation of whitespace-only string."""
        result = transformer.transform("   ", TransformationType.UPPERCASE)
        assert result == "   "

    def test_special_characters(self, transformer: TextTransformer) -> None:
        """Test transformation preserves special characters."""
        input_text = "!@#$%^&*()"
        result = transformer.transform(input_text, TransformationType.UPPERCASE)
        assert result == "!@#$%^&*()"

    def test_unicode_characters(self, transformer: TextTransformer) -> None:
        """Test transformation handles Unicode characters."""
        input_text = "héllo wörld"
        result = transformer.transform(input_text, TransformationType.UPPERCASE)
        assert result == "HÉLLO WÖRLD"

    def test_newlines_and_tabs(self, transformer: TextTransformer) -> None:
        """Test transformation preserves newlines and tabs."""
        input_text = "hello\nworld\ttab"
        result = transformer.transform(input_text, TransformationType.UPPERCASE)
        assert result == "HELLO\nWORLD\tTAB"

    # --- Error Handling Tests ---

    def test_invalid_operation_raises_error(self, transformer: TextTransformer) -> None:
        """Test that invalid operation raises ValueError."""
        with pytest.raises(ValueError):
            transformer.transform("hello", "invalid_operation")  # type: ignore

    def test_none_operation_raises_error(self, transformer: TextTransformer) -> None:
        """Test that None operation raises ValueError."""
        with pytest.raises(ValueError):
            transformer.transform("hello", None)  # type: ignore

    # --- Helper Method Tests ---

    def test_get_operation_display_name(self, transformer: TextTransformer) -> None:
        """Test getting display name for operations."""
        assert transformer.get_operation_display_name(TransformationType.UPPERCASE) == "Uppercase"
        assert transformer.get_operation_display_name(TransformationType.LOWERCASE) == "Lowercase"
        assert transformer.get_operation_display_name(TransformationType.CAPITALIZE) == "Capitalize"
        assert transformer.get_operation_display_name(TransformationType.TITLE) == "Title"

    def test_get_all_operation_names(self, transformer: TextTransformer) -> None:
        """Test getting all operation names."""
        names = transformer.get_all_operation_names()
        assert names == ["Uppercase", "Lowercase", "Capitalize", "Title"]

    @pytest.mark.parametrize(
        "name,expected",
        [
            ("Uppercase", TransformationType.UPPERCASE),
            ("Lowercase", TransformationType.LOWERCASE),
            ("Capitalize", TransformationType.CAPITALIZE),
            ("Title", TransformationType.TITLE),
            ("Invalid", None),
            ("", None),
        ],
    )
    def test_get_operation_from_name(
        self, transformer: TextTransformer, name: str, expected: TransformationType | None
    ) -> None:
        """Test getting operation type from name."""
        result = transformer.get_operation_from_name(name)
        assert result == expected

    @pytest.mark.parametrize(
        "name,expected",
        [
            ("Uppercase", True),
            ("Lowercase", True),
            ("Capitalize", True),
            ("Title", True),
            ("Invalid", False),
            ("", False),
            ("lowercase", False),  # Case sensitive
        ],
    )
    def test_is_valid_operation(
        self, transformer: TextTransformer, name: str, expected: bool
    ) -> None:
        """Test validating operation names."""
        result = transformer.is_valid_operation(name)
        assert result == expected


class TestTransformationType:
    """Test suite for TransformationType enum."""

    def test_enum_values(self) -> None:
        """Test enum has correct values."""
        assert TransformationType.UPPERCASE.value == "Uppercase"
        assert TransformationType.LOWERCASE.value == "Lowercase"
        assert TransformationType.CAPITALIZE.value == "Capitalize"
        assert TransformationType.TITLE.value == "Title"

    def test_enum_members(self) -> None:
        """Test all expected enum members exist."""
        members = list(TransformationType)
        assert len(members) == 4
        assert TransformationType.UPPERCASE in members
        assert TransformationType.LOWERCASE in members
        assert TransformationType.CAPITALIZE in members
        assert TransformationType.TITLE in members

    def test_enum_iteration(self) -> None:
        """Test enum can be iterated."""
        names = [op.value for op in TransformationType]
        assert names == ["Uppercase", "Lowercase", "Capitalize", "Title"]
