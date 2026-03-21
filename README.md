# Radhe Cars

A used car marketplace web application focused on Gujarat, India. Buy and sell pre-owned cars with an easy-to-use interface.

## Features

- **Browse Cars** – Filter by brand, fuel type, transmission, price, year, and more
- **Car Details** – Image gallery, specifications, price, seller contact
- **Sell Car** – Step-by-step form to list your car (brand, model, variant, photos, price)
- **Wishlist** – Save cars for later (requires login)
- **User Auth** – Email/password signup and Google OAuth login
- **Responsive UI** – Mobile-friendly design with sticky filters

## Tech Stack

- **Backend:** Django 5.x
- **Database:** PostgreSQL
- **Auth:** django-allauth (email + Google OAuth)
- **Frontend:** HTML, Tailwind CSS, vanilla JavaScript

## Prerequisites

- Python 3.10+
- PostgreSQL 12+
- pip / venv

## Local Setup

### 1. Clone and enter project

```bash
cd "Radhe Auto Project 1"
```

### 2. Create virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install psycopg2-binary
```

### 4. Configure environment

Copy `.env.example` to `.env` and fill in your values (optional for local dev):

```bash
cp .env.example .env
```

Or create a `.env` file manually:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DB_NAME=radhe_auto
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Google OAuth (for login)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 5. Create database

```bash
# In PostgreSQL
createdb radhe_auto
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 8. Collect static files (for production-style run)

```bash
python manage.py collectstatic --noinput
```

### 9. Run development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000

---

## Deployment

### Production checklist

Before deploying:

1. Set `DEBUG=False`
2. Set a strong `SECRET_KEY` (e.g. from `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
3. Set `ALLOWED_HOSTS` to your domain(s)
4. Use environment variables for DB credentials and OAuth
5. Serve static files (Whitenoise or CDN)
6. Use a production WSGI server (Gunicorn)
7. Use HTTPS

### Option A: Railway / Render / Fly.io

1. Add `requirements.txt` (already present). Add for production:

   ```
   gunicorn
   whitenoise
   psycopg2-binary
   ```

2. Create `Procfile` (Railway/Render):

   ```
   web: gunicorn radhe_cars.wsgi --bind 0.0.0.0:$PORT
   ```

3. Set environment variables in the platform dashboard:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-domain.com`
   - `DATABASE_URL` (if supported) or `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
   - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`

4. Add build command: `python manage.py collectstatic --noinput`
5. Add start command: `gunicorn radhe_cars.wsgi`

### Option B: VPS (Ubuntu) with Nginx + Gunicorn

1. Install Python, PostgreSQL, Nginx
2. Clone project and set up venv
3. Install: `pip install gunicorn whitenoise psycopg2-binary`
4. Update `settings.py` for production (see below)
5. Run Gunicorn: `gunicorn radhe_cars.wsgi:application --bind 0.0.0.0:8000`
6. Configure Nginx as reverse proxy
7. Use systemd or supervisor to keep Gunicorn running

### Option C: PythonAnywhere

1. Upload project
2. Create virtualenv and install requirements
3. Add `radhe-cars.pythonanywhere.com` to `ALLOWED_HOSTS`
4. Configure PostgreSQL (or use SQLite for small scale)
5. Set up static files and media in Web app config
6. Point WSGI to `radhe_cars.wsgi`

---

## Production settings example

Add to `radhe_cars/settings.py` or use a separate `settings_production.py`:

```python
import os

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Static files with Whitenoise
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database from env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'radhe_auto'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

---

## Project structure

```
Radhe Auto Project 1/
├── cars/                 # Main app (models, views, urls)
├── radhe_cars/           # Project settings, urls, wsgi
├── templates/            # HTML templates
│   ├── partials/         # Header, footer, car card, CTA
│   └── cars/             # Car list, detail, sell, etc.
├── media/                # User uploads (car images)
├── static/               # CSS, JS, images
├── requirements.txt
├── manage.py
└── README.md
```

---

## Environment variables reference

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | (dev key) |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated hosts | `*` |
| `DB_NAME` | PostgreSQL database name | `radhe_auto` |
| `DB_USER` | PostgreSQL user | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | - |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | - |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret | - |

---

## License

© 2026 Radhe Cars. All rights reserved.
