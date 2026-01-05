"""
Environment Variable Editor - Domain Layer

This package contains the domain model for environment variable management.
Following Domain-Driven Design principles with clean architecture.

The domain layer contains:
- Entities: Core business objects with identity and behavior
- Value Objects: Immutable objects defined by their attributes
- Domain Services: Business logic that doesn't belong to entities
- Repository Interfaces: Contracts for data access
- Domain Events: Significant business occurrences
- Exceptions: Domain-specific error conditions
"""

from .entities import *
from .value_objects import *
from .services import *
from .repositories import *
from .events import *
from .exceptions import *
from .dtos import *

__all__ = [
    # Entities
    'EnvironmentVariable',
    'EnvironmentContext',
    'AuditEntry',

    # Value Objects
    'VariableName',
    'VariableValue',
    'VariableScope',
    'ContextName',

    # Domain Services
    'VariableValidationService',
    'DefaultVariableValidationService',
    'AuditService',
    'DefaultAuditService',

    # Repository Interfaces
    'EnvironmentVariableRepository',
    'EnvironmentContextRepository',
    'AuditRepository',

    # Domain Events
    'VariableCreated',
    'VariableUpdated',
    'VariableDeleted',
    'ContextCreated',
    'ContextUpdated',
    'ContextDeleted',

    # Exceptions
    'DomainError',
    'DomainValidationError',
    'EntityNotFoundError',
    'DuplicateEntityError',
    'AggregateInvariantViolationError',
    'InsufficientPrivilegesError',
    'DomainServiceError'
]
