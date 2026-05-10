# Design System — Steward

## Table of Contents
- [Overview](#overview)
- [Color Tokens](#color-tokens)
- [Typography](#typography)
- [Spacing Scale](#spacing-scale)
- [Border Radius](#border-radius)
- [Shadows](#shadows)
- [Breakpoints](#breakpoints)
- [Motion](#motion)
- [Components](#components)
- [Usage Notes](#usage-notes)

## Overview

Steward's visual identity is warm, trustworthy, and community-focused. The design emphasizes clarity and approachability for nonprofit donors and staff managing donor-advised funds. Color palette anchored in earthy green conveys growth and impact; typography prioritizes readability for financial data and forms.

## Color Tokens

All colors use HSL format for easier manipulation and consistency. Access via Tailwind utility classes.

### Brand
| Token | Value | Tailwind Class Example |
|-------|-------|------------------------|
| Primary | `hsl(142, 76%, 36%)` | `bg-brand-primary`, `text-brand-primary`, `border-brand-primary` |
| Primary Hover | `hsl(142, 70%, 31%)` | `hover:bg-brand-primary-hover` |
| Primary Light | `hsl(142, 76%, 85%)` | `bg-brand-primary-light` |
| Primary Dark | `hsl(142, 76%, 20%)` | `text-brand-primary-dark` |

### Neutral
| Token | Value | Tailwind Class Example |
|-------|-------|------------------------|
| 50 | `hsl(0, 0%, 98%)` | `bg-neutral-50` |
| 100 | `hsl(0, 0%, 96%)` | `bg-neutral-100` |
| 200 | `hsl(0, 0%, 90%)` | `bg-neutral-200` |
| 300 | `hsl(0, 0%, 83%)` | `bg-neutral-300` |
| 400 | `hsl(0, 0%, 64%)` | `text-neutral-400` |
| 500 | `hsl(0, 0%, 45%)` | `text-neutral-500` |
| 600 | `hsl(0, 0%, 32%)` | `text-neutral-600` |
| 700 | `hsl(0, 0%, 25%)` | `text-neutral-700` |
| 800 | `hsl(0, 0%, 15%)` | `text-neutral-800` |
| 900 | `hsl(0, 0%, 9%)` | `text-neutral-900` |

### Semantic
| Token | Value | Tailwind Class Example |
|-------|-------|------------------------|
| Success | `hsl(142, 76%, 36%)` | `bg-success`, `text-success` |
| Success Light | `hsl(142, 76%, 93%)` | `bg-success-light` |
| Error | `hsl(0, 72%, 51%)` | `bg-error`, `text-error` |
| Error Light | `hsl(0, 93%, 94%)` | `bg-error-light` |
| Warning | `hsl(38, 92%, 50%)` | `bg-warning`, `text-warning` |
| Warning Light | `hsl(48, 96%, 89%)` | `bg-warning-light` |
| Info | `hsl(217, 91%, 60%)` | `bg-info`, `text-info` |
| Info Light | `hsl(214, 95%, 93%)` | `bg-info-light` |

## Typography

### Font Families
| Family | Tailwind Class | Value |
|--------|----------------|-------|
| Sans (default) | `font-sans` | Plus Jakarta Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif |
| Monospace | `font-mono` | JetBrains Mono, Fira Code, Courier New, monospace |

### Scale

| Token | Size | Line Height | Tailwind Class | Use Case |
|-------|------|-------------|----------------|----------|
| xs | 12px | 16px | `text-xs` | Captions, helper text |
| sm | 14px | 20px | `text-sm` | Table data, secondary labels |
| base | 16px | 24px | `text-base` | Body text, form inputs |
| lg | 18px | 28px | `text-lg` | Section subheadings |
| xl | 20px | 28px | `text-xl` | Card headings |
| 2xl | 24px | 32px | `text-2xl` | Page titles |
| 3xl | 30px | 36px | `text-3xl` | Hero headings |

### Weights
| Weight | Tailwind Class |
|--------|----------------|
| 400 (normal) | `font-normal` |
| 500 (medium) | `font-medium` |
| 600 (semibold) | `font-semibold` |
| 700 (bold) | `font-bold` |

## Spacing Scale

8px-based grid for consistent spacing.

| Value | Tailwind Class (padding) | Tailwind Class (margin) | Tailwind Class (gap) |
|-------|--------------------------|-------------------------|----------------------|
| 0px | `p-0` | `m-0` | `gap-0` |
| 8px | `p-1` | `m-1` | `gap-1` |
| 16px | `p-2` | `m-2` | `gap-2` |
| 24px | `p-3` | `m-3` | `gap-3` |
| 32px | `p-4` | `m-4` | `gap-4` |
| 40px | `p-5` | `m-5` | `gap-5` |
| 48px | `p-6` | `m-6` | `gap-6` |
| 64px | `p-7` | `m-7` | `gap-7` |
| 80px | `p-8` | `m-8` | `gap-8` |

## Border Radius

| Value | Tailwind Class | Use Case |
|-------|----------------|----------|
| 0px | `rounded-none` | Flush edges |
| 4px | `rounded-sm` | Subtle rounding (inputs, badges) |
| 8px | `rounded-md` | Standard rounding (buttons, cards) |
| 12px | `rounded-lg` | Prominent rounding (modals) |
| 9999px | `rounded-full` | Pills, circles |

## Shadows

| Token | Tailwind Class | Use Case |
|-------|----------------|----------|
| None | `shadow-none` | Flat elements |
| Small | `shadow-sm` | Subtle elevation (inputs on focus) |
| Medium | `shadow-md` | Cards, dropdowns |
| Large | `shadow-lg` | Modals, popovers |

## Breakpoints

Tailwind's default responsive prefixes:

| Breakpoint | Prefix | Min Width |
|------------|--------|-----------|
| Mobile (default) | (none) | 0px |
| Tablet | `sm:` | 640px |
| Desktop | `md:` | 768px |
| Large Desktop | `lg:` | 1024px |

Example: `class="text-sm md:text-base lg:text-lg"`

## Motion

Use Tailwind's transition utilities:

| Duration | Tailwind Class |
|----------|----------------|
| 150ms (fast) | `duration-150` |
| 200ms (base) | `duration-200` |
| 300ms (slow) | `duration-300` |

Combine with transition type: `transition-colors duration-200 ease-in-out`

## Components

### Button

**Purpose:** Primary interaction element for actions (submit forms, approve grants, create funds).

**Variants:**
- **Primary** — `class="bg-brand-primary hover:bg-brand-primary-hover text-white font-medium py-2 px-4 rounded-md shadow-sm transition-colors duration-200"`
- **Secondary** — `class="bg-neutral-100 hover:bg-neutral-200 text-neutral-900 font-medium py-2 px-4 rounded-md border border-neutral-200 transition-colors duration-200"`
- **Ghost** — `class="bg-transparent hover:bg-neutral-50 text-brand-primary font-medium py-2 px-4 rounded-md transition-colors duration-200"`
- **Destructive** — `class="bg-error hover:bg-error-dark text-white font-medium py-2 px-4 rounded-md shadow-sm transition-colors duration-200"`

**Sizes:**
- **Small** — `py-1 px-2 text-sm`
- **Medium** — `py-2 px-4 text-base` (default)
- **Large** — `py-3 px-6 text-lg`

**States:**
- **Hover** — Use `hover:` prefix: `hover:bg-brand-primary-hover`, `hover:shadow-md`
- **Focus** — `focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-offset-2`
- **Disabled** — `disabled:opacity-50 disabled:cursor-not-allowed`

**Full Example:**
```html
<button class="bg-brand-primary hover:bg-brand-primary-hover text-white font-medium py-2 px-4 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200">
  Submit Grant
</button>
```

**Usage Notes:**
Use primary for form submissions and critical actions. Use destructive only for irreversible actions (deny grant, delete fund). Ghost buttons for tertiary actions (cancel, view details).

---

### Input / Textarea

**Purpose:** Form fields for contributions, grant recommendations, fund creation.

**Base Style:**
```html
<input class="w-full px-3 py-2 border border-neutral-200 rounded-md text-base focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-brand-primary disabled:bg-neutral-100 disabled:text-neutral-400" />
```

**States:**
- **Focus** — `focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-brand-primary`
- **Error** — `border-error focus:ring-error` + error text `class="text-error text-xs mt-1"`
- **Disabled** — `disabled:bg-neutral-100 disabled:text-neutral-400 disabled:cursor-not-allowed`

**Full Form Example:**
```html
<div class="space-y-1">
  <label for="amount" class="block text-sm font-medium text-neutral-600">Amount</label>
  <input
    type="number"
    id="amount"
    class="w-full px-3 py-2 border border-neutral-200 rounded-md text-base focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-brand-primary"
  />
  <p class="text-error text-xs mt-1">Amount must be greater than $0</p>
</div>
```

**Usage Notes:**
Always pair with a `<label>` (`text-sm font-medium text-neutral-600`). Display validation errors below input (`text-error text-xs mt-1`).

---

### Card

**Purpose:** Container for fund summaries, grant recommendation cards, contribution history.

**Base Style:**
```html
<div class="bg-white border border-neutral-200 rounded-md p-4 shadow-sm">
  <!-- Card content -->
</div>
```

**Variants:**
- **Raised** — `bg-neutral-50 shadow-md`
- **Interactive** — `hover:shadow-lg hover:-translate-y-0.5 transition-all duration-150 cursor-pointer`

**Full Example:**
```html
<div class="bg-white border border-neutral-200 rounded-md p-4 shadow-sm hover:shadow-lg hover:-translate-y-0.5 transition-all duration-150 cursor-pointer">
  <h3 class="text-xl font-semibold text-neutral-900 mb-2">Community Impact Fund</h3>
  <p class="text-sm text-neutral-600">Balance: <span class="font-mono font-semibold text-brand-primary">$25,000</span></p>
</div>
```

**Usage Notes:**
Use for grouping related information (fund name + balance, grant details). Interactive variant for clickable cards linking to detail views.

---

### Table

**Purpose:** Display lists of contributions, grants, fund activity.

**Base Style:**
- `width: 100%`
- `border-collapse: collapse`
- **Header** — `background: --color-neutral-50`, `font-weight: --font-weight-semibold`, `font-size: --font-size-sm`, `padding: --spacing-2`
- **Row** — `border-bottom: 1px solid --color-surface-border`, `padding: --spacing-2`
- **Hover** — `background: --color-neutral-50`

**Usage Notes:**
Use monospace font (`--font-family-mono`) for numeric columns (amounts, dates). Right-align currency values.

---

### Badge

**Purpose:** Display grant status (pending, approved, denied), fund types, contribution methods.

**Base Classes:**
`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium`

**Variants:**
- **Success** (approved) — `bg-success-light text-success`
- **Warning** (pending) — `bg-warning-light text-warning`
- **Error** (denied) — `bg-error-light text-error`
- **Neutral** (default) — `bg-neutral-100 text-neutral-700`

**Examples:**
```html
<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-success-light text-success">
  Approved
</span>
<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-warning-light text-warning">
  Pending
</span>
<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-error-light text-error">
  Denied
</span>
```

**Usage Notes:**
Do not use for interactive elements. For clickable tags, use ghost button variant instead.

---

### Alert / Toast

**Purpose:** Display success confirmations, error messages, warnings after form submissions or grant approvals.

**Base Style:**
- `padding: --spacing-2 --spacing-3`
- `border-radius: --radius-md`
- `border-left: 4px solid [semantic color]`
- `font-size: --font-size-sm`

**Variants:**
- **Success** — `background: --color-success-light`, `border-color: --color-success`
- **Error** — `background: --color-error-light`, `border-color: --color-error`
- **Warning** — `background: --color-warning-light`, `border-color: --color-warning`
- **Info** — `background: --color-info-light`, `border-color: --color-info`

**Usage Notes:**
Toasts auto-dismiss after 5 seconds. Alerts persist until dismissed. Include icon (✓ for success, ✕ for error).

---

### Modal / Dialog

**Purpose:** Grant approval workflow, delete confirmations, fund creation forms.

**Base Style:**
- **Overlay** — `background: rgba(0, 0, 0, 0.5)`, fixed full-screen
- **Content** — `background: --color-surface-base`, `border-radius: --radius-lg`, `box-shadow: --shadow-xl`, `max-width: 600px`, `padding: --spacing-4`

**Structure:**
- **Header** — `font-size: --font-size-xl`, `margin-bottom: --spacing-3`
- **Body** — `font-size: --font-size-base`, `color: --color-text-secondary`
- **Footer** — Button group (right-aligned)

**Usage Notes:**
Always include a close button (X icon, top-right). Destructive actions require confirmation modal with red "Confirm" button.

---

### Dropdown / Select

**Purpose:** Filter grants by status, select fund for contribution, choose nonprofit from list.

**Base Style:**
- Inherits input styles
- `background: --color-surface-base`
- Dropdown panel: `box-shadow: --shadow-lg`, `border: 1px solid --color-surface-border`, `border-radius: --radius-md`

**States:**
- **Hover (option)** — `background: --color-neutral-50`
- **Selected** — `background: --color-brand-primary-light`, `color: --color-brand-primary-dark`

**Usage Notes:**
Use native `<select>` for simple cases. Use custom dropdown component for searchable lists (nonprofit search).

---

### Tabs

**Purpose:** Switch between dashboard sections (My Funds, Contributions, Grant Recommendations).

**Base Style:**
- `border-bottom: 2px solid --color-surface-border`
- **Tab** — `padding: --spacing-2 --spacing-3`, `font-size: --font-size-base`, `color: --color-text-secondary`
- **Active** — `border-bottom: 2px solid --color-brand-primary`, `color: --color-brand-primary`, `font-weight: --font-weight-semibold`

**States:**
- **Hover** — `color: --color-text-primary`

**Usage Notes:**
Do not use more than 5 tabs. For more options, use a dropdown filter instead.

---

### Progress Indicator

**Purpose:** Visualize fund balance, grant approval percentage, contribution trends (React dashboard).

**Base Style:**
- **Bar** — `height: 8px`, `background: --color-neutral-200`, `border-radius: --radius-full`
- **Fill** — `background: --color-brand-primary`, `border-radius: --radius-full`, `transition: width --duration-base`

**Usage Notes:**
Use Recharts for complex visualizations (bar charts, line charts). Use simple progress bar for single metrics (fund utilization).

---

## Usage Notes

### Anti-Patterns
- **Do not** use `--color-brand-primary` for text on white backgrounds (fails WCAG contrast). Use `--color-brand-primary-dark` instead.
- **Do not** stack shadows (e.g., card inside modal). Modals use `--shadow-xl`, inner cards use `--shadow-none`.
- **Do not** use destructive buttons without confirmation modals.
- **Do not** mix spacing values outside the 8px grid (no `padding: 10px`).

### Django Template Integration
- **Tailwind CSS** provides all design tokens via utility classes
- Configure Tailwind in `tailwind.config.js` with custom theme extending design system tokens
- Use utility classes directly in templates: `class="bg-brand-primary text-white py-2 px-4 rounded-md"`
- Component classes use Tailwind `@apply` directive or direct utility classes
- Form errors use utility classes: `class="text-error text-xs mt-1"`

### React Dashboard
- **Styling:** Tailwind CSS with custom configuration extending design tokens
- **Component Library:** Radix UI (headless, accessible primitives) for interactive components
- **Charts:** Recharts styled with Tailwind classes
- **Tailwind Configuration:** Custom theme extends default with design system tokens:
  - Colors: Brand primary/secondary, semantic colors, neutrals mapped to Tailwind palette
  - Spacing: 8px-based scale (`spacing-1` = `2`, `spacing-2` = `4`, etc.)
  - Border radius: `radius-sm/md/lg/full`
  - Shadows: `shadow-sm/md/lg/xl`
  - Font families: `font-sans` (Plus Jakarta Sans), `font-mono` (JetBrains Mono)
  - Font sizes: `text-xs/sm/base/lg/xl/2xl/3xl`
- **Radix Components:**
  - `@radix-ui/react-dialog` for modals (style with Tailwind classes matching Modal specs)
  - `@radix-ui/react-dropdown-menu` for dropdowns (style with Tailwind classes)
- Visual consistency: Tailwind classes should match Django template styles (same colors, spacing, shadows)

### Accessibility
- Minimum touch target: `44px × 44px` (buttons, inputs).
- Color is never the only indicator (use icons + text for status badges).
- Focus states must be visible (2px outline, `--color-brand-primary`).

### Decisions Made
- **Light mode only:** Faster to build, matches nonprofit/financial context.
- **Plus Jakarta Sans:** Warmer than Inter, better for community-focused branding.
- **8px grid:** Simplifies spacing decisions, aligns with border radius.
- **Monospace for data:** Improves readability of currency amounts and dates in tables.
