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
