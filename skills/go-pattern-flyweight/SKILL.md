---
name: go-pattern-flyweight
description: "Lightweight Go Flyweight file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: flyweight`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Flyweight in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Flyweight

## Purpose

Provide a file-by-file Go skeleton for Flyweight.

## Non-Obvious Go Notes

- Put the shared flyweight and its factory in one package. Keep flyweight fields private so callers cannot create mutable, unshared copies outside the factory.
- Keep per-instance state in a separate `extrinsic` package. Do not name that package `context`: `context` already belongs to the standard library in Go.
- Store a pointer to the flyweight in each context object. The context stays small, while the pointer identity makes sharing explicit.
- Pass extrinsic values as method arguments rather than storing them in the flyweight. One shared value can then serve every position, request, or instance.
- Protect a shared factory cache with `sync.RWMutex`. On a miss, release `RLock`, acquire `Lock`, and check again: Go mutexes cannot upgrade a read lock, and another goroutine may have inserted the entry meanwhile.
- Keep only immutable intrinsic state in a flyweight after it enters the cache. Mutating it would change every context that shares the pointer.

Read [the folder shape and file-by-file skeleton](references/skeleton.md) when implementing, scaffolding, or inspecting this pattern.
