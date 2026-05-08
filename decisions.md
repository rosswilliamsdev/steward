# Architecture Decisions

## Styling Strategy: Separation of Django Templates and React Frontend

**Date:** 2026-05-08

**Decision:**
- **Django templates** (login, staff admin views) use **inline CSS** for minimal styling
- **React dashboard component** uses **Tailwind CSS** bundled with the React build

**Rationale:**
- Django auth pages are internal/staff-facing and don't require polish
- Inline styles keep them lightweight and avoid asset pipeline complexity
- React dashboard is user-facing and benefits from Tailwind's utility classes
- Tailwind bundling happens only for the React component (via Vite/webpack)
- Keeps concerns separated: pragmatic styling for Django, modern styling for React

**Static Files Structure:**
```
static/
  js/
    dashboard.js       ê React bundle with Tailwind CSS included
```

**Trade-offs:**
- Django templates won't be as visually polished (acceptable for internal tools)
- Avoids setup complexity of compiling Tailwind for server-rendered pages
- React dashboard gets full Tailwind features without affecting Django page load times
