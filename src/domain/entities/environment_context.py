# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-05T01:19:28
# Last Updated: 2026-01-05T01:19:33
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""
EnvironmentContext Entity

Aggregate root representing a named collection of environment variables.
Manages relationships between variables and provides context-specific operations.
"""

import uuid
from datetime import datetime
from typing import Set, Dict, List, Optional

from ..value_objects import ContextName, VariableName
from ..events import ContextCreated, ContextUpdated, ContextDeleted
from ..exceptions import DomainValidationError, AggregateInvariantViolationError
from .environment_variable import EnvironmentVariable


class EnvironmentContext:
    """
    Environment Context Entity - Aggregate Root

    Represents a named collection of environment variables for a specific purpose
    (e.g., "Development", "Production", "Testing").

    Business Invariants:
    - Context name must be unique
    - Can contain multiple variables with the same name but different scopes
    - Variables are referenced by ID, not contained within the aggregate
    """

    def __init__(
        self,
        name: ContextName,
        description: Optional[str] = None,
        context_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        """
        Initialize EnvironmentContext.

        Args:
            name: The context name
            description: Optional description of the context
            context_id: Optional ID, generated if not provided
            created_at: Optional creation timestamp
            updated_at: Optional last update timestamp
        """
        self._id = context_id or str(uuid.uuid4())
        self._name = name
        self._description = description or ""
        self._variable_ids: Set[str] = set()  # References to EnvironmentVariable IDs
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or self._created_at
        self._domain_events: List[object] = []

        # Validate aggregate invariants
        self._validate_invariants()

        # Record creation event
        if not context_id:  # Only for new contexts
            self._add_domain_event(ContextCreated(
                context_id=self._id,
                name=str(self._name),
                variable_count=len(self._variable_ids),
                timestamp=self._created_at
            ))

    @property
    def id(self) -> str:
        """Get the unique identifier of this context."""
        return self._id

    @property
    def name(self) -> ContextName:
        """Get the context name."""
        return self._name

    @property
    def description(self) -> str:
        """Get the context description."""
        return self._description

    @property
    def variable_ids(self) -> Set[str]:
        """Get the set of variable IDs in this context."""
        return self._variable_ids.copy()

    @property
    def variable_count(self) -> int:
        """Get the number of variables in this context."""
        return len(self._variable_ids)

    @property
    def created_at(self) -> datetime:
        """Get the creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Get the last update timestamp."""
        return self._updated_at

    def update_description(self, description: str) -> None:
        """
        Update the context description.

        Args:
            description: New description for the context
        """
        if description == self._description:
            return  # No change needed

        self._description = description
        self._updated_at = datetime.now()

        self._add_domain_event(ContextUpdated(
            context_id=self._id,
            name=str(self._name),
            variable_count=self.variable_count,
            timestamp=self._updated_at
        ))

    def add_variable(self, variable: EnvironmentVariable) -> None:
        """
        Add a variable to this context.

        Args:
            variable: The EnvironmentVariable to add

        Raises:
            AggregateInvariantViolationError: If variable is invalid for this context
        """
        if variable.id in self._variable_ids:
            return  # Already in context

        self._variable_ids.add(variable.id)
        self._updated_at = datetime.now()

        # Validate invariants after change
        self._validate_invariants()

        self._add_domain_event(ContextUpdated(
            context_id=self._id,
            name=str(self._name),
            variable_count=self.variable_count,
            timestamp=self._updated_at
        ))

    def remove_variable(self, variable: EnvironmentVariable) -> None:
        """
        Remove a variable from this context.

        Args:
            variable: The EnvironmentVariable to remove
        """
        if variable.id not in self._variable_ids:
            return  # Not in context

        self._variable_ids.remove(variable.id)
        self._updated_at = datetime.now()

        self._add_domain_event(ContextUpdated(
            context_id=self._id,
            name=str(self._name),
            variable_count=self.variable_count,
            timestamp=self._updated_at
        ))

    def contains_variable(self, variable: EnvironmentVariable) -> bool:
        """
        Check if this context contains the specified variable.

        Args:
            variable: The EnvironmentVariable to check

        Returns:
            True if the variable is in this context
        """
        return variable.id in self._variable_ids

    def mark_for_deletion(self) -> None:
        """
        Mark this context for deletion.

        This method records the deletion event but doesn't actually
        delete the entity (that's handled by the repository).
        """
        self._add_domain_event(ContextDeleted(
            context_id=self._id,
            name=str(self._name),
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
        - Description length should be reasonable
        """
        if len(self._description) > 1000:
            raise AggregateInvariantViolationError(
                "Context description cannot exceed 1000 characters"
            )

    def _add_domain_event(self, event: object) -> None:
        """Add a domain event to the collection."""
        self._domain_events.append(event)

    def __str__(self) -> str:
        return f"Context '{self._name}' ({self.variable_count} variables)"

    def __repr__(self) -> str:
        return (
            f"EnvironmentContext(id='{self._id}', "
            f"name={self._name!r}, variable_count={self.variable_count})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EnvironmentContext):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)
