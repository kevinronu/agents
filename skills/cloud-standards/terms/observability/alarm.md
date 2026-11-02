# Alarm

A rule over a metric or a log query that notifies or pages when a threshold holds.

## AWS
Checked: 2026-11-02
- Chosen: CloudWatch alarm for platform metrics such as throttles and errors.
- Alternative: Elastic watcher, when the condition is a log query; in scrap-services they
  live in terraform under `elastic/metrics/watcher/`.
- Tradeoffs:
  - A log-based alarm that counts every error-level event counts one failure twice when the
    failing step and the execution close both log it. Count one event per execution, the
    execution close, or exclude it from the count.

## GCP
Checked: never
- Chosen: Cloud Monitoring alert

## Azure
Checked: never
- Chosen: Azure Monitor alert
