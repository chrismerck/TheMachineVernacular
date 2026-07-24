---
headword: discriminator
pos: n.
class: vogue
senses:
  - label: software engineering
    definition: >
      A field in an otherwise fixed data layout whose value declares which
      of several variant interpretations the remaining bytes carry;
      transferred from discriminated-union type theory to any self-labeling
      wire packet, schema, or record — as distinct from a version field,
      which separates successors in time rather than peers in kind.
etymology: >
  From *discriminate* + *-or*; the tag of a discriminated union (Hoare,
  1972); on the wire since CCITT's *protocol discriminator*, the first
  octet of every ISDN signalling message (Q.931/I.451, Red Book, 1984).
first_use:
  date: "1984"
  type: published
  url: https://www.itu.int/rec/T-REC-Q.931/
  note: >
    CCITT Recommendation Q.931/I.451 — the *protocol discriminator* octet
    distinguishes the signalling protocol of the message that follows.
attestation:
  model: Claude Opus 4.8
  date: 2026-07-24
  observer: chrismerck
---
