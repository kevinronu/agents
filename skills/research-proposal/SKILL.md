---
name: research-proposal
description: "Write or update a research or proposal doc (the design doc, its Implementation details tab and its tasks CSV). Use when asked to write, cut, restructure or re-estimate one, or to check it after a design change."
---

# Research or proposal

A research or proposal is read by PMs and engineers who do not know the product. Every claim
in it was checked at the sources [profile.md](profile.md) names, and every section says one
thing once, from the general to the particular.

## Profile

[profile.md](profile.md) holds what changes from one company or team to another: the header
fields, the cloud provider, where each kind of claim is verified, what already exists, and
how the author likes to work. Edit it when you adopt the skill.

Before writing, compare the profile with the repository: the provider and the infrastructure
tool against the directories and config files, the author against `git config user.name`,
the verification places against what exists. When they disagree, say so in the reply and ask
which one is right; do not change the profile on your own.

## What to read

| When | Read |
|---|---|
| Starting a doc, or unsure which kind it is | [references/document-shape.md](references/document-shape.md): research vs proposal, header, sections, size, the deliverables |
| Choosing or naming a service, a store, a queue or an operation | [references/providers.md](references/providers.md): one neutral term per role, the provider's default, and when its alternative applies |
| Writing or rewriting any section | [references/writing-rules.md](references/writing-rules.md): language, names, order, and what each section holds |
| Before stating a fact, a number, a call or a name | [references/verification.md](references/verification.md) |
| Writing or changing Tasks & Estimation or the CSV | [references/tasks.md](references/tasks.md) |
| Writing the Implementation details tab | [references/implementation-details.md](references/implementation-details.md): sections, the fields of each service, what goes there and not in the doc |
| After any design change, before answering | [references/change-checklist.md](references/change-checklist.md) |

Templates: [templates/proposal.md](templates/proposal.md) for a new doc,
[templates/implementation.md](templates/implementation.md) for its tab and
[templates/tasks.csv](templates/tasks.csv) for the tasks file. The architecture diagram comes
from the `architecture-diagram` skill; its PNG goes in the Architecture section.

Read code, infrastructure and metrics on your own to verify a claim. Ask only when the
profile and the repository disagree, or when the decision belongs to the author.

## Done

The doc, the Implementation details tab and the CSV agree with each other and with the
diagram; the body up to "Stop reading here" fits the size limit; the change checklist passed;
and the reply names every claim that is still unverified.
