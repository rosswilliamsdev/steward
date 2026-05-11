# Steward

> A Django application for managing donor-advised funds at nonprofit community foundations.

![Django](https://img.shields.io/badge/Django-6.0-brightgreen) ![Python](https://img.shields.io/badge/Python-3.14-blue) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue) ![React](https://img.shields.io/badge/React-19-61dafb) ![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38bdf8)

## Overview

Steward demonstrates production-level backend engineering for a real-world domain: donor-advised fund management. It models named funds, contributions, grant recommendations, and staff approval workflows with role-based permissions and a minimal React integration for an interactive donor dashboard.

**Built in one week as a portfolio project** to showcase Django expertise for Web Application Developer roles at nonprofit community foundations.

### Key Features

- **Donor Portal**: View fund balances, contribution history, grant recommendations with interactive charts
- **Grant Recommendations**: Donors submit grant requests; staff approve/deny with public notes
- **Staff Admin**: Full CRUD for funds, contributions, and grant workflow management
- **PDF Export**: Generate fund statements using xhtml2pdf
- **Role-Based Access**: Two-role system (`is_donor` / `is_admin`) with strict permission enforcement
- **Real-Time Balance**: Computed on-demand to eliminate race conditions during concurrent grant approvals

## Tech Stack

| Layer          | Technology                                      |
| -------------- | ----------------------------------------------- |
| **Backend**    | Django 6.0, Django REST Framework               |
| **Database**   | PostgreSQL                                      |
| **Frontend**   | Django templates + React 19 (dashboard only)    |
| **Styling**    | Tailwind CSS                                    |
| **Charts**     | Recharts                                        |
| **Components** | Radix UI (accessible headless components)       |
| **PDF Export** | xhtml2pdf (pure Python, no system dependencies) |
| **Deployment** | Railway/Render (free tier)                      |

## Architecture Highlights

### 1. Computed Balance Property

Fund balance is a model property (`sum(contributions) - sum(approved_grants)`), not a stored field. This eliminates race conditions during concurrent grant approvals—no optimistic locking or database transactions needed.

### 2. Django-First UI

Primary interface uses Django Class-Based Views and templates. React is reserved for a single interactive component (donor dashboard with charts), demonstrating justified framework integration rather than over-engineering.

### 3. Two-Role Permission System

Custom `is_donor` and `is_admin` fields on `CustomUser` gate all views via `UserPassesTestMixin`. No donor ever sees another donor's data.

## Data Models

```python
CustomUser (extends AbstractUser)
├── is_donor: bool
└── is_admin: bool

Fund
├── name: str
├── donor: FK → CustomUser
├── balance: @property  # computed, not stored
└── created_at: datetime

Contribution
├── fund: FK → Fund
├── amount: Decimal
├── date: date
├── note: str (optional)
├── created_by: FK → CustomUser (staff)
└── created_at: datetime

GrantRecommendation
├── fund: FK → Fund
├── nonprofit_name: str
├── amount: Decimal
├── memo: str (optional)
├── status: 'pending' | 'approved' | 'denied'
├── staff_note: str (optional, visible to donor)
├── reviewed_by: FK → CustomUser (nullable)
├── reviewed_at: datetime (nullable)
└── created_at: datetime
```

## Getting Started

### Prerequisites

- Python 3.14+
- PostgreSQL 14+
- Node.js 18+ (for Tailwind CSS and React build)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/rosswilliamsdev/steward.git
   cd steward
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node dependencies**

   ```bash
   npm install
   ```

5. **Set up environment variables**

   Create a `.env` file in the project root:

   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=postgresql://user:password@localhost:5432/steward
   ```

6. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

7. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

8. **Load sample data (optional)**

   ```bash
   python load_sample_data.py
   ```

9. **Build Tailwind CSS**

   ```bash
   npm run build:css
   ```

10. **Build React dashboard component**
    ```bash
    npm run build
    ```

### Running the Application

**Start the Django development server:**

```bash
python manage.py runserver
```

**Watch Tailwind CSS for changes (separate terminal):**

```bash
npm run watch:css
```

**Watch React builds for changes (separate terminal):**

```bash
npm run dev
```

Visit [http://localhost:8000](http://localhost:8000) to access the application.

## Usage

### For Donors

1. Log in with donor credentials
2. View your dashboard with fund balance, charts, and recent grants
3. Navigate to **My Grants** to submit new grant recommendations
4. Track recommendation status (pending/approved/denied)
5. Export fund statements as PDF

### For Staff

1. Log in with admin credentials
2. Access **Staff Portal** to:
   - Create new funds for donors
   - Log contributions
   - Review pending grant recommendations
   - Approve or deny grants with public notes
3. Use Django admin at `/admin/` for advanced management

## Development

### Project Structure

```
steward/
├── core/                    # Main Django app
│   ├── models.py           # User, Fund, Contribution, GrantRecommendation
│   ├── views.py            # CBVs for donor and staff views
│   ├── serializers.py      # DRF serializers for API
│   ├── forms.py            # Django forms
│   ├── templates/          # Django templates
│   └── admin.py            # Django admin customization
├── steward/                # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── frontend/               # React components
│   └── DonorDashboard.jsx
├── static/                 # Static assets
│   └── css/styles.css     # Compiled Tailwind CSS
├── .claude/               # Project documentation
│   ├── context/
│   │   ├── PRD.md         # Product requirements
│   │   └── design-system.md
│   └── docs/
├── requirements.txt
├── package.json
└── tailwind.config.js
```

### Commands

| Task               | Command                            |
| ------------------ | ---------------------------------- |
| Run dev server     | `python manage.py runserver`       |
| Build Tailwind CSS | `npm run build:css`                |
| Watch Tailwind CSS | `npm run watch:css`                |
| Build React        | `npm run build`                    |
| Watch React        | `npm run dev`                      |
| Run tests          | `python manage.py test`            |
| Make migrations    | `python manage.py makemigrations`  |
| Apply migrations   | `python manage.py migrate`         |
| Create superuser   | `python manage.py createsuperuser` |

### Testing

Run the test suite:

```bash
python manage.py test
```

Run tests with coverage:

```bash
coverage run --source='.' manage.py test
coverage report
```

### Git Workflow

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `style:` formatting, CSS changes
- `refactor:` code restructuring
- `test:` adding/updating tests
- `chore:` maintenance tasks

Group changes into logical commits—never commit all changes at once.

## Design System

The project uses a custom design system built on Tailwind CSS. All design tokens (colors, typography, spacing, shadows) are defined in [tailwind.config.js](tailwind.config.js) and documented in [.claude/context/design-system.md](.claude/context/design-system.md).

### Brand Colors

- **Primary**: `#047857` (Emerald 700) — Trust, growth, stewardship
- **Secondary**: `#0369A1` (Sky 700) — Stability, clarity
- **Accent**: `#7C3AED` (Violet 600) — Innovation, impact

See the full design system documentation for typography, spacing, and component specifications.

## Documentation

Detailed planning and architecture documents are in [.claude/](.claude/):

- [PRD.md](.claude/context/PRD.md) — Product requirements, data models, feature scope
- [design-system.md](.claude/context/design-system.md) — Visual tokens, color palette, typography
- [CLAUDE.md](CLAUDE.md) — Development conventions, architecture decisions

## Deployment

### Railway

1. Create a new project on [Railway](https://railway.app/)
2. Add a PostgreSQL database
3. Connect your GitHub repository
4. Set environment variables:
   - `SECRET_KEY`
   - `DATABASE_URL` (automatically set by Railway)
   - `ALLOWED_HOSTS`
5. Deploy

### Render

1. Create a new web service on [Render](https://render.com/)
2. Add a PostgreSQL database
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt && npm install && npm run build:css && npm run build`
5. Set start command: `python manage.py migrate && gunicorn steward.wsgi`
6. Add environment variables
7. Deploy

## Future Enhancements

- [ ] Email notifications for grant status changes
- [ ] Nonprofit verification via IRS API
- [ ] Cause area categorization with grants-by-category chart
- [ ] Donor self-registration with staff approval

## License

This is a portfolio project. Feel free to reference the code for learning purposes.

## Author

**Ross Williams**

- GitHub: [@rosswilliamsdev](https://github.com/rosswilliamsdev)
- Portfolio: [rosswilliams.dev](https://rosswilliams.dev)
