# Contributing to Environment Variable Editor

Thank you for your interest in contributing to the Environment Variable Editor! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment support

### Local Development
```bash
# Clone the repository
git clone <repository-url>
cd EnvEditor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest  # For testing

# Run the application
python main.py

# Run tests
python -m pytest tests/
```

## Architecture Guidelines

This project follows **Clean Architecture** principles:

### Layer Structure
```
src/
├── domain/           # Core business logic (no external dependencies)
├── application/      # Use cases and application services
├── infrastructure/   # External system adapters
└── presentation/     # PyQt GUI components
```

### Key Principles
- **Domain First**: Always start with domain modeling
- **Dependency Inversion**: Domain depends on abstractions, not concretions
- **SOLID Principles**: Single responsibility, open/closed, etc.
- **Testability**: Write tests before or alongside code

## Development Workflow

### 1. Choose an Issue
- Check existing issues or create a new one
- Discuss the approach if it's a significant change

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 3. Implement Changes
- Follow the existing code style and architecture patterns
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 4. Commit Changes
```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: Add new feature description

- What was changed
- Why it was changed
- Any breaking changes
"
```

### 5. Push and Create Pull Request
```bash
git push origin your-branch-name
# Create PR on GitHub/GitLab
```

## Code Style

### Python Style
- Follow PEP 8
- Use type hints for all public APIs
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Commit Messages
Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing related changes
- `chore`: Maintenance tasks

## Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/unit/test_domain.py
```

### Test Structure
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows

### Test Coverage
- Aim for >90% code coverage
- Test both happy path and error conditions
- Use descriptive test names

## Documentation

### Code Documentation
- Add docstrings to all public functions/classes
- Include type hints
- Explain complex business logic

### Architecture Documentation
- Update `docs/ARCHITECTURE_DECISIONS.md` for significant changes
- Update `docs/UBIQUITOUS_LANGUAGE.md` for new domain concepts
- Keep README.md current

## Review Process

### Pull Request Requirements
- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No breaking changes without discussion

### Review Checklist
- [ ] Code is readable and maintainable
- [ ] Follows architecture principles
- [ ] Adequate test coverage
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed

## Release Process

### Version Numbering
Follow Semantic Versioning (MAJOR.MINOR.PATCH)

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated
- [ ] Changelog updated
- [ ] Tag created: `git tag -a v1.2.3 -m "Release v1.2.3"`

## Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions
- **Documentation**: Check `docs/` directory first

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).
