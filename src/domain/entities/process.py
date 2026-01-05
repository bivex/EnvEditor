# Copyright (c) 2026 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2026-01-05T01:27:12
# Last Updated: 2026-01-05T01:28:30
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""
Process Entity

Represents a running process on the operating system.
This is a read-only entity that captures process state at a point in time.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from ..value_objects import ProcessId, ProcessName
from ..exceptions import DomainValidationError


class Process:
    """
    Process Entity

    Represents a running process with its identifying information.
    This is a snapshot entity - processes can terminate, so this
    represents the state at the time of inspection.

    Business Rules:
    - PID must be valid and positive
    - Process name cannot be empty
    - Command line provides additional context
    """

    def __init__(
        self,
        process_id: ProcessId,
        name: ProcessName,
        command_line: Optional[str] = None,
        parent_pid: Optional[int] = None,
        username: Optional[str] = None,
        snapshot_time: Optional[datetime] = None,
        process_uuid: Optional[str] = None
    ) -> None:
        """
        Initialize Process entity.

        Args:
            process_id: The process ID (PID)
            name: The process name/executable
            command_line: Full command line (optional)
            parent_pid: Parent process ID (optional)
            username: User running the process (optional)
            snapshot_time: When this process info was captured
            process_uuid: Optional unique identifier
        """
        self._id = process_uuid or str(uuid.uuid4())
        self._process_id = process_id
        self._name = name
        self._command_line = command_line or ""
        self._parent_pid = parent_pid
        self._username = username or ""
        self._snapshot_time = snapshot_time or datetime.now()
        self._is_running = True  # Assume running when created

        self._validate_invariants()

    @property
    def id(self) -> str:
        """Get the unique identifier of this process snapshot."""
        return self._id

    @property
    def process_id(self) -> ProcessId:
        """Get the process ID (PID)."""
        return self._process_id

    @property
    def name(self) -> ProcessName:
        """Get the process name."""
        return self._name

    @property
    def command_line(self) -> str:
        """Get the full command line."""
        return self._command_line

    @property
    def parent_pid(self) -> Optional[int]:
        """Get the parent process ID."""
        return self._parent_pid

    @property
    def username(self) -> str:
        """Get the username running this process."""
        return self._username

    @property
    def snapshot_time(self) -> datetime:
        """Get when this process information was captured."""
        return self._snapshot_time

    @property
    def is_running(self) -> bool:
        """Check if the process was running when captured."""
        return self._is_running

    def mark_as_terminated(self) -> None:
        """
        Mark this process as terminated.

        This doesn't delete the entity but marks it as no longer running.
        Useful for cached process information.
        """
        self._is_running = False

    def get_process_info(self) -> Dict[str, Any]:
        """
        Get a dictionary of process information for display.

        Returns:
            Dictionary with process details
        """
        return {
            'id': self._id,
            'pid': int(self._process_id),
            'name': str(self._name),
            'command_line': self._command_line,
            'parent_pid': self._parent_pid,
            'username': self._username,
            'snapshot_time': self._snapshot_time.isoformat(),
            'is_running': self._is_running
        }

    def _validate_invariants(self) -> None:
        """
        Validate entity invariants.

        Business Rules:
        - Process ID must be valid
        - Name must be valid
        - Snapshot time should not be in the future
        """
        if self._snapshot_time > datetime.now():
            raise DomainValidationError("Snapshot time cannot be in the future")

    def __str__(self) -> str:
        status = "running" if self._is_running else "terminated"
        return f"Process(pid={self._process_id}, name='{self._name}', status={status})"

    def __repr__(self) -> str:
        return (
            f"Process(id='{self._id}', pid={self._process_id}, "
            f"name={self._name!r}, running={self._is_running})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Process):
            return False
        # Two process snapshots are equal if they have the same PID and snapshot time
        return (self._process_id == other._process_id and
                self._snapshot_time == other._snapshot_time)

    def __hash__(self) -> int:
        return hash((self._process_id, self._snapshot_time))
