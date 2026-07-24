---
title: The Machine Vernacular
subtitle: A Contributor-Driven Dictionary of Emergent Machine Usage — Design
date: July 23, 2026
abstract: |
  Language models are developing observable lexical habits: occasional de novo
  coinages, more frequent novel senses of established words, and a distinct
  fondness for certain technical jargon deployed far beyond its home domain.
  The Machine Vernacular is a public, PR-driven dictionary documenting this
  vernacular with lexicographic rigor. A single GitHub repository serves three
  roles: the corpus (one Markdown file per entry, rendered by GitHub Pages as
  a single-page dictionary in a sepia old-dictionary-paper style), the
  instrument (a Claude Code plugin, "lexicographer," that drafts entries in
  proper dictionary register and researches first attestations), and the
  contribution pipeline (the plugin offers to open a pull request against its
  own home repository). This document specifies the taxonomy, entry model,
  site design, plugin architecture, and contribution workflow.
---

# Purpose and Scope

Document the emerging lexical habits of language models — "the machine
vernacular" — as a serious, compact, publicly contributable dictionary.
Entries are short, written in genuine dictionary register (genus +
differentia, Merriam-Webster/OED conventions), and each carries attestation
metadata identifying when the usage was first observed and by which speaker
(model). Anyone can contribute via pull request; the primary contribution
path is a Claude Code plugin that produces entries and opens the PR itself.

Out of scope for v1: custom domain (later, a 5-minute change), client-side
search (⌘F suffices on a single page), per-entry pages, RSS, and any build
tooling beyond GitHub Pages' native Jekyll.

# The Novelty Taxonomy

Every entry is classified into exactly one of three classes, displayed as a
small-caps chip beside the part of speech. All three are established
lexicographic terms.

**coinage** — a de novo form previously unattested; a neologism proper.
Rare; the trophies of the collection.

**neosemy** — an established word bearing a novel sense: figurative
extension, domain transfer, or repurposing (e.g., *gardener* for one who
maintains canonical records against drift).

**vogue** — an established word in an established sense, but with markedly
expanded frequency and domain range in machine speech (e.g., *load-bearing*,
*ergonomic*). "Vogue word" is a standing term of art in lexicography.

The class determines what the definition documents. For coinage and neosemy,
the numbered sense defines the new meaning. For vogue, the sense documents
the meaning *as deployed* — the differentia clause capturing the domain
transfer ("transferred from structural engineering to any component whose
failure propagates") — since the sense itself is not new.

# Entry Model

## Information order

Merriam-Webster "TLDR" order — the goods first:

1. **Headword** (large), part of speech, class chip
2. **Numbered senses**, each with an italic subject-area label
3. **Etymology** — always one line
4. **First Known Use** — the earliest attestable use of the headword *in
   this sense*, wherever it occurred, human or machine. For vogue words this
   will usually be a human, possibly decades old; that origin is itself the
   interesting datum. Linked when published; otherwise cited as
   correspondence.
5. **Machine attestation** — the observation that occasioned the entry:
   model (the informant), date, and the GitHub handle of the observer, e.g.
   *Claude Fable 5, 23 Jul 2026, observed by @chrismerck.* For an in-session
   coinage, First Known Use and the machine attestation coincide and are
   rendered as a single line.

## File format

One entry per file, `entries/<headword>.md`, all structure in YAML
frontmatter so the layout controls typography exactly and a contribution is
a clean ~20-line diff.[^schema] Multiple senses are a numbered list within
one entry; if a headword later acquires another machine sense, the PR adds a
sense to the existing file rather than a new file.

[^schema]: Frontmatter schema:

    ```yaml
    headword: gardener
    pos: n.              # n., v., adj., n. attrib., ...
    class: neosemy       # coinage | neosemy | vogue
    senses:
      - label: organizational computing   # italic subject-area label
        definition: >
          One who maintains an organization's canonical records against
          drift — pruning stale entries, reconciling contradictions, and
          correcting the agents that operate over them — as distinct from
          authoring the records or building their infrastructure.
    etymology: >
      Figurative extension of *gardener* ("one who tends a garden"), by
      analogy between a maintained knowledge base and a cultivated plot.
    first_use:
      date: 2026-07-12          # ISO date, or YYYY-MM / YYYY if imprecise
      type: correspondence      # published | correspondence
      url:                      # required when type: published
      note:                     # optional one-line source description
    attestation:
      model: Claude Fable 5     # the informant
      date: 2026-07-12
      observer: chrismerck      # GitHub handle
    ```

    Definitions and etymologies may contain Markdown italics; the layout
    renders them with `markdownify`. The filename is the slugified headword.

## Register and citation policy

Definitions follow the dictionary register rules already proven in the
lexicographer skill: genus + differentia; no full-sentence framing; 25–45
words per sense; one-line etymology classifying the formation (figurative
extension, blend, repurposed technical term, de novo). Entries are scrubbed
of private and proprietary context before publication. Correspondence
attestation — a usage witnessed only in a contributor's private session — is
a legitimate citation class (as private letters are for the OED), labeled as
such and credited to the observer's GitHub handle; its credibility rests on
a named person standing behind it. Entries may accrue at most two or three
later citations, OED-style, to keep them short.

# The Site

## Architecture

GitHub Pages with native Jekyll — zero CI configuration, no toolchain for
contributors. Entries are a Jekyll collection; one layout renders the entire
dictionary as a single page.[^jekyll] The page is tiny (hundreds of short
entries is still a few hundred KB), instantly ⌘F-searchable, and every
headword carries an anchor (`/#gardener`) for deep links from blog posts.

[^jekyll]: `_config.yml` declares `collections: entries` (not output as
    individual pages), excludes `plugins/`, `docs/`, and dot-directories
    from the build, and sorts by headword at render time. Local preview via
    `bundle exec jekyll serve` is optional, never required for
    contribution. Site URL for v1: `chrismerck.github.io/TheMachineVernacular`
    (set `baseurl` accordingly); custom domain later.

Layout: a short masthead (title, one-sentence thesis), a compact legend
explaining the three classes and the attestation standard — where the
linguistic seriousness shows — an A–Z index bar, then the entries,
alphabetical, separated by thin rules.

## Visual design

A nod to old dictionary paper: **sepia**. Aged-cream paper ground, dark
sepia ink, a muted rubrication red reserved for small accents (class chips,
anchors' hover state). Dark mode inverts to warm dark ("lamplight")
preserving the same hierarchy.[^palette]

Typography carries the whole design: a self-hosted old-style serif (EB
Garamond class) with true small caps and old-style figures[^font]; large
bold headwords; hanging-indent numbered senses; italic subject labels;
ETYMOLOGY and FIRST KNOWN USE as small-caps side-labels in muted ink. No
JavaScript. One CSS file. The page should feel like a plate from a
19th-century dictionary that happens to render in 40 ms.

[^palette]: Indicative palette — light: paper `#f4ecd8`-family, ink
    `#3b3128`-family, rubric `#8a3324`-family; dark: ground `#211d18`-family,
    ink `#e8ddc8`-family. Final values tuned during implementation for
    WCAG AA contrast in both modes.

[^font]: Subset via WOFF2 (regular, italic, bold, small-caps feature
    retained), self-hosted, `font-display: swap`, preloaded. System-serif
    fallback stack so the unstyled flash is still dictionary-shaped.

# The Plugin: `lexicographer`

## Marketplace

The same repository doubles as a Claude Code plugin marketplace:
`.claude-plugin/marketplace.json` at the root lists the single plugin at
`plugins/lexicographer/`. Installation:
`/plugin marketplace add chrismerck/TheMachineVernacular`. The existing
local `coinage-lexicographer` skill retires in favor of the plugin — one
source of truth, and the community can PR improvements to the lexicographic
method itself.

## Repository layout

```
TheMachineVernacular/
├── .claude-plugin/marketplace.json
├── plugins/lexicographer/
│   ├── .claude-plugin/plugin.json
│   └── skills/lexicographer/
│       ├── SKILL.md            # core craft — lean, loaded on trigger
│       ├── research.md         # first-attestation research method
│       └── publishing.md       # PR flow against this repository
├── entries/*.md
├── _layouts/dictionary.html
├── assets/css/vernacular.css   # + self-hosted font files
├── index.md
├── _config.yml
├── CONTRIBUTING.md
├── README.md
└── .github/PULL_REQUEST_TEMPLATE.md
```

## Skill flow — progressive disclosure

`SKILL.md` carries the craft (sense recovery from conversational evidence,
classification, dictionary register, compression, scrubbing) and stays lean;
the two companion files load only when their phase is reached, keeping
context unpolluted.

1. **Draft** — on trigger (user points at a term), recover the sense from
   actual usage in the conversation, classify class and formation, and draft
   the entry *in thinking* — not yet shown.
2. **Research** — read `research.md`; web-search the headword in the
   candidate sense; the earliest attestable use found, human or machine,
   becomes First Known Use (with URL when published). If nothing is found,
   First Known Use is this correspondence. Research also validates the
   class: an already-established sense demotes neosemy to vogue; a
   discovered established sense match may re-anchor the etymology.
3. **Present** — output the finished entry, screenshot-clean, then after a
   rule a single line: *"Publish to The Machine Vernacular? I'll open a PR
   under your handle."* Nothing else.
4. **Publish (on yes)** — read `publishing.md`: verify `gh` auth; check for
   an existing entry for the headword (if present, prepare an added sense or
   citation rather than a duplicate); fork, branch, add
   `entries/<headword>.md`, open a PR titled `entry: <headword>` with the
   template filled in, scrubbed of private context. Report the PR URL.

# Contribution Pipeline

The PR is the unit of contribution: one new file (or one added sense) per
PR. `CONTRIBUTING.md` is the public distillation of the skill — what counts
as attested, the three classes, the register rules, the frontmatter format —
so human contributors without the plugin can participate on equal footing.
The PR template checklists: class assigned, sense in register (25–45 words),
one-line etymology, first-use research performed, attestation fields
complete, private context scrubbed. Review (by the maintainer) is editorial:
is the sense real, the class right, the definition in register?

# Implementation Notes

Implementation proceeds via a separate plan document executed by Sonnet:
scaffold repo and Jekyll site, port and restructure the skill (site
information order: senses → etymology → first use), author
research.md/publishing.md, marketplace/plugin manifests, CSS, seed entries
(*gardener* first; further seeds produced by running the pipeline itself),
enable Pages, and end-to-end test the publish flow against a real fork.
