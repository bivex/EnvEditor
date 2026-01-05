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
