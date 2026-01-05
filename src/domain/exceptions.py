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
Domain Exceptions

Custom exceptions for domain-specific error conditions.
Following the principle of explicit error handling and clear contracts.
"""


class DomainError(Exception):
    """
    Base class for all domain-related errors.

    Domain errors represent business rule violations and
    should be handled explicitly by application services.
    """
    pass


class DomainValidationError(DomainError):
    """
    Raised when domain validation rules are violated.

    This includes invalid value objects, entity invariants, etc.
    """
    pass


class EntityNotFoundError(DomainError):
    """
    Raised when a requested entity is not found.

    This is different from technical NotFound errors as it
    represents a business-level concern.
    """
    pass


class DuplicateEntityError(DomainError):
    """
    Raised when attempting to create an entity that already exists.

    Used for enforcing uniqueness constraints in the domain.
    """
    pass


class AggregateInvariantViolationError(DomainError):
    """
    Raised when an aggregate invariant is violated.

    Aggregate invariants must be maintained across operations
    on the aggregate.
    """
    pass


class InsufficientPrivilegesError(DomainError):
    """
    Raised when an operation requires privileges that are not available.

    Used for authorization checks in the domain layer.
    """
    pass


class DomainServiceError(DomainError):
    """
    Raised when a domain service operation fails.

    Domain services encapsulate business logic that doesn't
    naturally fit within entities.
    """
    pass
