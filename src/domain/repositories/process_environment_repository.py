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
ProcessEnvironmentRepository Interface

Repository interface for ProcessEnvironment aggregate access.
Defines the contract for process environment investigation.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from ..entities import Process, ProcessEnvironment
from ..value_objects import ProcessId


class ProcessEnvironmentRepository(ABC):
    """
    Repository interface for ProcessEnvironment aggregates.

    This interface defines the contract for:
    - Discovering running processes
    - Retrieving process environment variables
    - Process inspection and monitoring
    """

    @abstractmethod
    def get_all_processes(self) -> List[Process]:
        """
        Get information about all currently running processes.

        Returns:
            List of Process entities representing running processes

        Raises:
            OSError: If process enumeration fails due to permissions
        """
        pass

    @abstractmethod
    def get_process_by_id(self, process_id: ProcessId) -> Optional[Process]:
        """
        Get information about a specific process by PID.

        Args:
            process_id: The process ID to look up

        Returns:
            Process entity if found and running, None otherwise
        """
        pass

    @abstractmethod
    def get_process_environment(self, process_id: ProcessId) -> Optional[ProcessEnvironment]:
        """
        Get the environment variables for a specific process.

        Args:
            process_id: The process ID

        Returns:
            ProcessEnvironment if process exists and accessible, None otherwise

        Raises:
            PermissionError: If access to process environment is denied
            OSError: If process inspection fails
        """
        pass

    @abstractmethod
    def get_processes_by_name(self, name: str) -> List[Process]:
        """
        Get all processes with a specific name.

        Args:
            name: The process name to search for

        Returns:
            List of matching Process entities
        """
        pass

    @abstractmethod
    def get_processes_by_user(self, username: str) -> List[Process]:
        """
        Get all processes running under a specific user.

        Args:
            username: The username to filter by

        Returns:
            List of Process entities for that user
        """
        pass

    @abstractmethod
    def is_process_running(self, process_id: ProcessId) -> bool:
        """
        Check if a process is currently running.

        Args:
            process_id: The process ID to check

        Returns:
            True if process is running, False otherwise
        """
        pass

    @abstractmethod
    def get_process_tree(self, root_process_id: ProcessId) -> Dict[ProcessId, List[Process]]:
        """
        Get the process tree starting from a root process.

        Args:
            root_process_id: The root process ID

        Returns:
            Dictionary mapping parent PIDs to lists of child processes
        """
        pass

    @abstractmethod
    def refresh_process_cache(self) -> None:
        """
        Refresh any cached process information.

        This method should clear any cached process data and
        force fresh enumeration on next access.
        """
        pass
