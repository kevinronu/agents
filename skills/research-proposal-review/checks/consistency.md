# Consistency

## When it applies

Always.

## What to look for

The same decision told in two sections with two outcomes. The usual pairs:

- **Goals and Scenarios vs Solution rules.** A goal says the account "keeps working as
  today"; a rule in Solution says the router returns an error for it.
- **Data model vs the operations that read it.** The model says a field is absent in most
  rows; a rollback finds rows by that field's value. The same state with two names in two
  sections (`manual_review` in the model, `multiple_faces` in the rules).
- **Non-Goals vs Tasks.** Something excluded in Non-Goals has a task.
- **Failure Modes vs Launch and Tasks.** An alarm in Failure Modes has no task; a deploy
  step in Launch does not match the order of the tasks.
- **The summary vs the body.** "Nothing changes for clients" in the TL;DR, and a step in
  Solution that deletes something the client created.

## How to confirm

Read the two passages side by side and quote both. No code needed: the contradiction is in
the text.

## Severity

Two sections with different outcomes: the design is undecided, grave. Two names for one
state: a fix of the doc, can be dropped if the author asks for fewer.

## Example

> So the account is blocked until someone reviews it, as the Overview and Launch also say.
> But the Goals still say "it is marked for manual review and keeps working as today", and
> the Scenarios say "validations work as today".
