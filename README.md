# Environment Variable Editor

A clean architecture PyQt GUI application for managing environment variables, env vars, and system environment configuration with comprehensive audit trails, context management, process investigation, and domain-driven design principles. Built with Python, Qt, PyQt6 for cross-platform desktop environment variable management, system administration tools, and development workflow optimization.

## Architecture Overview

This application follows **Domain-Driven Design (DDD)**, **Clean Architecture**, **Hexagonal Architecture**, and **SOLID design principles** for building maintainable, testable software systems:

```
┌─────────────────────────────────────┐
│         Presentation Layer          │  PyQt GUI
│         (UI Components)             │
└─────────────────────────────────────┘
                    │
┌─────────────────────────────────────┐
│        Application Layer            │  Use Cases
│        (Business Logic)             │
└─────────────────────────────────────┘
                    │
┌─────────────────────────────────────┐
│          Domain Layer               │  Core Business Rules
│    (Entities, Value Objects,        │
│     Domain Services, Events)        │
└─────────────────────────────────────┘
                    │
┌─────────────────────────────────────┐
│       Infrastructure Layer          │  External Systems
│       (Repositories, Adapters)      │
└─────────────────────────────────────┘
```

### Key Design Principles Applied

- **Domain-Driven Design**: Rich domain model with entities, value objects, and domain services
- **Clean Architecture**: Dependency inversion with ports and adapters
- **SOLID Principles**: Single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion
- **Hexagonal Architecture**: Isolated business logic with configurable adapters
- **CQRS-Style Separation**: Read and write operations handled differently where beneficial

## Domain Model

### Core Entities
- **EnvironmentVariable**: Represents a single environment variable with name, value, and scope
- **EnvironmentContext**: Collections of environment variables for specific purposes (development, production, testing)
- **AuditEntry**: Immutable audit trail entries for compliance and security auditing
- **Process**: Running system process with PID, name, and metadata
- **ProcessEnvironment**: Environment variables for a specific running process

### Value Objects
- **VariableName**: Validated environment variable names with identifier rules
- **VariableValue**: Environment variable values with security masking for sensitive data
- **VariableScope**: Environment variable scope enumeration (system, user, process)
- **ContextName**: Validated context names for environment organization
- **ProcessId**: Process identifier validation and type safety
- **ProcessName**: Process executable name validation and sanitization

### Business Rules (Invariants)
- Variable names must follow identifier naming conventions
- System variables cannot have empty values
- Variables are unique within their scope
- All changes are auditable

## Features

### Environment Variable Management
- ✅ View environment variables by scope (system, user, process)
- ✅ Create, read, update, delete (CRUD) operations for env vars
- ✅ Edit existing environment variables with validation
- ✅ Delete variables with confirmation dialogs
- ✅ Real-time validation for environment variable names and values

### Context Management
- ✅ Create named contexts for environment variable collections
- ✅ Add/remove environment variables from contexts
- ✅ Switch between different environment contexts (dev, prod, testing)

### Process Investigation & System Administration
- ✅ Investigate all running processes for environment variables
- ✅ Process environment variable inspection and analysis
- ✅ System process enumeration with psutil integration
- ✅ Environment variable comparison across processes
- ✅ Export process information to markdown format

### Audit & Compliance
- ✅ Complete audit trail for all environment variable changes
- ✅ User tracking and timestamps for compliance
- ✅ Change history per environment variable
- ✅ Audit logging for system administration and security

### User Experience & GUI
- ✅ Clean, intuitive PyQt GUI interface
- ✅ Table-based environment variable listing
- ✅ Search and filtering capabilities for env vars
- ✅ Detailed environment variable information display
- ✅ Error handling and user feedback for desktop application

## Technology Stack

- **GUI Framework**: PyQt6, Qt6 for cross-platform desktop application development
- **Architecture**: Clean Architecture, Domain-Driven Design (DDD), Hexagonal Architecture, Ports & Adapters pattern
- **Programming Language**: Python 3.8+ with type hints and modern Python features
- **Testing**: pytest framework with comprehensive unit test coverage and TDD practices
- **System Integration**: psutil library for process inspection, environment variable management, and system administration
- **Design Patterns**: Repository pattern, Factory pattern, Strategy pattern, Observer pattern
- **Development Tools**: Git version control, virtual environments, linting, and CI/CD ready

## Project Structure

```
src/
├── domain/                    # Domain layer
│   ├── entities/             # Domain entities
│   ├── value_objects/        # Value objects
│   ├── services/            # Domain services
│   ├── repositories/        # Repository interfaces
│   ├── ports/               # Port interfaces
│   ├── events/              # Domain events
│   └── dtos/                # Data transfer objects
├── application/             # Application layer
│   └── services/            # Use case implementations
├── infrastructure/          # Infrastructure layer
│   └── adapters/            # Port implementations
└── presentation/            # Presentation layer (PyQt)
tests/                       # Test suites
docs/                        # Documentation
```

## Installation & Running

### Prerequisites
- Python 3.8+
- macOS, Windows, or Linux

### Setup
```bash
# Clone or navigate to project directory
cd /path/to/EnvEditor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Development Guidelines

### Adding New Features
1. **Domain First**: Define domain concepts, entities, and business rules
2. **Ports & Adapters**: Define interfaces in the domain layer
3. **Application Services**: Implement use cases that orchestrate domain operations
4. **Infrastructure**: Implement adapters that fulfill the port contracts
5. **Presentation**: Update UI to use new application services

### Testing Strategy
- **Unit Tests**: Domain logic, entities, value objects
- **Integration Tests**: Repository implementations, external adapters
- **End-to-End Tests**: Complete user workflows

### Code Quality
- Type hints for all public interfaces
- Comprehensive docstrings
- Linting and formatting
- Pre-commit hooks for quality checks

## Configuration

The application uses environment-based configuration:
- Database connections
- External service endpoints
- Security settings
- UI preferences

Configuration is loaded from:
1. Environment variables
2. Configuration files
3. Default values

## Security Considerations

- Sensitive values are masked in the UI
- Audit trails track all changes
- Permission checks for system-level operations
- Input validation at all boundaries
- No hardcoded secrets

## Future Enhancements

- Persistent storage (SQLite/PostgreSQL)
- Real system environment variable integration
- Import/export functionality
- Context-based variable deployment
- Multi-user collaboration features
- Plugin system for custom validations

## Keywords

**Environment Variables**: env vars, environment management, system environment, user environment, process environment, environment configuration

**Python Development**: Python GUI, PyQt6, Qt application, desktop application, cross-platform development, Python tools

**Software Architecture**: Clean Architecture, Domain-Driven Design, DDD, Hexagonal Architecture, Ports and Adapters, SOLID principles, layered architecture

**System Administration**: process investigation, system monitoring, environment inspection, audit trails, compliance logging, security auditing

**Development Tools**: CRUD operations, data validation, search and filter, export functionality, markdown export, clipboard integration

## Development & Testing

### Quality Assurance
- **Unit Testing**: Comprehensive test coverage with pytest
- **Type Safety**: Full type hints throughout codebase
- **Code Quality**: Linting, formatting, and pre-commit hooks
- **Architecture Validation**: Clean Architecture principles enforced

### Testing Commands
```bash
# Run all unit tests
python -m pytest tests/

# Run with coverage report
python -m pytest --cov=src tests/

# Run specific test module
python -m pytest tests/unit/test_domain.py
```

## Contributing

1. Follow the established architecture patterns
2. Add tests for new functionality
3. Update documentation
4. Ensure all linting passes
5. Follow commit message conventions

## License

This project demonstrates clean architecture principles and is provided as educational material.
