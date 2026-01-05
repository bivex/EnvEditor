"""
Main Window - PyQt GUI

Main application window for the Environment Variable Editor.
Provides the primary user interface for managing environment variables.
"""

import sys
from typing import Optional, List

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QLabel,
    QMessageBox, QSplitter, QTextEdit, QGroupBox, QStatusBar,
    QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction

from ..application.services import (
    VariableManagementService,
    ContextManagementService,
    ProcessInvestigationService
)
from ..domain.dtos import VariableDTO
from .variable_dialog import VariableDialog
from .process_investigation_dialog import ProcessInvestigationDialog


class MainWindow(QMainWindow):
    """
    Main application window for environment variable management.

    Features:
    - Variable listing with filtering by scope
    - Create, edit, delete operations
    - Context management
    - Audit trail viewing
    - Search and filter capabilities
    """

    def __init__(
        self,
        variable_service: VariableManagementService,
        context_service: ContextManagementService,
        process_service: ProcessInvestigationService
    ) -> None:
        """
        Initialize the main window.

        Args:
            variable_service: Application service for variable operations
            context_service: Application service for context operations
            process_service: Application service for process investigation
        """
        super().__init__()

        self.variable_service = variable_service
        self.context_service = context_service
        self.process_service = process_service

        self.current_scope = "user"  # Default scope
        self.variables: List[VariableDTO] = []

        self.init_ui()
        self.load_variables()

    def init_ui(self) -> None:
        """Initialize the user interface."""
        self.setWindowTitle("Environment Variable Editor")
        self.setGeometry(100, 100, 1000, 700)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)

        # Top control panel
        self.create_control_panel(layout)

        # Main content splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)

        # Left panel - Variable table
        self.create_variable_panel(splitter)

        # Right panel - Details and audit
        self.create_details_panel(splitter)

        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

        # Menu bar
        self.create_menu_bar()

        # Connect signals
        self.connect_signals()

    def create_control_panel(self, parent_layout: QVBoxLayout) -> None:
        """Create the top control panel."""
        control_group = QGroupBox("Controls")
        control_layout = QHBoxLayout(control_group)

        # Scope selector
        scope_label = QLabel("Scope:")
        self.scope_combo = QComboBox()
        self.scope_combo.addItems(["system", "user", "process"])
        self.scope_combo.setCurrentText(self.current_scope)
        control_layout.addWidget(scope_label)
        control_layout.addWidget(self.scope_combo)

        # Action buttons
        self.add_button = QPushButton("Add Variable")
        self.edit_button = QPushButton("Edit Variable")
        self.delete_button = QPushButton("Delete Variable")
        self.copy_markdown_button = QPushButton("Copy to Markdown")
        self.process_button = QPushButton("Investigate Processes")
        self.refresh_button = QPushButton("Refresh")

        control_layout.addWidget(self.add_button)
        control_layout.addWidget(self.edit_button)
        control_layout.addWidget(self.delete_button)
        control_layout.addWidget(self.copy_markdown_button)
        control_layout.addWidget(self.process_button)
        control_layout.addStretch()
        control_layout.addWidget(self.refresh_button)

        parent_layout.addWidget(control_group)

    def create_variable_panel(self, splitter: QSplitter) -> None:
        """Create the variable listing panel."""
        variable_group = QGroupBox("Environment Variables")
        variable_layout = QVBoxLayout(variable_group)

        # Variable table
        self.variable_table = QTableWidget()
        self.variable_table.setColumnCount(4)
        self.variable_table.setHorizontalHeaderLabels([
            "Name", "Value", "Created", "Updated"
        ])
        self.variable_table.setAlternatingRowColors(True)
        self.variable_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        variable_layout.addWidget(self.variable_table)
        splitter.addWidget(variable_group)

    def create_details_panel(self, splitter: QSplitter) -> None:
        """Create the details and audit panel."""
        details_group = QGroupBox("Details & Audit")
        details_layout = QVBoxLayout(details_group)

        # Variable details
        details_label = QLabel("Selected Variable Details:")
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(150)

        # Audit trail
        audit_label = QLabel("Recent Changes:")
        self.audit_text = QTextEdit()
        self.audit_text.setReadOnly(True)

        details_layout.addWidget(details_label)
        details_layout.addWidget(self.details_text)
        details_layout.addWidget(audit_label)
        details_layout.addWidget(self.audit_text)

        splitter.addWidget(details_group)

    def create_menu_bar(self) -> None:
        """Create the application menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("View")
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.load_variables)
        view_menu.addAction(refresh_action)

        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        process_action = QAction("Investigate Processes", self)
        process_action.triggered.connect(self.on_investigate_processes)
        tools_menu.addAction(process_action)

        # Help menu
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def connect_signals(self) -> None:
        """Connect UI signals to handlers."""
        self.scope_combo.currentTextChanged.connect(self.on_scope_changed)
        self.add_button.clicked.connect(self.on_add_variable)
        self.edit_button.clicked.connect(self.on_edit_variable)
        self.delete_button.clicked.connect(self.on_delete_variable)
        self.copy_markdown_button.clicked.connect(self.on_copy_variables_to_markdown)
        self.process_button.clicked.connect(self.on_investigate_processes)
        self.refresh_button.clicked.connect(self.load_variables)
        self.variable_table.itemSelectionChanged.connect(self.on_variable_selected)

    def on_scope_changed(self, scope: str) -> None:
        """Handle scope selection change."""
        self.current_scope = scope
        self.load_variables()

    def on_add_variable(self) -> None:
        """Handle add variable button click."""
        dialog = VariableDialog("Add Variable", scope=self.current_scope)
        if dialog.exec():
            name, value = dialog.get_variable_data()
            try:
                # Here we would call the application service
                # For now, just show a placeholder
                QMessageBox.information(
                    self, "Add Variable",
                    f"Would add variable: {name} = {value}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add variable: {e}")

    def on_edit_variable(self) -> None:
        """Handle edit variable button click."""
        current_row = self.variable_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a variable to edit.")
            return

        # Get selected variable data
        name_item = self.variable_table.item(current_row, 0)
        value_item = self.variable_table.item(current_row, 1)

        if name_item and value_item:
            dialog = VariableDialog(
                "Edit Variable",
                name=name_item.text(),
                value=value_item.text(),
                scope=self.current_scope
            )
            if dialog.exec():
                new_name, new_value = dialog.get_variable_data()
                try:
                    # Here we would call the application service
                    QMessageBox.information(
                        self, "Edit Variable",
                        f"Would update variable: {new_name} = {new_value}"
                    )
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update variable: {e}")

    def on_delete_variable(self) -> None:
        """Handle delete variable button click."""
        current_row = self.variable_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a variable to delete.")
            return

        name_item = self.variable_table.item(current_row, 0)
        if name_item:
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete variable '{name_item.text()}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                try:
                    # Here we would call the application service
                    QMessageBox.information(
                        self, "Delete Variable",
                        f"Would delete variable: {name_item.text()}"
                    )
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to delete variable: {e}")

    def on_copy_variables_to_markdown(self) -> None:
        """Copy current environment variables to markdown format."""
        if not self.variables:
            QMessageBox.warning(self, "No Data", "No environment variables available to copy.")
            return

        try:
            # Generate markdown content
            markdown_content = self._generate_variables_markdown()

            # Copy to clipboard
            from PyQt6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(markdown_content)

            QMessageBox.information(
                self, "Copied to Clipboard",
                f"Environment variables ({len(self.variables)} variables) have been copied to clipboard in Markdown format."
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to copy variables to markdown: {e}")

    def _generate_variables_markdown(self) -> str:
        """Generate markdown formatted text with environment variables."""
        from datetime import datetime

        lines = []
        lines.append("# Environment Variables Export")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Scope:** {self.current_scope}")
        lines.append(f"**Total Variables:** {len(self.variables)}")
        lines.append("")

        # Environment variables table
        lines.append("## Environment Variables")
        lines.append("")
        lines.append("| Name | Value | Created | Updated |")
        lines.append("|------|-------|---------|---------|")

        for variable in self.variables:
            # Escape pipe characters in values for markdown table
            value = variable.value.replace("|", "\\|") if variable.value else ""
            # Truncate long values for readability
            if len(value) > 50:
                value = value[:47] + "..."

            created_str = variable.created_at.strftime("%Y-%m-%d %H:%M")
            updated_str = variable.updated_at.strftime("%Y-%m-%d %H:%M")

            lines.append(f"| {variable.name} | {value} | {created_str} | {updated_str} |")

        lines.append("")

        # Statistics
        lines.append("## Statistics")
        lines.append("")

        # Count variables by creation date (recent vs old)
        now = datetime.now()
        recent_threshold = now.replace(hour=0, minute=0, second=0, microsecond=0)  # Today

        recent_count = sum(1 for v in self.variables if v.created_at >= recent_threshold)
        total_count = len(self.variables)

        lines.append(f"- **Total Variables:** {total_count}")
        lines.append(f"- **Recently Created:** {recent_count}")
        lines.append(f"- **Scope:** {self.current_scope}")

        # Most common value patterns (basic analysis)
        if self.variables:
            empty_count = sum(1 for v in self.variables if not v.value.strip())
            if empty_count > 0:
                lines.append(f"- **Empty Values:** {empty_count}")

        lines.append("")
        lines.append("---")
        lines.append("*Report generated by Environment Variable Editor*")

        return "\n".join(lines)

    def on_investigate_processes(self) -> None:
        """Handle process investigation button/menu click."""
        try:
            # Get current system variables for comparison
            system_vars = []
            if self.current_scope == "system":
                system_vars = self.variables

            # Create and show process investigation dialog
            dialog = ProcessInvestigationDialog(
                process_service=self.process_service,
                system_variables=system_vars
            )
            dialog.exec()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open process investigation: {e}")

    def on_variable_selected(self) -> None:
        """Handle variable selection change."""
        current_row = self.variable_table.currentRow()
        if current_row >= 0 and current_row < len(self.variables):
            variable = self.variables[current_row]
            self.show_variable_details(variable)
            self.show_variable_audit(variable)

    def load_variables(self) -> None:
        """Load and display variables for the current scope."""
        try:
            # Here we would call the application service
            # For now, create some sample data
            self.variables = self._get_sample_variables()
            self.display_variables()
            self.status_bar.showMessage(f"Loaded {len(self.variables)} variables")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load variables: {e}")

    def display_variables(self) -> None:
        """Display variables in the table."""
        self.variable_table.setRowCount(len(self.variables))

        for row, variable in enumerate(self.variables):
            self.variable_table.setItem(row, 0, QTableWidgetItem(variable.name))
            self.variable_table.setItem(row, 1, QTableWidgetItem(variable.value))
            self.variable_table.setItem(row, 2, QTableWidgetItem(
                variable.created_at.strftime("%Y-%m-%d %H:%M")
            ))
            self.variable_table.setItem(row, 3, QTableWidgetItem(
                variable.updated_at.strftime("%Y-%m-%d %H:%M")
            ))

        # Resize columns to content
        self.variable_table.resizeColumnsToContents()

    def show_variable_details(self, variable: VariableDTO) -> None:
        """Show detailed information about a variable."""
        details = f"""
Name: {variable.name}
Value: {variable.value}
Scope: {variable.scope}
Created: {variable.created_at}
Updated: {variable.updated_at}
ID: {variable.id}
        """.strip()
        self.details_text.setPlainText(details)

    def show_variable_audit(self, variable: VariableDTO) -> None:
        """Show audit trail for a variable."""
        # Here we would call the audit service
        # For now, show placeholder
        audit_info = f"Audit trail for variable '{variable.name}':\n\n"
        audit_info += "No audit data available (placeholder)"
        self.audit_text.setPlainText(audit_info)

    def show_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(
            self, "About Environment Variable Editor",
            "Environment Variable Editor v1.0\n\n"
            "A clean architecture PyQt application for managing\n"
            "environment variables with audit trails and contexts."
        )

    def _get_sample_variables(self) -> List[VariableDTO]:
        """Get sample variables for demonstration."""
        from datetime import datetime
        return [
            VariableDTO(
                id="1",
                name="PATH",
                value="/usr/bin:/bin:/usr/local/bin",
                scope=self.current_scope,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            VariableDTO(
                id="2",
                name="HOME",
                value="/Users/user",
                scope=self.current_scope,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            VariableDTO(
                id="3",
                name="USER",
                value="testuser",
                scope=self.current_scope,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
