---
name: Stewardship Design Language
colors:
  surface: '#f6fbf2'
  surface-dim: '#d6dcd3'
  surface-bright: '#f6fbf2'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f5ec'
  surface-container: '#eaefe6'
  surface-container-high: '#e4eae1'
  surface-container-highest: '#dfe4db'
  on-surface: '#181d17'
  on-surface-variant: '#3f493f'
  inverse-surface: '#2c322c'
  inverse-on-surface: '#edf2e9'
  outline: '#6f7a6e'
  outline-variant: '#becabc'
  surface-tint: '#006d30'
  primary: '#00652c'
  on-primary: '#ffffff'
  primary-container: '#15803d'
  on-primary-container: '#d3ffd5'
  inverse-primary: '#79db8d'
  secondary: '#436648'
  on-secondary: '#ffffff'
  secondary-container: '#c4edc6'
  on-secondary-container: '#496d4d'
  tertiary: '#97344a'
  on-tertiary: '#ffffff'
  tertiary-container: '#b64c62'
  on-tertiary-container: '#fff1f1'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#95f8a7'
  primary-fixed-dim: '#79db8d'
  on-primary-fixed: '#00210a'
  on-primary-fixed-variant: '#005323'
  secondary-fixed: '#c4edc6'
  secondary-fixed-dim: '#a9d0ab'
  on-secondary-fixed: '#00210a'
  on-secondary-fixed-variant: '#2c4e32'
  tertiary-fixed: '#ffd9dd'
  tertiary-fixed-dim: '#ffb2bd'
  on-tertiary-fixed: '#400013'
  on-tertiary-fixed-variant: '#81233b'
  background: '#f6fbf2'
  on-background: '#181d17'
  surface-variant: '#dfe4db'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 60px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 38px
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  data-lg:
    fontFamily: JetBrains Mono
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 24px
  data-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  data-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
---

## Brand & Style

The visual identity of this design system centers on the concept of "Nurtured Stability." As a platform for community foundations, the UI must balance the gravitas of financial management with the approachability of local philanthropy. It is designed to evoke a sense of long-term partnership and communal growth.

The chosen style is **Corporate / Modern**, refined with a humanist touch. It avoids the coldness of traditional fintech by utilizing high-quality typography and soft organic tones, while maintaining the structural rigor expected of a professional management tool. The aesthetic priority is clarity and information density, ensuring that foundation administrators can manage complex fund distributions without cognitive fatigue. The "warmth" is achieved through generous whitespace and a color palette rooted in the natural world.

## Colors

The color strategy uses an **Earthy Green** as its primary anchor, symbolizing growth, sustainability, and the "evergreen" nature of donor-advised funds. 

- **Primary:** Utilized for key actions, active states, and brand-building moments.
- **Neutrals:** A vast range of grays allows for subtle layering of surfaces. Neutral-900 is used for high-contrast primary text, while Neutral-500 is the floor for accessible secondary text.
- **Semantic Palette:** These follow industry standards for immediate recognition but are calibrated to match the saturation levels of the primary green to ensure a cohesive visual field.
- **Contrast:** The system enforces a 1px border at `hsl(0, 0%, 90%)` for all surface divisions to maintain structural clarity in data-dense environments.

## Typography

This design system utilizes a dual-font strategy to separate narrative from data.

- **Plus Jakarta Sans** is the primary typeface. Its soft, rounded terminals provide an optimistic and welcoming tone for headlines and body copy. It excels in readability and gives the platform its "community-focused" personality.
- **JetBrains Mono** is reserved strictly for monospaced requirements: currency amounts, dates, account numbers, and transaction IDs. This creates a clear visual distinction for "hard data," signaling to the user that these elements require precise attention.

**Scale:** Headlines use a tighter letter-spacing to feel more authoritative, while body text uses a generous line-height to ensure accessibility for a diverse range of donor demographics.

## Layout & Spacing

This design system is built on a strict **8px spacing grid**. All padding, margins, and component heights must be multiples of 8 to maintain a mathematical rhythm across the interface.

**Layout Model:**
- **Desktop (1440px+):** 12-column fluid grid with 24px gutters and 32px outer margins.
- **Tablet (768px - 1439px):** 8-column fluid grid with 16px gutters and 24px outer margins.
- **Mobile (Below 768px):** 4-column fluid grid with 16px gutters and 16px outer margins.

**Principles:**
Use `spacing.lg` (24px) for the standard gap between distinct cards or sections. Use `spacing.sm` (8px) for internal component spacing, such as the distance between an icon and a text label. This hierarchy ensures that related items are visually grouped while maintaining breathing room between major functional areas.

## Elevation & Depth

Visual hierarchy is managed through **Tonal Layering** and **Layered Shadows**. To maintain a professional, trustworthy appearance, elevation is used sparingly to indicate interactivity or focus.

- **Level 0 (Flat):** The main canvas background (Neutral-50).
- **Level 1 (Card):** Surface-level elements like fund cards or tables. These use a 1px border (`hsl(0, 0%, 90%)`) and the `shadow-sm` (a subtle 2px blur) to sit just above the background.
- **Level 2 (Active/Hover):** Interactive cards upon hover use `shadow-md` to invite clicks.
- **Level 3 (Overlays):** Modals, dropdowns, and flyouts use `shadow-xl` (a deep, multi-layered 24px blur with low opacity) to create distinct separation from the underlying content.

Shadows should never be pure black; they are tinted with a hint of the primary green or a deep charcoal to maintain the "earthy" warmth of the brand.

## Shapes

The shape language is defined by a consistent **8px (0.5rem)** radius for most structural elements. This creates a "Softened Professional" look—not as rigid as sharp corners, but more serious than fully rounded bubbles.

- **Standard Radius:** 8px for cards, input fields, containers, and primary buttons.
- **Large Radius:** 16px (1rem) for decorative image containers or featured promotional cards.
- **Pill Radius:** 9999px for chips, tags, and status badges. This distinction ensures that data labels (pills) are never confused with structural containers (cards).
- **Iconography:** Icons should feature slightly rounded terminals to match the font characteristics of Plus Jakarta Sans.

## Components

**Buttons:**
- **Primary:** Earthy Green background, white text, 8px radius.
- **Secondary:** Neutral-100 background, Neutral-900 text.
- **Tertiary:** Ghost style (no background), Primary Green text.
- **Pill Variant:** Use 9999px radius only for "Apply Filter" or "Add Tag" style buttons to differentiate from primary DAF actions.

**Input Fields:**
Inputs must have a 1px border (Neutral-300) that thickens and changes to Primary Green on focus. Labels use `body-sm` in Neutral-700.

**Cards (The "Fund Card"):**
The core of the platform. Fund cards must feature a clear header using `headline-sm`, a dedicated area for "Balance" using `data-lg` in JetBrains Mono, and a 1px border.

**Status Chips:**
- **Active:** Success Green (10% opacity background, 100% opacity text).
- **Pending:** Warning Yellow (10% opacity background, 100% opacity text).
- **Closed:** Neutral-500.

**Data Tables:**
Headers should be Neutral-100 with `data-sm` labels. Row height should be a minimum of 56px to ensure touch-friendly targets and legibility.

**Fund Progress Bars:**
Used for tracking contribution goals. Use Primary Green for the filled state and Neutral-200 for the track, with an 8px radius for the container.