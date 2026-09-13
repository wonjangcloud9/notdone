<p align="center"><a href="README.md">English</a> | <a href="README.ko.md">한국어</a></p>

<p align="center">
  <a href="https://github.com/wonjangcloud9/notdone/actions/workflows/validate.yml"><img src="https://github.com/wonjangcloud9/notdone/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-6b5bd6" alt="Claude Code skill">
</p>

# notdone

**Your agent says it's done. It never looked at the screen.**

A skill that refuses to let a coding agent claim completion without evidence.

---

Every agent does this:

> I've updated the settings page to support dark mode. The changes should work correctly now.

It wrote CSS. It did not open the page. It does not know whether the text is readable, and neither do you — until you check it yourself, which is the part you installed an agent to avoid.

With `notdone`, the same turn ends like this:

> | Claim | Evidence | Verdict |
> |---|---|---|
> | Dark mode on settings | `shots/settings-dark.png` — labels readable, divider visible | DONE |
> | Light mode unaffected | `shots/settings-light.png` | DONE |
> | Empty state | — | **NOT DONE** |
> | Mobile width | — | **NOT DONE** |
>
> **NOT DONE.** I have not rendered the page with zero saved profiles, and I have not checked it at 400px.

Two rows of work, honestly labeled, beat four rows of confidence. Note that the unfinished rows are still *there*: the table covers what you asked for, not what the agent got around to, so four parts requested and two delivered is four rows — never a tidy report of the two. [A fuller before/after](examples/session.md) shows a turn where the honest version catches a bug the confident one ships.

## Install

```bash
git clone https://github.com/wonjangcloud9/notdone ~/.claude/skills/notdone
```

That is the whole install. The repository *is* the skill directory.

For one project only, clone into `.claude/skills/notdone` inside the repo instead.

Or install it as a plugin:

```bash
claude plugin marketplace add wonjangcloud9/notdone
claude plugin install notdone@wonjang-skills
```

Pick one of the two, not both. If the plugin and a clone are installed together the plugin wins, and the clone is silently not loaded — Claude Code reports the name as already taken.

To update a cloned install, pull:

```bash
git -C ~/.claude/skills/notdone pull
```

It activates on its own when the agent is about to report something finished, when a check it ran has just failed, and when it is about to cite a screenshot or test run from earlier in the session. You can also invoke it directly with `/notdone`, or ask "is this actually done?"

## The rule

The agent may not write **done**, **complete**, **fixed**, **working**, **ready**, or **should work** unless it holds an artifact from the current session:

- output from a command it actually ran,
- a screenshot it actually took and looked at,
- an HTTP response it actually received.

Code it wrote is not evidence. Reasoning about why the code will work is not evidence. A test it added but never ran is not evidence.

Evidence also goes stale. A screenshot taken before two more edits describes a version that no longer exists, so the artifact has to postdate the last change it speaks for.

## What counts as evidence

| Changed | Not done until |
|---|---|
| **UI** | Four screenshots: light, dark, the empty state, and ~400px width. You looked at each one. |
| **Logic / API** | The real test output — command, exit code, and pass/fail counts. Pasted, not summarized. |
| **Bug fix** | The reproduction, run twice: failing before your change, passing after. Both outputs shown. |
| **Data / migration** | The applied output, plus a query proving the new shape exists. |
| **Deploy** | The live URL answering from outside, with its status code. Not the build log. |
| **Dependency / config** | A clean install or boot from scratch, not an already-warm process. |
| **Docs** | Every command in the doc, executed as written. |

The [checklists](checklists/) go further — what to actually look for in a dark-mode screenshot, why a reproduction that never failed proves nothing, why a backfill count means nothing without the before, why a green build is not a working deploy.

## Phrases it removes

"Should work now." "This should fix it." "The change is straightforward, so..." "Presumably this resolves..." "I've updated X so it will now Y." "Looks good to me." "Everything is in place."

Each of these is a way of saying *I did not check*. The skill replaces them with the evidence, or with **NOT DONE** and the specific thing that is missing.

## When verification is impossible

Sometimes it genuinely can't check — no browser, no credentials, a paid third-party service. Then it says so, in a shape you can act on:

> **NOT VERIFIED** — I changed the Stripe webhook handler but cannot reach Stripe from here.
> To verify: trigger a test payment and confirm the handler logs `payment.succeeded`.

It never lets an unverifiable claim wear the word "done".

## Manufactured evidence is the worse failure

A failing check is a finding, not an obstacle. The skill forbids the moves that turn a red result green without fixing anything: editing the assertion until it passes, narrowing the run to the subset that works, screenshotting only the viewport that looks right, re-running a flake until it goes green and citing that run.

Every one of those produces a real artifact, so the ledger looks exactly like an honest one. That is what makes it worse than a claim with no evidence at all — you would at least have known to check that one.

## NOT DONE is not a shortcut

The ledger is the last step, not the first. The skill tells the agent to go and produce the artifacts — run the test, take the screenshot, request the URL — before writing the report. **NOT DONE** is reserved for what it attempted and could not finish, or what needs something it does not have: a credential, a device, a service, your decision.

Without that, the rules would be trivially satisfiable by doing nothing and marking every row NOT DONE. An honest report of work you never attempted is not an improvement on a false one.

## It knows when not to apply

Not every change owes a ledger. A comment, a rename the compiler verifies, a typo the tests already cover — there is nothing to observe, so demanding evidence is noise, and noise is how a rule gets switched off.

And when you waive it — "just push it" — it complies. It says once what is going unverified, then drops it. It does not repeat the warning, refuse, or quietly verify anyway. The risk is yours to take.

## Other agents

The same rules work anywhere with a project instruction file. Copy [AGENTS.md](AGENTS.md) to your repository root for Codex, Cursor, and others, or append it to an existing `CLAUDE.md`.

## Why

An agent that overstates completion is worse than a slow one. A slow agent costs you time; a confident wrong one costs you the ability to trust any of its reports, including the true ones.

Reporting **NOT DONE** is a success. Four finished things and an honest fifth row is something you can act on. Five claimed things where one is false is something you have to re-verify entirely — which puts you back to doing it yourself.

## License

MIT
