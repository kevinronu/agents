# Direct invocation

The handler receives the input contract and returns the output contract.

Return policy: return the error only when it is retryable, so the platform (async invoke) or
the caller (sync invoke) retries. Anything else is already in the logs and returns no error
and no output. On a synchronous call the caller gets an empty result after a rejection; the
only signal is the warning log.

The provider's types are in `cloud-standards`, `terms/event-sources/direct-invocation.md`.
scrap-services: `retryableOrNil(err)` in
`digital-identity/whatsapp/functions/repair-client-inbound-flows`.
