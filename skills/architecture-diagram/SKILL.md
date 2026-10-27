---
name: architecture-diagram
description: "Draw or update an AWS architecture diagram in draw.io. Use when asked to diagram a system, or the design of a proposal or research doc."
---

# Architecture Diagram

A diagram is evidence: every arrow is a call or an event that exists in code or terraform, or
that the design says will exist. A clean picture of a wrong flow is worse than no picture.

Read [references/standard.md](references/standard.md) before placing anything. It says what
goes in the picture, how each piece looks, and how to review the PNG.

## Tools

- `scripts/diagram_kit.py` builds the `.drawio` from a short Python file and exports the PNG
  with draw.io desktop (`brew install --cask drawio` if missing). It draws the legend, the
  states and the group boxes; you place pieces on a grid and declare arrows. Its docstring
  shows the API.
- When a service has no icon in the kit, add it to `SERVICES` in the kit, not to the builder.
- Write the builder script in the scratchpad, not in the repository. The `.drawio` is the
  source that lasts.
- Load `plain-writing` for subtitles and labels when it is available.

## Done

The `.drawio` and the `.png` sit together where the user asked (the repository root when
unsaid), the PNG passed the review in the standard, and the reply lists any arrow that comes
from the design rather than from code, and any claim still unverified.

## Changing this skill

When a task shows a gap or a rule that does not work, propose the change in the reply; write
it only after Kevin approves. Read the file that will change in full first, and merge or
replace a rule instead of adding one on top. Write rules, not history: no "now", "before" or
dates.
