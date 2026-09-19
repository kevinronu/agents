---
name: go-pattern-chain-of-responsibility
description: "Lightweight Go Chain of Responsibility file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: chain-of-responsibility`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Chain of Responsibility in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Chain Of Responsibility

## Purpose

Provide a file-by-file Go skeleton for Chain Of Responsibility.

## Non-Obvious Go Notes

- Put `Request`, `Handler`, and the reusable successor link in one `handler` package. Concrete steps can import that package without depending on one another.
- Embed `Successor` in each concrete handler. It replaces the next-link behavior that an abstract base class often provides in other languages; a step calls `Successor.Handle` only after its own check succeeds.
- Let `SetNext` return the handler passed to it, so `head.SetNext(second).SetNext(third)` reads naturally. Keep `head` separately: the return value is the next step, not the head.
- Treat a `nil` successor as successful completion. A final handler can delegate without knowing whether it is last.
- Build the chain where policy is configured, not inside a concrete step. Order is behavior: a rejection prevents every later handler from running.
- Let the protected server own one optional `handler.Handler`. `Serve` runs it before its own work, and a full chain fits in that single field.
- A rate limiter is mutable state. The GCRA version keeps a scheduled due time instead of a resetting counter, but a chain shared by goroutines still needs synchronization around that state.

Read [the folder shape and file-by-file skeleton](references/skeleton.md) when implementing, scaffolding, or inspecting this pattern.
