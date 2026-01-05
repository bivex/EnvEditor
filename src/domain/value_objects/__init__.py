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
