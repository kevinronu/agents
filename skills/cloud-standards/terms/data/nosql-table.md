# NoSQL table

A key-value or document store with no schema to migrate and no server to size.

## AWS
Checked: 2026-11-02
- Chosen: DynamoDB table
- Why: serverless and pay per request; a function keeps no connection pool; the storage
  packages and the minidyn mock of scrap-services target it.
- Tradeoffs:
  - A scan or a query returns one page: follow `LastEvaluatedKey` until it is empty.
  - A batch write can leave `UnprocessedItems`: read them and retry them.
  - A read-then-write can overwrite a concurrent write: use a condition expression and treat
    its failure as "changed, skip; a later run retries".

## GCP
Checked: never
- Chosen: Firestore collection
- Alternative: Bigtable table, when write volume is very high with simple keys

## Azure
Checked: never
- Chosen: Cosmos DB container
