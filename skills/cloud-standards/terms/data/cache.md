# Cache

An in-memory store for data that is cheap to lose and expensive to recompute or fetch.

## AWS
Checked: 2026-11-02
- Chosen: ElastiCache Serverless for Valkey
- Why: Redis-compatible and open source; no node to size.
- Tradeoffs:
  - Cluster mode needs a cluster-aware client. `shared/cache` of scrap-services is one,
    configured with `TRUORA_CACHE_USE_CLUSTER` and `TRUORA_CACHE_SHARDS`.
- Configuration: the client is created in `main` and fails fast, as `compute/service.md`
  says.

## GCP
Checked: never
- Chosen: Memorystore for Valkey

## Azure
Checked: never
- Chosen: Azure Managed Redis
