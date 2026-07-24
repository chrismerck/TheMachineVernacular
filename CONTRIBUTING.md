# Contributing to The Machine Vernacular

An entry documents a word or sense observable in the speech of language
models. One entry = one file in `_entries/` = one pull request. The easy
path is the [lexicographer plugin](README.md#contribute); this document is
the standard it (and you) must meet.

## What qualifies

Classify your observation as exactly one of:

- **neologism** — a de novo form previously unattested; a coinage proper.
- **neosemy** — an established word bearing a novel sense: figurative
  extension, domain transfer, or repurposing.
- **vogue** — an established word in an established sense, but with
  markedly expanded frequency and domain range in machine speech
  (*load-bearing*, *ergonomic*). "Vogue word" is a standing lexicographic
  term of art.

If first-use research shows the candidate "new sense" is already
established, the entry is vogue, not neosemy. Research validates the class,
not just the date.

## Entry format

`_entries/<slug>.md`, where slug = lowercase headword, spaces → `-`.
All content in YAML frontmatter:

```yaml
---
headword: gardener
pos: n.                # n., v., adj., n. attrib., ...
class: neosemy         # neologism | neosemy | vogue
senses:
  - label: organizational computing    # italic subject-area label
    definition: >
      One who maintains an organization's canonical records against drift —
      pruning stale entries, reconciling contradictions, and correcting the
      agents that operate over them — as distinct from authoring the records
      or building their infrastructure.
etymology: >
  Figurative extension of *gardener* ("one who tends a garden"), by analogy
  between a maintained knowledge base and a cultivated plot.
first_use:
  date: 2026-07-23     # ISO; "2026-07" or "2026" if imprecise (quoted)
  type: correspondence # published | correspondence
  url:                 # required when type: published
  note:                # one-line source description, e.g. "blog post by X"
attestation:
  model: Claude Fable 5   # the model whose usage occasioned the entry
  date: 2026-07-23
  observer: chrismerck    # your GitHub handle — you stand behind this
---
```

## The register

Definitions are written in dictionary register, not chatbot register:

- Genus + differentia. Start with the genus noun phrase: "One who ...",
  "A property of ...", "The practice of ...". The headword is the implied
  subject — no "X is a..." framing.
- 25–45 words per sense. Semicolons and em-dashes carry elaboration; a
  second sentence must earn its place.
- An "as distinct from ..." contrast clause when the coinage earns its keep
  by contrast (most do).
- Etymology is always one line, classifying the formation: figurative
  extension, blend, repurposed technical term, or de novo coinage.
- No hedging, no "in the context of", no marketing tone.

## Attestation standard

**First known use** is the earliest attestable use of the headword *in this
sense*, wherever it occurred — human or machine. For vogue words this will
usually be an old human usage; that origin is itself the interesting datum.
Link it when published. When no prior use is findable, the first use is
your own correspondence with the model: `type: correspondence`, dated,
credited to your GitHub handle. Correspondence attestation is legitimate
(private letters are citable sources in the OED tradition) — its
credibility is that a named person stands behind it.

**Scrub private context.** Entries are published. No employer names,
internal project names, or details identifiable to a private conversation.
Generalize until the definition points at the phenomenon, not the situation
that birthed it. No invented example sentences.

**Adding to an existing entry.** If the headword already has an entry, PR
an added numbered sense (new sense) or note it in the PR for the
maintainer to record as a further citation — don't create a duplicate file.

## Mechanics

1. Fork, branch (`entry/<slug>`), add your file.
2. Run `python3 scripts/validate_entries.py _entries/<slug>.md` (needs
   PyYAML). CI runs the same check on your PR.
3. Open the PR titled `entry: <headword>`; the template asks for your
   first-use research trail.

Review is editorial: is the sense real, the class right, the definition in
register?
