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
ProcessEnvironment Entity

Represents the environment variables of a specific process.
This aggregates the process information with its environment variables.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional

from ..value_objects import ProcessId, VariableName, VariableValue
from .process import Process
from .environment_variable import EnvironmentVariable


class ProcessEnvironment:
    """
    ProcessEnvironment Entity - Aggregate Root

    Represents the complete environment state of a running process.
    This includes both the process information and all its environment variables.

    Business Invariants:
    - Process must exist and be identified by PID
    - Environment variables are specific to this process
    - Snapshot represents a point-in-time capture
    """

    def __init__(
        self,
        process: Process,
        environment_variables: Dict[str, str],
        environment_id: Optional[str] = None,
        captured_at: Optional[datetime] = None
    ) -> None:
        """
        Initialize ProcessEnvironment.

        Args:
            process: The Process entity
            environment_variables: Dict of environment variable name -> value
            environment_id: Optional unique identifier
            captured_at: When the environment was captured
        """
        self._id = environment_id or str(uuid.uuid4())
        self._process = process
        self._environment_variables: Dict[VariableName, VariableValue] = {}
        self._captured_at = captured_at or datetime.now()

        # Convert and validate environment variables
        self._load_environment_variables(environment_variables)

        self._validate_invariants()

    @property
    def id(self) -> str:
        """Get the unique identifier of this process environment snapshot."""
        return self._id

    @property
    def process(self) -> Process:
        """Get the associated process."""
        return self._process

    @property
    def process_id(self) -> ProcessId:
        """Get the process ID."""
        return self._process.process_id

    @property
    def captured_at(self) -> datetime:
        """Get when this environment was captured."""
        return self._captured_at

    @property
    def variable_count(self) -> int:
        """Get the number of environment variables."""
        return len(self._environment_variables)

    def get_environment_variables(self) -> Dict[str, str]:
        """
        Get all environment variables as a dictionary.

        Returns:
            Dictionary mapping variable names to values
        """
        return {
            str(name): str(value)
            for name, value in self._environment_variables.items()
        }

    def get_variable(self, name: str) -> Optional[VariableValue]:
        """
        Get a specific environment variable by name.

        Args:
            name: The variable name

        Returns:
            The variable value if it exists, None otherwise
        """
        try:
            var_name = VariableName(name)
            return self._environment_variables.get(var_name)
        except Exception:
            return None

    def has_variable(self, name: str) -> bool:
        """
        Check if a specific environment variable exists.

        Args:
            name: The variable name

        Returns:
            True if the variable exists, False otherwise
        """
        try:
            var_name = VariableName(name)
            return var_name in self._environment_variables
        except Exception:
            return False

    def compare_with_system_variable(
        self,
        system_variable: EnvironmentVariable
    ) -> Dict[str, any]:
        """
        Compare a system variable with this process's version.

        Args:
            system_variable: The system environment variable to compare

        Returns:
            Dictionary with comparison results
        """
        process_value = self.get_variable(str(system_variable.name))

        return {
            'variable_name': str(system_variable.name),
            'system_value': str(system_variable.value),
            'process_value': str(process_value) if process_value else None,
            'is_inherited': process_value is not None,
            'matches_system': str(process_value) == str(system_variable.value) if process_value else False
        }

    def get_inherited_variables(self, system_variables: List[EnvironmentVariable]) -> List[Dict[str, any]]:
        """
        Get variables that are inherited from system defaults.

        Args:
            system_variables: List of system environment variables

        Returns:
            List of comparison dictionaries
        """
        comparisons = []
        for sys_var in system_variables:
            if self.has_variable(str(sys_var.name)):
                comparisons.append(self.compare_with_system_variable(sys_var))

        return comparisons

    def get_process_specific_variables(self, system_variables: List[EnvironmentVariable]) -> Dict[str, str]:
        """
        Get variables that are specific to this process (not inherited).

        Args:
            system_variables: List of system environment variables

        Returns:
            Dictionary of process-specific variables
        """
        system_names = {str(var.name) for var in system_variables}
        process_vars = self.get_environment_variables()

        return {
            name: value
            for name, value in process_vars.items()
            if name not in system_names
        }

    def _load_environment_variables(self, env_dict: Dict[str, str]) -> None:
        """Load and validate environment variables from dictionary."""
        for name_str, value_str in env_dict.items():
            try:
                name = VariableName(name_str)
                value = VariableValue(value_str)
                self._environment_variables[name] = value
            except Exception:
                # Skip invalid environment variables
                # In a real system, we might want to log these
                continue

    def _validate_invariants(self) -> None:
        """
        Validate aggregate invariants.

        Business Rules:
        - Process must be valid
        - Capture time should be reasonable
        """
        if self._captured_at < self._process.snapshot_time:
            # Environment captured before process snapshot - this might indicate stale data
            pass  # Could raise warning or log

    def __str__(self) -> str:
        return (
            f"ProcessEnvironment(pid={self._process.process_id}, "
            f"name='{self._process.name}', variables={self.variable_count})"
        )

    def __repr__(self) -> str:
        return (
            f"ProcessEnvironment(id='{self._id}', "
            f"process={self._process!r}, variable_count={self.variable_count})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProcessEnvironment):
            return False
        return (self._process == other._process and
                self._captured_at == other._captured_at)

    def __hash__(self) -> int:
        return hash((self._process, self._captured_at))
