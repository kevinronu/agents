# Queue trigger

The platform reads batches from a queue and runs the service once per batch.

## AWS
Checked: 2026-11-02
- Chosen: SQS event source mapping
- Tradeoffs:
  - A message reported as failed comes back after the queue's visibility timeout. A rejected
    message is dropped, not reported; the policy is in the `go` skill,
    `references/service/event-sources/queue.md`.
- Configuration:
  - Enable partial batch failure in the mapping,
    `function_response_types = ["ReportBatchItemFailures"]`. Without it the response's
    `BatchItemFailures` is ignored and a returned error retries the whole batch.
  - In Go the handler takes `events.SQSEvent` and returns `*events.SQSEventResponse`.

## GCP
Checked: never
- Chosen: Pub/Sub push subscription

## Azure
Checked: never
- Chosen: Service Bus queue trigger
