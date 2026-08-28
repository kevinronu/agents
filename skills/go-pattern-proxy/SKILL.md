---
name: go-pattern-proxy
description: "Lightweight Go Proxy file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: proxy`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Proxy in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Proxy

## Purpose

Provide a file-by-file Go skeleton for Proxy.

## Non-Obvious Go Notes

- Put the interface in a small `service` package. The real service and the proxy implement it, so clients never need to distinguish the stand-in from the origin.
- Keep the origin as that interface inside the proxy. This allows the proxy to wrap the real service, a different backend, or a test double without changing proxy behavior.
- For a concurrent cache, use `RLock` for hits and release it before acquiring `Lock` on a miss. Go cannot upgrade an `RWMutex` read lock; check the cache again after taking the write lock because another goroutine may have filled it.
- Return `bytes.Clone` of cached slices. Without a defensive copy, a caller could mutate the bytes held for later callers.
- If construction starts a cleanup goroutine, expose `Stop` and make it idempotent with `sync.OnceFunc`; closing a channel twice panics and garbage collection does not stop goroutines.
- A periodic full-cache clear has an interval, not per-entry TTL semantics. Use a separate expiry model when entries must age independently.

## Folder Shape

```text
<pattern-root>/
├── main.go
├── proxy/
│   └── cache.go
├── real/
│   └── remote.go
└── service/
    └── library.go
```

## File-By-File Skeleton

### `service/library.go`

```go
// Package service defines the contract shared by the origin and its proxy.
package service

// Library is all the client needs to download an asset.
type Library interface {
	Download(id string) ([]byte, error)
}
```

### `real/remote.go`

```go
// Package real holds the origin service behind the proxy.
package real

import (
	"fmt"
	"time"
)

var assets = map[string]string{
	"<first-id>":  "first result",
	"<second-id>": "second result",
}

// Remote has no state; the proxy saves its expensive calls.
type Remote struct{}

func (Remote) Download(id string) ([]byte, error) {
	time.Sleep(300 * time.Millisecond)

	asset, ok := assets[id]
	if !ok {
		return nil, fmt.Errorf("no asset with id %q", id)
	}

	return []byte(asset), nil
}
```

### `proxy/cache.go`

```go
// Package proxy holds the stand-in the client uses instead of the origin service.
package proxy

import (
	"bytes"
	"sync"
	"time"

	"<module>/<pattern-root>/service"
)

// Cache implements the same contract while avoiding repeat origin calls.
type Cache struct {
	mu     sync.RWMutex
	origin service.Library
	stored map[string][]byte
	stop   func()
}

// NewCache starts a cleanup goroutine, so callers must later call Stop.
func NewCache(origin service.Library, interval time.Duration) *Cache {
	done := make(chan struct{})
	cache := &Cache{
		origin: origin,
		stored: make(map[string][]byte),
		stop:   sync.OnceFunc(func() { close(done) }),
	}

	go cache.clean(interval, done)

	return cache
}

func (c *Cache) Download(id string) ([]byte, error) {
	c.mu.RLock()
	if asset, ok := c.stored[id]; ok {
		c.mu.RUnlock()

		return bytes.Clone(asset), nil
	}

	c.mu.RUnlock()

	c.mu.Lock()
	defer c.mu.Unlock()

	// An RWMutex read lock cannot be upgraded, so another caller may have filled
	// this entry meanwhile.
	if asset, ok := c.stored[id]; ok {
		return bytes.Clone(asset), nil
	}

	asset, err := c.origin.Download(id)
	if err != nil {
		return nil, err // A failed download is not cached.
	}

	c.stored[id] = asset

	return bytes.Clone(asset), nil
}

// Stop ends the cleanup goroutine exactly once.
func (c *Cache) Stop() {
	c.stop()
}

func (c *Cache) clean(interval time.Duration, done <-chan struct{}) {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			c.mu.Lock()
			clear(c.stored)
			c.mu.Unlock()
		case <-done:
			return
		}
	}
}
```

### `main.go`

```go
package main

import (
	"fmt"
	"time"

	"<module>/<pattern-root>/proxy"
	"<module>/<pattern-root>/real"
	"<module>/<pattern-root>/service"
)

func main() {
	cache := proxy.NewCache(real.Remote{}, time.Second)
	defer cache.Stop()

	var library service.Library = cache
	for _, id := range []string{"<first-id>", "<second-id>", "<first-id>"} {
		asset, err := library.Download(id)
		if err != nil {
			fmt.Println(err)
			continue
		}

		fmt.Println(id, string(asset))
	}
}
```
