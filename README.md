# Procrast Local - Django Authentication App

A Django application with user login functionality and a modern front-end interface.

## Features

- User authentication (login/logout)
- Modern, responsive login page
- Protected home page for authenticated users
- Beautiful gradient UI design

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**
   - Login page: http://127.0.0.1:8000/login/
   - Home page: http://127.0.0.1:8000/ (requires login)
   - Admin panel: http://127.0.0.1:8000/admin/ (requires superuser)

## Use PostgreSQL Instead of SQLite

This project can auto-switch to PostgreSQL if the following environment variables are set:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST` (default: `localhost`)
- `POSTGRES_PORT` (default: `5432`)

Example for bash/zsh (temporary, current shell only):
```bash
export POSTGRES_DB=procrast_local
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=changeme
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

Then run:
```bash
pip install -r requirements.txt
python manage.py migrate
```

### Migrating Existing Data from SQLite to Postgres
If you already have data in `db.sqlite3`, you can migrate it:

1) Dump data from SQLite:
```bash
python manage.py dumpdata --natural-primary --natural-foreign --indent 2 > data.json
```

2) Set the Postgres environment variables (as above), then apply migrations:
```bash
python manage.py migrate
```

3) Load the data into Postgres:
```bash
python manage.py loaddata data.json
```

Notes:
- Ensure your Postgres database exists and your user has privileges.
- If you see integrity errors while loading, try loading only the `auth` and `contenttypes` apps first, or exclude content types from the dump. In many cases the full dump works fine with `--natural-*` flags.

## Creating Test Users

You can create users in two ways:

1. **Via Django admin:**
   - Go to http://127.0.0.1:8000/admin/
   - Login with superuser credentials
   - Navigate to Users and create a new user

2. **Via Django shell:**
   ```bash
   python manage.py shell
   ```
   Then run:
   ```python
   from django.contrib.auth.models import User
   User.objects.create_user('testuser', 'test@example.com', 'testpass123')
   ```

## Project Structure

```
procrast-local/
├── manage.py
├── requirements.txt
├── procrast_local/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
└── templates/
    ├── base.html
    └── accounts/
        ├── login.html
        └── home.html
```

## Default Login Credentials

After creating a superuser, you can use those credentials to login. Or create a test user as described above.

