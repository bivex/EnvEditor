# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-05T01:58:45
# Last Updated: 2026-01-05T01:58:45
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""
VariableName Value Object

Represents the name/identifier of an environment variable.
Encapsulates validation rules for variable naming conventions.
"""

import re
from typing import Final

from ..exceptions import DomainValidationError


class VariableName:
    """
    Value object representing an environment variable name.

    Business Rules:
    - Must contain only alphanumeric characters and underscores
    - Must not start with a digit
    - Must not be empty
    - Maximum length of 255 characters
    - Case-sensitive
    """

    MAX_LENGTH: Final[int] = 255
    NAME_PATTERN: Final[str] = r'^[A-Za-z_][A-Za-z0-9_]*$'

    def __init__(self, value: str) -> None:
        """
        Initialize VariableName with validation.

        Args:
            value: The variable name string

        Raises:
            DomainValidationError: If the name violates business rules
        """
        self._validate(value)
        self._value = value

    @property
    def value(self) -> str:
        """Get the variable name value."""
        return self._value

    def _validate(self, value: str) -> None:
        """Validate the variable name against business rules."""
        if not isinstance(value, str):
            raise DomainValidationError("Variable name must be a string")

        if not value.strip():
            raise DomainValidationError("Variable name cannot be empty")

        if len(value) > self.MAX_LENGTH:
            raise DomainValidationError(
                f"Variable name cannot exceed {self.MAX_LENGTH} characters"
            )

        if not re.match(self.NAME_PATTERN, value):
            raise DomainValidationError(
                "Variable name must start with letter or underscore and contain only "
                "alphanumeric characters and underscores"
            )

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"VariableName('{self._value}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VariableName):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)
