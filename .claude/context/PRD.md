# Steward — Project Requirements Document

> **Type:** Portfolio project  
> **Status:** Draft  
> **Last Updated:** 2026-05-07

---

## Problem Statement

Community foundations need software to manage donor-advised funds: tracking named funds, logging contributions, processing grant recommendations from donors, and routing those recommendations through a staff approval workflow. Steward models that domain in Django to demonstrate production-grade backend engineering for a Web Application Developer role at a nonprofit community foundation.

---

## Goals & Non-Goals

### Goals
- Demonstrate Django depth: CBVs, ORM, admin customization, auth/permissions, templates
- Model a real-world domain with intentional, normalized data models
- Show ability to bridge Django and React with a justified, minimal integration
- Ship a polished, scoped v1 in one week

### Non-Goals
- Be a full-featured DAF platform
- Handle real money or payment processing
- Verify nonprofit 501(c)(3) status via external API
- Send email notifications

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.x |
| Database | PostgreSQL |
| Auth | Django built-in (django.contrib.auth) |
| Frontend (primary) | Django templates + minimal vanilla JS |
| Frontend (dashboard) | React 18 — single `DonorDashboard` component |
| API (dashboard only) | Django REST Framework — one endpoint |
| Charts | Recharts (inside React component) |
| PDF export | xhtml2pdf |
| Hosting | Railway or Render (free tier, managed PostgreSQL) |

---

## User Roles & Permissions

| Role | Access |
|---|---|
| Donor | Own funds, contributions, and grant recommendations only |
| Staff | All funds, all donors, all recommendations; approve/deny; fund management |

Enforced via `LoginRequiredMixin` and `UserPassesTestMixin`. No donor ever sees another donor's data.

---

## Data Models

### User
Extends `AbstractUser`. Two custom boolean fields added:
- `is_donor` — marks donor accounts; gates all donor views
- `is_admin` — marks foundation staff with full access; gates all staff views
- `is_staff` — Django built-in; retained for Django admin access only, not used as a role signal

No additional profile model in v1.

### Fund
| Field | Notes |
|---|---|
| `name` | e.g. "The Williams Family Fund" |
| `donor` (FK → User) | Must be a user with `is_donor=True` |
| `balance` | **Computed property**, not a stored field — sum of contributions minus approved grants |
| `created_at` | Auto timestamp |

### Contribution
Staff creates contributions manually — no payment processing.

| Field | Notes |
|---|---|
| `fund` (FK → Fund) | Target fund |
| `amount` (DecimalField) | Must be positive |
| `note` (optional) | Staff memo |
| `date` | Date of contribution |
| `created_by` (FK → User) | Staff member who logged it |

### GrantRecommendation
| Field | Notes |
|---|---|
| `fund` (FK → Fund) | Must belong to requesting donor |
| `nonprofit_name` | Free-text; no external lookup in v1 |
| `amount` (DecimalField) | Must not exceed fund balance |
| `memo` (optional) | Donor's purpose statement |
| `status` | Choices: `pending` / `approved` / `denied` |
| `staff_note` (optional) | Visible to donor; added on review |
| `reviewed_by` (FK → User, nullable) | Staff reviewer |
| `reviewed_at` (nullable) | Timestamp of decision |
| `created_at` | Auto timestamp |

**Balance:** Computed on demand as a model property — no stored field to update on approval. No race condition risk.

---

## Feature List & Scope

### In Scope
- Donor login, fund overview, contribution history, grant recommendation history
- Donor grant recommendation form (nonprofit name, amount, optional memo)
- Staff review queue: approve or deny with a public note
- Staff fund management: create funds, log contributions
- Django admin with inline editing, list filters, custom actions
- DonorDashboard React component: balance, contribution totals, balance-over-time chart, recent grants table
- PDF export of fund statement (xhtml2pdf, server-rendered)

### Out of Scope
- Email notifications
- Payment processing
- Nonprofit verification (IRS API, Candid/GuideStar)
- Cause area categorization / grants-by-category chart (future)
- Donor self-registration (staff creates accounts)

---

## Views Plan

| URL | View Type | Role |
|---|---|---|
| `/dashboard/` | TemplateView | Donor |
| `/api/dashboard/` | DRF APIView | Donor |
| `/contributions/` | ListView (CBV) | Donor |
| `/grants/` | ListView (CBV) | Donor |
| `/grants/new/` | CreateView (CBV) | Donor |
| `/grants/<id>/` | DetailView (CBV) | Donor |
| `/grants/export/` | View (xhtml2pdf) | Donor |
| `/staff/grants/` | ListView (CBV) | Staff |
| `/staff/grants/<id>/review/` | UpdateView (CBV) | Staff |
| `/staff/funds/` | ListView (CBV) | Staff |
| `/staff/funds/new/` | CreateView (CBV) | Staff |
| `/staff/contributions/new/` | CreateView (CBV) | Staff |

---

## Django Admin Customization

- `FundAdmin`: inline `ContributionInline` and `GrantRecommendationInline`
- `GrantRecommendationAdmin`: `list_display` with status, `list_filter` by status/fund, `search_fields` by nonprofit name and donor
- Custom action: bulk-approve pending recommendations
- `readonly_fields`: `reviewed_by`, `reviewed_at`

---

## Constraints

- **Timeline:** 1 week
- **Team:** Solo
- **Budget:** Free-tier hosting only

---

## Open Questions & Risks

| # | Question / Risk | Status |
|---|---|---|
| 1 | How does staff create donor accounts in v1? Via Django admin directly. | Resolved |
| 2 | Concurrent approval race condition: two staff approve the same grant, overdrawing a fund | Resolved — computed balance eliminates stored-field race condition entirely |
| 3 | WeasyPrint dependency can be finicky on some hosting environments | Resolved — switched to xhtml2pdf (pure Python, no system dependencies) |

---

## Future Phases

- Cause area field on grant recommendations + donut chart by category
- Email notifications on recommendation status changes
- Donor self-registration with staff approval
- Nonprofit verification via IRS Tax Exempt Organizations API
