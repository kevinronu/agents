# Verification

Every statement in the doc is checked before it is written. The places to check:

| Claim | Where |
|---|---|
| Who calls what, with which operation, in which order | The Go code: the lambda's `main.go`, the storage package, the models |
| Triggers, filters, retries, DLQs, regions | Terraform under `terraform/deploy/envs/cloud-arch/` |
| How much, how often, how many | Lens (the `lens-api` skill), with the query kept in the Appendix so anyone can run it |
| What a ticket decided, and when | Jira |
| Limits of an AWS service | The AWS docs, linked |

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
