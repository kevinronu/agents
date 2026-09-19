---
name: go-pattern-singleton
description: "Go Singleton skeleton and implementation notes. Use when the classifier recommends singleton or the user asks to implement, scaffold, or inspect this pattern in Go."
---

# Go Pattern Skeleton: Singleton

## Purpose

Provide a file-by-file Go skeleton for Singleton.

## Non-Obvious Go Notes

- Keep the shared holder and the exported accessor in the same small package so callers cannot construct competing instances accidentally.
- Return the shared instance through an accessor like `Default(...)` instead of exposing a package variable directly. This keeps lazy initialization, locking, and setup errors behind one stable entry point.
- Use a pointer return when callers must share one identity.
- If one-time setup can fail or depends on `context.Context`, prefer an explicit locking flow over `sync.Once`, so the accessor can return an error and retry later if initialization did not complete.
- Use a fast path for already-created reads and a guarded slow path for first creation when concurrent access matters.
- Keep the one-time build logic in a private helper so expensive setup stays isolated from the concurrency control.

Read [the folder shape and file-by-file skeleton](references/skeleton.md) when implementing, scaffolding, or inspecting this pattern.
