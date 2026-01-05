"""
Variable Domain Events

Events related to environment variable lifecycle changes.
These events enable loose coupling and can trigger side effects.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class VariableCreated:
    """
    Domain event fired when a new environment variable is created.

    This event can trigger:
    - Audit logging
    - Notification systems
    - Cache invalidation
    - Validation of dependent variables
    """
    variable_id: str
    name: str
    value: str
    scope: str
    timestamp: datetime


@dataclass(frozen=True)
class VariableUpdated:
    """
    Domain event fired when an environment variable is modified.

    This event can trigger:
    - Audit logging
    - Notification of dependent systems
    - Cache updates
    - Environment reload notifications
    """
    variable_id: str
    name: str
    old_value: str
    new_value: str
    scope: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class VariableDeleted:
    """
    Domain event fired when an environment variable is deleted.

    This event can trigger:
    - Audit logging
    - Cleanup of dependent configurations
    - Notification of affected systems
    - Cache invalidation
    """
    variable_id: str
    name: str
    value: str
    scope: str
    timestamp: datetime
