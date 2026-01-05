
# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-05T01:55:34
# Last Updated: 2026-01-05T01:58:43
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
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(project_root))

def main():
    """Simple CLI implementation that avoids complex imports."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Environment Variable Editor - CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py env list
  python cli.py env get PATH
  python cli.py env set MY_VAR "value"
  python cli.py process list
        """
    )

    parser.add_argument(
        'command',
        choices=['env', 'process'],
        help='Command to run'
    )

    parser.add_argument(
        'subcommand',
        nargs='?',
        help='Subcommand'
    )

    parser.add_argument(
        'args',
        nargs='*',
        help='Additional arguments'
    )

    args = parser.parse_args()

    try:
        if args.command == 'env':
            handle_env_command(args.subcommand, args.args)
        elif args.command == 'process':
            handle_process_command(args.subcommand, args.args)
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0

def handle_env_command(subcommand, args):
    """Handle environment variable commands."""
    if subcommand == 'list':
        print("Environment Variables:")
        print("NAME=VALUE format (showing all)")
        print("-" * 80)
        # Show all environment variables
        import os
        for name, value in sorted(os.environ.items()):
            print(f"{name}={value}")
        print(f"\nTotal: {len(os.environ)} environment variables")
    elif subcommand == 'get' and args:
        import os
        var_name = args[0]
        value = os.environ.get(var_name)
        if value is not None:
            print(f"{var_name}={value}")
        else:
            print(f"Environment variable '{var_name}' not found")
    elif subcommand == 'set' and len(args) >= 2:
        import os
        var_name, var_value = args[0], args[1]
        os.environ[var_name] = var_value
        print(f"Set {var_name}={var_value}")
    else:
        print("Usage: python cli.py env <list|get|set> [args]")

def handle_process_command(subcommand, args):
    """Handle process commands."""
    if subcommand == 'list':
        print("Running Processes:")
        print("PID       Name              Command")
        print("-" * 80)
        # Show all accessible processes
        import psutil
        count = 0
        for proc in psutil.process_iter():
            try:
                pid = proc.pid
                name = proc.name()[:18] if proc.name() else 'unknown'
                cmdline = proc.cmdline()
                cmd = ' '.join(cmdline[:2]) if cmdline else ''
                cmd = cmd[:35] + '...' if len(cmd) > 35 else cmd
                print(f"{pid:<10} {name:<18} {cmd:<35}")
                count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        print(f"\nTotal: {count} accessible processes")
    else:
        print("Usage: python cli.py process <list> [args]")

if __name__ == "__main__":
    sys.exit(main())
