---
name: go-pattern-singleton
description: "Lightweight Go Singleton file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: singleton`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Singleton in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Singleton

## Purpose

Provide a file-by-file Go skeleton for Singleton.

## Non-Obvious Go Notes

- Keep the shared holder and the exported accessor in the same small package so callers cannot construct competing instances accidentally.
- Return the shared instance through an accessor like `GetInstance(...)` instead of exposing a package variable directly. This keeps lazy initialization, locking, and setup errors behind one stable entry point.
- Use a pointer return when callers must share one identity.
- If one-time setup can fail or depends on `context.Context`, prefer an explicit locking flow over `sync.Once`, so the accessor can return an error and retry later if initialization did not complete.
- Use a fast path for already-created reads and a guarded slow path for first creation when concurrent access matters.
- Keep the one-time build logic in a private helper so expensive setup stays isolated from the concurrency control.

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
package singleton

import "fmt"

// Instance is the single shared value this package exposes.
type Instance struct {
	name string
}

// Describe reports the shared instance identity.
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

// instanceSingleton holds the lazily-created Instance behind a lock.
type instanceSingleton struct {
	instance *Instance
	mu       sync.RWMutex
}

// shared is the package-level holder for the singleton instance.
var shared instanceSingleton

// GetInstance returns the shared Instance, creating it on first use.
func GetInstance(ctx context.Context) (*Instance, error) {
	// Fast path: return the instance if it already exists.
	shared.mu.RLock()
	if shared.instance != nil {
		shared.mu.RUnlock()

		return shared.instance, nil
	}

	shared.mu.RUnlock()

	// Slow path: take the write lock to create it.
	shared.mu.Lock()
	defer shared.mu.Unlock()

	// Re-check after the write lock in case another goroutine created it.
	if shared.instance != nil {
		return shared.instance, nil
	}

	created, err := buildInstance(ctx)
	if err != nil {
		return nil, fmt.Errorf("building instance: %w", err)
	}

	shared.instance = created

	return shared.instance, nil
}

// buildInstance performs the one-time setup that may fail.
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

	first, err := singleton.GetInstance(ctx)
	if err != nil {
		log.Fatalf("get instance: %v", err)
	}

	second, err := singleton.GetInstance(ctx)
	if err != nil {
		log.Fatalf("get instance: %v", err)
	}

	fmt.Println(first.Describe())
	fmt.Printf("same instance: %t\n", first == second)
}
```
