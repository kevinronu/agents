---
name: go-pattern-chain-of-responsibility
description: "Lightweight Go Chain of Responsibility file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: chain-of-responsibility`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Chain of Responsibility in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Chain Of Responsibility

## Purpose

Provide a file-by-file Go skeleton for Chain Of Responsibility.

## Non-Obvious Go Notes

- Put `Request`, `Handler`, and the reusable successor link in one `handler` package. Concrete steps can import that package without depending on one another.
- Embed `Successor` in each concrete handler. It replaces the next-link behavior that an abstract base class often provides in other languages; a step calls `Successor.Handle` only after its own check succeeds.
- Let `SetNext` return the handler passed to it, so `head.SetNext(second).SetNext(third)` reads naturally. Keep `head` separately: the return value is the next step, not the head.
- Treat a `nil` successor as successful completion. A final handler can delegate without knowing whether it is last.
- Build the chain where policy is configured, not inside a concrete step. Order is behavior: a rejection prevents every later handler from running.
- Let the protected server own one optional `handler.Handler`. `Serve` runs it before its own work, and a full chain fits in that single field.
- A rate limiter is mutable state. The GCRA version keeps a scheduled due time instead of a resetting counter, but a chain shared by goroutines still needs synchronization around that state.

## Folder Shape

```text
<pattern-root>/
├── main.go
├── concrete/
│   ├── admin_only.go
│   ├── auth.go
│   └── rate_limit.go
├── handler/
│   └── handler.go
└── server/
    └── server.go
```

## File-By-File Skeleton

### `handler/handler.go`

```go
// Package handler defines the contract of the chain and the link between its steps.
package handler

// Request is what travels down the chain. It carries everything any step might need to decide.
type Request struct {
	Email    string
	Password string
	Path     string
}

// Handler either stops the request with an error or passes it to its successor.
type Handler interface {
	SetNext(next Handler) Handler
	Handle(req Request) error
}

// Successor is embedded by concrete handlers to share the link and end-of-chain behavior.
type Successor struct {
	next Handler
}

func (s *Successor) SetNext(next Handler) Handler {
	s.next = next
	return next
}

func (s *Successor) Handle(req Request) error {
	if s.next == nil {
		return nil
	}

	return s.next.Handle(req)
}
```

### `server/server.go`

```go
// Package server holds the service that the chain protects.
package server

import (
	"fmt"

	"<module>/<pattern-root>/handler"
)

type account struct {
	password string
	admin    bool
}

var pages = map[string]string{
	"/reports":        "quarterly report",
	"/admin/settings": "server settings",
}

// Server knows one middleware Handler, which may represent a whole chain.
type Server struct {
	accounts   map[string]account
	middleware handler.Handler
}

func New() *Server {
	return &Server{accounts: make(map[string]account)}
}

func (s *Server) SetMiddleware(middleware handler.Handler) {
	s.middleware = middleware
}

func (s *Server) Register(email, password string) {
	s.accounts[email] = account{password: password}
}

func (s *Server) RegisterAdmin(email, password string) {
	s.accounts[email] = account{password: password, admin: true}
}

// Serve runs middleware first, then performs the server's normal work.
func (s *Server) Serve(req handler.Request) (string, error) {
	if s.middleware != nil {
		if err := s.middleware.Handle(req); err != nil {
			return "", err
		}
	}

	page, ok := pages[req.Path]
	if !ok {
		return "", fmt.Errorf("no page at %q", req.Path)
	}

	return page, nil
}

func (s *Server) HasEmail(email string) bool {
	_, ok := s.accounts[email]
	return ok
}

func (s *Server) IsValidPassword(email, password string) bool {
	return s.accounts[email].password == password
}

func (s *Server) IsAdmin(email string) bool {
	return s.accounts[email].admin
}
```

### `concrete/rate_limit.go`

```go
// Package concrete holds independent steps in the chain.
package concrete

import (
	"fmt"
	"time"

	"<module>/<pattern-root>/handler"
)

// RateLimit uses GCRA: it stores when the next request is due, not a resetting window counter.
// Add a lock if one chain instance serves concurrent requests.
type RateLimit struct {
	handler.Successor

	interval time.Duration
	burst    time.Duration
	due      time.Time
}

func NewRateLimit(limit int, window time.Duration) *RateLimit {
	return &RateLimit{interval: window / time.Duration(limit), burst: window}
}

func (r *RateLimit) Handle(req handler.Request) error {
	now := time.Now()
	due := r.due
	if due.Before(now) {
		due = now // A fresh or idle limiter starts from the current time.
	}

	if allowAt := due.Add(r.interval - r.burst); now.Before(allowAt) {
		return fmt.Errorf("rate limit: too many requests, wait %v", allowAt.Sub(now).Round(time.Millisecond))
	}

	r.due = due.Add(r.interval)
	return r.Successor.Handle(req)
}
```

### `concrete/auth.go`

```go
package concrete

import (
	"errors"

	"<module>/<pattern-root>/handler"
	"<module>/<pattern-root>/server"
)

// Auth establishes the identity later handlers can use.
type Auth struct {
	handler.Successor
	server *server.Server
}

func NewAuth(server *server.Server) *Auth {
	return &Auth{server: server}
}

func (a *Auth) Handle(req handler.Request) error {
	if !a.server.HasEmail(req.Email) {
		return errors.New("auth: no such account")
	}
	if !a.server.IsValidPassword(req.Email, req.Password) {
		return errors.New("auth: wrong password")
	}

	return a.Successor.Handle(req)
}
```

### `concrete/admin_only.go`

```go
package concrete

import (
	"errors"
	"strings"

	"<module>/<pattern-root>/handler"
	"<module>/<pattern-root>/server"
)

// AdminOnly runs after Auth because roles require an established identity.
type AdminOnly struct {
	handler.Successor
	server *server.Server
}

func NewAdminOnly(server *server.Server) *AdminOnly {
	return &AdminOnly{server: server}
}

func (a *AdminOnly) Handle(req handler.Request) error {
	if strings.HasPrefix(req.Path, "/admin") && !a.server.IsAdmin(req.Email) {
		return errors.New("admin only: not an admin")
	}

	return a.Successor.Handle(req)
}
```

### `main.go`

```go
package main

import (
	"fmt"
	"time"

	"<module>/<pattern-root>/concrete"
	"<module>/<pattern-root>/handler"
	"<module>/<pattern-root>/server"
)

func main() {
	const (
		limit  = 5
		window = 300 * time.Millisecond
	)

	srv := server.New()
	srv.RegisterAdmin("admin@example.com", "admin_pass")
	srv.Register("user@example.com", "user_pass")

	// Keep the head: SetNext returns the step it attached, not the head itself.
	middleware := concrete.NewRateLimit(limit, window)
	middleware.SetNext(concrete.NewAuth(srv)).SetNext(concrete.NewAdminOnly(srv))
	srv.SetMiddleware(middleware)

	requests := []handler.Request{
		{Email: "admin@example.com", Password: "admin_pass", Path: "/admin/settings"},
		{Email: "user@example.com", Password: "user_pass", Path: "/reports"},
		{Email: "user@example.com", Password: "user_pass", Path: "/admin/settings"},
		{Email: "admin@example.com", Password: "wrong_pass", Path: "/reports"},
		{Email: "ghost@example.com", Password: "secret", Path: "/reports"},
		{Email: "admin@example.com", Password: "admin_pass", Path: "/reports"},
	}

	for _, req := range requests {
		page, err := srv.Serve(req)
		if err != nil {
			fmt.Println(req.Path, err)
			continue
		}

		fmt.Println(req.Path, page)
	}
}
```
