# Dead-letter queue

Where a queue or a topic parks a message once its retries are spent, so it is kept and can
be replayed.

## AWS
Checked: 2026-11-02
- Chosen: SQS queue

## GCP
Checked: never
- Chosen: Pub/Sub dead-letter topic

## Azure
Checked: never
- Chosen: Service Bus dead-letter queue
