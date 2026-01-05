# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-05T01:19:29
# Last Updated: 2026-01-05T01:58:45
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""
EnvironmentVariable Entity

Core domain entity representing an environment variable.
This is an aggregate root that enforces business invariants.
"""

import uuid
from datetime import datetime
from typing import Optional, List

from ..value_objects import VariableName, VariableValue, VariableScope
from ..events import VariableCreated, VariableUpdated, VariableDeleted
from ..exceptions import DomainValidationError, AggregateInvariantViolationError


class EnvironmentVariable:
    """
    Environment Variable Entity - Aggregate Root

    Represents a single environment variable with its name, value, and scope.
    Enforces business rules and maintains integrity of the variable.

    Business Invariants:
    - Name must be valid and unique within scope
    - Value must be valid for the given scope
    - Scope determines accessibility and persistence
    - Changes are tracked through domain events
    """

    def __init__(
        self,
        name: VariableName,
        value: VariableValue,
        scope: VariableScope,
        variable_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        """
        Initialize EnvironmentVariable.

        Args:
            name: The variable name (must be valid)
            value: The variable value
            scope: The variable scope
            variable_id: Optional ID, generated if not provided
            created_at: Optional creation timestamp
            updated_at: Optional last update timestamp
        """
        self._id = variable_id or str(uuid.uuid4())
        self._name = name
        self._value = value
        self._scope = scope
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or self._created_at
        self._domain_events: List[object] = []

        # Validate aggregate invariants
        self._validate_invariants()

        # Record creation event
        if not variable_id:  # Only for new variables
            self._add_domain_event(VariableCreated(
                variable_id=self._id,
                name=str(self._name),
                value=str(self._value),
                scope=str(self._scope),
                timestamp=self._created_at
            ))

    @property
    def id(self) -> str:
        """Get the unique identifier of this variable."""
        return self._id

    @property
    def name(self) -> VariableName:
        """Get the variable name."""
        return self._name

    @property
    def value(self) -> VariableValue:
        """Get the variable value."""
        return self._value

    @property
    def scope(self) -> VariableScope:
        """Get the variable scope."""
        return self._scope

    @property
    def created_at(self) -> datetime:
        """Get the creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Get the last update timestamp."""
        return self._updated_at

    def update_value(self, new_value: VariableValue) -> None:
        """
        Update the variable value.

        Args:
            new_value: The new value for the variable

        Raises:
            DomainValidationError: If the new value is invalid
        """
        if new_value == self._value:
            return  # No change needed

        old_value = str(self._value)
        self._value = new_value
        self._updated_at = datetime.now()

        # Validate invariants after change
        self._validate_invariants()

        # Record update event
        self._add_domain_event(VariableUpdated(
            variable_id=self._id,
            name=str(self._name),
            old_value=old_value,
            new_value=str(self._value),
            scope=str(self._scope),
            timestamp=self._updated_at
        ))

    def change_scope(self, new_scope: VariableScope) -> None:
        """
        Change the variable scope.

        Args:
            new_scope: The new scope for the variable

        Raises:
            AggregateInvariantViolationError: If scope change violates business rules
        """
        if new_scope == self._scope:
            return  # No change needed

        # Business rule: Scope changes may have restrictions
        if self._scope == VariableScope.SYSTEM and new_scope != VariableScope.SYSTEM:
            raise AggregateInvariantViolationError(
                "Cannot change scope of system variables"
            )

        old_scope = str(self._scope)
        self._scope = new_scope
        self._updated_at = datetime.now()

        # Validate invariants after change
        self._validate_invariants()

        # Record update event (scope change is a special type of update)
        self._add_domain_event(VariableUpdated(
            variable_id=self._id,
            name=str(self._name),
            old_value=str(self._value),
            new_value=str(self._value),
            scope=str(self._scope),
            timestamp=self._updated_at,
            metadata={"scope_changed": True, "old_scope": old_scope}
        ))

    def mark_for_deletion(self) -> None:
        """
        Mark this variable for deletion.

        This method records the deletion event but doesn't actually
        delete the entity (that's handled by the repository).
        """
        self._add_domain_event(VariableDeleted(
            variable_id=self._id,
            name=str(self._name),
            value=str(self._value),
            scope=str(self._scope),
            timestamp=datetime.now()
        ))

    def collect_domain_events(self) -> List[object]:
        """
        Collect and return all domain events that have occurred.

        Returns:
            List of domain events
        """
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events

    def _validate_invariants(self) -> None:
        """
        Validate aggregate invariants.

        Business Rules:
        - System variables cannot have empty values (may be critical)
        - All components must be valid value objects
        """
        if self._scope == VariableScope.SYSTEM and self._value.is_empty:
            raise AggregateInvariantViolationError(
                "System environment variables cannot have empty values"
            )

    def _add_domain_event(self, event: object) -> None:
        """Add a domain event to the collection."""
        self._domain_events.append(event)

    def __str__(self) -> str:
        return f"{self._name}={self._value} ({self._scope})"

    def __repr__(self) -> str:
        return (
            f"EnvironmentVariable(id='{self._id}', "
            f"name={self._name!r}, value={self._value!r}, "
            f"scope={self._scope!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EnvironmentVariable):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)
