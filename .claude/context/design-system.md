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

All colors use HSL format for easier manipulation and consistency.

### Brand
```css
--color-brand-primary: hsl(142, 76%, 36%);        /* Earthy green — primary actions, links */
--color-brand-primary-hover: hsl(142, 70%, 31%);  /* Darker on hover */
--color-brand-primary-light: hsl(142, 76%, 85%);  /* Backgrounds, badges */
--color-brand-primary-dark: hsl(142, 76%, 20%);   /* Text on light backgrounds */
```

### Neutral
```css
--color-neutral-50: hsl(0, 0%, 98%);
--color-neutral-100: hsl(0, 0%, 96%);
--color-neutral-200: hsl(0, 0%, 90%);
--color-neutral-300: hsl(0, 0%, 83%);
--color-neutral-400: hsl(0, 0%, 64%);
--color-neutral-500: hsl(0, 0%, 45%);
--color-neutral-600: hsl(0, 0%, 32%);
--color-neutral-700: hsl(0, 0%, 25%);
--color-neutral-800: hsl(0, 0%, 15%);
--color-neutral-900: hsl(0, 0%, 9%);
```

### Semantic
```css
--color-success: hsl(142, 76%, 36%);              /* Approved grants, confirmations */
--color-success-light: hsl(142, 76%, 93%);
--color-error: hsl(0, 72%, 51%);                  /* Denied grants, validation errors */
--color-error-light: hsl(0, 93%, 94%);
--color-warning: hsl(38, 92%, 50%);               /* Pending grants, alerts */
--color-warning-light: hsl(48, 96%, 89%);
--color-info: hsl(217, 91%, 60%);                 /* Informational messages */
--color-info-light: hsl(214, 95%, 93%);
```

### Surface
```css
--color-surface-base: hsl(0, 0%, 100%);         /* Page background */
--color-surface-raised: hsl(0, 0%, 98%);        /* Cards, modals */
--color-surface-border: hsl(0, 0%, 90%);        /* Dividers, input borders */
--color-text-primary: hsl(0, 0%, 9%);           /* Headings, body text */
--color-text-secondary: hsl(0, 0%, 32%);        /* Labels, captions */
--color-text-tertiary: hsl(0, 0%, 64%);         /* Placeholders, disabled */
```

## Typography

### Font Families
```css
--font-family-base: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-family-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
```

### Scale

| Token | Size | Line Height | Weight | Use Case |
|-------|------|-------------|--------|----------|
| `--font-size-xs` | 12px | 16px | 400 | Captions, helper text |
| `--font-size-sm` | 14px | 20px | 400 | Table data, secondary labels |
| `--font-size-base` | 16px | 24px | 400 | Body text, form inputs |
| `--font-size-lg` | 18px | 28px | 500 | Section subheadings |
| `--font-size-xl` | 20px | 28px | 600 | Card headings |
| `--font-size-2xl` | 24px | 32px | 700 | Page titles |
| `--font-size-3xl` | 30px | 36px | 700 | Hero headings |

### Weights
```css
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

## Spacing Scale

| Token | Value |
|-------|-------|
| `--spacing-0` | 0px |
| `--spacing-1` | 8px |
| `--spacing-2` | 16px |
| `--spacing-3` | 24px |
| `--spacing-4` | 32px |
| `--spacing-5` | 40px |
| `--spacing-6` | 48px |
| `--spacing-8` | 64px |
| `--spacing-10` | 80px |

## Border Radius

| Token | Value |
|-------|-------|
| `--radius-none` | 0px |
| `--radius-sm` | 4px |
| `--radius-md` | 8px |
| `--radius-lg` | 12px |
| `--radius-full` | 9999px |

## Shadows

| Token | Value |
|-------|-------|
| `--shadow-none` | none |
| `--shadow-sm` | 0 1px 2px rgba(0, 0, 0, 0.05) |
| `--shadow-md` | 0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.05) |
| `--shadow-lg` | 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05) |
| `--shadow-xl` | 0 20px 25px rgba(0, 0, 0, 0.1), 0 10px 10px rgba(0, 0, 0, 0.04) |

## Breakpoints

| Token | Value |
|-------|-------|
| `--breakpoint-mobile` | 640px |
| `--breakpoint-tablet` | 768px |
| `--breakpoint-desktop` | 1024px |

## Motion

| Token | Value |
|-------|-------|
| `--duration-fast` | 150ms |
| `--duration-base` | 200ms |
| `--easing-base` | ease |

## Components

### Button

**Purpose:** Primary interaction element for actions (submit forms, approve grants, create funds).

**Variants:**
- **Primary** — `background: --color-brand-primary`, `color: white`, `--shadow-sm`, `--radius-md`
- **Secondary** — `background: --color-neutral-100`, `color: --color-text-primary`, `border: 1px solid --color-surface-border`
- **Ghost** — `background: transparent`, `color: --color-brand-primary`, no border
- **Destructive** — `background: --color-error`, `color: white`

**Sizes:**
- **Small** — `padding: --spacing-1 --spacing-2`, `font-size: --font-size-sm`
- **Medium** — `padding: --spacing-1 --spacing-3`, `font-size: --font-size-base`
- **Large** — `padding: --spacing-2 --spacing-4`, `font-size: --font-size-lg`

**States:**
- **Hover** — Darken background by 10%, apply `--shadow-md`
- **Focus** — `outline: 2px solid --color-brand-primary`, `outline-offset: 2px`
- **Disabled** — `opacity: 0.5`, `cursor: not-allowed`

**Usage Notes:**
Use primary for form submissions and critical actions. Use destructive only for irreversible actions (deny grant, delete fund). Ghost buttons for tertiary actions (cancel, view details).

---

### Input / Textarea

**Purpose:** Form fields for contributions, grant recommendations, fund creation.

**Base Style:**
- `border: 1px solid --color-surface-border`
- `background: --color-surface-base`
- `padding: --spacing-1 --spacing-2`
- `font-size: --font-size-base`
- `border-radius: --radius-md`

**States:**
- **Focus** — `border-color: --color-brand-primary`, `outline: 2px solid --color-brand-primary-light`
- **Error** — `border-color: --color-error`, helper text in `--color-error`
- **Disabled** — `background: --color-neutral-100`, `color: --color-text-tertiary`

**Usage Notes:**
Always pair with a `<label>` (font-size: `--font-size-sm`, color: `--color-text-secondary`). Display validation errors below input in `--font-size-xs`.

---

### Card

**Purpose:** Container for fund summaries, grant recommendation cards, contribution history.

**Base Style:**
- `background: --color-surface-base`
- `border: 1px solid --color-surface-border`
- `border-radius: --radius-md`
- `padding: --spacing-3`
- `box-shadow: --shadow-sm`

**Variants:**
- **Raised** — `background: --color-surface-raised`, `box-shadow: --shadow-md`
- **Interactive** — Hover: `box-shadow: --shadow-lg`, `transform: translateY(-2px)`, `transition: --duration-fast`

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

**Base Style:**
- `display: inline-flex`
- `padding: 4px 12px`
- `border-radius: --radius-full`
- `font-size: --font-size-xs`
- `font-weight: --font-weight-medium`

**Variants:**
- **Success** (approved) — `background: --color-success-light`, `color: --color-success`
- **Warning** (pending) — `background: --color-warning-light`, `color: --color-warning`
- **Error** (denied) — `background: --color-error-light`, `color: --color-error`
- **Neutral** (default) — `background: --color-neutral-100`, `color: --color-neutral-700`

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
- Apply base styles via `static/css/styles.css` using CSS custom properties.
- Component classes follow BEM naming: `.btn`, `.btn--primary`, `.btn--large`.
- Form errors rendered with `.form-error` class (color: `--color-error`, font-size: `--font-size-xs`).

### React Dashboard
- **Component Library:** Radix UI (headless, accessible primitives)
- **Styling:** CSS custom properties from design system (no CSS-in-JS)
- **BEM Naming:** `.dashboard-card`, `.dashboard-card__header`, etc.
- **Charts:** Recharts with design tokens (`--color-brand-primary`, `--color-neutral-200`)
- **Radix Components:**
  - `@radix-ui/react-dialog` for modals (match Modal component specs)
  - `@radix-ui/react-dropdown-menu` for dropdowns (match Dropdown component specs)
  - Apply design tokens directly: `background: var(--color-surface-base)`, `border-radius: var(--radius-md)`
- Match card, button, and table styles to Django templates for visual consistency across app

### Accessibility
- Minimum touch target: `44px × 44px` (buttons, inputs).
- Color is never the only indicator (use icons + text for status badges).
- Focus states must be visible (2px outline, `--color-brand-primary`).

### Decisions Made
- **Light mode only:** Faster to build, matches nonprofit/financial context.
- **Plus Jakarta Sans:** Warmer than Inter, better for community-focused branding.
- **8px grid:** Simplifies spacing decisions, aligns with border radius.
- **Monospace for data:** Improves readability of currency amounts and dates in tables.
