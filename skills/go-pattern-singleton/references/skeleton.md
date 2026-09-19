## Folder Shape

```text
<pattern-root>/
├── main.go
└── singleton/
    ├── instance.go
    └── singleton.go
```

## File-By-File Skeleton

### `singleton/instance.go`

```go
// Package singleton owns the one shared value and the accessor that builds it.
package singleton

import "fmt"

// Instance is the single shared value this package exposes.
type Instance struct {
	name string
}

func (i Instance) Describe() string {
	return fmt.Sprintf("instance %q", i.name)
}
```

### `singleton/singleton.go`

```go
package singleton

import (
	"context"
	"fmt"
	"sync"
)

// lazyInstance holds the lazily-created Instance behind a lock.
type lazyInstance struct {
	instance *Instance
	mu       sync.RWMutex
}

var defaultInstance lazyInstance

// Default builds the one process-wide Instance on first use and is safe for concurrent use.
func Default(ctx context.Context) (*Instance, error) {
	defaultInstance.mu.RLock()
	if defaultInstance.instance != nil {
		defaultInstance.mu.RUnlock()

		return defaultInstance.instance, nil
	}

	defaultInstance.mu.RUnlock()

	defaultInstance.mu.Lock()
	defer defaultInstance.mu.Unlock()

	// A write lock cannot be acquired atomically after a read lock, so another
	// goroutine may have created the instance meanwhile.
	if defaultInstance.instance != nil {
		return defaultInstance.instance, nil
	}

	created, err := buildInstance(ctx)
	if err != nil {
		return nil, fmt.Errorf("building instance: %w", err)
	}

	defaultInstance.instance = created

	return defaultInstance.instance, nil
}

func buildInstance(ctx context.Context) (*Instance, error) {
	if err := ctx.Err(); err != nil {
		return nil, err
	}

	return &Instance{name: "shared"}, nil
}
```

Keep the setup helper private. If initialization is trivial and cannot fail, the same skeleton can be simplified to `sync.Once`, but keep the explicit accessor.

### `main.go`

```go
package main

import (
	"context"
	"fmt"
	"log"

	"<module>/<pattern-root>/singleton"
)

func main() {
	ctx := context.Background()

	first, err := singleton.Default(ctx)
	if err != nil {
		log.Fatalf("default instance: %v", err)
	}

	second, err := singleton.Default(ctx)
	if err != nil {
		log.Fatalf("default instance: %v", err)
	}

	fmt.Println(first.Describe())
	fmt.Printf("same instance: %t\n", first == second)
}
```
