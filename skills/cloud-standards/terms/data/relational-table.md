# Relational table

A store with a schema, joins and transactions, reached with SQL.

## AWS
Checked: 2026-11-02
- Chosen: Aurora DSQL
- Why: serverless and PostgreSQL-compatible; no instance to size.
- Alternative: Aurora PostgreSQL, when the design needs a PostgreSQL feature DSQL does not
  have: extensions, triggers, foreign keys.
- Configuration: connections go through the `shared/dsql` pool of scrap-services.

## GCP
Checked: never
- Chosen: AlloyDB
- Alternative: Cloud SQL, when the database is small and AlloyDB's cost is not justified

## Azure
Checked: never
- Chosen: Azure SQL Database
- Alternative: Azure Database for PostgreSQL, when the code or the team needs PostgreSQL
