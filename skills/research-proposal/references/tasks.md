# Tasks & Estimation

One story point is one day of work. The doc does not say this; the reader knows it.

## One task

- Starts with a verb: "Create the storage", "Send the videos to the queue".
- Names what it builds and which files or packages it touches, in one sentence a reviewer
  can read in one sitting. Depends on: the ids it needs merged first.
- The same list goes to the CSV ([templates/tasks.csv](../templates/tasks.csv)).

## The CSV

- `Días PRISM` and `Estimación Final` stay empty: the Google sheet computes them from the
  other columns. Say so when handing the CSV to the agent that fills the sheet.
- The PRISM columns describe the task as it is: an open technical unknown goes in
  `Predictabilidad` ("Existen algunos desconocidos y se necesita investigar"), not in risk.
- `Alto riesgo` is `Si` only when the ticket can break something that works in production
  today: it changes a lambda that runs for every client (even behind a client list), a table
  or contract that others read, or shared permissions and resources. A ticket that only
  creates things nobody uses yet (a table, a library, a lambda with no trigger) is `No`, even
  with an unknown inside.

## Order

models → storage (the table and bucket terraform go with it) → pure-logic packages →
the lambda with its own terraform → what connects to it (queues, triggers) → what sends to
it → deletion → consumers → frontend.

What receives is deployed before what sends, and senders start with an empty client list,
so nothing is ever connected to something that does not exist yet.

## Split or group

- Split pure logic from AWS calls, and backend from frontend, even when both are small: a
  reviewer reads them in different ways, and they deploy separately.
- Group loose models and small resources: a lambda never weighs the same as creating a table.
- Using the DynamoDB and S3 mocks that exist adds no work. Only a new shared library does.
- A task with an open unknown does not take extra scope.
