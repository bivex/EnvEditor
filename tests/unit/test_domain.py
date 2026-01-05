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
Unit Tests for Domain Layer

Tests domain entities, value objects, and business logic.
"""

import pytest
from datetime import datetime

from src.domain.entities import EnvironmentVariable
from src.domain.value_objects import VariableName, VariableValue, VariableScope
from src.domain.exceptions import DomainValidationError, AggregateInvariantViolationError


class TestVariableName:
    """Test VariableName value object."""

    def test_valid_name_creation(self):
        """Test creating valid variable names."""
        name = VariableName("MY_VARIABLE")
        assert str(name) == "MY_VARIABLE"
        assert name.value == "MY_VARIABLE"

    def test_name_starting_with_underscore(self):
        """Test variable name starting with underscore."""
        name = VariableName("_PRIVATE_VAR")
        assert str(name) == "_PRIVATE_VAR"

    def test_name_with_numbers(self):
        """Test variable name with numbers."""
        name = VariableName("VAR123")
        assert str(name) == "VAR123"

    def test_invalid_empty_name(self):
        """Test that empty names are rejected."""
        with pytest.raises(DomainValidationError, match="cannot be empty"):
            VariableName("")

    def test_invalid_whitespace_name(self):
        """Test that whitespace-only names are rejected."""
        with pytest.raises(DomainValidationError, match="cannot be empty"):
            VariableName("   ")

    def test_name_starting_with_number(self):
        """Test that names starting with numbers are rejected."""
        with pytest.raises(DomainValidationError, match="start with letter or underscore"):
            VariableName("123VAR")

    def test_name_with_invalid_characters(self):
        """Test that names with invalid characters are rejected."""
        with pytest.raises(DomainValidationError, match="alphanumeric characters and underscores"):
            VariableName("MY-VAR")

    def test_name_too_long(self):
        """Test that overly long names are rejected."""
        long_name = "A" * 256
        with pytest.raises(DomainValidationError, match="cannot exceed"):
            VariableName(long_name)


class TestVariableValue:
    """Test VariableValue value object."""

    def test_valid_value_creation(self):
        """Test creating valid variable values."""
        value = VariableValue("some value")
        assert str(value) == "some value"
        assert value.value == "some value"

    def test_empty_value_creation(self):
        """Test creating empty values."""
        value = VariableValue("")
        assert str(value) == ""
        assert value.is_empty is True

    def test_none_value_rejected(self):
        """Test that None values are rejected."""
        with pytest.raises(DomainValidationError, match="cannot be None"):
            VariableValue(None)

    def test_value_too_long(self):
        """Test that overly long values are rejected."""
        long_value = "A" * 32768
        with pytest.raises(DomainValidationError, match="cannot exceed"):
            VariableValue(long_value)

    def test_sensitive_value_masking(self):
        """Test that sensitive values are masked in string representation."""
        sensitive_value = VariableValue("password=secret123")
        assert str(sensitive_value) == "***"
        assert sensitive_value.value == "password=secret123"  # Actual value preserved


class TestVariableScope:
    """Test VariableScope enumeration."""

    def test_scope_values(self):
        """Test scope enumeration values."""
        assert VariableScope.SYSTEM.value == "system"
        assert VariableScope.USER.value == "user"
        assert VariableScope.PROCESS.value == "process"

    def test_scope_string_conversion(self):
        """Test string representation of scopes."""
        assert str(VariableScope.SYSTEM) == "system"
        assert str(VariableScope.USER) == "user"

    def test_elevation_requirement(self):
        """Test elevation requirements for scopes."""
        assert VariableScope.SYSTEM.requires_elevation() is True
        assert VariableScope.USER.requires_elevation() is False
        assert VariableScope.PROCESS.requires_elevation() is False

    def test_scope_from_string(self):
        """Test creating scope from string."""
        assert VariableScope.from_string("SYSTEM") == VariableScope.SYSTEM
        assert VariableScope.from_string("user") == VariableScope.USER

    def test_invalid_scope_string(self):
        """Test invalid scope string raises error."""
        with pytest.raises(ValueError, match="Invalid scope"):
            VariableScope.from_string("invalid")


class TestEnvironmentVariable:
    """Test EnvironmentVariable entity."""

    def test_variable_creation(self):
        """Test creating a valid environment variable."""
        name = VariableName("TEST_VAR")
        value = VariableValue("test value")
        scope = VariableScope.USER

        variable = EnvironmentVariable(name, value, scope)

        assert variable.name == name
        assert variable.value == value
        assert variable.scope == scope
        assert variable.id is not None
        assert variable.created_at is not None
        assert variable.updated_at is not None

    def test_system_variable_empty_value_rejected(self):
        """Test that system variables cannot have empty values."""
        name = VariableName("SYSTEM_VAR")
        value = VariableValue("")  # Empty value
        scope = VariableScope.SYSTEM

        with pytest.raises(AggregateInvariantViolationError, match="cannot have empty values"):
            EnvironmentVariable(name, value, scope)

    def test_variable_value_update(self):
        """Test updating variable value."""
        name = VariableName("TEST_VAR")
        value = VariableValue("initial value")
        scope = VariableScope.USER

        variable = EnvironmentVariable(name, value, scope)
        initial_updated_at = variable.updated_at

        new_value = VariableValue("updated value")
        variable.update_value(new_value)

        assert variable.value == new_value
        assert variable.updated_at > initial_updated_at

    def test_variable_scope_change_restricted(self):
        """Test that system variable scope changes are restricted."""
        name = VariableName("SYSTEM_VAR")
        value = VariableValue("system value")
        scope = VariableScope.SYSTEM

        variable = EnvironmentVariable(name, value, scope)

        # Attempt to change scope
        with pytest.raises(AggregateInvariantViolationError, match="Cannot change scope"):
            variable.change_scope(VariableScope.USER)

    def test_domain_events_collected(self):
        """Test that domain events are collected."""
        name = VariableName("TEST_VAR")
        value = VariableValue("test value")
        scope = VariableScope.USER

        variable = EnvironmentVariable(name, value, scope)

        events = variable.collect_domain_events()
        assert len(events) == 1
        # Note: Event type checking would require importing event classes

    def test_variable_equality(self):
        """Test variable equality based on ID."""
        name1 = VariableName("VAR1")
        name2 = VariableName("VAR2")
        value = VariableValue("value")
        scope = VariableScope.USER

        var1 = EnvironmentVariable(name1, value, scope, variable_id="id1")
        var2 = EnvironmentVariable(name2, value, scope, variable_id="id1")  # Same ID
        var3 = EnvironmentVariable(name1, value, scope, variable_id="id2")  # Different ID

        assert var1 == var2
        assert var1 != var3
