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
VariableDTO - Data Transfer Object

Simple data structure for transferring environment variable data
between layers without exposing domain entity internals.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class VariableDTO:
    """
    Data Transfer Object for EnvironmentVariable.

    Contains all the data needed to represent a variable
    without any business logic or domain behavior.
    """

    id: str
    name: str
    value: str
    scope: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, variable: 'EnvironmentVariable') -> 'VariableDTO':
        """
        Create DTO from domain entity.

        Args:
            variable: The EnvironmentVariable entity

        Returns:
            VariableDTO instance
        """
        from ..entities import EnvironmentVariable
        return cls(
            id=variable.id,
            name=str(variable.name),
            value=str(variable.value),
            scope=str(variable.scope),
            created_at=variable.created_at,
            updated_at=variable.updated_at
        )

    def to_dict(self) -> dict:
        """
        Convert to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value,
            'scope': self.scope,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'VariableDTO':
        """
        Create DTO from dictionary.

        Args:
            data: Dictionary with variable data

        Returns:
            VariableDTO instance
        """
        return cls(
            id=data['id'],
            name=data['name'],
            value=data['value'],
            scope=data['scope'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )
