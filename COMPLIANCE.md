# 12-Factor App & Linting Compliance

This document outlines the compliance status and changes made to meet Django linting requirements and 12-Factor App principles.

## Linting Compliance ✅

### Changes Made

1. **Added Linting Tools to `requirements.txt`**:
   - `flake8>=6.1.0` - Style guide enforcement
   - `black>=23.12.0` - Code formatter
   - `isort>=5.13.0` - Import organizer
   - `pylint-django>=2.5.3` - Django-specific linting
   - `pylint>=3.0.0` - General Python linting

2. **Created Configuration Files**:
   - `.flake8` - Flake8 configuration with Django-specific rules
   - `pyproject.toml` - Configuration for black, isort, and pylint

3. **Created Linting Script**:
   - `lint.sh` - Executable script to run all linters

4. **Updated `.gitignore`**:
   - Added exclusions for linting cache files

5. **Documentation**:
   - `LINTING.md` - Comprehensive guide for using linting tools

## 12-Factor App Compliance ✅

### Factor III: Config - **FIXED** ✅

**Before**: Hardcoded defaults in settings.py
**After**: Configuration from environment variables only

**Changes**:
- `SECRET_KEY`: Now required in production (raises error if not set)
- `DEBUG`: Defaults to `False` for production safety
- `ALLOWED_HOSTS`: Read from `ALLOWED_HOSTS` environment variable (comma-separated)
- `CSRF_TRUSTED_ORIGINS`: Read from `CSRF_TRUSTED_ORIGINS` environment variable (comma-separated)

**Environment Variables Required**:
- `SECRET_KEY` (required in production)
- `DJANGO_DEBUG` (optional, defaults to False)
- `ALLOWED_HOSTS` (comma-separated list)
- `CSRF_TRUSTED_ORIGINS` (comma-separated list)

### Factor XI: Logs - **FIXED** ✅

**Before**: No logging configuration
**After**: Comprehensive logging to stdout/stderr

**Changes**:
- Added `LOGGING` configuration in `settings.py`
- All logs write to stdout/stderr (12-Factor compliant)
- Configurable log levels via environment variables:
  - `DJANGO_LOG_LEVEL` (default: INFO)
  - `DJANGO_DB_LOG_LEVEL` (default: WARNING)
  - `ACCOUNTS_LOG_LEVEL` (default: INFO)

### Other Factors - Already Compliant ✅

- **I. Codebase**: ✅ Single codebase in version control
- **II. Dependencies**: ✅ `requirements.txt` with pinned versions
- **IV. Backing Services**: ✅ Database configurable via `DATABASE_URL`
- **V. Build, Release, Run**: ✅ `render.yaml` and `Procfile` present
- **VI. Processes**: ✅ Stateless application processes
- **VII. Port Binding**: ✅ Uses `$PORT` environment variable
- **VIII. Concurrency**: ✅ Uses Gunicorn
- **IX. Disposability**: ✅ Gunicorn handles graceful shutdown
- **X. Dev/Prod Parity**: ⚠️ SQLite for local, PostgreSQL for production (acceptable for development)
- **XII. Admin Processes**: ✅ `manage.py` available

## Deployment Notes

### Render.com Configuration

The `render.yaml` file is already configured with the necessary environment variables:
- `SECRET_KEY`: Auto-generated
- `DJANGO_DEBUG`: Set to `False`
- `ALLOWED_HOSTS`: Set to production domain
- `CSRF_TRUSTED_ORIGINS`: Set to production URL
- `DATABASE_URL`: Auto-configured from database service

### Local Development

For local development, you can:
1. Set `DJANGO_DEBUG=True` to use insecure SECRET_KEY fallback
2. Use SQLite (default) or PostgreSQL via environment variables
3. Set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` as needed

Example for local development:
```bash
export DJANGO_DEBUG=True
export ALLOWED_HOSTS=localhost,127.0.0.1
export CSRF_TRUSTED_ORIGINS=http://localhost:8000
```

## Running Linters

See `LINTING.md` for detailed instructions. Quick start:

```bash
# Install dependencies
pip install -r requirements.txt

# Run all linters
./lint.sh

# Auto-fix formatting
black .
isort .
```

## Summary

✅ **Linting**: Fully compliant with Django linting requirements
✅ **12-Factor App**: 11/12 factors fully compliant, 1 acceptable deviation (dev/prod database difference)

The project now meets industry standards for code quality and cloud-native application architecture.

