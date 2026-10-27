# Mediator in Go

Use this shape when several controls have local actions but their cross-control
rules belong in one coordinator. The reference is a spacecraft bridge that
coordinates thrusters, weapons, shields, and a scanner. Keep the typed events,
registration, and guarded coordination; replace the domain names when needed.

## Folder shape

```text
<pattern-root>/
├── main.go
├── mediator/
│   └── mediator.go
├── controls/
│   ├── thruster.go
│   ├── weapons.go
│   ├── shields.go
│   └── scanner.go
└── bridge/
    └── bridge.go
```

`bridge.Bridge` is the concrete mediator, not the Bridge design pattern. The
four control files follow the same component contract; show one fully and add
only the state and local action needed by each additional control.

## File-by-file skeleton

### `mediator/mediator.go`

```go
package mediator

import "slices"

type Mediator interface {
	Register(component Component)
	Notify(sender Component, event Event)
}

type Component interface {
	Type() ComponentType
	SetMediator(mediator Mediator)
}

type ComponentType string

const (
	ThrusterType ComponentType = "thruster"
	WeaponsType  ComponentType = "weapons"
	ShieldsType  ComponentType = "shields"
	ScannerType  ComponentType = "scanner"
)

type Event interface {
	Name() EventName
}

type EventName string

const (
	ThrustSetName      EventName = "SET_THRUST"
	WeaponsToggledName EventName = "TOGGLE_WEAPONS"
	ShieldsToggledName EventName = "TOGGLE_SHIELDS"
	ScanRequestedName  EventName = "RUN_SCAN"
)

type ThrustSet struct{ Percent int }
type WeaponsToggled struct{ Armed bool }
type ShieldsToggled struct{ Up bool }
type ScanRequested struct{}

func (ThrustSet) Name() EventName      { return ThrustSetName }
func (WeaponsToggled) Name() EventName { return WeaponsToggledName }
func (ShieldsToggled) Name() EventName { return ShieldsToggledName }
func (ScanRequested) Name() EventName  { return ScanRequestedName }

var allowedEvents = map[ComponentType][]EventName{
	ThrusterType: {ThrustSetName},
	WeaponsType:  {WeaponsToggledName},
	ShieldsType:  {ShieldsToggledName},
	ScannerType:  {ScanRequestedName},
}

func Allows(component ComponentType, event EventName) bool {
	return slices.Contains(allowedEvents[component], event)
}
```

### `controls/thruster.go`

```go
package controls

import "<module>/<pattern-root>/mediator"

type Thruster struct {
	mediator mediator.Mediator

	Enabled bool
	Thrust  int
}

func NewThruster() *Thruster { return &Thruster{Enabled: true} }

func (t *Thruster) SetMediator(m mediator.Mediator) { t.mediator = m }

func (t *Thruster) Type() mediator.ComponentType { return mediator.ThrusterType }

func (t *Thruster) Enable()  { t.Enabled = true }
func (t *Thruster) Disable() { t.Enabled = false }

func (t *Thruster) SetThrust(percent int) {
	if !t.Enabled {
		return
	}

	t.Thrust = min(100, max(0, percent))
	if t.mediator != nil {
		t.mediator.Notify(t, mediator.ThrustSet{Percent: t.Thrust})
	}
}
```

Implement the remaining components with the same `mediator` field,
`SetMediator`, and `Type` methods. Preserve their local state and originating
event: `Weapons.ToggleArm` emits `WeaponsToggled`, `Shields.ToggleShields`
emits `ShieldsToggled`, and `Scanner.RequestScan` emits `ScanRequested`.
`Scanner.Run` is a local operation the bridge calls after deciding a scan is
allowed; it does not emit another event.

### `bridge/bridge.go`

```go
package bridge

import (
	"<module>/<pattern-root>/controls"
	"<module>/<pattern-root>/mediator"
)

const safeThrust = 60

type Bridge struct {
	thruster *controls.Thruster
	weapons  *controls.Weapons
	shields  *controls.Shields
	scanner  *controls.Scanner
}

func New(components ...mediator.Component) *Bridge {
	bridge := &Bridge{}
	for _, component := range components {
		bridge.Register(component)
	}

	return bridge
}

func (b *Bridge) Register(component mediator.Component) {
	component.SetMediator(b)

	switch control := component.(type) {
	case *controls.Thruster:
		b.thruster = control
	case *controls.Weapons:
		b.weapons = control
	case *controls.Shields:
		b.shields = control
	case *controls.Scanner:
		b.scanner = control
	}
}

func (b *Bridge) Notify(sender mediator.Component, event mediator.Event) {
	if !mediator.Allows(sender.Type(), event.Name()) {
		return
	}

	switch event := event.(type) {
	case mediator.ThrustSet:
		b.dropShieldsAtHighThrust(event.Percent)
		b.capThrustWhileArmed(event.Percent)
	case mediator.WeaponsToggled:
		if event.Armed {
			b.capThrustWhileArmed(b.thruster.Thrust)
		}
	case mediator.ShieldsToggled:
		b.followShields(event.Up)
	case mediator.ScanRequested:
		b.runScan()
	}
}

func (b *Bridge) dropShieldsAtHighThrust(thrust int) {
	if thrust <= 80 {
		return
	}

	b.shields.Up = false
	b.shields.Disable()
}

func (b *Bridge) capThrustWhileArmed(thrust int) {
	if !b.weapons.Armed || thrust <= safeThrust {
		return
	}

	// Do not call SetThrust: it would emit a second event and re-enter Notify.
	b.thruster.Thrust = safeThrust
}

func (b *Bridge) followShields(up bool) {
	if !up {
		b.runScan()
		return
	}

	if b.weapons.Armed {
		b.weapons.Armed = false
	}
}

func (b *Bridge) runScan() {
	if !b.scanner.Enabled {
		return
	}

	b.thruster.Disable()
	b.scanner.Run()
	b.thruster.Enable()
}
```

Keep cross-control rules in `Bridge`; controls should only validate and mutate
their own local state, then notify their mediator.

### `main.go`

```go
package main

import (
	"<module>/<pattern-root>/bridge"
	"<module>/<pattern-root>/controls"
)

func main() {
	thruster := controls.NewThruster()
	weapons := controls.NewWeapons()
	shields := controls.NewShields()
	scanner := controls.NewScanner()

	bridge.New(thruster, weapons, shields, scanner)

	thruster.SetThrust(90)
	weapons.ToggleArm()
	shields.ToggleShields()
	scanner.RequestScan()
}
```

Construction registers every control before it performs an action. Clients
operate controls normally; the controls do not call one another directly.

## Important Go Details

- Put `Mediator`, `Component`, identifiers, events, and event validation in one
  shared package. Controls and the concrete mediator can then import that
  package without importing each other.
- Give each event its own struct and a common `Name` method. The mediator gets
  typed event data through a type switch instead of asserting an untyped
  payload.
- `Register` both injects the mediator into each component and stores the
  concrete pointer the coordinator needs to apply cross-component rules.
- A component can construct another component's event in Go, so validate the
  component/event pairing before reacting.
- Public component actions notify the mediator. When a mediator reaction must
  change component state, write the field directly (or use a non-notifying
  internal operation) rather than calling the public action again; otherwise
  it re-enters `Notify`.
