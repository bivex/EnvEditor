"""
Domain Entities

Entities represent domain concepts with identity and lifecycle.
They enforce business invariants and encapsulate business logic.
"""

from .environment_variable import EnvironmentVariable
from .environment_context import EnvironmentContext
from .audit_entry import AuditEntry
from .process import Process
from .process_environment import ProcessEnvironment

__all__ = [
    'EnvironmentVariable',
    'EnvironmentContext',
    'AuditEntry',
    'Process',
    'ProcessEnvironment'
]
