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
ProcessId Value Object

Represents a process identifier (PID) with validation.
"""

from typing import Final

from ..exceptions import DomainValidationError


class ProcessId:
    """
    Value object representing a process ID.

    Business Rules:
    - Must be a positive integer
    - Must be within valid system PID range
    - Cannot be zero (system idle process)
    """

    MIN_PID: Final[int] = 1
    MAX_PID: Final[int] = 99999  # Common system limit

    def __init__(self, value: int) -> None:
        """
        Initialize ProcessId with validation.

        Args:
            value: The process ID number

        Raises:
            DomainValidationError: If the PID is invalid
        """
        self._validate(value)
        self._value = value

    @property
    def value(self) -> int:
        """Get the process ID value."""
        return self._value

    def _validate(self, value: int) -> None:
        """Validate the process ID."""
        if not isinstance(value, int):
            raise DomainValidationError("Process ID must be an integer")

        if value < self.MIN_PID:
            raise DomainValidationError(f"Process ID must be at least {self.MIN_PID}")

        if value > self.MAX_PID:
            raise DomainValidationError(f"Process ID cannot exceed {self.MAX_PID}")

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"ProcessId({self._value})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProcessId):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __lt__(self, other: 'ProcessId') -> bool:
        """Enable sorting by PID."""
        if not isinstance(other, ProcessId):
            return NotImplemented
        return self._value < other._value

    def __int__(self) -> int:
        """Enable conversion to int."""
        return self._value
