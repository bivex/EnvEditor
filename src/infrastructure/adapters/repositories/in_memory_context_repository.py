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
In-Memory Environment Context Repository

In-memory implementation of EnvironmentContextRepository for testing and development.
"""

from typing import List, Optional, Set

from ....domain import (
    EnvironmentContext,
    ContextName,
    EnvironmentContextRepository
)


class InMemoryEnvironmentContextRepository(EnvironmentContextRepository):
    """
    In-memory implementation of EnvironmentContextRepository.
    """

    def __init__(self) -> None:
        """Initialize empty repository."""
        self._contexts: dict[str, EnvironmentContext] = {}
        self._contexts_by_name: dict[str, EnvironmentContext] = {}
        self._variable_to_contexts: dict[str, Set[str]] = {}

    def save(self, context: EnvironmentContext) -> None:
        """Save a context."""
        self._contexts[context.id] = context
        self._contexts_by_name[str(context.name)] = context

        # Update variable-to-contexts mapping
        for var_id in context.variable_ids:
            if var_id not in self._variable_to_contexts:
                self._variable_to_contexts[var_id] = set()
            self._variable_to_contexts[var_id].add(context.id)

    def find_by_id(self, context_id: str) -> Optional[EnvironmentContext]:
        """Find context by ID."""
        return self._contexts.get(context_id)

    def find_by_name(self, name: ContextName) -> Optional[EnvironmentContext]:
        """Find context by name."""
        return self._contexts_by_name.get(str(name))

    def find_all(self) -> List[EnvironmentContext]:
        """Find all contexts."""
        return list(self._contexts.values())

    def delete(self, context: EnvironmentContext) -> None:
        """Delete a context."""
        if context.id in self._contexts:
            del self._contexts[context.id]
            if str(context.name) in self._contexts_by_name:
                del self._contexts_by_name[str(context.name)]

            # Remove from variable-to-contexts mapping
            for var_id in context.variable_ids:
                if var_id in self._variable_to_contexts:
                    self._variable_to_contexts[var_id].discard(context.id)
                    if not self._variable_to_contexts[var_id]:
                        del self._variable_to_contexts[var_id]

    def exists_by_name(self, name: ContextName) -> bool:
        """Check if context exists by name."""
        return str(name) in self._contexts_by_name

    def find_contexts_containing_variable(self, variable_id: str) -> List[EnvironmentContext]:
        """Find contexts containing a variable."""
        context_ids = self._variable_to_contexts.get(variable_id, set())
        return [self._contexts[cid] for cid in context_ids if cid in self._contexts]

    def get_variable_ids_in_context(self, context_id: str) -> Set[str]:
        """Get variable IDs in a context."""
        context = self.find_by_id(context_id)
        return context.variable_ids if context else set()

    def add_variable_to_context(self, context_id: str, variable_id: str) -> None:
        """Add variable to context."""
        context = self.find_by_id(context_id)
        if context:
            # This would normally update the context entity
            # For in-memory, we'll track it here
            if variable_id not in self._variable_to_contexts:
                self._variable_to_contexts[variable_id] = set()
            self._variable_to_contexts[variable_id].add(context_id)

    def remove_variable_from_context(self, context_id: str, variable_id: str) -> None:
        """Remove variable from context."""
        if variable_id in self._variable_to_contexts:
            self._variable_to_contexts[variable_id].discard(context_id)
            if not self._variable_to_contexts[variable_id]:
                del self._variable_to_contexts[variable_id]
