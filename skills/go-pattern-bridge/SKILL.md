---
name: go-pattern-bridge
description: "Lightweight Go Bridge file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: bridge`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Bridge in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Bridge

## Purpose

Provide a file-by-file Go skeleton for Bridge.

## Non-Obvious Go Notes

- Keep the implementation interface in its own package so refined abstractions depend on one shared low-level contract instead of concrete renderers or backends.
- Use embedding or composition in the abstraction side to hold the implementation. This is the Go substitute for carrying shared implementation state through an abstract base type.
- Bridge fits when both sides vary independently. If only one side varies, a simpler pattern is usually enough.
- Keep implementation methods small and composable so refined abstractions can assemble different outputs without learning format-specific details.
- Refined abstractions should differ mainly in the content or workflow they compose, not in how they talk to the implementation.

Read [the folder shape and file-by-file skeleton](references/skeleton.md) when implementing, scaffolding, or inspecting this pattern.
