---
name: go-pattern-proxy
description: "Go Proxy skeleton and implementation notes. Use when the classifier recommends proxy or the user asks to implement, scaffold, or inspect this pattern in Go."
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

Read [the folder shape and file-by-file skeleton](references/skeleton.md) when implementing, scaffolding, or inspecting this pattern.
