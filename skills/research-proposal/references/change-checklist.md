# After every design change

Before answering, run this on the doc, the Implementation details tab, the CSV and the
diagram. A change that reaches only one of them is not done.

1. **Stale text.** Search the old name, the old mechanism and the old number in all four.
   A sentence that was true before the change and is false after it is the most common bug.
2. **Text that repeats.** Read the touched sections as a newcomer: each idea once, in the
   section that owns it. Delete opening sentences that a new paragraph now covers.
3. **Order.** General to particular inside each section; nothing used before it is presented.
4. **Agreement.** Goals, Non-Goals, Solution, Failure Modes, Launch and Tasks say the same
   thing. A task is not a non-goal; an alarm in Failure Modes exists in a task; a deploy step
   in Launch matches the order of the tasks.
5. **Size.** Count the words of the body up to "Stop reading here" and compare with the
   limit in [document-shape.md](document-shape.md).
6. **Verification.** Every new claim went through [verification.md](verification.md); every
   pending item is marked and listed in the reply.
