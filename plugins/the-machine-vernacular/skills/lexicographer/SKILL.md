---
name: lexicographer
description: Craft a concise, screenshot-ready dictionary entry (Wiktionary/OED register) for a word or sense a model organically coined, extended, or is conspicuously fond of. Use whenever the user points at a term and asks to "define" it "as you used it", asks for a "dictionary definition" of a session term, mentions The Machine Vernacular, collecting coinages/neologisms from AI conversations, or pastes a word and says "dictionary entry, please."
---

# Lexicographer

Turn a term observed in machine speech into a compact dictionary entry,
written the way a professional lexicographer would write it — then offer to
publish it to The Machine Vernacular
(https://chrismerck.github.io/TheMachineVernacular/), the public dictionary
of emergent machine usage.

## Workflow

1. **Recover the sense from evidence** (below), classify, and draft the
   entry in your thinking — do NOT present it yet.
2. **Read `research.md`** (in this skill's directory) and perform the
   first-use research it prescribes. It may change the class and will fill
   the First Known Use line.
3. **Present the entry** in the format below, screenshot-clean, followed by
   a horizontal rule and exactly one line:
   *Publish to The Machine Vernacular? I'll open a PR under your handle.*
4. **If the user accepts**, read `publishing.md` and follow it.

## 1. Recover the sense from evidence

Do not define the word from general knowledge. The subject is a *specific
usage* in a specific conversation. Find every place the term was used
(scroll the conversation; search past chats if a tool is available). From
actual usage, extract:

- **Genus**: what kind of thing is it? (a role, a property, a process, an
  artifact, a failure mode)
- **Differentia**: what distinguishes it from neighbors in the same genus?
  The best entries earn their keep by contrast — capture it in an "as
  distinct from ..." clause when it applies.
- **What's new**: how does this usage differ from the word's established
  senses? This drives the class, the etymology line, and whether the entry
  deserves to exist.

## 2. Classify

**Class** (one per entry; research.md validates this):

- `neologism` — de novo form, previously unattested; a coinage proper.
- `neosemy` — established word, novel sense: figurative extension, domain
  transfer, repurposing.
- `vogue` — established word in an established sense, but with markedly
  expanded frequency and domain range in machine speech (*load-bearing*,
  *ergonomic*). For vogue entries, the sense documents the meaning *as
  deployed*, with the differentia capturing the domain transfer
  ("transferred from structural engineering to any component whose failure
  propagates").

**Formation** (drives the one-line etymology — neologism and neosemy only;
vogue entries carry the word's history in `first_use.note` instead):

- Figurative extension: `Figurative extension of *word* ("gloss"), by
  analogy between X and Y.`
- Blend/compound: `Blend of *a* + *b*.` or `From *a* + *b*.`
- Repurposed technical term: `From *field* usage, transferred to *new
  field*.`
- De novo: state the formation as best it can be reconstructed, one clause.

## 3. Dictionary register

- Genus + differentia, not narrative. Start with the genus noun phrase:
  "One who ...", "A property of ...", "The practice of ...". The headword
  is the implied subject — never "X is a ...".
- One italic subject-area label per sense, broad field, lowercase:
  *(organizational computing)*, *(software engineering)*, *(AI agents)*.
- Semicolons and em-dashes carry elaboration; no second sentence unless it
  earns it. No hedging, no "in the context of", no marketing tone.
- Target 25–45 words per sense. Draft long, cut 50–70%. Compression is the
  actual work.
- Etymology: neologism and neosemy only, always one line. Vogue entries
  omit it — fold anything essential into `first_use.note`, where it reads
  alongside the citation.
- Number senses even when there is only one (the numeral signals "one sense
  among the word's senses"). Two related senses: most-general first.
- Part of speech abbreviated: (n.), (v.), (adj.), (n. attrib.).

## 4. Scrub private context

The entry may be published. Remove company names, internal project names,
and anything identifiable to the user's employer or private conversation,
unless the user says otherwise. An example sentence, if one is carried, must
be generalized from the attested usage and scrubbed to the same standard —
never invented from whole cloth, never verbatim from the private
conversation. Generalize until the definition points at the phenomenon, not
the situation that birthed it.

## Presentation format

Information order is definition-first (Merriam-Webster "TLDR" order):

```
**headword** (pos.) — CLASS

1. *(subject label)* Definition in dictionary register.
   *"Example sentence, if one is carried — italic, quoted."*

*Etymology:* One line (neologism/neosemy only; omit for vogue).

*First known use:* From research.md — a dated, linked published source, or
"Attested <date>, in correspondence between @<handle> and <model>."
```

Reply with the entry, the rule, and the one-line publish offer — no
preamble, no commentary. The user screenshots these. If something is
ambiguous (part of speech, which of two senses), decide; only ask if
genuinely undecidable.

## Failure modes

- Defining the ordinary sense instead of the observed one.
- Explaining instead of defining: paragraphs, "this term refers to...".
- Etymology bloat: more than one line, or any etymology at all on a vogue
  entry.
- Leaking private context.
- Chatty framing around the entry.
- Presenting before doing the research phase.
