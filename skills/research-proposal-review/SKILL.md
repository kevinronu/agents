---
name: research-proposal-review
description: "Review a research or proposal doc and draft the comments to post on it. Use when asked to review, check or comment a research or proposal doc, or to cross it with another doc."
---

# Research or proposal review

The output is a list of comments, each anchored on literal text of the doc, ordered by
severity. Every fact a comment states was checked in code, infrastructure or data. The rules
a doc must follow live in the `research-proposal` skill and in the skills of the code it
describes; this skill reads the doc against them and adds the questions that only exist
when reviewing.

## Inputs

- The doc to review, with its Implementation details tab and tasks when it has them.
- Optionally, one or more docs the author or the user trusts more than the doc under review.
  [references/sources.md](references/sources.md) says how they weigh.
- The profile of the `research-proposal` skill (`../research-proposal/profile.md`): company,
  provider, where to verify, how the author works. Compare it with the repository as that
  skill does, and report any disagreement.

Read code, infrastructure and metrics on your own to confirm a claim; do not ask first. Ask
only when a decision belongs to the author.

## How to work

[references/process.md](references/process.md): understand the doc, pick the checks, verify,
deliver, and how another skill is used from here.
[references/comment-style.md](references/comment-style.md): how each comment reads.

## Checks

| When | Check |
|---|---|
| Always | The references of `research-proposal`; [checks/consistency.md](checks/consistency.md) |
| The doc writes to a table, a queue, a bucket or an external service | [checks/failure-modes.md](checks/failure-modes.md), [checks/data-lifecycle.md](checks/data-lifecycle.md) |
| The doc changes something a client, a public API or another team sees | [checks/external-contracts.md](checks/external-contracts.md) |
| The doc launches by stages or behind a flag | [checks/rollout.md](checks/rollout.md) |
| The doc has an architecture diagram | The `architecture-diagram` skill |
| The doc introduces something that varies: providers, channels, formats, sources | The `design-pattern-decision` skill |
| The doc or its tab holds code, signatures, operations or infrastructure resources | The skill of that code: `go`, `typescript`, `html-css`, `terraform` |

`checks/` holds the questions that only exist when reviewing a doc, one file each with when
it applies, what to look for, how to confirm it, its severity and an example. A new question
is a new file and one row here.

## Done

Every comment anchors on text that exists in the doc; every fact in a comment was verified
or is marked as not verified; the reply lists the comments by severity, in the format of
[templates/comment.md](templates/comment.md), and says which ones can be dropped.
