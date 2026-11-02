# Topic

The handler receives the topic event with one record per invocation and returns only an
error. `createProcessor` parses the record's message into the input contract.

Return policy: as in a direct invocation, return the error only when it is retryable. A
returned error makes the topic redeliver the message, so a rejection must return nil or it is
redelivered until the retry policy gives up.

scrap-services (AWS): `events.SNSEvent` with `retryableOrNil(err)`.
Example: `digital-identity/whatsapp/functions/follow-up`.
