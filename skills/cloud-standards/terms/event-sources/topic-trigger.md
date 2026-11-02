# Topic trigger

A topic subscription runs the service once per published message.

## AWS
Checked: 2026-11-02
- Chosen: SNS subscription
- Tradeoffs:
  - A returned error makes the topic redeliver the message until its retry policy gives up,
    so a rejection must return nil; the policy is in the `go` skill,
    `references/service/event-sources/topic.md`.
- Configuration: in Go the handler takes `events.SNSEvent`, one record per invocation.

## GCP
Checked: never
- Chosen: Pub/Sub topic subscription

## Azure
Checked: never
- Chosen: Service Bus topic trigger
