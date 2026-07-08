---
name: go-pattern-adapter
description: "Lightweight Go Adapter file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: adapter`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Adapter in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Adapter

## Purpose

Provide a file-by-file Go skeleton for Adapter.

## Non-Obvious Go Notes

- Keep the client-owned contract in a small `port` or `target` package so the rest of the code depends on the interface the client expects, not on vendor or legacy APIs.
- Keeping the client in `target` and the contract in `port` makes ownership explicit: the client owns the abstraction even when adapters live elsewhere.
- Let backends that already match the port implement it directly. Only incompatible backends need adapters.
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
├── native/
│   └── service.go
├── port/
│   └── processor.go
└── target/
    └── service.go
```

## File-By-File Skeleton

### `port/processor.go`

```go
package port

// PaymentProcessor is the client-owned port. Native backends and adapters plug in behind it.
type PaymentProcessor interface {
	Pay(amountCents int) (string, error)
}
```

### `target/service.go`

```go
package target

import "<module>/<pattern-root>/port"

// PaymentService is the client: it depends only on the port.
type PaymentService struct {
	Processor port.PaymentProcessor
}

func (s PaymentService) Buy(amountCents int) (string, error) {
	return s.Processor.Pay(amountCents)
}
```

### `native/service.go`

```go
package native

import "fmt"

type Service struct{}

func (Service) Pay(amountCents int) (string, error) {
	return fmt.Sprintf("paid $%.2f via native service", float64(amountCents)/100), nil
}
```

### `adaptee/<legacy-service>.go`

```go
package adaptee

// <legacyServiceName> is useful existing code whose API does not match the port.
type <legacyServiceName> struct{}

func (<legacyServiceName>) Charge(dollars float64) bool {
	return dollars > 0
}
```

### `adapter/<legacy-adapter>.go`

```go
package adapter

import (
	"errors"
	"fmt"

	"<module>/<pattern-root>/adaptee"
)

// <legacyAdapterName> connects the adaptee to the client-owned port.
type <legacyAdapterName> struct {
	Adaptee adaptee.<legacyServiceName>
}

// Pay translates the call and result between the port and the adaptee API.
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
	"<module>/<pattern-root>/native"
	"<module>/<pattern-root>/target"
)

func main() {
	// A backend that already fits the port is used directly.
	nativePayment := target.PaymentService{
		Processor: native.Service{},
	}

	receipt, err := nativePayment.Buy(1999)
	if err != nil {
		log.Fatalf("native payment: %v", err)
	}

	fmt.Println("no adapter:", receipt)

	// A backend whose API does not match the port needs an adapter.
	legacyPayment := target.PaymentService{
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
