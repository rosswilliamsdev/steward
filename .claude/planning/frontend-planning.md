# Frontend Planning Doc: Steward
_Generated 2026-05-07_

## Project Context
Portfolio project demonstrating production-grade Django backend engineering for a Web Application Developer role at a nonprofit community foundation. Models the donor-advised fund (DAF) domain. Two user roles: donors (self-service) and staff (management). Hard deadline: 1 week, solo build.

**Core donor job-to-be-done:** Check grant recommendation status and submit new grant recommendations — the dashboard is the launchpad for both actions.

### Dashboard API Contract (`GET /api/dashboard/`)
The `DonorDashboard` component consumes this endpoint. Expected shape:
```json
{
  "balance": "5000.00",
  "total_contributed": "7500.00",
  "balance_over_time": [
    { "month": "2025-01", "balance": "3000.00" }
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
- `recent_grants`: 5 most recent grants, ordered by `created_at` descending
- `balance_over_time`: last 12 months of monthly snapshots
- **On error:** API returns HTTP 500 with no body. Component should guard against a failed fetch and render nothing (no crash).

**Core staff job-to-be-done:** Review and act on pending grant recommendations; manage funds and log contributions via Django admin and staff views.

## Tech Stack
| Layer | Technology |
|---|---|
| Primary frontend | Django templates + minimal vanilla JS |
| Dashboard component | React 18 — single `DonorDashboard` component |
| Charts | Recharts (inside React component) |
| Styling | Tailwind CSS |
| API (dashboard only) | Django REST Framework — one endpoint (`GET /api/dashboard/`) |
| PDF export | xhtml2pdf |
| Hosting | Railway or Render (free tier) |

## Aesthetic Direction
Community foundation prestige register. The visual language should feel like institutional wealth management software — serious, trustworthy, unhurried.

- **Palette:** Deep green primary (`#0F6E56` range), muted supporting tones, white surfaces
- **Typography:** Serif or semi-serif for fund name display; sans-serif for data and UI
- **Density:** Spacious — generous whitespace, data feels weighty not crowded
- **Light/dark:** Light mode only in v1
- **One-word feel:** Authoritative
- **Key visual:** Hero fund balance number, large and prominent, top-left of dashboard. Fund displayed with donor family name ("The Williams Family Fund").

## Interaction Philosophy
- **Motion budget:** Subtle polish only — no decorative animations
- **Input modality:** Desktop pointer-primary; keyboard-navigable forms
- **No complex interaction patterns** — no drag-and-drop, no gestures
- The grant recommendation form is intentionally simple: "writing a check." One page, no multi-step flow.

## UX Flows

### Primary Donor Flow
1. Donor logs in → redirected to `/dashboard/`
2. Dashboard loads — React component fetches `GET /api/dashboard/` and renders fund summary, charts, recent grant table
3. Donor reviews grant status in the recent grants table (pending / approved / denied badges)
4. Donor clicks "Recommend a grant" CTA → `/grants/new/`
5. Donor fills out single-page form: nonprofit name, amount, optional memo → submit
6. On success → redirect to `/grants/` (list view) or grant detail

### Primary Staff Flow
1. Staff logs in → redirected to `/staff/grants/` (review queue)
2. Staff reviews pending recommendations, clicks into detail
3. Staff approves or denies with optional public note → `/staff/grants/<id>/review/`
4. Staff manages funds and contributions via `/staff/funds/` and Django admin

### Edge States
- **Empty state:** Out of scope for v1 — new funds with no data show zeros and blank chart areas
- **Loading:** Minimal — React dashboard shows no explicit skeleton; loads fast on free tier
- **Error:** Standard Django error pages for template views. React component guards against HTTP 500 (no body) from the dashboard API — fails silently with no data rendered, no crash.
- **Form validation errors:** Django form errors rendered inline below fields, non-field errors at top of form

### Forms & Validation
- Grant recommendation form: single page, server-side validation via Django `CreateView`
- Balance check (amount must not exceed fund balance) enforced in form `clean()` — error surfaces as a non-field error
- All other forms follow standard Django form error rendering
- No client-side validation in v1

### URL State
- Nothing lives in the URL beyond the resource identifier — no filter/sort state in query params in v1

## Responsive & Accessibility
- **Breakpoint strategy:** Desktop-first; mobile is "good enough" — no dedicated mobile layouts
- **Accessibility:** Semantic HTML, reasonable color contrast, keyboard-navigable forms — no formal WCAG target in v1

## Performance & Quality Targets
- No meaningful scale requirements — small internal tool
- React dashboard component is the only async data fetch; one DRF endpoint, fast query
- No infinite scroll, no file uploads, no real-time data
- **Priority quality areas:** Correctness of business logic (balance validation), visual polish of dashboard

## Deferred Decisions
- Exact CTA placement and label for "Recommend a grant" on dashboard
- Whether grant list `/grants/` or grant detail is the post-submission redirect target
- Empty state designs (explicitly deferred to future phase)

## References
- PRD: PRD.md
- Backend Planning Doc: backend-planning.md
