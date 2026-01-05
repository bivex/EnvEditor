# Environment Variable Editor

A clean architecture PyQt GUI application for managing environment variables with comprehensive audit trails, context management, and domain-driven design principles.

## Architecture Overview

This application follows **Domain-Driven Design (DDD)** and **Clean Architecture** principles:

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
- **EnvironmentContext**: Collections of variables for specific purposes (dev, prod, testing)
- **AuditEntry**: Immutable audit trail entries for compliance

### Value Objects
- **VariableName**: Validated environment variable names
- **VariableValue**: Environment variable values with security masking
- **VariableScope**: System, user, or process scope enumeration
- **ContextName**: Validated context names

### Business Rules (Invariants)
- Variable names must follow identifier naming conventions
- System variables cannot have empty values
- Variables are unique within their scope
- All changes are auditable

## Features

### Environment Variable Management
- ✅ View variables by scope (system, user, process)
- ✅ Create new environment variables
- ✅ Edit existing variables
- ✅ Delete variables with confirmation
- ✅ Real-time validation

### Context Management
- ✅ Create named contexts for variable collections
- ✅ Add/remove variables from contexts
- ✅ Switch between contexts

### Audit & Compliance
- ✅ Complete audit trail for all changes
- ✅ User tracking and timestamps
- ✅ Change history per variable
- ✅ Compliance reporting

### User Experience
- ✅ Clean, intuitive PyQt interface
- ✅ Table-based variable listing
- ✅ Search and filtering capabilities
- ✅ Detailed variable information
- ✅ Error handling and user feedback

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

## Contributing

1. Follow the established architecture patterns
2. Add tests for new functionality
3. Update documentation
4. Ensure all linting passes
5. Follow commit message conventions

## License

This project demonstrates clean architecture principles and is provided as educational material.
