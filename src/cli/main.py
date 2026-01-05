
# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-05T01:54:19
# Last Updated: 2026-01-05T01:58:45
#
# Licensed under the MIT License.
# Commercial licensing available upon request.
"""
Environment Variable Editor - Command Line Interface

Provides CLI access to environment variable management and process investigation.
"""

import sys
import argparse
from typing import List, Optional
from pathlib import Path

# Import modules - handle different import scenarios
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

try:
    # Try direct imports first
    from application.services import (
        VariableManagementService,
        ContextManagementService,
        ProcessInvestigationService
    )
    from infrastructure.adapters.repositories import (
        InMemoryEnvironmentVariableRepository,
        InMemoryEnvironmentContextRepository,
        InMemoryAuditRepository
    )
    from infrastructure.adapters.system_process_adapter import SystemProcessAdapter
    from domain.services import DefaultVariableValidationService, DefaultAuditService
    from cli.commands import env_commands, process_commands, export_commands
except ImportError as e:
    # If imports fail, provide helpful error message
    print(f"Import error: {e}", file=sys.stderr)
    print("This CLI needs to be run from the project root directory.", file=sys.stderr)
    print("Try: python cli.py <command>", file=sys.stderr)
    sys.exit(1)


class CLIApp:
    """Main CLI application class."""

    def __init__(self):
        """Initialize CLI application with dependencies."""
        # Initialize repositories
        self.var_repo = InMemoryEnvironmentVariableRepository()
        self.context_repo = InMemoryEnvironmentContextRepository()
        self.audit_repo = InMemoryAuditRepository()
        self.process_adapter = SystemProcessAdapter()

        # Initialize domain services
        self.validation_service = DefaultVariableValidationService()
        self.audit_service = DefaultAuditService()

        # Initialize application services
        self.var_service = VariableManagementService(
            self.var_repo, self.validation_service, self.audit_service
        )
        self.context_service = ContextManagementService(
            self.context_repo, self.var_repo
        )
        self.process_service = ProcessInvestigationService(
            self.process_adapter
        )

    def create_parser(self) -> argparse.ArgumentParser:
        """Create the main argument parser."""
        parser = argparse.ArgumentParser(
            description="Environment Variable Editor - CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # List all environment variables
  python -m src.cli.main env list

  # Get a specific environment variable
  python -m src.cli.main env get PATH

  # Set an environment variable
  python -m src.cli.main env set MY_VAR "my value"

  # List all running processes
  python -m src.cli.main process list

  # Get environment variables from a specific process
  python -m src.cli.main process env 1234

  # Export environment variables to file
  python -m src.cli.main export env --output env_vars.json

  # Export process information to markdown
  python -m src.cli.main export processes --output processes.md
            """
        )

        parser.add_argument(
            '--version', '-v',
            action='version',
            version=f'Environment Variable Editor CLI {__version__}'
        )

        # Create subparsers for different command groups
        subparsers = parser.add_subparsers(
            dest='command_group',
            help='Command group',
            metavar='GROUP'
        )

        # Environment variables commands
        env_parser = subparsers.add_parser(
            'env',
            help='Environment variable operations'
        )
        env_commands.add_env_subparsers(env_parser, self.var_service)

        # Process investigation commands
        process_parser = subparsers.add_parser(
            'process',
            help='Process investigation operations'
        )
        process_commands.add_process_subparsers(process_parser, self.process_service)

        # Export commands
        export_parser = subparsers.add_parser(
            'export',
            help='Export operations'
        )
        export_commands.add_export_subparsers(
            export_parser,
            self.var_service,
            self.process_service
        )

        return parser

    def run(self, args: Optional[List[str]] = None) -> int:
        """Run the CLI application."""
        parser = self.create_parser()

        if args is None:
            args = sys.argv[1:]

        parsed_args = parser.parse_args(args)

        if not hasattr(parsed_args, 'command_group') or parsed_args.command_group is None:
            parser.print_help()
            return 1

        try:
            # Dispatch to appropriate command handler
            if parsed_args.command_group == 'env':
                return env_commands.handle_env_command(parsed_args, self.var_service)
            elif parsed_args.command_group == 'process':
                return process_commands.handle_process_command(parsed_args, self.process_service)
            elif parsed_args.command_group == 'export':
                return export_commands.handle_export_command(
                    parsed_args, self.var_service, self.process_service
                )
            else:
                parser.print_help()
                return 1

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.", file=sys.stderr)
            return 130
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1


def main() -> int:
    """Main entry point for CLI."""
    app = CLIApp()
    return app.run()


if __name__ == '__main__':
    sys.exit(main())
