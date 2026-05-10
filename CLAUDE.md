# Steward — Django Donor-Advised Fund Manager

## Overview

**Steward** is a portfolio-grade Django web application for managing donor-advised funds at a nonprofit community foundation. It demonstrates production-level backend engineering: modeling a real-world domain (named funds, contributions, grant recommendations, staff approval workflows), implementing role-based permissions, and integrating a minimal React component for an interactive donor dashboard.

**Tech Stack:** Django 5.x · PostgreSQL · Django REST Framework · React 18 · Tailwind CSS · Recharts · Radix UI
**Timeline:** 1 week solo build
**Deployment:** Railway or Render (free tier)

## Project Documentation

All detailed planning documents live in [.claude/docs/](.claude/docs/):

- **[PRD.md](.claude/context/PRD.md)** — Full product requirements: data models, user roles, feature scope, constraints
- **[backend-planning.md](.claude/backend-planning.md)** — Django architecture, views, forms, admin customization
- **[frontend-planning.md](.claude/frontend-planning.md)** — React dashboard component, charts, DRF API integration
- **[design-system.md](.claude/context/design-system.md)** — Visual tokens, color palette, typography, component specifications

## Git Workflow

- Never commit all changes in a single commit
- Group changes into logical commits before pushing
- Follow Conventional Commits format: `type: short description`
- Example sequence for a new feature:
  - `feat: add grant approval model`
  - `feat: add grant approval views`
  - `test: add grant approval tests`
  - `chore: update grant approval routes`

## Commands

### Development

```bash
python manage.py runserver
```

### Tailwind CSS Build

```bash
npm run build:css    # Build Tailwind CSS once
npm run watch:css    # Watch for changes and rebuild
```

### Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### Testing

```bash
python manage.py test
```

### Create Superuser

```bash
python manage.py createsuperuser
```

## Key Architecture Decisions

1. **Computed Balance:** Fund balance is a model property (sum of contributions minus approved grants), not a stored field — eliminates race conditions during concurrent grant approvals
2. **Django-First UI:** Primary interface uses Django templates + minimal vanilla JS; React reserved for the single interactive donor dashboard
3. **Two-Role System:** `is_donor` and `is_admin` custom User fields gate all views; enforced via `UserPassesTestMixin`
4. **No Payment Processing:** Staff manually logs contributions; no Stripe/payment gateway in v1
5. **PDF Export:** Uses `xhtml2pdf` (pure Python, no system dependencies) for fund statements

## Data Models

- **User** (extends `AbstractUser`) — `is_donor`, `is_admin` flags
- **Fund** — `name`, `donor` FK, computed `balance` property
- **Contribution** — `fund` FK, `amount`, `date`, `created_by` (staff)
- **GrantRecommendation** — `fund` FK, `nonprofit_name`, `amount`, `status` (pending/approved/denied), `reviewed_by`, `staff_note`

See [PRD.md → Data Models](.claude/docs/PRD.md#data-models) for full schema.

## User Roles

| Role      | Access                                                    |
| --------- | --------------------------------------------------------- |
| **Donor** | Own funds, contributions, grant recommendations only      |
| **Staff** | All data; approve/deny grants; create funds/contributions |

No donor ever sees another donor's data.

## Development Conventions

### Backend (Django)

- Use Django Class-Based Views (CBVs) for all views
- Enforce permissions with `LoginRequiredMixin` + `UserPassesTestMixin`
- Keep business logic in model methods/properties where possible
- Follow Django's naming conventions for templates: `app_name/model_list.html`, `app_name/model_form.html`
- API endpoints live under `/api/` prefix, served by DRF

### Frontend (Styling)

- **Tailwind CSS** for all styling (both Django templates and React components)
- Use utility classes directly in templates: `class="bg-brand-primary text-white py-2 px-4 rounded-md"`
- Design tokens configured in `tailwind.config.js` (colors, spacing, typography, shadows)
- Custom theme extends Tailwind defaults with design system tokens
- Run `npm run watch:css` during development to rebuild CSS on changes
- Compiled CSS outputs to `static/css/styles.css`

### React Components

- Use Tailwind utility classes for styling: `className="bg-white border border-neutral-200 rounded-md p-4"`
- Radix UI for accessible headless components (dialogs, dropdowns, etc.)
- Style Radix primitives with Tailwind classes
- Recharts for data visualization, styled with design system color values
