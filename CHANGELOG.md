# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Python version support**: Now requires Python 3.13+ (dropped support for 3.10, 3.11, 3.12)
- Updated CI/CD to test Python 3.13 and 3.14 (pre-release)
- Updated all tooling configurations to target Python 3.13

### Added
- Comprehensive type hints throughout the codebase
- `py.typed` marker file for PEP 561 compatibility
- Pre-commit hooks configuration
- **Makefile** with convenient development commands:
  - `make help` - Show all available commands
  - `make dev-setup` - Complete development environment setup
  - `make test-coverage` - Run tests with coverage
  - `make check` - Run all code quality checks
  - `make dev-check` - Simulate CI locally
  - And 25+ more commands for common tasks
- Modern GitHub Actions CI/CD workflow with:
  - Linting (ruff)
  - Type checking (mypy)
  - Testing across Python 3.13-3.14 and multiple OS platforms
  - Code coverage reporting
  - Build artifact generation
- Comprehensive pyproject.toml configuration with:
  - Complete project metadata
  - Development dependencies group
  - Tool configurations for pytest, mypy, ruff, and coverage

### Changed
- Renamed `test/` directory to `tests/` following standard convention
- Enhanced pyproject.toml with complete metadata and classifiers
- Switched from `poetry-core` to `hatchling` as build backend
- Improved README example with correct syntax and clearer usage
- Updated function signatures with proper Optional type hints
- Consolidated GitHub Actions workflows into a single comprehensive CI workflow

### Fixed
- Syntax error in README.md example code (incorrect comma placement in `round()` call)
- Incorrect description in `pwr_2way` function output
- Duplicate "NOTE:" text in `ss_2way` function output
- Function parameter types (changed from float to int where appropriate)

### Removed
- Redundant `requirements.txt` file (dependencies now managed via pyproject.toml)
- Old GitHub Actions workflows (linter.yml and python-package.yml)

## [1.0.0] - Initial Release

### Added
- One-way ANOVA power and sample size calculations
- Two-way ANOVA power and sample size calculations
- Functions: `pwr_1way`, `ss_1way`, `pwr_2way`, `ss_2way`
- Basic documentation and examples
