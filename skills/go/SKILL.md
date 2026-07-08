---
name: go
description: Enforce strict guardrails for implementing and validating Go code changes. Use when Codex writes, modifies, reviews, tests, formats, scopes, or statically analyzes Go code, including deriving the affected Go package scope from changed files before running quality commands and orchestrating design-pattern classification when Go code may need pattern-level structure.
---

# Go

## Purpose

Act as a Go implementation guard. Apply these rules before and during every Go code change, then validate only the derived change scope unless escalation rules require a broader scope.

## Change Scope

Derive validation, testing, and analysis scope from the current change set before running quality commands.

1. Identify modified Go files with `git diff --name-only <base>...HEAD` or the equivalent base for the current task.
2. Map each modified `*.go` file to its owning package directory.
3. Resolve each package with `go list` from the package directory.
4. Treat packages under `shared/` or `shared-services/` as shared ownership and include direct dependents.
5. Escalate scope when a change affects exported APIs, shared or reused units, cross-boundary contracts, or linked functional/contract tests.
6. Escalate to full repository scope only when the change invalidates global assumptions or the user explicitly requests full-repo validation.

Report the scoped packages, any escalations, and assumptions when scope is non-obvious.

## Code Constraints

- Keep changes minimal and focused.
- Prefer value receivers and value parameters by default.
- Use pointers only when needed for mutation, nil semantics, shared identity, interface requirements, to avoid expensive copies, or when explicitly requested by the user.

Bad:

```go
func (m *Money) IsZero() bool { return m.Amount == 0 }
func HasSameCurrency(m *Money, other *Money) bool { return m.Currency == other.Currency }
```

Good:

```go
func (m Money) IsZero() bool { return m.Amount == 0 }
func HasSameCurrency(m Money, other Money) bool { return m.Currency == other.Currency }
```

Use pointer only when needed:

```go
func (c *Counter) Increment() { c.value++ }
```

- Do not refactor unrelated code.
- Do not introduce new dependencies unless explicitly requested.
- Preserve existing architecture and abstractions.
- Declare code in increasing order of abstraction: leaf logic before higher-level orchestration.

## Errors

- Return explicit, contextual errors.
- Wrap underlying errors with `%w` when preserving cause matters.
- Do not swallow errors, assign meaningful errors to `_`, or hide errors with comments.

## Exported Identifiers

- Add documentation comments for every exported identifier.

## Packages

- Use short, lowercase package names.
- Do not use underscores or hyphens in package names.

## Validation Methods

- Make each `Validate()` method validate only fields owned by its struct.
- Use pointer receivers when the struct is optional or may be `nil`, such as API boundary or decoded request structs.
- Use value receivers for required value objects that validate their own invariants.
- Make pointer receiver `Validate()` methods handle `nil` explicitly.
- Do not duplicate presence checks across layers; validate data at the layer that owns it.

## Formatting Verbs

- Use explicit formatting verbs based on intent, such as `%q`, `%s`, `%d`, or `%#v`.
- Avoid generic/default formatting when precision matters.

```go
quoted := fmt.Sprintf("value=%q", value)
raw := fmt.Sprintf("value=%s", value)
```

## Architecture

- Respect clean architecture boundaries.
- For existing code, request confirmation before introducing or changing a design pattern.
- Define small interfaces at the point of use.
- Avoid `init()` unless runtime constraints require it.

## Design Patterns

Before choosing the Go design, invoke `design-pattern-decision` with this input contract:

```text
User request:
Language:
Relevant files, package, module, or component:
Existing local conventions:
Plan, tentative code, or current code summary:
Abstractions being considered or already present:
Variation points:
Expected future cases:
Testing impact:
```

Set `Language` to `go`.

Continue based on `Recommended pattern`:

- `none`: continue with this Go skill only.
- any other pattern: use it to develop or adjust the plan, tentative code, current code, or intended change. If a matching `go-pattern-<recommended-pattern>` skill is available, invoke it and treat its result as a pattern skeleton. Otherwise, apply the pattern using general Go knowledge. Then continue in this Go skill for implementation rules, tests, formatting, and validation.

Do not invoke `design-pattern-decision` again after returning from a Go pattern skill unless the plan, tentative code, or current code summary materially changes.

## Concurrency

- Pass `context.Context` as the first parameter for cancellable or long-running work.
- Do not store `context.Context` in structs except for rare, clearly documented exceptions.
- Do not accept `context.Context` in constructors unless construction itself performs cancellable work.
- Treat cancellation, deadlines, and request-scoped metadata as caller-owned per call.
- Avoid unbounded goroutines.

## Tests

- Add or update tests when behavior changes.
- Use one top-level `Test...` function per unit, behavior, condition, or failure mode.
- Do not use table-driven scenario encoding with `[]struct`, maps, or equivalent case collections plus loops.
- Do not generate subtests via loops.
- Use `t.Run` only when shared setup cost is high and cannot be reasonably extracted; include a brief inline comment justifying the exception.
- Prefer names like `Test<Unit>_<Condition>_<ExpectedResult>`.
- Validate one logical condition or failure mode per test.
- Use a single assertion helper instance scoped to each test context.
- Always assert errors and relevant side effects.
- Isolate dependencies with mocks or fakes.
- Use `t.Context()` by default.
- Use `t.Cleanup` for teardown.
- Make reusable test helpers call `t.Helper()`.
- Use `t.Parallel()` only when isolation is safe.
- Do not call `t.Parallel()` in tests that mutate package-level vars, logger output, shared mocks, or other shared mutable globals.
- Do not call `t.Parallel()` on parent tests that exist only as `t.Run` containers.
- Never combine parent and child parallelization in a subtest hierarchy.
- Avoid `time.Now()` in tests; use fixed timestamps.
- Avoid global state in tests.

## Benchmarks

- Ensure each changed package has at least one benchmark.
- Benchmark a representative, performance-relevant operation when practical.
- Prepare deterministic inputs outside the timed loop.
- Call `b.ResetTimer()` before measured work.
- Prefer `for b.Loop()` for benchmark loops.
- Fail fast with benchmark-appropriate methods when benchmarked operations return unexpected errors.

```go
func BenchmarkProcess(b *testing.B) {
	input := []byte("example-input")
	p := NewProcessor()

	b.ResetTimer()
	for b.Loop() {
		if _, err := p.Process(input); err != nil {
			b.Fatalf("Process failed: %v", err)
		}
	}
}
```

## Anti-Patterns

Do not introduce:

- Table-driven unit test scenario loops.
- Loop-driven subtest generation.
- Parent and child parallel test execution.
- Unrelated refactors.
- New dependencies without explicit user approval.
- Hidden or ignored errors.
- Nonessential `init()` functions.

## Execution Contract

A Go-related task is complete only when all steps succeed in this order:

1. Format changed Go files in the derived scope with `gofmt -w <files>`.
2. Format changed Go files in the derived scope with `goimports -w <files>`.
3. Run `go test` only for scoped packages.
4. Run `golangci-lint run` only for scoped packages.

Do not run `go test ./...` or `golangci-lint run ./...` unless the user explicitly requests it or scope escalation reaches full-repository impact.

If any step fails, fix the issue and rerun the sequence from the appropriate failed step until the scoped validation succeeds or a blocker is clearly reported.

## Required Closeout

When finishing a Go task, report:

- Files created or updated.
- Scoped packages validated.
- Commands run and outcomes.
- Any assumptions or skipped validation with the reason.
