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
