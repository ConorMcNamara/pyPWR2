# pyPWR2

[![Python package](https://github.com/ConorMcNamara/pyPWR2/actions/workflows/ci.yml/badge.svg)](https://github.com/ConorMcNamara/pyPWR2/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.13%20%7C%203.14-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python implementation of the [pwr2](https://cran.r-project.org/web/packages/pwr2/index.html) R package; a library
for calculating the power, sample size and minimum detectable effect of 1 and 2-way ANOVA tests.

To quote the documentation:

> User friendly functions for power and sample size analysis at one-way and two-way ANOVA settings take either effect
> size or delta and sigma as arguments. They are designed for both one-way and two-way ANOVA settings.

## Features

- **Type-safe**: Comprehensive type hints throughout the codebase
- **Well-tested**: 91%+ test coverage
- **Modern Python**: Supports Python 3.13+ (including 3.14)
- **Cross-platform**: Tested on Linux, macOS, and Windows
- **Easy to use**: Simple, intuitive API

## Installation

```bash
pip install pypwr2
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Example

```python
from pwr2.pwr import pwr_1way

# Calculate power for one-way ANOVA
power = pwr_1way(k=5, n=15, alpha=0.05, f=None, delta=1.5, sigma=1, print_pretty=False)
print(round(power, 4))
# 0.9074
```

## Available Functions

- `pwr_1way()`: Calculate power for one-way ANOVA models
- `ss_1way()`: Calculate sample size for one-way ANOVA models
- `pwr_2way()`: Calculate power for two-way ANOVA models
- `ss_2way()`: Calculate sample size for two-way ANOVA models

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines.

### Quick Start for Contributors

The project includes a Makefile for convenient development tasks. Run `make help` to see all available commands.

```bash
# Clone the repository
git clone https://github.com/ConorMcNamara/pyPWR2.git
cd pyPWR2

# Complete development setup (install deps + pre-commit hooks)
make dev-setup

# Run tests with coverage
make test-coverage

# Run all code quality checks
make check

# Run everything (simulate CI locally)
make dev-check
```

<details>
<summary>Manual commands (if not using Make)</summary>

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
ruff check .

# Run type checking
mypy pwr2
```
</details>

## Notes

Whenever possible, I tried to follow the R naming and code-style to ensure as much 1-1 comparison as possible; however,
some liberties were taken to ensure the code follows modern Python best practices.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

Pengcheng Lu, Junhao Liu, Devin Koestler. (2017). pwr2: Power and Sample Size Analysis for One-way and Two-way ANOVA
Models. https://cran.r-project.org/web/packages/pwr2/index.html
