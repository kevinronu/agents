# Service

Code that runs on demand as a managed function: the platform starts it on an event, scales
it and stops it. What starts it is in `terms/event-sources/`.

## AWS
Checked: 2026-11-02
- Chosen: Lambda
- Why: no server to run, scales per invocation, and the build, deploy and logging tooling of
  scrap-services target it.
- Alternative: ECS Fargate, when the work does not fit a function: it runs longer than 15
  minutes or keeps connections open.
- Tradeoffs:
  - A container may serve several invocations at once (Lambda Managed Instances), so package
    state that changes per invocation is a race. Initialize dependencies in `main` and keep
    the handler free of mutable package state.
  - A log written during init has no request id. It reaches CloudWatch; reaching the log
    pipeline through the logger extension was verified in the extension's code, not in a
    real run (open).
- Configuration:
  - Dependencies initialize in `main` and fail fast. A failed init discards the container
    and the platform starts a fresh one, so the handler holds no retry code.
  - The shape of the entry point and its return policy per event source are in the `go`
    skill, `references/service/`.

## GCP
Checked: never
- Chosen: Cloud Run service
- Alternative: Cloud Run job, when the work runs to completion with no request to answer

## Azure
Checked: never
- Chosen: Azure Function
- Alternative: Container App, when the work does not fit a function: long runs or open
  connections
