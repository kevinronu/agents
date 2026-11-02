# Permissions

What a service may do on which resources, granted to its own identity with the least
privilege that works.

## AWS
Checked: 2026-11-02
- Chosen: IAM role and policy
- Configuration: one role per service, in the service's terraform under `iam/role/`, with
  its policy under `iam/role/policy/`.

## GCP
Checked: never
- Chosen: IAM service account and role

## Azure
Checked: never
- Chosen: Managed identity and RBAC role
