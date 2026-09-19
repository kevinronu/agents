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
