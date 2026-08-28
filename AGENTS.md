
# Global Agent Instructions

You are a senior engineer. Follow the instructions for the language or task you are modifying.

---

## Skills

Before writing code, running validation, or generating commit messages, load the relevant skill(s) for the task.

Available project skills:

- `$go`
- `$typescript`
- `$html-css`
- `$terraform`
- `$commit-message`

If a change touches multiple areas, load every relevant skill before making edits.

---

## Validation Scope

Do not decide validation scope manually from memory. The relevant skill must derive the change scope from the current change set before formatting, testing, linting, validating, planning, type-checking, or generating commit messages.

---

## Code Organization & Readability

These rules are mandatory and take precedence over repository-level skills. Repository skills may add stricter or additional requirements, but they must not weaken or override these rules.

- Declare code in increasing order of abstraction.
- Low-level, leaf logic must appear before higher-level orchestration.
- A reader should be able to understand any block using only code defined above it.
- Avoid forward mental jumps: do not reference logic that is defined later.

### Comments

This section governs explanatory comments. Documentation on exported identifiers is a separate category, covered below.

Default to no comment. A comment is a last resort, not a habit.

> "The proper use of comments is to compensate for our failure to express ourselves in code. Note that I used the word failure. I meant it. Comments are always failures of either our languages or our abilities."
>
> — Robert C. Martin, *Clean Code*, 2nd ed. (2025), ch. 5 "Comments"

Before writing a comment, try to delete the need for it: rename, extract a function, or simplify the structure. Write the comment only if the need survives that attempt.

A comment may only say why. Write one to record:

- A decision, a tradeoff, or a constraint the reader cannot see in the code.
- Intent behind code whose purpose is not obvious from its shape.
- A consequence or risk the reader would not expect.
- A warning about something that looks trivial or removable but is not.
- Behavior forced by an external API, a known bug, or a legal requirement you do not control.
- A `TODO` for work deliberately deferred, with the reason stated.

Never write:

- Prose that restates the code, a name, a type, a signature, or a test.
- Narration of control flow, or an announcement of what the next lines do.
- Section banners, position markers, or closing-brace labels.
- Change logs, dates, migration notes, or author attributions. Git already holds that history.
- Commented-out code. Delete it.

Length is a hard limit, not a preference. One line. Two only when the why genuinely needs them, never a paragraph. If the explanation does not fit, the code or the name is the problem: fix that first. If it still does not fit, it is not a comment: it belongs in the commit message, the pull request, or project documentation.

Do not narrate your reasoning. State the constraint that remains, not how you reached it. Name an option you rejected only when that option is the point of the comment, and in one clause.

Write in plain English around a B2 level. Update or delete any comment your change makes false: an inaccurate comment is worse than no comment. These rules govern the comments you write or touch; do not sweep unrelated comments out of files you only happen to open.

### Documentation Comments

Documentation on an exported identifier is a contract for callers, not an explanation of the implementation, so the default above does not apply to it. Write it when a language or task skill requires it, such as doc comments on exported Go identifiers.

- Open with one sentence stating the purpose. Add a line only for an input, output, error, or side effect the caller cannot infer from the signature.
- Do not describe how the body works. The implementation may change; the contract should not.
- Never fill in a template. The skill decides the syntax, not the volume: skip any section the format offers when it would restate the signature.
- Do not document unexported identifiers for symmetry. There the default applies.
- The delete-first rule applies here too: if a linter demands documentation for an identifier whose contract tells the reader nothing, unexport it instead of writing the comment.
- Follow the format the language skill requires.
