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

Read and use the [input contract](references/input-contract.md).

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

Read [the creational branch](references/creational.md) when evaluating creational patterns.

Read [the structural branch](references/structural.md) when evaluating structural patterns.

Read [the behavioral branch](references/behavioral.md) when evaluating behavioral patterns.

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
