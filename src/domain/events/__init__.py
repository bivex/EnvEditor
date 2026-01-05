"""
Domain Events

Domain events represent significant business occurrences.
They enable loose coupling between aggregates and external reactions.
"""

from .variable_events import VariableCreated, VariableUpdated, VariableDeleted
from .context_events import ContextCreated, ContextUpdated, ContextDeleted

__all__ = [
    'VariableCreated',
    'VariableUpdated',
    'VariableDeleted',
    'ContextCreated',
    'ContextUpdated',
    'ContextDeleted'
]
