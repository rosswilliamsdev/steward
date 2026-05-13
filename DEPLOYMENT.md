# Deployment Guide — Steward on Render

This guide walks through deploying Steward to Render's free tier for portfolio/interview demonstrations.

## Why Render?

- Free tier includes PostgreSQL
- Simpler than Railway for Django projects
- Good static file handling out of the box
- One-click deploy from GitHub

**Trade-off:** Free tier spins down after 15 min inactivity (first load takes ~30s). Upgrade to $7/mo for always-on if actively interviewing.

---

## Pre-Deployment Setup

### 1. Install Production Dependencies

```bash
pip install dj-database-url whitenoise gunicorn psycopg2-binary
pip freeze > requirements.txt
```

### 2. Update `config/settings.py`

Add this production configuration block at the end of your settings file:

```python
# Production settings (Render)
import os
import dj_database_url

if os.environ.get('RENDER'):
    DEBUG = False
    ALLOWED_HOSTS = ['.onrender.com']

    # Database (Render provides DATABASE_URL)
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

    # Static files (WhiteNoise)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # Security
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    # Keep existing dev settings
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

### 3. Add WhiteNoise Middleware

In `config/settings.py`, update the `MIDDLEWARE` list:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line (second position)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ... rest of middleware
]
```

### 4. Create Build Script

Create `build.sh` in project root:

```bash
#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Seed demo data
python manage.py seed_demo
```

Make it executable:

```bash
chmod +x build.sh
```

### 5. Create Demo Data Seeder

Create `core/management/commands/seed_demo.py`:

```python
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Fund, Contribution, GrantRecommendation
from decimal import Decimal
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds demo data for portfolio showcase'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing demo data...')

        # Clear existing non-superuser data
        GrantRecommendation.objects.all().delete()
        Contribution.objects.all().delete()
        Fund.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creating demo users...')

        # Create staff user
        staff = User.objects.create_user(
            username='staff',
            password='demo123',
            email='staff@steward.demo',
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_admin=True
        )

        # Create donor users
        donor1 = User.objects.create_user(
            username='donor',
            password='demo123',
            email='donor@steward.demo',
            first_name='Jane',
            last_name='Smith',
            is_donor=True
        )

        donor2 = User.objects.create_user(
            username='donor2',
            password='demo123',
            email='donor2@steward.demo',
            first_name='Robert',
            last_name='Johnson',
            is_donor=True
        )

        self.stdout.write('Creating funds...')

        # Create funds
        fund1 = Fund.objects.create(
            name="Smith Family Foundation",
            donor=donor1
        )

        fund2 = Fund.objects.create(
            name="Johnson Education Fund",
            donor=donor2
        )

        self.stdout.write('Creating contributions...')

        # Seed contributions for fund1
        Contribution.objects.create(
            fund=fund1,
            amount=Decimal('50000.00'),
            date=date(2024, 1, 15),
            created_by=staff
        )
        Contribution.objects.create(
            fund=fund1,
            amount=Decimal('25000.00'),
            date=date(2024, 6, 10),
            created_by=staff
        )
        Contribution.objects.create(
            fund=fund1,
            amount=Decimal('10000.00'),
            date=date(2024, 11, 5),
            created_by=staff
        )

        # Seed contributions for fund2
        Contribution.objects.create(
            fund=fund2,
            amount=Decimal('100000.00'),
            date=date(2024, 3, 1),
            created_by=staff
        )
        Contribution.objects.create(
            fund=fund2,
            amount=Decimal('50000.00'),
            date=date(2024, 9, 15),
            created_by=staff
        )

        self.stdout.write('Creating grant recommendations...')

        # Seed grant recommendations for fund1
        GrantRecommendation.objects.create(
            fund=fund1,
            nonprofit_name="Local Food Bank",
            amount=Decimal('5000.00'),
            purpose="Monthly meal program support",
            status='approved',
            reviewed_by=staff,
            staff_note="Approved - established nonprofit with strong track record"
        )

        GrantRecommendation.objects.create(
            fund=fund1,
            nonprofit_name="Youth Literacy Program",
            amount=Decimal('3000.00'),
            purpose="After-school reading initiative",
            status='pending'
        )

        GrantRecommendation.objects.create(
            fund=fund1,
            nonprofit_name="Community Arts Center",
            amount=Decimal('2500.00'),
            purpose="Art supplies for underserved schools",
            status='approved',
            reviewed_by=staff
        )

        # Seed grant recommendations for fund2
        GrantRecommendation.objects.create(
            fund=fund2,
            nonprofit_name="State University Scholarship Fund",
            amount=Decimal('25000.00'),
            purpose="Engineering scholarships for first-gen students",
            status='approved',
            reviewed_by=staff
        )

        GrantRecommendation.objects.create(
            fund=fund2,
            nonprofit_name="STEM Education Coalition",
            amount=Decimal('15000.00'),
            purpose="K-12 robotics program equipment",
            status='pending'
        )

        self.stdout.write(self.style.SUCCESS('✓ Demo data seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('  Donor: username=donor, password=demo123'))
        self.stdout.write(self.style.SUCCESS('  Staff: username=staff, password=demo123'))
```

Test it locally:

```bash
python manage.py seed_demo
```

### 6. Update Login Page with Demo Credentials

The login page at `core/templates/registration/login.html` now displays demo account credentials directly, eliminating the need for a separate landing page. Demo users see:

- **Donor View:** `donor` / `demo123`
- **Staff View:** `staff` / `demo123`

### 7. Commit Everything

```bash
git add .
git commit -m "chore: add production deployment configuration"
git push origin main
```

---

## Deploy to Render

### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### Step 2: Create PostgreSQL Database

1. Click **New +** → **PostgreSQL**
2. Configure:
   - **Name:** steward-db
   - **Database:** steward
   - **User:** steward
   - **Region:** Choose closest to you
   - **Plan:** Free
3. Click **Create Database**
4. Wait 2-3 minutes for provisioning

### Step 3: Create Web Service

1. Click **New +** → **Web Service**
2. Connect your GitHub repo: `steward`
3. Configure:
   - **Name:** steward-demo (or your preferred name)
   - **Region:** Same as database
   - **Branch:** main
   - **Runtime:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn config.wsgi:application`
   - **Plan:** Free

### Step 4: Add Environment Variables

In the web service settings, add:

| Key              | Value                                                                                                                            |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `RENDER`         | `1`                                                                                                                              |
| `PYTHON_VERSION` | `3.11.0`                                                                                                                         |
| `SECRET_KEY`     | Generate a new one: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |

### Step 5: Connect Database

1. In web service settings, scroll to **Environment**
2. Click **Add Environment Variable**
3. Select **Add from Database** dropdown
4. Choose `steward-db` → `Internal Database URL`
5. This auto-adds `DATABASE_URL`

### Step 6: Deploy

1. Click **Create Web Service**
2. Render will:
   - Clone your repo
   - Run `build.sh` (install deps, collect static, migrate, seed data)
   - Start gunicorn
3. First deploy takes 3-5 minutes
4. You'll get a URL like: `https://steward-demo.onrender.com`

---

## Verify Deployment

1. Visit your Render URL (e.g., `https://steward-demo.onrender.com`)
2. Should see **login page** with demo credentials displayed
3. Test **Donor Account** (`donor` / `demo123`):
   - Should redirect to `/` (dashboard)
   - Interactive React dashboard with balance chart
   - Smith Family Foundation fund details
   - Can view `/grants/` and `/funds/`
   - Can create new grant recommendations
4. Test **Staff Account** (`staff` / `demo123`):
   - Should redirect to `/` (dashboard shows admin view)
   - Go to `/admin/` for Django admin panel
   - Can view all funds across all donors
   - Can approve/deny grant recommendations
   - Can log new contributions

---

## Troubleshooting

### Build fails with "permission denied: ./build.sh"

Locally run:

```bash
chmod +x build.sh
git add build.sh
git commit -m "fix: make build script executable"
git push
```

Render will auto-redeploy.

### Static files not loading (no CSS)

Check that:

- WhiteNoise middleware is installed (step 3)
- `STATIC_ROOT` is set in production settings
- `collectstatic` runs in `build.sh`

View logs in Render dashboard → Logs tab.

### Database connection error

Verify:

- `DATABASE_URL` environment variable exists (added in Step 5)
- `dj-database-url` is in `requirements.txt`

### Seed data not appearing

Check build logs in Render dashboard for `seed_demo` errors. Common issues:

- Unique constraint violations (run `python manage.py flush` locally first)
- Missing model fields

---

## Interview Prep

### What to highlight (for non-technical interviewers):

1. **It's live software** — Not just code on GitHub, it's running on the internet
2. **Real-world problem** — DAFs are complex: multi-user, workflows, money
3. **Production-ready patterns** — Role-based permissions, data integrity, REST API
4. **Full-stack** — Backend (Django), frontend (React), database (PostgreSQL), deployment (Render)
5. **Solo build** — Planned, designed, and shipped in one week

### Sample talking points:

> "This is a donor-advised fund management platform—think of it like a mini-foundation where donors contribute money, recommend grants to nonprofits, and staff approve them. I built it to demonstrate production Django patterns: multi-user roles, approval workflows, data integrity, and a React dashboard pulling from a REST API."

> "It's deployed with continuous deployment—every push to main automatically rebuilds and deploys. The database is PostgreSQL, static files are served via WhiteNoise, and it's all running on Render's infrastructure."

> "You can log in as a donor to see their custom dashboard—interactive React charts showing fund balance over time, recent grants, and contribution history. Or log in as staff to access the Django admin panel where you can approve grant recommendations, log new contributions, and manage all donor accounts."

### Send this in applications:

**Live Demo:** https://your-app.onrender.com
**GitHub:** https://github.com/yourusername/steward
**Demo Credentials:** donor/demo123 or staff/demo123

---

## Maintenance

### Updating the app after deployment:

```bash
# Make changes locally
git add .
git commit -m "feat: your change"
git push origin main
```

Render auto-deploys on push to main (takes ~2-3 min).

### Manually trigger deploy:

Render dashboard → your web service → **Manual Deploy** → Deploy latest commit

### View logs:

Render dashboard → your web service → **Logs** tab (real-time)

---

## Cost & Limits (Free Tier)

- **Web service:** Free, spins down after 15 min inactivity (cold start ~30s)
- **PostgreSQL:** Free, 90-day expiration (resets with activity)
- **Bandwidth:** 100 GB/month free
- **Build minutes:** 500/month free

**Upgrade to $7/mo** for always-on (recommended if actively interviewing).

---

## Next Steps After Deployment

1. ✅ Test both demo accounts thoroughly
2. ✅ Add live URL to your resume/LinkedIn
3. ✅ Screenshot key views for your portfolio
4. ✅ Practice explaining the architecture in 2 minutes
5. ✅ Send to hiring managers with context

---

**Questions or issues?** Check Render's [Django deployment guide](https://render.com/docs/deploy-django) or open an issue in this repo.
