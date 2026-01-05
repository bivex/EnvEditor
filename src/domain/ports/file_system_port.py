"""
FileSystemPort - Port for File System Operations

Interface for file system operations needed by the application.
Abstracts away file system details and enables testing.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from pathlib import Path


class FileSystemPort(ABC):
    """
    Port for file system operations.

    This interface abstracts file system operations to enable:
    - Testing with mock file systems
    - Platform-independent file operations
    - Centralized file access patterns
    """

    @abstractmethod
    def read_text_file(self, path: Path) -> str:
        """
        Read the contents of a text file.

        Args:
            path: Path to the file

        Returns:
            The file contents as a string

        Raises:
            FileNotFoundError: If the file doesn't exist
            PermissionError: If access is denied
            OSError: For other file system errors
        """
        pass

    @abstractmethod
    def write_text_file(self, path: Path, content: str) -> None:
        """
        Write content to a text file.

        Args:
            path: Path to the file
            content: Content to write

        Raises:
            PermissionError: If access is denied
            OSError: For other file system errors
        """
        pass

    @abstractmethod
    def file_exists(self, path: Path) -> bool:
        """
        Check if a file exists.

        Args:
            path: Path to check

        Returns:
            True if the file exists, False otherwise
        """
        pass

    @abstractmethod
    def create_directory(self, path: Path) -> None:
        """
        Create a directory and any necessary parent directories.

        Args:
            path: Path to the directory to create

        Raises:
            PermissionError: If access is denied
            OSError: For other file system errors
        """
        pass

    @abstractmethod
    def list_files_in_directory(self, path: Path) -> List[Path]:
        """
        List all files in a directory.

        Args:
            path: Path to the directory

        Returns:
            List of file paths in the directory

        Raises:
            FileNotFoundError: If the directory doesn't exist
            PermissionError: If access is denied
            OSError: For other file system errors
        """
        pass

    @abstractmethod
    def get_user_config_directory(self) -> Path:
        """
        Get the user's configuration directory.

        Returns:
            Path to the user config directory
        """
        pass

    @abstractmethod
    def get_application_data_directory(self) -> Path:
        """
        Get the application's data directory.

        Returns:
            Path to the application data directory
        """
        pass
