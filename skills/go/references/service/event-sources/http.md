# HTTP

The handler receives the request and returns a response, never an error: a returned error
becomes a generic 5xx from the gateway, with no body the client can act on.

Return policy by case:

| Case | Response |
|---|---|
| Rejection | 4xx with the error's public message |
| Failure | 5xx; `p.err` is set and the client gets no internal detail |
| Success | 200 with the output contract as the body |

The processor takes its fields from the path, the query and the body through its value-object
constructors; the client id and the authorizer come from the request context.

The provider's types and response helpers are in `cloud-standards`,
`terms/event-sources/http-request.md`.
scrap-services: `digital-identity/whatsapp/functions/list-inbounds`.
