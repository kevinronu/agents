# Failure modes

## When it applies

The doc writes to a table, a queue, a bucket or an external service, or changes something
and later wants to go back.

## What to look for

For each external write, in order: what is left if it fails halfway, what a retry does, and
what the go-back path finds.

- **Partial results.** A batch call that accepts some items and rejects others
  (`Unsuccessful*`, `UnprocessedItems`, `UnsuccessfulFaceAssociations`); the doc covers only
  "all fail".
- **Order of side effects.** A step that others depend on runs before its condition holds (a
  resource used before it is active, a switch written before the thing it points to exists).
- **Rollback that does not restore.** The go-back path assumes something that an earlier step
  already deleted or moved, so the account, record or user ends up with less than before.
- **Provider behavior the docs do not state.** The design relies on how a service behaves in
  a case its documentation does not describe (what a call does on an empty target, what a
  threshold means with one reference). That needs a test, not an assumption.
- **Retries that duplicate.** A retry without a fixed key or a check creates a second copy.

## How to confirm

The code of each call and the consumers that run after it (stream handlers, cleanup jobs);
the provider's API reference for what the call returns; the doc's own Failure Modes table
for what it already covers.

## Severity

A rollback that loses data, or a success path that depends on undocumented behavior: grave.
A missing partial-result case: grave if the partial case is the normal one, otherwise can be
dropped.

## Examples

> We need to test in staging what happens when we associate faces to an empty user vector,
> because AWS does not say whether AssociateFaces checks them when there is nothing to
> compare with.

> Before the rollback, delete-enrollment has already removed the face vectors of the older
> enrollments and moved their images. So the rollback brings the account back with only one
> face vector.
