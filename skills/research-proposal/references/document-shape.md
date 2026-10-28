# Document shape

## Research or proposal

Both use the same template. A research is for a small change; a proposal for a bigger one.
A doc can start as a research and become a proposal while it grows; the title says which it
is (`# Proposal: <name>`).

## Header

The fields and their values are in [profile.md](../profile.md). One line each, with a blank
line between them: without it markdown joins them into one paragraph. The same applies to
the labeled fields of the Implementation details tab.

## Sections, in this order

1. TL;DR
2. Concepts (table: Concept, Meaning), then "How X works today"
3. Facts & Data
4. Beliefs and assumptions
5. Hard Questions
6. Goals
7. Non-Goals
8. Solution, with these subsections: the design in short sections, Architecture, `<Service>`
   responsibilities (the provider's name for the service, from
   [providers.md](providers.md)), Data model, Cost, Alternative solutions considered,
   Failure Modes, Launch and adoption
9. `Stop reading here`
10. Tasks & Estimation
11. Appendix, one `##` per topic with a descriptive title (no "Appendix A")

## Size

The body up to "Stop reading here" is at most 4,700 words (about 15 pages). Move detail to
the Appendix or to the Implementation details tab first (measurement methods, cost tables,
reasons behind chosen numbers, tables that only gain a field, diagram source, history that
only supports a belief). If it still does not fit, split the proposal into two parts or
steps; do not cut what the reader needs.

## Deliverables

- `<name>.md`: the doc.
- `<name>_implementation.md`: the Implementation details tab.
- `<name>_tasks.csv`: the tasks with the estimation columns of
  [templates/tasks.csv](../templates/tasks.csv).
- The architecture diagram (`.drawio` and `.png`) from the `architecture-diagram` skill.

A design change touches all four. Images are linked by relative path, so the PNG travels
with the doc.
