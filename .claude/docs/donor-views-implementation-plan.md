# Donor Views Implementation Plan

## Overview

This document outlines the step-by-step implementation plan for building all donor-facing views in the Steward application. The plan follows the design principles and technical requirements defined in [frontend-planning.md](frontend-planning.md) and [frontend-rules.md](../rules/frontend-rules.md).

---

## Phase 1: Foundation & Navigation

### 1.1 Update Base Template Navigation

**File:** `core/templates/base.html`

- Add navigation menu with donor-specific links
- Links: Dashboard, My Grants, Recommend Grant, My Funds
- Conditionally show nav items based on `user.is_donor`
- Use semantic `<nav>` with `<a>` tags for navigation
- Ensure keyboard-navigable with visible focus states

**Acceptance Criteria:**

- Donors see only their navigation items
- Staff see different navigation
- All links are keyboard-accessible
- Active page has visual indicator

---

### 1.2 Tailwind CSS Design System ✓

**Files:** `tailwind.config.js`, `static/css/styles.css`, `.claude/context/design-system.md`

**Status: COMPLETE**

- ✓ Design system created and documented with Tailwind utility class examples
- ✓ Tailwind CSS configured with custom theme extending design tokens
- ✓ `static/css/styles.css` updated with `@tailwind` directives
- ✓ Plus Jakarta Sans font integrated via Tailwind config
- ✓ Full component specifications with Tailwind classes (Button, Input, Card, Table, Badge, Alert, Modal)
- ✓ 8px spacing grid, warm earthy green color palette, light mode only
- ✓ Build process configured: `npm run build:css` and `npm run watch:css`

---

## Phase 2: Dashboard View (React Component)

### 2.1 Create DRF API Endpoint

**Status: COMPLETE**

**Files:**

- `core/serializers.py` (new)
- `core/views.py` (add API view)
- `core/urls.py` (add API route)

**Endpoint:** `GET /api/dashboard/`

**Response Schema:**

```json
{
  "fund_name": "Smith Family Fund",
  "balance": "125000.00",
  "total_contributed": "150000.00",
  "balance_over_time": [
    {"month": "2025-01", "balance": "120000.00"},
    {"month": "2025-02", "balance": "122500.00"},
    ...
  ],
  "recent_grants": [
    {
      "id": 1,
      "nonprofit_name": "Local Food Bank",
      "amount": "5000.00",
      "status": "approved",
      "created_at": "2025-03-15"
    },
    ...
  ]
}
```

**Business Logic:**

- If donor has multiple funds, show first fund (sorted by `-created_at`)
- `balance_over_time`: last 12 months, one data point per month
- `recent_grants`: 5 most recent grant recommendations
- Error handling: return HTTP 500 with empty body on exceptions

**Security:**

- Require authentication (`LoginRequiredMixin`)
- Only return data for current user's funds
- Test that donors can't access other donors' data

**Acceptance Criteria:**

- Endpoint returns correct data structure
- Balance calculated correctly (contributions - approved grants)
- Time series data covers exactly 12 months
- Permission checks prevent cross-donor data access
- Error states return HTTP 500 (no stack traces)

---

### 2.2 Build React DonorDashboard Component

**Status: COMPLETE**

**File:** `static/js/DonorDashboard.jsx`

**Component Library:** Radix UI (headless components for accessibility)

**Dependencies:**

- `react`, `react-dom`
- `@radix-ui/react-dialog` (for future modals)
- `@radix-ui/react-dropdown-menu` (for future dropdowns)
- `recharts` (for balance chart)

**Component Structure:**

```
DonorDashboard
├── FundHero (fund name + balance)
├── BalanceChart (Recharts line chart)
└── RecentGrantsTable (table with status badges)
```

**Features:**

- Fetch `/api/dashboard/` on mount
- Hero section: Large fund balance (top-left, prominent)
- Fund name with family name format (e.g., "Smith Family Fund")
- Balance chart: simple line chart, last 12 months
- Recent grants table: nonprofit, amount, status, date
- Status badges: color + text (pending/approved/denied)
- "Recommend a Grant" CTA button → `/grants/create/`
- Loading state while fetching
- Error handling: fail silently on HTTP 500, show fallback UI

**Styling Approach:**

- **Tailwind CSS** for all styling via utility classes
- Apply Tailwind classes directly to Radix UI primitives: `<Dialog.Content className="bg-white rounded-lg shadow-lg p-6">`
- Use design system tokens: `bg-brand-primary`, `text-neutral-600`, `shadow-md`, etc.
- Recharts styled with Tailwind color values: `stroke="hsl(142, 76%, 36%)"`
- No custom CSS classes needed for layout/styling

**Accessibility:**

- Semantic HTML (`<table>` for data, `<h1>` for fund name)
- Chart has text alternative (data table below)
- Keyboard navigable throughout (Radix UI provides this)
- Status badges not color-only (include text)
- Focus states use `--color-brand-primary` from design system

**Recharts Configuration:**

- Line chart with single line (balance over time)
- X-axis: month labels (Jan, Feb, etc.)
- Y-axis: dollar amounts with $ prefix
- Minimal styling (no excessive animation)
- Responsive within container
- Use `--color-brand-primary` for line color
- Use `--color-neutral-200` for grid lines

**Acceptance Criteria:**

- Component renders without errors
- Data fetched and displayed correctly
- Chart is readable and accessible
- Status badges use color + text
- CTA button links to grant form
- No crashes on API errors
- Keyboard navigation works
- Radix UI components integrate seamlessly with design system

---

### 2.3 Set Up React Build Process

**Status: COMPLETE**

**Files:**

- `package.json` (add build scripts)
- `core/templates/core/dashboard.html` (add React root)
- Configure static file serving

**Build Setup:**

- Use Vite or similar for JSX compilation
- Output bundle to `static/js/`
- Include React, ReactDOM, Recharts in bundle
- Dev mode: watch for changes
- Prod mode: minified bundle

**Template Integration:**

- Add `<div id="donor-dashboard-root"></div>` to dashboard template
- Load React bundle via `<script>` tag
- Conditional rendering: only show for donors

**Acceptance Criteria:**

- JSX compiles successfully
- Bundle loaded in template
- React component mounts and renders
- Changes rebuild automatically in dev mode
- Production bundle is minified

---

## Phase 3: Grant Recommendation Form

### 3.1 Create GrantRecommendationForm

**Status: COMPLETE**

**File:** `core/forms.py` (new)

**Form Fields:**

- `fund`: ModelChoiceField (dropdown of user's funds)
- `nonprofit_name`: CharField (max 200)
- `amount`: DecimalField (max_digits=10, decimal_places=2)
- `memo`: CharField (optional, textarea)

**Custom Validation (`clean()` method):**

```python
def clean(self):
    cleaned_data = super().clean()
    fund = cleaned_data.get('fund')
    amount = cleaned_data.get('amount')

    if fund and amount:
        if amount > fund.balance:
            raise ValidationError(
                f"Amount exceeds available balance of ${fund.balance:,.2f}"
            )

    return cleaned_data
```

**Form Rendering:**

- Use Django form rendering (no manual HTML)
- Error messages display inline below fields
- Non-field errors (balance check) display at top

**Acceptance Criteria:**

- Form validates amount ≤ fund balance
- Error message is clear and actionable
- Fund dropdown shows only user's funds
- Memo field is optional
- Form prevents submission if invalid

---

### 3.2 Build GrantRecommendationCreateView

**Status: COMPLETE**

**File:** `core/views.py`

**View Class:**

```python
class GrantRecommendationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = GrantRecommendation
    form_class = GrantRecommendationForm
    template_name = 'core/grant_form.html'
    success_url = reverse_lazy('core:grant-list')

    def test_func(self):
        return self.request.user.is_donor

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.status = 'pending'
        return super().form_valid(form)
```

**Access Control:**

- `LoginRequiredMixin`: must be authenticated
- `UserPassesTestMixin`: must have `is_donor = True`
- Form filters fund choices to current user's funds only

**Success Behavior:**

- Redirect to grant list view (`/grants/`)
- Show success message (use Django messages framework)

**Acceptance Criteria:**

- Only donors can access view
- Non-donors get 403 Forbidden
- Fund dropdown shows only user's funds
- Grant created with status='pending'
- Successful redirect with confirmation message

---

### 3.3 Create Grant Recommendation Form Template

**Status: COMPLETE**

**File:** `core/templates/core/grant_form.html`

**Layout:**

- Page title: "Recommend a Grant"
- Breadcrumb navigation: Dashboard → My Grants → Recommend
- Form in centered card (max-width: 600px)
- Generous spacing between fields
- Non-field errors at top (red background)
- Field errors below each input
- Submit button: "Submit Recommendation"
- Cancel link: back to grant list

**Styling:**

- Follow design system typography
- Clear label/input hierarchy
- Readable field spacing (1.5rem between fields)
- Submit button prominent but not aggressive
- Keyboard-friendly (Enter to submit)

**Accessibility:**

- Labels associated with inputs (`for` attribute)
- Required fields marked with asterisk + aria-required
- Error messages linked via aria-describedby
- Focus order logical (top to bottom)

**Acceptance Criteria:**

- Form follows design system aesthetic
- All fields keyboard-accessible
- Error messages clear and visible
- Submit button properly styled
- Responsive on tablet/mobile (though desktop-first)

---

## Phase 4: Grant List & Detail Views

**UI Reference:** `.claude/ui/desktop/fund_overview_desktop/screen.png`

### 4.1 Build GrantRecommendationListView

**Status: COMPLETE**

**File:** `core/views.py`

**View Class:**

```python
class GrantRecommendationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = GrantRecommendation
    template_name = 'core/grant_list.html'
    context_object_name = 'grants'

    def test_func(self):
        return self.request.user.is_donor

    def get_queryset(self):
        return GrantRecommendation.objects.filter(
            fund__donor=self.request.user
        ).select_related('fund').order_by('-created_at')
```

**Features:**

- Show all grants for current donor's funds
- Order by most recent first
- Eager load fund data (select_related)
- Link to grant detail for each row
- "Recommend a Grant" button at top

**Table Columns:**

- Nonprofit Name
- Amount (formatted with $, commas)
- Fund Name (if donor has multiple funds)
- Status (badge)
- Date Submitted
- Actions (View Details link)

**Status Badges:**

- Pending: Blue badge, clock icon
- Approved: Green badge, checkmark icon
- Denied: Red badge, X icon
- Not color-only (include icon + text)

**Acceptance Criteria:**

- List shows only current donor's grants
- Ordered by newest first
- Status badges accessible
- Table is semantic HTML
- Monetary values use tabular numbers
- Empty state shows helpful message

---

### 4.2 Build GrantRecommendationDetailView

**Status: COMPELTE**

**File:** `core/views.py`

**View Class:**

```python
class GrantRecommendationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = GrantRecommendation
    template_name = 'core/grant_detail.html'
    context_object_name = 'grant'

    def test_func(self):
        grant = self.get_object()
        return self.request.user.is_donor and grant.fund.donor == self.request.user
```

**Display:**

- Grant details card
- Nonprofit name (large, serif font)
- Amount (prominent)
- Fund name
- Memo (if provided)
- Status with badge
- Timeline: Date submitted, Date reviewed (if reviewed)
- Staff note (if status is approved/denied)
- Back to list link

**Access Control:**

- Donors can only view their own grants
- Permission check in `test_func()`
- Return 403 if donor doesn't own this grant

**Acceptance Criteria:**

- Only grant owner can access detail
- All grant information displayed
- Staff note shown if present
- Timeline clear and readable
- Back navigation works
- 403 for unauthorized access

---

### 4.3 Create grant_list.html Template

**Status: COMPLETE**

**File:** `core/templates/core/grant_list.html`

**Layout:**
- Page title: "Grant Recommendations"
- Primary action: "Recommend a Grant" button (top-right, links to `core:grant-create`)
- Table displaying all grants
- Empty state if no grants exist

**Table Structure:**

```html
<table class="w-full">
  <thead class="bg-surface-container">
    <tr>
      <th class="text-left px-6 py-4 text-sm font-semibold text-on-surface-variant">Nonprofit</th>
      <th class="text-left px-6 py-4 text-sm font-semibold text-on-surface-variant">Amount</th>
      <th class="text-left px-6 py-4 text-sm font-semibold text-on-surface-variant">Fund</th>
      <th class="text-left px-6 py-4 text-sm font-semibold text-on-surface-variant">Status</th>
      <th class="text-left px-6 py-4 text-sm font-semibold text-on-surface-variant">Date Submitted</th>
      <th class="text-right px-6 py-4 text-sm font-semibold text-on-surface-variant">Actions</th>
    </tr>
  </thead>
  <tbody>
    {% for grant in grants %}
    <tr class="border-b border-outline-variant hover:bg-surface-container-low transition-colors">
      <td class="px-6 py-4 text-base text-on-surface">{{ grant.nonprofit_name }}</td>
      <td class="px-6 py-4 text-base font-mono text-on-surface">${{ grant.amount|floatformat:2|intcomma }}</td>
      <td class="px-6 py-4 text-sm text-on-surface-variant">{{ grant.fund.name }}</td>
      <td class="px-6 py-4">
        <!-- Status badge: see below -->
      </td>
      <td class="px-6 py-4 text-sm font-mono text-on-surface-variant">{{ grant.created_at|date:"M d, Y" }}</td>
      <td class="px-6 py-4 text-right">
        <a href="{% url 'core:grant-detail' grant.pk %}" class="text-primary hover:text-primary-container font-medium text-sm">
          View Details
        </a>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
```

**Status Badge Component:**

```html
{% if grant.status == 'pending' %}
<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold bg-tertiary-container text-on-tertiary-container">
  <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
  </svg>
  Pending
</span>
{% elif grant.status == 'approved' %}
<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold bg-secondary-container/30 text-secondary">
  <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
  </svg>
  Approved
</span>
{% elif grant.status == 'denied' %}
<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold bg-error-container text-on-error-container">
  <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
  </svg>
  Denied
</span>
{% endif %}
```

**Empty State:**

```html
{% if not grants %}
<div class="bg-surface-container-lowest border border-outline-variant rounded-lg p-8 text-center">
  <p class="text-on-surface-variant text-base mb-4">You haven't recommended any grants yet.</p>
  <a href="{% url 'core:grant-create' %}" class="inline-block bg-primary hover:bg-primary-container text-on-primary font-medium py-2 px-4 rounded-md shadow-sm transition-all">
    Recommend Your First Grant
  </a>
</div>
{% endif %}
```

**Page Header:**

```html
<div class="flex justify-between items-center mb-6">
  <h1 class="text-3xl font-bold text-on-surface">Grant Recommendations</h1>
  <a href="{% url 'core:grant-create' %}" class="bg-primary hover:bg-primary-container text-on-primary font-medium py-2 px-4 rounded-md shadow-sm transition-all focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2">
    Recommend a Grant
  </a>
</div>
```

**Design System Compliance:**

- Table header: `bg-surface-container` with `text-on-surface-variant` text
- Row hover: `hover:bg-surface-container-low transition-colors`
- Borders: `border-outline-variant` (subtle)
- Status badges: Use design system badge variants with icons
- Monetary values: `font-mono` for tabular numbers
- Primary button: `bg-primary hover:bg-primary-container text-on-primary py-2 px-4 rounded-md shadow-sm`
- Links: `text-primary hover:text-primary-container`

**Accessibility:**

- Semantic `<table>` with `<thead>` and `<tbody>`
- Status badges include both icon and text (not color-only)
- Focus states on all interactive elements
- `aria-label` on icon-only elements if needed (though all badges have text)

**Template Extends:**

```html
{% extends "core/base.html" %}
{% load humanize %}

{% block title %}Grant Recommendations{% endblock %}

{% block content %}
<!-- Page header and table here -->
{% endblock %}
```

**Acceptance Criteria:**

- Table displays all donor's grants
- Status badges accessible (icon + text)
- Hover states on rows
- Monetary values right-aligned with tabular numbers
- Empty state displays helpful CTA
- "Recommend a Grant" button prominent at top
- Responsive on mobile (consider horizontal scroll or card layout on small screens)

---

### 4.4 Create grant_detail.html Template

**Status: COMPELTE**

**File:** `core/templates/core/grant_detail.html`

**Layout:**
- Page title: Nonprofit name
- Back to list link (top-left)
- Card with grant details
- All information displayed in definition list format

**Card Structure:**

```html
<div class="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 shadow-sm">
  <div class="mb-6">
    <h2 class="text-3xl font-bold text-on-surface mb-2">{{ grant.nonprofit_name }}</h2>
    <p class="text-2xl font-mono font-semibold text-primary">${{ grant.amount|floatformat:2|intcomma }}</p>
  </div>

  <dl class="space-y-4">
    <div>
      <dt class="text-sm font-semibold text-on-surface-variant">Fund</dt>
      <dd class="text-base text-on-surface">{{ grant.fund.name }}</dd>
    </div>

    {% if grant.memo %}
    <div>
      <dt class="text-sm font-semibold text-on-surface-variant">Memo</dt>
      <dd class="text-base text-on-surface">{{ grant.memo }}</dd>
    </div>
    {% endif %}

    <div>
      <dt class="text-sm font-semibold text-on-surface-variant">Status</dt>
      <dd class="mt-1">
        <!-- Status badge (same as list template) -->
      </dd>
    </div>

    <div>
      <dt class="text-sm font-semibold text-on-surface-variant">Date Submitted</dt>
      <dd class="text-base font-mono text-on-surface">{{ grant.created_at|date:"F d, Y g:i A" }}</dd>
    </div>

    {% if grant.reviewed_at %}
    <div>
      <dt class="text-sm font-semibold text-on-surface-variant">Date Reviewed</dt>
      <dd class="text-base font-mono text-on-surface">{{ grant.reviewed_at|date:"F d, Y g:i A" }}</dd>
    </div>
    {% endif %}

    {% if grant.staff_note %}
    <div>
      <dt class="text-sm font-semibold text-on-surface-variant">Staff Note</dt>
      <dd class="text-base text-on-surface">{{ grant.staff_note }}</dd>
    </div>
    {% endif %}
  </dl>
</div>
```

**Back Navigation:**

```html
<div class="mb-4">
  <a href="{% url 'core:grant-list' %}" class="inline-flex items-center gap-2 text-primary hover:text-primary-container font-medium text-sm transition-colors">
    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
    </svg>
    Back to Grant Recommendations
  </a>
</div>
```

**Design System Compliance:**

- Card: `bg-surface-container-lowest border border-outline-variant rounded-lg p-6 shadow-sm`
- Definition list: `<dl>` with `space-y-4` spacing
- Labels: `text-sm font-semibold text-on-surface-variant`
- Values: `text-base text-on-surface` (or `font-mono` for dates/amounts)
- Amount: Large, prominent, with `text-primary` color
- Status badge: Same component as list template

**Template Extends:**

```html
{% extends "core/base.html" %}
{% load humanize %}

{% block title %}{{ grant.nonprofit_name }} - Grant Detail{% endblock %}

{% block content %}
<!-- Back link, nonprofit name, and detail card here -->
{% endblock %}
```

**Conditional Display:**

- Only show `memo` if present
- Only show `reviewed_at` if grant has been reviewed (approved or denied)
- Only show `staff_note` if present

**Acceptance Criteria:**

- All grant information displayed
- Back navigation works
- Status badge matches list template
- Conditional fields only show when data exists
- Clear visual hierarchy (nonprofit name → amount → details)
- Responsive on mobile

---

## Phase 5: Fund & Contribution Views (Read-Only for Donors)

### 5.1 Build FundListView

**File:** `core/views.py`

**View Class:**

```python
class FundListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Fund
    template_name = 'core/fund_list.html'
    context_object_name = 'funds'

    def test_func(self):
        return self.request.user.is_donor

    def get_queryset(self):
        return self.request.user.funds.all()
```

**Display:**

- Table or card layout of funds
- Fund name (serif font, prominent)
- Current balance (computed property)
- Total contributed
- Number of grants (pending/approved)
- Link to fund detail

**Summary Stats (if multiple funds):**

- Total balance across all funds
- Total contributed across all funds
- Display at top of page

**Acceptance Criteria:**

- Shows only current donor's funds
- Balance calculated correctly
- Summary stats accurate
- Links to fund detail work
- Monetary values formatted consistently

---

### 5.2 Create fund_list.html Template

**File:** `core/templates/core/fund_list.html`

**Layout:**
- Page title: "My Funds"
- Primary action: "View All Grants" button (top-right, links to `core:grant-list`)
- Summary stats card (if multiple funds): total balance, total contributed
- Table or card layout displaying all funds
- Empty state if no funds exist

**Table Structure:**

```html
<table class="w-full">
  <thead>
    <tr class="bg-surface-container text-on-surface-variant text-xs uppercase tracking-wider font-semibold">
      <th class="px-6 py-4">Fund Name</th>
      <th class="px-6 py-4">Balance</th>
      <th class="px-6 py-4">Total Contributed</th>
      <th class="px-6 py-4">Grants</th>
      <th class="px-6 py-4 text-right">Actions</th>
    </tr>
  </thead>
  <tbody class="divide-y divide-outline-variant">
    {% for fund in funds %}
    <tr class="hover:bg-surface-container transition-colors">
      <td class="px-6 py-4">
        <p class="text-base font-semibold text-on-surface">{{ fund.name }}</p>
      </td>
      <td class="px-6 py-4 text-sm text-on-surface" style="font-variant-numeric: tabular-nums;">
        ${{ fund.balance|floatformat:2|intcomma }}
      </td>
      <td class="px-6 py-4 text-sm text-on-surface-variant" style="font-variant-numeric: tabular-nums;">
        ${{ fund.total_contributed|floatformat:2|intcomma }}
      </td>
      <td class="px-6 py-4 text-sm text-on-surface-variant">
        {{ fund.grant_recommendations.count }} grant{{ fund.grant_recommendations.count|pluralize }}
      </td>
      <td class="px-6 py-4 text-right">
        <a href="{% url 'core:fund-detail' fund.pk %}" class="text-primary hover:text-primary-container font-medium text-sm transition-colors">
          View Details
        </a>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
```

**Design System Compliance:**

- Table header: `bg-surface-container` with `text-on-surface-variant` text, uppercase
- Row hover: `hover:bg-surface-container transition-colors`
- Borders: `divide-y divide-outline-variant`
- Monetary values: `font-variant-numeric: tabular-nums`
- Fund name: `text-base font-semibold text-on-surface`

**Template Extends:**

```html
{% extends "base.html" %}
{% load humanize %}

{% block title %}My Funds{% endblock %}

{% block content %}
<!-- Page header, summary stats, and table here -->
{% endblock %}
```

**Acceptance Criteria:**

- Table displays all donor's funds
- Summary stats accurate if multiple funds
- Monetary values right-aligned with tabular numbers
- Empty state displays helpful message if no funds
- "View Details" links work correctly

---

### 5.3 Build FundDetailView

**File:** `core/views.py`

**View Class:**

```python
class FundDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Fund
    template_name = 'core/fund_detail.html'
    context_object_name = 'fund'

    def test_func(self):
        fund = self.get_object()
        return self.request.user.is_donor and fund.donor == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contributions'] = self.object.contributions.order_by('-date')
        context['grants'] = self.object.grant_recommendations.order_by('-created_at')
        return context
```

**Display:**

- Fund header: name, balance
- Two sections: Contributions and Grants
- Contributions table: Date, Amount, Note, Created by (staff name)
- Grants table: Same as grant list view
- Link to recommend new grant
- Back to fund list link

**Access Control:**

- Donors can only view their own funds
- Permission check in `test_func()`
- Return 403 if donor doesn't own fund

**Acceptance Criteria:**

- Only fund owner can access
- Contributions ordered by date (newest first)
- Grants ordered by date (newest first)
- All monetary values formatted
- Navigation links work
- 403 for unauthorized access

---

### 5.4 Create fund_detail.html Template

**File:** `core/templates/core/fund_detail.html`

**Layout:**
- Page title: Fund name
- Back to fund list link (top-left)
- Fund header card: balance, total contributed
- Two sections: Contributions and Grants
- "Recommend a Grant" CTA button

**Fund Header Card:**

```html
<div class="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 shadow-sm mb-6">
  <h1 class="text-3xl font-bold text-on-surface mb-4">{{ fund.name }}</h1>
  <div class="grid grid-cols-2 gap-6">
    <div>
      <p class="text-sm font-semibold text-on-surface-variant mb-1">Current Balance</p>
      <p class="text-2xl font-mono font-semibold text-primary">${{ fund.balance|floatformat:2|intcomma }}</p>
    </div>
    <div>
      <p class="text-sm font-semibold text-on-surface-variant mb-1">Total Contributed</p>
      <p class="text-2xl font-mono font-semibold text-on-surface">${{ fund.total_contributed|floatformat:2|intcomma }}</p>
    </div>
  </div>
</div>
```

**Contributions Section:**

```html
<div class="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 shadow-sm mb-6">
  <h2 class="text-xl font-semibold text-on-surface mb-4">Contributions</h2>
  {% if contributions %}
  <div class="overflow-x-auto">
    <table class="w-full">
      <thead>
        <tr class="bg-surface-container text-on-surface-variant text-xs uppercase tracking-wider font-semibold">
          <th class="px-6 py-4">Date</th>
          <th class="px-6 py-4">Amount</th>
          <th class="px-6 py-4">Note</th>
          <th class="px-6 py-4">Added By</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-outline-variant">
        {% for contribution in contributions %}
        <tr class="hover:bg-surface-container transition-colors">
          <td class="px-6 py-4 text-sm text-on-surface" style="font-variant-numeric: tabular-nums;">
            {{ contribution.date|date:"m/d/Y" }}
          </td>
          <td class="px-6 py-4 text-sm text-on-surface" style="font-variant-numeric: tabular-nums;">
            ${{ contribution.amount|floatformat:2|intcomma }}
          </td>
          <td class="px-6 py-4 text-sm text-on-surface-variant">
            {{ contribution.note|default:"—" }}
          </td>
          <td class="px-6 py-4 text-sm text-on-surface-variant">
            {{ contribution.created_by.get_full_name|default:contribution.created_by.username }}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  {% else %}
  <p class="text-on-surface-variant">No contributions yet.</p>
  {% endif %}
</div>
```

**Grants Section:**

```html
<div class="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 shadow-sm">
  <div class="flex justify-between items-center mb-4">
    <h2 class="text-xl font-semibold text-on-surface">Grant Recommendations</h2>
    <a href="{% url 'core:grant-create' %}" class="bg-primary hover:bg-primary-container text-on-primary font-medium py-2 px-4 rounded-md shadow-sm transition-all">
      Recommend a Grant
    </a>
  </div>
  {% if grants %}
  <!-- Same table structure as grant_list.html -->
  {% else %}
  <p class="text-on-surface-variant">No grant recommendations yet.</p>
  {% endif %}
</div>
```

**Back Navigation:**

```html
<div class="mb-4">
  <a href="{% url 'core:fund-list' %}" class="inline-flex items-center gap-2 text-primary hover:text-primary-container font-medium text-sm transition-colors">
    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
    </svg>
    Back to My Funds
  </a>
</div>
```

**Design System Compliance:**

- Cards: `bg-surface-container-lowest border border-outline-variant rounded-lg p-6 shadow-sm`
- Section headers: `text-xl font-semibold text-on-surface`
- Tables match grant_list.html styling
- Monetary values: `font-mono` with `font-variant-numeric: tabular-nums`
- Empty states: `text-on-surface-variant`

**Template Extends:**

```html
{% extends "base.html" %}
{% load humanize %}

{% block title %}{{ fund.name }} - Fund Detail{% endblock %}

{% block content %}
<!-- Back link, fund header, contributions, and grants here -->
{% endblock %}
```

**Acceptance Criteria:**

- Fund header displays balance and total contributed
- Contributions table shows all contributions ordered by date
- Grants table shows all grants ordered by date
- Empty states for both sections if no data
- "Recommend a Grant" CTA prominent
- Back navigation works
- All monetary values formatted consistently

---

### 5.5 Create ContributionListView (Optional)

**File:** `core/views.py`

**View Class:**

```python
class ContributionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Contribution
    template_name = 'core/contribution_list.html'
    context_object_name = 'contributions'

    def test_func(self):
        return self.request.user.is_donor

    def get_queryset(self):
        return Contribution.objects.filter(
            fund__donor=self.request.user
        ).select_related('fund', 'created_by').order_by('-date')
```

**Display:**

- Table of all contributions across all funds
- Date, Amount, Fund, Note, Added By
- Order by date (newest first)

**Acceptance Criteria:**

- Shows only current donor's contributions
- Ordered by newest first
- Fund column shows fund name
- Monetary values formatted

---

### 5.6 Create contribution_list.html Template

**File:** `core/templates/core/contribution_list.html`

**Layout:**
- Page title: "Contributions"
- Table displaying all contributions
- Empty state if no contributions

**Table Structure:**

```html
<table class="w-full">
  <thead>
    <tr class="bg-surface-container text-on-surface-variant text-xs uppercase tracking-wider font-semibold">
      <th class="px-6 py-4">Date</th>
      <th class="px-6 py-4">Amount</th>
      <th class="px-6 py-4">Fund</th>
      <th class="px-6 py-4">Note</th>
      <th class="px-6 py-4">Added By</th>
    </tr>
  </thead>
  <tbody class="divide-y divide-outline-variant">
    {% for contribution in contributions %}
    <tr class="hover:bg-surface-container transition-colors">
      <td class="px-6 py-4 text-sm text-on-surface" style="font-variant-numeric: tabular-nums;">
        {{ contribution.date|date:"m/d/Y" }}
      </td>
      <td class="px-6 py-4 text-sm text-on-surface" style="font-variant-numeric: tabular-nums;">
        ${{ contribution.amount|floatformat:2|intcomma }}
      </td>
      <td class="px-6 py-4 text-sm text-on-surface-variant">
        <a href="{% url 'core:fund-detail' contribution.fund.pk %}" class="text-primary hover:text-primary-container">
          {{ contribution.fund.name }}
        </a>
      </td>
      <td class="px-6 py-4 text-sm text-on-surface-variant">
        {{ contribution.note|default:"—" }}
      </td>
      <td class="px-6 py-4 text-sm text-on-surface-variant">
        {{ contribution.created_by.get_full_name|default:contribution.created_by.username }}
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
```

**Template Extends:**

```html
{% extends "base.html" %}
{% load humanize %}

{% block title %}Contributions{% endblock %}

{% block content %}
<!-- Page header and table here -->
{% endblock %}
```

**Acceptance Criteria:**

- Table displays all donor's contributions across all funds
- Fund name links to fund detail
- Monetary values formatted consistently
- Empty state if no contributions

---

## Phase 6: URL Configuration & Polish

### 6.1 Wire Up URL Patterns

**File:** `core/urls.py`

**URL Configuration:**

```python
app_name = 'core'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    # API endpoints
    path('api/dashboard/', DashboardAPIView.as_view(), name='api-dashboard'),

    # Grant recommendation URLs
    path('grants/', GrantRecommendationListView.as_view(), name='grant-list'),
    path('grants/<int:pk>/', GrantRecommendationDetailView.as_view(), name='grant-detail'),
    path('grants/create/', GrantRecommendationCreateView.as_view(), name='grant-create'),

    # Fund URLs
    path('funds/', FundListView.as_view(), name='fund-list'),
    path('funds/<int:pk>/', FundDetailView.as_view(), name='fund-detail'),
]
```

**Naming Conventions:**

- Use kebab-case for URL paths
- Use underscores for route names (`grant-list`, `grant-detail`)
- RESTful patterns where applicable
- Deep-linkable URLs (all views have unique paths)

**Acceptance Criteria:**

- All URLs resolve correctly
- Named URLs work with `{% url %}` tag
- URL patterns follow Django conventions
- Routes are RESTful and predictable

---

### 6.2 Add Empty State Handling

**Scope:** Explicitly deferred to future per frontend-planning.md:179

**Current Behavior:**

- Empty grant list: show message "No grant recommendations yet"
- Empty contribution list: show zeros
- Balance chart with no data: show blank chart area
- No custom illustrations or complex empty states

**Future Enhancement:**

- Custom empty state illustrations
- Contextual CTAs based on empty state
- More helpful onboarding messages

**Acceptance Criteria:**

- Empty lists show basic text message
- No crashes with empty data
- Charts render empty (no errors)
- Zeros displayed correctly

---

### 6.3 Cross-Browser Testing & Accessibility Pass

**Browser Testing:**

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

**Keyboard Navigation:**

- All interactive elements reachable via Tab
- Focus order is logical (top to bottom, left to right)
- Focus rings visible (`:focus-visible`)
- Enter submits forms
- Escape closes modals (if added)

**Accessibility Checklist:**

- All images have alt text
- Forms have associated labels
- Tables use `<th>` with scope
- Color contrast meets WCAG AA
- Status not conveyed by color alone
- ARIA labels where needed (charts, dynamic content)
- Semantic HTML throughout

**Form Testing:**

- Password manager compatibility
- Autofill works correctly
- Field validation clear
- Error messages associated with fields

**Number Formatting:**

- All monetary values use `font-variant-numeric: tabular-nums`
- Consistent decimal places (2 for dollars)
- Thousand separators (commas)
- Dollar sign prefix

**Acceptance Criteria:**

- No keyboard traps
- Focus visible on all elements
- Color contrast verified with tools
- Forms work with password managers
- Numbers aligned in tables
- Semantic HTML validates
- No accessibility errors in audit tools

---

## Phase 7: Integration & Testing

### 7.1 Manual Testing: Full Donor Flow

**Test Scenario 1: First-Time Donor**

1. Login as donor with one fund
2. View dashboard (should show fund balance and chart)
3. Navigate to "My Grants" (should be empty)
4. Click "Recommend a Grant"
5. Fill form with valid data
6. Submit successfully
7. Verify redirect to grant list
8. Verify new grant appears with "pending" status
9. View grant detail
10. Return to dashboard (balance unchanged, grant appears in recent list)

**Test Scenario 2: Insufficient Balance**

1. Login as donor
2. Navigate to "Recommend a Grant"
3. Enter amount > fund balance
4. Submit form
5. Verify error message at top of form
6. Correct amount
7. Submit successfully

**Test Scenario 3: Multiple Funds**

1. Login as donor with multiple funds
2. View fund list (should show all funds)
3. Navigate to grant form
4. Verify fund dropdown shows all user's funds
5. Select fund, submit grant
6. Verify grant associated with correct fund
7. View fund detail (grant appears in fund's grant list)

**Test Scenario 4: Grant Lifecycle**

1. Login as donor, submit grant
2. Grant shows "pending" status
3. Admin approves grant (via admin panel)
4. Donor refreshes dashboard
5. Fund balance decreased by grant amount
6. Grant shows "approved" status in list
7. Grant detail shows staff note and approval date

**Acceptance Criteria:**

- All test scenarios pass without errors
- Balance calculations correct throughout
- Status updates reflect immediately
- Navigation flows logically
- No crashes or unexpected behavior

---

### 7.2 Write Django Tests

**Test File:** `core/tests.py` (or `core/tests/test_donor_views.py`)

**Permission Tests:**

```python
class DonorViewPermissionTests(TestCase):
    def test_donor_cannot_see_other_donor_funds(self):
        # Create two donors with separate funds
        # Verify donor1 cannot access donor2's fund detail

    def test_donor_cannot_see_other_donor_grants(self):
        # Create two donors with grants
        # Verify donor1 cannot access donor2's grant detail

    def test_non_donor_cannot_access_donor_views(self):
        # Create non-donor user
        # Verify 403 on all donor views

    def test_unauthenticated_user_redirected_to_login(self):
        # Attempt to access donor views without login
        # Verify redirect to login page
```

**Form Validation Tests:**

```python
class GrantRecommendationFormTests(TestCase):
    def test_form_rejects_amount_exceeding_balance(self):
        # Create fund with balance of $1000
        # Submit form with amount of $1500
        # Verify validation error

    def test_form_accepts_amount_equal_to_balance(self):
        # Create fund with balance of $1000
        # Submit form with amount of $1000
        # Verify form valid

    def test_form_accepts_amount_less_than_balance(self):
        # Create fund with balance of $1000
        # Submit form with amount of $500
        # Verify form valid

    def test_memo_is_optional(self):
        # Submit form without memo
        # Verify form valid
```

**View Tests:**

```python
class DonorViewTests(TestCase):
    def test_dashboard_shows_correct_fund_data(self):
        # Create donor with fund, contributions, grants
        # Access dashboard
        # Verify correct balance, contribution total

    def test_grant_list_shows_only_user_grants(self):
        # Create donor with grants
        # Create other donor with grants
        # Access grant list
        # Verify only user's grants shown

    def test_grant_create_success_redirect(self):
        # Submit valid grant form
        # Verify redirect to grant list
        # Verify grant created with pending status

    def test_fund_detail_shows_contributions_and_grants(self):
        # Create fund with contributions and grants
        # Access fund detail
        # Verify both lists present
```

**API Tests:**

```python
class DashboardAPITests(TestCase):
    def test_api_returns_correct_data_structure(self):
        # Create donor with fund, contributions, grants
        # Call /api/dashboard/
        # Verify response matches schema

    def test_api_balance_over_time_has_12_months(self):
        # Call /api/dashboard/
        # Verify balance_over_time has exactly 12 data points

    def test_api_recent_grants_limited_to_5(self):
        # Create donor with 10 grants
        # Call /api/dashboard/
        # Verify recent_grants has exactly 5 items

    def test_api_requires_authentication(self):
        # Call /api/dashboard/ without auth
        # Verify 401 or redirect to login
```

**Acceptance Criteria:**

- All tests pass
- Test coverage >80% for donor views
- Permission checks verified
- Form validation verified
- API contract verified
- No test flakiness

---

## Key Design Principles (Reference)

**Aesthetic:** Community foundation prestige

- Authoritative, trustworthy, spacious
- Serif fonts for fund names
- Deep green primary color (#0F6E56)
- Generous whitespace, "unhurried" feel

**Interaction:**

- Minimal motion (no fancy animations)
- Keyboard-navigable throughout
- Desktop-first (mobile deferred)
- Fast on free-tier hosting

**Forms:**

- Single-page forms (no multi-step wizards)
- Server-side validation only (v1)
- Clear error messaging
- Simple, "writing a check" feel

**Accessibility:**

- Semantic HTML everywhere
- WCAG AA contrast ratios
- Keyboard support with visible focus
- Status not color-only
- Password manager friendly

**Performance:**

- Minimal async (just one DRF endpoint)
- No heavy JavaScript libraries (except React for dashboard)
- Fast page loads on free tier
- Efficient database queries (select_related)

---

## Success Criteria (Phase Complete)

- [ ] All donor views implemented and accessible
- [ ] Navigation works throughout donor interface
- [ ] Design system fully implemented in CSS
- [ ] React dashboard component renders correctly
- [ ] API endpoint returns correct data
- [ ] Grant recommendation form validates balance
- [ ] Grant list and detail views working
- [ ] Fund list and detail views working
- [ ] All URLs wired correctly
- [ ] Keyboard navigation works throughout
- [ ] Accessibility audit passes (no critical issues)
- [ ] All Django tests passing
- [ ] Manual test scenarios pass
- [ ] Permission checks prevent cross-donor access
- [ ] Forms work with password managers
- [ ] Numbers formatted consistently with tabular nums
- [ ] Empty states handled gracefully
- [ ] Cross-browser compatibility verified

---

## Future Enhancements (Post-MVP)

- Custom empty state illustrations
- Mobile-responsive layouts
- Client-side form validation
- Multi-step grant recommendation wizard
- PDF export of fund statements
- Email notifications for grant status changes
- Dark mode support
- Advanced filtering/search on grant list
- Bulk grant operations
- Fund activity timeline visualization
