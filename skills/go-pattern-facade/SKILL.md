---
name: go-pattern-facade
description: "Lightweight Go Facade file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: facade`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Facade in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Facade

## Purpose

Provide a file-by-file Go skeleton for Facade.

## Non-Obvious Go Notes

- Keep the subsystem in its own package. The facade imports and orders its parts; subsystem types do not import the facade or know the whole workflow.
- Let the facade own stateless subsystem values directly. Zero-value structs need no constructor or dependency wiring when their behavior has no configuration.
- Put repeated prerequisite selection in a private helper returning one small result struct. This prevents public facade methods such as `Check` and `Convert` from drifting apart.
- Use a distinct intermediate type for a workflow stage when it prevents invalid call order. A decoded `Raw` value can flow through processing and encoding without allowing callers to encode an unprocessed file by mistake.
- A facade is a shortcut, not a wall: retain useful subsystem errors and leave direct subsystem access possible when callers genuinely need lower-level control.

## Folder Shape

```text
<pattern-root>/
├── main.go
├── facade/
│   └── converter.go
└── subsystem/
    ├── asset.go
    ├── codec.go
    ├── enhancer.go
    └── transcoder.go
```

## File-By-File Skeleton

### `subsystem/asset.go`

```go
// Package subsystem holds the parts that do the real work.
package subsystem

import (
	"path/filepath"
	"strings"
)

// Asset is the input and output owned by the subsystem.
type Asset struct {
	Name  string
	Bytes int64
}

func (a Asset) Format() string {
	return strings.TrimPrefix(filepath.Ext(a.Name), ".")
}

func (a Asset) BaseName() string {
	return strings.TrimSuffix(a.Name, filepath.Ext(a.Name))
}
```

### `subsystem/codec.go`

```go
package subsystem

import "fmt"

// Codec is one format supported by the subsystem.
type Codec struct {
	Format string
	Ratio  int
}

var codecs = map[string]Codec{
	"<format-one>": {Format: "<format-one>", Ratio: 12},
	"<format-two>": {Format: "<format-two>", Ratio: 20},
}

func CodecFor(format string) (Codec, error) {
	codec, ok := codecs[format]
	if !ok {
		return Codec{}, fmt.Errorf("no codec for format %q", format)
	}

	return codec, nil
}
```

### `subsystem/transcoder.go`

```go
package subsystem

// Raw is the intermediate representation accepted only by processing and encoding stages.
type Raw struct {
	Bytes int64
}

// Transcoder has no state, so the facade can keep its zero value.
type Transcoder struct{}

func (Transcoder) Decode(asset Asset, codec Codec) Raw {
	return Raw{Bytes: asset.Bytes * int64(codec.Ratio)}
}

func (Transcoder) Encode(raw Raw, codec Codec, baseName string) Asset {
	return Asset{
		Name:  baseName + "." + codec.Format,
		Bytes: raw.Bytes / int64(codec.Ratio),
	}
}
```

### `subsystem/enhancer.go`

```go
package subsystem

// Enhancer works on Raw, so it can only run between decoding and encoding.
type Enhancer struct{}

func (Enhancer) Process(raw Raw) Raw {
	return Raw{Bytes: raw.Bytes * 95 / 100}
}
```

### `facade/converter.go`

```go
// Package facade holds the only type the client needs for the common workflow.
package facade

import (
	"fmt"

	"<module>/<pattern-root>/subsystem"
)

// Converter owns the stateless subsystem parts needed by the shortcut workflow.
type Converter struct {
	transcoder subsystem.Transcoder
	enhancer   subsystem.Enhancer
}

// codecPair keeps source and target lookup shared by the public facade methods.
type codecPair struct {
	source subsystem.Codec
	target subsystem.Codec
}

func codecsFor(asset subsystem.Asset, targetFormat string) (codecPair, error) {
	source, err := subsystem.CodecFor(asset.Format())
	if err != nil {
		return codecPair{}, fmt.Errorf("source codec: %w", err)
	}

	target, err := subsystem.CodecFor(targetFormat)
	if err != nil {
		return codecPair{}, fmt.Errorf("target codec: %w", err)
	}

	return codecPair{source: source, target: target}, nil
}

// Check validates both ends without starting the full workflow.
func (Converter) Check(asset subsystem.Asset, targetFormat string) error {
	_, err := codecsFor(asset, targetFormat)
	return err
}

// Convert hides the subsystem sequence while preserving its errors.
func (c Converter) Convert(asset subsystem.Asset, targetFormat string) (subsystem.Asset, error) {
	pair, err := codecsFor(asset, targetFormat)
	if err != nil {
		return subsystem.Asset{}, err
	}

	raw := c.transcoder.Decode(asset, pair.source)
	return c.transcoder.Encode(c.enhancer.Process(raw), pair.target, asset.BaseName()), nil
}
```

### `main.go`

```go
package main

import (
	"fmt"
	"log"

	"<module>/<pattern-root>/facade"
	"<module>/<pattern-root>/subsystem"
)

func main() {
	asset := subsystem.Asset{Name: "input.<format-one>", Bytes: 614_400}
	var converter facade.Converter // Its zero value owns zero-value subsystem parts.

	if err := converter.Check(asset, "<format-two>"); err != nil {
		log.Fatal(err)
	}

	result, err := converter.Convert(asset, "<format-two>")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(result.Name, result.Bytes)
}
```
