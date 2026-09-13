#!/usr/bin/env python3
"""Break each invariant on purpose and check that validate.py notices.

A validator nobody has seen fail is a validator that might be passing for the
wrong reason — the same trap checklists/bugfix.md describes for a test written
after the fix. Each case here copies the repo, damages exactly one thing, and
asserts the run fails and names the right check.
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent


def run(tree):
    proc = subprocess.run([sys.executable, str(tree / "scripts" / "validate.py")],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def edit(tree, rel, old, new):
    path = tree / rel
    text = path.read_text()
    assert old in text, f"fixture drifted: {old!r} not in {rel}"
    path.write_text(text.replace(old, new, 1))


def orphan_checklist(tree):
    (tree / "checklists" / "orphan.md").write_text("# orphan\n")


def relative_link_in_agents(tree):
    (tree / "AGENTS.md").write_text(
        (tree / "AGENTS.md").read_text() + "\nSee [the checklists](checklists/ui.md).\n")


def drift_evidence_table(tree):
    edit(tree, "AGENTS.md", "| **Docs** |", "| **Documentation** |")


def desync_version(tree):
    edit(tree, ".claude-plugin/plugin.json", '"version": ', '"version": "9.9.9", "_old": ')


def non_spec_frontmatter(tree):
    edit(tree, "SKILL.md", "license: MIT", "license: MIT\nmodel: opus")


def drop_forbidden_word(tree):
    edit(tree, "AGENTS.md", "**done**, **complete**,", "**done**,")


def drop_banned_phrase(tree):
    edit(tree, "AGENTS.md", ' \u00b7 "everything is in place"', "")


def broken_link(tree):
    edit(tree, "README.md", "](checklists/)", "](checklists/nope.md)")


CASES = [
    ("an unlinked checklist", orphan_checklist, "reachable from SKILL.md"),
    ("a relative link in AGENTS.md", relative_link_in_agents, "no relative links"),
    ("the evidence tables drifting", drift_evidence_table, "evidence tables agree"),
    ("a version out of sync with the changelog", desync_version, "matches plugin.json"),
    ("a non-spec frontmatter field", non_spec_frontmatter, "Agent Skills spec fields"),
    ("a banned phrase dropped from AGENTS.md", drop_banned_phrase, "banned phrase lists agree"),
    ("a forbidden word dropped from the core rule", drop_forbidden_word, "core rule forbids the same words"),
    ("a link to a file that does not exist", broken_link, "nope.md"),
]

failures = []

with tempfile.TemporaryDirectory() as tmp:
    clean = pathlib.Path(tmp) / "clean"
    shutil.copytree(ROOT, clean, ignore=shutil.ignore_patterns(".git"))
    code, output = run(clean)
    if code == 0:
        print("  PASS  an untouched copy passes")
    else:
        print("  FAIL  an untouched copy passes — the fixture itself is broken")
        print(output)
        failures.append("baseline")

    for label, damage, expected in CASES:
        work = pathlib.Path(tmp) / re.sub(r"\W+", "-", label)
        shutil.copytree(clean, work)
        damage(work)
        code, output = run(work)
        caught = code != 0 and expected in output
        print(f"  {'PASS' if caught else 'FAIL'}  catches {label}")
        if not caught:
            failures.append(label)
            print(f"        expected a failure mentioning {expected!r}, exit was {code}")

print(f"\n{len(CASES) + 1 - len(failures)}/{len(CASES) + 1} checks passed")
if failures:
    print("NOT DONE:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print("DONE")
