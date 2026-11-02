# Object storage bucket

A store for files of any size, addressed by key, that clients reach with presigned access.

## AWS
Checked: 2026-11-02
- Chosen: S3 bucket
- Why: the default object store; presigned URLs come from `shared/files` in scrap-services.

## GCP
Checked: never
- Chosen: Cloud Storage bucket

## Azure
Checked: never
- Chosen: Blob Storage container
