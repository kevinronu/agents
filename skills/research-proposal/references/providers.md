# Provider names

These references use one neutral term per role. The doc, the tab and the tasks use the
provider's names, so the reader sees the console's words; a heading that holds a neutral
term takes the provider's name too (`<Service> responsibilities` is "Lambda
responsibilities" on AWS). The provider comes from [profile.md](../profile.md).

## How to choose

Use the default: the newest, most managed option the provider offers for that role. Use the
alternative only when its condition holds, or when the design extends something that
already uses it (one entity never lives in two stores). When the doc uses the alternative,
Alternatives says which condition held. A choice fixed in the profile wins over the default.

## AWS

| Role | Default | Alternative | When the alternative |
|---|---|---|---|
| Service | Lambda | ECS Fargate | The work does not fit a function: it runs longer than 15 minutes or keeps connections open |
| NoSQL table | DynamoDB table | | |
| Relational table | Aurora DSQL | Aurora PostgreSQL | The design needs a PostgreSQL feature DSQL does not have (extensions, triggers, foreign keys) |
| Cache | ElastiCache Serverless for Valkey | | |
| Object storage bucket | S3 bucket | | |
| Queue | SQS queue | | |
| Topic | SNS topic | | |
| Change stream | DynamoDB stream | Kinesis Data Streams for DynamoDB | More than two consumers, or retention longer than 24 hours |
| Event router | EventBridge Pipe (from a stream to a queue) or EventBridge rule | | |
| Dead-letter queue | SQS queue | | |
| Permissions | IAM role and policy | | |
| Alarm | CloudWatch alarm | | |
| Secret | Secrets Manager secret | | |
| Operation | The API action as the SDK names it (`UpdateItem`, `CopyObject`) | | |

## GCP

| Role | Default | Alternative | When the alternative |
|---|---|---|---|
| Service | Cloud Run service | Cloud Run job | The work runs to completion with no request to answer |
| NoSQL table | Firestore collection | Bigtable table | Very high write volume with simple keys |
| Relational table | AlloyDB | Cloud SQL | A small database where AlloyDB's cost is not justified |
| Cache | Memorystore for Valkey | | |
| Object storage bucket | Cloud Storage bucket | | |
| Queue | Pub/Sub subscription | | |
| Topic | Pub/Sub topic | | |
| Change stream | Firestore trigger (Eventarc) | | |
| Event router | Eventarc trigger | | |
| Dead-letter queue | Pub/Sub dead-letter topic | | |
| Permissions | IAM service account and role | | |
| Alarm | Cloud Monitoring alert | | |
| Secret | Secret Manager secret | | |
| Operation | The API method as the client library names it | | |

## Azure

| Role | Default | Alternative | When the alternative |
|---|---|---|---|
| Service | Azure Function | Container App | The work does not fit a function: long runs or open connections |
| NoSQL table | Cosmos DB container | | |
| Relational table | Azure SQL Database | Azure Database for PostgreSQL | The code or the team needs PostgreSQL |
| Cache | Azure Managed Redis | | |
| Object storage bucket | Blob Storage container | | |
| Queue | Service Bus queue | | |
| Topic | Service Bus topic | | |
| Change stream | Cosmos DB change feed | | |
| Event router | Event Grid subscription | | |
| Dead-letter queue | Service Bus dead-letter queue | | |
| Permissions | Managed identity and RBAC role | | |
| Alarm | Azure Monitor alert | | |
| Secret | Key Vault secret | | |
| Operation | The API operation as the SDK names it | | |

For a provider that is not here, add a section with the same columns. The infrastructure
tool (Terraform, Pulumi, CDK) comes from the profile, not from these tables.
