# Linting and Code Quality

This project uses several linting and code formatting tools to maintain code quality and consistency.

## Tools

- **black**: Code formatter for Python
- **isort**: Import statement organizer
- **flake8**: Style guide enforcement
- **pylint-django**: Django-specific linting rules for pylint

## Installation

All linting tools are included in `requirements.txt`. Install them with:

```bash
pip install -r requirements.txt
```

## Running Linters

### Quick Check (All Tools)

Run the provided script to check all code:

```bash
./lint.sh
```

### Individual Tools

#### Format Code with Black

```bash
# Check formatting (dry-run)
black --check --diff .

# Auto-format code
black .
```

#### Sort Imports with isort

```bash
# Check import sorting (dry-run)
isort --check-only --diff .

# Auto-sort imports
isort .
```

#### Lint with flake8

```bash
flake8 .
```

#### Lint with pylint

```bash
pylint accounts/ procrast_local/ --load-plugins=pylint_django
```

## Configuration Files

- **`.flake8`**: Configuration for flake8
- **`pyproject.toml`**: Configuration for black, isort, and pylint

## Pre-commit Hooks (Optional)

To automatically run linters before each commit, you can set up pre-commit hooks:

1. Install pre-commit: `pip install pre-commit`
2. Create `.pre-commit-config.yaml` with your desired hooks
3. Run: `pre-commit install`

## CI/CD Integration

For continuous integration, add linting checks to your CI pipeline:

```yaml
# Example GitHub Actions
- name: Run linters
  run: |
    pip install -r requirements.txt
    ./lint.sh
```

## Auto-fixing Issues

Most formatting issues can be auto-fixed:

```bash
black .
isort .
```

Note: Some linting issues (like complexity warnings) require manual code changes.

