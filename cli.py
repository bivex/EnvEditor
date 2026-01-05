
# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-05T01:55:34
# Last Updated: 2026-01-05T01:55:36
#
# Licensed under the MIT License.
# Commercial licensing available upon request.
"""
Environment Variable Editor - CLI Entry Point

Run this script to access the command line interface for environment variable management.
"""

import sys
from pathlib import Path

# Add src to path so imports work correctly
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    from cli.main import main
    sys.exit(main())
