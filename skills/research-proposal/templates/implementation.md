# Implementation details: <name>

This tab is the developer guide for the proposal "<name>". Read the proposal first: its Solution has the architecture, the job of each <service> and the data model.

# Architecture

![Architecture](<name>.png)

# Libraries

## <package> (new | changes)

**Path:** `<directory>`

**Used by:** `<service>`, `<service>`

**Description:** <What it does, in two or three sentences. A new function's signature goes here.>

**Steps:**

1. <Step with the function and the operation.>

# <Services>

## <service> (new | changes)

**Path:** `<directory>`

**Triggered by:** <the trigger, batch size, link to the [message](#message) in the Appendix; or "as today">

**Settings:** `<VAR>` = <value>

**Description:** <What it does today and what changes.>

**Steps (new):**

* <Step.>

**Writes:** <table or bucket>, <what>.

**On failure:** <What happens halfway, what a retry does, where the failed item ends up.>

**<Permissions> (new):** <action> on <resource>.

# <Infrastructure tool>

**Regions.** <Where each piece runs and why.>

**Resources:**

* <Table, bucket, queue or event router with the settings that matter.>
* The <permissions> of each <service>, listed in its section.

# Alarms

| Alarm | Metric | Fires when | What to do |
| :---- | :---- | :---- | :---- |

# Operations

**Turn on.** 

**Turn off.** 

**Go back.** 

# Important tests

* <A test on code that does not change here but can silently break the feature.>

# Appendix

## <Message>

```json
{}
```
