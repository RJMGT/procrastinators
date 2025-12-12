#!/bin/bash
# Linting script for Django project
# Run all linting tools to check code quality

set -e

echo "Running code formatters and linters..."
echo ""

# Check if tools are installed
if ! command -v black &> /dev/null; then
    echo "Error: black is not installed. Run: pip install -r requirements.txt"
    exit 1
fi

if ! command -v isort &> /dev/null; then
    echo "Error: isort is not installed. Run: pip install -r requirements.txt"
    exit 1
fi

if ! command -v flake8 &> /dev/null; then
    echo "Error: flake8 is not installed. Run: pip install -r requirements.txt"
    exit 1
fi

# Format code with black
echo "1. Formatting code with black..."
black --check --diff .

# Sort imports with isort
echo ""
echo "2. Checking import sorting with isort..."
isort --check-only --diff .

# Lint with flake8
echo ""
echo "3. Linting with flake8..."
flake8 .

# Optional: Run pylint (can be slow)
if command -v pylint &> /dev/null; then
    echo ""
    echo "4. Running pylint (this may take a while)..."
    pylint accounts/ procrast_local/ --load-plugins=pylint_django || true
else
    echo ""
    echo "4. Skipping pylint (not installed or not in PATH)"
fi

echo ""
echo "✅ Linting complete!"
echo ""
echo "To auto-fix formatting issues, run:"
echo "  black ."
echo "  isort ."

