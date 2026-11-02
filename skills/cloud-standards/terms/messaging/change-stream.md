# Change stream

An ordered feed of the writes to a table, for consumers that react to data changes.

## AWS
Checked: 2026-11-02
- Chosen: DynamoDB stream
- Alternative: Kinesis Data Streams for DynamoDB, when there are more than two consumers or
  retention must exceed 24 hours.

## GCP
Checked: never
- Chosen: Firestore trigger (Eventarc)

## Azure
Checked: never
- Chosen: Cosmos DB change feed
