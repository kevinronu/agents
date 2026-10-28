# Verification

Every statement in the doc is checked before it is written. The concrete places are in the
"Where to verify" table of [profile.md](../profile.md); this is what each kind of claim needs.

| Claim | Source |
|---|---|
| Who calls what, with which operation, in which order | The code |
| Triggers, filters, retries, dead-letter queues, regions | The infrastructure code |
| How much, how often, how many | The metrics source, with the query kept in the Appendix so anyone can run it |
| What a ticket decided, and when | The ticket tracker |
| Limits of a provider service | The provider's docs, linked |

## Follow the data end to end

For every field or record the design adds or reads: who writes it, who rewrites it later,
and who reads it. A value that reaches a table "by accident" can still be the one the
design depends on; a later rewrite can drop it without any error.

## Numbers

A number in the doc comes from a documented quota, a verified setting or a measurement. A
measurement keeps its date, its window and its filters, and its query in the Appendix. An
estimate says it is one.

## What is not verified

Mark it as pending, with the test that is missing: `[Pending: test in staging]` and one
line on what the test does. Never write a guess as a fact. The reply that delivers the doc
lists every pending item.
