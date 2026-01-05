"""
VariableManagementService - Application Service

Use case implementations for environment variable management.
Orchestrates domain operations for variable CRUD operations.
"""

from typing import List, Optional
from dataclasses import dataclass

from ...domain import (
    EnvironmentVariable,
    VariableName,
    VariableValue,
    VariableScope,
    EnvironmentVariableRepository,
    VariableValidationService,
    AuditService,
    DomainValidationError,
    EntityNotFoundError
)


@dataclass
class CreateVariableCommand:
    """Command for creating a new environment variable."""
    name: str
    value: str
    scope: str
    user_id: str


@dataclass
class UpdateVariableCommand:
    """Command for updating an existing environment variable."""
    variable_id: str
    value: str
    user_id: str


@dataclass
class DeleteVariableCommand:
    """Command for deleting an environment variable."""
    variable_id: str
    user_id: str


class VariableManagementService:
    """
    Application service for environment variable management use cases.

    This service orchestrates the domain operations for:
    - Creating new environment variables
    - Updating existing variables
    - Deleting variables
    - Retrieving variables
    """

    def __init__(
        self,
        variable_repository: EnvironmentVariableRepository,
        validation_service: VariableValidationService,
        audit_service: AuditService
    ) -> None:
        """
        Initialize the service with dependencies.

        Args:
            variable_repository: Repository for variable persistence
            validation_service: Service for variable validation
            audit_service: Service for audit trail management
        """
        self._variable_repository = variable_repository
        self._validation_service = validation_service
        self._audit_service = audit_service

    def create_variable(self, command: CreateVariableCommand) -> str:
        """
        Create a new environment variable.

        Args:
            command: Command containing variable creation data

        Returns:
            The ID of the created variable

        Raises:
            DomainValidationError: If the variable data is invalid
        """
        # Parse and validate input
        try:
            name = VariableName(command.name)
            value = VariableValue(command.value)
            scope = VariableScope.from_string(command.scope)
        except ValueError as e:
            raise DomainValidationError(f"Invalid input data: {e}")

        # Validate business rules
        self._validation_service.validate_variable(name, value, scope)

        # Check for uniqueness
        if self._variable_repository.exists_by_name_and_scope(name, scope):
            raise DomainValidationError(
                f"Variable '{name}' already exists in {scope} scope"
            )

        # Create the variable
        variable = EnvironmentVariable(name, value, scope)

        # Save to repository
        self._variable_repository.save(variable)

        # Record audit trail
        self._audit_service.record_variable_creation(variable, command.user_id)

        return variable.id

    def update_variable(self, command: UpdateVariableCommand) -> None:
        """
        Update an existing environment variable.

        Args:
            command: Command containing update data

        Raises:
            EntityNotFoundError: If the variable doesn't exist
            DomainValidationError: If the new value is invalid
        """
        # Find the variable
        variable = self._variable_repository.find_by_id(command.variable_id)
        if not variable:
            raise EntityNotFoundError(f"Variable with ID {command.variable_id} not found")

        # Parse and validate new value
        try:
            new_value = VariableValue(command.value)
        except ValueError as e:
            raise DomainValidationError(f"Invalid value: {e}")

        # Validate business rules
        self._validation_service.validate_variable(variable.name, new_value, variable.scope)

        # Store old value for audit
        old_value = str(variable.value)

        # Update the variable
        variable.update_value(new_value)

        # Save changes
        self._variable_repository.save(variable)

        # Record audit trail
        self._audit_service.record_variable_update(variable, old_value, command.user_id)

    def delete_variable(self, command: DeleteVariableCommand) -> None:
        """
        Delete an environment variable.

        Args:
            command: Command containing deletion data

        Raises:
            EntityNotFoundError: If the variable doesn't exist
        """
        # Find the variable
        variable = self._variable_repository.find_by_id(command.variable_id)
        if not variable:
            raise EntityNotFoundError(f"Variable with ID {command.variable_id} not found")

        # Mark for deletion (records domain event)
        variable.mark_for_deletion()

        # Delete from repository
        self._variable_repository.delete(variable)

        # Record audit trail
        self._audit_service.record_variable_deletion(variable, command.user_id)

    def get_variable(self, variable_id: str) -> Optional[EnvironmentVariable]:
        """
        Get a specific environment variable.

        Args:
            variable_id: The ID of the variable to retrieve

        Returns:
            The variable if found, None otherwise
        """
        return self._variable_repository.find_by_id(variable_id)

    def get_variables_by_scope(self, scope: str) -> List[EnvironmentVariable]:
        """
        Get all variables in a specific scope.

        Args:
            scope: The scope to filter by

        Returns:
            List of variables in the scope
        """
        try:
            variable_scope = VariableScope.from_string(scope)
            return self._variable_repository.find_by_scope(variable_scope)
        except ValueError:
            return []

    def get_all_variables(self) -> List[EnvironmentVariable]:
        """
        Get all environment variables.

        Returns:
            List of all variables
        """
        return self._variable_repository.find_all()

    def get_variable_by_name_and_scope(
        self,
        name: str,
        scope: str
    ) -> Optional[EnvironmentVariable]:
        """
        Get a variable by name and scope.

        Args:
            name: The variable name
            scope: The variable scope

        Returns:
            The variable if found, None otherwise
        """
        try:
            variable_name = VariableName(name)
            variable_scope = VariableScope.from_string(scope)
            return self._variable_repository.find_by_name_and_scope(variable_name, variable_scope)
        except (ValueError, DomainValidationError):
            return None
