# Backend Planning Doc: Steward
_Generated 2026-05-07_

## Project Context
Portfolio project demonstrating production-grade Django backend engineering for a Web Application Developer role at a nonprofit community foundation. Models the donor-advised fund (DAF) domain: named funds, contributions, and staff-reviewed grant recommendations. Hard deadline: 1 week, solo build, free-tier hosting.

## Tech Stack
| Layer | Technology |
|---|---|
| Language | Python |
| Framework | Django 5.x |
| Database | PostgreSQL |
| ORM | Django ORM |
| Auth | django.contrib.auth (built-in) |
| API | Django REST Framework (one endpoint only) |
| Frontend (primary) | Django templates + vanilla JS |
| Frontend (dashboard) | React 18 — single `DonorDashboard` component |
| Charts | Recharts |
| PDF Export | xhtml2pdf |
| Config | python-decouple (local) + platform env vars (prod) |
| Logging | Django built-in logging |
| Hosting | Railway or Render (free tier, managed PostgreSQL) |

## Data Model

### Entities

**User** — Extends `AbstractUser`. Two custom boolean fields added:
- `is_donor` — marks donor accounts; gates all donor views
- `is_admin` — marks foundation staff with full access; gates all staff views
- `is_staff` — Django built-in; retained for Django admin access only, not used as a role signal

> **⚠️ Dual-flag requirement:** Staff accounts need *both* `is_admin=True` (gates staff views) and `is_staff=True` (gates Django admin). Set both when creating staff users. Consider a manager method `create_staff_user()` that sets both flags atomically to avoid silent misconfiguration.

No additional profile model in v1.

**Fund**
- `name` — e.g. "The Williams Family Fund"
- `donor` (FK → User) — must be a user with `is_donor=True`
- `created_at` — auto timestamp
- `balance` — **computed property**, not a stored field (see Notes)

**Contribution**
- `fund` (FK → Fund, `on_delete=PROTECT`) — don't lose contribution records if a fund is deleted
- `amount` (DecimalField, `max_digits=10, decimal_places=2`) — must be positive
- `note` (optional)
- `date`
- `created_by` (FK → User, `on_delete=PROTECT`) — contribution records must not be lost if a staff account is deleted

**GrantRecommendation**
- `fund` (FK → Fund, `on_delete=PROTECT`) — a fund with grant history should not be deletable
- `nonprofit_name` — free text, no external lookup in v1
- `amount` (DecimalField, `max_digits=10, decimal_places=2`) — validated against computed balance at submission
- `memo` (optional)
- `status` — choices: `pending` / `approved` / `denied`
- `staff_note` (optional) — visible to donor
- `reviewed_by` (FK → User, nullable, `on_delete=SET_NULL`) — reviewer leaving shouldn't invalidate the grant record
- `reviewed_at` (nullable)
- `created_at` — auto timestamp

### Relationships
- User → Fund: one-to-many (one donor, many funds)
- Fund → Contribution: one-to-many
- Fund → GrantRecommendation: one-to-many

### Notes
- **Balance is computed**, not stored. Lives as a model property on `Fund`:
  ```python
  @property
  def balance(self):
      contributed = self.contributions.aggregate(Sum('amount'))['amount__sum'] or 0
      granted = self.grant_recommendations.filter(
          status='approved'
      ).aggregate(Sum('amount'))['amount__sum'] or 0
      return contributed - granted
  ```
- No race condition risk since there's no balance field to corrupt.
- **Hard deletes** — staff can delete records directly. No soft delete in v1.
- No versioning or history tracking in v1.

## API Design
REST. Single DRF endpoint for the React dashboard — everything else is Django template views.

**`GET /api/dashboard/`** — Donor only. Returns:
```json
{
  "balance": "5000.00",
  "total_contributed": "7500.00",
  "balance_over_time": [
    { "month": "2025-01", "balance": "3000.00" },
    { "month": "2025-03", "balance": "5000.00" }
  ],
  "recent_grants": [
    {
      "id": 1,
      "nonprofit_name": "Lawrence Humane Society",
      "amount": "500.00",
      "status": "approved",
      "created_at": "2025-03-15"
    }
  ]
}
```
- `recent_grants`: 5 most recent `GrantRecommendation` records for the donor's fund(s), ordered by `created_at` descending. Fields: `id`, `nonprofit_name`, `amount`, `status`, `created_at`.
- `balance_over_time`: last 12 months of monthly snapshots. Computed in Python by walking forward month-by-month, accumulating contributions minus approved grants within each month. Months with no activity are included with the carry-forward balance.
- No API versioning in v1
- No real-time (no websockets/SSE)
- On error (unexpected exception): returns HTTP 500 with no body. React component renders nothing gracefully.

## Error Handling
- Grant amount exceeding balance: form validation error (non-field error on `CreateView` form)
- Standard Django form errors for all other validation
- HTTP 403 for permission violations (handled by `UserPassesTestMixin`)
- No structured API error envelope needed — only one DRF endpoint and it's read-only

## Auth & Authorization
- Session-based auth via `django.contrib.auth`
- `LoginRequiredMixin` on all views
- `UserPassesTestMixin` for role enforcement:
  ```python
  # Donor views
  lambda u: u.is_donor

  # Staff views
  lambda u: u.is_admin
  ```
- No donor ever sees another donor's data — enforced at queryset level (filter by `request.user`)
- No public (unauthenticated) endpoints
- No multi-tenancy — single-org system
- Staff creates donor accounts via Django admin (no self-registration in v1)
- **CSRF:** DRF `SessionAuthentication` enforces CSRF. The dashboard endpoint is `GET`-only so no CSRF token wiring is needed in v1. If mutations are ever added to the React component, `X-CSRFToken` header handling will be required.

## Business Logic & Edge Cases
- **Grant submission validation:** `amount` must not exceed `fund.balance` at time of submission — enforced in form `clean()` method
- **No background jobs, queues, or external API dependencies in v1**
- **No transactions needed** — computed balance eliminates the approval race condition entirely
- **xhtml2pdf PDF export** — pure Python, no system dependencies; renders from Django templates synchronously

## Performance & Scalability
- Small internal tool — no meaningful scale requirements in v1
- Balance computed on demand — acceptable for dashboard/detail views; revisit with annotation if list views become slow
- **N+1 risk on staff list views:** `/staff/grants/` renders `fund__donor__name` and computed `fund.balance` per row. The `balance` property fires two aggregation queries per fund. Use `select_related('fund__donor')` and consider annotating balance at the queryset level if the staff list view feels slow.
- No caching in v1
- No file uploads or binary data beyond PDF export
- No full-text search — simple queryset filtering only

## Config & Environment
- **Local:** `python-decouple` with `.env` file
- **Production:** Platform environment variables (Railway/Render UI)
- Required vars: `SECRET_KEY`, `DATABASE_URL`, `DEBUG`, `ALLOWED_HOSTS`
- Two environments: local and prod (no staging in v1)
- No feature flags

## Observability & Quality
- **Logging:** Django built-in logging — no Sentry in v1
- **Testing:** Critical business logic only
  - `fund.balance` property computes correctly (contributed minus approved grants)
  - Grant approval logic (status change, balance impact)
  - Permission enforcement (donor cannot access another donor's data)
- No compliance constraints (no real PII, no payments)

## Deferred Decisions
- Whether to add queryset annotation for `balance` on staff list views if performance becomes an issue (see Performance section)

## References
- [Steward PRD](PRD.md)
