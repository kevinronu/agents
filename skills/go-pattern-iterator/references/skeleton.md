# Iterator in Go

Use this shape when a client needs to traverse related values without knowing
how a concrete source stores or retrieves them. The reference implementation
models profiles from two social networks; preserve the sequence contract and
replace that domain only when the task calls for another one.

## Important Go details

- `iter.Seq[T]` is consumed with `for value := range sequence`. Its function
  receives a `yield` callback; return as soon as `yield` returns `false`, so a
  caller's `break` stops work upstream.
- Use `iter.Pull` only when a caller must manually pause and resume. The
  returned `stop` function releases the iterator early, so expose it and call
  it with `defer` when the sequence might not be exhausted.
- When looking up a pointer in `[]Profile`, range over indices and return
  `&profiles[index]`. A range value is a copy, so `&profile` would not point to
  the element in the slice.
- Keep clients dependent on `SocialNetwork`, not on a concrete source. Each
  source may differ internally while yielding the same profiles.
- A lookup can yield `nil` for a configured contact that is no longer present.
  Consumers that dereference profiles must intentionally skip it.

## Folder shape

```text
<pattern-root>/
├── main.go
├── aggregate/
│   ├── aggregate.go
│   ├── <network-one>.go
│   └── <network-two>.go
├── client/
│   ├── social_spammer.go
│   └── profile_reviewer.go
└── item/
    └── profile.go
```

`<network-one>` and `<network-two>` are separate concrete sources (for example,
Facebook and LinkedIn). They implement the same interface. Show one complete
implementation, then repeat its public behavior for the other source while
allowing its storage or lookup details to vary.

## File-by-file skeleton

### `item/profile.go`

```go
package item

type ContactType string

const (
	Friend   ContactType = "friends"
	Coworker ContactType = "coworkers"
)

type Profile struct {
	Email    string
	Name     string
	Contacts map[ContactType][]string
}
```

The reference also has a constructor that parses contacts such as
`"friends:alex@example.com"`; parsing is incidental. Keep it only if the
incoming data has that compact format.

### `aggregate/aggregate.go`

```go
// Package aggregate defines sources whose results can be ranged over.
package aggregate

import (
	"iter"

	"<module>/<pattern-root>/item"
)

// SocialNetwork hides the concrete network and its lookup mechanism.
type SocialNetwork interface {
	FriendsFor(profileEmail string) iter.Seq[*item.Profile]
	CoworkersFor(profileEmail string) iter.Seq[*item.Profile]
}
```

### `aggregate/<network-one>.go`

```go
package aggregate

import (
	"iter"

	"<module>/<pattern-root>/item"
)

type <networkOneName> struct {
	profiles []item.Profile
}

func New<networkOneName>(profiles []item.Profile) *<networkOneName> {
	return &<networkOneName>{profiles: profiles}
}

// requestProfile returns the element itself, not the copy produced by range.
func (n *<networkOneName>) requestProfile(email string) *item.Profile {
	for index := range n.profiles {
		if n.profiles[index].Email == email {
			return &n.profiles[index]
		}
	}

	return nil
}

func (n *<networkOneName>) requestProfileContactEmails(
	email string,
	contactType item.ContactType,
) []string {
	profile := n.requestProfile(email)
	if profile == nil {
		return nil
	}

	return profile.Contacts[contactType]
}

// profileSeqFor is below its lookup dependencies and above its public callers.
func (n *<networkOneName>) profileSeqFor(
	email string,
	contactType item.ContactType,
) iter.Seq[*item.Profile] {
	return func(yield func(*item.Profile) bool) {
		contactEmails := n.requestProfileContactEmails(email, contactType)
		for _, contactEmail := range contactEmails {
			contact := n.requestProfile(contactEmail)
			keepGoing := yield(contact)
			if !keepGoing {
				return
			}
		}
	}
}

func (n *<networkOneName>) FriendsFor(email string) iter.Seq[*item.Profile] {
	return n.profileSeqFor(email, item.Friend)
}

func (n *<networkOneName>) CoworkersFor(email string) iter.Seq[*item.Profile] {
	return n.profileSeqFor(email, item.Coworker)
}
```

The second network implements the same two public methods. Do not expose its
storage or network-specific request work through `SocialNetwork`.

### `client/social_spammer.go`

```go
// Package client consumes profile sequences through the aggregate contract.
package client

import (
	"fmt"
	"iter"

	"<module>/<pattern-root>/aggregate"
	"<module>/<pattern-root>/item"
)

type SocialSpammer struct {
	network aggregate.SocialNetwork
}

func New(network aggregate.SocialNetwork) SocialSpammer {
	return SocialSpammer{network: network}
}

func (s SocialSpammer) SendToFriends(profileEmail, message string) {
	s.send(s.network.FriendsFor(profileEmail), message)
}

func (s SocialSpammer) SendToCoworkers(profileEmail, message string) {
	s.send(s.network.CoworkersFor(profileEmail), message)
}

func (SocialSpammer) send(profiles iter.Seq[*item.Profile], message string) {
	for profile := range profiles {
		if profile == nil {
			continue
		}

		fmt.Printf("Sent %q to %s (%s)\n", message, profile.Name, profile.Email)
	}
}
```

### `client/profile_reviewer.go`

```go
package client

import (
	"iter"

	"<module>/<pattern-root>/item"
)

// ProfileReviewer is for a UI or workflow that advances one profile at a time.
type ProfileReviewer struct {
	Next func() (*item.Profile, bool)
	Stop func()
}

func NewProfileReviewer(profiles iter.Seq[*item.Profile]) *ProfileReviewer {
	next, stop := iter.Pull(profiles)
	return &ProfileReviewer{Next: next, Stop: stop}
}
```

### `main.go`

```go
package main

import (
	"fmt"

	"<module>/<pattern-root>/aggregate"
	"<module>/<pattern-root>/client"
	"<module>/<pattern-root>/item"
)

func main() {
	profiles := []item.Profile{
		{
			Email: "ana@example.com",
			Name:  "Ana",
			Contacts: map[item.ContactType][]string{
				item.Friend: []string{"max@example.com"},
			},
		},
		{Email: "max@example.com", Name: "Max"},
	}

	network := aggregate.New<networkOneName>(profiles)
	spammer := client.New(network)
	spammer.SendToFriends("ana@example.com", "Hello!")

	// Pull iteration lets this workflow pause after each call to Next.
	reviewer := client.NewProfileReviewer(network.FriendsFor("ana@example.com"))
	defer reviewer.Stop()

	if profile, ok := reviewer.Next(); ok && profile != nil {
		fmt.Println("Reviewing", profile.Email)
	}
}
```

Use `range` for the normal bulk-processing path. Keep `ProfileReviewer` only
when its explicit pause/resume behavior is part of the requirement.
