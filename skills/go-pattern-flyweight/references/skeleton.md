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
