---
name: design-pattern-decision
description: Internal design-pattern classifier. Use primarily when another active language skill invokes this skill with a plan, tentative code, current code, or intended change to classify; also use when the user explicitly asks which design pattern fits or whether no formal pattern should be used. Return only the classification. Do not trigger this skill just because the codebase contains pattern-related code; a language skill must invoke it, and that language skill keeps ownership of routing and follow-up.
---

# Design Pattern Decision

## Purpose

Act as a language-agnostic design-pattern classifier for a received plan, tentative code, current code, or proposed change.

Use this skill only to answer:

- Which design pattern fits?
- Should the answer be `none`?

Use this skill primarily when another skill explicitly asks for classification. Also use it when the user explicitly asks for that classification. Do not trigger it from general code inspection alone.

This skill does not route to other skills, implement changes, validate code, or decide language-specific structure.

## Input Contract

Use the available code context. If the caller has not made this explicit, reconstruct it from the user request and files already inspected.

```text
User request:
Language:
Relevant files, package, module, or component:
Existing local conventions:
Plan, tentative code, or current code summary:
Abstractions being considered or already present:
Variation points:
Expected future cases:
Testing impact:
```

Set `Language` to the lowercase base skill name, such as `go`, `typescript`, or `html-css`.

Do not ask the user for this template if the information can be inferred from local code.

## Output Contract

Return only the design-pattern classification:

```text
Recommended pattern: none | singleton | builder | factory-method | abstract-factory | prototype | adapter | facade | decorator | proxy | composite | flyweight | bridge | chain-of-responsibility | command | strategy | state | observer | memento | mediator | visitor | iterator | template-method
Primary pain:
Evidence in code:
Selected family: none | creational | structural | behavioral
Why this pattern fits:
Rejected alternatives:
Risk if misapplied:
```

Return `Recommended pattern` exactly as one of the lowercase hyphen-case values in the template so orchestrating skills can map it directly to language-specific skills.

If evidence is weak, choose `none`. Name the future signal that would justify revisiting the classification.

## Core Rule

Prefer the least powerful design that solves the observed pain.

Design patterns fit when they reduce a recurring cost in a controlled place. Do not recommend one because the pattern is familiar, because the code already resembles it, or because a future extension is merely possible.

## Recommend None When

- The change is one-off.
- The abstraction would have only one implementation and no concrete near-term variation.
- A direct function, method, struct, helper, plain object, or existing local convention is clearer.
- The pattern would hide dependencies, control flow, network calls, storage calls, or mutable state.
- The pattern would make tests harder to read.
- The proposed pattern does not match an actual pain in the code.
- The caller cannot explain what cost the pattern would reduce.

## Root Decision Tree

Ask: where is the pain coming from?

- Object creation is becoming complex: use the creational branch.
- Objects, modules, or components do not fit together cleanly: use the structural branch.
- Behavior changes across cases or over time: use the behavioral branch.
- None of these: do not use a formal design pattern.

## Creational Branch

Use this branch when construction logic is the problem: repeated setup, too many parameters, unclear defaults, valid combinations, expensive initialization, or scattered decisions about which implementation to create.

### Singleton

Choose only when exactly one process-wide shared instance is truly required.

Use when:

- the object is stateless or immutable after setup
- sharing is explicit and harmless
- lifecycle is genuinely process-wide

Be careful when:

- the real motivation is easy access
- the object stores request state or mutable state
- tests would need global reset hooks

Prefer explicit wiring or dependency injection when controlled construction is the real need.

### Builder

Choose when construction is complex or easy to misuse.

Use when:

- constructors or config structs have many optional values
- valid combinations matter
- defaults and presets should be explicit
- validation should happen before the object is used

Be careful when:

- the object has only a few required fields
- normal constructors, options, or config structs are clearer in the active language

### Factory Method

Choose when creation of concrete implementations should be centralized behind a stable contract.

Use when:

- creation branches on provider, file type, country, document type, feature flag, environment, or config
- callers should not know concrete types
- adding an implementation should not modify every caller

Be careful when:

- there is only one implementation
- the factory only renames a constructor

### Abstract Factory

Choose when a family of related objects must be selected together.

Use when:

- provider-specific clients, mappers, validators, parsers, serializers, or formatters must match
- mixing objects from different families would be invalid

Be careful when:

- only one object varies
- Strategy, Adapter, or a simple factory is enough

### Prototype

Choose when cloning an existing configured object is cheaper, safer, or clearer than rebuilding it.

Use when:

- initialization is expensive
- configuration is deep or repetitive
- new instances start from known templates

Be careful when:

- copying creates ambiguous ownership
- shared mutable state could leak between instances

## Structural Branch

Use this branch when boundaries are awkward: external shapes leak into domain code, subsystem usage requires too many steps, optional responsibilities create variant explosions, or composition is hard to manage.

### Adapter

Choose when internal code expects one interface and an external, legacy, or infrastructure dependency exposes another.

Use when:

- vendor-specific fields, names, errors, or request shapes are spreading
- translation code is duplicated
- tests need a stable internal contract

Keep adapters focused on translation. Move business rules out of adapters.

### Facade

Choose when a subsystem is too complex to use correctly.

Use when:

- callers must remember a multi-step sequence
- low-level APIs are called inconsistently
- the safe path should be one entry point

Be careful when:

- the facade would hide important choices
- it would become a catch-all service

### Decorator

Choose when optional responsibilities should be composed without subclass or variant explosion.

Use when:

- combinations such as logging, caching, compression, encryption, metrics, retries, or tracing should be layered
- each wrapper can stay small and predictable

Be careful when:

- wrapper order is unclear
- wrappers depend on each other's internals

### Proxy

Choose when a stand-in should control access to another object or service.

Use when:

- lazy loading, caching, access control, instrumentation, or remote calls need a local-looking contract

Be careful when:

- direct calls are clearer
- the proxy would hide costly network, storage, or authorization behavior

### Composite

Choose when the domain is a tree and leaf nodes and containers should be treated uniformly.

Use when:

- nested content, UI trees, file-system-like structures, or recursive operations are central to the model

Be careful when:

- the hierarchy is incidental or shallow

### Flyweight

Choose when many objects share identical data and duplication has a meaningful memory cost.

Use when:

- repeated immutable state can be shared safely
- memory pressure is proven or very likely
- the code resembles editors, renderers, parsers, simulations, or large in-memory models

Be careful in ordinary application code unless memory cost is part of the problem.

### Bridge

Choose when abstraction and implementation must vary independently.

Use when:

- two dimensions of change are creating a matrix of subclasses, structs, components, or conditionals
- examples include export format vs export destination, device type vs control type, or channel vs provider

Be careful when:

- only one dimension varies
- Strategy or Adapter captures the actual pain more directly

## Behavioral Branch

Use this branch when rules, algorithms, workflows, or state-dependent behavior are becoming hard to extend.

### Chain Of Responsibility

Choose when requests pass through a sequence of independent steps.

Use when:

- the solution is middleware-like
- each step may stop or continue processing
- order matters and each step has one responsibility

Be careful when:

- handlers mutate shared state unpredictably
- handlers depend on each other's internals
- direct orchestration is shorter and clearer

### Command

Choose when actions should be represented as values or objects.

Use when:

- actions need queueing, retries, audit logs, delayed execution, replay, or undo

Be careful when:

- a direct function call is enough

### Strategy

Choose when callers should stay stable while algorithms or policies vary.

Use when:

- branching recurs by plan, provider, channel, country, document type, status, or feature flag
- multiple implementations perform the same role
- adding a case should not modify the caller
- tests duplicate setup across branches

Be careful when:

- there is only one behavior
- the variation is only data
- a simple map, table, switch, or function value is more idiomatic and enough in the active language

### State

Choose when behavior depends on well-defined modes and transitions.

Use when:

- conditionals multiply around status, lifecycle, workflow step, approval stage, connection state, or session state
- transitions are explicit and testable

Be careful when:

- the state machine is tiny
- transition rules are not explicit

### Observer

Choose for one-to-many notification flows.

Use when:

- domain events or subscription-style updates are central
- multiple listeners react to the same change

Be careful when:

- control flow would become surprising
- side effects would be hidden from the caller

### Memento

Choose when snapshots and restores are first-class requirements.

Use when:

- undo, rollback, or restore-prior-version behavior is required without exposing internal representation

Be careful when:

- simple persistence or versioning already solves the problem

### Mediator

Choose when many objects coordinate through direct references and coupling is growing.

Use when:

- UI or workflow coordination is complex
- components should not depend on each other directly

Be careful when:

- the mediator would become a large procedural hub
- responsibilities are not narrow

### Visitor

Choose when the object structure is stable but new operations are frequently added.

Use when:

- the code models ASTs, expression trees, or stable hierarchies with many operations

Be careful in typical application code unless the structure is truly stable.

### Iterator

Choose when traversal should be abstracted from collection representation.

Use when:

- callers should not know internal collection structure
- traversal logic repeats

Be careful when:

- native language iteration already provides the needed abstraction

### Template Method

Choose when an algorithm skeleton is stable but specific steps vary.

Use when:

- there is a fixed workflow with overridable steps
- inheritance or embedding is already an idiomatic local pattern

Be careful when:

- composition via Strategy is clearer
- inheritance would make tests or dependencies harder

## Example Input

```text
User request: add support for multiple notification channels.
Language: go.
Relevant files: checks/notifications/...
Plan, tentative code, or current code summary: create a NotificationSender interface and one implementation per channel, selected by config.
Abstractions being considered or already present: interface, selector, concrete senders.
Variation points: channel/provider.
Expected future cases: SMS, WhatsApp, email, push.
Testing impact: shared caller tests plus implementation-specific tests.
```

## Example Output

```text
Recommended pattern: strategy
Primary pain: delivery behavior varies by channel while callers should remain stable.
Evidence in code: channel/provider is the variation point and more channels are expected.
Selected family: behavioral
Why this pattern fits: multiple implementations perform the same role and can be selected outside the caller.
Rejected alternatives: factory-method creates implementations but does not model the behavior variation itself.
Risk if misapplied: unnecessary interface if only one channel exists or future channels are speculative.
```

## Common Situations

- API request processing with ordered checks such as rate limiting, auth, and handler execution maps to `chain-of-responsibility` when each step is independent and has a clear stop/continue contract.
- Report generation with many configuration options maps to `builder` when valid combinations, defaults, or assembly steps matter.
- Report generation maps to `strategy` when the main variation is a single rendering or calculation policy behind a stable caller.
- Report generation maps to `bridge` when report type and output format vary independently, such as invoices and reports that can each be exported as PDF, CSV, or HTML.
