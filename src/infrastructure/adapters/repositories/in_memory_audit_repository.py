"""
In-Memory Audit Repository

In-memory implementation of AuditRepository for testing and development.
"""

from typing import List, Optional
from datetime import datetime

from ....domain import (
    AuditEntry,
    AuditRepository
)


class InMemoryAuditRepository(AuditRepository):
    """
    In-memory implementation of AuditRepository.
    """

    def __init__(self) -> None:
        """Initialize empty repository."""
        self._audit_entries: dict[str, AuditEntry] = {}
        self._entries_by_variable: dict[str, List[AuditEntry]] = {}
        self._entries_by_user: dict[str, List[AuditEntry]] = {}

    def save(self, audit_entry: AuditEntry) -> None:
        """Save an audit entry."""
        self._audit_entries[audit_entry.id] = audit_entry

        # Index by variable
        var_id = audit_entry.variable_id
        if var_id not in self._entries_by_variable:
            self._entries_by_variable[var_id] = []
        self._entries_by_variable[var_id].append(audit_entry)

        # Index by user
        user_id = audit_entry.user_id
        if user_id not in self._entries_by_user:
            self._entries_by_user[user_id] = []
        self._entries_by_user[user_id].append(audit_entry)

    def find_by_id(self, audit_id: str) -> Optional[AuditEntry]:
        """Find audit entry by ID."""
        return self._audit_entries.get(audit_id)

    def find_by_variable_id(
        self,
        variable_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[AuditEntry]:
        """Find audit entries by variable ID."""
        entries = sorted(
            self._entries_by_variable.get(variable_id, []),
            key=lambda e: e.timestamp,
            reverse=True
        )
        if offset:
            entries = entries[offset:]
        if limit:
            entries = entries[:limit]
        return entries

    def find_by_user_id(
        self,
        user_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[AuditEntry]:
        """Find audit entries by user ID."""
        entries = sorted(
            self._entries_by_user.get(user_id, []),
            key=lambda e: e.timestamp,
            reverse=True
        )
        if offset:
            entries = entries[offset:]
        if limit:
            entries = entries[:limit]
        return entries

    def find_by_time_range(
        self,
        start_time: datetime,
        end_time: datetime,
        limit: Optional[int] = None
    ) -> List[AuditEntry]:
        """Find audit entries in time range."""
        entries = [
            entry for entry in self._audit_entries.values()
            if start_time <= entry.timestamp <= end_time
        ]
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        return entries[:limit] if limit else entries

    def find_by_variable_and_time_range(
        self,
        variable_id: str,
        start_time: datetime,
        end_time: datetime,
        limit: Optional[int] = None
    ) -> List[AuditEntry]:
        """Find audit entries for variable in time range."""
        entries = [
            entry for entry in self._entries_by_variable.get(variable_id, [])
            if start_time <= entry.timestamp <= end_time
        ]
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        return entries[:limit] if limit else entries

    def count_by_variable_id(self, variable_id: str) -> int:
        """Count entries for variable."""
        return len(self._entries_by_variable.get(variable_id, []))

    def count_by_user_id(self, user_id: str) -> int:
        """Count entries for user."""
        return len(self._entries_by_user.get(user_id, []))

    def get_most_recent_entry_for_variable(self, variable_id: str) -> Optional[AuditEntry]:
        """Get most recent entry for variable."""
        entries = self._entries_by_variable.get(variable_id, [])
        return max(entries, key=lambda e: e.timestamp) if entries else None
