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

## Folder Shape

```text
<pattern-root>/
├── main.go
├── factory/
│   ├── factory.go
│   ├── factory_<family-one>.go
│   └── factory_<family-two>.go
└── product/
    ├── product.go
    ├── <family-one>/
    │   ├── family.go
    │   ├── product_a.go
    │   └── product_b.go
    └── <family-two>/
        ├── family.go
        ├── product_a.go
        └── product_b.go
```

## File-By-File Skeleton

### `product/product.go`

```go
// Package product defines the contracts and the family identifier every family implements.
package product

// FamilyType identifies a family of related products.
type FamilyType string

// ProductA is the common contract for the first product kind.
type ProductA interface {
	Family() FamilyType
	DoA() string
}

// ProductB is the common contract for the second product kind.
type ProductB interface {
	Family() FamilyType
	DoB() string
}
```

### `product/<family>/family.go`

```go
// Package <familyPackage> holds one complete family of products that belong together.
package <familyPackage>

import "<module>/<pattern-root>/product"

// <familyName> identifies one product family.
const <familyName> product.FamilyType = "<family>"
```

### `product/<family>/product_a.go`

```go
package <familyPackage>

import "<module>/<pattern-root>/product"

type <productAName> struct{}

// Family identifies the family that callers must not mix this product out of.
func (p <productAName>) Family() product.FamilyType {
	return <familyName>
}

func (p <productAName>) DoA() string {
	return "<family> product A behavior"
}
```

### `product/<family>/product_b.go`

```go
package <familyPackage>

import "<module>/<pattern-root>/product"

type <productBName> struct{}

// Family identifies the family that callers must not mix this product out of.
func (p <productBName>) Family() product.FamilyType {
	return <familyName>
}

func (p <productBName>) DoB() string {
	return "<family> product B behavior"
}
```

### `factory/factory.go`

```go
// Package factory picks the family a caller gets, so callers never name a concrete product.
package factory

import (
	"fmt"

	"<module>/<pattern-root>/product"
	<firstFamilyPackage> "<module>/<pattern-root>/product/<family-one>"
	<secondFamilyPackage> "<module>/<pattern-root>/product/<family-two>"
)

// Factory creates a full family of related products.
type Factory interface {
	CreateProductA() product.ProductA
	CreateProductB() product.ProductB
}

// OneTimeAction is what an abstract base class would implement in other languages.
func OneTimeAction(factory Factory) string {
	productA := factory.CreateProductA()
	productB := factory.CreateProductB()

	return fmt.Sprintf("%s. %s", productA.DoA(), productB.DoB())
}

func New(family product.FamilyType) (Factory, error) {
	switch family {
	case <firstFamilyPackage>.<firstFamilyName>:
		return <firstFactoryName>{}, nil
	case <secondFamilyPackage>.<secondFamilyName>:
		return <secondFactoryName>{}, nil
	default:
		return nil, fmt.Errorf("unsupported product family: %q", family)
	}
}
```

### `factory/factory_<family>.go`

```go
package factory

import (
	"<module>/<pattern-root>/product"
	<familyPackage> "<module>/<pattern-root>/product/<family>"
)

// <factoryName> creates products of one concrete family.
type <factoryName> struct{}

// CreateProductA and CreateProductB always return products of the same family.
func (f <factoryName>) CreateProductA() product.ProductA {
	return <familyPackage>.<productAName>{}
}

func (f <factoryName>) CreateProductB() product.ProductB {
	return <familyPackage>.<productBName>{}
}
```

Use one file like the template above per concrete family, replacing placeholders such as `<factoryName>`, `<productAName>`, `<productBName>`, and `<familyName>` with names that match the chosen family.

### `main.go`

```go
package main

import (
	"fmt"
	"log"

	"<module>/<pattern-root>/factory"
	"<module>/<pattern-root>/product"
	<firstFamilyPackage> "<module>/<pattern-root>/product/<family-one>"
	<secondFamilyPackage> "<module>/<pattern-root>/product/<family-two>"
)

func printProductADetails(p product.ProductA) {
	fmt.Printf("Family: %s\n", p.Family())
	fmt.Printf("Action: %s\n", p.DoA())
}

func printProductBDetails(p product.ProductB) {
	fmt.Printf("Family: %s\n", p.Family())
	fmt.Printf("Action: %s\n", p.DoB())
}

func main() {
	familyOneID := <firstFamilyPackage>.<firstFamilyName>
	factoryOne, err := factory.New(familyOneID)
	if err != nil {
		log.Fatalf("get factory one: %v", err)
	}

	familyTwoID := <secondFamilyPackage>.<secondFamilyName>
	factoryTwo, err := factory.New(familyTwoID)
	if err != nil {
		log.Fatalf("get factory two: %v", err)
	}

	productAFromOne := factoryOne.CreateProductA()
	productBFromOne := factoryOne.CreateProductB()

	productAFromTwo := factoryTwo.CreateProductA()
	productBFromTwo := factoryTwo.CreateProductB()

	printProductADetails(productAFromOne)
	printProductBDetails(productBFromOne)

	printProductADetails(productAFromTwo)
	printProductBDetails(productBFromTwo)

	fmt.Println(factory.OneTimeAction(factoryOne))
	fmt.Println(factory.OneTimeAction(factoryTwo))
}
```
