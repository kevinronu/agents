# Queue

A buffer of messages that each consumer takes once. A message that fails comes back after
its visibility timeout and, after too many tries, goes to the dead-letter queue.

## AWS
Checked: 2026-11-02
- Chosen: SQS queue
- Tradeoffs:
  - Messages arrive in batches; without partial batch failure one bad message retries the
    whole batch. How to enable it is in `event-sources/queue-trigger.md`.

## GCP
Checked: never
- Chosen: Pub/Sub subscription

## Azure
Checked: never
- Chosen: Service Bus queue
