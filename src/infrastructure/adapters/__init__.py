# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-05T01:28:31
# Last Updated: 2026-01-05T01:58:45
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""
Infrastructure Adapters

Concrete implementations of the ports defined in the domain layer.
These adapters handle external system integrations and persistence.
"""

from .repositories import *
from .system_process_adapter import SystemProcessAdapter

__all__ = [
    'SystemProcessAdapter'
]
