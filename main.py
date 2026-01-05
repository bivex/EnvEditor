#!/usr/bin/env python3
"""
Environment Variable Editor - Main Application

Entry point for the PyQt GUI application.
Composes all dependencies and starts the application.
"""

import sys
from PyQt6.QtWidgets import QApplication

# Domain layer
from src.domain.services import DefaultVariableValidationService, DefaultAuditService

# Infrastructure layer
from src.infrastructure.adapters.repositories import (
    InMemoryEnvironmentVariableRepository,
    InMemoryEnvironmentContextRepository,
    InMemoryAuditRepository
)
from src.infrastructure.adapters.system_process_adapter import SystemProcessAdapter

# Application layer
from src.application.services import (
    VariableManagementService,
    ContextManagementService,
    AuditQueryService,
    ProcessInvestigationService
)

# Presentation layer
from src.presentation.main_window import MainWindow


def main() -> None:
    """
    Main application entry point.

    Sets up dependency injection and starts the GUI application.
    """
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
