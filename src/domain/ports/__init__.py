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
Ports - Interfaces for External Dependencies

Ports define the interfaces that the application uses to communicate
with external systems. They follow the Dependency Inversion Principle.
"""

from .system_environment_port import SystemEnvironmentPort
from .file_system_port import FileSystemPort
from .user_interface_port import UserInterfacePort

__all__ = [
    'SystemEnvironmentPort',
    'FileSystemPort',
    'UserInterfacePort'
]
