"""
AuditEntry Entity

Entity representing an audit trail entry for environment variable changes.
Provides accountability and compliance tracking.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

from ..exceptions import DomainValidationError


class AuditAction(Enum):
    """Types of audit actions that can be performed."""
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    ACCESSED = "accessed"


class AuditEntry:
    """
    Audit Entry Entity

    Represents a single audit trail entry for tracking changes to environment variables.
    This entity is immutable once created.

    Business Rules:
    - All changes to environment variables must be auditable
    - Audit entries cannot be modified after creation
    - Must include timestamp, user, and action details
    """

    def __init__(
        self,
        variable_id: str,
        variable_name: str,
        action: AuditAction,
        user_id: str,
        timestamp: Optional[datetime] = None,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
        scope: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        audit_id: Optional[str] = None
    ) -> None:
        """
        Initialize AuditEntry.

        Args:
            variable_id: ID of the variable that was affected
            variable_name: Name of the variable
            action: The action that was performed
            user_id: ID of the user who performed the action
            timestamp: When the action occurred (defaults to now)
            old_value: Previous value (for updates)
            new_value: New value (for creates/updates)
            scope: Variable scope
            metadata: Additional audit metadata
            audit_id: Optional ID, generated if not provided

        Raises:
            DomainValidationError: If required fields are missing or invalid
        """
        self._validate_required_fields(variable_id, variable_name, action, user_id)

        self._id = audit_id or str(uuid.uuid4())
        self._variable_id = variable_id
        self._variable_name = variable_name
        self._action = action
        self._user_id = user_id
        self._timestamp = timestamp or datetime.now()
        self._old_value = old_value
        self._new_value = new_value
        self._scope = scope
        self._metadata = metadata or {}

        # Audit entries are immutable - no domain events needed

    @property
    def id(self) -> str:
        """Get the unique identifier of this audit entry."""
        return self._id

    @property
    def variable_id(self) -> str:
        """Get the ID of the affected variable."""
        return self._variable_id

    @property
    def variable_name(self) -> str:
        """Get the name of the affected variable."""
        return self._variable_name

    @property
    def action(self) -> AuditAction:
        """Get the audit action."""
        return self._action

    @property
    def user_id(self) -> str:
        """Get the ID of the user who performed the action."""
        return self._user_id

    @property
    def timestamp(self) -> datetime:
        """Get when the action occurred."""
        return self._timestamp

    @property
    def old_value(self) -> Optional[str]:
        """Get the previous value (for updates)."""
        return self._old_value

    @property
    def new_value(self) -> Optional[str]:
        """Get the new value (for creates/updates)."""
        return self._new_value

    @property
    def scope(self) -> Optional[str]:
        """Get the variable scope."""
        return self._scope

    @property
    def metadata(self) -> Dict[str, Any]:
        """Get additional audit metadata."""
        return self._metadata.copy()

    def _validate_required_fields(
        self,
        variable_id: str,
        variable_name: str,
        action: AuditAction,
        user_id: str
    ) -> None:
        """Validate that all required fields are present and valid."""
        if not variable_id:
            raise DomainValidationError("Variable ID is required for audit entry")

        if not variable_name:
            raise DomainValidationError("Variable name is required for audit entry")

        if not isinstance(action, AuditAction):
            raise DomainValidationError("Valid audit action is required")

        if not user_id:
            raise DomainValidationError("User ID is required for audit entry")

        # Validate action-specific requirements
        if action == AuditAction.UPDATED and old_value is None:
            raise DomainValidationError("Old value is required for update actions")

        if action in [AuditAction.CREATED, AuditAction.UPDATED] and new_value is None:
            raise DomainValidationError("New value is required for create/update actions")

    def __str__(self) -> str:
        return (
            f"AuditEntry(action={self._action.value}, "
            f"variable='{self._variable_name}', user='{self._user_id}', "
            f"timestamp={self._timestamp.isoformat()})"
        )

    def __repr__(self) -> str:
        return (
            f"AuditEntry(id='{self._id}', variable_id='{self._variable_id}', "
            f"action={self._action!r}, user_id='{self._user_id}', "
            f"timestamp={self._timestamp!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AuditEntry):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __lt__(self, other: 'AuditEntry') -> bool:
        """Enable sorting audit entries by timestamp."""
        if not isinstance(other, AuditEntry):
            return NotImplemented
        return self._timestamp < other._timestamp
