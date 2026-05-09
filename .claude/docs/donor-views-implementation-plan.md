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

### 1.2 Expand CSS Design System ✓

**File:** `static/css/styles.css`

**Status: COMPLETE**

- ✓ Design system created and documented in `.claude/context/design-system.md`
- ✓ CSS custom properties implemented in `static/css/styles.css` with HSL color format
- ✓ Plus Jakarta Sans font integrated in `core/templates/base.html`
- ✓ Full component specifications documented (Button, Input, Card, Table, Badge, Alert, Modal, Dropdown, Tabs, Progress)
- ✓ 8px spacing grid, warm earthy green color palette, light mode only

---

## Phase 2: Dashboard View (React Component)

### 2.1 Create DRF API Endpoint

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

- Use CSS custom properties from design system (`var(--color-brand-primary)`, etc.)
- Apply design tokens directly to Radix UI primitives
- BEM class names for custom components (`.fund-hero`, `.balance-chart`, etc.)
- No CSS-in-JS, pure CSS with design system tokens

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

### 4.1 Build GrantRecommendationListView

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

### 5.2 Build FundDetailView

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
        context['contributions'] = self.object.contributions.all()
        context['grants'] = self.object.grant_recommendations.all()
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
