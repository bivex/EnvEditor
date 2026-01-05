"""
VariableValidationService Domain Service

Domain service for validating environment variables against system constraints
and business rules that require external knowledge.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

from ..value_objects import VariableName, VariableValue, VariableScope
from ..entities import EnvironmentVariable
from ..exceptions import DomainValidationError


class VariableValidationService(ABC):
    """
    Domain service for environment variable validation.

    This service encapsulates validation logic that requires:
    - Knowledge of system constraints
    - Access to external validation rules
    - Complex business rule evaluation
    """

    @abstractmethod
    def validate_variable(
        self,
        name: VariableName,
        value: VariableValue,
        scope: VariableScope
    ) -> None:
        """
        Validate an environment variable against all business rules.

        Args:
            name: The variable name to validate
            value: The variable value to validate
            scope: The variable scope

        Raises:
            DomainValidationError: If validation fails
        """
        pass

    @abstractmethod
    def validate_variable_uniqueness(
        self,
        variable: EnvironmentVariable,
        existing_variables: List[EnvironmentVariable]
    ) -> None:
        """
        Validate that a variable is unique within its scope.

        Args:
            variable: The variable to check
            existing_variables: List of existing variables in the same scope

        Raises:
            DomainValidationError: If uniqueness constraint is violated
        """
        pass

    @abstractmethod
    def get_validation_rules(self, scope: VariableScope) -> Dict[str, Any]:
        """
        Get validation rules applicable to a specific scope.

        Args:
            scope: The variable scope

        Returns:
            Dictionary of validation rules
        """
        pass


class DefaultVariableValidationService(VariableValidationService):
    """
    Default implementation of VariableValidationService.

    Contains standard validation rules that don't require external dependencies.
    """

    def validate_variable(
        self,
        name: VariableName,
        value: VariableValue,
        scope: VariableScope
    ) -> None:
        """
        Validate variable using built-in business rules.
        """
        # System scope has stricter rules
        if scope == VariableScope.SYSTEM:
            self._validate_system_variable(name, value)
        elif scope == VariableScope.USER:
            self._validate_user_variable(name, value)
        else:  # PROCESS scope
            self._validate_process_variable(name, value)

    def validate_variable_uniqueness(
        self,
        variable: EnvironmentVariable,
        existing_variables: List[EnvironmentVariable]
    ) -> None:
        """
        Check uniqueness within the same scope.
        """
        for existing in existing_variables:
            if (existing.name == variable.name and
                existing.scope == variable.scope and
                existing.id != variable.id):
                raise DomainValidationError(
                    f"Variable '{variable.name}' already exists in {variable.scope} scope"
                )

    def get_validation_rules(self, scope: VariableScope) -> Dict[str, Any]:
        """
        Get validation rules for the scope.
        """
        base_rules = {
            "name_pattern": r'^[A-Za-z_][A-Za-z0-9_]*$',
            "max_name_length": 255,
            "max_value_length": 32767
        }

        if scope == VariableScope.SYSTEM:
            base_rules.update({
                "requires_value": True,
                "restricted_names": ["PATH", "HOME", "USER", "SHELL"]
            })

        return base_rules

    def _validate_system_variable(self, name: VariableName, value: VariableValue) -> None:
        """Validate system scope specific rules."""
        restricted_names = ["PATH", "HOME", "USER", "SHELL"]
        if str(name).upper() in restricted_names:
            raise DomainValidationError(
                f"System variable '{name}' is restricted and cannot be modified"
            )

        if value.is_empty:
            raise DomainValidationError(
                "System variables cannot have empty values"
            )

    def _validate_user_variable(self, name: VariableName, value: VariableValue) -> None:
        """Validate user scope specific rules."""
        # User variables have fewer restrictions
        pass

    def _validate_process_variable(self, name: VariableName, value: VariableValue) -> None:
        """Validate process scope specific rules."""
        # Process variables have the fewest restrictions
        pass
