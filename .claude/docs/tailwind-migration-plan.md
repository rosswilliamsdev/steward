# Tailwind CSS Migration Plan

## Context

**Current State:**
- Completed design system creation via `/design-system` slash command
- Design tokens defined: earthy green palette (#16A34A / hsl(142, 76%, 36%)), Plus Jakarta Sans typography, light mode only, 8px spacing grid
- Initially implemented with CSS custom properties in `static/css/styles.css` (lines 1-100)
- Decided to use Radix UI for React dashboard components
- User wants to switch to **Tailwind CSS** for styling

**Why Tailwind:**
- Works seamlessly with both Django templates (`.html`) and React components (`.jsx`)
- Utility-first approach matches modern development practices
- Built-in design system via `tailwind.config.js`
- Better integration with Radix UI headless components
- Single build process generates CSS for entire app

**How Tailwind Works with Django + React:**
- Django templates: `<button class="bg-brand-primary hover:bg-brand-primary-hover text-white font-medium py-2 px-4 rounded-md">`
- React components: `<button className="bg-brand-primary hover:bg-brand-primary-hover text-white font-medium py-2 px-4 rounded-md">`
- Configure Tailwind to scan both file types: `content: ['**/*.html', '**/*.jsx']`
- One CSS output file used by both Django and React

## Tasks

### 1. Update Design System Documentation
**File:** `.claude/context/design-system.md`

- [ ] Replace CSS custom properties approach with Tailwind utility class examples
- [ ] Update component specifications to show Tailwind classes instead of custom properties
- [ ] Update "Django Template Integration" section for Tailwind usage
- [ ] Update "React Dashboard" section for Tailwind + Radix UI integration
- [ ] Add Tailwind config reference section

### 2. Create Tailwind Configuration
**File:** `tailwind.config.js` (new file)

Convert design tokens from `.claude/context/design-system.md` to Tailwind config:

```javascript
module.exports = {
  content: [
    './core/templates/**/*.html',
    './core/static/**/*.jsx',
    // Add other template paths as needed
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: 'hsl(142, 76%, 36%)',
          'primary-hover': 'hsl(142, 70%, 31%)',
          'primary-light': 'hsl(142, 76%, 85%)',
          'primary-dark': 'hsl(142, 76%, 20%)',
        },
        neutral: {
          50: 'hsl(0, 0%, 98%)',
          100: 'hsl(0, 0%, 96%)',
          // ... full neutral scale
        },
        // semantic colors, surface colors, etc.
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Courier New', 'monospace'],
      },
      fontSize: {
        xs: '0.75rem',
        sm: '0.875rem',
        base: '1rem',
        lg: '1.125rem',
        xl: '1.25rem',
        '2xl': '1.5rem',
      },
      spacing: {
        // 8px grid: 0, 4, 8, 12, 16, 24, 32, 40, 48
      },
      borderRadius: {
        none: '0',
        sm: '4px',
        md: '8px',
        lg: '12px',
        full: '9999px',
      },
      boxShadow: {
        // sm, md, lg, xl shadows from design system
      },
    },
  },
  plugins: [],
}
```

### 3. Setup Tailwind Build Process
**Files:** `package.json`, PostCSS config

- [ ] Install Tailwind: `npm install -D tailwindcss postcss autoprefixer`
- [ ] Create `postcss.config.js`
- [ ] Create CSS entry point that imports Tailwind directives
- [ ] Update build scripts in `package.json`
- [ ] Configure Django to serve the compiled Tailwind CSS

### 4. Update Static CSS File
**File:** `static/css/styles.css`

- [ ] Replace CSS custom properties (lines 1-87) with Tailwind imports:
  ```css
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
  ```
- [ ] Move any custom non-Tailwind styles below the imports
- [ ] Keep base.html styles for layout if needed

### 5. Update Implementation Plan
**File:** `.claude/docs/donor-views-implementation-plan.md`

- [ ] Update section 1.2 to reflect Tailwind approach instead of CSS custom properties
- [ ] Update section 2.2 React dashboard implementation to use Tailwind + Radix UI

### 6. Update CLAUDE.md (Optional)
**File:** `CLAUDE.md`

- [ ] Add note about Tailwind CSS usage in project conventions
- [ ] Document that both Django templates and React use Tailwind

## Design Token Reference

All tokens from `.claude/context/design-system.md` to be converted:

- **Colors:** Brand (primary, hover, light, dark), Neutral (50-900), Semantic (success, warning, error, info), Surface (base, raised, overlay), Text (primary, secondary, tertiary, inverse)
- **Typography:** Font families (Plus Jakarta Sans, JetBrains Mono), Font sizes (xs-2xl), Font weights (400-700)
- **Spacing:** 8px grid (0, 4, 8, 12, 16, 24, 32, 40, 48)
- **Border Radius:** none, sm (4px), md (8px), lg (12px), full (9999px)
- **Shadows:** none, sm, md, lg (with RGBA values)
- **Motion:** Fast (150ms), slow (300ms), ease

## Notes

- Tailwind content paths must include both Django templates (`**/*.html`) and React files (`**/*.jsx`)
- Use custom color names (e.g., `bg-brand-primary`) rather than Tailwind defaults for brand consistency
- Radix UI components will be styled using Tailwind utility classes
- BEM naming still applies to custom component classes not covered by Tailwind utilities
- Keep the 8px spacing grid intact via Tailwind spacing scale
