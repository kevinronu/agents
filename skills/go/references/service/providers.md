# Providers

The shape uses neutral terms. This table translates them; AWS is the default in
scrap-services, and its Go event types come from `github.com/aws/aws-lambda-go/events`.

| Term | AWS | GCP | Azure |
|---|---|---|---|
| Service | Lambda | Cloud Run service | Azure Function |
| Direct invocation | `lambda.Start(handler)` with the input contract | HTTP request to the service | HTTP trigger |
| Queue | SQS: `events.SQSEvent`, `events.SQSEventResponse` | Pub/Sub push subscription | Service Bus queue trigger |
| Topic | SNS: `events.SNSEvent` | Pub/Sub topic | Service Bus topic trigger |
| HTTP | API Gateway: `events.APIGatewayProxyRequest` | Cloud Run request | HTTP trigger |
| Execution log | `logger.LogLambdaExecution` | the same logger | the same logger |
