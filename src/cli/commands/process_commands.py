"""
Process CLI Commands

Handles CLI operations for process investigation.
"""

import sys
from typing import List

from ...application.services import ProcessInvestigationService


def add_process_subparsers(subparsers, process_service: ProcessInvestigationService):
    """Add process investigation subcommands to the parser."""

    # process list
    list_parser = subparsers.add_parser(
        'list',
        help='List running processes'
    )
    list_parser.add_argument(
        '--format',
        choices=['table', 'json'],
        default='table',
        help='Output format (default: table)'
    )
    list_parser.add_argument(
        '--user',
        help='Filter by username'
    )

    # process env <pid>
    env_parser = subparsers.add_parser(
        'env',
        help='Get environment variables from a specific process'
    )
    env_parser.add_argument(
        'pid',
        type=int,
        help='Process ID to get environment from'
    )
    env_parser.add_argument(
        '--format',
        choices=['table', 'json', 'shell'],
        default='table',
        help='Output format (default: table)'
    )

    # process info <pid>
    info_parser = subparsers.add_parser(
        'info',
        help='Get detailed information about a specific process'
    )
    info_parser.add_argument(
        'pid',
        type=int,
        help='Process ID to get information about'
    )


def handle_process_command(args, process_service: ProcessInvestigationService) -> int:
    """Handle process commands."""

    if hasattr(args, 'list') and args.list:
        return _handle_process_list(args, process_service)
    elif hasattr(args, 'env') and args.env:
        return _handle_process_env(args, process_service)
    elif hasattr(args, 'info') and args.info:
        return _handle_process_info(args, process_service)
    else:
        print("Error: No subcommand specified", file=sys.stderr)
        return 1


def _handle_process_list(args, process_service: ProcessInvestigationService) -> int:
    """Handle process list command."""
    try:
        if args.user:
            processes = process_service.find_processes_by_user(args.user)
        else:
            processes = process_service.get_all_processes()

        if not processes:
            print("No processes found.")
            return 0

        if args.format == 'table':
            _print_process_table(processes)
        elif args.format == 'json':
            _print_process_json(processes)

        return 0

    except Exception as e:
        print(f"Error listing processes: {e}", file=sys.stderr)
        return 1


def _handle_process_env(args, process_service: ProcessInvestigationService) -> int:
    """Handle process env command."""
    try:
        report = process_service.get_process_environment_report(args.pid)

        if not report:
            print(f"Could not access environment for process {args.pid}. It may not exist or access may be denied.", file=sys.stderr)
            return 1

        if not report.all_variables:
            print(f"Process {args.pid} has no accessible environment variables.")
            return 0

        if args.format == 'table':
            _print_env_table(report.all_variables)
        elif args.format == 'json':
            _print_env_json(report.all_variables)
        elif args.format == 'shell':
            _print_env_shell(report.all_variables)

        return 0

    except Exception as e:
        print(f"Error getting process environment: {e}", file=sys.stderr)
        return 1


def _handle_process_info(args, process_service: ProcessInvestigationService) -> int:
    """Handle process info command."""
    try:
        processes = process_service.get_all_processes()
        process = next((p for p in processes if p.pid == args.pid), None)

        if not process:
            print(f"Process {args.pid} not found.", file=sys.stderr)
            return 1

        print(f"Process Information:")
        print(f"  PID: {process.pid}")
        print(f"  Name: {process.name}")
        print(f"  Command: {process.command_line}")
        print(f"  User: {process.username}")
        print(f"  Parent PID: {process.parent_pid}")
        print(f"  Variables: {process.variable_count}")

        return 0

    except Exception as e:
        print(f"Error getting process information: {e}", file=sys.stderr)
        return 1


def _print_process_table(processes):
    """Print processes in table format."""
    print(f"{'PID':<8} {'Name':<25} {'Command':<50} {'User':<15} {'Vars':<5}")
    print("-" * 105)

    for proc in processes[:50]:  # Limit to first 50 for readability
        pid = str(proc.pid)[:7]
        name = proc.name[:24] if len(proc.name) > 24 else proc.name
        cmd = proc.command_line[:49] if len(proc.command_line) > 49 else proc.command_line
        user = proc.username[:14] if len(proc.username) > 14 else proc.username
        vars_count = str(proc.variable_count)[:4]

        print(f"{pid:<8} {name:<25} {cmd:<50} {user:<15} {vars_count:<5}")

    if len(processes) > 50:
        print(f"\n... and {len(processes) - 50} more processes")


def _print_process_json(processes):
    """Print processes in JSON format."""
    import json

    process_list = []
    for proc in processes:
        process_list.append({
            'pid': proc.pid,
            'name': proc.name,
            'command_line': proc.command_line,
            'username': proc.username,
            'parent_pid': proc.parent_pid,
            'variable_count': proc.variable_count
        })

    print(json.dumps(process_list, indent=2))


def _print_env_table(env_vars):
    """Print environment variables in table format."""
    print(f"{'Variable':<30} {'Value':<50}")
    print("-" * 81)

    for name, value in list(env_vars.items())[:50]:  # Limit for readability
        var_name = name[:29] if len(name) > 29 else name
        var_value = value[:49] if len(value) > 49 else value
        print(f"{var_name:<30} {var_value:<50}")

    if len(env_vars) > 50:
        print(f"\n... and {len(env_vars) - 50} more variables")


def _print_env_json(env_vars):
    """Print environment variables in JSON format."""
    import json
    print(json.dumps(env_vars, indent=2))


def _print_env_shell(env_vars):
    """Print environment variables in shell export format."""
    for name, value in env_vars.items():
        # Escape quotes and special characters for shell
        safe_value = value.replace('"', '\\"').replace('`', '\\`').replace('$', '\\$')
        print(f'export {name}="{safe_value}"')
