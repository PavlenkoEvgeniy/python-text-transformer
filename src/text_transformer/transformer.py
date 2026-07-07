"""
Core text transformation logic module.

This module contains the pure business logic for text transformations,
separate from any GUI concerns.
"""

from enum import Enum
from typing import Protocol, runtime_checkable


class TransformationType(Enum):
    """Enumeration of available text transformation types."""

    UPPERCASE = "Uppercase"
    LOWERCASE = "Lowercase"
    CAPITALIZE = "Capitalize"
    TITLE = "Title"


@runtime_checkable
class TextTransformerProtocol(Protocol):
    """Protocol defining the text transformer interface."""

    available_operations: list[TransformationType]

    def transform(self, text: str, operation: TransformationType) -> str:
        """Transform text according to the specified operation."""
        ...

    def get_all_operation_names(self) -> list[str]:
        """Get a list of all available operation display names."""
        ...

    def get_operation_from_name(self, name: str) -> TransformationType | None:
        """Get the TransformationType enum from its display name."""
        ...


class TextTransformer:
    """
    Handles text transformations with support for multiple case operations.

    This class encapsulates all text transformation logic, making it
    easy to test and reuse without any GUI dependencies.

    Attributes:
        available_operations: List of all supported transformation types.

    Example:
        >>> transformer = TextTransformer()
        >>> transformer.transform("hello world", TransformationType.UPPERCASE)
        'HELLO WORLD'
    """

    def __init__(self) -> None:
        """Initialize the text transformer."""
        self.available_operations = list(TransformationType)

    def transform(self, text: str, operation: TransformationType) -> str:
        """
        Transform the input text according to the specified operation.

        Args:
            text: The input text to transform.
            operation: The type of transformation to apply.

        Returns:
            The transformed text, or empty string if operation is unknown.

        Raises:
            ValueError: If the operation is not recognized.
        """
        if not isinstance(operation, TransformationType):
            raise ValueError(f"Unknown operation: {operation}")

        if not text:
            return ""

        return self._apply_transformation(text, operation)

    def _apply_transformation(self, text: str, operation: TransformationType) -> str:
        """
        Apply the actual transformation to the text.

        Args:
            text: The input text to transform.
            operation: The transformation type to apply.

        Returns:
            The transformed text.
        """
        match operation:
            case TransformationType.UPPERCASE:
                return text.upper()
            case TransformationType.LOWERCASE:
                return text.lower()
            case TransformationType.CAPITALIZE:
                return text.capitalize()
            case TransformationType.TITLE:
                return text.title()
            case _:
                return ""

    def get_operation_display_name(self, operation: TransformationType) -> str:
        """
        Get the display-friendly name for an operation.

        Args:
            operation: The transformation type.

        Returns:
            The display name for the operation.
        """
        return operation.value

    def get_all_operation_names(self) -> list[str]:
        """
        Get a list of all available operation display names.

        Returns:
            List of operation display names in order.
        """
        return [op.value for op in self.available_operations]

    def is_valid_operation(self, operation_name: str) -> bool:
        """
        Check if an operation name is valid.

        Args:
            operation_name: The name to check.

        Returns:
            True if the operation name is valid, False otherwise.
        """
        return operation_name in self.get_all_operation_names()

    def get_operation_from_name(self, name: str) -> TransformationType | None:
        """
        Get the TransformationType enum from its display name.

        Args:
            name: The display name of the operation.

        Returns:
            The corresponding TransformationType, or None if not found.
        """
        for operation in self.available_operations:
            if operation.value == name:
                return operation
        return None
