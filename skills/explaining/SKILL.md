---
name: explaining
description: Explains one thing the user did not understand, for a reader whose only context is this session. Use when the user says "no entiendo", "explícame", "qué es X", "de qué hablas", "por qué", or asks what a term, change or number means.
license: Apache-2.0
metadata:
  author: kevinronu
  version: "1.0"
---

# Explaining

The reader knows only what this session has shown them. Nothing from a file,
log or doc you read on your own exists for them until you put it in the answer.

## Shape

1. The answer in one sentence, in the reader's own words from the question.
2. The mechanism, cause to effect, one new fact per sentence.
3. One concrete case with the real ids, numbers or names from this session.
4. Stop. No summary, no options, no "si quieres".

## Rules

- Define every term the session has not shown, in the same sentence, in
  parentheses. A term the reader asked about ("de qué contador me hablas")
  is the proof it was never defined.
- Length follows the question: "qué es X" takes two or three sentences;
  "por qué" takes the chain and nothing else. A detail that would leave the
  answer unchanged if removed (a bucket name, an ARN, a UUID) is not part of
  the chain. One screen is the ceiling.
- Concrete before abstract: show the line, the id or the number, then the rule.
- Take a position when the question has a judgment in it ("¿es mucha carga?"):
  answer yes or no first, then why.
- Spanish, natural, no headings for a short answer; a two-column table only
  when the reader has to compare.

## Learning

When the user says they still did not understand, find which rule failed,
fix the answer, and update this file in the same turn: merge the lesson into
the rule it belongs to, keep rules not history.
