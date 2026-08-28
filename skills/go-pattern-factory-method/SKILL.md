---
name: go-pattern-factory-method
description: "Lightweight Go Factory Method file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: factory-method`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Factory Method in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
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

## Folder Shape

```text
<pattern-root>/
├── main.go
├── factory/
│   ├── factory.go
│   ├── factory_<type-one>.go
│   └── factory_<type-two>.go
└── product/
    ├── product.go
    ├── product_<type-one>.go
    └── product_<type-two>.go
```

## File-By-File Skeleton

### `product/product.go`

```go
// Package product defines the contract and the type identifier every product shares.
package product

// Type identifies a concrete product.
type Type string

// Product is the common contract for every concrete product.
type Product interface {
	Type() Type
	DoSomething() string
}
```

### `product/product_<type>.go`

```go
package product

import "fmt"

// <productTypeName> identifies one concrete product type.
const <productTypeName> Type = "<type>"

// <productName> is one concrete product: its type is fixed and only its owner varies.
type <productName> struct {
	Owner string
}

// Type is fixed per concrete product, so it never depends on how the product was built.
func (p <productName>) Type() Type {
	return <productTypeName>
}

func (p <productName>) DoSomething() string {
	return fmt.Sprintf(
		"product of type %s owned by %s is doing something",
		<productTypeName>,
		p.Owner,
	)
}
```

### `factory/factory.go`

```go
// Package factory picks which concrete product a caller gets.
package factory

import (
	"fmt"

	"<module>/<pattern-root>/product"
)

// Factory creates one product through the shared factory method.
type Factory interface {
	CreateProduct(owner string) product.Product
}

// OneTimeAction is what an abstract base class would implement in other languages.
func OneTimeAction(factory Factory, temporaryOwner string) string {
	created := factory.CreateProduct(temporaryOwner)

	return created.DoSomething()
}

func New(productType product.Type) (Factory, error) {
	switch productType {
	case product.<firstProductTypeName>:
		return <firstFactoryName>{}, nil
	case product.<secondProductTypeName>:
		return <secondFactoryName>{}, nil
	default:
		return nil, fmt.Errorf("unsupported product type: %q", productType)
	}
}
```

### `factory/factory_<type>.go`

```go
package factory

import "<module>/<pattern-root>/product"

// <factoryName> creates one concrete product type.
type <factoryName> struct{}

// CreateProduct injects the caller's data into this factory's own concrete type.
func (f <factoryName>) CreateProduct(owner string) product.Product {
	return product.<productName>{Owner: owner}
}
```

Use one file like the template above per concrete product type, replacing placeholders such as `<factoryName>`, `<productName>`, and `<productTypeName>` with names that match the chosen product type.

### `main.go`

```go
package main

import (
	"fmt"
	"log"

	"<module>/<pattern-root>/factory"
	"<module>/<pattern-root>/product"
)

func printDetails(p product.Product) {
	fmt.Printf("Type: %s\n", p.Type())
	fmt.Printf("Action: %s\n", p.DoSomething())
}

func main() {
	typeOne := product.<firstProductTypeName>
	factoryOne, err := factory.New(typeOne)
	if err != nil {
		log.Fatalf("get factory one: %v", err)
	}

	typeTwo := product.<secondProductTypeName>
	factoryTwo, err := factory.New(typeTwo)
	if err != nil {
		log.Fatalf("get factory two: %v", err)
	}

	productOne := factoryOne.CreateProduct("Alice")
	productTwo := factoryTwo.CreateProduct("Bob")

	printDetails(productOne)
	printDetails(productTwo)

	fmt.Println(factory.OneTimeAction(factoryOne, "Carol"))
	fmt.Println(factory.OneTimeAction(factoryTwo, "Dave"))
}
```
