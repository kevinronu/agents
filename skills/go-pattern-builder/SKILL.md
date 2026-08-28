---
name: go-pattern-builder
description: "Lightweight Go Builder file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: builder`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Builder in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Builder

## Purpose

Provide a file-by-file Go skeleton for Builder.

## Non-Obvious Go Notes

- Keep the shared `Builder` interface, selector type, and shared validation helper together in `builder/builder.go`. This gives callers and concrete builders one common contract without scattering the construction rules.
- Make chainable step methods return the shared `Builder` interface so concrete builders stay interchangeable at call sites.
- Use pointer receivers for concrete builders so they can accumulate state across steps.
- Let `Build` validate required parts and return the shared `product.Product`. Keep clearing accumulated state in `Reset`, called by whoever starts the next product, so `Build` does not silently discard the state a caller may still read.
- Keep `Director` as an optional layer for fixed recipes. It is useful when multiple construction sequences should stay reusable, but callers can still drive the builder directly when no recipe abstraction is needed.
- If one part depends on another, keep that dependency creation in the recipe or caller, not hidden inside unrelated builder steps.
- If an optional part depends on a required one, a small constructor helper can make that dependency explicit before the part enters the builder chain.

## Folder Shape

```text
<pattern-root>/
├── main.go
├── builder/
│   ├── builder.go
│   ├── builder_<variant-one>.go
│   ├── builder_<variant-two>.go
│   └── director.go
├── part/
│   ├── part_<required-one>/
│   │   └── part_<required-one>.go
│   ├── part_<required-two>/
│   │   └── part_<required-two>.go
│   └── part_<optional>/
│       └── part_<optional>.go
└── product/
    ├── product.go
    ├── product_<variant-one>/
    │   └── product_<variant-one>.go
    └── product_<variant-two>/
        └── product_<variant-two>.go
```

## File-By-File Skeleton

### `product/product.go`

```go
// Package product defines what every builder produces.
package product

// Product is what a builder produces.
type Product interface {
	Describe() string
}
```

### `part/part_<required-one>/part_<required-one>.go`

```go
// Package <requiredOnePackage> holds one part every product variant requires.
package <requiredOnePackage>

type <requiredOneName> struct {
	Value string
}
```

### `part/part_<required-two>/part_<required-two>.go`

```go
// Package <requiredTwoPackage> holds the second required part.
package <requiredTwoPackage>

type <requiredTwoName> struct {
	Enabled bool
}
```

### `part/part_<optional>/part_<optional>.go`

```go
// Package <optionalPartPackage> holds the part a caller may leave out.
package <optionalPartPackage>

import <requiredOnePackage> "<module>/<pattern-root>/part/part_<required-one>"

// <optionalPartName> is an optional part that can depend on another part.
type <optionalPartName> struct {
	related *<requiredOnePackage>.<requiredOneName>
}

// New<optionalPartName> makes the dependency on another part explicit at construction.
func New<optionalPartName>(related *<requiredOnePackage>.<requiredOneName>) *<optionalPartName> {
	return &<optionalPartName>{related: related}
}

// Describe reports whether the dependency was supplied at construction.
func (p *<optionalPartName>) Describe() string {
	if p.related == nil {
		return "<optional-part> not configured"
	}

	return "<optional-part> configured"
}
```

### `builder/builder.go`

```go
// Package builder assembles products step by step and picks which builder runs.
package builder

import (
	"errors"
	"fmt"

	<optionalPartPackage> "<module>/<pattern-root>/part/part_<optional>"
	<requiredOnePackage> "<module>/<pattern-root>/part/part_<required-one>"
	<requiredTwoPackage> "<module>/<pattern-root>/part/part_<required-two>"
	"<module>/<pattern-root>/product"
)

// Builder assembles a product through chainable steps.
type Builder interface {
	Reset() Builder
	Set<requiredOneName>(part <requiredOnePackage>.<requiredOneName>) Builder
	Set<requiredTwoName>(part <requiredTwoPackage>.<requiredTwoName>) Builder
	Set<optionalPartName>(part <optionalPartPackage>.<optionalPartName>) Builder
	Build() (product.Product, error)
}

// Type selects a concrete builder.
type Type string

// One constant per concrete builder, so callers pick a variant without naming its type.
const (
	<firstBuilderTypeName>  Type = "<variant-one>"
	<secondBuilderTypeName> Type = "<variant-two>"
)

func New(builderType Type) (Builder, error) {
	switch builderType {
	case <firstBuilderTypeName>:
		return &<firstBuilderName>{}, nil
	case <secondBuilderTypeName>:
		return &<secondBuilderName>{}, nil
	default:
		return nil, fmt.Errorf("unsupported builder type: %q", builderType)
	}
}

func validateParts(
	partOne *<requiredOnePackage>.<requiredOneName>,
	partTwo *<requiredTwoPackage>.<requiredTwoName>,
) error {
	if partOne == nil {
		return errors.New("missing required part: <required-one>")
	}

	if partTwo == nil {
		return errors.New("missing required part: <required-two>")
	}

	return nil
}
```

### `builder/builder_<variant>.go`

```go
package builder

import (
	<optionalPartPackage> "<module>/<pattern-root>/part/part_<optional>"
	<requiredOnePackage> "<module>/<pattern-root>/part/part_<required-one>"
	<requiredTwoPackage> "<module>/<pattern-root>/part/part_<required-two>"
	"<module>/<pattern-root>/product"
	<productPackage> "<module>/<pattern-root>/product/product_<variant>"
)

// <builderName> assembles one concrete product variant.
type <builderName> struct {
	partOne *<requiredOnePackage>.<requiredOneName>
	partTwo *<requiredTwoPackage>.<requiredTwoName>
	partOpt *<optionalPartPackage>.<optionalPartName>
}

// Reset returns the builder itself, so a recipe can chain the first step onto it.
func (b *<builderName>) Reset() Builder {
	*b = <builderName>{}

	return b
}

// Set<requiredOneName> stores a copy, so later edits by the caller do not reach the product.
func (b *<builderName>) Set<requiredOneName>(part <requiredOnePackage>.<requiredOneName>) Builder {
	b.partOne = &part

	return b
}

func (b *<builderName>) Set<requiredTwoName>(part <requiredTwoPackage>.<requiredTwoName>) Builder {
	b.partTwo = &part

	return b
}

// Set<optionalPartName> may be skipped entirely; Build succeeds without it.
func (b *<builderName>) Set<optionalPartName>(part <optionalPartPackage>.<optionalPartName>) Builder {
	b.partOpt = &part

	return b
}

// Build reports the first missing required part and leaves accumulated state intact.
func (b *<builderName>) Build() (product.Product, error) {
	if err := validateParts(b.partOne, b.partTwo); err != nil {
		return nil, err
	}

	return <productPackage>.<productName>{
		<requiredOneFieldName>:  b.partOne,
		<requiredTwoFieldName>:  b.partTwo,
		<optionalPartFieldName>: b.partOpt,
	}, nil
}
```

Use one file like the template above per concrete builder and product variant, replacing placeholders such as `<builderName>`, `<productName>`, and the field placeholders with names that match the chosen variant.

### `builder/director.go`

```go
package builder

import (
	<optionalPartPackage> "<module>/<pattern-root>/part/part_<optional>"
	<requiredOnePackage> "<module>/<pattern-root>/part/part_<required-one>"
	<requiredTwoPackage> "<module>/<pattern-root>/part/part_<required-two>"
	"<module>/<pattern-root>/product"
)

// Director drives a builder through reusable recipes.
type Director struct {
	builder Builder
}

// NewDirector binds the recipes to one builder; SetBuilder swaps it later.
func NewDirector(builder Builder) *Director {
	return &Director{builder: builder}
}

// SetBuilder points the same recipes at another builder.
func (d *Director) SetBuilder(builder Builder) {
	d.builder = builder
}

// BuildVariantOne resets first, so the recipe never inherits an earlier product's parts.
func (d *Director) BuildVariantOne() (product.Product, error) {
	partOne := <requiredOnePackage>.<requiredOneName>{Value: "default"}

	d.builder.
		Reset().
		Set<requiredOneName>(partOne).
		Set<requiredTwoName>(<requiredTwoPackage>.<requiredTwoName>{Enabled: true}).
		Set<optionalPartName>(*<optionalPartPackage>.New<optionalPartName>(&partOne))

	return d.builder.Build()
}

// BuildVariantTwo leaves the optional part unset, which Build accepts.
func (d *Director) BuildVariantTwo() (product.Product, error) {
	d.builder.
		Reset().
		Set<requiredOneName>(<requiredOnePackage>.<requiredOneName>{Value: "custom"}).
		Set<requiredTwoName>(<requiredTwoPackage>.<requiredTwoName>{Enabled: false})

	return d.builder.Build()
}
```

Keep `Director` only when reusable recipes are part of the problem. If callers assemble products directly and no shared construction sequences exist, it can be omitted.

### `product/product_<variant>/product_<variant>.go`

```go
// Package <productPackage> holds one assembled product variant.
package <productPackage>

import (
	<optionalPartPackage> "<module>/<pattern-root>/part/part_<optional>"
	<requiredOnePackage> "<module>/<pattern-root>/part/part_<required-one>"
	<requiredTwoPackage> "<module>/<pattern-root>/part/part_<required-two>"
	"<module>/<pattern-root>/product"
)

// <productName> is one assembled variant; only a builder should construct it.
type <productName> struct {
	<requiredOneFieldName>  *<requiredOnePackage>.<requiredOneName>
	<requiredTwoFieldName>  *<requiredTwoPackage>.<requiredTwoName>
	<optionalPartFieldName> *<optionalPartPackage>.<optionalPartName>
}

var _ product.Product = <productName>{}

func (p <productName>) Describe() string {
	if p.<optionalPartFieldName> == nil {
		return "<product-name> assembled"
	}

	return "<product-name> assembled with " + p.<optionalPartFieldName>.Describe()
}
```

Use one file like the template above per concrete product variant. Let each product render itself in its own way while keeping the same `product.Product` contract.

### `main.go`

```go
package main

import (
	"fmt"
	"log"

	"<module>/<pattern-root>/builder"
)

func main() {
	builderOne, err := builder.New(builder.<firstBuilderTypeName>)
	if err != nil {
		log.Fatalf("get builder one: %v", err)
	}

	builderTwo, err := builder.New(builder.<secondBuilderTypeName>)
	if err != nil {
		log.Fatalf("get builder two: %v", err)
	}

	director := builder.NewDirector(builderOne)

	productOne, err := director.BuildVariantOne()
	if err != nil {
		log.Fatalf("build product one: %v", err)
	}

	fmt.Println(productOne.Describe())

	director.SetBuilder(builderTwo)

	productTwo, err := director.BuildVariantTwo()
	if err != nil {
		log.Fatalf("build product two: %v", err)
	}

	fmt.Println(productTwo.Describe())
}
```
