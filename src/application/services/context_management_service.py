"""
ContextManagementService - Application Service

Use case implementations for environment context management.
Orchestrates domain operations for context CRUD operations.
"""

from typing import List, Optional
from dataclasses import dataclass

from ...domain import (
    EnvironmentContext,
    ContextName,
    EnvironmentContextRepository,
    EnvironmentVariableRepository,
    DomainValidationError,
    EntityNotFoundError
)


@dataclass
class CreateContextCommand:
    """Command for creating a new environment context."""
    name: str
    description: str
    user_id: str


@dataclass
class UpdateContextCommand:
    """Command for updating an existing environment context."""
    context_id: str
    description: str
    user_id: str


@dataclass
class DeleteContextCommand:
    """Command for deleting an environment context."""
    context_id: str
    user_id: str


@dataclass
class AddVariableToContextCommand:
    """Command for adding a variable to a context."""
    context_id: str
    variable_id: str
    user_id: str


@dataclass
class RemoveVariableFromContextCommand:
    """Command for removing a variable from a context."""
    context_id: str
    variable_id: str
    user_id: str


class ContextManagementService:
    """
    Application service for environment context management use cases.

    This service orchestrates the domain operations for:
    - Creating and managing environment contexts
    - Adding/removing variables from contexts
    - Retrieving context information
    """

    def __init__(
        self,
        context_repository: EnvironmentContextRepository,
        variable_repository: EnvironmentVariableRepository
    ) -> None:
        """
        Initialize the service with dependencies.

        Args:
            context_repository: Repository for context persistence
            variable_repository: Repository for variable access
        """
        self._context_repository = context_repository
        self._variable_repository = variable_repository

    def create_context(self, command: CreateContextCommand) -> str:
        """
        Create a new environment context.

        Args:
            command: Command containing context creation data

        Returns:
            The ID of the created context

        Raises:
            DomainValidationError: If the context data is invalid
        """
        # Parse and validate input
        try:
            name = ContextName(command.name)
        except ValueError as e:
            raise DomainValidationError(f"Invalid context name: {e}")

        # Check for uniqueness
        if self._context_repository.exists_by_name(name):
            raise DomainValidationError(f"Context '{name}' already exists")

        # Create the context
        context = EnvironmentContext(name, command.description)

        # Save to repository
        self._context_repository.save(context)

        return context.id

    def update_context(self, command: UpdateContextCommand) -> None:
        """
        Update an existing environment context.

        Args:
            command: Command containing update data

        Raises:
            EntityNotFoundError: If the context doesn't exist
        """
        # Find the context
        context = self._context_repository.find_by_id(command.context_id)
        if not context:
            raise EntityNotFoundError(f"Context with ID {command.context_id} not found")

        # Update the context
        context.update_description(command.description)

        # Save changes
        self._context_repository.save(context)

    def delete_context(self, command: DeleteContextCommand) -> None:
        """
        Delete an environment context.

        Args:
            command: Command containing deletion data

        Raises:
            EntityNotFoundError: If the context doesn't exist
        """
        # Find the context
        context = self._context_repository.find_by_id(command.context_id)
        if not context:
            raise EntityNotFoundError(f"Context with ID {command.context_id} not found")

        # Mark for deletion (records domain event)
        context.mark_for_deletion()

        # Delete from repository
        self._context_repository.delete(context)

    def add_variable_to_context(self, command: AddVariableToContextCommand) -> None:
        """
        Add a variable to an environment context.

        Args:
            command: Command containing the operation data

        Raises:
            EntityNotFoundError: If context or variable doesn't exist
        """
        # Find the context
        context = self._context_repository.find_by_id(command.context_id)
        if not context:
            raise EntityNotFoundError(f"Context with ID {command.context_id} not found")

        # Find the variable
        variable = self._variable_repository.find_by_id(command.variable_id)
        if not variable:
            raise EntityNotFoundError(f"Variable with ID {command.variable_id} not found")

        # Add variable to context
        context.add_variable(variable)

        # Save changes
        self._context_repository.save(context)

    def remove_variable_from_context(self, command: RemoveVariableFromContextCommand) -> None:
        """
        Remove a variable from an environment context.

        Args:
            command: Command containing the operation data

        Raises:
            EntityNotFoundError: If context or variable doesn't exist
        """
        # Find the context
        context = self._context_repository.find_by_id(command.context_id)
        if not context:
            raise EntityNotFoundError(f"Context with ID {command.context_id} not found")

        # Find the variable
        variable = self._variable_repository.find_by_id(command.variable_id)
        if not variable:
            raise EntityNotFoundError(f"Variable with ID {command.variable_id} not found")

        # Remove variable from context
        context.remove_variable(variable)

        # Save changes
        self._context_repository.save(context)

    def get_context(self, context_id: str) -> Optional[EnvironmentContext]:
        """
        Get a specific environment context.

        Args:
            context_id: The ID of the context to retrieve

        Returns:
            The context if found, None otherwise
        """
        return self._context_repository.find_by_id(context_id)

    def get_context_by_name(self, name: str) -> Optional[EnvironmentContext]:
        """
        Get a context by name.

        Args:
            name: The context name

        Returns:
            The context if found, None otherwise
        """
        try:
            context_name = ContextName(name)
            return self._context_repository.find_by_name(context_name)
        except DomainValidationError:
            return None

    def get_all_contexts(self) -> List[EnvironmentContext]:
        """
        Get all environment contexts.

        Returns:
            List of all contexts
        """
        return self._context_repository.find_all()

    def get_contexts_containing_variable(self, variable_id: str) -> List[EnvironmentContext]:
        """
        Get all contexts that contain a specific variable.

        Args:
            variable_id: The ID of the variable

        Returns:
            List of contexts containing the variable
        """
        return self._context_repository.find_contexts_containing_variable(variable_id)
