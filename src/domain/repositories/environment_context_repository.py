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
EnvironmentContextRepository Interface

Repository interface for EnvironmentContext aggregate access.
Defines the contract for persisting and retrieving environment contexts.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Set

from ..entities import EnvironmentContext
from ..value_objects import ContextName


class EnvironmentContextRepository(ABC):
    """
    Repository interface for EnvironmentContext aggregates.

    This interface defines the contract for:
    - Persisting environment contexts
    - Retrieving contexts by various criteria
    - Managing context-variable relationships
    """

    @abstractmethod
    def save(self, context: EnvironmentContext) -> None:
        """
        Save an environment context.

        Args:
            context: The context to save
        """
        pass

    @abstractmethod
    def find_by_id(self, context_id: str) -> Optional[EnvironmentContext]:
        """
        Find a context by its ID.

        Args:
            context_id: The unique identifier of the context

        Returns:
            The context if found, None otherwise
        """
        pass

    @abstractmethod
    def find_by_name(self, name: ContextName) -> Optional[EnvironmentContext]:
        """
        Find a context by name.

        Args:
            name: The context name

        Returns:
            The context if found, None otherwise
        """
        pass

    @abstractmethod
    def find_all(self) -> List[EnvironmentContext]:
        """
        Find all environment contexts.

        Returns:
            List of all contexts
        """
        pass

    @abstractmethod
    def delete(self, context: EnvironmentContext) -> None:
        """
        Delete an environment context.

        Args:
            context: The context to delete
        """
        pass

    @abstractmethod
    def exists_by_name(self, name: ContextName) -> bool:
        """
        Check if a context exists with the given name.

        Args:
            name: The context name

        Returns:
            True if exists, False otherwise
        """
        pass

    @abstractmethod
    def find_contexts_containing_variable(self, variable_id: str) -> List[EnvironmentContext]:
        """
        Find all contexts that contain a specific variable.

        Args:
            variable_id: The ID of the variable

        Returns:
            List of contexts containing the variable
        """
        pass

    @abstractmethod
    def get_variable_ids_in_context(self, context_id: str) -> Set[str]:
        """
        Get all variable IDs in a specific context.

        Args:
            context_id: The context ID

        Returns:
            Set of variable IDs in the context
        """
        pass

    @abstractmethod
    def add_variable_to_context(self, context_id: str, variable_id: str) -> None:
        """
        Add a variable to a context.

        Args:
            context_id: The context ID
            variable_id: The variable ID to add
        """
        pass

    @abstractmethod
    def remove_variable_from_context(self, context_id: str, variable_id: str) -> None:
        """
        Remove a variable from a context.

        Args:
            context_id: The context ID
            variable_id: The variable ID to remove
        """
        pass
