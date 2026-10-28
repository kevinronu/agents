# Process

Four goals, in this order. How much each one takes depends on the doc.

## 1. Understand the doc

Before any comment, say in a few lines what the doc proposes and which services, tables,
queues and external systems it touches. Use the vocabulary of the trusted docs when there
are any ([sources.md](sources.md)); otherwise the doc's own. A reviewer who cannot explain
the design in plain words is not ready to find where it breaks.

## 2. Pick the checks

The table in `SKILL.md` says which checks and skills apply. Read only those. A check that
does not apply produces no comment.

## 3. Verify before stating

A comment that says "X happens" was confirmed where the profile says to verify that kind of
claim: the code for calls and order, the infrastructure for triggers and retries, the data
for numbers. When something cannot be confirmed, the comment says so ("I could not confirm
whether…") instead of stating it. Verification follows
`../../research-proposal/references/verification.md`.

The anchor of each comment is searched in the doc before delivering. An anchor that is not
found is a bug in the review.

## 4. Deliver

The reply lists the comments by severity: what breaks the design first, then what sections
contradict each other, then what is missing, then wording. Two comments that overlap merge,
or one points to the other by its section. The last line says which comments can be dropped
when the author wants fewer. The format is in `../templates/comment.md`.

## Using another skill from here

Each skill says when it applies and what its rules are; this review adds only how to use it
on a doc:

- It is used to read, not to change. Nothing is formatted, run or written, so the parts of a
  skill about change scope, execution and closeout do not apply.
- Its input is the text of the doc (Solution, the Implementation details tab, the diagram)
  plus the code the doc extends.
- A rule the doc breaks becomes a comment, with the rule as the consequence. A rule the doc
  follows produces nothing.
- With `design-pattern-decision`, a comment exists only when its answer and the doc
  disagree: the doc adds an abstraction and the answer is `none`, or the doc branches by case
  and the answer is a pattern. The review does not push a pattern.
