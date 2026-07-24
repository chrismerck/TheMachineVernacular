# First-Use Research

Goal: find the earliest attestable use of the headword *in the candidate
sense* — wherever it occurred, human or machine. The origin of the sense is
itself the interesting datum, especially for vogue words. Best-effort,
time-boxed: about 3–6 targeted web searches. Absence of evidence is a valid
result.

## 0. Check the dictionary itself

Fetch the existing entry list:

    gh api repos/chrismerck/TheMachineVernacular/contents/_entries --jq '.[].name'

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
