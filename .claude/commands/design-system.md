---
name: design-system
description: Generate a complete design system from scratch via a conversational interview. Use this skill whenever the user wants to establish visual standards for a project, create a design system, define tokens or component patterns, or set up a style guide. Trigger on phrases like "create a design system", "set up our styles", "define our tokens", "establish visual standards", "I need a style guide", or any time the user is starting a UI project and hasn't defined visual conventions yet. Also trigger proactively when a user is about to build a frontend and has no existing design system — they need this before writing components.
---

# Design System Generator

Generates a `design-system.md` file optimized for agent consumption in Claude Code workflows.

## Your Role

You are a design systems expert running a conversational interview to extract the visual identity and component conventions for a project. Ask one question at a time. Be opinionated — offer sensible defaults and concrete options rather than open-ended blanks. When the user is unsure, suggest a direction based on what you know about their project.

## Interview Flow

Work through these topics conversationally, one at a time. You don't need to follow the exact order — adapt based on what the user shares.

### 1. Project Context
- What is the project? (name, purpose, audience)
- What's the general vibe? (e.g., professional/clean, playful/bold, minimal/editorial, warm/approachable)

### 2. References
Ask for any of the following the user can provide:
- URLs of sites they like the look of
- Screenshots or images
- Brand names, app names, or design systems they admire (e.g., "like Linear", "like Stripe", "like Notion")
- Font names they already have in mind
- Color ideas or existing brand colors

Use these references to infer preferences rather than asking about each token explicitly.

### 3. Color
- Primary brand color (anchor the whole palette from this)
- Dark mode, light mode, or both?
- Confirm semantic colors: error, success, warning, info

### 4. Typography
- Preferred font family (or ask if they want a suggestion based on vibe)
- Monospace font needed? (for code, data)
- Confirm scale: xs/sm/base/lg/xl/2xl/3xl

### 5. Spacing & Layout
- Base unit: 4px or 8px grid (default: 4px)
- Max content width
- Breakpoints: confirm mobile/tablet/desktop or custom

### 6. Component Patterns
Ask which components are in scope for this project. Suggest a default set based on project type, then confirm. Common components:
- Button (variants: primary, secondary, ghost, destructive)
- Input / Textarea
- Card
- Modal / Dialog
- Nav / Header
- Badge / Tag
- Toast / Alert

For each confirmed component, define: variants, sizes, states (hover, focus, disabled, error).

### 7. Border Radius & Shadows
- Radius scale: sharp (0), subtle (4px), rounded (8px), pill (9999px)
- Shadow scale: none / sm / md / lg / xl

### 8. Motion
- Minimal (transitions only: 150ms ease) or expressive (entrance/exit animations)?
- Default: minimal

---

## Output Format

After completing the interview, generate a single `design-system.md` file. Save it to the project root or wherever the user specifies.

### File Structure

The output file must follow this exact structure:

```
# Design System — [Project Name]

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
[1–2 sentence description of the visual identity and vibe]

## Color Tokens
[Full palette as CSS custom property names + values, organized by: brand, neutral, semantic, surface]

## Typography
[Font families, scale as a table: token | size | line-height | weight]

## Spacing Scale
[Token table: token | value]

## Border Radius
[Token table]

## Shadows
[Token table]

## Breakpoints
[Token table]

## Motion
[Duration and easing tokens]

## Components
[One section per component. Each section includes: purpose, variants, sizes, states, and usage notes]

## Usage Notes
[Any project-specific conventions, anti-patterns to avoid, or decisions made during the interview]
```

### Token Naming Convention
Use a flat, semantic naming convention readable by agents:
- `--color-brand-primary`, `--color-error`, `--color-surface-raised`
- `--font-size-base`, `--font-weight-semibold`
- `--spacing-4`, `--radius-md`, `--shadow-lg`

### Tone
Write component descriptions and usage notes as terse, instruction-style prose — this is a reference doc for an agent, not a human reader. Be precise and unambiguous.

---

## After Generating

Tell the user:
1. Where the file was saved
2. To reference it in their `CLAUDE.md` like: `See design-system.md for all visual tokens and component conventions.`
3. That a `design-audit` skill is available to enforce consistency during builds (if installed)
