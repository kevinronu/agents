---
name: go-pattern-builder
description: "Lightweight Go Builder file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: builder`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Builder in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Builder

## Purpose

Provide a file-by-file Go skeleton for Builder.

## Non-Obvious Go Notes

- Keep the shared `Builder` interface, selector type, and shared validation helper together in `builder/builder.go`. This gives callers and concrete builders one common contract without scattering the construction rules.
- Make chainable step methods return the shared `Builder` interface so concrete builders stay interchangeable at call sites.
- Use pointer receivers for concrete builders so they can accumulate state across steps.
- Let `Build` validate required parts and return the shared `product.Product`. Keep clearing accumulated state in `Reset`, called by whoever starts the next product, so `Build` does not silently discard the state a caller may still read.
- Keep `Director` as an optional layer for fixed recipes. It is useful when multiple construction sequences should stay reusable, but callers can still drive the builder directly when no recipe abstraction is needed.
- If one part depends on another, keep that dependency creation in the recipe or caller, not hidden inside unrelated builder steps.
- If an optional part depends on a required one, a small constructor helper can make that dependency explicit before the part enters the builder chain.

Read [the folder shape and file-by-file skeleton](references/skeleton.md) when implementing, scaffolding, or inspecting this pattern.
