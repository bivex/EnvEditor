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
In-Memory Environment Variable Repository

In-memory implementation of EnvironmentVariableRepository for testing and development.
Stores data in memory without persistence.
"""

from typing import List, Optional, Set, Dict

from ....domain import (
    EnvironmentVariable,
    VariableName,
    VariableScope,
    EnvironmentVariableRepository
)


class InMemoryEnvironmentVariableRepository(EnvironmentVariableRepository):
    """
    In-memory implementation of EnvironmentVariableRepository.

    This implementation stores variables in memory and is suitable for:
    - Testing
    - Development
    - Temporary storage during a session

    Note: Data is lost when the application restarts.
    """

    def __init__(self) -> None:
        """Initialize empty repository."""
        self._variables: Dict[str, EnvironmentVariable] = {}
        self._variables_by_name_scope: Dict[tuple, EnvironmentVariable] = {}

    def save(self, variable: EnvironmentVariable) -> None:
        """
        Save a variable to the repository.

        Args:
            variable: The variable to save
        """
        self._variables[variable.id] = variable
        key = (str(variable.name), variable.scope)
        self._variables_by_name_scope[key] = variable

    def find_by_id(self, variable_id: str) -> Optional[EnvironmentVariable]:
        """
        Find a variable by ID.

        Args:
            variable_id: The variable ID

        Returns:
            The variable if found, None otherwise
        """
        return self._variables.get(variable_id)

    def find_by_name_and_scope(
        self,
        name: VariableName,
        scope: VariableScope
    ) -> Optional[EnvironmentVariable]:
        """
        Find a variable by name and scope.

        Args:
            name: The variable name
            scope: The variable scope

        Returns:
            The variable if found, None otherwise
        """
        key = (str(name), scope)
        return self._variables_by_name_scope.get(key)

    def find_by_scope(self, scope: VariableScope) -> List[EnvironmentVariable]:
        """
        Find all variables in a scope.

        Args:
            scope: The scope to search

        Returns:
            List of variables in the scope
        """
        return [
            var for var in self._variables.values()
            if var.scope == scope
        ]

    def find_all(self) -> List[EnvironmentVariable]:
        """
        Find all variables.

        Returns:
            List of all variables
        """
        return list(self._variables.values())

    def delete(self, variable: EnvironmentVariable) -> None:
        """
        Delete a variable from the repository.

        Args:
            variable: The variable to delete
        """
        if variable.id in self._variables:
            del self._variables[variable.id]
            key = (str(variable.name), variable.scope)
            if key in self._variables_by_name_scope:
                del self._variables_by_name_scope[key]

    def exists_by_name_and_scope(
        self,
        name: VariableName,
        scope: VariableScope
    ) -> bool:
        """
        Check if a variable exists by name and scope.

        Args:
            name: The variable name
            scope: The variable scope

        Returns:
            True if exists, False otherwise
        """
        key = (str(name), scope)
        return key in self._variables_by_name_scope

    def count_by_scope(self, scope: VariableScope) -> int:
        """
        Count variables in a scope.

        Args:
            scope: The scope to count

        Returns:
            Number of variables in the scope
        """
        return len(self.find_by_scope(scope))

    def find_names_by_scope(self, scope: VariableScope) -> Set[VariableName]:
        """
        Get all variable names in a scope.

        Args:
            scope: The scope to get names from

        Returns:
            Set of variable names in the scope
        """
        return {
            var.name for var in self._variables.values()
            if var.scope == scope
        }
