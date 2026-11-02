# Direct invocation

A caller runs the service with its input contract and gets its output contract back.

## AWS
Checked: 2026-11-02
- Chosen: Lambda invoke, synchronous (`RequestResponse`) or asynchronous (`Event`).
- Tradeoffs:
  - On an asynchronous invoke the platform retries a returned error twice by default; on a
    synchronous one the caller gets the error and decides. Return only retryable errors; the
    policy is in the `go` skill, `references/service/event-sources/direct.md`.
- Configuration: in Go the handler takes the input struct and returns the output struct.

## GCP
Checked: never
- Chosen: HTTP request to the service

## Azure
Checked: never
- Chosen: HTTP trigger
