---
name: go-pattern-abstract-factory
description: "Lightweight Go Abstract Factory file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: abstract-factory`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Abstract Factory in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Abstract Factory

## Purpose

Provide a file-by-file Go skeleton for Abstract Factory.

## Non-Obvious Go Notes

- Keep the shared family type beside the shared product interfaces in `product/product.go`. This lets products, family identifiers, and the selector use one shared type without duplicating identifiers or forcing circular package relationships.
- Keep each family identifier in `product/<family>/family.go`. Concrete products from that family return that identifier.
- The selector should return the abstract factory interface, not a concrete factory type.
- When concrete factories hold no state, they can be zero-value structs returned by value from the selector.
- A helper like `OneTimeAction` is the Go substitute for a method that would already be implemented in an abstract factory or abstract base class in other languages.
- Import aliases are useful when family packages would otherwise collide or become unclear at call sites.

Read [the folder shape and file-by-file skeleton](references/skeleton.md) when implementing, scaffolding, or inspecting this pattern.
