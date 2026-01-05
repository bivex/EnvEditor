"""
AuditRepository Interface

Repository interface for AuditEntry access.
Defines the contract for persisting and retrieving audit trails.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from ..entities import AuditEntry


class AuditRepository(ABC):
    """
    Repository interface for AuditEntry access.

    This interface defines the contract for:
    - Persisting audit entries
    - Retrieving audit history
    - Audit trail queries
    """

    @abstractmethod
    def save(self, audit_entry: AuditEntry) -> None:
        """
        Save an audit entry.

        Args:
            audit_entry: The audit entry to save
        """
        pass

    @abstractmethod
    def find_by_id(self, audit_id: str) -> Optional[AuditEntry]:
        """
        Find an audit entry by its ID.

        Args:
            audit_id: The unique identifier of the audit entry

        Returns:
            The audit entry if found, None otherwise
        """
        pass

    @abstractmethod
    def find_by_variable_id(
        self,
        variable_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[AuditEntry]:
        """
        Find audit entries for a specific variable.

        Args:
            variable_id: The variable ID
            limit: Optional limit on number of entries
            offset: Optional offset for pagination

        Returns:
            List of audit entries for the variable, most recent first
        """
        pass

    @abstractmethod
    def find_by_user_id(
        self,
        user_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[AuditEntry]:
        """
        Find audit entries for a specific user.

        Args:
            user_id: The user ID
            limit: Optional limit on number of entries
            offset: Optional offset for pagination

        Returns:
            List of audit entries for the user, most recent first
        """
        pass

    @abstractmethod
    def find_by_time_range(
        self,
        start_time: datetime,
        end_time: datetime,
        limit: Optional[int] = None
    ) -> List[AuditEntry]:
        """
        Find audit entries within a time range.

        Args:
            start_time: Start of the time range
            end_time: End of the time range
            limit: Optional limit on number of entries

        Returns:
            List of audit entries in the time range, most recent first
        """
        pass

    @abstractmethod
    def find_by_variable_and_time_range(
        self,
        variable_id: str,
        start_time: datetime,
        end_time: datetime,
        limit: Optional[int] = None
    ) -> List[AuditEntry]:
        """
        Find audit entries for a variable within a time range.

        Args:
            variable_id: The variable ID
            start_time: Start of the time range
            end_time: End of the time range
            limit: Optional limit on number of entries

        Returns:
            List of audit entries for the variable in the time range
        """
        pass

    @abstractmethod
    def count_by_variable_id(self, variable_id: str) -> int:
        """
        Count audit entries for a specific variable.

        Args:
            variable_id: The variable ID

        Returns:
            Number of audit entries for the variable
        """
        pass

    @abstractmethod
    def count_by_user_id(self, user_id: str) -> int:
        """
        Count audit entries for a specific user.

        Args:
            user_id: The user ID

        Returns:
            Number of audit entries for the user
        """
        pass

    @abstractmethod
    def get_most_recent_entry_for_variable(self, variable_id: str) -> Optional[AuditEntry]:
        """
        Get the most recent audit entry for a variable.

        Args:
            variable_id: The variable ID

        Returns:
            The most recent audit entry, or None if none exists
        """
        pass
