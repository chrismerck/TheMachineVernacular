#!/usr/bin/env python3
"""Validate Machine Vernacular entry files against the schema.

Usage: validate_entries.py [file-or-dir ...]   (default: _entries/)
Exit 0 = all valid. Errors fail; style warnings (word counts) do not.
"""
import re
import sys
from pathlib import Path

import yaml

CLASSES = {"neologism", "neosemy", "vogue"}
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
            ex = s.get("example")
            if ex is not None:
                if not isinstance(ex, str) or not ex.strip():
                    errors.append(f"sense {i}: example must be a non-empty string")
                elif len(ex.split()) > 60:
                    warnings.append(
                        f"sense {i}: example {len(ex.split())} words "
                        "(keep it to a sentence or two)")

    ety = fm.get("etymology")
    if cls == "vogue":
        if ety:
            warnings.append(
                "etymology is not rendered for vogue entries — fold anything "
                "essential into first_use.note")
    else:
        ety = need("etymology")
    if ety and ety.strip().count("\n") > 0 and len(ety.split()) > 40:
        warnings.append("etymology should be one line")

    fu_type = need("first_use.type")
    if fu_type and fu_type not in FIRST_USE_TYPES:
        errors.append(f"first_use.type must be one of {sorted(FIRST_USE_TYPES)}")
    if fu_type == "published":
        fu = fm.get("first_use") or {}
        if not fu.get("url"):
            errors.append("first_use.url required when type is published")
        if not fu.get("source"):
            warnings.append(
                "first_use.source missing — it becomes the link text "
                "(without it, only the url's domain is shown)")
    note = (fm.get("first_use") or {}).get("note") or ""
    if note.strip().endswith("."):
        warnings.append(
            "first_use.note should not end with '.' — the template adds "
            "terminal punctuation")

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
    targets = [Path(a) for a in argv] or [Path("_entries")]
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
