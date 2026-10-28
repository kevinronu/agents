# Writing rules

## Language

- B1 English: short sentences, plain words. A PM who never saw the product follows it.
- Official names only: the provider's names for its services and resources
  ([providers.md](providers.md)), and the real names of tables, services, fields and API
  operations, as they appear in the code.
- We act, the service does not: "we ask the provider to index the image", never "the
  provider saves".
- Never invent a team, and never name another person's research in the doc.

## Order and repetition

- General to particular, like a newspaper: nothing appears before it is presented. A
  section that holds several pieces opens with a short paragraph that names them and how
  they relate, then the detail.
- Each idea lives in one place. When a new paragraph presents something, delete the opening
  sentences that repeated it in older sections.
- Concepts explains each term in one or two lines, in the abstract. How the term is used in
  this design belongs to Solution. The TL;DR uses the terms without defining them.
- Process flows are mermaid in the body, with the same code in the Appendix so a published
  copy that cannot render mermaid can link to it. The architecture is the PNG from
  `architecture-diagram`.

## What each section holds

- **TL;DR**: the problem, the goal, the proposal in three or four bullets, the cost line.
- **Facts & Data**: only facts that support a decision, each with number, date and source.
  The method of a measurement goes to the Appendix. A fact that no decision uses is deleted.
- **Beliefs**: what we believe and why, without repeating the studies of Facts.
- **Hard Questions**: only real open problems that change the design. A question with an
  obvious answer is a decision in Solution. "None." is a valid section.
- **Non-Goals**: cannot contradict Tasks. If something is a task, it is not a non-goal.
- **Solution**: short sections, each one decision. One paragraph per service: what it does and
  why it exists. Triggers, steps, inputs, outputs and the reasons behind a design choice go to
  the Implementation details tab.
- **Data model**: an opening paragraph that names every table and field added; the label
  legend (**NEW**, **UPDATED**, **DELETE**; an attribute with no label stays as today); then
  one table per real table: a NoSQL table always with **(PK)** and **(SK)**, a relational
  table with its primary key and its foreign keys. New tables stay in the body;
  tables that only gain a field go to the Appendix. When a field lives in two tables, the
  opening paragraph says why.
- **Cost**: one sentence with the total in the body; the prices and the table in the Appendix.
- **Alternatives**: one or two reasons per row. Do not list an option the doc already rules
  out at the start.
- **Failure Modes**: one row per real failure: what happens, how we find out (the alarm) or
  how we go back. Failures that exist today and do not change with this work stay out.
  Scripts and their steps go to the Implementation details tab.
- **Launch and adoption**: deploy order, what turns on with what, who must be told.
