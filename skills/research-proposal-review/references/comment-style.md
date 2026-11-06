# Comment style

A comment is read by the author of the doc, in the doc, next to the text it talks about.

## Anchor

- The anchor is literal text of the doc, copied as it is, short enough to find with search.
- The section name goes outside the anchor, only to locate it.

## Quotes

- Inside the comment, quotes hold only literal text of the doc. Everything else is said as
  the reviewer's own words. Never put in quotes a paraphrase of what the doc says.

## Voice

- B1 English, like one engineer talking to another: short sentences, plain words.
- At most three sentences, in this order: the fact, its consequence, the suggestion. The
  author reads the comment next to the text, so a sentence that repeats what the doc already
  says is cut.
- State what is true. Ask only when the answer is unknown and the doc does not give it.
- Say the consequence: what happens if the text stays as it is. A comment without a
  consequence is a remark, not a review.
- A suggestion is marked as one ("I suggest…"). A fact is not.
- Write for an author who read only this doc. A field, table, lambda or project that comes
  from another doc gets a few words on what it is, or the comment cannot be understood.
- When a component cannot do something, say what it does read ("reads only the face
  validation, which has the `enrollment_id` but not its status"), so the gap is visible.
- When the point is a difference between two cases, say each case and what follows from it
  ("`pending` must go to the queue, because…; `success` must not").
- Name the components each sentence talks about. When a sentence says "both", "they" or
  "the deletion", put the names in parentheses after it, because the author acts on the
  suggestion alone and must not go back to find what it points to.
- When the comment needs a test to settle it, say what to test and why the sources do not
  answer it ("We need to test in staging what happens when…, because the provider's docs do
  not say…").

Example:

> `start-delete-process` and `delete-enrollment` remove the members, but `status` stays
> `quarantined`, and only support can clear it. A client that deletes everything leaves the
> account blocked forever. I suggest that both deletions (`start-delete-process` and
> `delete-enrollment`) clear the quarantine when they remove an id in
> `quarantine_validation_ids`.

## What not to write

- A question the doc already answers in another section.
- A coordination question with an obvious answer ("who tells the client?" when Launch names
  who). State the decision instead.
- A remark that another comment already makes. If two comments touch, one points to the
  other by its section ("see my comment on the majority rule in Beliefs") or is dropped.
- A fix of grammar or style, unless the sentence cannot be understood.

## Severity, said to the user, not in the comment

In the reply, group the comments by what they mean for the doc:

1. The design breaks or lets something wrong through.
2. Two sections say different things.
3. Something the doc needs is missing (a cost, a scenario, a failure mode).
4. Wording.

Say for each one whether it is grave or can be left out, when the author asks for fewer.
