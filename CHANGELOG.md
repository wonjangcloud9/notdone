# Changelog

## 0.8.4

- The README offered two install paths without saying they collide. Installing both leaves the clone silently unloaded — the plugin takes the name and Claude Code reports it as already taken — so anyone who cloned first and later "upgraded" to the plugin would be running a copy they were not editing. Found by re-running both documented install paths against the current version.

## 0.8.3

- `checklists/ui.md` had not been touched since the first release, while eight versions of rules shipped past it. Screenshots are where both of the newer rules land hardest — they are the artifact that goes stale fastest, and the easiest place to keep the three shots that came out well and skip the fourth — and neither was mentioned in the checklist people actually open for UI work.

## 0.8.2

- 0.7.0's rule — the ledger covers what was asked for, not what got done — reached `SKILL.md` and `AGENTS.md` but never the READMEs, so the pitch was missing the behaviour that stops a five-part request being reported as two tidy DONE rows. Folded into the opening example rather than added as a twelfth section.

## 0.8.1

- The README never said how to update a cloned install, and implied only the plugin route could be updated. It is `git -C ~/.claude/skills/notdone pull`. With eight releases in a day, anyone who cloned early was sitting on a materially weaker skill with no way to know.
- The same section still described activation as "when the agent is about to report completion", which 0.8.0 had already outgrown. It now names the failed-check and stale-artifact triggers too.

## 0.8.0

- **The skill now activates at the moments its newer rules are about to be broken.** The description had not changed since 0.1.0 and only listed "about to report completion", so the two rules that matter most — do not shape the check to fit the result, and evidence goes stale — could never fire at the moment they apply: a check that just failed, or a screenshot from earlier in the session about to be cited. Both are now trigger conditions. A rule that does not activate is not a rule.

## 0.7.0

- **The ledger must cover the whole request, not just the parts that got done.** Nothing previously required a row for work that was never started, so a five-part request finished twice over could be reported as two DONE rows and look flawless. Rows now come from what was asked for; anything skipped or deliberately dropped gets a row saying so, because silence is not a verdict.

## 0.6.0

- **Manufactured evidence is now forbidden explicitly.** Until this release the rules could be satisfied perfectly while engineering the result: edit the assertion until it goes green, narrow the run to the passing subset, screenshot only the viewport that looks right, re-run a flake and cite the good run. Each produces a real artifact, so the ledger looks identical to an honest one — which makes it worse than an unverified claim, not better. A failing check is a finding; if the check itself was wrong, fixing it is its own change and has to be said.

## 0.5.0

- **Evidence now has to postdate the last change it speaks for.** The rule said an artifact is something observed after the change, which left the common case open: take the screenshot, edit twice more, cite the screenshot. It describes a version that no longer exists. Re-run the check, or mark the row NOT DONE.
- The README's copy of the core rule was still missing "complete" — the word check only compared `SKILL.md` and `AGENTS.md`. It now covers all three.

## 0.4.5

- Both READMEs listed five banned phrases where the skill forbids seven; "presumably this resolves..." and "everything is in place" were missing. Added, and `validate.py` now compares the lists, normalising for the sentence case the README deliberately uses. The Korean README is checked on count.

## 0.4.4

- The README carried a fourth copy of the evidence table, left on the pre-0.2.0 wording when `SKILL.md` and `AGENTS.md` were unified. It promised less than the skill delivers — no "Not the build log", no "Pasted, not summarized" — in the document people read first. Synced, and `validate.py` now holds it to the skill's table. The Korean README is a translation, so only its row count is checkable; that is checked too.

## 0.4.3

- The core rule sentence forbade six words in `SKILL.md` and five in `AGENTS.md` — "complete" was missing from the copy other agents read. Restored, and `validate.py` now compares that sentence's word list too. This is the third instance of the same drift, each in a different duplicated passage.

## 0.4.2

- `AGENTS.md` was missing one banned phrase — "everything is in place" — so anyone using the Codex/Cursor copy was not covered by it. Restored, and `validate.py` now compares the two phrase lists the same way it compares the evidence tables. The check found this drift on its first run, as the table check did before it.

## 0.4.1

- The worked example was written before 0.4.0 and modelled the behaviour that release exists to stop: the browser was already open for two screenshots, yet the example marked the 400px width NOT DONE. It now verifies everything within reach and leaves a single `NOT VERIFIED` row for the panel that needs a Stripe test credential.

## 0.4.0

- **The skill now tells the agent to go and verify, not only what it may not claim.** Every rule so far governed the report, so a lazy agent could satisfy all of them by doing nothing and writing NOT DONE on every row — and "Reporting NOT DONE is a success" encouraged exactly that. The ledger is now explicitly the last step: produce the artifacts first, and reserve NOT DONE for what you attempted and could not complete, or what needs a credential, a device, a service, or the user's decision.

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
