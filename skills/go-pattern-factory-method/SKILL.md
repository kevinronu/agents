---
name: go-pattern-factory-method
description: "Go Factory Method skeleton and implementation notes. Use when the classifier recommends factory-method or the user asks to implement, scaffold, or inspect this pattern in Go."
---

# Go Pattern Skeleton: Factory Method

## Purpose

Provide a file-by-file Go skeleton for Factory Method.

## Non-Obvious Go Notes

- Keep the shared product type beside the shared product interface in `product/product.go`. This lets concrete products, the selector, and callers use one shared type without duplicating identifiers or forcing circular package relationships.
- In a minimal Go implementation, a concrete product file can own both its type constant and its concrete struct.
- The selector should return the abstract factory interface, not a concrete factory type.
- When concrete factories hold no state, they can be zero-value structs returned by value from the selector.
- A helper like `OneTimeAction` is the Go substitute for a method that would already be implemented in an abstract creator or abstract base class in other languages.
- The factory method can receive constructor data, such as `owner`, `name`, `config`, or another small input set, and each concrete factory can inject its own concrete type while preserving the shared contract.

Read [the folder shape and file-by-file skeleton](references/skeleton.md) when implementing, scaffolding, or inspecting this pattern.
