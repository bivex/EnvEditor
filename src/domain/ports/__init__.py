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
