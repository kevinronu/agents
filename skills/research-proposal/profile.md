# Profile

What changes from one company or team to another. Edit it when you adopt the skill. The
skill compares it with the repository before writing and reports any disagreement.

## Company

- Company: Truora
- Cloud provider: AWS. The doc uses its names, from [references/providers.md](references/providers.md).
- Fixed choices, over the defaults of that table: Service is Lambda.
- Infrastructure as code: Terraform, under `terraform/deploy/envs/cloud-arch/`.
- Code: Go. A Lambda has its `main.go`; storage packages live under `storage/`.

## Header

One line each, with a blank line between them. Date and Parent Proposal change from doc to doc; leave the Parent Proposal line out when there is no parent.

```
Date: <the day the doc is written>
PM: Juan Carlos Giraldo
Tech Owner: Kevin Robles
Parent Proposal: <link to the parent doc, only when there is one>
Team: Spica
Time to read: ⌛30:00
Time to discuss: ⌛15:00
```

## Where to verify

| Kind of claim | Where |
|---|---|
| Code: who calls what, which operation, in which order | The service's `main.go`, the storage package, the models |
| Infrastructure: triggers, filters, retries, dead-letter queues, regions | The Terraform directory above |
| Numbers: how much, how often, how many | Lens, through the `lens-api` skill |
| Decisions: what a ticket decided, and when | Jira |

## What already exists

Reusing it adds no work to a task:

- The DynamoDB mock (minidyn) and the S3 mock.

## Estimation

- One story point is one day of work.

## How to work with the author

- Propose before changing when the decision is his: a design choice, what to cut, how to
  split a task. Apply directly when it is a rule in the references.
- Give options with one recommendation, not a neutral list. Answer in Spanish, short.
- Save a lesson in the skill only when he asks. Read the whole file first, merge or replace
  the rule that exists; never add on top. Rules, not history: no "now", "before", dates.
