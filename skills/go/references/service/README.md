# Services

A service is one entry point deployed as a managed function: a Lambda on AWS, see
[providers.md](providers.md) for the other providers. This document gives the shape every
service follows and the reason behind each rule. The rules name mechanisms, not libraries;
[Names in scrap-services](#names-in-scrap-services) maps each mechanism to that repo, and the
canonical example is `digital-identity/whatsapp/functions/repair-client-inbound-flows` there.
Read it before writing a new service.

## Shape

The entry point does four things, in this order: it puts the logger in the context, builds
the processor from the event, runs it, and decides what to return.

```go
// scrap-services
func main() {
	defaultLogger.Must(context.Background(), cache.InitFromEnv(), logger.ThreeMonths)
	lambda.Start(handler)
}

func handler(ctx context.Context, input models.<Service>Input) (*models.<Service>Output, error) {
	ctxWithLogger := logger.Set(ctx, defaultLogger)

	p, err := createProcessor(ctxWithLogger, input)
	defer p.finish(ctxWithLogger)

	if err != nil {
		return nil, retryableOrNil(err)
	}

	output, err := p.process(ctxWithLogger)
	if err != nil {
		return nil, retryableOrNil(err)
	}

	return output, nil
}
```

- `main` initializes dependencies and fails fast when one cannot be created. The platform
  discards the container and starts a fresh one, so the handler holds no retry code and no
  mutable package state.
- The handler sets the logger in the context once. The return policy depends on the event
  source: [event-sources/](event-sources/).
- `createProcessor` validates and resolves the input and builds the collaborators. It always
  returns a processor, so `finish` closes the execution even on a rejection.
- `process(ctx)` receives only the context and returns the output.
- `finish` closes the execution with the start time, the recorded error and the recovered
  panic. `defer` must call it directly: inside a closure the panic recovery returns nil and
  panics go unlogged.

## Contracts in a shared package

The input and the output are types of the service's shared models package, one file each:
`<service>_input.go` and `<service>_output.go`. Another service invokes this one, or reads its
result, by importing them instead of copying structs. Validation, defaults such as
`IsDryRun`, and the loggable representation are part of the contract and live there too.
Validation errors are exported, non-retryable values in the same file.

## The processor

```go
type processor struct {
	repairer repairStrategy
	cursor   scanCursor

	startTime time.Time
	err       error
}
```

- It holds what the work consumes, named by the domain (`filters`, `cursor`, `policy`), never
  by the transport (`queryParams`, `body`, `record`).
- Fields a step reads together form a value object with a constructor that reads the
  transport, applies defaults and validates (`newScanCursor(input)`). When the transport
  changes, only that constructor changes.
- Policies on how each item is handled (`dryRun`, `maxItems`) belong to the collaborator that
  handles the item, not to the processor.
- `startTime` and `err` come last, after a blank line. The literal in `createProcessor`
  follows the field order.
- Its loggable representation composes what its fields expose, so `processor_created` shows
  the resolved state without a second copy of the input.

## Functions over methods

Prefer a plain function. Write a method only when the receiver's state is what the function
works on (`process`, `finish`, `processPage`) or an interface requires it. A helper that only
needs its arguments stays a function (`overwriteItem`, `withDeadlineOffset`, `tally`): the
reader sees every input in the signature instead of looking for hidden state.

## Errors

Every error carries whether it is retryable. There are three cases, decided where the error
is produced:

| Case | Log of the step | `p.err` | Returned |
|---|---|---|---|
| Transient failure: a store or a client failed | error | set, where it is logged | yes, so the platform retries |
| Permanent failure: bug, corrupted data, bad config | error | set, where it is logged | no |
| Rejection: invalid input, nothing to do | warning | untouched | no |

- `p.err` marks the execution as failed; that is what an error alarm counts. Set it only for
  failures, in the same place that logs them. A failure that forgets `p.err` closes the
  execution as `info` and no alarm sees it.
- The handler never inspects concrete errors. It only applies the return policy of its event
  source.

## Logs

- The logger travels in the context: the handler sets it once and every function reads it
  from there. No function takes it from a package variable or a field.
- Event names end in a past participle: `processor_created`, `repair_performed`,
  `fetch_waba_line_failed`, `repair_item_changed_skipped`.
- `processor_created` logs the input and the processor once the processor is complete. Its
  presence means creation succeeded; there is no `*_started` event.
- Between creation and `finish`, log only the relevant steps and what went wrong.
- `process` logs its output with `defer` in its own event (`<work>_performed`), so a run that
  stops halfway still records its progress. `finish` does not log the output.
- Retention by severity: errors three months; success and expected skips one month; a
  caller's mistake in the input one week.

## Order

The reading order of `~/.agents/AGENTS.md` applies: the entry point first, the processor and
its methods in execution order, then helpers and types by first use, each type below its
first user. Tests follow the order of the code they prove: the happy path first, then each
branch, helpers last.

## Changing an existing service

Every rule above applies to what you add or touch; leave the rest alone, and do not
restructure the whole service to match the skeleton unless that is the task. The slips to
watch in old code: a logger read from a package variable or a field, an error without its
retryability, a failure that does not set `p.err`, and a new field added to a local struct
instead of the shared contract.

## Done

The package tests and the linter pass, and a happy-path run logs `processor_created`,
`<work>_performed` and the execution close at `info`.

## Keeping this reference current

This reference grows with each service. While working:

- When the task needs a decision this reference does not cover, or the user chooses something
  it contradicts, finish the task and then ask whether to add or change the rule here. Do not
  edit the reference silently, and do not add a rule the user has not confirmed.
- Before adding a rule, check that it is not already stated in [SKILL.md](../../SKILL.md),
  in `~/.agents/AGENTS.md` or in this folder. State each rule once, in the most general
  place it applies; this folder keeps only what is specific to services.
- A new rule that contradicts an existing one is raised, not added. The user decides which
  one stays, and the other is removed in the same change.
- After any edit, read this folder end to end and remove what became redundant, duplicated
  or contradictory, including an example that no longer matches the canonical service.

## Names in scrap-services

| Mechanism | scrap-services |
|---|---|
| Logger in the context | `logger.Set(ctx, defaultLogger)` and `logger.Get(ctx)` |
| Fail-fast init | `defaultLogger.Must(ctx, err, retention)` |
| Retryability mark | `shared/retryableerror`: `WrapError`, `NewNonRetryableError`, `IsErrorRetryable` |
| Execution close | `logger.Get(ctx).LogLambdaExecution(ctx, p.startTime, p.err, recover(), objects...)` |
| Loggable representation | `logger.Object`: `LogName` and `LogProperties` |
| Retention | `logger.OneWeek`, `logger.OneMonth`, `logger.ThreeMonths` |
| Shared contracts package | the service's `shared/models` package |
| Linter | `golangci-lint run` on the package |
