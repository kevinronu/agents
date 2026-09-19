---
name: go-pattern-adapter
description: "Go Adapter skeleton and implementation notes. Use when the classifier recommends adapter or the user asks to implement, scaffold, or inspect this pattern in Go."
---

# Go Pattern Skeleton: Adapter

## Purpose

Provide a file-by-file Go skeleton for Adapter.

## Non-Obvious Go Notes

- Keep the interface the client expects in a small `target` package so the rest of the code depends on that contract, not on vendor or legacy APIs.
- Keep the client in its own `client` package. This makes the roles explicit: `target` defines the expected shape, while `client` consumes only that shape.
- Let backends that already match the target implement it directly. Only incompatible backends need adapters.
- Keep the adapter focused on translation: input shape, output shape, units, names, and error mapping. Do not move business policy into the adapter.
- If the adaptee is not yours to change, model it in a separate package so the adapter boundary stays explicit.
- Prefer one adapter per incompatible backend or protocol instead of one large adapter that branches on many backend shapes.

Read [the folder shape and file-by-file skeleton](references/skeleton.md) when implementing, scaffolding, or inspecting this pattern.
