---
name: typescript
description: Enforce strict guardrails for implementing and validating TypeScript changes. Use when Codex writes, modifies, reviews, formats, scopes, type-checks, or tests TypeScript code, TSX/JSX code, JavaScript in TypeScript-owned modules, Vue script blocks, frontend modules, or public TypeScript contracts, including deriving the affected app, module, or component scope from changed files before running checks and orchestrating design-pattern classification when TypeScript code may need pattern-level structure.
---

# TypeScript

## Purpose

Act as a TypeScript implementation guard. Apply these rules to all TypeScript-related changes, then format, type-check, and test only within the derived change scope unless escalation rules require a broader scope.

## Change Scope

Derive formatting, type-checking, and test scope from the current change set before running quality commands.

1. Identify changed files using [Validation Scope](../../AGENTS.md#validation-scope).
2. Treat `*.ts`, `*.tsx`, `*.js`, `*.jsx`, and Vue `<script>` blocks as TypeScript-relevant when they belong to a TypeScript app or module.
3. Treat `*.vue` changes as TypeScript-relevant when script logic, component contracts, props, emits, stores, routing, API calls, or tests are affected.
4. Map each changed frontend file to the nearest app, module, or component boundary.
5. Use the nearest `package.json`, `tsconfig`, app root, component directory, store directory, or feature module as the practical ownership boundary.
6. Escalate scope when a change affects exported/public interfaces, shared modules, reusable components, shared stores, API clients, cross-boundary contracts, or shared frontend paths such as `frontends/shared/`.
7. Include directly dependent units and linked component, contract, functional, or frontend tests when scope escalates.
8. Escalate to full repository scope only when the change invalidates global assumptions or the user explicitly requests full-repo validation.

Report the scoped files or ownership units, any escalations, and assumptions when scope is non-obvious.

## Change Rules

- Do not modify unrelated code, modules, components, stores, routes, or tests.
- Keep changes minimal and focused.
- Do not introduce new runtime dependencies unless explicitly requested.

## Code Rules

### Types and Contracts

- Prefer explicit types at module boundaries.
- Avoid `any` and `unknown` unless explicitly justified.
- Narrow types as early as possible.
- Add runtime validation for untrusted input.
- Preserve public contract compatibility unless a breaking change is explicitly required.
- Keep type assertions local and justified by surrounding validation or framework constraints.

### Architecture

- Apply design patterns only when they clearly match the problem.
- For new code, introduce patterns when appropriate.
- For existing code, request confirmation before changing design patterns.
- Keep domain logic independent from frameworks and runtime concerns.
- Prefer existing project helpers, stores, composables, services, and API clients over new abstractions.

## Design Patterns

Invoke `design-pattern-decision` when choosing or changing an abstraction to address recurring complexity, or when explicitly asked to select a pattern. Simple fixes and direct implementations do not require classification.

When invoking it, read and use the [input contract](../design-pattern-decision/references/input-contract.md).

Set `Language` to `typescript`.

Continue based on `Recommended pattern`:

- `none`: continue with this TypeScript skill only.
- any other pattern: use it to develop or adjust the plan, tentative code, current code, or intended change. If a matching `typescript-pattern-<recommended-pattern>` skill is available, invoke it and treat its result as a pattern skeleton. Otherwise, apply the pattern using general TypeScript knowledge. Then continue in this TypeScript skill for implementation rules, type-checking, tests, formatting, and validation.

Do not invoke `design-pattern-decision` again after returning from a TypeScript pattern skill unless the plan, tentative code, or current code summary materially changes.

### Async

- Prefer `async` and `await` over promise chaining.
- Do not introduce unhandled promises.
- Avoid shared mutable state across async boundaries.
- Handle errors explicitly and preserve user-visible failure states where relevant.

## Tests

### Structure

- Add or update tests when behavior changes.
- Use one explicit `it(...)` or `test(...)` per scenario.
- Prefer explicit tests over grouped or generated scenarios.

### Rules

- Do not use parameterized or table-driven tests by default, including `it.each`, `test.each`, or loops that generate tests.
- Validate a single logical condition per test.
- Always assert errors and relevant side effects.
- Avoid global state in tests.
- Keep mocks, fixtures, and setup scoped to the owning test or module.

### Exceptions

- Use parameterized tests only when duplication is extreme.
- Include a brief justification comment when using parameterized tests.

## Validation Rules

- Ensure formatting is consistent.
- Ensure type-checking passes with `tsc --noEmit` or the project equivalent.
- Ensure no type regressions are introduced.
- Ensure module boundaries are respected.
- Run scoped tests when behavior changes.

## Execution Contract

A TypeScript task is complete only when all steps succeed in this order:

1. Format only edited files with the project formatter, using a command that targets those files.
2. Type-check within the derived change scope with the project typecheck script or `tsc --noEmit`.
3. Run tests only within the derived change scope.

Do not format, type-check, or test the entire repository unless the user explicitly requests it or scope escalation reaches full-repository impact.

If no scoped formatter exists, run Prettier only on modified files. If no scoped type-check or test command exists, run the smallest project-level command that covers the derived scope and report that assumption.

## Required Closeout

When finishing a TypeScript task, report:

- Files created or updated.
- Scoped apps, modules, components, stores, or tests validated.
- Commands run and outcomes.
- Any assumptions or skipped validation with the reason.
