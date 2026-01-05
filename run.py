
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
Simple runner script for the Environment Variable Editor.

This script activates the virtual environment and runs the application.
"""

import os
import sys
import subprocess

def main():
    """Run the application with proper environment setup."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Check if virtual environment exists
    venv_dir = os.path.join(script_dir, 'venv')
    if not os.path.exists(venv_dir):
        print("Virtual environment not found. Please run setup first:")
        print("python3 -m venv venv")
        print("source venv/bin/activate")
        print("pip install -r requirements.txt")
        sys.exit(1)

    # Activate virtual environment and run
    activate_script = os.path.join(venv_dir, 'bin', 'activate')
    python_exe = os.path.join(venv_dir, 'bin', 'python')

    # Run the main application
    cmd = f"source {activate_script} && {python_exe} main.py"
    result = subprocess.run(cmd, shell=True, cwd=script_dir)

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
