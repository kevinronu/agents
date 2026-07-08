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
package product

// ProductType identifies a concrete product.
type ProductType string

// Product is the common contract for every concrete product.
type Product interface {
	GetType() ProductType
	DoSomething() string
}
```

### `product/product_<type>.go`

```go
package product

import "fmt"

const (
	// <productTypeName> identifies one concrete product type.
	<productTypeName> ProductType = "<type>"
)

type <productName> struct {
	Owner string
	Type  ProductType
}

func (p <productName>) GetType() ProductType {
	return <productTypeName>
}

func (p <productName>) DoSomething() string {
	return fmt.Sprintf(
		"product of type %s owned by %s is doing something",
		p.Type,
		p.Owner,
	)
}
```

### `factory/factory.go`

```go
package factorymethod

import (
	"fmt"

	"<module>/<pattern-root>/product"
)

// Factory creates one product through the shared factory method.
type Factory interface {
	CreateProduct(owner string) product.Product
}

// OneTimeAction is an example of the shared operation that, in other languages,
// might already be implemented in an abstract creator or abstract base class.
func OneTimeAction(factory Factory, temporaryOwner string) string {
	product := factory.CreateProduct(temporaryOwner)

	return product.DoSomething()
}

// GetFactory returns the factory for the given product type.
func GetFactory(productType product.ProductType) (Factory, error) {
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
package factorymethod

import "<module>/<pattern-root>/product"

// <factoryName> creates one concrete product type.
type <factoryName> struct{}

func (f <factoryName>) CreateProduct(owner string) product.Product {
	return product.<productName>{
		Owner: owner,
		Type:  product.<productTypeName>,
	}
}
```

Use one file like the template above per concrete product type, replacing placeholders such as `<factoryName>`, `<productName>`, and `<productTypeName>` with names that match the chosen product type.

### `main.go`

```go
package main

import (
	"fmt"
	"log"

	factorymethod "<module>/<pattern-root>/factory"
	"<module>/<pattern-root>/product"
)

func printDetails(p product.Product) {
	fmt.Printf("Type: %s\n", p.GetType())
	fmt.Printf("Action: %s\n", p.DoSomething())
}

func main() {
	typeOne := product.<firstProductTypeName>
	factoryOne, err := factorymethod.GetFactory(typeOne)
	if err != nil {
		log.Fatalf("get factory one: %v", err)
	}

	typeTwo := product.<secondProductTypeName>
	factoryTwo, err := factorymethod.GetFactory(typeTwo)
	if err != nil {
		log.Fatalf("get factory two: %v", err)
	}

	productOne := factoryOne.CreateProduct("Alice")
	productTwo := factoryTwo.CreateProduct("Bob")

	printDetails(productOne)
	printDetails(productTwo)

	fmt.Println(factorymethod.OneTimeAction(factoryOne, "Carol"))
	fmt.Println(factorymethod.OneTimeAction(factoryTwo, "Dave"))
}
```
