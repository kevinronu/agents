# Implementation details tab

The developer guide of the proposal. The proposal says what and why; this tab says how, with
the paths, operations, settings and failure handling a developer needs to build each ticket.
It never repeats the proposal: a struct lives in Data model, a reason lives in Solution; the
tab links to them.

Template: [templates/implementation.md](../templates/implementation.md).

## Sections, in this order

1. **Intro line**: "This tab is the developer guide for the proposal <name>. Read the proposal first."
2. **Architecture**: the same PNG as the proposal, nothing else.
3. **Libraries**: one `##` per package that more than one lambda uses, or that holds logic
   worth testing on its own. Name it as the repo does: `<entity>` storage packages under
   `storage/` (`storage/accounts` → `accounts`), logic packages by what they do. A function
   that one lambda uses and that is one call long goes in that lambda's Steps, not here.
4. **Lambdas**: one `##` per lambda, new or changed, in the order the data flows.
5. **Terraform**: regions first, then the resources (tables, buckets, queues, pipes) with the
   settings that matter (keys, billing mode, encryption, global or local, retries, batch
   size, concurrency and the quota it comes from). The IAM of each lambda is in its own
   section; here only "the IAM of each lambda, listed in its section".
6. **Alarms**: a table with Alarm, Metric and threshold, Fires when, What to do.
7. **Operations**: turn on, turn off, go back, failover; scripts with their steps.
8. **Important tests**: only tests nobody would think of, usually on code that does not
   change in the proposal but can silently break the feature. Tests that follow from the
   Steps are not listed.
9. **Appendix**: the exact JSON of every message, filter and transformer, each under its own
   `##`, linked from the lambda that sends or reads it.

## One library or lambda

Fields, each on its own paragraph (a blank line between them, or markdown joins them):

- **Path**: the directory; for a changed file, the file. `(new)` or `(changes)` in the title.
- **Triggered by** (lambdas) / **Used by** (libraries): the trigger with its batch size and
  a link to the message in the Appendix; or the list of callers.
- **Settings**: the environment variables it reads, with their values, only when it has any.
- **Description**: what it does today and what changes, in two or three sentences.
- **Steps** (`Steps (new)` for a changed lambda): numbered or bulleted, with the function
  names and the AWS operations (`UpdateItem` with its `SET`, `CopyObject`, `AssociateFaces`).
  For a field that must reach a filter or another table, the steps say every write that
  carries it there.
- **Writes**: what it leaves in each table, bucket or service, one line.
- **On failure**: what happens if it fails halfway, and what a retry does (duplicates, fixed
  keys, the retry check). Where the failed item ends up.
- **IAM**: the new permissions, by action and resource.

A library has Path, Used by, Description, Steps; the signature of a new function goes under
Description when it is a new contract.

## What goes here and not in the proposal

Triggers and their filters, steps, inputs and outputs, the reasons behind a design choice,
scripts, IAM, alarms with their metrics and thresholds, settings, the history of why a trigger
is what it is (with its ticket).

## What goes in the proposal and not here

Structs and tables (Data model), what each lambda is for (Solution), the cost, the
alternatives, the failure modes as the reader sees them, the launch order.
