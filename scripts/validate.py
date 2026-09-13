#!/usr/bin/env python3
"""Evidence that this repo is what it claims to be.

A skill that demands proof should be able to produce some. This checks the
things that actually break for users: a frontmatter Claude Code won't parse,
a field that makes a claude.ai upload fail, a checklist link pointing at a
file that isn't there, and manifests that disagree with the skill.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Fields in the Agent Skills open standard. Anything else is a Claude Code
# extension and causes a hard error when the skill is uploaded to claude.ai.
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

def evidence_table(path):
    """The rows of the 'Changed | Not done until' table, wherever it appears.

    SKILL.md and AGENTS.md both carry this table — the skill for Claude Code,
    AGENTS.md for anything else. Duplication is deliberate (AGENTS.md has to
    survive being copied into a repo alone) so the rows have to be kept equal
    by something other than memory.
    """
    rows, inside = [], False
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith("| Changed ") and "Not done until" in stripped:
            inside = True
            continue
        if inside:
            if not stripped.startswith("|"):
                break
            if set(stripped) <= set("|- "):
                continue
            rows.append(tuple(c.strip() for c in stripped.strip("|").split("|")))
    return rows


def banned_phrases(path, heading):
    """The quoted phrases under a heading, as a set.

    Duplicated between SKILL.md and AGENTS.md for the same reason the evidence
    table is: AGENTS.md has to survive being copied into a repo on its own.
    """
    text = path.read_text()
    start = text.index(heading) + len(heading)
    rest = text[start:]
    end = rest.index("\n## ") if "\n## " in rest else len(rest)

    # Only lines that are nothing but quoted phrases and separators — SKILL.md
    # uses a bullet per phrase, AGENTS.md runs them together with "·". This
    # skips the prose around them, which also contains quotes.
    phrases = set()
    for line in rest[:end].splitlines():
        quoted = re.findall(r'"([^"]+)"', line)
        if not quoted:
            continue
        if set(re.sub(r'"[^"]+"', "", line)) <= set("-· \t"):
            phrases.update(quoted)
    return phrases


def forbidden_words(path):
    """The bolded words in the core rule sentence, as a set.

    The most important sentence in both documents, and the one most likely to
    be edited in only one of them.
    """
    for line in path.read_text().splitlines():
        if "unless you hold an artifact" in line:
            return set(re.findall(r"\*\*([^*]+)\*\*", line))
    return set()


failures = []
checks = 0


def check(label, ok, detail=""):
    global checks
    checks += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {label}{'  — ' + detail if detail else ''}")
    if not ok:
        failures.append(label)
    return ok


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields, key = {}, None
    for line in m.group(1).split("\n"):
        if re.match(r"^[A-Za-z0-9_-]+:", line):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
        elif key and line.startswith((" ", "\t")):
            fields[key] += " " + line.strip()
    return fields


print("SKILL.md")
skill_path = ROOT / "SKILL.md"
if not check("exists at repo root", skill_path.exists(),
             "the repo doubles as a skill directory, so it must live here"):
    sys.exit(1)

text = skill_path.read_text()
fm = parse_frontmatter(text)
check("frontmatter parses", fm is not None, "the opening --- must be the first line")

if fm:
    check("has name", "name" in fm)
    check("has description", "description" in fm)
    unknown = sorted(set(fm) - SPEC_FIELDS)
    check("uses only Agent Skills spec fields", not unknown,
          f"claude.ai rejects: {', '.join(unknown)}" if unknown else "also uploadable to claude.ai")
    length = len(fm.get("description", ""))
    check("description within 1536 chars", length <= 1536, f"{length} chars")

lines = len(text.splitlines())
check("SKILL.md under 500 lines", lines <= 500, f"{lines} lines")

print("\nReferenced files")
for source in ["SKILL.md", "README.md", "README.ko.md", "CHANGELOG.md"]:
    body = (ROOT / source).read_text()
    for ref in re.findall(r"\]\((?!https?:)([^)#]+)\)", body):
        target = ROOT / ref
        check(f"{source} -> {ref}", target.exists())

print("\nManifests")
plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
check("plugin.json has a name", "name" in plugin)
check("plugin name matches the skill", plugin.get("name") == (fm or {}).get("name"),
      f"{plugin.get('name')} vs {(fm or {}).get('name')}")
check("marketplace lists the plugin",
      any(p.get("name") == plugin.get("name") for p in market.get("plugins", [])))
check("marketplace owner declared", "name" in market.get("owner", {}))

changelog = (ROOT / "CHANGELOG.md").read_text()
headings = re.findall(r"^## \[?(\d+\.\d+\.\d+)\]?", changelog, re.M)
check("CHANGELOG has a version heading", bool(headings))
check("CHANGELOG top entry matches plugin.json", bool(headings) and headings[0] == plugin.get("version"),
      f"changelog {headings[0] if headings else '-'} vs plugin.json {plugin.get('version')}; "
      "the skill's rules ship inside the plugin, so a changed rule needs a changed version")

print("\nDoc invariants")
linked = (ROOT / "SKILL.md").read_text()
for path in sorted((ROOT / "checklists").glob("*.md")):
    rel = f"checklists/{path.name}"
    check(f"{rel} is reachable from SKILL.md", rel in linked,
          "a checklist nothing links to is a checklist nobody reads")

agents = (ROOT / "AGENTS.md").read_text()
relative_links = re.findall(r"\]\((?!https?:)([^)]+)\)", agents)
check("AGENTS.md has no relative links", not relative_links,
      f"it gets copied into other repos alone; these would break: {', '.join(relative_links)}"
      if relative_links else "safe to copy standalone")

skill_rows = evidence_table(ROOT / "SKILL.md")
agents_rows = evidence_table(ROOT / "AGENTS.md")
check("evidence table found in both files", bool(skill_rows) and bool(agents_rows),
      f"SKILL.md {len(skill_rows)} rows, AGENTS.md {len(agents_rows)} rows")
check("evidence tables agree", skill_rows == agents_rows,
      "SKILL.md and AGENTS.md have drifted" if skill_rows != agents_rows
      else f"{len(skill_rows)} rows identical")

skill_phrases = banned_phrases(ROOT / "SKILL.md", "## Phrases that are never acceptable")
agents_phrases = banned_phrases(ROOT / "AGENTS.md", "## Never use these phrases")
missing = (skill_phrases | agents_phrases) - (skill_phrases & agents_phrases)
skill_words = forbidden_words(ROOT / "SKILL.md")
agents_words = forbidden_words(ROOT / "AGENTS.md")
word_gap = (skill_words | agents_words) - (skill_words & agents_words)
check("the core rule forbids the same words", skill_words and not word_gap,
      f"only in one file: {', '.join(sorted(word_gap))}" if word_gap
      else f"{len(skill_words)} words identical")

check("banned phrase lists agree", skill_phrases and not missing,
      f"only in one file: {', '.join(sorted(missing))}" if missing
      else f"{len(skill_phrases)} phrases identical")

print(f"\n{checks - len(failures)}/{checks} checks passed")
if failures:
    print("NOT DONE:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print("DONE")
