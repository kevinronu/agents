---
name: go-pattern-adapter
description: "Lightweight Go Adapter file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: adapter`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Adapter in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Adapter

## Purpose

Provide a file-by-file Go skeleton for Adapter.

## Non-Obvious Go Notes

- Keep the interface the client expects in a small `target` package so the rest of the code depends on that contract, not on vendor or legacy APIs.
- Keep the client in its own `client` package. This makes the roles explicit: `target` defines the expected shape, while `client` consumes only that shape.
- Let backends that already match the target implement it directly. Only incompatible backends need adapters.
- Keep the adapter focused on translation: input shape, output shape, units, names, and error mapping. Do not move business policy into the adapter.
- If the adaptee is not yours to change, model it in a separate package so the adapter boundary stays explicit.
- Prefer one adapter per incompatible backend or protocol instead of one large adapter that branches on many backend shapes.

## Folder Shape

```text
<pattern-root>/
├── main.go
├── adaptee/
│   └── <legacy-service>.go
├── adapter/
│   └── <legacy-adapter>.go
├── client/
│   └── service.go
├── native/
│   └── service.go
└── target/
    └── processor.go
```

## File-By-File Skeleton

### `target/processor.go`

```go
// Package target defines the interface the client depends on.
package target

// PaymentProcessor is the target interface. Native backends and adapters both reach it.
type PaymentProcessor interface {
	Pay(amountCents int) (string, error)
}
```

### `client/service.go`

```go
// Package client holds code that works only through the target interface.
package client

import "<module>/<pattern-root>/target"

// PaymentService is the client: it depends only on the target interface.
type PaymentService struct {
	Processor target.PaymentProcessor
}

// Buy behaves the same whether the processor is native or adapted.
func (s PaymentService) Buy(amountCents int) (string, error) {
	return s.Processor.Pay(amountCents)
}
```

### `native/service.go`

```go
// Package native holds a backend that already satisfies the target.
package native

import "fmt"

// Service already speaks the target contract, so it needs no adapter.
type Service struct{}

// Pay already matches the target signature, so nothing is translated here.
func (Service) Pay(amountCents int) (string, error) {
	return fmt.Sprintf("paid $%.2f via native service", float64(amountCents)/100), nil
}
```

### `adaptee/<legacy-service>.go`

```go
// Package adaptee holds existing code whose API you cannot change.
package adaptee

// <legacyServiceName> is useful existing code whose API does not match the target.
type <legacyServiceName> struct{}

// Charge's dollars-and-bool shape is the mismatch the adapter absorbs.
func (<legacyServiceName>) Charge(dollars float64) bool {
	return dollars > 0
}
```

### `adapter/<legacy-adapter>.go`

```go
// Package adapter translates between the adaptee and the target.
package adapter

import (
	"errors"
	"fmt"

	"<module>/<pattern-root>/adaptee"
)

// <legacyAdapterName> connects the adaptee to the target.
type <legacyAdapterName> struct {
	Adaptee adaptee.<legacyServiceName>
}

// Pay translates the call and result between the target and the adaptee API.
func (a <legacyAdapterName>) Pay(amountCents int) (string, error) {
	dollars := float64(amountCents) / 100

	if !a.Adaptee.Charge(dollars) {
		return "", errors.New("legacy service declined the payment")
	}

	return fmt.Sprintf("paid $%.2f via legacy service", dollars), nil
}
```

### `main.go`

```go
package main

import (
	"fmt"
	"log"

	"<module>/<pattern-root>/adaptee"
	"<module>/<pattern-root>/adapter"
	"<module>/<pattern-root>/client"
	"<module>/<pattern-root>/native"
)

func main() {
	// A backend that already fits the target is used directly.
	nativePayment := client.PaymentService{
		Processor: native.Service{},
	}

	receipt, err := nativePayment.Buy(1999)
	if err != nil {
		log.Fatalf("native payment: %v", err)
	}

	fmt.Println("no adapter:", receipt)

	// A backend whose API does not match the target needs an adapter.
	legacyPayment := client.PaymentService{
		Processor: adapter.<legacyAdapterName>{
			Adaptee: adaptee.<legacyServiceName>{},
		},
	}

	receipt, err = legacyPayment.Buy(2500)
	if err != nil {
		log.Fatalf("legacy payment: %v", err)
	}

	fmt.Println("via adapter:", receipt)
}
```
