#!/usr/bin/env python3
"""
Environment Variable Editor - Main Application

Entry point for both GUI and CLI modes.
Use --cli flag for command line interface, otherwise launches GUI.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def main() -> None:
    """
    Main application entry point.

    Checks command line arguments to determine GUI or CLI mode.
    """
    # Check if CLI mode is requested
    if len(sys.argv) > 1 and sys.argv[1] in ['--cli', 'cli']:
        # Remove the CLI flag from arguments
        sys.argv.pop(1)

        # Import and run CLI
        from cli.main import main as cli_main
        sys.exit(cli_main())

    # Default to GUI mode
    _run_gui()


def _run_gui() -> None:
    """Run the GUI application."""
    from PyQt6.QtWidgets import QApplication

    # Domain layer
    from domain.services import DefaultVariableValidationService, DefaultAuditService

    # Infrastructure layer
    from infrastructure.adapters.repositories import (
        InMemoryEnvironmentVariableRepository,
        InMemoryEnvironmentContextRepository,
        InMemoryAuditRepository
    )
    from infrastructure.adapters.system_process_adapter import SystemProcessAdapter

    # Application layer
    from application.services import (
        VariableManagementService,
        ContextManagementService,
        AuditQueryService,
        ProcessInvestigationService
    )

    # Presentation layer
    from presentation.main_window import MainWindow

    # Create infrastructure adapters (outermost layer)
    variable_repository = InMemoryEnvironmentVariableRepository()
    context_repository = InMemoryEnvironmentContextRepository()
    audit_repository = InMemoryAuditRepository()
    process_adapter = SystemProcessAdapter()

    # Create domain services
    validation_service = DefaultVariableValidationService()
    audit_service = DefaultAuditService()

    # Create application services
    variable_service = VariableManagementService(
        variable_repository=variable_repository,
        validation_service=validation_service,
        audit_service=audit_service
    )

    context_service = ContextManagementService(
        context_repository=context_repository,
        variable_repository=variable_repository
    )

    audit_query_service = AuditQueryService(
        audit_repository=audit_repository
    )

    process_service = ProcessInvestigationService(
        process_repository=process_adapter
    )

    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Environment Variable Editor")
    app.setApplicationVersion("1.0.0")

    # Create and show main window
    window = MainWindow(
        variable_service=variable_service,
        context_service=context_service,
        process_service=process_service
    )
    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
