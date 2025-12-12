# Procrast Local

A Django-based social media application for tracking and sharing procrastination experiences. Users can create posts about their procrastination activities, interact with posts through likes and dislikes, and compete on leaderboards based on hours procrastinated.

## Features

- **User Authentication**: Sign up, login, and logout functionality
- **Post Creation**: Create posts with title, description, and hours procrastinated
- **Social Interaction**: Like and dislike posts (mutually exclusive)
- **Leaderboards**: 
  - Post leaderboard sorted by likes, dislikes, or time
  - User leaderboard ranked by total hours procrastinated
- **Real-time Updates**: Check for new posts via API endpoint
- **A/B Testing**: Built-in A/B testing functionality for button variants
- **Modern UI**: Responsive design with gradient styling

## Project Structure

```
procrast-local/
├── manage.py
├── requirements.txt
├── Procfile
├── render.yaml
├── procrast_local/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── models.py          # Post, Like, Dislike, ABTest models
│   ├── views.py           # All view logic
│   ├── urls.py            # URL routing
│   └── admin.py
└── templates/
    ├── base.html
    └── accounts/
        ├── login.html
        ├── signup.html
        ├── home.html
        ├── create_post.html
        ├── leaderboard.html
        ├── user_leaderboard.html
        └── abtest.html
```

## Local Development Setup

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
   - Signup page: http://127.0.0.1:8000/signup/
   - Home page: http://127.0.0.1:8000/ (requires login)
   - Admin panel: http://127.0.0.1:8000/admin/ (requires superuser)

## Local Development with PostgreSQL

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

1. Dump data from SQLite:
   ```bash
   python manage.py dumpdata --natural-primary --natural-foreign --indent 2 > data.json
   ```

2. Set the Postgres environment variables (as above), then apply migrations:
   ```bash
   python manage.py migrate
   ```

3. Load the data into Postgres:
   ```bash
   python manage.py loaddata data.json
   ```

## Deployment on Render

This project includes a `render.yaml` configuration file for easy deployment on Render. The configuration automatically sets up both a PostgreSQL database and a web service.

### Deployment Steps

#### Option 1: Using render.yaml (Recommended)

1. **Push your code** to a Git repository (GitHub, GitLab, or Bitbucket)

2. **Connect to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" and select "Blueprint"
   - Connect your repository
   - Render will automatically detect the `render.yaml` file

3. **Review and Deploy:**
   - Render will create both the PostgreSQL database and web service
   - The database connection will be automatically configured
   - Click "Apply" to deploy

4. **Environment Variables:**
   The `render.yaml` file automatically configures most environment variables. However, you may need to manually set or update:
   - `ALLOWED_HOSTS` - Your Render domain (e.g., `your-app.onrender.com`)
   - `CSRF_TRUSTED_ORIGINS` - Your Render URL (e.g., `https://your-app.onrender.com`)

#### Option 2: Manual Setup

If you prefer to set up services manually:

1. **Create a PostgreSQL Database:**
   - Go to Render Dashboard → "New +" → "PostgreSQL"
   - Choose a name and plan
   - Note the connection details

2. **Create a Web Service:**
   - Go to Render Dashboard → "New +" → "Web Service"
   - Connect your repository
   - Configure the service:
     - **Build Command:** `pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput`
     - **Start Command:** `gunicorn procrast_local.wsgi:application --bind 0.0.0.0:$PORT`

3. **Set Environment Variables:**
   In the web service's "Environment" tab, add the following variables:

### Environment Variables

The following environment variables are used by the application:

#### Required Variables:

- `SECRET_KEY` - Django secret key (auto-generated by Render if using `generateValue: true`)
- `DATABASE_URL` - PostgreSQL connection string (automatically set when database is linked)
  - OR use individual Postgres variables:
    - `POSTGRES_DB` - Database name
    - `POSTGRES_USER` - Database user
    - `POSTGRES_PASSWORD` - Database password
    - `POSTGRES_HOST` - Database host
    - `POSTGRES_PORT` - Database port (default: 5432)

#### Optional Variables:

- `PYTHON_VERSION` - Python version (default: 3.11.0)
- `DJANGO_DEBUG` - Set to `False` for production (default: `True`)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts (or use `ADDITIONAL_ALLOWED_HOSTS` to append)
- `ADDITIONAL_ALLOWED_HOSTS` - Additional hosts to append to `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS` - Comma-separated list of trusted origins (or use `ADDITIONAL_CSRF_TRUSTED_ORIGINS` to append)
- `ADDITIONAL_CSRF_TRUSTED_ORIGINS` - Additional origins to append to `CSRF_TRUSTED_ORIGINS`

### Post-Deployment

After deployment:

1. **Create a superuser** (if needed):
   - Use Render's shell: `python manage.py createsuperuser`
   - Or run locally with `DATABASE_URL` set to your Render database

2. **Verify the deployment:**
   - Check that migrations ran successfully
   - Verify static files are being served
   - Test the application endpoints

### Notes

- The `render.yaml` file automatically runs migrations during the build process
- Static files are handled by WhiteNoise middleware
- The app automatically uses `DATABASE_URL` if available, or falls back to individual Postgres variables
- Health checks are configured at the root path (`/`)

## Creating Test Users

You can create users in two ways:

1. **Via Django admin:**
   - Go to `/admin/`
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

3. **Via signup page:**
   - Navigate to `/signup/`
   - Fill in username, email, and password
   - Password must be at least 8 characters long

## Technology Stack

- **Backend:** Django 4.2+
- **Database:** PostgreSQL (production) / SQLite (local development)
- **Web Server:** Gunicorn
- **Static Files:** WhiteNoise
- **Deployment:** Render
