# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-05T01:28:36
# Last Updated: 2026-01-05T01:28:36
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""
VariableValue Value Object

Represents the value of an environment variable.
Encapsulates value validation and business rules.
"""

from typing import Final

from ..exceptions import DomainValidationError


class VariableValue:
    """
    Value object representing an environment variable value.

    Business Rules:
    - Can contain any characters including spaces and special characters
    - Maximum length depends on the operating system (typically 32KB)
    - Cannot be None (use empty string for no value)
    """

    MAX_LENGTH: Final[int] = 32767  # 32KB - 1, typical OS limit

    def __init__(self, value: str) -> None:
        """
        Initialize VariableValue with validation.

        Args:
            value: The variable value string (can be empty but not None)

        Raises:
            DomainValidationError: If the value violates business rules
        """
        if value is None:
            raise DomainValidationError("Variable value cannot be None")

        self._validate(value)
        self._value = value

    @property
    def value(self) -> str:
        """Get the variable value."""
        return self._value

    @property
    def is_empty(self) -> bool:
        """Check if the value is empty."""
        return not self._value

    def _validate(self, value: str) -> None:
        """Validate the variable value against business rules."""
        if not isinstance(value, str):
            raise DomainValidationError("Variable value must be a string")

        if len(value) > self.MAX_LENGTH:
            raise DomainValidationError(
                f"Variable value cannot exceed {self.MAX_LENGTH} characters"
            )

    def __str__(self) -> str:
        # Mask sensitive-looking values for security
        if self._looks_sensitive():
            return "***"
        return self._value

    def __repr__(self) -> str:
        if self._looks_sensitive():
            return "VariableValue('***')"
        return f"VariableValue('{self._value}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VariableValue):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def _looks_sensitive(self) -> bool:
        """
        Check if the value appears to contain sensitive information.
        This is a heuristic for display purposes only.
        """
        sensitive_keywords = ['password', 'secret', 'key', 'token', 'auth']
        value_lower = self._value.lower()

        return any(keyword in value_lower for keyword in sensitive_keywords)
