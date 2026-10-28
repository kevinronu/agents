# Trusted sources

The user can give one or more docs, tickets or ADRs that were already verified: a sibling
proposal, an earlier research, a decision record. They weigh more than the doc under review.

- A fact in a trusted doc stands. When the doc under review contradicts it, the comment
  cites the trusted doc's value and where it was measured.
- The vocabulary of the trusted doc is the vocabulary of the review: the same names for the
  same things, so the author can map one doc to the other.
- A trusted doc is still checked before a comment relies on it: its number has a date and a
  window, its claim has a source. A trusted doc with an unverified claim does not make the
  claim true.
- When the two docs touch the same design (the same table, the same flow), the review says
  how they meet: what one assumes that the other changes, what order they need, what one
  can reuse from the other.
