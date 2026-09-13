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
for source in ["SKILL.md", "README.md", "README.ko.md"]:
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

print(f"\n{checks - len(failures)}/{checks} checks passed")
if failures:
    print("NOT DONE:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print("DONE")
