# Diagram standard

## Reader and size

The reader does not know the product, unless the user says otherwise. The picture shows them
the flow; the document around it explains the details.

The diagram goes in a document, so it must be readable at page width. Draw it whole first.
If it is too wide or too tall to read, propose to the user to split it by flow (one PNG per
flow, named `<name>-<flow>.png`), and split it only if they agree.

## Scope

Draw what the request covers: the design of the document, or the part of the system the user
named. Never the whole system around it.

A piece that does not change enters only when the reader needs it to follow the flow. Show
only what the picture needs to explain: a name, a list or a detail that the reader does not
need here stays in the document.

The legend always sits on top of the picture. The kit draws it from the services and states
used, so the document does not need another one.

There are two kinds of diagram:

- **A design** (a proposal, a research, a planned change): pieces are `new`, `changed` or
  `unchanged`, and subtitles say what each piece does in this change.
- **A system as it is** (how X works today): every piece is `plain`, the legend has no State
  block, and subtitles say what each piece does in this flow.

## Evidence

For every arrow, have a file and line that shows it, or leave it out:

- the operation, the AWS API name the code calls through any wrapper;
- the direction: who calls, or who emits and who receives;
- sync or async: does the caller wait for the answer;
- the filter, when the sender or the receiver filters.

Find triggers in terraform (`sns_triggers`, `event_source_triggers`, SQS mappings, schedules,
S3 notifications, Lambda destinations) and calls in the code. An env var or a helper that
builds a name is not proof of the target until you trace it to the real resource.

Follow each piece of data the flow depends on end to end: who writes it, who rewrites it
later, who reads it.

In a design, new pieces and new arrows come from the document. Check that they fit what
exists: the trigger exists or the design creates it, someone writes the data they read, and
the operation fits the resource. When the document and the code disagree about what exists
today, the code wins: tell the user what is wrong in the document and propose the fix; do not
draw the wrong version.

## Pieces

Each piece takes the form of its role in the flow:

| Form | When | How it looks |
| :---- | :---- | :---- |
| Icon | One resource that is a step of the flow | The AWS icon, 50×50 |
| Group box | Several resources that act as one step: the same trigger, the same output and, in a design, the same change | Gray box of fixed width. Name with the count (`Synchronous checks (10)`); subtitle with what they do in this change, not which ones they are |
| Frame | A system with a name that holds icons and boxes, so the reader sees which pieces belong together | Light frame with a bold title. No arrow touches it; it is not in the legend |
| External | A service outside AWS or outside the team, only when the flow drawn is about the call to it | Blue cloud, named after the service |
| Name on an arrow | A topic, queue or stream, or an unchanged step the reader does not need to see | `SNS <topic>`, `stream`, `through <lambda>` in the label |

A resource whose trigger, output or change differs from the others gets its own icon, even
when it belongs to the same system. Put it next to the group, inside the same frame.

### State

- **New**: full color, a ring in the service color and a `+` mark. The eye finds it first.
- **Changed**: full color and a `~` mark.
- **Unchanged**: the icon at 70% opacity; the text stays dark because the piece matters.
- **Plain**: full color, no mark, only in a diagram of a system as it is.
- A group box carries the mark of the state all its pieces share; without a mark, none of
  them changes.
- Color belongs to the service and never changes with the state. The marks carry the state.

### Subtitles

One or two short lines: what the piece does in this change (design) or in this flow (system).
Where it runs, how it fails or how it is deployed belong to the document.

## Arrows

- Draw the arrows the flow travels through and the ones the reader needs to follow it. Leave
  out the other calls of a piece (logs, timeouts, metrics) unless the picture is about them.
- Solid: sync, the caller waits for the answer. Dashed: async, the caller does not wait.
- A call goes from the caller to what it calls. An event goes from its source to what receives it.
- A queue or topic you draw is a resource: sending to it is a sync call, consuming from it is
  an async event. A table's stream leaves from the table.
- Draw only real interactions. Signing an S3 URL is not a call to S3.

## Labels

- Call: `Operation (r / w / rw)` on line one, what it sends or gets on line two. Use the exact
  API name (`PutItem`, `CopyObject`, `Invoke`). The letter appears only when the operation
  reads or writes data.
- Event: up to three lines, each only when it adds something: how it arrives, when the icon
  it leaves does not say it; the filter, when the sender or the receiver filters; the delivery
  setting, when it matters to the design (`in batches of 10`). A number comes from a
  documented quota or a verified setting.
- Break a line only between different facts, never inside a name. If a label does not fit,
  move the columns.
- A label sits at the middle of one segment of its line: the whole line when it is straight,
  the longest segment when it bends once, the middle segment when it bends twice. Leave the
  middle only to keep it away from another label or line.

## Layout

- Fixed grid, so horizontal arrows are straight. Rows follow the flow; pieces sit next to the
  resources they touch.
- No arrow enters or leaves through the side of an icon that carries text, or through a mark.
- Ports on one side are symmetric: one arrow at the middle, n arrows at n + 1 equal parts. A
  straight line between two aligned pieces wins over the split.
- Prefer straight arrows; a bend exists only to avoid something. Parallel lines keep enough
  distance that a label on one does not cover the other.
- No spare space at either side: compact column by column until the widest label sets the gap.
- When A covers B, move A; do not shrink B.

## Review

You cannot see a diagram from its XML. Every change ends with looking at the PNG:

1. Run the builder; `Diagram.save` and `Diagram.export` write the `.drawio` and the PNG.
2. Open the PNG and check: no line or label covers an icon, a text or a mark; no two labels
   touch, and each sits next to its own line; every arrow has the right style, direction and
   label; every arrow still follows the port and label rules after a piece moves; no spare
   space at the sides; the diagram reads at page width.
3. Fix the builder and repeat. Pin routes with ports and waypoints. A label has three knobs:
   `label_position` slides it along the line (-1 start, 1 end), `label_shift_x` moves it
   sideways, and a waypoint moves the line itself.

To compare options, export each one to its own PNG next to the main one, and delete the ones
not chosen.
