# HTTP request

A gateway turns an HTTP request into an invocation and the result into the response.

## AWS
Checked: 2026-11-02
- Chosen: API Gateway
- Tradeoffs:
  - A returned Go error becomes a generic 502 with no body the client can act on, so the
    handler returns a response for every case; the policy is in the `go` skill,
    `references/service/event-sources/http.md`.
- Configuration:
  - In Go the handler takes `events.APIGatewayProxyRequest` and returns
    `events.APIGatewayProxyResponse`; `shared/apigateway` of scrap-services builds error and
    JSON responses. The client id and the authorizer come from the request context.

## GCP
Checked: never
- Chosen: Cloud Run request

## Azure
Checked: never
- Chosen: HTTP trigger
