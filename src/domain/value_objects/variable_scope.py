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
VariableScope Value Object

Represents the scope/context where an environment variable is defined.
Defines accessibility and persistence characteristics.
"""

from enum import Enum
from typing import Dict, Any


class VariableScope(Enum):
    """
    Enumeration of environment variable scopes.

    SYSTEM: Available to all users and processes on the machine
    USER: Available to all processes of the current user
    PROCESS: Available only to the specific process
    """

    SYSTEM = "system"
    USER = "user"
    PROCESS = "process"

    def __str__(self) -> str:
        return self.value

    def requires_elevation(self) -> bool:
        """
        Check if this scope requires elevated privileges to modify.

        Returns:
            True if system scope (requires admin/sudo), False otherwise
        """
        return self == VariableScope.SYSTEM

    def get_persistence_info(self) -> Dict[str, Any]:
        """
        Get information about how variables in this scope are persisted.

        Returns:
            Dictionary with persistence details
        """
        persistence_map = {
            VariableScope.SYSTEM: {
                "location": "/etc/environment or registry",
                "persistence": "permanent",
                "requires_restart": True
            },
            VariableScope.USER: {
                "location": "~/.bashrc or user registry",
                "persistence": "permanent",
                "requires_restart": False
            },
            VariableScope.PROCESS: {
                "location": "process memory",
                "persistence": "temporary",
                "requires_restart": False
            }
        }
        return persistence_map[self]

    @classmethod
    def from_string(cls, value: str) -> 'VariableScope':
        """
        Create VariableScope from string value.

        Args:
            value: String representation of the scope

        Returns:
            VariableScope instance

        Raises:
            ValueError: If the string doesn't match any scope
        """
        for scope in cls:
            if scope.value == value.lower():
                return scope
        raise ValueError(f"Invalid scope: {value}")
