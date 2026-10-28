---
name: go
description: "Implement, review, format, test, or lint Go code with package-scoped checks."
---

# Go

## Purpose

Apply these rules when implementing or reviewing Go code. Derive validation scope before running checks.

## Change Scope

Derive validation, testing, and analysis scope from the current change set before running quality commands.

1. Identify changed files using the `Validation Scope` section in [AGENTS.md](../../AGENTS.md).
2. Map each modified `*.go` file to its owning package directory.
3. Resolve each package with `go list` from the package directory.
4. Treat packages under `shared/` or `shared-services/` as shared ownership and include direct dependents.
5. Escalate scope when a change affects exported APIs, shared or reused units, cross-boundary contracts, or linked functional/contract tests.

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

## Architecture

- Respect clean architecture boundaries.
- For existing code, request confirmation before introducing or changing a design pattern outside the authorized task.
- Define small interfaces at the point of use.
- Avoid `init()` unless runtime constraints require it.

## Design Patterns

Invoke `design-pattern-decision` when choosing or changing an abstraction to address recurring complexity, or when explicitly asked to select a pattern. Simple fixes and direct implementations do not require classification.

When invoking it, read and use the [input contract](../design-pattern-decision/references/input-contract.md).

Set `Language` to `go`.

Continue based on `Recommended pattern`:

- `none`: continue with this Go skill only.
- any other pattern: read `references/patterns/<recommended-pattern>.md` and treat it as a skeleton for the plan, tentative code, current code, or intended change. Adapt it to the task; do not copy structure the task does not need. If no file exists for the pattern, apply it using general Go knowledge. Then continue in this Go skill for implementation rules, tests, formatting, and validation.

Do not invoke `design-pattern-decision` again after reading a pattern skeleton unless the plan, tentative code, or current code summary materially changes.

## Generics

- Use a type parameter when the same logic serves several types and the caller's own types must be checked at compile time. Do not use one for a single type, or where an interface already expresses the behavior.
- Put a type parameter on the narrowest declaration that needs it. A method may declare its own type parameters; put one on the type only when its fields or most of its methods use it.
- Name a type parameter by its scope and meaning. Use a conventional letter for a short scope and a known shape (`T`; `K`, `V`; `S ~[]E`; `M ~map[K]V`). Use a descriptive noun when the parameter spans a type's fields and methods, when several parameters share a constraint, or when no letter convention fits. Never reuse the name of another identifier in the package.
- Let callers rely on type inference. When a type parameter appears only in the result or in no argument, callers must pass it explicitly; prefer that over a placeholder type inside the generic code.

## Concurrency

- Pass `context.Context` as the first parameter for cancellable or long-running work.
- Do not store `context.Context` in structs except for rare, clearly documented exceptions.
- Do not accept `context.Context` in constructors unless construction itself performs cancellable work.
- Treat cancellation, deadlines, and request-scoped metadata as caller-owned per call.
- Avoid unbounded goroutines.

## Errors

- Return explicit, contextual errors.
- Wrap underlying errors with `%w` when preserving cause matters.
- Do not swallow errors, assign meaningful errors to `_`, or hide errors with comments.

## Exported Identifiers

- Document an exported identifier when its contract is not already clear from its name and signature. Leave it undocumented when a comment could only repeat them.
- Add a package comment when the package boundary is not obvious from its name.
- Never change the code to avoid writing a comment. Exporting, naming, and structure answer to the design, not to a linter.

Open with the identifier name and the shortest true sentence about what it yields, never with the failure case. That opening is the summary `go doc` lists, and it stands alone when nothing below applies. Then add, folding it into the opening sentence when it fits:

1. What can bite the caller: panics, zero-value behavior, nil results, concurrency safety, aliasing, cost, or an invariant worth stating. `strings.Builder.Grow` documents `If n is negative, Grow panics`, and `strings.Builder.Len` documents `b.Len() == len(b.String())`.
2. The specification that defines the behavior, when the authority is outside this code. `base64.StdEncoding` documents `as defined in RFC 4648`.

## Function and Method Names

Classify every new or renamed function or method before naming it. The first row that matches decides.

| Kind | Test | Name |
| :---- | :---- | :---- |
| Constructor | Returns a new value of a type in its package | `New` or `New<Type>` |
| Predicate | Returns only a `bool` | `Is…`, `Has…`, `Can…` |
| Accessor | A method that only reads its receiver, at most looking it up by its arguments: no side effects, cannot fail, cheap | A noun, never `Get…` (`Counts`, not `GetCounts`) |
| Mutator | A method that sets one field of its receiver | `Set<Field>`; the asymmetry with the accessor is intentional in Go |
| Everything else | Builds, converts, derives from its arguments, validates, can fail, blocks, or has side effects | A verb or verb phrase (`CollectReasons`, `Validate`, `Fetch`) |

- A package-level function is never an accessor, even when the standard library names one with a noun (`reflect.TypeOf`, `maps.Keys`).
- Name the accessor for a process-wide shared value after what it returns, such as `Shared` or `Default`. Prefer an exported variable when the value needs no lazy or fallible setup.

## Packages

- Use short, lowercase package names.
- Do not use underscores or hyphens in package names.

## Validation Methods

- Make each `Validate()` method validate only fields owned by its struct.
- Use pointer receivers when the struct is optional or may be `nil`, such as API boundary or decoded request structs.
- Use value receivers for required value objects that validate their own invariants.
- Make pointer receiver `Validate()` methods handle `nil` explicitly.
- Do not duplicate presence checks across layers; validate data at the layer that owns it.
- Parse enum-like input once, at the boundary that reads the request, into a typed value built by a single constructor. Pass only the typed value inward; do not re-validate or re-normalize it downstream.
- Match enum-like input exactly against its canonical spelling. Do not trim or case-fold it to make it match; reject anything else.
- The rejection names the parameter and the accepted values, or where they are documented when the set is large. It does not echo the received value; log that instead.
- When a contract requires normalization, such as Unicode NFC, do it inside that constructor before validating, and document it as part of the contract.

## Formatting Verbs

- Use explicit formatting verbs based on intent, such as `%q`, `%s`, `%d`, or `%#v`.
- Avoid generic/default formatting when precision matters.

```go
quoted := fmt.Sprintf("value=%q", value)
raw := fmt.Sprintf("value=%s", value)
```

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
- When a test changes shared state (package-level vars, mock flags, logger output), capture the original value first, change it, then restore that exact value in `t.Cleanup` right after the change. Restore only what the test changed; do not reset the whole mock or assign a hardcoded value.

```go
originalValue := pkg.SharedValue
pkg.SharedValue = testValue

t.Cleanup(func() {
	pkg.SharedValue = originalValue
})
```
- Make reusable test helpers call `t.Helper()`.
- Use `t.Parallel()` only when isolation is safe.
- Do not call `t.Parallel()` in tests that mutate package-level vars, logger output, shared mocks, or other shared mutable globals.
- Do not call `t.Parallel()` on parent tests that exist only as `t.Run` containers.
- Never combine parent and child parallelization in a subtest hierarchy.
- Avoid `time.Now()` in tests; use fixed timestamps.
- Avoid global state in tests.

## Benchmarks

- Ensure each changed package has at least one benchmark; if one already exists, the minimum is satisfied and no additional benchmark is required solely to meet it.
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

## Execution Contract

For implementation, complete these checks in order:

0. List every identifier the change adds or renames, exported or not, and check each against "Function and Method Names" and the Names section of `~/.claude/CLAUDE.md`. Rename before formatting.
1. Format changed Go files in the derived scope with `gofmt -w <files>`.
2. Format changed Go files in the derived scope with `goimports -w <files>`.
3. Run `go test` only for scoped packages.
4. Run `golangci-lint run` only for scoped packages.

## Required Closeout

When finishing a Go task, report:

- Files created or updated.
- Scoped packages validated.
- Commands run and outcomes.
- Any assumptions or skipped validation with the reason.
