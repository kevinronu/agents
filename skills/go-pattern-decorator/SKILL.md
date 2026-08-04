---
name: go-pattern-decorator
description: "Lightweight Go Decorator file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: decorator`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Decorator in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Decorator

## Purpose

Provide a file-by-file Go skeleton for Decorator.

## Non-Obvious Go Notes

- Put the shared contract in a small `component` package so the concrete component and every wrapper can substitute for one another at the client boundary.
- Keep the wrapped component in a private named field such as `wrappee`; do not embed the interface. If the contract gains a method, named delegation makes incomplete decorators fail to compile instead of silently forwarding that method unchanged.
- Let each decorator implement every contract method explicitly. Transform data before delegation on `Write`, then reverse the transformation after delegation on `Read`.
- Wrapper order is observable: the outer decorator runs first on `Write` and last on `Read`. Construct the stack in the intended order and document it when operations do not commute.
- Use a pointer receiver for the concrete component when it owns mutable state. Stateless decorators or decorators whose fields are immutable after construction can use values.
- Return a constructor error only when configuration must be valid immediately. A codec level can fail on the first `Write`; a cipher key must fail while constructing the decorator.
- If a decorator derives working state from a secret, keep the derived value instead of the secret. For AEAD encryption, prepend the nonce to the ciphertext so `Read` can recover it.
- Propagate errors from the wrapped component unchanged unless the decorator can add useful local context; wrap errors created by its own transformation.

## Folder Shape

```text
<pattern-root>/
├── main.go
├── component/
│   └── data_source.go
├── concrete/
│   └── store.go
└── decorator/
    ├── <decorator-one>.go
    └── <decorator-two>.go
```

## File-By-File Skeleton

### `component/data_source.go`

```go
// Package component defines the contract shared by the store and its decorators.
package component

// DataSource is all the client sees, so a plain store and a full stack can replace each other.
type DataSource interface {
	Write(data []byte) error
	Read() ([]byte, error)
}
```

### `concrete/store.go`

```go
// Package concrete holds the concrete component that decorators wrap.
package concrete

type Store struct {
	data []byte
}

func (s *Store) Write(data []byte) error {
	s.data = data
	return nil
}

func (s *Store) Read() ([]byte, error) {
	return s.data, nil
}
```

### `decorator/<decorator-one>.go`

```go
// Package decorator holds one wrapper for each behavior added to a DataSource.
package decorator

import (
	"bytes"
	"compress/gzip"
	"fmt"
	"io"

	"<module>/<pattern-root>/component"
)

type <decoratorOneName> struct {
	wrappee component.DataSource
	level   int
}

// New<decoratorOneName> only stores the level; the codec validates it on Write.
func New<decoratorOneName>(wrappee component.DataSource, level int) <decoratorOneName> {
	return <decoratorOneName>{wrappee: wrappee, level: level}
}

func compress(data []byte, level int) ([]byte, error) {
	var buf bytes.Buffer
	writer, err := gzip.NewWriterLevel(&buf, level)
	if err != nil {
		return nil, fmt.Errorf("open gzip writer: %w", err)
	}
	if _, err := writer.Write(data); err != nil {
		return nil, fmt.Errorf("write gzip: %w", err)
	}
	if err := writer.Close(); err != nil { // Close writes the gzip footer.
		return nil, fmt.Errorf("close gzip writer: %w", err)
	}

	return buf.Bytes(), nil
}

func (d <decoratorOneName>) Write(data []byte) error {
	transformed, err := compress(data, d.level)
	if err != nil {
		return err
	}

	return d.wrappee.Write(transformed)
}

func decompress(data []byte) ([]byte, error) {
	reader, err := gzip.NewReader(bytes.NewReader(data))
	if err != nil {
		return nil, fmt.Errorf("open gzip reader: %w", err)
	}
	plain, err := io.ReadAll(reader)
	if err != nil {
		return nil, fmt.Errorf("read gzip: %w", err)
	}
	if err := reader.Close(); err != nil {
		return nil, fmt.Errorf("close gzip reader: %w", err)
	}

	return plain, nil
}

func (d <decoratorOneName>) Read() ([]byte, error) {
	data, err := d.wrappee.Read()
	if err != nil {
		return nil, err
	}

	return decompress(data)
}
```

### `decorator/<decorator-two>.go`

```go
package decorator

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"fmt"

	"<module>/<pattern-root>/component"
)

type <decoratorTwoName> struct {
	wrappee component.DataSource
	aead    cipher.AEAD
}

func New<decoratorTwoName>(wrappee component.DataSource, key []byte) (<decoratorTwoName>, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return <decoratorTwoName>{}, fmt.Errorf("new cipher: %w", err)
	}
	aead, err := cipher.NewGCM(block)
	if err != nil {
		return <decoratorTwoName>{}, fmt.Errorf("new GCM: %w", err)
	}

	return <decoratorTwoName>{wrappee: wrappee, aead: aead}, nil
}

func (d <decoratorTwoName>) Write(data []byte) error {
	nonce := make([]byte, d.aead.NonceSize())
	if _, err := rand.Read(nonce); err != nil {
		return fmt.Errorf("read nonce: %w", err)
	}

	return d.wrappee.Write(d.aead.Seal(nonce, nonce, data, nil))
}

func (d <decoratorTwoName>) Read() ([]byte, error) {
	data, err := d.wrappee.Read()
	if err != nil {
		return nil, err
	}
	if len(data) < d.aead.NonceSize() {
		return nil, fmt.Errorf("stored data is shorter than the nonce")
	}

	nonce, ciphertext := data[:d.aead.NonceSize()], data[d.aead.NonceSize():]
	plain, err := d.aead.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		return nil, fmt.Errorf("open ciphertext: %w", err)
	}

	return plain, nil
}
```

### `main.go`

```go
package main

import (
	"compress/gzip"
	"fmt"
	"log"

	"<module>/<pattern-root>/component"
	"<module>/<pattern-root>/concrete"
	"<module>/<pattern-root>/decorator"
)

func main() {
	store := &concrete.Store{}
	first := decorator.New<decoratorOneName>(store, gzip.BestCompression)

	key := []byte("0123456789abcdef0123456789abcdef")
	second, err := decorator.New<decoratorTwoName>(first, key)
	if err != nil {
		log.Fatal(err)
	}

	// The outer decorator transforms first on Write and last on Read.
	var source component.DataSource = second
	if err := source.Write([]byte("hello")); err != nil {
		log.Fatal(err)
	}

	data, err := source.Read()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(string(data))
}
```
