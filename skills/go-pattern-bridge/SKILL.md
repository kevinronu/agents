---
name: go-pattern-bridge
description: "Lightweight Go Bridge file-by-file pattern skeleton. Use primarily when the active `go` skill calls `design-pattern-decision`, receives `Recommended pattern: bridge`, and then loads this skill; also use when the user explicitly asks to implement, scaffold, or inspect Bridge in Go. Contains only the folder shape, file-by-file code skeleton, and the few non-obvious Go adaptations worth preserving."
---

# Go Pattern Skeleton: Bridge

## Purpose

Provide a file-by-file Go skeleton for Bridge.

## Non-Obvious Go Notes

- Keep the implementation interface in its own package so refined abstractions depend on one shared low-level contract instead of concrete renderers or backends.
- Use embedding or composition in the abstraction side to hold the implementation. This is the Go substitute for carrying shared implementation state through an abstract base type.
- Bridge fits when both sides vary independently. If only one side varies, a simpler pattern is usually enough.
- Keep implementation methods small and composable so refined abstractions can assemble different outputs without learning format-specific details.
- Refined abstractions should differ mainly in the content or workflow they compose, not in how they talk to the implementation.

## Folder Shape

```text
<pattern-root>/
├── main.go
├── abstraction/
│   ├── document.go
│   ├── <refined-one>.go
│   └── <refined-two>.go
└── implementation/
    ├── exporter.go
    ├── <implementation-one>.go
    └── <implementation-two>.go
```

## File-By-File Skeleton

### `implementation/exporter.go`

```go
package implementation

// Exporter is the low-level side of the bridge: the primitives abstractions compose with.
type Exporter interface {
	Heading(text string) string
	Field(label, value string) string
}
```

### `implementation/<implementation-one>.go`

```go
package implementation

type <implementationOneName> struct{}

func (<implementationOneName>) Heading(text string) string {
	return "# " + text + "\n"
}

func (<implementationOneName>) Field(label, value string) string {
	return label + "," + value + "\n"
}
```

### `implementation/<implementation-two>.go`

```go
package implementation

type <implementationTwoName> struct{}

func (<implementationTwoName>) Heading(text string) string {
	return "<h1>" + text + "</h1>\n"
}

func (<implementationTwoName>) Field(label, value string) string {
	return "<p><b>" + label + ":</b> " + value + "</p>\n"
}
```

### `abstraction/document.go`

```go
package abstraction

import "<module>/<pattern-root>/implementation"

// Document is the base abstraction: refined documents build on one implementation.
type Document struct {
	Exporter implementation.Exporter
}
```

### `abstraction/<refined-one>.go`

```go
package abstraction

// <refinedOneName> is one refined abstraction with its own content.
type <refinedOneName> struct {
	Document
	Title string
	Date  string
	Total string
}

func (d <refinedOneName>) Export() string {
	return d.Exporter.Heading(d.Title) +
		d.Exporter.Field("Date", d.Date) +
		d.Exporter.Field("Total", d.Total)
}
```

### `abstraction/<refined-two>.go`

```go
package abstraction

// <refinedTwoName> is another refined abstraction that reuses the same implementation primitives.
type <refinedTwoName> struct {
	Document
	Title   string
	Author  string
	Summary string
}

func (d <refinedTwoName>) Export() string {
	return d.Exporter.Heading(d.Title) +
		d.Exporter.Field("Author", d.Author) +
		d.Exporter.Field("Summary", d.Summary)
}
```

### `main.go`

```go
package main

import (
	"fmt"

	"<module>/<pattern-root>/abstraction"
	"<module>/<pattern-root>/implementation"
)

func main() {
	first := abstraction.<refinedOneName>{
		Title: "Invoice 001",
		Date:  "2026-06-10",
		Total: "$50",
	}

	second := abstraction.<refinedTwoName>{
		Title:   "Q1 Report",
		Author:  "Ana",
		Summary: "all good",
	}

	// Swap implementations without changing the refined abstractions.
	for _, exporter := range []implementation.Exporter{
		implementation.<implementationOneName>{},
		implementation.<implementationTwoName>{},
	} {
		first.Exporter = exporter
		second.Exporter = exporter

		fmt.Print(first.Export())
		fmt.Println()
		fmt.Print(second.Export())
		fmt.Println()
	}
}
```
