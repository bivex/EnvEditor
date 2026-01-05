"""
Infrastructure Layer

Contains adapters that implement the ports defined in the domain layer.
This layer is responsible for external system integrations and persistence.

Adapters follow the Dependency Inversion Principle:
- Domain depends on ports (interfaces)
- Infrastructure implements ports (concrete classes)
- Application depends on domain abstractions

This layer contains:
- Repository implementations
- External system adapters
- Persistence mechanisms
- Configuration management
"""

from .adapters import *

__all__ = []  # Will be populated as adapters are created
