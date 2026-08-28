---
name: go-pattern-prototype
description: "Lightweight Go Prototype file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: prototype`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Prototype in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Prototype

## Purpose

Provide a file-by-file Go skeleton for Prototype.

## Non-Obvious Go Notes

- Keep the shared `Prototype[T]` contract in its own small package when multiple concrete types clone themselves. This gives leaf and composite prototypes one common shape without forcing inheritance-style structure.
- Let each type clone only the state it owns directly. If a parent type must re-link back-references or repair relationships, do that in the parent's `Clone`, not in child clones.
- Use a value receiver for simple leaf values that copy cleanly by value. Use a pointer receiver when cloning a parent object that owns slices, nested references, or identity that should stay attached to the new instance.
- Be explicit about deep vs shallow copy behavior. Prototype is useful only when the clone boundary is unambiguous.
- If slices, maps, pointers, or nested prototypes are present, clone them intentionally so the result does not silently share mutable state with the original.

## Folder Shape

```text
<pattern-root>/
├── main.go
├── prototype/
│   └── prototype.go
└── model/
    ├── <leaf>.go
    ├── <node>.go
    └── <owner>.go
```

## File-By-File Skeleton

### `prototype/prototype.go`

```go
// Package prototype defines the contract for values that copy themselves.
package prototype

// Prototype is anything that can copy itself.
type Prototype[T any] interface {
	Clone() T
}
```

### `model/<leaf>.go`

```go
// Package model holds the values that implement Prototype.
package model

// <leafName> is a leaf prototype with no nested mutable references.
type <leafName> struct {
	Name string
	Tag  string
}

// Clone returns a value copy of the leaf prototype.
func (v <leafName>) Clone() <leafName> {
	return <leafName>{
		Name: v.Name,
		Tag:  v.Tag,
	}
}
```

### `model/<node>.go`

```go
package model

// <nodeName> is a composite prototype with nested state and an optional
// back-reference to its owner.
type <nodeName> struct {
	Label string
	Leaf  <leafName>
	Data  string
	Owner *<ownerName>
}

// Clone deep-copies the state owned by the node. Owner is left nil so the
// aggregate clone can re-link it to the new owner.
func (v <nodeName>) Clone() <nodeName> {
	return <nodeName>{
		Label: v.Label,
		Leaf:  v.Leaf.Clone(),
		Data:  v.Data,
		Owner: nil,
	}
}
```

### `model/<owner>.go`

```go
package model

// <ownerName> owns a collection of composite prototypes.
type <ownerName> struct {
	Name  string
	Nodes []<nodeName>
}

// Clone rebuilds the aggregate so cloned children point back to the clone,
// not to the original owner.
func (v *<ownerName>) Clone() *<ownerName> {
	clone := &<ownerName>{
		Name: v.Name,
	}

	for _, node := range v.Nodes {
		clonedNode := node.Clone()
		clonedNode.Owner = clone
		clone.Nodes = append(clone.Nodes, clonedNode)
	}

	return clone
}
```

### `main.go`

```go
package main

import (
	"fmt"

	"<module>/<pattern-root>/model"
)

func main() {
	owner := &model.<ownerName>{Name: "base"}
	owner.Nodes = []model.<nodeName>{
		{
			Label: "first",
			Leaf: model.<leafName>{
				Name: "alpha",
				Tag:  "x",
			},
			Data: "d1",
		},
		{
			Label: "second",
			Leaf: model.<leafName>{
				Name: "beta",
				Tag:  "y",
			},
		},
	}

	clonedOwner := owner.Clone()

	fmt.Printf("original name=%q leaf=%q\n", owner.Name, owner.Nodes[0].Leaf.Name)
	fmt.Printf("clone name=%q leaf=%q\n", clonedOwner.Name, clonedOwner.Nodes[0].Leaf.Name)
	fmt.Printf("back-reference=%q\n", clonedOwner.Nodes[0].Owner.Name)
}
```
