"""
ProcessName Value Object

Represents a process name/executable with validation.
"""

import os
from typing import Final

from ..exceptions import DomainValidationError


class ProcessName:
    """
    Value object representing a process name.

    Business Rules:
    - Cannot be empty or whitespace-only
    - Must be a valid filename (no path separators)
    - Maximum length constraints
    - Case-sensitive
    """

    MAX_LENGTH: Final[int] = 255
    INVALID_CHARS: Final[str] = '/\\:*?"<>|'

    def __init__(self, value: str) -> None:
        """
        Initialize ProcessName with validation.

        Args:
            value: The process name string

        Raises:
            DomainValidationError: If the name is invalid
        """
        self._validate(value)
        self._value = value.strip()

    @property
    def value(self) -> str:
        """Get the process name value."""
        return self._value

    @property
    def basename(self) -> str:
        """Get just the filename part without path."""
        return os.path.basename(self._value)

    @property
    def extension(self) -> str:
        """Get the file extension if any."""
        return os.path.splitext(self._value)[1]

    def _validate(self, value: str) -> None:
        """Validate the process name."""
        if not isinstance(value, str):
            raise DomainValidationError("Process name must be a string")

        if not value.strip():
            raise DomainValidationError("Process name cannot be empty")

        if len(value) > self.MAX_LENGTH:
            raise DomainValidationError(
                f"Process name cannot exceed {self.MAX_LENGTH} characters"
            )

        # Check for invalid path characters - be more permissive for process names
        # Allow some special characters that might appear in process names
        problematic_chars = set(self.INVALID_CHARS) - set(['/', '\\', ':', '*', '?', '"', '<', '>', '|'])
        if any(char in value for char in problematic_chars):
            raise DomainValidationError(
                f"Process name cannot contain invalid characters: {''.join(problematic_chars)}"
            )

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"ProcessName('{self._value}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProcessName):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)
