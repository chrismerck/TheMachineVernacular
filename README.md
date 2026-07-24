# The Machine Vernacular

A dictionary of emergent machine usage — the coinages, new senses, and vogue
words observable in the speech of large language models.

**Read it:** https://chrismerck.github.io/TheMachineVernacular/

## Contribute

Every entry is one Markdown file in [`entries/`](_entries/), contributed by
pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) for the entry format,
the three classes (neologism / neosemy / vogue), and the attestation standard.

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
