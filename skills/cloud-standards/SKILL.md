---
name: cloud-standards
description: "The managed building blocks we build with: the neutral term for each, what it means, the service chosen on each provider, when its alternative applies, and why. Use when naming, choosing, configuring or translating a service, store, cache, queue, topic, event source or operation."
---

# Cloud standards

## A term

One file per building block, `terms/<category>/<term>.md`. The file name is the neutral
term every skill and doc uses. The file says what the block is and, per provider, what we
use:

```md
# <Term>

<One sentence: what it is, with no provider's name.>

## AWS
Checked: <date>
- Chosen: <service>
- Why: <one line>
- Alternative: <service>, when <condition>
- Tradeoffs: <one per line, each with how it is handled; "open" when it is not>
- Configuration: <a decided setting and its reason, one per line>
```

The meaning, the provider heading, `Checked` and `Chosen` are required; the rest appears
when there is something to say. A provider the term was never used with has
`Checked: never`.

Categories: `compute`, `data`, `messaging`, `event-sources`, `security`, `observability`.
Find a term with `ls terms/<category>` and open only the one the task needs.

## Choosing

Use Chosen. Use the alternative only when its condition holds, or when the design extends
something that already uses it: one entity never lives in two stores. A doc says which
condition held. A choice fixed by the project, such as `Service is Lambda` in a profile,
wins over Chosen.

## Operations

An operation is named as the provider's SDK names it: `UpdateItem` or `CopyObject` on AWS,
the client library's method on GCP, the SDK operation on Azure.

## Keeping this skill current

- **A term is missing**, or a provider is missing in a term: do not invent it. Search the
  web for the current recommendation for that use, with an extended search because rankings
  change; present two or three options with one recommendation and the sources; write the
  file only after the user decides, with `Checked` set to that day.
- **On use**, when the provider's `Checked` is older than 30 days or the task touches
  something the file does not mention, search the web for what changed for that block and
  that use: limits, features, recommended configuration, deprecations. Bring what is new into
  the task and propose the file update when the task ends.
- **A finding on the way**, such as a tradeoff, the way around it or a configuration decided,
  is proposed when the task ends and written only when the user confirms.
- Every update replaces what it changes, dated and sourced; it never adds on top. Before
  adding, check the rule is not already in the file or in the skill that uses the term; a
  contradiction is raised, not added, and the user decides which one stays. After an edit,
  read the file end to end and remove what became redundant, duplicated or contradictory.

Adding a provider is a section in the terms it matters for. Another kind of standard, such
as regions, retention or sizing, is a folder next to `terms/`.
