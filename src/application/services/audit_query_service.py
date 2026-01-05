"""
AuditQueryService - Application Service

Use case implementations for audit trail queries.
Provides read-only access to audit information.
"""

from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

from ...domain import (
    AuditEntry,
    AuditRepository,
    AuditDTO
)


@dataclass
class AuditQuery:
    """Query parameters for audit searches."""
    variable_id: Optional[str] = None
    user_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


class AuditQueryService:
    """
    Application service for audit trail queries.

    This service provides read-only access to audit information for:
    - Variable change history
    - User activity tracking
    - Compliance and security auditing
    """

    def __init__(self, audit_repository: AuditRepository) -> None:
        """
        Initialize the service with dependencies.

        Args:
            audit_repository: Repository for audit data access
        """
        self._audit_repository = audit_repository

    def get_variable_audit_history(
        self,
        variable_id: str,
        limit: Optional[int] = None
    ) -> List[AuditDTO]:
        """
        Get the complete audit history for a specific variable.

        Args:
            variable_id: The ID of the variable
            limit: Optional limit on number of entries to return

        Returns:
            List of audit entries as DTOs, most recent first
        """
        audit_entries = self._audit_repository.find_by_variable_id(
            variable_id=variable_id,
            limit=limit
        )

        return [AuditDTO.from_entity(entry) for entry in audit_entries]

    def get_user_audit_history(
        self,
        user_id: str,
        limit: Optional[int] = None
    ) -> List[AuditDTO]:
        """
        Get the audit history for a specific user.

        Args:
            user_id: The ID of the user
            limit: Optional limit on number of entries to return

        Returns:
            List of audit entries as DTOs, most recent first
        """
        audit_entries = self._audit_repository.find_by_user_id(
            user_id=user_id,
            limit=limit
        )

        return [AuditDTO.from_entity(entry) for entry in audit_entries]

    def get_audit_history_by_time_range(
        self,
        start_time: datetime,
        end_time: datetime,
        limit: Optional[int] = None
    ) -> List[AuditDTO]:
        """
        Get audit entries within a specific time range.

        Args:
            start_time: Start of the time range
            end_time: End of the time range
            limit: Optional limit on number of entries

        Returns:
            List of audit entries as DTOs, most recent first
        """
        audit_entries = self._audit_repository.find_by_time_range(
            start_time=start_time,
            end_time=end_time,
            limit=limit
        )

        return [AuditDTO.from_entity(entry) for entry in audit_entries]

    def get_variable_audit_history_in_time_range(
        self,
        variable_id: str,
        start_time: datetime,
        end_time: datetime,
        limit: Optional[int] = None
    ) -> List[AuditDTO]:
        """
        Get audit entries for a variable within a specific time range.

        Args:
            variable_id: The ID of the variable
            start_time: Start of the time range
            end_time: End of the time range
            limit: Optional limit on number of entries

        Returns:
            List of audit entries as DTOs for the variable in the time range
        """
        audit_entries = self._audit_repository.find_by_variable_and_time_range(
            variable_id=variable_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit
        )

        return [AuditDTO.from_entity(entry) for entry in audit_entries]

    def get_audit_entry_count_for_variable(self, variable_id: str) -> int:
        """
        Get the total number of audit entries for a variable.

        Args:
            variable_id: The ID of the variable

        Returns:
            Number of audit entries for the variable
        """
        return self._audit_repository.count_by_variable_id(variable_id)

    def get_audit_entry_count_for_user(self, user_id: str) -> int:
        """
        Get the total number of audit entries for a user.

        Args:
            user_id: The ID of the user

        Returns:
            Number of audit entries for the user
        """
        return self._audit_repository.count_by_user_id(user_id)

    def get_most_recent_audit_entry_for_variable(self, variable_id: str) -> Optional[AuditDTO]:
        """
        Get the most recent audit entry for a variable.

        Args:
            variable_id: The ID of the variable

        Returns:
            The most recent audit entry as DTO, or None if none exists
        """
        audit_entry = self._audit_repository.get_most_recent_entry_for_variable(variable_id)
        if audit_entry:
            return AuditDTO.from_entity(audit_entry)
        return None

    def get_audit_entry(self, audit_id: str) -> Optional[AuditDTO]:
        """
        Get a specific audit entry by ID.

        Args:
            audit_id: The ID of the audit entry

        Returns:
            The audit entry as DTO if found, None otherwise
        """
        audit_entry = self._audit_repository.find_by_id(audit_id)
        if audit_entry:
            return AuditDTO.from_entity(audit_entry)
        return None
