---
name: go-pattern-flyweight
description: "Lightweight Go Flyweight file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: flyweight`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Flyweight in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Flyweight

## Purpose

Provide a file-by-file Go skeleton for Flyweight.

## Non-Obvious Go Notes

- Put the shared flyweight and its factory in one package. Keep flyweight fields private so callers cannot create mutable, unshared copies outside the factory.
- Keep per-instance state in a separate `extrinsic` package. Do not name that package `context`: `context` already belongs to the standard library in Go.
- Store a pointer to the flyweight in each context object. The context stays small, while the pointer identity makes sharing explicit.
- Pass extrinsic values as method arguments rather than storing them in the flyweight. One shared value can then serve every position, request, or instance.
- Protect a shared factory cache with `sync.RWMutex`. On a miss, release `RLock`, acquire `Lock`, and check again: Go mutexes cannot upgrade a read lock, and another goroutine may have inserted the entry meanwhile.
- Keep only immutable intrinsic state in a flyweight after it enters the cache. Mutating it would change every context that shares the pointer.

## Folder Shape

```text
<pattern-root>/
├── main.go
├── extrinsic/
│   └── item.go
└── flyweight/
    ├── factory.go
    └── style.go
```

## File-By-File Skeleton

### `flyweight/style.go`

```go
// Package flyweight holds shared objects and the factory that returns them.
package flyweight

import "fmt"

// Style is the flyweight: state shared by every item of one kind.
type Style struct {
	name    string
	color   string
	texture string
}

// Draw receives position as extrinsic state, so one Style works for every matching item.
func (s *Style) Draw(x, y int) string {
	return fmt.Sprintf("%s at (%d,%d) in %s", s.name, x, y, s.color)
}
```

### `flyweight/factory.go`

```go
package flyweight

import "sync"

// Factory keeps one shared Style per intrinsic-state key.
type Factory struct {
	mu     sync.RWMutex
	styles map[string]*Style
}

// NewFactory starts empty; every flyweight is created on its first request.
func NewFactory() *Factory {
	return &Factory{styles: make(map[string]*Style)}
}

// Get returns the existing flyweight or creates it once. It is safe for concurrent use.
func (f *Factory) Get(name, color, texture string) *Style {
	key := name + "|" + color + "|" + texture

	f.mu.RLock()
	if shared, ok := f.styles[key]; ok {
		f.mu.RUnlock()

		return shared
	}

	f.mu.RUnlock()

	f.mu.Lock()
	defer f.mu.Unlock()

	// An RWMutex read lock cannot be upgraded, so another goroutine may have
	// inserted this key meanwhile.
	if shared, ok := f.styles[key]; ok {
		return shared
	}

	shared := &Style{name: name, color: color, texture: texture}
	f.styles[key] = shared

	return shared
}

// Size counts distinct flyweights, not the items that share them.
func (f *Factory) Size() int {
	f.mu.RLock()
	defer f.mu.RUnlock()

	return len(f.styles)
}
```

### `extrinsic/item.go`

```go
// Package extrinsic holds the per-instance state that is not shared.
package extrinsic

import "<module>/<pattern-root>/flyweight"

// Item keeps only what differs per instance plus a pointer to shared state.
type Item struct {
	X     int
	Y     int
	Style *flyweight.Style
}

// Draw hands this item's own position to the Style it shares with other items.
func (i Item) Draw() string {
	return i.Style.Draw(i.X, i.Y)
}
```

### `main.go`

```go
package main

import (
	"fmt"

	"<module>/<pattern-root>/extrinsic"
	"<module>/<pattern-root>/flyweight"
)

func main() {
	factory := flyweight.NewFactory()
	first := factory.Get("<name>", "<color>", "<texture>")
	second := factory.Get("<name>", "<color>", "<texture>")

	items := []extrinsic.Item{
		{X: 10, Y: 20, Style: first},
		{X: 30, Y: 40, Style: second},
	}

	// Equal intrinsic state reuses one pointer while each item retains its own position.
	fmt.Println(first == second)
	for _, item := range items {
		fmt.Println(item.Draw())
	}
}
```
