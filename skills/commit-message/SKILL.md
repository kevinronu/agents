---
name: commit-message
description: "Generate, review, or rewrite commit messages from staged changes and the current branch ticket."
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
- Keep the title between 20 and 79 characters.
- Use imperative mood, such as `Fix`, not `Fixed`.
- Capitalize the title.
- Do not end the title with a period.

## Body Rules

- Write the message in English.
- Keep every line under 80 characters.
- Use concise, specific wording based on the staged diff.
- Preserve exact spacing: one blank line after the title and one blank line before the ticket when a ticket exists.
- Do not add extra blank lines.

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

Verify the message against the template, title, body, ticket, and type rules above.

If any check fails, rewrite and re-validate before returning.

## Execution Contract

Complete the required inspection, generate the message, and pass the validation checklist before returning.

Return only one plain-text commit message unless the user explicitly asks for analysis or multiple options.
