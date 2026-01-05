"""
ProcessInvestigationDialog - PyQt Dialog

Dialog for investigating system processes and their environment variables.
Provides comprehensive process inspection capabilities.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QSplitter, QTableWidget,
    QTableWidgetItem, QTextEdit, QPushButton, QLabel, QLineEdit,
    QComboBox, QGroupBox, QProgressBar, QMessageBox, QTabWidget,
    QWidget, QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QClipboard
from typing import List, Dict, Optional
import time

from ..application.services import ProcessInvestigationService
from ..domain.entities import EnvironmentVariable


class ProcessLoaderThread(QThread):
    """Background thread for loading process information."""

    finished = pyqtSignal(list)  # Emits list of process summaries
    error = pyqtSignal(str)

    def __init__(self, service: ProcessInvestigationService):
        super().__init__()
        self.service = service

    def run(self):
        """Load process information in background."""
        try:
            processes = self.service.get_all_processes()
            self.finished.emit(processes)
        except Exception as e:
            self.error.emit(str(e))


class ProcessInvestigationDialog(QDialog):
    """
    Dialog for comprehensive process environment investigation.

    Features:
    - Process list with filtering and search
    - Process environment variable inspection
    - Comparison with system variables
    - Process tree visualization
    - Environment variable analysis
    """

    def __init__(
        self,
        process_service: ProcessInvestigationService,
        system_variables: Optional[List[EnvironmentVariable]] = None
    ) -> None:
        """
        Initialize the process investigation dialog.

        Args:
            process_service: Service for process investigation
            system_variables: Optional system variables for comparison
        """
        super().__init__()

        self.process_service = process_service
        self.system_variables = system_variables or []
        self.processes = []
        self.selected_pid = None

        self.setWindowTitle("Process Environment Investigation")
        self.setGeometry(200, 200, 1200, 800)
        self.setModal(True)

        self.init_ui()
        self.load_processes()

    def init_ui(self) -> None:
        """Initialize the user interface."""
        layout = QVBoxLayout(self)

        # Top controls
        self.create_controls(layout)

        # Progress bar for loading
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Main content splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)

        # Left panel - Process list
        self.create_process_panel(splitter)

        # Right panel - Details tabs
        self.create_details_panel(splitter)

        # Bottom buttons
        self.create_buttons(layout)

    def create_controls(self, parent_layout: QVBoxLayout) -> None:
        """Create top control panel."""
        controls_group = QGroupBox("Controls")
        controls_layout = QHBoxLayout(controls_group)

        # Search controls
        search_label = QLabel("Search:")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by name, PID, or command...")
        controls_layout.addWidget(search_label)
        controls_layout.addWidget(self.search_edit)

        # Filter controls
        filter_label = QLabel("Filter by user:")
        self.user_combo = QComboBox()
        self.user_combo.addItem("All Users", "")
        controls_layout.addWidget(filter_label)
        controls_layout.addWidget(self.user_combo)

        # Action buttons
        self.refresh_button = QPushButton("Refresh")
        self.inspect_button = QPushButton("Inspect Environment")
        self.inspect_button.setEnabled(False)

        controls_layout.addWidget(self.refresh_button)
        controls_layout.addWidget(self.inspect_button)

        parent_layout.addWidget(controls_group)

        # Connect signals
        self.search_edit.textChanged.connect(self.filter_processes)
        self.user_combo.currentTextChanged.connect(self.filter_processes)
        self.refresh_button.clicked.connect(self.load_processes)

    def create_process_panel(self, splitter: QSplitter) -> None:
        """Create the process list panel."""
        process_group = QGroupBox("Running Processes")
        process_layout = QVBoxLayout(process_group)

        # Process table
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(5)
        self.process_table.setHorizontalHeaderLabels([
            "PID", "Name", "Command Line", "User", "Variables"
        ])
        self.process_table.setAlternatingRowColors(True)
        self.process_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.process_table.setSortingEnabled(True)

        # Set column widths
        self.process_table.setColumnWidth(0, 80)   # PID
        self.process_table.setColumnWidth(1, 150)  # Name
        self.process_table.setColumnWidth(2, 300)  # Command
        self.process_table.setColumnWidth(3, 100)  # User
        self.process_table.setColumnWidth(4, 80)   # Variables

        process_layout.addWidget(self.process_table)
        splitter.addWidget(process_group)

        # Connect signals
        self.process_table.itemSelectionChanged.connect(self.on_process_selected)

    def create_details_panel(self, splitter: QSplitter) -> None:
        """Create the details panel with tabs."""
        details_group = QGroupBox("Process Details")
        details_layout = QVBoxLayout(details_group)

        # Tab widget for different views
        self.tab_widget = QTabWidget()

        # Environment variables tab
        self.env_tab = QWidget()
        self.create_environment_tab()
        self.tab_widget.addTab(self.env_tab, "Environment Variables")

        # Process info tab
        self.info_tab = QWidget()
        self.create_info_tab()
        self.tab_widget.addTab(self.info_tab, "Process Information")

        # Comparison tab
        self.compare_tab = QWidget()
        self.create_comparison_tab()
        self.tab_widget.addTab(self.compare_tab, "System Comparison")

        details_layout.addWidget(self.tab_widget)
        splitter.addWidget(details_group)

    def create_environment_tab(self) -> None:
        """Create the environment variables tab."""
        layout = QVBoxLayout(self.env_tab)

        # Environment table
        self.env_table = QTableWidget()
        self.env_table.setColumnCount(2)
        self.env_table.setHorizontalHeaderLabels(["Variable", "Value"])
        self.env_table.setAlternatingRowColors(True)
        self.env_table.setSortingEnabled(True)

        layout.addWidget(self.env_table)

    def create_info_tab(self) -> None:
        """Create the process information tab."""
        layout = QVBoxLayout(self.info_tab)

        # Process information display
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setFont(QFont("Monospace", 10))

        layout.addWidget(self.info_text)

    def create_comparison_tab(self) -> None:
        """Create the system comparison tab."""
        layout = QVBoxLayout(self.compare_tab)

        # Comparison table
        self.compare_table = QTableWidget()
        self.compare_table.setColumnCount(4)
        self.compare_table.setHorizontalHeaderLabels([
            "Variable", "System Value", "Process Value", "Status"
        ])
        self.compare_table.setAlternatingRowColors(True)
        self.compare_table.setSortingEnabled(True)

        layout.addWidget(self.compare_table)

    def create_buttons(self, parent_layout: QVBoxLayout) -> None:
        """Create bottom button panel."""
        button_layout = QHBoxLayout()

        self.copy_markdown_button = QPushButton("Copy to Markdown")
        self.copy_markdown_button.clicked.connect(self.copy_processes_to_markdown)
        self.copy_markdown_button.setEnabled(False)  # Enable after processes are loaded

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)

        button_layout.addWidget(self.copy_markdown_button)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)

        parent_layout.addLayout(button_layout)

    def load_processes(self) -> None:
        """Load and display process information."""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress

        # Start background loading
        self.loader_thread = ProcessLoaderThread(self.process_service)
        self.loader_thread.finished.connect(self.on_processes_loaded)
        self.loader_thread.error.connect(self.on_load_error)
        self.loader_thread.start()

    def on_processes_loaded(self, processes: List) -> None:
        """Handle successful process loading."""
        self.progress_bar.setVisible(False)
        self.processes = processes
        self.display_processes(processes)

        # Enable copy to markdown button
        self.copy_markdown_button.setEnabled(True)

        # Update user filter
        users = set(p.username for p in processes if p.username)
        self.user_combo.clear()
        self.user_combo.addItem("All Users", "")
        for user in sorted(users):
            self.user_combo.addItem(user, user)

    def on_load_error(self, error_msg: str) -> None:
        """Handle process loading error."""
        self.progress_bar.setVisible(False)
        QMessageBox.warning(self, "Load Error", f"Failed to load processes: {error_msg}")

    def display_processes(self, processes: List) -> None:
        """Display processes in the table."""
        self.process_table.setRowCount(len(processes))

        for row, process in enumerate(processes):
            self.process_table.setItem(row, 0, QTableWidgetItem(str(process.pid)))
            self.process_table.setItem(row, 1, QTableWidgetItem(process.name))
            self.process_table.setItem(row, 2, QTableWidgetItem(process.command_line))
            self.process_table.setItem(row, 3, QTableWidgetItem(process.username))
            self.process_table.setItem(row, 4, QTableWidgetItem(str(process.variable_count)))

        self.process_table.resizeRowsToContents()

    def filter_processes(self) -> None:
        """Filter processes based on search and user criteria."""
        search_text = self.search_edit.text().lower()
        selected_user = self.user_combo.currentData()

        filtered_processes = []
        for process in self.processes:
            # Search filter
            matches_search = (
                search_text in str(process.pid).lower() or
                search_text in process.name.lower() or
                search_text in process.command_line.lower()
            )

            # User filter
            matches_user = not selected_user or process.username == selected_user

            if matches_search and matches_user:
                filtered_processes.append(process)

        self.display_processes(filtered_processes)

    def on_process_selected(self) -> None:
        """Handle process selection."""
        current_row = self.process_table.currentRow()
        if current_row >= 0:
            # Get PID from table
            pid_item = self.process_table.item(current_row, 0)
            if pid_item:
                try:
                    self.selected_pid = int(pid_item.text())
                    self.inspect_button.setEnabled(True)
                    self.inspect_process()
                except ValueError:
                    self.selected_pid = None
                    self.inspect_button.setEnabled(False)

    def inspect_process(self) -> None:
        """Inspect the selected process's environment."""
        if not self.selected_pid:
            return

        try:
            # Get process environment report
            report = self.process_service.get_process_environment_report(
                self.selected_pid,
                self.system_variables
            )

            if report:
                self.display_environment_report(report)
            else:
                self.clear_details()
                QMessageBox.warning(
                    self, "Inspection Failed",
                    f"Could not inspect process {self.selected_pid}. "
                    "It may have terminated or access may be denied."
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to inspect process: {e}")

    def copy_processes_to_markdown(self) -> None:
        """Generate markdown formatted text with all process information and copy to clipboard."""
        if not self.processes:
            QMessageBox.warning(self, "No Data", "No process information available to copy.")
            return

        try:
            # Generate markdown content
            markdown_content = self._generate_processes_markdown()

            # Copy to clipboard
            clipboard = self.screen().clipboard()
            clipboard.setText(markdown_content)

            QMessageBox.information(
                self, "Copied to Clipboard",
                f"Process information for {len(self.processes)} processes has been copied to clipboard in Markdown format."
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to copy processes to markdown: {e}")

    def _generate_processes_markdown(self) -> str:
        """Generate markdown formatted text with all process information."""
        from datetime import datetime

        lines = []
        lines.append("# System Process Investigation Report")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Total Processes:** {len(self.processes)}")
        lines.append("")

        # Process summary table
        lines.append("## Process Summary")
        lines.append("")
        lines.append("| PID | Name | Command Line | User | Parent PID | Variables |")
        lines.append("|-----|------|--------------|------|------------|-----------|")

        for process in sorted(self.processes, key=lambda p: p.pid):
            # Escape pipe characters in command line for markdown table
            cmd_line = process.command_line.replace("|", "\\|") if process.command_line else ""
            # Truncate long command lines for readability
            if len(cmd_line) > 80:
                cmd_line = cmd_line[:77] + "..."

            lines.append(f"| {process.pid} | {process.name} | {cmd_line} | {process.username} | {process.parent_pid or ''} | {process.variable_count} |")

        lines.append("")

        # Process statistics
        lines.append("## Process Statistics")
        lines.append("")

        # Count by user
        user_counts = {}
        for process in self.processes:
            user = process.username or "system"
            user_counts[user] = user_counts.get(user, 0) + 1

        lines.append("### Processes by User")
        lines.append("")
        for user, count in sorted(user_counts.items()):
            lines.append(f"- **{user}:** {count} processes")
        lines.append("")

        # Most common process names
        name_counts = {}
        for process in self.processes:
            name_counts[process.name] = name_counts.get(process.name, 0) + 1

        lines.append("### Most Common Process Names")
        lines.append("")
        for name, count in sorted(name_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            lines.append(f"- **{name}:** {count} instances")
        lines.append("")

        # System information
        import platform
        import psutil

        lines.append("## System Information")
        lines.append("")
        lines.append(f"- **Platform:** {platform.platform()}")
        lines.append(f"- **Python Version:** {platform.python_version()}")
        lines.append(f"- **CPU Cores:** {psutil.cpu_count()}")
        lines.append(f"- **Total Memory:** {self._format_bytes(psutil.virtual_memory().total)}")

        # Current memory usage
        memory = psutil.virtual_memory()
        lines.append(f"- **Memory Used:** {self._format_bytes(memory.used)} ({memory.percent:.1f}%)")

        lines.append("")
        lines.append("---")
        lines.append("*Report generated by Environment Variable Editor*")

        return "\n".join(lines)

    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes into human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return ".1f"
            bytes_value /= 1024.0
        return ".1f"

    def display_environment_report(self, report) -> None:
        """Display the environment report in all tabs."""
        # Environment variables tab
        self.env_table.setRowCount(len(report.all_variables))
        for row, (name, value) in enumerate(report.all_variables.items()):
            self.env_table.setItem(row, 0, QTableWidgetItem(name))
            # Mask sensitive values
            display_value = self._mask_sensitive_value(name, value)
            self.env_table.setItem(row, 1, QTableWidgetItem(display_value))

        self.env_table.resizeColumnsToContents()

        # Process info tab
        info_text = f"""Process Information:
PID: {report.process.pid}
Name: {report.process.name}
Command Line: {report.process.command_line}
Username: {report.process.username}
Parent PID: {report.process.parent_pid or 'N/A'}
Environment Variables: {len(report.all_variables)}

Inherited Variables: {len(report.inherited_variables)}
Process-Specific Variables: {len(report.process_specific_variables)}
"""
        self.info_text.setPlainText(info_text)

        # Comparison tab
        self.compare_table.setRowCount(len(report.inherited_variables))
        for row, comparison in enumerate(report.inherited_variables):
            self.compare_table.setItem(row, 0, QTableWidgetItem(comparison.variable_name))
            self.compare_table.setItem(row, 1, QTableWidgetItem(
                comparison.system_value or "Not set"
            ))
            self.compare_table.setItem(row, 2, QTableWidgetItem(
                comparison.process_value or "Not set"
            ))

            # Status
            if comparison.matches_system:
                status = "✓ Match"
            elif comparison.is_inherited:
                status = "~ Modified"
            else:
                status = "✗ Not inherited"

            status_item = QTableWidgetItem(status)
            self.compare_table.setItem(row, 3, status_item)

        self.compare_table.resizeColumnsToContents()

    def clear_details(self) -> None:
        """Clear all detail displays."""
        self.env_table.setRowCount(0)
        self.info_text.clear()
        self.compare_table.setRowCount(0)

    def _mask_sensitive_value(self, name: str, value: str) -> str:
        """Mask sensitive environment variable values."""
        sensitive_keywords = ['password', 'secret', 'key', 'token', 'auth', 'credential']
        name_lower = name.lower()

        if any(keyword in name_lower for keyword in sensitive_keywords):
            return "***"

        return value
