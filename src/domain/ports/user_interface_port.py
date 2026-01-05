"""
UserInterfacePort - Port for User Interface Interactions

Interface for user interface operations and user interaction patterns.
Abstracts UI concerns to enable different UI implementations.
"""

from abc import ABC, abstractmethod
from typing import Optional, Callable, Any


class UserInterfacePort(ABC):
    """
    Port for user interface operations.

    This interface abstracts user interface interactions to enable:
    - Different UI frameworks (Qt, GTK, web-based)
    - Testing with mock UIs
    - Separation of UI logic from business logic
    """

    @abstractmethod
    def show_message(
        self,
        title: str,
        message: str,
        message_type: str = "info"
    ) -> None:
        """
        Show a message to the user.

        Args:
            title: Message title
            message: Message content
            message_type: Type of message (info, warning, error, question)
        """
        pass

    @abstractmethod
    def show_confirmation_dialog(
        self,
        title: str,
        message: str,
        default_button: str = "no"
    ) -> bool:
        """
        Show a confirmation dialog and get user response.

        Args:
            title: Dialog title
            message: Confirmation message
            default_button: Default button ("yes" or "no")

        Returns:
            True if user confirmed, False otherwise
        """
        pass

    @abstractmethod
    def show_input_dialog(
        self,
        title: str,
        message: str,
        default_value: str = ""
    ) -> Optional[str]:
        """
        Show an input dialog and get user input.

        Args:
            title: Dialog title
            message: Input prompt message
            default_value: Default value for the input field

        Returns:
            User input string, or None if cancelled
        """
        pass

    @abstractmethod
    def show_error_dialog(self, title: str, error_message: str) -> None:
        """
        Show an error dialog.

        Args:
            title: Error dialog title
            error_message: Error message to display
        """
        pass

    @abstractmethod
    def run_with_progress(
        self,
        title: str,
        operation: Callable[[], Any]
    ) -> Any:
        """
        Run an operation with progress indication.

        Args:
            title: Progress dialog title
            operation: Function to execute with progress indication

        Returns:
            Result of the operation
        """
        pass

    @abstractmethod
    def refresh_display(self) -> None:
        """
        Refresh the user interface display.

        This method should be called when underlying data changes
        and the UI needs to be updated to reflect those changes.
        """
        pass

    @abstractmethod
    def get_current_user_id(self) -> str:
        """
        Get the ID of the current user.

        Returns:
            User identifier for audit trails
        """
        pass
