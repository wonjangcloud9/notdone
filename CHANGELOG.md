# Changelog

## 0.3.1

- `scripts/selftest.py` breaks each invariant on purpose — an unlinked checklist, a relative link in `AGENTS.md`, a drifted evidence table, a version out of sync with this file, a non-spec frontmatter field, a dead link — and asserts `validate.py` fails and names the right check. A validator nobody has watched fail might be passing for the wrong reason. No change to the skill's rules.

## 0.3.0

- New checklist: [documentation](checklists/docs.md). Every row of the evidence table now has one. A command in a README is a claim that it works, and the install block is the one command every reader runs and the author never does.

## 0.2.0

- **Proportionality.** The skill now says when *not* to demand evidence — a comment, a rename the compiler verifies, a typo the tests already cover. A NOT DONE verdict on a comment is noise, and noise is how a rule gets switched off.
- **User waiver.** Previously undefined. When you say "just push it", the agent complies: it states once what is going unverified, then drops it. It does not repeat the warning, refuse, or quietly verify anyway.
- New checklists: [bug fix](checklists/bugfix.md) (a reproduction that never failed is not evidence), [logic and API](checklists/logic.md) ("tests pass" is a summary, not output), [dependency and config](checklists/dependency.md) (a warm process is a liar).
- `scripts/validate.py` now blocks three ways the docs drift apart: an unlinked checklist, a relative link in `AGENTS.md` (which gets copied into other repos alone), and the evidence table diverging between `SKILL.md` and `AGENTS.md`. Adding the last check immediately caught all seven rows already worded differently; they are now identical and CI keeps them that way.

## 0.1.0

- Initial release. The rule, the evidence table, the ledger, and the `NOT VERIFIED` escape hatch, plus checklists for UI, data and deploys.
- Installable two ways: clone the repo as a skill directory, or add it as a plugin marketplace.
