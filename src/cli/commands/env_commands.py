# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-05T01:55:16
# Last Updated: 2026-01-05T01:55:16
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""
Environment Variable CLI Commands

Handles CLI operations for environment variables.
"""

import sys
from typing import List

from ...application.services import VariableManagementService


def add_env_subparsers(subparsers, var_service: VariableManagementService):
    """Add environment variable subcommands to the parser."""

    # env list
    list_parser = subparsers.add_parser(
        'list',
        help='List environment variables'
    )
    list_parser.add_argument(
        '--scope',
        choices=['system', 'user', 'process'],
        default='user',
        help='Scope to list variables from (default: user)'
    )
    list_parser.add_argument(
        '--format',
        choices=['table', 'json', 'shell'],
        default='table',
        help='Output format (default: table)'
    )

    # env get <name>
    get_parser = subparsers.add_parser(
        'get',
        help='Get a specific environment variable'
    )
    get_parser.add_argument(
        'name',
        help='Variable name to get'
    )
    get_parser.add_argument(
        '--scope',
        choices=['system', 'user', 'process'],
        default='user',
        help='Scope to get variable from (default: user)'
    )

    # env set <name> <value>
    set_parser = subparsers.add_parser(
        'set',
        help='Set an environment variable'
    )
    set_parser.add_argument(
        'name',
        help='Variable name to set'
    )
    set_parser.add_argument(
        'value',
        help='Variable value to set'
    )
    set_parser.add_argument(
        '--scope',
        choices=['system', 'user', 'process'],
        default='user',
        help='Scope to set variable in (default: user)'
    )

    # env delete <name>
    delete_parser = subparsers.add_parser(
        'delete',
        help='Delete an environment variable'
    )
    delete_parser.add_argument(
        'name',
        help='Variable name to delete'
    )
    delete_parser.add_argument(
        '--scope',
        choices=['system', 'user', 'process'],
        default='user',
        help='Scope to delete variable from (default: user)'
    )


def handle_env_command(args, var_service: VariableManagementService) -> int:
    """Handle environment variable commands."""

    if args.list:
        return _handle_env_list(args, var_service)
    elif args.get:
        return _handle_env_get(args, var_service)
    elif args.set:
        return _handle_env_set(args, var_service)
    elif args.delete:
        return _handle_env_delete(args, var_service)
    else:
        print("Error: No subcommand specified", file=sys.stderr)
        return 1


def _handle_env_list(args, var_service: VariableManagementService) -> int:
    """Handle env list command."""
    try:
        if args.scope == 'user':
            variables = var_service.get_variables_by_scope('user')
        elif args.scope == 'system':
            variables = var_service.get_variables_by_scope('system')
        else:  # process
            variables = var_service.get_variables_by_scope('process')

        if not variables:
            print(f"No environment variables found in {args.scope} scope.")
            return 0

        if args.format == 'table':
            _print_env_table(variables)
        elif args.format == 'json':
            _print_env_json(variables)
        elif args.format == 'shell':
            _print_env_shell(variables)

        return 0

    except Exception as e:
        print(f"Error listing environment variables: {e}", file=sys.stderr)
        return 1


def _handle_env_get(args, var_service: VariableManagementService) -> int:
    """Handle env get command."""
    try:
        variable = var_service.get_variable_by_name_and_scope(args.name, args.scope)

        if variable:
            print(f"{args.name}={variable.value.value}")
            return 0
        else:
            print(f"Environment variable '{args.name}' not found in {args.scope} scope.", file=sys.stderr)
            return 1

    except Exception as e:
        print(f"Error getting environment variable: {e}", file=sys.stderr)
        return 1


def _handle_env_set(args, var_service: VariableManagementService) -> int:
    """Handle env set command."""
    try:
        # For CLI, we'll use a generic user ID since this is a demo
        user_id = "cli_user"

        # Check if variable already exists
        existing = var_service.get_variable_by_name_and_scope(args.name, args.scope)

        if existing:
            # Update existing variable
            var_service.update_variable(
                var_service.UpdateVariableCommand(
                    variable_id=existing.id,
                    value=args.value,
                    user_id=user_id
                )
            )
            print(f"Updated {args.name} in {args.scope} scope.")
        else:
            # Create new variable
            var_id = var_service.create_variable(
                var_service.CreateVariableCommand(
                    name=args.name,
                    value=args.value,
                    scope=args.scope,
                    user_id=user_id
                )
            )
            print(f"Created {args.name} in {args.scope} scope.")

        return 0

    except Exception as e:
        print(f"Error setting environment variable: {e}", file=sys.stderr)
        return 1


def _handle_env_delete(args, var_service: VariableManagementService) -> int:
    """Handle env delete command."""
    try:
        variable = var_service.get_variable_by_name_and_scope(args.name, args.scope)

        if not variable:
            print(f"Environment variable '{args.name}' not found in {args.scope} scope.", file=sys.stderr)
            return 1

        # For CLI, we'll use a generic user ID since this is a demo
        user_id = "cli_user"

        var_service.delete_variable(
            var_service.DeleteVariableCommand(
                variable_id=variable.id,
                user_id=user_id
            )
        )

        print(f"Deleted {args.name} from {args.scope} scope.")
        return 0

    except Exception as e:
        print(f"Error deleting environment variable: {e}", file=sys.stderr)
        return 1


def _print_env_table(variables):
    """Print environment variables in table format."""
    print(f"{'Name':<30} {'Value':<50} {'Scope':<10} {'Created':<19}")
    print("-" * 110)

    for var in variables:
        name = var.name.value[:29] if len(var.name.value) > 29 else var.name.value
        value = var.value.value[:49] if len(var.value.value) > 49 else var.value.value
        scope = str(var.scope)[:9]
        created = var.created_at.strftime("%Y-%m-%d %H:%M:%S")

        print(f"{name:<30} {value:<50} {scope:<10} {created:<19}")


def _print_env_json(variables):
    """Print environment variables in JSON format."""
    import json

    env_dict = {}
    for var in variables:
        env_dict[var.name.value] = {
            'value': var.value.value,
            'scope': str(var.scope),
            'created': var.created_at.isoformat(),
            'updated': var.updated_at.isoformat()
        }

    print(json.dumps(env_dict, indent=2))


def _print_env_shell(variables):
    """Print environment variables in shell export format."""
    for var in variables:
        # Escape quotes and special characters for shell
        safe_value = var.value.value.replace('"', '\\"').replace('`', '\\`').replace('$', '\\$')
        print(f'export {var.name.value}="{safe_value}"')
