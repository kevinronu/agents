# Proposal: <name>

Date: <Mon DD, YYYY>

PM: <from the profile>

Tech Owner: <from the profile>

Parent Proposal: <link, only when there is one>

Team: <from the profile>

Time to read: ⌛30:00

Time to discuss: ⌛15:00

# TL;DR

<The problem in two or three sentences. The goal in one line. The proposal in three or four bullets. The cost line.>

# Concepts

| Concept | Meaning |
| :---- | :---- |
| <term> | <one or two lines, in the abstract> |

## How <X> works today

<The current flow. A mermaid diagram if it has branches; its code also goes in the Appendix.>

# Facts & Data

<Facts that support a decision, each with number, date and source.>

# Beliefs and assumptions

# Hard Questions

None.

# Goals

# Non-Goals

# Solution

<One paragraph: what we will do.>

## <One decision per section>

## Architecture

![Architecture](<name>.png)

The legend at the top of the diagram explains the colors, the marks and the lines.

## <Service> responsibilities

**<service> (new | changes).** <What it does and why it exists, in one paragraph.>

The **Implementation details** tab has the steps of each <service>.

## Data model

<Opening paragraph: the tables and fields added, and how they relate.>

Labels: **NEW** is added, **UPDATED** changes, **DELETE** is removed. An attribute with no label stays as today. **(PK)** is the partition key and **(SK)** the sort key.

### NEW <table> (table)

Path: `<model file>`

| Attribute | Type | Description | Example |
| :---- | :---- | :---- | :---- |
| `<key>` **(PK)** | string | | |

## Cost

<One sentence with the total. The details are in [Cost details](#cost-details).>

## Alternative solutions considered

| Alternative | Why we did not choose it |
| :---- | :---- |

## Failure Modes

| Situation | What happens |
| :---- | :---- |

## Launch and adoption

Stop reading here

# Tasks & Estimation

| ID | Task | Depends on | SP |
| :---- | :---- | :---- | :---- |
| 1 | <Verb> … | — | 1 |

# Appendix

## Cost details

## <Measurement method>
