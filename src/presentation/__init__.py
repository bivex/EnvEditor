# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-05T01:22:25
# Last Updated: 2026-01-05T01:27:11
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""
Presentation Layer

Contains the PyQt GUI implementation and user interface components.
This layer handles user interactions and displays data from the application layer.

The presentation layer:
- Contains UI components and layouts
- Handles user input and events
- Displays data from application services
- Delegates business logic to application layer
- Follows MVP or MVVM patterns for separation of concerns
"""

from .main_window import MainWindow
from .variable_dialog import VariableDialog
from .process_investigation_dialog import ProcessInvestigationDialog

__all__ = [
    'MainWindow',
    'VariableDialog',
    'ProcessInvestigationDialog'
]
