# Steward — Remaining Scaffolding Steps

_Generated 2026-05-07_

## Current Status

- [x] Repo created
- [x] Virtual environment set up
- [x] Dependencies installed
- [x] Django project initialized (`config/`)
- [x] `core` app created
- [x] `CustomUser` model defined
- [x] `AUTH_USER_MODEL` set in settings
- [x] `core` added to `INSTALLED_APPS`
- [ ] `settings.py` updated with decouple + PostgreSQL
- [ ] `.env` file created
- [ ] Local database created
- [ ] Migrations run
- [ ] Superuser created
- [ ] Server verified

---

## Step 6 — Update `settings.py`

Replace the top of `settings.py`:

```python
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool, default=True)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
```

Replace the `DATABASES` block:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

Add `rest_framework` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'core',
]
```

---

## Step 7 — Create `.env`

Create `.env` in the project root (same level as `manage.py`):

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=steward
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

Add `.env` to `.gitignore`.

---

## Step 8 — Create the local database

```bash
createdb steward
```

Or create via psql/pgAdmin if preferred.

---

## Step 9 — Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Step 10 — Create superuser

```bash
python manage.py createsuperuser
```

Set this user up with both `is_staff=True` and `is_admin=True` after creation via the shell:

```bash
python manage.py shell
```

```python
from core.models import CustomUser
u = CustomUser.objects.get(username='admin')
u.is_admin = True
u.save()
```

---

## Step 11 — Verify

```bash
python manage.py runserver
```

- Hit `localhost:8000/admin` — login page should load
- Log in with your superuser — Django admin should load
- Confirm `CustomUser` appears in the admin

If all three pass, scaffolding is complete.

---

## Next Stage: Auth & Permissions

Once scaffolding is verified, the next stage is wiring up auth:

- `LoginRequiredMixin` on all views
- `UserPassesTestMixin` for role enforcement
- Login/logout URLs
- Role-based redirects on login (`is_donor` → `/dashboard/`, `is_admin` → `/staff/grants/`)
