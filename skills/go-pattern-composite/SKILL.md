---
name: go-pattern-composite
description: "Lightweight Go Composite file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: composite`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Composite in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Composite

## Purpose

Provide a file-by-file Go skeleton for Composite.

## Non-Obvious Go Notes

- Put the shared `Component` contract in its own package so leaves and composites can import it without a circular dependency. The client needs only this contract.
- Keep child-management methods such as `Add` and `Remove` off `Component`: leaves have no children, while the composite owns tree mutation.
- Use pointer receivers for a mutable composite, then store `*Composite` behind `Component`. A parent must retain the same object when a nested composite changes.
- A stateless leaf can use value receivers and be stored by value; it still satisfies the same `Component` contract.
- Remove a child by a stable identifier, rather than comparing interface values with `==`. A concrete component containing a slice, map, or function is not comparable and can make that comparison panic.
- Let recursive operations delegate through `Component`. A composite should not need type switches to distinguish a leaf from another composite.

## Folder Shape

```text
<pattern-root>/
├── main.go
├── component/
│   └── component.go
├── composite/
│   └── <container>.go
└── leaf/
    ├── <leaf-one>.go
    └── <leaf-two>.go
```

## File-By-File Skeleton

### `component/component.go`

```go
// Package component defines the contract shared by leaves and composites.
package component

// Component lets clients handle one item and a whole subtree uniformly.
type Component interface {
	Name() string
	Size() int64
	Find(path string) (Component, bool)
}
```

### `composite/<container>.go`

```go
// Package composite holds components that own children.
package composite

import (
	"fmt"
	"slices"
	"strings"

	"<module>/<pattern-root>/component"
)

// <containerName> is a component that can contain other components.
type <containerName> struct {
	Title    string
	children []component.Component
}

func (c *<containerName>) Name() string {
	return c.Title
}

// Add belongs only to the composite because leaves cannot own children.
func (c *<containerName>) Add(children ...component.Component) {
	c.children = append(c.children, children...)
}

// Remove uses a stable name so it never compares possibly non-comparable interface values.
func (c *<containerName>) Remove(name string) error {
	for i, child := range c.children {
		if child.Name() == name {
			c.children = slices.Delete(c.children, i, i+1)
			return nil
		}
	}

	return fmt.Errorf("%s has no child named %q", c.Title, name)
}

func (c *<containerName>) Size() int64 {
	var total int64
	for _, child := range c.children {
		total += child.Size()
	}

	return total
}

// Find consumes one path segment, then delegates the rest without knowing a child's concrete type.
func (c *<containerName>) Find(path string) (component.Component, bool) {
	head, tail, _ := strings.Cut(path, "/")
	if head != c.Title {
		return nil, false
	}
	if tail == "" {
		return c, true
	}

	for _, child := range c.children {
		if found, ok := child.Find(tail); ok {
			return found, true
		}
	}

	return nil, false
}
```

### `leaf/<leaf-one>.go`

```go
// Package leaf holds components with no children.
package leaf

import "<module>/<pattern-root>/component"

type <leafOneName> struct {
	Title string
	Bytes int64
}

func (l <leafOneName>) Name() string {
	return l.Title
}

func (l <leafOneName>) Size() int64 {
	return l.Bytes
}

func (l <leafOneName>) Find(path string) (component.Component, bool) {
	if path != l.Title {
		return nil, false
	}

	return l, true
}
```

### `leaf/<leaf-two>.go`

```go
package leaf

import "<module>/<pattern-root>/component"

// <leafTwoName> shows that another leaf can compute the same operation differently.
type <leafTwoName> struct {
	Title  string
	Target string
}

func (l <leafTwoName>) Name() string {
	return l.Title
}

func (l <leafTwoName>) Size() int64 {
	return int64(len(l.Target))
}

func (l <leafTwoName>) Find(path string) (component.Component, bool) {
	if path != l.Title {
		return nil, false
	}

	return l, true
}
```

### `main.go`

```go
package main

import (
	"fmt"

	"<module>/<pattern-root>/composite"
	"<module>/<pattern-root>/leaf"
)

func main() {
	child := &composite.<containerName>{Title: "child"}
	child.Add(leaf.<leafOneName>{Title: "item", Bytes: 128})

	root := &composite.<containerName>{Title: "root"}
	root.Add(child, leaf.<leafTwoName>{Title: "shortcut", Target: "child/item"})

	// The client uses the same operations for a nested composite and either leaf.
	fmt.Println(root.Size())

	if found, ok := root.Find("root/child/item"); ok {
		fmt.Println(found.Name())
	}
}
```
