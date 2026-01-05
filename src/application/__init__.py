"""
Application Layer

Contains application services (use cases) that orchestrate domain operations.
This layer coordinates between the presentation layer and domain layer.

Application services:
- Are thin and focus on orchestration
- Handle cross-cutting concerns (transactions, security)
- Don't contain business logic (that's in the domain)
- Define the API for the presentation layer
"""

from .services import *

__all__ = []  # Will be populated as services are created
