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
Domain Value Objects for Environment Variable Management

Value objects are immutable and defined by their attributes.
They encapsulate validation logic and business rules.
"""

from .variable_name import VariableName
from .variable_value import VariableValue
from .variable_scope import VariableScope
from .context_name import ContextName
from .process_id import ProcessId
from .process_name import ProcessName

__all__ = [
    'VariableName',
    'VariableValue',
    'VariableScope',
    'ContextName',
    'ProcessId',
    'ProcessName'
]
