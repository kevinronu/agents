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
