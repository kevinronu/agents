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
