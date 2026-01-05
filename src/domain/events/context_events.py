"""
Context Domain Events

Events related to environment context lifecycle changes.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class ContextCreated:
    """
    Domain event fired when a new environment context is created.

    This event can trigger:
    - Audit logging
    - Context validation
    - UI updates
    """
    context_id: str
    name: str
    variable_count: int
    timestamp: datetime


@dataclass(frozen=True)
class ContextUpdated:
    """
    Domain event fired when an environment context is modified.

    This event can trigger:
    - Audit logging
    - Cache invalidation
    - UI updates
    """
    context_id: str
    name: str
    variable_count: int
    timestamp: datetime


@dataclass(frozen=True)
class ContextDeleted:
    """
    Domain event fired when an environment context is deleted.

    This event can trigger:
    - Audit logging
    - Cleanup operations
    - UI updates
    """
    context_id: str
    name: str
    timestamp: datetime
