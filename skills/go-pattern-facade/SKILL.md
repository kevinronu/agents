---
name: go-pattern-facade
description: "Lightweight Go Facade file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: facade`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Facade in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Facade

## Purpose

Provide a file-by-file Go skeleton for Facade.

## Non-Obvious Go Notes

- Keep the subsystem in its own package. The facade imports and orders its parts; subsystem types do not import the facade or know the whole workflow.
- Let the facade own stateless subsystem values directly. Zero-value structs need no constructor or dependency wiring when their behavior has no configuration.
- Put repeated prerequisite selection in a private helper returning one small result struct. This prevents public facade methods such as `Check` and `Convert` from drifting apart.
- Use a distinct intermediate type for a workflow stage when it prevents invalid call order. A decoded `Raw` value can flow through processing and encoding without allowing callers to encode an unprocessed file by mistake.
- A facade is a shortcut, not a wall: retain useful subsystem errors and leave direct subsystem access possible when callers genuinely need lower-level control.

Read [the folder shape and file-by-file skeleton](references/skeleton.md) when implementing, scaffolding, or inspecting this pattern.
