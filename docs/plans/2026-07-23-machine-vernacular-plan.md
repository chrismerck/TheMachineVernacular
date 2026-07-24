# The Machine Vernacular Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Machine Vernacular repository: a GitHub-Pages dictionary of emergent machine usage that doubles as a Claude Code plugin marketplace whose `lexicographer` plugin drafts entries and opens PRs against this same repo.

**Architecture:** One repo, three roles. `entries/*.md` (YAML-frontmatter entry files) are rendered by native GitHub-Pages Jekyll into a single-page sepia dictionary — no CI build, no JS. `plugins/lexicographer/` is a Claude Code plugin (skill + two progressively-disclosed companion docs) listed by a root `marketplace.json`. A small Python validator lints entries locally and in a PR-triggered GitHub Action.

**Tech Stack:** Jekyll (GitHub Pages native), plain CSS, EB Garamond (self-hosted WOFF2), Python 3 + PyYAML (entry linter), GitHub Actions (PR validation only), `gh` CLI, Claude Code plugin format.

**Reference:** Design doc at `docs/plans/2026-07-23-machine-vernacular-design.md`. Read it before starting.

**Working directory:** `/Users/cmerck/src/chrismerck/TheMachineVernacular` (already a git repo on `main` with the design doc committed).

---

### Task 1: Repo scaffold

**Files:**
- Create: `.gitignore`
- Create: `_config.yml`
- Create: `README.md`

- [ ] **Step 1: Write `.gitignore`**

```gitignore
_site/
.jekyll-cache/
.DS_Store
Gemfile.lock
vendor/
```

- [ ] **Step 2: Write `_config.yml`**

```yaml
title: The Machine Vernacular
description: A dictionary of emergent machine usage
url: "https://chrismerck.github.io"
baseurl: "/TheMachineVernacular"
markdown: kramdown

collections:
  entries:
    output: false

exclude:
  - plugins/
  - docs/
  - scripts/
  - README.md
  - CONTRIBUTING.md
  - Gemfile
  - Gemfile.lock
  - vendor/
```

- [ ] **Step 3: Write `README.md`**

```markdown
# The Machine Vernacular

A dictionary of emergent machine usage — the coinages, new senses, and vogue
words observable in the speech of large language models.

**Read it:** https://chrismerck.github.io/TheMachineVernacular/

## Contribute

Every entry is one Markdown file in [`entries/`](entries/), contributed by
pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) for the entry format,
the three classes (coinage / neosemy / vogue), and the attestation standard.

The easiest way to contribute is the **lexicographer** plugin for Claude
Code, hosted in this very repository:

    /plugin marketplace add chrismerck/TheMachineVernacular
    /plugin install lexicographer@the-machine-vernacular

When you notice a model coin a word or bend a sense, invoke the skill: it
drafts a dictionary entry in proper register, researches the first
attestable use, and offers to open a PR here under your handle.

## Local preview (optional, never required)

    gem install bundler jekyll && bundle init
    bundle add jekyll --version "~> 4.3" && bundle exec jekyll serve
```

- [ ] **Step 4: Commit**

```bash
git add .gitignore _config.yml README.md
git commit -m "chore: scaffold repo (config, readme, gitignore)"
```

---

### Task 2: Seed entry

**Files:**
- Create: `entries/gardener.md`

- [ ] **Step 1: Write `entries/gardener.md`**

This file is the schema's reference implementation; every later file (validator, layout, CONTRIBUTING) must agree with it exactly.

```yaml
---
headword: gardener
pos: n.
class: neosemy
senses:
  - label: organizational computing
    definition: >
      One who maintains an organization's canonical records against drift —
      pruning stale entries, reconciling contradictions, and correcting the
      agents that operate over them — as distinct from authoring the records
      or building their infrastructure.
etymology: >
  Figurative extension of *gardener* ("one who tends a garden"), by analogy
  between a maintained knowledge base and a cultivated plot.
first_use:
  date: 2026-07-23
  type: correspondence
attestation:
  model: Claude Fable 5
  date: 2026-07-23
  observer: chrismerck
---
```

Schema notes (also enforced by the Task 3 validator):
- `class` ∈ `coinage | neosemy | vogue`.
- `first_use.type` ∈ `published | correspondence`. When `published`, `first_use.url` is required and `first_use.note` (one-line source description) is recommended. When `correspondence`, the first use *is* the attestation and the layout renders one merged line.
- Dates are ISO (`2026-07-23`); `2026-07` or `2026` allowed when imprecise (quote them: `date: "2026-07"`).
- Filename is the slugified headword (lowercase, spaces → `-`).
- Body below the frontmatter is unused in v1 (reserved for future usage notes).

- [ ] **Step 2: Commit**

```bash
git add entries/gardener.md
git commit -m "entry: gardener"
```

---

### Task 3: Entry validator (TDD)

**Files:**
- Create: `scripts/validate_entries.py`
- Test fixture: `scripts/testdata/bad-entry.md`

- [ ] **Step 1: Check PyYAML is available**

Run: `python3 -c "import yaml; print(yaml.__version__)"`
If it fails: `pip3 install --user pyyaml` (or `python3 -m pip install --user pyyaml`).

- [ ] **Step 2: Write the failing test fixture**

Create `scripts/testdata/bad-entry.md` — wrong class, missing url on published, filename mismatch:

```yaml
---
headword: Load Bearing
pos: adj.
class: fashionable
senses:
  - label: software engineering
    definition: Something important.
etymology: >
  From structural engineering.
first_use:
  date: 2026-01-01
  type: published
attestation:
  model: Claude Fable 5
  date: 2026-01-01
  observer: nobody
---
```

- [ ] **Step 3: Write `scripts/validate_entries.py`**

```python
#!/usr/bin/env python3
"""Validate Machine Vernacular entry files against the schema.

Usage: validate_entries.py [file-or-dir ...]   (default: entries/)
Exit 0 = all valid. Errors fail; style warnings (word counts) do not.
"""
import re
import sys
from pathlib import Path

import yaml

CLASSES = {"coinage", "neosemy", "vogue"}
FIRST_USE_TYPES = {"published", "correspondence"}
DATE_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\A---\n(.*?)\n---\n?", text, re.DOTALL)
    if not m:
        raise ValueError("no YAML frontmatter block")
    return yaml.safe_load(m.group(1))


def check(path):
    errors, warnings = [], []
    try:
        fm = frontmatter(path)
    except Exception as e:
        return [f"unparseable: {e}"], []

    def need(field):
        cur = fm
        for part in field.split("."):
            if not isinstance(cur, dict) or part not in cur or cur[part] in (None, ""):
                errors.append(f"missing field: {field}")
                return None
            cur = cur[part]
        return cur

    headword = need("headword")
    need("pos")
    cls = need("class")
    if cls and cls not in CLASSES:
        errors.append(f"class must be one of {sorted(CLASSES)}, got {cls!r}")

    senses = fm.get("senses")
    if not isinstance(senses, list) or not senses:
        errors.append("senses must be a non-empty list")
    else:
        for i, s in enumerate(senses, 1):
            if not isinstance(s, dict) or not s.get("label") or not s.get("definition"):
                errors.append(f"sense {i}: needs label and definition")
                continue
            n = len(s["definition"].split())
            if not 15 <= n <= 60:
                warnings.append(f"sense {i}: {n} words (target 25-45)")

    ety = need("etymology")
    if ety and ety.strip().count("\n") > 0 and len(ety.split()) > 40:
        warnings.append("etymology should be one line")

    fu_type = need("first_use.type")
    if fu_type and fu_type not in FIRST_USE_TYPES:
        errors.append(f"first_use.type must be one of {sorted(FIRST_USE_TYPES)}")
    if fu_type == "published" and not (fm.get("first_use") or {}).get("url"):
        errors.append("first_use.url required when type is published")

    for field in ("first_use.date", "attestation.model", "attestation.date",
                  "attestation.observer"):
        need(field)
    for field in ("first_use", "attestation"):
        d = (fm.get(field) or {}).get("date")
        if d is not None and not DATE_RE.match(str(d)):
            errors.append(f"{field}.date must be YYYY[-MM[-DD]], got {d!r}")

    if headword and path.stem != slugify(headword):
        errors.append(f"filename {path.name!r} != slug {slugify(headword)!r}.md")

    return errors, warnings


def main(argv):
    targets = [Path(a) for a in argv] or [Path("entries")]
    files = []
    for t in targets:
        files += sorted(t.glob("*.md")) if t.is_dir() else [t]
    failed = False
    for f in files:
        errors, warnings = check(f)
        for w in warnings:
            print(f"WARN  {f}: {w}")
        for e in errors:
            print(f"ERROR {f}: {e}")
            failed = True
        if not errors:
            print(f"ok    {f}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run against the bad fixture — must fail**

Run: `python3 scripts/validate_entries.py scripts/testdata/bad-entry.md; echo "exit=$?"`
Expected: `exit=1` with ERROR lines for: bad class, missing `first_use.url`, filename mismatch.

- [ ] **Step 5: Run against real entries — must pass**

Run: `python3 scripts/validate_entries.py; echo "exit=$?"`
Expected: `ok    entries/gardener.md`, `exit=0`.

- [ ] **Step 6: Commit**

```bash
git add scripts/
git commit -m "feat: entry schema validator with test fixture"
```

---

### Task 4: PR validation workflow

**Files:**
- Create: `.github/workflows/validate.yml`

- [ ] **Step 1: Write the workflow**

```yaml
name: validate entries
on:
  pull_request:
    paths: ["entries/**"]
  push:
    branches: [main]
    paths: ["entries/**", "scripts/**"]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pyyaml
      - run: python3 scripts/validate_entries.py
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/validate.yml
git commit -m "ci: validate entries on PR"
```

---

### Task 5: Self-hosted fonts

**Files:**
- Create: `assets/fonts/ebgaramond-regular.woff2`, `assets/fonts/ebgaramond-italic.woff2`, `assets/fonts/ebgaramond-bold.woff2`

- [ ] **Step 1: Download EB Garamond latin WOFF2 files from the Google Fonts API**

```bash
mkdir -p assets/fonts
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
curl -s -A "$UA" "https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,700;1,400&display=swap" -o /tmp/ebg.css
python3 - <<'EOF'
import re
css = open('/tmp/ebg.css').read()
# blocks look like: /* latin */ @font-face { font-style: X; font-weight: Y; ... url(...woff2) ... }
names = {('normal','400'):'ebgaramond-regular',('italic','400'):'ebgaramond-italic',('normal','700'):'ebgaramond-bold'}
for block in re.findall(r'/\* latin \*/\s*@font-face\s*{(.*?)}', css, re.DOTALL):
    style = re.search(r'font-style:\s*(\w+)', block).group(1)
    weight = re.search(r'font-weight:\s*(\d+)', block).group(1)
    url = re.search(r'url\((\S+?\.woff2)\)', block).group(1)
    print(url, names[(style, weight)])
EOF
```

Then for each printed `URL NAME` pair: `curl -s -o assets/fonts/NAME.woff2 URL`.
Verify: `file assets/fonts/*.woff2` → all three report `Web Open Font Format (Version 2)`.

**If the download fails** (API shape changed, no network): skip this task and delete the three `@font-face` blocks from the CSS in Task 7 — the fallback stack (`Iowan Old Style, Palatino Linotype, Palatino, Georgia, serif`) is acceptable. Note the skip in the commit message.

- [ ] **Step 2: Commit**

```bash
git add assets/fonts/
git commit -m "feat: self-host EB Garamond (latin woff2 subset)"
```

---

### Task 6: Jekyll layout and index page

**Files:**
- Create: `_layouts/default.html`
- Create: `index.html`

- [ ] **Step 1: Write `_layouts/default.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ site.title }}</title>
  <meta name="description" content="{{ site.description }}">
  <link rel="preload" href="{{ '/assets/fonts/ebgaramond-regular.woff2' | relative_url }}" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{{ '/assets/css/vernacular.css' | relative_url }}">
</head>
<body>
{{ content }}
<footer>
  <p>Maintained on <a href="https://github.com/chrismerck/TheMachineVernacular">GitHub</a>.
  Contributions by pull request — see the
  <a href="https://github.com/chrismerck/TheMachineVernacular/blob/main/CONTRIBUTING.md">contribution guide</a>,
  or install the <em>lexicographer</em> plugin for Claude Code:
  <code>/plugin marketplace add chrismerck/TheMachineVernacular</code></p>
</footer>
</body>
</html>
```

- [ ] **Step 2: Write `index.html`**

```html
---
layout: default
---
{% assign entries = site.entries | sort_natural: "headword" %}

<header class="masthead">
  <h1>The Machine Vernacular</h1>
  <p class="thesis">A dictionary of emergent machine usage — the coinages,
  new senses, and vogue words observable in the speech of large language
  models, each attested to a dated first use.</p>
</header>

<section class="legend">
  <p><span class="chip chip-coinage">coinage</span> a form previously
  unattested; a neologism proper.</p>
  <p><span class="chip chip-neosemy">neosemy</span> an established word
  bearing a novel sense — figurative extension, domain transfer,
  repurposing.</p>
  <p><span class="chip chip-vogue">vogue</span> an established sense with
  markedly expanded frequency and range in machine speech.</p>
  <p class="standard">Each entry cites the earliest attestable use of its
  sense — published and linked where findable, otherwise witnessed in
  correspondence between a named contributor and a model — and identifies
  the model whose usage occasioned the entry.</p>
</section>

<nav class="alpha">
  {% assign seen = "" | split: "" %}
  {% for e in entries %}
    {% assign l = e.headword | slice: 0 | upcase %}
    {% unless seen contains l %}
      {% assign seen = seen | push: l %}
      <a href="#letter-{{ l }}">{{ l }}</a>
    {% endunless %}
  {% endfor %}
</nav>

<main>
{% assign prev = "" %}
{% for e in entries %}
  {% assign l = e.headword | slice: 0 | upcase %}
  <article class="entry" id="{{ e.headword | slugify }}">
    {% if l != prev %}<span class="letter-anchor" id="letter-{{ l }}"></span>{% assign prev = l %}{% endif %}
    <h2 class="headword"><a href="#{{ e.headword | slugify }}">{{ e.headword }}</a>
      <span class="pos">({{ e.pos }})</span>
      <span class="chip chip-{{ e.class }}">{{ e.class }}</span></h2>
    <ol class="senses">
      {% for s in e.senses %}
      <li><span class="label">({{ s.label }})</span>
        {{ s.definition | markdownify | remove: "<p>" | remove: "</p>" }}</li>
      {% endfor %}
    </ol>
    <p class="apparatus"><span class="section-label">Etymology</span>
      {{ e.etymology | markdownify | remove: "<p>" | remove: "</p>" }}</p>
    {% if e.first_use.type == "correspondence" %}
    <p class="apparatus"><span class="section-label">First known use</span>
      Attested {{ e.first_use.date | date: "%-d %B %Y" }}, in correspondence
      between <a href="https://github.com/{{ e.attestation.observer }}">@{{ e.attestation.observer }}</a>
      and {{ e.attestation.model }}.</p>
    {% else %}
    <p class="apparatus"><span class="section-label">First known use</span>
      {{ e.first_use.date | date: "%-d %B %Y" }},
      <a href="{{ e.first_use.url }}">{% if e.first_use.note %}{{ e.first_use.note }}{% else %}{{ e.first_use.url }}{% endif %}</a>.</p>
    <p class="apparatus"><span class="section-label">Machine attestation</span>
      {{ e.attestation.model }}, {{ e.attestation.date | date: "%-d %B %Y" }},
      observed by <a href="https://github.com/{{ e.attestation.observer }}">@{{ e.attestation.observer }}</a>.</p>
    {% endif %}
  </article>
{% endfor %}
</main>
```

Notes:
- `date:` filters pass unparseable values (e.g. `"2026-07"`) through unchanged — imprecise dates render as written, which is correct.
- The correspondence branch merges First Known Use and machine attestation into one line, per the design.

- [ ] **Step 3: Commit**

```bash
git add _layouts/default.html index.html
git commit -m "feat: single-page dictionary layout"
```

---

### Task 7: CSS — sepia dictionary

**Files:**
- Create: `assets/css/vernacular.css`

- [ ] **Step 1: Write `assets/css/vernacular.css`**

```css
/* The Machine Vernacular — sepia dictionary paper, lamplight dark mode */

@font-face {
  font-family: "EB Garamond";
  src: url("../fonts/ebgaramond-regular.woff2") format("woff2");
  font-weight: 400; font-style: normal; font-display: swap;
}
@font-face {
  font-family: "EB Garamond";
  src: url("../fonts/ebgaramond-italic.woff2") format("woff2");
  font-weight: 400; font-style: italic; font-display: swap;
}
@font-face {
  font-family: "EB Garamond";
  src: url("../fonts/ebgaramond-bold.woff2") format("woff2");
  font-weight: 700; font-style: normal; font-display: swap;
}

:root {
  --paper: #f6eeda;
  --ink: #3d3427;
  --ink-muted: #7c705b;
  --rubric: #8a3324;
  --rule: #d9caa9;
  --highlight: #efe2c0;
}
@media (prefers-color-scheme: dark) {
  :root {
    --paper: #211c15;
    --ink: #e9dfc9;
    --ink-muted: #9c917c;
    --rubric: #cd7a63;
    --rule: #3d352a;
    --highlight: #2e2820;
  }
}

* { box-sizing: border-box; margin: 0; }

html { font-size: 18px; }
body {
  font-family: "EB Garamond", "Iowan Old Style", "Palatino Linotype",
    Palatino, Georgia, serif;
  background: var(--paper);
  color: var(--ink);
  line-height: 1.5;
  max-width: 42rem;
  margin: 0 auto;
  padding: 3.5rem 1.25rem 5rem;
  font-feature-settings: "liga" 1, "onum" 1;
  text-rendering: optimizeLegibility;
}

a { color: var(--rubric); text-decoration-thickness: 1px; text-underline-offset: 2px; }

/* --- masthead & legend --- */
.masthead h1 {
  font-size: 2.7rem; font-weight: 700; line-height: 1.1;
  letter-spacing: .005em;
}
.masthead .thesis {
  margin-top: .75rem; font-style: italic; color: var(--ink-muted);
}
.legend {
  margin: 2.25rem 0; padding: 1.1rem 1.25rem;
  border: 1px solid var(--rule);
}
.legend p { margin: .35rem 0; }
.legend .standard {
  margin-top: .8rem; padding-top: .8rem;
  border-top: 1px solid var(--rule);
  font-size: .92rem; color: var(--ink-muted);
}

/* --- alphabet bar --- */
.alpha { margin: 1.5rem 0 .5rem; }
.alpha a {
  display: inline-block; padding: 0 .3rem;
  font-weight: 700; text-decoration: none;
}
.alpha a:hover { color: var(--ink); }

/* --- entries --- */
.entry { padding: 1.5rem 0; border-top: 1px solid var(--rule); position: relative; }
.entry:target { background: var(--highlight); }
.letter-anchor { position: absolute; top: -1rem; }

.headword { font-size: 1.65rem; font-weight: 700; line-height: 1.2; }
.headword a { color: inherit; text-decoration: none; }
.headword a:hover { color: var(--rubric); }
.pos { font-weight: 400; font-style: italic; font-size: 1.05rem; }

.chip {
  display: inline-block; vertical-align: .25em;
  font-size: .58em; font-weight: 400; font-style: normal;
  letter-spacing: .09em; text-transform: uppercase;
  color: var(--rubric); border: 1px solid currentColor;
  border-radius: 2px; padding: .05em .5em; margin-left: .35em;
}

.senses { margin: .6rem 0 .6rem 0; padding-left: 2rem; }
.senses li { margin: .4rem 0; }
.senses .label { font-style: italic; }

.apparatus { margin: .45rem 0 0; font-size: .95rem; }
.section-label {
  font-size: .72em; letter-spacing: .09em; text-transform: uppercase;
  color: var(--ink-muted); margin-right: .4em;
}

/* --- footer --- */
footer {
  margin-top: 3rem; padding-top: 1.25rem;
  border-top: 1px solid var(--rule);
  font-size: .9rem; color: var(--ink-muted);
}
footer code {
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: .85em;
}

@media (max-width: 480px) {
  html { font-size: 16.5px; }
  body { padding-top: 2rem; }
  .masthead h1 { font-size: 2.1rem; }
}
```

If Task 5 was skipped, delete the three `@font-face` blocks and the `preload` line in `_layouts/default.html`.

- [ ] **Step 2: Build check (best-effort)**

If `bundle exec jekyll build` or `jekyll build` is available locally, run it and confirm `_site/index.html` contains `id="gardener"` and the etymology text with `<em>gardener</em>`. If Jekyll is not installed, skip — Task 11 verifies the live build.

- [ ] **Step 3: Commit**

```bash
git add assets/css/vernacular.css
git commit -m "feat: sepia dictionary stylesheet"
```

---

### Task 8: Contribution docs

**Files:**
- Create: `CONTRIBUTING.md`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`

- [ ] **Step 1: Write `CONTRIBUTING.md`**

````markdown
# Contributing to The Machine Vernacular

An entry documents a word or sense observable in the speech of language
models. One entry = one file in `entries/` = one pull request. The easy
path is the [lexicographer plugin](README.md#contribute); this document is
the standard it (and you) must meet.

## What qualifies

Classify your observation as exactly one of:

- **coinage** — a de novo form previously unattested; a neologism proper.
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

`entries/<slug>.md`, where slug = lowercase headword, spaces → `-`.
All content in YAML frontmatter:

```yaml
---
headword: gardener
pos: n.                # n., v., adj., n. attrib., ...
class: neosemy         # coinage | neosemy | vogue
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
2. Run `python3 scripts/validate_entries.py entries/<slug>.md` (needs
   PyYAML). CI runs the same check on your PR.
3. Open the PR titled `entry: <headword>`; the template asks for your
   first-use research trail.

Review is editorial: is the sense real, the class right, the definition in
register?
````

- [ ] **Step 2: Write `.github/PULL_REQUEST_TEMPLATE.md`**

```markdown
## Entry

**Headword:**
**Class:** coinage / neosemy / vogue

## First-use research

What was searched, and what was (or wasn't) found. If `type: published`,
how was the linked source dated? If `type: correspondence`, confirm the
usage arose organically in your session (not prompted for).

-

## Checklist

- [ ] Class assigned per CONTRIBUTING.md (research validates the class)
- [ ] Sense(s) in dictionary register, ~25–45 words, genus + differentia
- [ ] Etymology is one line and classifies the formation
- [ ] `first_use` and `attestation` fields complete; url present if published
- [ ] Private/proprietary context scrubbed
- [ ] `python3 scripts/validate_entries.py` passes
```

- [ ] **Step 3: Commit**

```bash
git add CONTRIBUTING.md .github/PULL_REQUEST_TEMPLATE.md
git commit -m "docs: contribution guide and PR template"
```

---

### Task 9: Plugin manifests

**Files:**
- Create: `.claude-plugin/marketplace.json`
- Create: `plugins/lexicographer/.claude-plugin/plugin.json`

- [ ] **Step 1: Write `.claude-plugin/marketplace.json`**

```json
{
  "name": "the-machine-vernacular",
  "owner": {
    "name": "Chris Merck",
    "url": "https://github.com/chrismerck"
  },
  "plugins": [
    {
      "name": "lexicographer",
      "source": "./plugins/lexicographer",
      "description": "Craft compact dictionary entries for words and senses coined by language models, research their first attestable use, and optionally publish them to The Machine Vernacular by pull request."
    }
  ]
}
```

- [ ] **Step 2: Write `plugins/lexicographer/.claude-plugin/plugin.json`**

```json
{
  "name": "lexicographer",
  "version": "0.1.0",
  "description": "Dictionary entries for machine coinages, neosemy, and vogue words — drafted in professional lexicographic register, first-use researched, publishable to The Machine Vernacular via PR.",
  "author": {
    "name": "Chris Merck",
    "url": "https://github.com/chrismerck"
  },
  "homepage": "https://chrismerck.github.io/TheMachineVernacular/"
}
```

- [ ] **Step 3: Validate JSON**

Run: `jq empty .claude-plugin/marketplace.json plugins/lexicographer/.claude-plugin/plugin.json && echo OK`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/ plugins/lexicographer/.claude-plugin/
git commit -m "feat: plugin marketplace and lexicographer manifest"
```

---

### Task 10: The lexicographer skill

**Files:**
- Create: `plugins/lexicographer/skills/lexicographer/SKILL.md`
- Create: `plugins/lexicographer/skills/lexicographer/research.md`
- Create: `plugins/lexicographer/skills/lexicographer/publishing.md`

This is the heart of the plugin. The three files implement progressive
disclosure: SKILL.md carries the craft and stays lean; research.md loads
before presenting; publishing.md loads only if the user accepts the offer.

- [ ] **Step 1: Write `SKILL.md`**

````markdown
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

- `coinage` — de novo form, previously unattested; a neologism proper.
- `neosemy` — established word, novel sense: figurative extension, domain
  transfer, repurposing.
- `vogue` — established word in an established sense, but with markedly
  expanded frequency and domain range in machine speech (*load-bearing*,
  *ergonomic*). For vogue entries, the sense documents the meaning *as
  deployed*, with the differentia capturing the domain transfer
  ("transferred from structural engineering to any component whose failure
  propagates").

**Formation** (drives the one-line etymology):

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
- Etymology: always present, always one line.
- Number senses even when there is only one (the numeral signals "one sense
  among the word's senses"). Two related senses: most-general first.
- Part of speech abbreviated: (n.), (v.), (adj.), (n. attrib.).

## 4. Scrub private context

The entry may be published. Remove company names, internal project names,
and anything identifiable to the user's employer or private conversation,
unless the user says otherwise. No example sentences drawn from the private
conversation. Generalize until the definition points at the phenomenon, not
the situation that birthed it.

## Presentation format

Information order is definition-first (Merriam-Webster "TLDR" order):

```
**headword** (pos.) — CLASS

1. *(subject label)* Definition in dictionary register.

*Etymology:* One line.

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
- Etymology bloat: more than one line.
- Leaking private context.
- Chatty framing around the entry.
- Presenting before doing the research phase.
````

- [ ] **Step 2: Write `research.md`**

````markdown
# First-Use Research

Goal: find the earliest attestable use of the headword *in the candidate
sense* — wherever it occurred, human or machine. The origin of the sense is
itself the interesting datum, especially for vogue words. Best-effort,
time-boxed: about 3–6 targeted web searches. Absence of evidence is a valid
result.

## 0. Check the dictionary itself

Fetch the existing entry list:

    gh api repos/chrismerck/TheMachineVernacular/contents/entries --jq '.[].name'

(or fetch https://chrismerck.github.io/TheMachineVernacular/ and scan). If
the headword already has an entry, you are drafting an *added sense* or a
*further citation*, not a new entry — say so when presenting.

## 1. Establish the baseline senses

Search the word in standard references (Wiktionary, Merriam-Webster,
etymonline). This determines the class:

- Form not attested anywhere → **coinage**.
- Form exists, candidate sense absent from references → **neosemy**
  (provisionally — continue to step 2).
- Candidate sense already documented → **vogue**. Research validates the
  class, not just the date. Demote honestly.

## 2. Hunt the sense's first use

Search the headword together with collocates from your differentia — the
words that only co-occur in the candidate sense. Useful angles:

- Exact phrases the sense would appear in, quoted.
- Technical venues where senses are born: arXiv, GitHub, Hacker News,
  engineering blogs, papers, mailing lists.
- If an established sense exists in a home domain (vogue), search for early
  *domain-transferred* uses — the first time it escaped its field.

For each candidate source, pin down a date (page date, archive date, commit
date). Earliest dated source wins. Imprecise dates are fine: `2019`,
`2014-03`.

## 3. Record the result

- Found a published prior use → `first_use: {date, type: published, url,
  note}` where note is a one-line source description ("blog post by Dan
  Luu"). The entry will also carry a separate machine-attestation line
  (model, date, observer).
- Nothing found → `first_use: {date: <today>, type: correspondence}` — the
  first known use *is* this conversation, merged with the attestation line.

Keep the search trail (queries tried, best candidates rejected and why) —
it goes in the PR body if the user publishes.
````

- [ ] **Step 3: Write `publishing.md`**

````markdown
# Publishing to The Machine Vernacular

Open a pull request adding the entry to
github.com/chrismerck/TheMachineVernacular. The PR is the contribution
unit: one entry file (or one added sense), nothing else.

## 1. Preconditions

- `gh auth status` succeeds. If not, stop and ask the user to run
  `gh auth login`.
- Handle: `HANDLE=$(gh api user --jq .login)` — this is the
  `attestation.observer` and the fork owner. Confirm it matches the handle
  the user expects to stand behind the attestation.

## 2. Write the entry file

`entries/<slug>.md` where slug = lowercase headword, spaces → `-`. All
content in YAML frontmatter (see any existing entry, or
CONTRIBUTING.md, for the schema):

    headword, pos, class, senses[{label, definition}], etymology,
    first_use{date, type, url?, note?}, attestation{model, date, observer}

`attestation.model` is the model whose usage occasioned the entry — your
own identity if the coinage happened in this session. Dates ISO; quote
imprecise dates ("2026-07"). Markdown italics allowed in definition and
etymology.

## 3. Fork, branch, PR

Work in a temp directory. If `$HANDLE` == `chrismerck` (repo owner), clone
the repo directly and branch; otherwise:

    gh repo fork chrismerck/TheMachineVernacular --clone=false
    git clone "https://github.com/$HANDLE/TheMachineVernacular" "$TMPDIR/tmv-pr"
    cd "$TMPDIR/tmv-pr"
    git checkout -b "entry/<slug>"
    # write entries/<slug>.md
    python3 scripts/validate_entries.py "entries/<slug>.md"   # if PyYAML available
    git add "entries/<slug>.md"
    git commit -m "entry: <headword>"
    git push -u origin "entry/<slug>"
    gh pr create --repo chrismerck/TheMachineVernacular \
      --title "entry: <headword>" --body-file <body.md>

If the headword already has an entry file, edit it instead: add the new
numbered sense (most-general first) and note the change in the PR body.

## 4. PR body

Fill the repo's PR template sections honestly:

- Headword and class.
- First-use research trail: queries tried, what was found or not found,
  how the linked source was dated.
- Complete the checklist only for items actually done.
- Sign off: `Submitted via the lexicographer plugin by @<handle>, with
  <model name>.` — use the actual model authoring the PR, never a
  hardcoded name.

## 5. Report and clean up

Report the PR URL to the user. Remove the temp clone.
````

- [ ] **Step 4: Verify skill frontmatter parses**

Run:
```bash
python3 - <<'EOF'
import re, yaml
for p in ["plugins/lexicographer/skills/lexicographer/SKILL.md"]:
    text = open(p).read()
    fm = yaml.safe_load(re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL).group(1))
    assert fm["name"] == "lexicographer" and fm["description"], fm
print("OK")
EOF
```
Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add plugins/lexicographer/skills/
git commit -m "feat: lexicographer skill with research and publishing phases"
```

---

### Task 11: Publish to GitHub and enable Pages

**Files:** none (remote operations)

- [ ] **Step 1: Create the GitHub repo and push**

```bash
gh repo create chrismerck/TheMachineVernacular --public --source . --push \
  --description "A dictionary of emergent machine usage"
```

- [ ] **Step 2: Enable GitHub Pages (branch build, Jekyll)**

```bash
gh api -X POST repos/chrismerck/TheMachineVernacular/pages \
  -f "source[branch]=main" -f "source[path]=/"
```

If it returns 409 (already exists), that's fine.

- [ ] **Step 3: Wait for the Pages build and verify the live site**

Poll until built (a few minutes max):

```bash
gh api repos/chrismerck/TheMachineVernacular/pages/builds/latest --jq .status
```

Expected: `built`. If `errored`, fetch `.error.message` from the same endpoint, fix, push, re-poll.

Then:

```bash
curl -s https://chrismerck.github.io/TheMachineVernacular/ | grep -c 'id="gardener"'
```

Expected: `1`. Also fetch the CSS URL (grep the HTML for `vernacular.css` and curl it) and confirm HTTP 200.

- [ ] **Step 4: Visual check**

Open https://chrismerck.github.io/TheMachineVernacular/ in a browser (`open <url>`). Confirm: sepia paper, serif headwords, chips render, `/#gardener` anchor highlights the entry, dark mode looks right (toggle OS appearance or DevTools emulation). Screenshot for the user.

---

### Task 12: Plugin end-to-end check and local-skill retirement

**Files:**
- Move: `~/.claude/skills/coinage-lexicographer` → `~/.claude/skills-archive/coinage-lexicographer`

- [ ] **Step 1: Structural check of the marketplace**

```bash
jq -e '.plugins[0].source == "./plugins/lexicographer"' .claude-plugin/marketplace.json
test -f plugins/lexicographer/skills/lexicographer/SKILL.md && echo layout-ok
```

Expected: `true`, `layout-ok`.

- [ ] **Step 2: Archive the superseded local skill**

The plugin replaces the user-level `coinage-lexicographer` skill; both active at once would double-trigger. Archive (don't delete):

```bash
mkdir -p ~/.claude/skills-archive
mv ~/.claude/skills/coinage-lexicographer ~/.claude/skills-archive/
```

- [ ] **Step 3: Hand off interactive verification to the user**

The marketplace-add flow is interactive; ask the user to run, in any Claude Code session:

```
/plugin marketplace add chrismerck/TheMachineVernacular
/plugin install lexicographer@the-machine-vernacular
```

then trigger the skill on a test term and, if they choose, exercise the publish flow — the resulting `entry:` PR against the repo is the true end-to-end test.

- [ ] **Step 4: Final commit if anything changed, and report**

Report: live site URL, marketplace add command, and the two follow-ups deliberately deferred (custom domain; further seed entries produced by running the pipeline itself).
