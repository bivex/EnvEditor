# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-05T01:30:18
# Last Updated: 2026-01-05T01:38:16
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""
AuditDTO - Data Transfer Object

Simple data structure for transferring audit entry data
between layers without exposing domain entity internals.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class AuditDTO:
    """
    Data Transfer Object for AuditEntry.

    Contains all the data needed to represent an audit entry
    without any business logic or domain behavior.
    """

    id: str
    variable_id: str
    variable_name: str
    action: str
    user_id: str
    timestamp: datetime
    old_value: Optional[str]
    new_value: Optional[str]
    scope: Optional[str]
    metadata: Dict[str, Any]

    @classmethod
    def from_entity(cls, audit_entry: 'AuditEntry') -> 'AuditDTO':
        """
        Create DTO from domain entity.

        Args:
            audit_entry: The AuditEntry entity

        Returns:
            AuditDTO instance
        """
        from ..entities import AuditEntry
        return cls(
            id=audit_entry.id,
            variable_id=audit_entry.variable_id,
            variable_name=audit_entry.variable_name,
            action=audit_entry.action.value,
            user_id=audit_entry.user_id,
            timestamp=audit_entry.timestamp,
            old_value=audit_entry.old_value,
            new_value=audit_entry.new_value,
            scope=audit_entry.scope,
            metadata=audit_entry.metadata
        )

    def to_dict(self) -> dict:
        """
        Convert to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        result = {
            'id': self.id,
            'variable_id': self.variable_id,
            'variable_name': self.variable_name,
            'action': self.action,
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }

        if self.old_value is not None:
            result['old_value'] = self.old_value
        if self.new_value is not None:
            result['new_value'] = self.new_value
        if self.scope is not None:
            result['scope'] = self.scope

        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'AuditDTO':
        """
        Create DTO from dictionary.

        Args:
            data: Dictionary with audit entry data

        Returns:
            AuditDTO instance
        """
        return cls(
            id=data['id'],
            variable_id=data['variable_id'],
            variable_name=data['variable_name'],
            action=data['action'],
            user_id=data['user_id'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            old_value=data.get('old_value'),
            new_value=data.get('new_value'),
            scope=data.get('scope'),
            metadata=data.get('metadata', {})
        )
