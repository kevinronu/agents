---
name: go-pattern-facade
description: "Go Facade skeleton and implementation notes. Use when the classifier recommends facade or the user asks to implement, scaffold, or inspect this pattern in Go."
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
