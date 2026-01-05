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
