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

Steward uses Material Design 3's adaptive color system. All colors use HSL format for easier manipulation. The palette creates a warm, earthy aesthetic with green tones symbolizing growth and sustainability.

### Surface Colors

Used for backgrounds and containers to create visual hierarchy through tonal layering.

| Token                     | Value                | Tailwind Class                 | Usage                                   |
| ------------------------- | -------------------- | ------------------------------ | --------------------------------------- |
| background                | `hsl(93, 53%, 97%)`  | `bg-background`                | Main page background (cream-green tint) |
| surface                   | `hsl(93, 53%, 97%)`  | `bg-surface`                   | Header, footer surfaces                 |
| surface-container-lowest  | `hsl(0, 0%, 100%)`   | `bg-surface-container-lowest`  | Highest elevation cards (pure white)    |
| surface-container-low     | `hsl(93, 31%, 94%)`  | `bg-surface-container-low`     | Subtle raised surfaces                  |
| surface-container         | `hsl(93, 22%, 92%)`  | `bg-surface-container`         | Standard container elevation            |
| surface-container-high    | `hsl(100, 18%, 90%)` | `bg-surface-container-high`    | Higher emphasis containers              |
| surface-container-highest | `hsl(93, 14%, 88%)`  | `bg-surface-container-highest` | Highest container emphasis              |

### Primary Colors

Earthy green representing growth, sustainability, and the evergreen nature of donor-advised funds.

| Token                | Value                 | Tailwind Class               | Usage                                   |
| -------------------- | --------------------- | ---------------------------- | --------------------------------------- |
| primary              | `hsl(146, 100%, 20%)` | `bg-primary`, `text-primary` | Primary buttons, active nav, brand text |
| on-primary           | `hsl(0, 0%, 100%)`    | `text-on-primary`            | Text on primary-colored backgrounds     |
| primary-container    | `hsl(142, 72%, 29%)`  | `bg-primary-container`       | Less prominent primary elements         |
| on-primary-container | `hsl(123, 100%, 91%)` | `text-on-primary-container`  | Text on primary containers              |

### Secondary Colors

Complementary green tones for secondary actions and accents.

| Token                  | Value                | Tailwind Class                   | Usage                               |
| ---------------------- | -------------------- | -------------------------------- | ----------------------------------- |
| secondary              | `hsl(129, 21%, 33%)` | `bg-secondary`, `text-secondary` | Secondary buttons and actions       |
| on-secondary           | `hsl(0, 0%, 100%)`   | `text-on-secondary`              | Text on secondary backgrounds       |
| secondary-container    | `hsl(123, 53%, 85%)` | `bg-secondary-container`         | Soft secondary surfaces, info boxes |
| on-secondary-container | `hsl(127, 20%, 36%)` | `text-on-secondary-container`    | Text on secondary containers        |

### Tertiary Colors

Warm amber/yellow tones for pending states and warnings.

| Token                 | Value               | Tailwind Class                 | Usage                                |
| --------------------- | ------------------- | ------------------------------ | ------------------------------------ |
| tertiary              | `hsl(43, 85%, 35%)` | `bg-tertiary`, `text-tertiary` | Pending states, warnings             |
| on-tertiary           | `hsl(0, 0%, 100%)`  | `text-on-tertiary`             | Text on tertiary-colored backgrounds |
| tertiary-container    | `hsl(43, 90%, 88%)` | `bg-tertiary-container`        | Pending badge backgrounds            |
| on-tertiary-container | `hsl(43, 85%, 20%)` | `text-on-tertiary-container`   | Text on pending backgrounds          |

### Text & Outline Colors

| Token              | Value                | Tailwind Class            | Usage                            |
| ------------------ | -------------------- | ------------------------- | -------------------------------- |
| on-surface         | `hsl(110, 12%, 10%)` | `text-on-surface`         | Primary text (dark green-tinted) |
| on-surface-variant | `hsl(120, 7%, 27%)`  | `text-on-surface-variant` | Secondary text, labels           |
| on-background      | `hsl(110, 12%, 10%)` | `text-on-background`      | Text on background surfaces      |
| outline            | `hsl(115, 5%, 45%)`  | `border-outline`          | Standard borders (stronger)      |
| outline-variant    | `hsl(111, 12%, 76%)` | `border-outline-variant`  | Subtle borders (most common)     |

### Error Colors

| Token              | Value                 | Tailwind Class            | Usage                             |
| ------------------ | --------------------- | ------------------------- | --------------------------------- |
| error              | `hsl(0, 75%, 42%)`    | `bg-error`, `text-error`  | Error states, destructive actions |
| on-error           | `hsl(0, 0%, 100%)`    | `text-on-error`           | Text on error backgrounds         |
| error-container    | `hsl(6, 100%, 92%)`   | `bg-error-container`      | Error message backgrounds         |
| on-error-container | `hsl(356, 100%, 29%)` | `text-on-error-container` | Error message text                |

### Color Usage Examples

**Surface Layering:**

```html
<body class="bg-background">
  <div class="bg-surface-container-lowest">
    <!-- White card -->
    <div class="bg-surface-container-high"><!-- Nested element --></div>
  </div>
</body>
```

**Primary Actions:**

```html
<button class="bg-primary text-on-primary">Submit</button>
<button class="bg-primary-container text-on-primary-container">
  Secondary Action
</button>
```

**Text Hierarchy:**

```html
<h1 class="text-on-surface">Heading</h1>
<p class="text-on-surface-variant">Secondary text</p>
```

## Typography

### Font Families

| Family         | Tailwind Class | Value                                                                              |
| -------------- | -------------- | ---------------------------------------------------------------------------------- |
| Sans (default) | `font-sans`    | Plus Jakarta Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif |
| Monospace      | `font-mono`    | JetBrains Mono, Fira Code, Courier New, monospace                                  |

### Scale

| Token | Size | Line Height | Tailwind Class | Use Case                     |
| ----- | ---- | ----------- | -------------- | ---------------------------- |
| xs    | 12px | 16px        | `text-xs`      | Captions, helper text        |
| sm    | 14px | 20px        | `text-sm`      | Table data, secondary labels |
| base  | 16px | 24px        | `text-base`    | Body text, form inputs       |
| lg    | 18px | 28px        | `text-lg`      | Section subheadings          |
| xl    | 20px | 28px        | `text-xl`      | Card headings                |
| 2xl   | 24px | 32px        | `text-2xl`     | Page titles                  |
| 3xl   | 30px | 36px        | `text-3xl`     | Hero headings                |

### Weights

| Weight         | Tailwind Class  |
| -------------- | --------------- |
| 400 (normal)   | `font-normal`   |
| 500 (medium)   | `font-medium`   |
| 600 (semibold) | `font-semibold` |
| 700 (bold)     | `font-bold`     |

### Numeric Formatting

| Feature       | Tailwind Class | Use Case                                      |
| ------------- | -------------- | --------------------------------------------- |
| Tabular Nums  | `tabular-nums` | Financial data, tables, dashboards (required) |

**Usage:** Apply `tabular-nums` to all monetary amounts, dates, and numeric data to ensure uniform digit widths and proper column alignment.

## Spacing Scale

8px-based grid for consistent spacing.

| Value | Tailwind Class (padding) | Tailwind Class (margin) | Tailwind Class (gap) |
| ----- | ------------------------ | ----------------------- | -------------------- |
| 0px   | `p-0`                    | `m-0`                   | `gap-0`              |
| 8px   | `p-1`                    | `m-1`                   | `gap-1`              |
| 16px  | `p-2`                    | `m-2`                   | `gap-2`              |
| 24px  | `p-3`                    | `m-3`                   | `gap-3`              |
| 32px  | `p-4`                    | `m-4`                   | `gap-4`              |
| 40px  | `p-5`                    | `m-5`                   | `gap-5`              |
| 48px  | `p-6`                    | `m-6`                   | `gap-6`              |
| 64px  | `p-7`                    | `m-7`                   | `gap-7`              |
| 80px  | `p-8`                    | `m-8`                   | `gap-8`              |

## Border Radius

| Value  | Tailwind Class | Use Case                         |
| ------ | -------------- | -------------------------------- |
| 0px    | `rounded-none` | Flush edges                      |
| 4px    | `rounded-sm`   | Subtle rounding (inputs, badges) |
| 8px    | `rounded-md`   | Standard rounding (buttons)      |
| 12px   | `rounded-lg`   | Prominent rounding (cards)       |
| 16px   | `rounded-xl`   | Large rounding (modals)          |
| 9999px | `rounded-full` | Pills, circles (badges only)     |

## Shadows

| Token  | Tailwind Class | Use Case                           |
| ------ | -------------- | ---------------------------------- |
| None   | `shadow-none`  | Flat elements                      |
| Small  | `shadow-sm`    | Subtle elevation (inputs on focus) |
| Medium | `shadow-md`    | Cards, dropdowns                   |
| Large  | `shadow-lg`    | Modals, popovers                   |

## Breakpoints

Tailwind's default responsive prefixes:

| Breakpoint       | Prefix | Min Width |
| ---------------- | ------ | --------- |
| Mobile (default) | (none) | 0px       |
| Tablet           | `sm:`  | 640px     |
| Desktop          | `md:`  | 768px     |
| Large Desktop    | `lg:`  | 1024px    |

Example: `class="text-sm md:text-base lg:text-lg"`

## Motion

Use Tailwind's transition utilities:

| Duration     | Tailwind Class |
| ------------ | -------------- |
| 150ms (fast) | `duration-150` |
| 200ms (base) | `duration-200` |
| 300ms (slow) | `duration-300` |

Combine with transition type: `transition-colors duration-200 ease-in-out`

## Components

### Button

**Purpose:** Primary interaction element for actions (submit forms, approve grants, create funds).

**Variants:**

- **Primary** — `class="bg-primary hover:bg-primary-container text-on-primary font-medium py-2 px-4 rounded-md shadow-sm transition-all"`
- **Outline** — `class="border border-primary text-primary hover:bg-primary-container hover:text-on-primary-container font-medium py-2 px-4 rounded-md transition-all"`
- **Secondary** — `class="bg-surface-container hover:bg-surface-container-high text-on-surface font-medium py-2 px-4 rounded-md border border-outline-variant transition-all"`
- **Ghost** — `class="bg-transparent hover:bg-surface-container text-primary font-medium py-2 px-4 rounded-md transition-all"`
- **Destructive** — `class="bg-error hover:bg-error-container text-on-error font-medium py-2 px-4 rounded-md shadow-sm transition-all"`

**Sizes:**

- **Small** — `py-1 px-2 text-sm rounded-md`
- **Medium** — `py-2 px-4 text-base rounded-md` (default)
- **Large** — `py-3 px-6 text-lg rounded-md`

**States:**

- **Hover** — Use `hover:` prefix: `hover:bg-primary-container`, `hover:shadow-md`
- **Focus** — `focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2`
- **Disabled** — `disabled:opacity-50 disabled:cursor-not-allowed`

**Full Example:**

```html
<button
  class="bg-primary hover:bg-primary-container text-on-primary font-medium py-2 px-4 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
>
  Submit Grant
</button>
```

**Usage Notes:**

- All button sizes use `rounded-md` (8px). Never use `rounded-lg`, `rounded-xl`, or `rounded-full` on buttons.
- Ghost buttons have no border and no background — only `bg-transparent`.
- Use primary for form submissions and critical actions.
- Use outline for secondary actions that need more visual weight than ghost (e.g., table row actions like "View Details").
- Use destructive only for irreversible actions (deny grant, delete fund).
- Ghost buttons for tertiary actions (cancel, dismiss).
- Outline buttons maintain visual hierarchy — they won't compete with primary CTAs on the page.

---

### Input / Textarea

**Purpose:** Form fields for contributions, grant recommendations, fund creation.

**Base Style:**

```html
<input
  class="w-full px-3 py-3 border border-outline-variant rounded-lg text-base focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary disabled:bg-surface-container disabled:text-on-surface-variant"
/>
```

**States:**

- **Focus** — `focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary`
- **Error** — `border-error focus:ring-error` + error text `class="text-error text-xs mt-1"`
- **Disabled** — `disabled:bg-surface-container disabled:text-on-surface-variant disabled:cursor-not-allowed`

**Full Form Example:**

```html
<div class="space-y-2">
  <label
    for="amount"
    class="block text-sm font-semibold text-on-surface-variant"
    >Amount</label
  >
  <input
    type="number"
    id="amount"
    class="w-full px-3 py-3 border border-outline-variant rounded-lg text-base focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary"
  />
  <p class="text-error text-xs mt-1">Amount must be greater than $0</p>
</div>
```

**Usage Notes:**
Always pair with a `<label>` (`text-sm font-semibold text-on-surface-variant`). Display validation errors below input (`text-error text-xs mt-1`).

---

### Card

**Purpose:** Container for fund summaries, grant recommendation cards, contribution history.

**Base Style:**

```html
<div
  class="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 shadow-sm"
>
  <!-- Card content -->
</div>
```

**Variants:**

- **Raised** — `bg-surface-container-low shadow-md`
- **Interactive** — `hover:shadow-lg transition-all cursor-pointer`

**Full Example:**

```html
<div
  class="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 shadow-sm hover:shadow-md transition-all cursor-pointer"
>
  <h3 class="text-xl font-semibold text-on-surface mb-2">
    Community Impact Fund
  </h3>
  <p class="text-sm text-on-surface-variant">
    Balance: <span class="font-mono font-semibold text-primary">$25,000</span>
  </p>
</div>
```

**Usage Notes:**
Use `rounded-lg` (12px) for cards. Use `rounded-xl` (16px) for modals only. Interactive variant for clickable cards linking to detail views.

---

### Table

**Purpose:** Display lists of contributions, grants, fund activity.

**Base Style:**

- `width: 100%`
- `border-collapse: collapse`
- **Header** — `bg-surface-container text-on-surface-variant font-semibold text-sm px-6 py-4`
- **Row** — `border-b border-outline-variant px-6 py-4`
- **Hover** — `hover:bg-surface-container-low transition-colors`

**Usage Notes:**
Use monospace font (`font-mono`) for numeric columns (amounts, dates). Right-align currency values.

---

### Badge

**Purpose:** Display grant status (pending, approved, denied), fund types, contribution methods.

**Base Classes:**
`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold`

**Variants:**

- **Success** (approved) — `bg-secondary-container/30 text-secondary`
- **Warning** (pending) — `bg-tertiary-container text-on-tertiary-container`
- **Error** (denied) — `bg-error-container text-on-error-container`
- **Neutral** (default) — `bg-surface-container-high text-on-surface-variant`

**Examples:**

```html
<span
  class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-secondary-container/30 text-secondary"
>
  Approved
</span>
<span
  class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-tertiary-container text-on-tertiary-container"
>
  Pending
</span>
<span
  class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-error-container text-on-error-container"
>
  Denied
</span>
<span
  class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-surface-container-high text-on-surface-variant"
>
  Neutral
</span>
```

**Usage Notes:**

- No borders on any badge variant.
- Do not use for interactive elements. For clickable tags, use ghost button variant instead.

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

- **Overlay** — `fixed inset-0 bg-black/50 z-40`
- **Content** — `bg-surface-container-lowest border border-outline-variant rounded-xl shadow-lg max-w-lg w-full p-6`

**Structure:**

- **Header** — `text-2xl font-semibold text-on-surface mb-3`
- **Body** — `text-base text-on-surface-variant mb-6`
- **Footer** — `flex justify-end gap-3` (right-aligned buttons)

**Usage Notes:**
Always include a close button (X icon, top-right). Destructive actions require confirmation modal with destructive "Confirm" button. Modals use `rounded-xl` (16px) — do not use on cards or buttons.

---

### Dropdown / Select

**Purpose:** Filter grants by status, select fund for contribution, choose nonprofit from list.

**Base Style:**

- Inherits input styles
- Dropdown panel: `bg-surface-container-lowest shadow-lg border border-outline-variant rounded-lg`

**States:**

- **Hover (option)** — `bg-surface-container-low`
- **Selected** — `bg-primary-container/20 text-primary`

**Usage Notes:**
Use native `<select>` for simple cases. Use custom dropdown component for searchable lists (nonprofit search).

---

### Tabs

**Purpose:** Switch between dashboard sections (My Funds, Contributions, Grant Recommendations).

**Base Style:**

- `border-b border-outline-variant`
- **Tab** — `px-6 py-2 text-base text-on-surface-variant`
- **Active** — `border-b-2 border-primary text-primary font-semibold`

**States:**

- **Hover** — `text-on-surface`

**Usage Notes:**
Do not use more than 5 tabs. For more options, use a dropdown filter instead.

---

### Progress Indicator

**Purpose:** Visualize fund balance, grant approval percentage, contribution trends (React dashboard).

**Base Style:**

- **Bar** — `h-2 bg-surface-container-highest rounded-full`
- **Fill** — `h-2 bg-primary rounded-full transition-all`

**Usage Notes:**
Use Recharts for complex visualizations (bar charts, line charts). Use simple progress bar for single metrics (fund utilization).

---

## Usage Notes

### Anti-Patterns

- **Do not** use `rounded-lg` on buttons — buttons always use `rounded-md`.
- **Do not** use `rounded-full` on buttons — that is for badges only.
- **Do not** add borders to ghost buttons — ghost variant is borderless by definition.
- **Do not** use `text-primary` on `bg-surface-container-lowest` (white) without checking contrast — the dark green passes WCAG AA.
- **Do not** stack shadows (e.g., card inside modal). Modals use `shadow-lg`, inner cards use `shadow-none`.
- **Do not** use destructive buttons without confirmation modals.
- **Do not** mix spacing values outside the 8px grid (no `p-[10px]`).
- **Do not** use pure grays — all surfaces should use the green-tinted surface tokens for brand consistency.
- **Do not** use hardcoded hex colors — use only the Tailwind token classes defined in this document.

### Border Radius Quick Reference

| Element             | Class          | px     |
| ------------------- | -------------- | ------ |
| Buttons (all sizes) | `rounded-md`   | 8px    |
| Inputs, badges      | `rounded-sm`   | 4px    |
| Badge pills         | `rounded-full` | 9999px |
| Cards               | `rounded-lg`   | 12px   |
| Modals              | `rounded-xl`   | 16px   |

### Django Template Integration

- **Tailwind CSS** provides all design tokens via utility classes
- Material Design 3 color tokens configured in `tailwind.config.js`
- Use utility classes directly in templates: `class="bg-primary text-on-primary py-2 px-4 rounded-md"`
- Component classes use Tailwind utility classes directly (no `@apply`)
- Form errors use: `class="text-error text-xs mt-1"`
- Surface layering: `bg-background` (page) → `bg-surface-container-lowest` (card) → `bg-surface-container` (nested)

### React Dashboard

- **Styling:** Tailwind CSS with Material Design 3 color tokens
- **Component Library:** Radix UI (headless, accessible primitives)
- **Charts:** Recharts styled with primary/secondary colors
- **Tailwind Configuration:** Extends with MD3 tokens:
  - Colors: Surface system, primary, secondary, tertiary, error, outline tokens
  - Spacing: 8px-based scale
  - Border radius: `rounded-sm` (4px) / `rounded-md` (8px) / `rounded-lg` (12px) / `rounded-xl` (16px)
  - Shadows: `shadow-sm/md/lg`
  - Fonts: `font-sans` (Plus Jakarta Sans), `font-mono` (JetBrains Mono)
- **Radix Components:**
  - `@radix-ui/react-dialog` for modals with `bg-surface-container-lowest` styling
  - `@radix-ui/react-dropdown-menu` for dropdowns
- Visual consistency: Use same MD3 tokens as Django templates

### tailwind.config.js Token Reference

All custom tokens must be registered here. Tertiary colors are required for pending badge states:

```js
colors: {
  // ... primary, secondary, surface tokens ...
  tertiary: 'hsl(43, 85%, 35%)',
  'on-tertiary': 'hsl(0, 0%, 100%)',
  'tertiary-container': 'hsl(43, 90%, 88%)',
  'on-tertiary-container': 'hsl(43, 85%, 20%)',
}
```

### Accessibility

- Minimum touch target: `44px × 44px` (buttons, inputs)
- Color is never the only indicator (use icons + text for status badges)
- Focus states must be visible: `focus:ring-2 focus:ring-primary`

### Decisions Made

- **Light mode only:** Faster to build, matches nonprofit/financial context.
- **Plus Jakarta Sans:** Warmer than Inter, better for community-focused branding.
- **8px grid:** Simplifies spacing decisions, aligns with border radius.
- **Monospace for data:** Improves readability of currency amounts and dates in tables.
- **`rounded-md` for buttons:** 8px rounding keeps buttons distinct from cards (`rounded-lg`) and modals (`rounded-xl`). Each element type has one assigned radius — no exceptions.
