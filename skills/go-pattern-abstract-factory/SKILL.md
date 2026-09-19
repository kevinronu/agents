---
name: go-pattern-abstract-factory
description: "Go Abstract Factory skeleton and implementation notes. Use when the classifier recommends abstract-factory or the user asks to implement, scaffold, or inspect this pattern in Go."
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
