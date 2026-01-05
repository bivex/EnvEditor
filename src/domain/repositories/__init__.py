"""
Repository Interfaces

Repository interfaces define contracts for data access.
The domain layer depends on these abstractions, not concrete implementations.
"""

from .environment_variable_repository import EnvironmentVariableRepository
from .environment_context_repository import EnvironmentContextRepository
from .audit_repository import AuditRepository
from .process_environment_repository import ProcessEnvironmentRepository

__all__ = [
    'EnvironmentVariableRepository',
    'EnvironmentContextRepository',
    'AuditRepository',
    'ProcessEnvironmentRepository'
]
