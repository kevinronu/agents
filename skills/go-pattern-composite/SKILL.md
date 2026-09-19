---
name: go-pattern-composite
description: "Lightweight Go Composite file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: composite`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Composite in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Composite

## Purpose

Provide a file-by-file Go skeleton for Composite.

## Non-Obvious Go Notes

- Put the shared `Component` contract in its own package so leaves and composites can import it without a circular dependency. The client needs only this contract.
- Keep child-management methods such as `Add` and `Remove` off `Component`: leaves have no children, while the composite owns tree mutation.
- Use pointer receivers for a mutable composite, then store `*Composite` behind `Component`. A parent must retain the same object when a nested composite changes.
- A stateless leaf can use value receivers and be stored by value; it still satisfies the same `Component` contract.
- Remove a child by a stable identifier, rather than comparing interface values with `==`. A concrete component containing a slice, map, or function is not comparable and can make that comparison panic.
- Let recursive operations delegate through `Component`. A composite should not need type switches to distinguish a leaf from another composite.

Read [the folder shape and file-by-file skeleton](references/skeleton.md) when implementing, scaffolding, or inspecting this pattern.
