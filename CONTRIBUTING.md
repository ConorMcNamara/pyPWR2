# Contributing to pyPWR2

Thank you for your interest in contributing to pyPWR2! This document provides guidelines and instructions for contributing.

## Development Setup

### Quick Setup (Using Make)

This project includes a Makefile for convenient development tasks. Run `make help` to see all available commands.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ConorMcNamara/pyPWR2.git
   cd pyPWR2
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Complete development setup:**
   ```bash
   make dev-setup
   ```

This single command will install all development dependencies and set up pre-commit hooks.

### Manual Setup (Without Make)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ConorMcNamara/pyPWR2.git
   cd pyPWR2
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package with development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

## Development Workflow

### Code Style

This project uses modern Python tooling for code quality:

- **Ruff**: For linting and formatting
- **mypy**: For type checking
- **pytest**: For testing

All of these are configured in `pyproject.toml`.

### Using the Makefile

The Makefile provides convenient shortcuts for common tasks:

```bash
# Show all available commands
make help

# Run tests with coverage
make test-coverage

# Run linting
make lint

# Format code
make format

# Run type checking
make type-check

# Run all quality checks
make check

# Simulate CI locally (run all checks + tests)
make dev-check

# Clean build artifacts
make clean
```

### Running Tests

**Using Make:**
```bash
make test                # Run tests
make test-coverage       # Run tests with coverage report
make test-verbose        # Run tests with verbose output
```

**Manual commands:**
```bash
pytest                   # Run all tests
pytest --cov=pwr2        # Run with coverage report
pytest tests/test_pwr2.py  # Run specific test file
```

### Code Formatting and Linting

**Using Make:**
```bash
make format              # Format code with ruff
make lint                # Run linter
make lint-fix            # Run linter and auto-fix issues
make type-check          # Run type checker
```

**Manual commands:**
```bash
ruff format .            # Format code with ruff
ruff check .             # Run linter
mypy pwr2                # Run type checker
```

Pre-commit hooks will automatically run these checks before each commit.

### Type Hints

All code must include comprehensive type hints. The project uses:
- `Optional[Type]` for nullable parameters
- Proper return type annotations
- PEP 561 compliance (via `py.typed` marker)

## Making Changes

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clear, concise code
   - Add type hints to all functions
   - Follow existing code style
   - Update docstrings (numpydoc style)

3. **Add tests:**
   - All new features must include tests
   - Aim for high code coverage
   - Use parametrized tests where appropriate

4. **Update documentation:**
   - Update docstrings
   - Update README.md if needed
   - Add entry to CHANGELOG.md under `[Unreleased]`

5. **Run the test suite:**
   ```bash
   make dev-check  # Recommended: runs all checks
   # Or manually:
   # pytest
   # ruff check .
   # mypy pwr2
   ```

6. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

   Pre-commit hooks will run automatically. If they fail, fix the issues and commit again.

7. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request:**
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all CI checks pass

## Pull Request Guidelines

- **Keep PRs focused**: One feature or fix per PR
- **Write clear commit messages**: Use present tense ("Add feature" not "Added feature")
- **Update tests**: All PRs should include or update tests
- **Maintain backward compatibility**: Unless it's a major version bump
- **Update CHANGELOG.md**: Add your changes under `[Unreleased]`

## Code Review Process

1. A maintainer will review your PR
2. Address any requested changes
3. Once approved, a maintainer will merge your PR

## Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## Questions?

Feel free to open an issue for any questions or concerns.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
