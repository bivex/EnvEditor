"""
ProcessInvestigationService - Application Service

Use case implementations for process environment variable investigation.
Orchestrates process discovery and environment inspection.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from ...domain import (
    Process,
    ProcessEnvironment,
    EnvironmentVariable,
    ProcessEnvironmentRepository,
    ProcessId,
    ProcessName,
    DomainValidationError,
    EntityNotFoundError
)


@dataclass
class ProcessSummary:
    """Summary information about a process."""
    pid: int
    name: str
    command_line: str
    username: str
    parent_pid: Optional[int]
    variable_count: int = 0


@dataclass
class EnvironmentComparison:
    """Comparison between system and process environment variables."""
    variable_name: str
    system_value: Optional[str]
    process_value: Optional[str]
    is_inherited: bool
    matches_system: bool


@dataclass
class ProcessEnvironmentReport:
    """Complete report of a process's environment."""
    process: ProcessSummary
    all_variables: Dict[str, str]
    inherited_variables: List[EnvironmentComparison]
    process_specific_variables: Dict[str, str]


class ProcessInvestigationService:
    """
    Application service for process environment investigation use cases.

    This service orchestrates the domain operations for:
    - Discovering running processes
    - Inspecting process environments
    - Comparing process environments with system defaults
    - Generating environment reports
    """

    def __init__(
        self,
        process_repository: ProcessEnvironmentRepository
    ) -> None:
        """
        Initialize the service with dependencies.

        Args:
            process_repository: Repository for process and environment access
        """
        self._process_repository = process_repository

    def get_all_processes(self) -> List[ProcessSummary]:
        """
        Get summary information about all running processes.

        Returns:
            List of process summaries
        """
        try:
            processes = self._process_repository.get_all_processes()
            summaries = []
            for p in processes:
                try:
                    # Try to count environment variables for this process
                    variable_count = 0
                    try:
                        # p.process_id is already a ProcessId object, use it directly
                        process_env = self._process_repository.get_process_environment(p.process_id)
                        if process_env:
                            variable_count = process_env.variable_count
                    except Exception:
                        # If we can't access environment variables, variable_count remains 0
                        pass

                    summary = self._create_process_summary(p, variable_count)
                    summaries.append(summary)
                except Exception as e:
                    print(f"Error creating summary for process {p}: {e}")
                    continue
            return summaries
        except (OSError, PermissionError) as e:
            # Log the error but return empty list for UI to handle
            print(f"Failed to enumerate processes: {e}")
            return []
        except Exception as e:
            # Catch any other unexpected errors
            print(f"Unexpected error while loading processes: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_process_environment_report(
        self,
        pid: int,
        system_variables: Optional[List[EnvironmentVariable]] = None
    ) -> Optional[ProcessEnvironmentReport]:
        """
        Get a complete environment report for a specific process.

        Args:
            pid: The process ID
            system_variables: Optional list of system variables for comparison

        Returns:
            Complete environment report, or None if process not found
        """
        try:
            process_id = ProcessId(pid)
        except DomainValidationError:
            return None

        # Get process information
        process = self._process_repository.get_process_by_id(process_id)
        if not process:
            return None

        # Get process environment
        process_env = self._process_repository.get_process_environment(process_id)
        if not process_env:
            return None

        # Create summary
        summary = self._create_process_summary(process, process_env.variable_count)

        # Get all variables
        all_vars = process_env.get_environment_variables()

        # Compare with system variables if provided
        inherited_vars = []
        process_specific_vars = all_vars.copy()

        if system_variables:
            inherited_vars = process_env.get_inherited_variables(system_variables)
            process_specific_vars = process_env.get_process_specific_variables(system_variables)

        return ProcessEnvironmentReport(
            process=summary,
            all_variables=all_vars,
            inherited_variables=inherited_vars,
            process_specific_variables=process_specific_vars
        )

    def compare_process_with_system(
        self,
        pid: int,
        system_variables: List[EnvironmentVariable]
    ) -> List[EnvironmentComparison]:
        """
        Compare a process's environment with system defaults.

        Args:
            pid: The process ID
            system_variables: List of system environment variables

        Returns:
            List of environment comparisons
        """
        try:
            process_id = ProcessId(pid)
            process_env = self._process_repository.get_process_environment(process_id)

            if not process_env:
                return []

            comparisons = []
            for sys_var in system_variables:
                comparison = process_env.compare_with_system_variable(sys_var)
                comparisons.append(EnvironmentComparison(**comparison))

            return comparisons

        except (DomainValidationError, OSError, PermissionError):
            return []

    def find_processes_by_name(self, name: str) -> List[ProcessSummary]:
        """
        Find all processes with a specific name.

        Args:
            name: The process name to search for

        Returns:
            List of matching process summaries
        """
        try:
            processes = self._process_repository.get_processes_by_name(name)
            return [self._create_process_summary(p) for p in processes]
        except (OSError, PermissionError):
            return []

    def find_processes_by_user(self, username: str) -> List[ProcessSummary]:
        """
        Find all processes running under a specific user.

        Args:
            username: The username to filter by

        Returns:
            List of process summaries for that user
        """
        try:
            processes = self._process_repository.get_processes_by_user(username)
            return [self._create_process_summary(p) for p in processes]
        except (OSError, PermissionError):
            return []

    def get_process_tree(self, root_pid: int) -> Dict[int, List[ProcessSummary]]:
        """
        Get the process tree starting from a root process.

        Args:
            root_pid: The root process ID

        Returns:
            Dictionary mapping parent PIDs to lists of child process summaries
        """
        try:
            process_id = ProcessId(root_pid)
            tree = self._process_repository.get_process_tree(process_id)

            # Convert to summaries
            result = {}
            for parent_pid, children in tree.items():
                result[int(parent_pid)] = [
                    self._create_process_summary(child) for child in children
                ]

            return result

        except (DomainValidationError, OSError, PermissionError):
            return {}

    def refresh_process_data(self) -> None:
        """
        Refresh cached process information.

        This forces fresh enumeration of processes on next access.
        """
        self._process_repository.refresh_process_cache()

    def _create_process_summary(self, process: Process, variable_count: int = 0) -> ProcessSummary:
        """Create a ProcessSummary from a Process entity."""
        return ProcessSummary(
            pid=int(process.process_id),
            name=str(process.name),
            command_line=process.command_line,
            username=process.username,
            parent_pid=process.parent_pid,
            variable_count=variable_count
        )
