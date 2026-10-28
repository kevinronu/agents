# Data lifecycle

## When it applies

The doc adds, changes or reads a field, a record, a file or a message.

## What to look for

For each piece of data the design depends on: who writes it, who rewrites it later, who
reads it, and who deletes it. A link that is missing in that chain:

- A value read by a filter, a rollback or a query that nobody writes with that value.
- A field written to one table and read from another, with a step in between that rewrites
  the whole item and drops it.
- A record deleted by an existing consumer (a stream, a cleanup job) before the step that
  still needs it runs.
- An identifier the design uses to find something later (`legacy_collection_id`) that is
  not in the Data model.

## How to confirm

Follow the data in the code: the storage package for writes, every lambda or job that
touches the table for rewrites, the stream consumers for deletes. The rule is "Follow the
data end to end" in `../../research-proposal/references/verification.md`.

## Severity

A read with no writer, or a delete before a read: the feature does not work, grave. A field
missing from the Data model: the doc, not the design; can be dropped.

## Example

> `legacy_collection_id` is not in the Data model. Also, photo-only rows have no
> `collection_id`, so the similarity check uses the `account_id` as the face collection.
