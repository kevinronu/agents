## Folder Shape

```text
<pattern-root>/
├── main.go
├── command/
│   ├── command.go
│   └── history.go
├── commands/
│   ├── command_state.go
│   ├── copy.go
│   └── paste.go
└── editor/
    └── editor.go
```

## File-By-File Skeleton

### `command/command.go`

```go
package command

type Command interface {
	Execute() bool
	Undo()
}
```

### `command/history.go`

```go
package command

type History struct {
	commands []Command
}

func (h *History) Push(command Command) {
	h.commands = append(h.commands, command)
}

func (h *History) Pop() Command {
	if h.Empty() {
		return nil
	}

	last := len(h.commands) - 1
	command := h.commands[last]
	h.commands = h.commands[:last]

	return command
}

func (h History) Empty() bool {
	return len(h.commands) == 0
}
```

### `editor/editor.go`

```go
package editor

import "<module>/<pattern-root>/command"

type Editor struct {
	Text      string
	Clipboard string
	Caret     int
	history   command.History
}

func New(text string) *Editor {
	return &Editor{Text: text, Caret: len(text)}
}

func (e *Editor) Execute(command command.Command) {
	if command.Execute() {
		e.history.Push(command)
	}
}

func (e *Editor) Undo() {
	if e.history.Empty() {
		return
	}

	e.history.Pop().Undo()
}
```

### `commands/command_state.go`

```go
package commands

import "<module>/<pattern-root>/editor"

// commandState replaces the shared receiver and backup of an abstract command class.
type commandState struct {
	editor     *editor.Editor
	backupText string
}

func (c *commandState) backup() {
	c.backupText = c.editor.Text
}

func (c *commandState) Undo() {
	c.editor.Text = c.backupText
}
```

### `commands/copy.go`

```go
package commands

import "<module>/<pattern-root>/editor"

type Copy struct {
	commandState
}

func NewCopy(editor *editor.Editor) *Copy {
	return &Copy{commandState: commandState{editor: editor}}
}

func (c *Copy) Execute() bool {
	c.editor.Clipboard = c.editor.Text

	return false
}
```

### `commands/paste.go`

```go
package commands

import "<module>/<pattern-root>/editor"

type Paste struct {
	commandState
}

func NewPaste(editor *editor.Editor) *Paste {
	return &Paste{commandState: commandState{editor: editor}}
}

func (p *Paste) Execute() bool {
	if p.editor.Clipboard == "" {
		return false
	}

	p.backup()
	p.editor.Text = p.editor.Text[:p.editor.Caret] +
		p.editor.Clipboard + p.editor.Text[p.editor.Caret:]
	p.editor.Caret += len(p.editor.Clipboard)

	return true
}
```

`Cut` and other reversible operations use the same embedded state.
Each saves the receiver state before changing it and inherits `Undo`.

### `main.go`

```go
package main

import (
	"<module>/<pattern-root>/commands"
	"<module>/<pattern-root>/editor"
)

func main() {
	document := editor.New("draft")

	document.Execute(commands.NewPaste(document))
	document.Undo()
}
```

## Important Go Details

- Keep the small `Command` contract and its LIFO history together. `Execute` returns whether the receiver should record the operation, so non-reversible commands stay out of undo history.
- Let the receiver own execution, history, and undo. Clients create a command with its receiver, then submit it without learning how history is stored.
- Embed a private state struct in commands that share a receiver and backup. Its `Undo` method is the Go substitute for shared fields and behavior in an abstract command class.
- Give each command a constructor only when it binds a receiver or required state. A command that changes nothing returns `false`; it does not need a compensating undo entry.
- Keep concrete commands focused on one receiver operation. The receiver need not depend on concrete command packages.
