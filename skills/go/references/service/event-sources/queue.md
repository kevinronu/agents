# Queue

The handler receives a batch of messages and returns which ones go back to the queue, so one
bad message does not retry the whole batch.

Return policy: report a message as failed only when its error is retryable. A rejected message
is dropped with its warning. Return an error for the whole batch only when none of it could be
processed; then every message is retried.

The provider's types and the setting that makes the platform honor the response are in
`cloud-standards`, `terms/event-sources/queue-trigger.md`.
scrap-services: `digital-identity/whatsapp/functions/send-outbound-batch`.
