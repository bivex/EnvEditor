"""
AuditService Domain Service

Domain service for managing audit trails and compliance tracking.
Handles the creation and management of audit entries.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities import AuditEntry, EnvironmentVariable
from ..events import VariableCreated, VariableUpdated, VariableDeleted
from ..value_objects import VariableScope


class AuditService(ABC):
    """
    Domain service for audit trail management.

    This service is responsible for:
    - Creating audit entries for variable changes
    - Retrieving audit history
    - Ensuring compliance with audit requirements
    """

    @abstractmethod
    def record_variable_creation(
        self,
        variable: EnvironmentVariable,
        user_id: str
    ) -> AuditEntry:
        """
        Record the creation of a new environment variable.

        Args:
            variable: The newly created variable
            user_id: ID of the user who created it

        Returns:
            The created audit entry
        """
        pass

    @abstractmethod
    def record_variable_update(
        self,
        variable: EnvironmentVariable,
        old_value: str,
        user_id: str
    ) -> AuditEntry:
        """
        Record the update of an existing environment variable.

        Args:
            variable: The updated variable
            old_value: The previous value
            user_id: ID of the user who updated it

        Returns:
            The created audit entry
        """
        pass

    @abstractmethod
    def record_variable_deletion(
        self,
        variable: EnvironmentVariable,
        user_id: str
    ) -> AuditEntry:
        """
        Record the deletion of an environment variable.

        Args:
            variable: The deleted variable
            user_id: ID of the user who deleted it

        Returns:
            The created audit entry
        """
        pass

    @abstractmethod
    def get_variable_audit_history(
        self,
        variable_id: str,
        limit: Optional[int] = None
    ) -> List[AuditEntry]:
        """
        Get the audit history for a specific variable.

        Args:
            variable_id: ID of the variable
            limit: Optional limit on number of entries to return

        Returns:
            List of audit entries, most recent first
        """
        pass

    @abstractmethod
    def get_user_audit_history(
        self,
        user_id: str,
        limit: Optional[int] = None
    ) -> List[AuditEntry]:
        """
        Get the audit history for a specific user.

        Args:
            user_id: ID of the user
            limit: Optional limit on number of entries to return

        Returns:
            List of audit entries, most recent first
        """
        pass


class DefaultAuditService(AuditService):
    """
    Default implementation of AuditService.

    Stores audit entries in memory. In a real application,
    this would be backed by a persistent audit store.
    """

    def __init__(self) -> None:
        self._audit_entries: List[AuditEntry] = []

    def record_variable_creation(
        self,
        variable: EnvironmentVariable,
        user_id: str
    ) -> AuditEntry:
        """Record variable creation."""
        entry = AuditEntry(
            variable_id=variable.id,
            variable_name=str(variable.name),
            action=AuditEntry.AuditAction.CREATED,
            user_id=user_id,
            new_value=str(variable.value),
            scope=str(variable.scope)
        )
        self._audit_entries.append(entry)
        return entry

    def record_variable_update(
        self,
        variable: EnvironmentVariable,
        old_value: str,
        user_id: str
    ) -> AuditEntry:
        """Record variable update."""
        entry = AuditEntry(
            variable_id=variable.id,
            variable_name=str(variable.name),
            action=AuditEntry.AuditAction.UPDATED,
            user_id=user_id,
            old_value=old_value,
            new_value=str(variable.value),
            scope=str(variable.scope)
        )
        self._audit_entries.append(entry)
        return entry

    def record_variable_deletion(
        self,
        variable: EnvironmentVariable,
        user_id: str
    ) -> AuditEntry:
        """Record variable deletion."""
        entry = AuditEntry(
            variable_id=variable.id,
            variable_name=str(variable.name),
            action=AuditEntry.AuditAction.DELETED,
            user_id=user_id,
            old_value=str(variable.value),
            scope=str(variable.scope)
        )
        self._audit_entries.append(entry)
        return entry

    def get_variable_audit_history(
        self,
        variable_id: str,
        limit: Optional[int] = None
    ) -> List[AuditEntry]:
        """Get audit history for a variable."""
        entries = [
            entry for entry in self._audit_entries
            if entry.variable_id == variable_id
        ]
        entries.sort(reverse=True)  # Most recent first
        return entries[:limit] if limit else entries

    def get_user_audit_history(
        self,
        user_id: str,
        limit: Optional[int] = None
    ) -> List[AuditEntry]:
        """Get audit history for a user."""
        entries = [
            entry for entry in self._audit_entries
            if entry.user_id == user_id
        ]
        entries.sort(reverse=True)  # Most recent first
        return entries[:limit] if limit else entries
