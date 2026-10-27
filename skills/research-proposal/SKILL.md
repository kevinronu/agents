---
name: research-proposal
description: "Write or update a Truora research or proposal doc (the design doc, its Implementation details tab and its tasks CSV). Use when asked to write, cut, restructure or re-estimate one, or to check it after a design change."
---

# Research or proposal

A research or proposal is read by PMs and engineers who do not know the product. Every claim
in it was checked in code, terraform, Lens or Jira, and every section says one thing once,
from the general to the particular.

## What to read

| When | Read |
|---|---|
| Starting a doc, or unsure which kind it is | [references/document-shape.md](references/document-shape.md): research vs proposal, header, sections, size, the three deliverables |
| Writing or rewriting any section | [references/writing-rules.md](references/writing-rules.md): language, names, order, and what each section holds |
| Before stating a fact, a number, a call or a name | [references/verification.md](references/verification.md) |
| Writing or changing Tasks & Estimation or the CSV | [references/tasks.md](references/tasks.md) |
| After any design change, before answering | [references/change-checklist.md](references/change-checklist.md) |
| Writing the Implementation details tab | [references/implementation-details.md](references/implementation-details.md): sections, the fields of each lambda, what goes there and not in the doc |

Templates: [templates/proposal.md](templates/proposal.md) for a new doc,
[templates/implementation.md](templates/implementation.md) for its tab and
[templates/tasks.csv](templates/tasks.csv) for the tasks file. The architecture diagram comes
from the `architecture-diagram` skill; its PNG goes in the Architecture section.

## How to work with Kevin

- Propose before changing when the decision is his (a design choice, what to cut, how to
  split a task). Apply directly when it is a rule in these references.
- Give options with one recommendation, not a neutral list. Answer in Spanish, short.
- Save a lesson here only when he asks. Read the whole file first, merge or replace the rule
  that exists; never add on top. Rules, not history: no "now", "before", dates.

## Done

The doc, the Implementation details tab and the CSV agree with each other and with the
diagram; the body up to "Stop reading here" fits the size limit; the change checklist passed;
and the reply names every claim that is still unverified.
