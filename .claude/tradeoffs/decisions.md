# Architecture Decisions

## Styling Strategy: Separation of Django Templates and React Frontend

**Date:** 2026-05-08

**Decision:**

- **Django templates** (login, staff admin views) use **external CSS file** (`static/css/styles.css`) for styling
- **React dashboard component** uses **Tailwind CSS** bundled with the React build

**Rationale:**

- All Django template styles are in a single external CSS file for maintainability
- No inline `<style>` tags or `style=""` attributes in HTML templates
- Django auth pages are internal/staff-facing and don't require a full design system
- React dashboard is user-facing and benefits from Tailwind's utility classes
- Tailwind bundling happens only for the React component (via Vite/webpack)
- Keeps concerns separated: simple CSS for Django, modern design system for React

**Static Files Structure:**

```
static/
  css/
    styles.css         ← All Django template styles
  js/
    dashboard.js       ← React bundle with Tailwind CSS included
```

**Trade-offs:**

- Django templates use basic CSS, not a modern utility framework (acceptable for internal tools)
- Avoids setup complexity of compiling Tailwind for server-rendered pages
- React dashboard gets full Tailwind features without affecting Django page load times
- Simple CSS file is easy to maintain without build tooling

## Tailwind CSS Version: v3 vs v4

**Date:** 2026-05-09

**Decision:**

Use **Tailwind CSS v3.4.16** instead of the latest v4.3.0.

**Context:**

- Solo developer, familiar with Tailwind
- 1-week project timeline
- Django project with eventual React integration
- Need stable tooling and clear documentation

**Options Considered:**

### Option 1: Tailwind v4 (latest stable)
- **What it is:** Newest version with PostCSS-only architecture, no CLI, no `tailwind.config.js`
- **Optimized for:** Cutting-edge projects comfortable with newer tooling patterns
- **Limitation:** Fundamentally different setup; less mature Django integration examples; fewer guides

### Option 2: Tailwind v3 (mature)
- **What it is:** Established version with standalone CLI and traditional config file approach
- **Optimized for:** Production projects needing stability, mature ecosystem, well-trodden paths
- **Limitation:** Not the "latest" version; eventual migration to v4 needed

**Why v3:**

1. **Tight timeline:** Don't want surprises or undocumented quirks during 1-week build
2. **Django integration:** v3 has extensive Django-specific guides and examples
3. **Tooling maturity:** Better VS Code extensions, more Stack Overflow answers
4. **npm scripts workflow:** v3's PostCSS integration is well-established and works seamlessly with eventual React build setup
5. **Risk mitigation:** v4's new architecture is stable but less battle-tested in Django contexts

**Build Process Decisions:**

- **Method:** npm scripts with PostCSS (not standalone CLI)
  - **Why:** Unifies with eventual React build process; single toolchain
  - **Alternative considered:** Tailwind CLI (simpler but isolated)

- **File scanning scope:** Broad patterns (`*/templates/**/*.html`, `*/static/**/*.{js,jsx,tsx}`)
  - **Why:** Future-proof; never forget to add paths as project grows
  - **Trade-off:** Slightly slower builds (~200-300ms vs 50ms), negligible for small project

- **File organization:**
  - **Source:** `src/input.css` (Tailwind directives + custom CSS)
  - **Output:** `core/static/core/css/styles.css` (compiled, Django-served)
  - **Why:** Follows Django best practices for app-level static files; keeps source separate from compiled output

**Design System Integration:**

Tailwind config extends with Steward design tokens from `.claude/context/design-system.md`:
- Custom color palette (brand, neutral, semantic colors)
- Typography scale (Plus Jakarta Sans, custom sizes)
- Spacing, border radius, shadows matching design system

**Trade-offs Accepted:**

- Will need to migrate to v4 eventually (but not during MVP week)
- Slightly more verbose config than v4's new approach
- Build process is developer-time overhead (200-300ms), not user-facing

**Outcome:**

Stable, predictable Tailwind setup ready for both Django templates and React components.

---

## Using HSL for all colors