"""
ContextName Value Object

Represents the name of an environment context.
Encapsulates validation rules for context naming.
"""

import re
from typing import Final

from ..exceptions import DomainValidationError


class ContextName:
    """
    Value object representing an environment context name.

    Business Rules:
    - Must contain only alphanumeric characters, spaces, hyphens, and underscores
    - Must not be empty
    - Maximum length of 100 characters
    - Case-sensitive
    """

    MAX_LENGTH: Final[int] = 100
    NAME_PATTERN: Final[str] = r'^[A-Za-z0-9\s\-_]+$'

    def __init__(self, value: str) -> None:
        """
        Initialize ContextName with validation.

        Args:
            value: The context name string

        Raises:
            DomainValidationError: If the name violates business rules
        """
        self._validate(value)
        self._value = value.strip()  # Normalize whitespace

    @property
    def value(self) -> str:
        """Get the context name value."""
        return self._value

    def _validate(self, value: str) -> None:
        """Validate the context name against business rules."""
        if not isinstance(value, str):
            raise DomainValidationError("Context name must be a string")

        if not value.strip():
            raise DomainValidationError("Context name cannot be empty")

        if len(value) > self.MAX_LENGTH:
            raise DomainValidationError(
                f"Context name cannot exceed {self.MAX_LENGTH} characters"
            )

        if not re.match(self.NAME_PATTERN, value):
            raise DomainValidationError(
                "Context name can only contain alphanumeric characters, "
                "spaces, hyphens, and underscores"
            )

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"ContextName('{self._value}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ContextName):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)
