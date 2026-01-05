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
SystemEnvironmentPort - Port for System Environment Access

Interface for interacting with the operating system's environment variables.
This port abstracts away platform-specific details.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional

from ..value_objects import VariableName, VariableValue, VariableScope


class SystemEnvironmentPort(ABC):
    """
    Port for accessing and modifying system environment variables.

    This interface abstracts the operating system's environment variable
    management, allowing for different implementations on different platforms.
    """

    @abstractmethod
    def get_environment_variable(
        self,
        name: VariableName,
        scope: VariableScope
    ) -> Optional[VariableValue]:
        """
        Get the value of an environment variable from the system.

        Args:
            name: The variable name
            scope: The scope to read from

        Returns:
            The variable value if it exists, None otherwise
        """
        pass

    @abstractmethod
    def set_environment_variable(
        self,
        name: VariableName,
        value: VariableValue,
        scope: VariableScope
    ) -> None:
        """
        Set an environment variable in the system.

        Args:
            name: The variable name
            value: The variable value
            scope: The scope to write to

        Raises:
            PermissionError: If the operation requires elevated privileges
            OSError: If the system operation fails
        """
        pass

    @abstractmethod
    def delete_environment_variable(
        self,
        name: VariableName,
        scope: VariableScope
    ) -> None:
        """
        Delete an environment variable from the system.

        Args:
            name: The variable name
            scope: The scope to delete from

        Raises:
            PermissionError: If the operation requires elevated privileges
            OSError: If the system operation fails
        """
        pass

    @abstractmethod
    def get_all_environment_variables(
        self,
        scope: VariableScope
    ) -> Dict[str, str]:
        """
        Get all environment variables in a specific scope.

        Args:
            scope: The scope to read from

        Returns:
            Dictionary mapping variable names to values
        """
        pass

    @abstractmethod
    def requires_elevation(self, scope: VariableScope) -> bool:
        """
        Check if operations on this scope require elevated privileges.

        Args:
            scope: The scope to check

        Returns:
            True if elevation is required, False otherwise
        """
        pass

    @abstractmethod
    def get_scope_persistence_info(self, scope: VariableScope) -> Dict[str, str]:
        """
        Get information about how variables in this scope are persisted.

        Args:
            scope: The scope to get info for

        Returns:
            Dictionary with persistence information
        """
        pass
