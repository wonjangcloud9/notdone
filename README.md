<p align="center"><a href="README.md">English</a> | <a href="README.ko.md">한국어</a></p>

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

Two rows of work, honestly labeled, beat four rows of confidence.

## Install

```bash
git clone https://github.com/wonjangcloud9/notdone ~/.claude/skills/notdone
```

That is the whole install. The repository *is* the skill directory.

For one project only, clone into `.claude/skills/notdone` inside the repo instead.

It activates on its own when the agent is about to report completion. You can also invoke it directly with `/notdone`, or ask "is this actually done?"

## The rule

The agent may not write **done**, **fixed**, **working**, **ready**, or **should work** unless it holds an artifact from the current session:

- output from a command it actually ran,
- a screenshot it actually took and looked at,
- an HTTP response it actually received.

Code it wrote is not evidence. Reasoning about why the code will work is not evidence. A test it added but never ran is not evidence.

## What counts as evidence

| Changed | Not done until |
|---|---|
| UI | Light, dark, empty state, ~400px — four screenshots, each one looked at |
| Logic / API | Real test output: command, exit code, pass/fail counts |
| Bug fix | The reproduction failing before the change and passing after |
| Data / migration | Applied output plus a query proving the new shape |
| Deploy | The live URL answering from outside, with its status code |
| Dependency / config | A clean install or boot, not an already-warm process |
| Docs | Every command in the doc, run as written |

The [checklists](checklists/) go further — what to actually look for in a dark-mode screenshot, why a backfill count means nothing without the before, why a green build is not a working deploy.

## Phrases it removes

"Should work now." "This should fix it." "The change is straightforward, so..." "I've updated X so it will now Y." "Looks good to me."

Each of these is a way of saying *I did not check*. The skill replaces them with the evidence, or with **NOT DONE** and the specific thing that is missing.

## When verification is impossible

Sometimes it genuinely can't check — no browser, no credentials, a paid third-party service. Then it says so, in a shape you can act on:

> **NOT VERIFIED** — I changed the Stripe webhook handler but cannot reach Stripe from here.
> To verify: trigger a test payment and confirm the handler logs `payment.succeeded`.

It never lets an unverifiable claim wear the word "done".

## Other agents

The same rules work anywhere with a project instruction file. Copy [AGENTS.md](AGENTS.md) to your repository root for Codex, Cursor, and others, or append it to an existing `CLAUDE.md`.

## Why

An agent that overstates completion is worse than a slow one. A slow agent costs you time; a confident wrong one costs you the ability to trust any of its reports, including the true ones.

Reporting **NOT DONE** is a success. Four finished things and an honest fifth row is something you can act on. Five claimed things where one is false is something you have to re-verify entirely — which puts you back to doing it yourself.

## License

MIT
