---
name: html-css
description: "Implement, review, or validate HTML, CSS, SCSS, Vue templates/styles, and JSX/TSX markup or styling."
---

# HTML/CSS

## Purpose

Apply these rules when implementing or reviewing markup and styles. Derive validation scope before running checks.

## Change Scope

Derive validation and formatting scope from the current change set before running quality commands.

1. Identify changed files using the `Validation Scope` section in [AGENTS.md](../../AGENTS.md).
2. Treat `*.html`, `*.css`, `*.scss`, Vue `<template>` blocks, Vue `<style>` blocks, and JSX/TSX markup as HTML/CSS-relevant changes.
3. Map frontend files such as `*.ts`, `*.tsx`, `*.js`, and `*.vue` to the nearest app, module, or component boundary.
4. Map style/UI files to the owning component or layout boundary.
5. Use the nearest `package.json`, `tsconfig`, app root, component directory, or layout directory as the practical ownership boundary.
6. Escalate scope when a change affects shared UI, reusable styles, exported/public components, design-system contracts, global styles, cross-boundary contracts, or shared frontend paths such as `frontends/shared/`.
7. Include directly dependent units and linked component, visual, contract, or functional tests when scope escalates.

Report the scoped files or ownership units, any escalations, and assumptions when scope is non-obvious.

## Markup Rules

### Semantics

- Use semantic elements whenever possible, such as `header`, `nav`, `main`, `section`, `article`, `aside`, and `footer`.
- Use `div` and `span` only when no semantic element applies.
- Structure markup based on meaning, not visual layout.

### Accessibility

- Prefer semantic elements that provide accessibility by default.
- Ensure interactive elements are keyboard-accessible.
- Do not replace native elements such as `button`, `a`, `input`, `select`, or `textarea` with non-semantic equivalents.
- Preserve accessible names, labels, roles, focus behavior, and form associations when changing existing UI.

## Styling Rules

### Architecture and Naming

- Use BEM naming for new CSS classes: `block__element--modifier`. An existing convention is an exception only when it is consistent and at least as clear as BEM.
- When a BEM migration is needed for the task, limit it to the affected markup and styles.
- Do not introduce ad hoc or inconsistent class names or imitate an ad hoc local pattern to match nearby code.

### Scope

- Keep styles scoped to components, blocks, or layouts.
- Avoid global styles unless explicitly required by the requested change.
- Check for unintended global style leaks when touching shared or global CSS.

### Selectors

- Avoid styling based on element selectors except for resets or base typography.
- Avoid deep nesting.
- Prefer class-based selectors that remain local to the owning component or block.

### Layout

- Prefer modern layout primitives such as `flex` and `grid`.
- Avoid layout hacks.
- Avoid inline styles.
- Avoid hardcoded dimensions unless the component requires a fixed-format constraint.
- Use responsive constraints so text and UI elements do not overlap or overflow across common viewport sizes.

## Change Rules

- Do not modify unrelated markup or styles.
- Do not introduce new runtime dependencies unless explicitly requested.
- Keep changes minimal and focused.

## Validation Rules

- Ensure scoped styles remain scoped and do not leak globally.
- Identify any visually breaking change explicitly.
- Preserve keyboard accessibility and semantic behavior for interactive UI.

## Execution Contract

For implementation, complete these checks in order:

1. Format only edited files with the project formatter, such as Prettier or an equivalent command that targets those files.
2. Keep indentation, class ordering, and attribute ordering consistent with the shared `Formatting` section in [AGENTS.md](../../AGENTS.md).
3. Validate that HTML, Vue templates, or JSX/TSX markup are structurally valid within the derived scope.
4. Validate that CSS, SCSS, or Vue styles compile without errors or warnings within the derived scope.

## Required Closeout

When finishing an HTML/CSS task, report:

- Files created or updated.
- Scoped files, components, layouts, apps, or modules validated.
- Commands run and outcomes.
- Any assumptions, skipped validation, or visually breaking changes with the reason.
