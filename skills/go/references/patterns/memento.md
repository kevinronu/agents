# Memento in Go

Use this layout when an originator must restore prior state without exposing its
internal representation to its history. The reference is a text editor with
commands, undo, and redo; retain the snapshot ownership and history cursor,
while replacing editor-specific operations when appropriate.

## Folder shape

```text
<pattern-root>/
├── main.go
├── memento/
│   └── memento.go
├── command/
│   └── command.go
├── commands/
│   ├── <mutating-command>.go
│   └── <non-undoable-command>.go
├── originator/
│   ├── originator.go
│   ├── state.go
│   ├── editor.go
│   └── editor_memento.go
└── caretaker/
    └── history.go
```

The `memento` package exposes only restoration. `caretaker` records that
interface, while `originator` remains the only package that owns the concrete
snapshot state.

## File-by-file skeleton

### `memento/memento.go`

```go
package memento

type Memento interface {
	Restore()
}
```

### `command/command.go`

```go
package command

type Command interface {
	Name() Name
	Execute()
	// Undoable says whether this command changes state that history should restore.
	Undoable() bool
}

type Name string
```

### `originator/originator.go` and `originator/state.go`

```go
package originator

import "slices"

type Originator interface {
	State() State
	SetState(state State)
}

type Range struct {
	Start int
	End   int
}

type State struct {
	Content        string
	Cursor         int
	SelectionStart int
	SelectionEnd   int
	Clipboard      string
	Bold           []Range
}

// Clone copies reference fields so a snapshot cannot share mutable data.
func (s State) Clone() State {
	s.Bold = slices.Clone(s.Bold)
	return s
}
```

### `originator/editor_memento.go`

```go
package originator

type EditorMemento struct {
	editor Originator
	state  State
}

func NewEditorMemento(editor Originator) *EditorMemento {
	return &EditorMemento{editor: editor, state: editor.State()}
}

func (m *EditorMemento) Restore() {
	m.editor.SetState(m.state)
}
```

### `caretaker/history.go`

```go
package caretaker

import (
	"<module>/<pattern-root>/command"
	"<module>/<pattern-root>/memento"
)

type Checkpoint struct {
	Command command.Command
	Memento memento.Memento
}

// History retains undone checkpoints for redo. applied is the next undo index.
type History struct {
	checkpoints []Checkpoint
	applied     int
}

func (h *History) Push(checkpoint Checkpoint) {
	if h.applied != len(h.checkpoints) {
		h.checkpoints = h.checkpoints[:h.applied]
	}

	h.checkpoints = append(h.checkpoints, checkpoint)
	h.applied = len(h.checkpoints)
}

func (h *History) Undo() bool {
	if h.applied == 0 {
		return false
	}

	h.applied--
	h.checkpoints[h.applied].Memento.Restore()
	return true
}

func (h *History) Redo() bool {
	if h.applied == len(h.checkpoints) {
		return false
	}

	checkpoint := h.checkpoints[h.applied]
	h.applied++
	checkpoint.Memento.Restore()
	checkpoint.Command.Execute()
	return true
}
```

### `originator/editor.go`

```go
package originator

import (
	"<module>/<pattern-root>/caretaker"
	"<module>/<pattern-root>/command"
)

type Editor struct {
	state   State
	history caretaker.History
}

func NewEditor(content string) *Editor {
	position := len(content)
	return &Editor{state: State{
		Content:        content,
		Cursor:         position,
		SelectionStart: position,
		SelectionEnd:   position,
	}}
}

func (e *Editor) State() State {
	return e.state.Clone()
}

func (e *Editor) SetState(state State) {
	e.state = state.Clone()
}

func (e *Editor) Execute(command command.Command) {
	if command.Undoable() {
		// Snapshot the state the command is about to replace.
		e.history.Push(caretaker.Checkpoint{
			Command: command,
			Memento: NewEditorMemento(e),
		})
	}

	command.Execute()
}

func (e *Editor) Undo() bool { return e.history.Undo() }
func (e *Editor) Redo() bool { return e.history.Redo() }
```

### `commands/<mutating-command>.go`

```go
package commands

import (
	"slices"

	"<module>/<pattern-root>/command"
	"<module>/<pattern-root>/originator"
)

const ToggleBoldName command.Name = "TOGGLE_BOLD"

type ToggleBold struct {
	editor originator.Originator
}

func NewToggleBold(editor originator.Originator) *ToggleBold {
	return &ToggleBold{editor: editor}
}

func (t *ToggleBold) Name() command.Name { return ToggleBoldName }
func (t *ToggleBold) Undoable() bool      { return true }

func (t *ToggleBold) Execute() {
	state := t.editor.State()
	if state.SelectionStart == state.SelectionEnd {
		return
	}

	selection := originator.Range{Start: state.SelectionStart, End: state.SelectionEnd}
	if bolded := slices.Index(state.Bold, selection); bolded >= 0 {
		state.Bold = slices.Delete(state.Bold, bolded, bolded+1)
	} else {
		state.Bold = append(state.Bold, selection)
	}

	t.editor.SetState(state)
}
```

Non-mutating commands, such as moving a caret or selecting a range, return
`false` from `Undoable`; they execute normally but do not create checkpoints.

### `main.go`

```go
package main

import (
	"<module>/<pattern-root>/commands"
	"<module>/<pattern-root>/originator"
)

func main() {
	editor := originator.NewEditor("Hello world")
	editor.Execute(commands.NewToggleBold(editor))

	editor.Undo()
	editor.Redo()
}
```

## Important Go Details

- Snapshot before executing an undoable command. The memento must describe the
  state the command is about to replace, not the state after it has changed.
- `State` and `SetState` both clone mutable reference fields. Copying a struct
  with a slice only copies its header, so without `slices.Clone` a snapshot and
  the live editor could mutate the same backing array.
- Keep the concrete `EditorMemento` in `originator`; `History` only knows the
  narrow `memento.Memento` interface and cannot inspect snapshot state.
- `applied` separates the applied prefix from the redoable suffix. A new
  checkpoint after undo truncates that suffix, because it starts a new history
  branch.
- Redo restores the checkpoint before re-executing its command. This makes the
  command run from the same pre-command state it had originally.
- Commands that do not mutate state should not enter memento history. Their
  `Undoable` result makes that policy explicit without coupling history to
  concrete command types.
