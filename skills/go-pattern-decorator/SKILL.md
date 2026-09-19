---
name: go-pattern-decorator
description: "Lightweight Go Decorator file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: decorator`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Decorator in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Decorator

## Purpose

Provide a file-by-file Go skeleton for Decorator.

## Non-Obvious Go Notes

- Put the shared contract in a small `component` package so the concrete component and every wrapper can substitute for one another at the client boundary.
- Keep the wrapped component in a private named field such as `wrappee`; do not embed the interface. If the contract gains a method, named delegation makes incomplete decorators fail to compile instead of silently forwarding that method unchanged.
- Let each decorator implement every contract method explicitly. Transform data before delegation on `Write`, then reverse the transformation after delegation on `Read`.
- Wrapper order is observable: the outer decorator runs first on `Write` and last on `Read`. Construct the stack in the intended order and document it when operations do not commute.
- Use a pointer receiver for the concrete component when it owns mutable state. Stateless decorators or decorators whose fields are immutable after construction can use values.
- Return a constructor error only when configuration must be valid immediately. A codec level can fail on the first `Write`; a cipher key must fail while constructing the decorator.
- If a decorator derives working state from a secret, keep the derived value instead of the secret. For AEAD encryption, prepend the nonce to the ciphertext so `Read` can recover it.
- Propagate errors from the wrapped component unchanged unless the decorator can add useful local context; wrap errors created by its own transformation.

Read [the folder shape and file-by-file skeleton](references/skeleton.md) when implementing, scaffolding, or inspecting this pattern.
