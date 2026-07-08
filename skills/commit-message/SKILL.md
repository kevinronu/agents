---
name: commit-message
description: Enforce strict guardrails for generating high-quality commit messages. Use when Codex is asked to create, draft, suggest, validate, or rewrite a commit message, especially from staged git changes and the current branch ticket.
---

# Commit Message

## Purpose

Act as a commit message generation guard. Generate exactly one high-quality commit message based strictly on staged changes, validated context, and the current branch ticket when available.

## Required Inspection

Inspect staged changes before generating any message:

1. Run `git diff --staged --name-only`.
2. Run `git diff --staged`.
3. Run `git branch --show-current`.

Use staged changes as the primary source of truth. Use chat context only when it clearly explains intent or rationale already visible in the staged changes. Ignore unrelated context and never fabricate missing information.

If there are no staged changes, do not invent a message. Report that no staged changes were found.

## Message Template

Produce exactly this structure:

```text
<type>[optional scope]: <subject>

What: <explain what changed>
Why: <explain why it changed>

<ticket>
```

Omit the final blank line and ticket line when no ticket is detected.

## Title Rules

- Use one of the allowed types: `Feat`, `Fix`, `Refactor`, `Docs`, `Test`, or `Chore`.
- Use optional scope only when it is clear and useful.
- Keep the title between 20 and 80 characters.
- Use imperative mood, such as `Fix`, not `Fixed`.
- Capitalize the title.
- Do not include the ticket in the title.
- Do not end the title with a period.

## Body Rules

- Include both `What:` and `Why:` lines.
- Write the message in English.
- Keep every line under 80 characters.
- Use concise, specific wording based on the staged diff.
- Preserve exact spacing: one blank line after the title and one blank line before the ticket when a ticket exists.
- Do not add extra blank lines.
- Do not output commentary, alternatives, markdown fences, or explanations unless the user explicitly asks for them.

## Ticket Rules

- Extract the ticket from the current branch using `([A-Za-z]+-\d+)`.
- Normalize the ticket to uppercase.
- For branches like `IACE-925-add-component-for-options-list`, use only `IACE-925`.
- Include the ticket only when extraction succeeds.
- Omit the ticket for `main` and `master`.
- Never fabricate tickets or use placeholders.
- Never put the ticket in the title.

## Type Mapping

- `Feat`: New behavior or capability.
- `Fix`: Bug fix.
- `Refactor`: Structural change without behavior change.
- `Docs`: Documentation-only change.
- `Test`: Test-related changes.
- `Chore`: Maintenance, tooling, configuration, formatting, or dependency updates.

When multiple mappings appear possible, choose the type that reflects the dominant staged change.

## Validation Checklist

Before returning, verify:

- The message follows the required template exactly.
- The title is 20 to 80 characters.
- The title uses imperative mood and no ticket.
- `What:` and `Why:` are present.
- Every line is under 80 characters.
- The ticket, when present, was extracted from the branch and uppercased.
- No placeholder ticket or fabricated rationale is present.
- The output is a single commit message.

If any check fails, rewrite and re-validate before returning.

## Execution Contract

A commit message task is complete only when all steps succeed in this order:

1. Inspect staged files, staged diff, and current branch.
2. Derive intent from staged changes.
3. Use relevant chat context only when it clarifies staged changes.
4. Extract and normalize the ticket from the branch when available.
5. Generate one message with the required template and type mapping.
6. Validate structure, spacing, title, body, line length, and ticket rules.

Return only the commit message unless the user explicitly asks for analysis or multiple options.
