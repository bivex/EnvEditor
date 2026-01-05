"""
ContextDTO - Data Transfer Object

Simple data structure for transferring environment context data
between layers without exposing domain entity internals.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Set, Optional


@dataclass(frozen=True)
class ContextDTO:
    """
    Data Transfer Object for EnvironmentContext.

    Contains all the data needed to represent a context
    without any business logic or domain behavior.
    """

    id: str
    name: str
    description: str
    variable_count: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, context: 'EnvironmentContext') -> 'ContextDTO':
        """
        Create DTO from domain entity.

        Args:
            context: The EnvironmentContext entity

        Returns:
            ContextDTO instance
        """
        from ..entities import EnvironmentContext
        return cls(
            id=context.id,
            name=str(context.name),
            description=context.description,
            variable_count=context.variable_count,
            created_at=context.created_at,
            updated_at=context.updated_at
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
            'description': self.description,
            'variable_count': self.variable_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ContextDTO':
        """
        Create DTO from dictionary.

        Args:
            data: Dictionary with context data

        Returns:
            ContextDTO instance
        """
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            variable_count=data['variable_count'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )
