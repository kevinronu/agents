# Rollout

## When it applies

The doc launches by stages, by client, behind a flag, with a pilot, a dry run or a kill
switch.

## What to look for

- **A dry run that cannot measure what it claims.** "Write nothing" and "compare both paths"
  cannot both hold when the second path needs something written first.
- **A kill switch that does not stop the damage.** Turning the flag off stops new work; what
  already changed stays. The doc says what happens to it.
- **A pilot that cannot reach its metric.** The pilot client has too few events in the
  window, or the success metric needs data the pilot does not produce.
- **An order that connects before it exists.** A sender turned on before its receiver is
  deployed, a filter that needs a field the old records do not have, a step that waits a
  day for the new field and the doc does not say so.
- **Who does what.** Each manual step in Launch names who runs it and what they need to know
  before: support, legal, the client.

## How to confirm

The configuration the doc names (flags, allow-lists, their defaults); the volumes of the
pilot client from data; the deploy order against the order of the tasks.

## Severity

A dry run or pilot that cannot answer the question it exists for: grave, because the
go/no-go decision has no basis. A missing step owner: a line in Launch, can be dropped.

## Example

> To get the new score, the user vector must already exist. But the Configuration says dry
> run will "write nothing", so it never creates the user vector. In dry run we can only get
> today's score, not the new one.
