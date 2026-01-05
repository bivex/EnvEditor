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
Variable Dialog - PyQt Dialog

Dialog for creating and editing environment variables.
Provides form inputs with validation.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QMessageBox, QComboBox, QGroupBox
)
from PyQt6.QtCore import Qt


class VariableDialog(QDialog):
    """
    Dialog for variable creation and editing.

    Features:
    - Name input with validation
    - Value input (multi-line for complex values)
    - Scope selection
    - Form validation
    """

    def __init__(
        self,
        title: str,
        name: str = "",
        value: str = "",
        scope: str = "user"
    ) -> None:
        """
        Initialize the variable dialog.

        Args:
            title: Dialog window title
            name: Initial variable name (for editing)
            value: Initial variable value (for editing)
            scope: Initial scope selection
        """
        super().__init__()

        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(500, 400)

        self.name_edit = None
        self.value_edit = None
        self.scope_combo = None

        self.init_ui(name, value, scope)

    def init_ui(self, name: str, value: str, scope: str) -> None:
        """Initialize the user interface."""
        layout = QVBoxLayout(self)

        # Variable details group
        details_group = QGroupBox("Variable Details")
        details_layout = QVBoxLayout(details_group)

        # Name input
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        self.name_edit = QLineEdit(name)
        self.name_edit.setPlaceholderText("Enter variable name")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        details_layout.addLayout(name_layout)

        # Scope selection
        scope_layout = QHBoxLayout()
        scope_label = QLabel("Scope:")
        self.scope_combo = QComboBox()
        self.scope_combo.addItems(["system", "user", "process"])
        self.scope_combo.setCurrentText(scope)
        scope_layout.addWidget(scope_label)
        scope_layout.addWidget(self.scope_combo)
        details_layout.addLayout(scope_layout)

        layout.addWidget(details_group)

        # Value input group
        value_group = QGroupBox("Variable Value")
        value_layout = QVBoxLayout(value_group)

        value_label = QLabel("Value:")
        self.value_edit = QTextEdit(value)
        self.value_edit.setPlaceholderText("Enter variable value")
        # Set minimum height for better usability
        self.value_edit.setMinimumHeight(100)

        value_layout.addWidget(value_label)
        value_layout.addWidget(self.value_edit)

        layout.addWidget(value_group)

        # Buttons
        button_layout = QHBoxLayout()

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDefault(True)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        # Connect validation
        self.name_edit.textChanged.connect(self.validate_input)
        self.value_edit.textChanged.connect(self.validate_input)

        # Initial validation
        self.validate_input()

    def validate_input(self) -> None:
        """Validate user input and update dialog state."""
        name = self.name_edit.text().strip()
        value = self.value_edit.toPlainText().strip()

        # Basic validation
        is_valid = bool(name and value)

        # Variable name validation (basic check)
        if name:
            # Check for valid identifier characters
            import re
            if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name):
                is_valid = False

        self.ok_button.setEnabled(is_valid)

        # Provide visual feedback
        if name and not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name):
            self.name_edit.setStyleSheet("border: 1px solid red;")
        else:
            self.name_edit.setStyleSheet("")

    def get_variable_data(self) -> tuple[str, str]:
        """
        Get the variable data from the dialog.

        Returns:
            Tuple of (name, value)
        """
        name = self.name_edit.text().strip()
        value = self.value_edit.toPlainText().strip()
        return name, value

    def accept(self) -> None:
        """Handle dialog acceptance with final validation."""
        name, value = self.get_variable_data()

        # Final validation
        if not name:
            QMessageBox.warning(self, "Invalid Input", "Variable name is required.")
            return

        if not value:
            QMessageBox.warning(self, "Invalid Input", "Variable value is required.")
            return

        # Variable name validation
        import re
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name):
            QMessageBox.warning(
                self, "Invalid Name",
                "Variable name must start with a letter or underscore "
                "and contain only alphanumeric characters and underscores."
            )
            return

        super().accept()
