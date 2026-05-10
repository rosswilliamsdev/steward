# Steward UI Prototype Prompt

Use this prompt with Lovable, v0, or similar AI UI prototyping tools to generate component mockups.

---

## Project Context

Build UI components for **Steward**, a donor-advised fund management platform for community foundations. The app has two user types:

- **Donors** — view their funds, submit grant recommendations, see contribution history
- **Staff** — review/approve grant recommendations, create funds, log contributions

Tech stack: Django templates for primary UI, React 18 + Tailwind CSS for interactive donor dashboard.

---

## Design System

### Colors (HSL format)
```css
/* Brand */
--color-brand-primary: hsl(142, 76%, 36%);        /* Earthy green */
--color-brand-primary-hover: hsl(142, 70%, 31%);
--color-brand-primary-light: hsl(142, 76%, 85%);
--color-brand-primary-dark: hsl(142, 76%, 20%);

/* Neutrals */
--color-neutral-50: hsl(0, 0%, 98%);
--color-neutral-100: hsl(0, 0%, 96%);
--color-neutral-200: hsl(0, 0%, 90%);
--color-neutral-300: hsl(0, 0%, 83%);
--color-neutral-600: hsl(0, 0%, 32%);
--color-neutral-700: hsl(0, 0%, 25%);
--color-neutral-800: hsl(0, 0%, 15%);
--color-neutral-900: hsl(0, 0%, 9%);

/* Semantic */
--color-success: hsl(142, 76%, 36%);
--color-success-light: hsl(142, 76%, 93%);
--color-error: hsl(0, 72%, 51%);
--color-error-light: hsl(0, 93%, 94%);
--color-warning: hsl(38, 92%, 50%);
--color-warning-light: hsl(48, 96%, 89%);
--color-info: hsl(217, 91%, 60%);
--color-info-light: hsl(214, 95%, 93%);

/* Surface */
--color-surface-base: hsl(0, 0%, 100%);
--color-surface-raised: hsl(0, 0%, 98%);
--color-surface-border: hsl(0, 0%, 90%);
--color-text-primary: hsl(0, 0%, 9%);
--color-text-secondary: hsl(0, 0%, 32%);
--color-text-tertiary: hsl(0, 0%, 64%);
```

### Typography
- **Font family:** 'Plus Jakarta Sans' (primary), 'JetBrains Mono' (monospace for currency/dates)
- **Scale:** 12px (captions) → 14px (labels) → 16px (body) → 18px (subheadings) → 20px (card headings) → 24px (page titles) → 30px (hero)
- **Weights:** 400 (normal), 500 (medium), 600 (semibold), 700 (bold)
- **Line heights:** 1.5 for body text, 1.2 for headings

### Spacing
8px grid: `8px, 16px, 24px, 32px, 40px, 48px, 64px, 80px`

### Border Radius
`4px (sm), 8px (md), 12px (lg), 9999px (full)`

### Shadows
```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.05);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1), 0 10px 10px rgba(0, 0, 0, 0.04);
```

---

## Component Specifications

### Button
**Variants:**
- **Primary:** Green background (`--color-brand-primary`), white text, 8px border radius, small shadow
- **Secondary:** Light gray background (`--color-neutral-100`), dark text, 1px border
- **Ghost:** Transparent background, green text, no border
- **Destructive:** Red background (`--color-error`), white text

**Sizes:**
- Small: `padding: 8px 16px`, `font-size: 14px`
- Medium: `padding: 8px 24px`, `font-size: 16px`
- Large: `padding: 16px 32px`, `font-size: 18px`

**States:**
- Hover: Darken background 10%, increase shadow
- Focus: 2px green outline, 2px offset
- Disabled: 50% opacity, not-allowed cursor

### Input / Textarea
- 1px border (`--color-surface-border`), 8px border radius, 8px-16px padding
- **Focus:** Green border + light green outline glow
- **Error:** Red border, helper text below in red (12px)
- Always pair with label (14px, gray text)

### Card
- White background, 1px gray border, 8px border radius, 24px padding, small shadow
- **Raised variant:** Light gray background, medium shadow
- **Interactive variant:** Hover lifts card (-2px translateY) with larger shadow

### Table
- 100% width, collapsed borders
- **Header:** Light gray background, semibold 14px text, 16px padding
- **Rows:** 1px bottom border, 16px padding
- **Hover:** Light gray background
- Use monospace font for currency/dates, right-align numbers

### Badge (Status Indicators)
- Small pill: `4px 12px padding`, `9999px border radius`, `12px font`, `500 weight`
- **Success (approved):** Light green background, dark green text
- **Warning (pending):** Light yellow background, dark yellow text
- **Error (denied):** Light red background, dark red text
- **Neutral:** Light gray background, dark gray text

### Alert / Toast
- 16px-24px padding, 8px border radius, 4px left border in semantic color
- **Success:** Light green background, green left border
- **Error:** Light red background, red left border
- **Warning:** Light yellow background, yellow left border
- Include icon (✓ for success, ✕ for error, ! for warning)

### Modal
- **Overlay:** `rgba(0, 0, 0, 0.5)` full-screen backdrop
- **Content:** White background, 12px border radius, extra-large shadow, 600px max-width, 32px padding
- **Header:** 20px bold text, 24px bottom margin
- **Footer:** Right-aligned button group
- Close button (X) in top-right corner

---

## Key Screens to Prototype

### 1. Donor Dashboard (React Component)
**Layout:** Grid with 3 cards + chart + table

**Cards (top row):**
1. **Current Balance** — Large number (30px, bold), "Available to Grant" subtitle
2. **Total Contributed** — Large number, "All-time" subtitle
3. **Grants This Year** — Large number, count + total amount subtitle

**Chart (middle):**
- **Balance Over Time** — Line chart (Recharts), green line, light gray grid, last 12 months
- Responsive: Full-width on mobile, 2/3 width on desktop

**Table (bottom):**
- **Recent Grant Recommendations** — 5 columns: Date, Nonprofit, Amount, Status (badge), Staff Note
- Mobile: Stack rows, hide less critical columns
- Empty state: "No grant recommendations yet" with "Recommend a Grant" button

**Tabs:** "Dashboard" (active, green underline), "Contributions", "Grant Recommendations"

### 2. Grant Recommendation Form (Donor)
**Fields:**
1. **Nonprofit Name** (text input, required) — Placeholder: "e.g., Local Food Bank…"
2. **Amount** (number input, required) — Prefix with "$", placeholder: "0.00"
3. **Memo** (textarea, optional) — Placeholder: "Why does this grant matter to you?…"

**Validation:**
- Show "Amount exceeds fund balance ($X,XXX.XX available)" error below amount field if invalid
- Submit button disabled until nonprofit + valid amount entered

**Footer:** "Cancel" (ghost button) + "Submit Recommendation" (primary button)

### 3. Staff Grant Review Queue
**Layout:** Table with filters

**Filters (top):**
- Dropdown: "All Statuses" / "Pending" / "Approved" / "Denied"
- Search: "Search by donor or nonprofit…"

**Table columns:**
1. **Donor** — Name + fund name (small gray text below)
2. **Nonprofit** — Name
3. **Amount** — Right-aligned, monospace, bold
4. **Status** — Badge (pending/approved/denied)
5. **Actions** — "Review" button (small, secondary)

**Empty state:** "No pending recommendations" with illustration placeholder

### 4. Staff Grant Review Modal
**Header:** "Review Grant Recommendation"

**Details (read-only):**
- Donor: "Jane Doe (The Williams Family Fund)"
- Nonprofit: "Local Food Bank"
- Amount: "$5,000.00" (large, bold)
- Donor Memo: "Supporting food security in our community…" (light gray box, italic)

**Form:**
1. **Staff Note** (textarea, optional) — Placeholder: "Visible to donor. Explain your decision…"
2. **Decision buttons:**
   - "Deny" (destructive button, left-aligned)
   - "Approve" (primary button, right-aligned)

**Validation:** Require confirmation modal for "Deny" action

### 5. Fund Overview (Staff)
**Layout:** List of cards (one per fund)

**Card contents:**
- Fund name (20px bold)
- Donor name (14px gray)
- Balance: "$12,345.67" (large, green, bold)
- Stats: "3 contributions · 2 grants approved · 1 pending"
- "View Details" button (ghost)

**Empty state:** "No funds yet" + "Create Fund" button

---

## UI/UX Requirements

### Accessibility
- ✅ Minimum 44px touch targets on mobile
- ✅ Visible focus rings (2px green outline, 2px offset)
- ✅ Color + icon for status (not color-only)
- ✅ Form labels always visible (no floating labels)
- ✅ Error messages next to fields, focus first error on submit

### Mobile Responsiveness
- ✅ Single-column layout <640px
- ✅ Hamburger menu for navigation
- ✅ Stack table rows on mobile (card-style)
- ✅ 16px minimum font size on inputs (prevent iOS zoom)

### Forms
- ✅ Keep submit button enabled until request starts
- ✅ Show spinner on loading buttons (keep label visible)
- ✅ Inline validation (on blur or submit)
- ✅ Autofocus on desktop (first input), not on mobile
- ✅ Warn on unsaved changes before navigation

### Visual Polish
- ✅ Use monospace font for all currency amounts and dates
- ✅ Right-align numeric values in tables
- ✅ Empty states with helpful next actions
- ✅ Consistent 8px spacing grid
- ✅ Layered shadows (combine ambient + directional)
- ✅ Loading skeletons mirror final content layout

---

## Brand Tone

**Warm, trustworthy, community-focused.** The design should feel approachable for nonprofit donors and staff managing important financial decisions. Earthy green conveys growth and impact. Typography prioritizes clarity for financial data and forms.

---

## Example Prompt for AI Tool

```
Build a donor dashboard for a nonprofit donor-advised fund platform.

DESIGN SYSTEM:
- Primary color: earthy green (hsl(142, 76%, 36%))
- Font: Plus Jakarta Sans
- Spacing: 8px grid
- Shadows: Subtle layered shadows
- Border radius: 8px for cards, 9999px for badges

LAYOUT:
3 metric cards (Current Balance, Total Contributed, Grants This Year) in a row at the top. Below that, a full-width line chart showing "Balance Over Time" (last 12 months, green line, light gray grid). Below the chart, a table of recent grant recommendations with columns: Date, Nonprofit, Amount, Status (badge), Staff Note.

COMPONENTS:
- Cards: White background, 1px gray border, 8px radius, 24px padding, small shadow
- Badges: Pill-shaped, 12px font. Green for "approved", yellow for "pending", red for "denied"
- Table: Light gray header, 1px borders, monospace font for amounts, right-align numbers
- Chart: Use Recharts, green line, responsive

TONE: Warm, trustworthy, clean. Optimized for readability of financial data.
```

---

**Next Steps:**
1. Paste this prompt into Lovable/v0
2. Iterate on spacing, shadows, and responsive behavior
3. Export React components or static HTML
4. Integrate into Django templates or React dashboard
