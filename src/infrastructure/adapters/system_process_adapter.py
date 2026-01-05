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
SystemProcessAdapter - Infrastructure Adapter

Implementation of ProcessEnvironmentRepository using psutil.
Provides access to system process information and environments.
"""

import psutil
from typing import List, Optional, Dict
from datetime import datetime

from ...domain import (
    Process,
    ProcessEnvironment,
    ProcessEnvironmentRepository,
    ProcessId,
    ProcessName
)


class SystemProcessAdapter(ProcessEnvironmentRepository):
    """
    System process inspection adapter using psutil.

    This adapter provides real access to system processes and their
    environment variables. It handles permission issues gracefully
    and provides fallbacks for restricted access.
    """

    def __init__(self) -> None:
        """Initialize the adapter."""
        self._process_cache: Optional[List[Process]] = None
        self._cache_timestamp: Optional[datetime] = None
        self._cache_timeout_seconds = 30  # Cache for 30 seconds

    def get_all_processes(self) -> List[Process]:
        """
        Get information about all currently running processes.

        Returns:
            List of Process entities
        """
        self._refresh_cache_if_needed()

        if self._process_cache is not None:
            return self._process_cache.copy()

        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'ppid', 'username']):
            try:
                process = self._create_process_from_psutil(proc)
                if process:
                    processes.append(process)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Skip processes that terminate, are inaccessible, or are zombies
                continue
            except Exception as e:
                # Log unexpected errors but continue processing other processes
                # In a real application, you'd use proper logging here
                print(f"Warning: Failed to process a process (PID may be invalid): {e}")
                continue

        self._process_cache = processes
        self._cache_timestamp = datetime.now()

        return processes

    def get_process_by_id(self, process_id: ProcessId) -> Optional[Process]:
        """
        Get information about a specific process by PID.
        """
        try:
            proc = psutil.Process(int(process_id))
            return self._create_process_from_psutil(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError):
            return None

    def get_process_environment(self, process_id: ProcessId) -> Optional[ProcessEnvironment]:
        """
        Get the environment variables for a specific process.
        """
        try:
            proc = psutil.Process(int(process_id))
            process = self._create_process_from_psutil(proc)

            if not process:
                return None

            # Get environment variables
            env_vars = proc.environ()

            return ProcessEnvironment(
                process=process,
                environment_variables=env_vars
            )

        except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError):
            return None

    def get_processes_by_name(self, name: str) -> List[Process]:
        """
        Get all processes with a specific name.
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and name.lower() in proc.info['name'].lower():
                    process = self._create_process_from_psutil(proc)
                    if process:
                        processes.append(process)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return processes

    def get_processes_by_user(self, username: str) -> List[Process]:
        """
        Get all processes running under a specific user.
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                if proc.info['username'] == username:
                    process = self._create_process_from_psutil(proc)
                    if process:
                        processes.append(process)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return processes

    def is_process_running(self, process_id: ProcessId) -> bool:
        """
        Check if a process is currently running.
        """
        return psutil.pid_exists(int(process_id))

    def get_process_tree(self, root_process_id: ProcessId) -> Dict[ProcessId, List[Process]]:
        """
        Get the process tree starting from a root process.
        """
        tree = {}
        root_pid = int(root_process_id)

        try:
            root_proc = psutil.Process(root_pid)
            self._build_process_tree(root_proc, tree)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

        return tree

    def refresh_process_cache(self) -> None:
        """
        Refresh cached process information.
        """
        self._process_cache = None
        self._cache_timestamp = None

    def _refresh_cache_if_needed(self) -> None:
        """Refresh cache if it's stale."""
        if self._cache_timestamp is None:
            return

        elapsed = (datetime.now() - self._cache_timestamp).total_seconds()
        if elapsed > self._cache_timeout_seconds:
            self.refresh_process_cache()

    def _create_process_from_psutil(self, proc: psutil.Process) -> Optional[Process]:
        """Create a Process entity from a psutil Process object."""
        try:
            info = proc.as_dict(['pid', 'name', 'cmdline', 'ppid', 'username'])

            # Validate PID before creating ProcessId
            pid = info.get('pid')
            if not isinstance(pid, int) or pid < 1:
                # Skip invalid PIDs (like 0 or negative values)
                return None

            # Create value objects
            process_id = ProcessId(pid)

            # Sanitize process name to remove invalid characters
            raw_name = info['name'] or 'unknown'
            sanitized_name = self._sanitize_process_name(raw_name)
            name = ProcessName(sanitized_name)

            # Build command line
            cmdline = info.get('cmdline')
            command_line = ' '.join(cmdline) if cmdline else ''

            return Process(
                process_id=process_id,
                name=name,
                command_line=command_line,
                parent_pid=info.get('ppid'),
                username=info.get('username') or '',
                snapshot_time=datetime.now()
            )

        except (ValueError, TypeError, KeyError):
            # Skip invalid process data
            return None

    def _sanitize_process_name(self, name: str) -> str:
        """Sanitize a process name to make it valid for ProcessName."""
        if not name:
            return 'unknown'

        # Remove or replace invalid characters
        invalid_chars = '/\\:*?"<>|'
        sanitized = name

        # Replace invalid characters with underscores
        for char in invalid_chars:
            sanitized = sanitized.replace(char, '_')

        # Ensure it's not empty after sanitization
        sanitized = sanitized.strip()
        if not sanitized:
            return 'unknown'

        # Truncate if too long (ProcessName.MAX_LENGTH is 255)
        if len(sanitized) > 255:
            sanitized = sanitized[:252] + '...'

        return sanitized

    def _build_process_tree(
        self,
        root_proc: psutil.Process,
        tree: Dict[ProcessId, List[Process]]
    ) -> None:
        """Recursively build the process tree."""
        try:
            root_pid = ProcessId(root_proc.pid)
            tree[root_pid] = []

            for child in root_proc.children(recursive=False):
                try:
                    child_process = self._create_process_from_psutil(child)
                    if child_process:
                        tree[root_pid].append(child_process)
                        # Recursively add children
                        self._build_process_tree(child, tree)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError):
            pass
