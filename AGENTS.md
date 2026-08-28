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

These rules are mandatory and govern every line of code you write or modify. Language-specific, task-specific, and repository-level skills may add stricter or additional requirements, but they may not weaken, contradict, reinterpret, or override this section.

Language syntax and compiler requirements remain binding. When they constrain how a rule can be applied, preserve its intent as far as the language allows. Do not treat language idioms, repository conventions, or existing code as permission to ignore these rules.

Existing code and repository conventions are not authority for organization or readability. Apply these rules even when the surrounding code does the opposite. Do not imitate a local smell for consistency, and do not rewrite unrelated code solely to make it comply.

Optimize for the reader because code is read far more often than it is written. Prefer the simplest design that supports the required behavior. Before adding a hook or generalization for a possible future need, consider the cost of leaving it out and adding it later if it becomes necessary.

### Organization and Reading Order

- Give each module, class, and function one coherent topic or responsibility.
- Organize code like a newspaper article: public entry points and high-level policy first, then progressively lower-level details.
- Place a caller above the helpers it invokes when the language permits it. Keep those helpers nearby and, when practical, order them by first use.
- Descend one level of abstraction at a time. Do not mix business intent, orchestration, and low-level mechanics in the same block.
- Keep strongly related concepts vertically close. Use blank lines to separate distinct concepts.
- Declare local variables close to their first use. Keep fields, constants, and other module-level declarations in a predictable location that preserves the clearest reading order allowed by the language.
- Keep high-level policy ignorant of low-level implementation details. Use abstractions to isolate those details and keep source dependencies pointing from low-level details toward high-level policy.

### Names

- Use intention-revealing names that make purpose, behavior, and usage clear without a comment.
- Use one consistent word for each concept. Match the domain vocabulary used by the product and the solution vocabulary used by the codebase.
- Prefer pronounceable and searchable names. Reserve single-letter or abbreviated names for tiny scopes and established conventions.
- Make variable-name length proportional to scope: a short local may be concise, while a long-lived or widely visible value needs a more explicit name.
- Name functions and methods with verbs or verb phrases and classes or objects with nouns or noun phrases. Name accessors, mutators, and predicates according to the language's established idioms.
- Include the unit in a name when it is needed to reveal intent, such as `elapsedDays`.
- Avoid encodings, type prefixes, misleading container names, arbitrary numeric suffixes, noise words such as `Data` or `Info` when they add no distinction, and cute or cryptic names.
- Replace an unexplained index or value with a named constant or an object that exposes its meaning.

### Functions

- Keep functions small enough to understand at a glance, but do not extract code solely to satisfy a line-count target.
- A function must do one coherent thing at one level of abstraction. If a block can be given a precise name and separating it improves the reading flow, extract it.
- Make function bodies read like well-written prose. Keep blocks short and avoid nesting beyond one or two indentation levels when practical.
- Use few arguments. Treat more than three as a design signal to examine, not as an automatic failure; group arguments only when they form a cohesive concept.
- Avoid boolean flag arguments that select different behaviors. Prefer separate functions for the separate cases.
- Prefer return values to output arguments.
- Separate commands from queries when practical: a function should either change state or answer a question, not obscurely do both.
- Keep error handling as one concern. In Go, returning an error together with a value is reasonable when that convention is applied narrowly and consistently.
- Avoid side effects when practical. When they are necessary, encapsulate them so their temporal coupling does not leak to callers.
- Remove duplication when it represents one concept or policy that must change together. Do not force coincidentally similar code into a shared abstraction.

### Modules, Classes, and Data

- Keep modules and classes cohesive, with a narrow public surface and implementation details hidden behind it.
- Split a module or class when separate groups of behavior have different reasons to change.
- Use objects to hide data behind behavior and abstractions. Use data structures to expose data without significant behavior. Avoid hybrids that expose their internals while also containing significant behavior.
- Do not expose an object's implementation merely by adding getters and setters for its internal variables.
- Keep source dependencies pointing toward stable abstractions and away from volatile concrete details.

### Formatting

- Use the repository's automated formatter for mechanical formatting when available. Its output does not override the organization and readability rules in this section.
- Keep formatting consistent across the codebase so the same structural cues carry the same meaning in every file.
- Use blank lines to separate distinct concepts and keep tightly related lines visually dense.
- Keep indentation shallow. Do not collapse scopes or control flow onto one line merely because the body is short.
- Keep lines short enough that readers do not need to scroll horizontally. A repository limit may be followed only when it is equally or more restrictive.
- Do not use manual column alignment that normal formatting will break.

### Comments

This section governs explanatory comments. Documentation for public APIs is covered separately below.

Default to no comment. First try to express the idea through a better name, an extracted function, or a simpler structure. Write a comment only when the code cannot express the necessary information clearly.

A comment is acceptable only when it fits one of these forms:

- **Legal requirements** — required copyright, license, or attribution text.
- **Informative context** — facts the code cannot state, such as the intended format of a regular expression.
- **Intent and rationale** — why a non-obvious decision or tradeoff exists.
- **Clarification** — the meaning of an obscure value from an API or dependency that cannot be changed.
- **Warning of consequences** — a surprising risk, side effect, performance cost, or concurrency constraint.
- **Amplification** — why a detail that looks trivial or removable is essential.
- **Public API documentation** — caller-facing contracts, governed by [Documentation Comments](#documentation-comments).

Do not commit `TODO` comments. Complete the work, remove the need, or record it in the project's tracked backlog before committing.

Never write comments that:

- Restate code, names, types, signatures, or tests.
- Narrate control flow or announce what the following lines do.
- Compensate for confusing code that can be renamed, extracted, or simplified.
- Repeat information already stated elsewhere or describe behavior far from the code that owns it.
- Serve as section banners, position markers, closing-brace labels, journals, change logs, dates, or personal bylines.
- Preserve commented-out code. Delete it; version control retains history.
- Contain HTML, irrelevant history, or more information than the code's reader needs.
- Depend on private context or have a connection to the code that is not obvious.

Keep every necessary comment precise, local to the code it qualifies, and no more detailed than needed. Write it for a reader who does not share the author's private context. Update or delete any comment made inaccurate by the change; a misleading comment is worse than no comment.

### Documentation Comments

Well-written documentation is valuable for public APIs, but it is subject to the same accuracy and relevance requirements as every other comment.

- Write useful documentation for public APIs and follow the documentation syntax required by the language.
- Do not restate the identifier's name, signature, or behavior when the code already expresses it clearly.
- Keep documentation accurate, local, and limited to information callers need.
- Do not add documentation to nonpublic code merely for formality.

### Tests

- Apply the same naming, organization, formatting, and comment standards to test code as to production code.
- Give each test one clearly named behavioral fact. Multiple assertions are acceptable when they establish that same fact.
- Follow Arrange–Act–Assert and keep one act per test.
- Extract test helpers or a small domain-specific testing vocabulary when they remove noise without hiding behavior.
- Keep tests fast, isolated, repeatable, self-validating, and timely by writing them with the production code they protect.

Working code is not finished until it reads well. First make it work, then make it right, and leave the code cleaner than you found it.
