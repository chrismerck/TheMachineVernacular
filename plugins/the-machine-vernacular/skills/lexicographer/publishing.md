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

`_entries/<slug>.md` where slug = lowercase headword, spaces → `-`. All
content in YAML frontmatter (see any existing entry, or
CONTRIBUTING.md, for the schema):

    headword, pos, class, senses[{label, definition}], etymology,
    first_use{date, type, url?, source?, note?}, attestation{model, date, observer}

`attestation.model` is the model whose usage occasioned the entry — your
own identity if the coinage happened in this session. If the occasioning
usage lives in a machine-authored artifact (PR body, design doc, commit
message), attest the model that authored the artifact; date by the
artifact's authorship date when known, else the observation date. Dates
ISO; quote imprecise dates ("2026-07"). Markdown italics allowed in definition and
etymology.

## 3. Fork, branch, PR

Work in a temp directory. If `$HANDLE` == `chrismerck` (repo owner), clone
the repo directly and branch; otherwise:

    gh repo fork chrismerck/TheMachineVernacular --clone=false
    git clone "https://github.com/$HANDLE/TheMachineVernacular" "$TMPDIR/tmv-pr"
    cd "$TMPDIR/tmv-pr"
    git checkout -b "entry/<slug>"
    # write _entries/<slug>.md
    python3 scripts/validate_entries.py "_entries/<slug>.md"   # if PyYAML available
    git add "_entries/<slug>.md"
    git commit -m "entry: <headword>" \
      -m "Co-Authored-By: <model name> <noreply@anthropic.com>"   # actual authoring model
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
