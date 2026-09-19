---
name: go-pattern-prototype
description: "Go Prototype skeleton and implementation notes. Use when the classifier recommends prototype or the user asks to implement, scaffold, or inspect this pattern in Go."
---

# Go Pattern Skeleton: Prototype

## Purpose

Provide a file-by-file Go skeleton for Prototype.

## Non-Obvious Go Notes

- Keep the shared `Prototype[T]` contract in its own small package when multiple concrete types clone themselves. This gives leaf and composite prototypes one common shape without forcing inheritance-style structure.
- Let each type clone only the state it owns directly. If a parent type must re-link back-references or repair relationships, do that in the parent's `Clone`, not in child clones.
- Use a value receiver for simple leaf values that copy cleanly by value. Use a pointer receiver when cloning a parent object that owns slices, nested references, or identity that should stay attached to the new instance.
- Be explicit about deep vs shallow copy behavior. Prototype is useful only when the clone boundary is unambiguous.
- If slices, maps, pointers, or nested prototypes are present, clone them intentionally so the result does not silently share mutable state with the original.

Read [the folder shape and file-by-file skeleton](references/skeleton.md) when implementing, scaffolding, or inspecting this pattern.
