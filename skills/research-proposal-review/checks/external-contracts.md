# External contracts

## When it applies

The doc changes something that a client, a public API, a dashboard or another team reads:
a response, a field, a record the client created, an id, an error code, a limit.

## What to look for

- A record the client created that the design marks deleted, moves or renames. If a read by
  id now returns not found, or a list shows fewer items, the client sees a change, even when
  the doc says it sees none.
- An id or a key that changes. A client that stored the old one cannot come back.
- A new error the client receives in a flow that used to pass (a router that stops creating
  validations, a 409 where there was a 200).
- A field removed or renamed in a response, a webhook or an event.
- A limit, a cost or a latency that moves, in either direction.

## How to confirm

The API handlers and the storage reads behind them: what a GET returns for the changed
record, what a list filters out. Compare with what the doc promises in the summary and in
Launch ("nothing changes for clients", "no notice needed").

## Severity

A change the doc says does not exist: grave, because the launch plan is built on it. A
change the doc names but does not tell the client about: a line in Launch, can be dropped.

## Example

> After the migration, the account has only one enrollment, as in the video-confirmed
> enrollment. The APIs are the same, but the older enrollments are deleted, so getting one of
> them by its id returns not found. We need to tell the clients before we enable it for them.
