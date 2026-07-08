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
- Use pointer receivers for concrete builders so they can accumulate state across steps and reset themselves after `Build`.
- Let `Build` validate required parts, return the shared `product.Product`, and then clear internal state for reuse.
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
package product

// Product is what a builder produces.
type Product interface {
	Describe() string
}
```

### `part/part_<required-one>/part_<required-one>.go`

```go
package <requiredOnePackage>

type <requiredOneName> struct {
	Value string
}
```

### `part/part_<required-two>/part_<required-two>.go`

```go
package <requiredTwoPackage>

type <requiredTwoName> struct {
	Enabled bool
}
```

### `part/part_<optional>/part_<optional>.go`

```go
package <optionalPartPackage>

import <requiredOnePackage> "<module>/<pattern-root>/part/part_<required-one>"

// <optionalPartName> is an optional part that can depend on another part.
type <optionalPartName> struct {
	related *<requiredOnePackage>.<requiredOneName>
}

func New<optionalPartName>(related *<requiredOnePackage>.<requiredOneName>) *<optionalPartName> {
	return &<optionalPartName>{related: related}
}

func (p *<optionalPartName>) Describe() string {
	if p.related == nil {
		return "<optional-part> not configured"
	}

	return "<optional-part> configured"
}
```

### `builder/builder.go`

```go
package builder

import (
	"fmt"

	<requiredOnePackage> "<module>/<pattern-root>/part/part_<required-one>"
	<requiredTwoPackage> "<module>/<pattern-root>/part/part_<required-two>"
	<optionalPartPackage> "<module>/<pattern-root>/part/part_<optional>"
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

// BuilderType selects a concrete builder.
type BuilderType string

const (
	<firstBuilderTypeName> BuilderType = "<variant-one>"
	<secondBuilderTypeName> BuilderType = "<variant-two>"
)

// GetBuilder returns the concrete builder for the given type.
func GetBuilder(builderType BuilderType) (Builder, error) {
	switch builderType {
	case <firstBuilderTypeName>:
		return &<firstBuilderName>{}, nil
	case <secondBuilderTypeName>:
		return &<secondBuilderName>{}, nil
	default:
		return nil, fmt.Errorf("unsupported builder type: %q", builderType)
	}
}

// ValidateParts checks that every required part is set.
func ValidateParts(
	partOne *<requiredOnePackage>.<requiredOneName>,
	partTwo *<requiredTwoPackage>.<requiredTwoName>,
) error {
	if partOne == nil {
		return fmt.Errorf("missing required part: <required-one>")
	}

	if partTwo == nil {
		return fmt.Errorf("missing required part: <required-two>")
	}

	return nil
}
```

### `builder/builder_<variant>.go`

```go
package builder

import (
	<requiredOnePackage> "<module>/<pattern-root>/part/part_<required-one>"
	<requiredTwoPackage> "<module>/<pattern-root>/part/part_<required-two>"
	<optionalPartPackage> "<module>/<pattern-root>/part/part_<optional>"
	"<module>/<pattern-root>/product"
	<productPackage> "<module>/<pattern-root>/product/product_<variant>"
)

// <builderName> assembles one concrete product variant.
type <builderName> struct {
	partOne *<requiredOnePackage>.<requiredOneName>
	partTwo *<requiredTwoPackage>.<requiredTwoName>
	partOpt *<optionalPartPackage>.<optionalPartName>
}

func (b *<builderName>) Reset() Builder {
	*b = <builderName>{}

	return b
}

func (b *<builderName>) Set<requiredOneName>(part <requiredOnePackage>.<requiredOneName>) Builder {
	b.partOne = &part

	return b
}

func (b *<builderName>) Set<requiredTwoName>(part <requiredTwoPackage>.<requiredTwoName>) Builder {
	b.partTwo = &part

	return b
}

func (b *<builderName>) Set<optionalPartName>(part <optionalPartPackage>.<optionalPartName>) Builder {
	b.partOpt = &part

	return b
}

func (b *<builderName>) Build() (product.Product, error) {
	if err := ValidateParts(b.partOne, b.partTwo); err != nil {
		return nil, err
	}

	result := <productPackage>.<productName>{
		<requiredOneFieldName>: b.partOne,
		<requiredTwoFieldName>: b.partTwo,
		<optionalPartFieldName>: b.partOpt,
	}

	b.Reset()

	return result, nil
}
```

Use one file like the template above per concrete builder and product variant, replacing placeholders such as `<builderName>`, `<productName>`, and the field placeholders with names that match the chosen variant.

### `builder/director.go`

```go
package builder

import (
	<requiredOnePackage> "<module>/<pattern-root>/part/part_<required-one>"
	<requiredTwoPackage> "<module>/<pattern-root>/part/part_<required-two>"
	<optionalPartPackage> "<module>/<pattern-root>/part/part_<optional>"
	"<module>/<pattern-root>/product"
)

// Director drives a builder through reusable recipes.
type Director struct {
	builder Builder
}

func NewDirector(builder Builder) *Director {
	return &Director{builder: builder}
}

func (d *Director) SetBuilder(builder Builder) {
	d.builder = builder
}

func (d *Director) BuildVariantOne() (product.Product, error) {
	partOne := <requiredOnePackage>.<requiredOneName>{Value: "default"}

	d.builder.
		Reset().
		Set<requiredOneName>(partOne).
		Set<requiredTwoName>(<requiredTwoPackage>.<requiredTwoName>{Enabled: true}).
		Set<optionalPartName>(*<optionalPartPackage>.New<optionalPartName>(&partOne))

	return d.builder.Build()
}

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
package <productPackage>

import (
	"strings"

	<requiredOnePackage> "<module>/<pattern-root>/part/part_<required-one>"
	<requiredTwoPackage> "<module>/<pattern-root>/part/part_<required-two>"
	<optionalPartPackage> "<module>/<pattern-root>/part/part_<optional>"
	"<module>/<pattern-root>/product"
)

type <productName> struct {
	<requiredOneFieldName> *<requiredOnePackage>.<requiredOneName>
	<requiredTwoFieldName> *<requiredTwoPackage>.<requiredTwoName>
	<optionalPartFieldName> *<optionalPartPackage>.<optionalPartName>
}

var _ product.Product = <productName>{}

func (p <productName>) Describe() string {
	var b strings.Builder

	b.WriteString("<product-name> assembled")

	return b.String()
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
	builderOne, err := builder.GetBuilder(builder.<firstBuilderTypeName>)
	if err != nil {
		log.Fatalf("get builder one: %v", err)
	}

	builderTwo, err := builder.GetBuilder(builder.<secondBuilderTypeName>)
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
