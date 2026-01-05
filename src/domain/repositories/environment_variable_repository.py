# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-05T01:16:34
# Last Updated: 2026-01-05T01:19:33
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""
EnvironmentVariableRepository Interface

Repository interface for EnvironmentVariable aggregate access.
Defines the contract for persisting and retrieving environment variables.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Set

from ..entities import EnvironmentVariable
from ..value_objects import VariableName, VariableScope


class EnvironmentVariableRepository(ABC):
    """
    Repository interface for EnvironmentVariable aggregates.

    This interface defines the contract for:
    - Persisting environment variables
    - Retrieving variables by various criteria
    - Ensuring data consistency
    """

    @abstractmethod
    def save(self, variable: EnvironmentVariable) -> None:
        """
        Save an environment variable.

        Args:
            variable: The variable to save
        """
        pass

    @abstractmethod
    def find_by_id(self, variable_id: str) -> Optional[EnvironmentVariable]:
        """
        Find a variable by its ID.

        Args:
            variable_id: The unique identifier of the variable

        Returns:
            The variable if found, None otherwise
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def find_by_scope(self, scope: VariableScope) -> List[EnvironmentVariable]:
        """
        Find all variables in a specific scope.

        Args:
            scope: The scope to search in

        Returns:
            List of variables in the scope
        """
        pass

    @abstractmethod
    def find_all(self) -> List[EnvironmentVariable]:
        """
        Find all environment variables.

        Returns:
            List of all variables
        """
        pass

    @abstractmethod
    def delete(self, variable: EnvironmentVariable) -> None:
        """
        Delete an environment variable.

        Args:
            variable: The variable to delete
        """
        pass

    @abstractmethod
    def exists_by_name_and_scope(
        self,
        name: VariableName,
        scope: VariableScope
    ) -> bool:
        """
        Check if a variable exists with the given name and scope.

        Args:
            name: The variable name
            scope: The variable scope

        Returns:
            True if exists, False otherwise
        """
        pass

    @abstractmethod
    def count_by_scope(self, scope: VariableScope) -> int:
        """
        Count variables in a specific scope.

        Args:
            scope: The scope to count in

        Returns:
            Number of variables in the scope
        """
        pass

    @abstractmethod
    def find_names_by_scope(self, scope: VariableScope) -> Set[VariableName]:
        """
        Get all variable names in a specific scope.

        Args:
            scope: The scope to get names from

        Returns:
            Set of variable names in the scope
        """
        pass
