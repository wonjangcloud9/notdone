# What changes in practice

A real shape of turn, before and after. The work is identical; only the report differs.

## Without the skill

> I've added dark mode support to the settings page. I updated `settings.css` to use CSS custom properties and added a `prefers-color-scheme` block. The changes should work correctly now — let me know if you see any issues.

Three things are wrong with this, and none of them are visible to you:

- It never rendered the page, so "should work correctly" is a guess.
- The `prefers-color-scheme` block defines the dark values only. Light has no value at all, so one of the two themes is broken and the message cannot tell you which.
- "Let me know if you see any issues" moves the verification to you. That is the work you delegated.

## With the skill

> I updated `settings.css` to use custom properties and rendered the page in both themes.
>
> The first pass was broken: I had defined the palette only inside `@media (prefers-color-scheme: dark)`, so light mode fell back to the browser defaults and the panel border disappeared. Fixed by defining the full palette on `:root` and overriding only what changes in dark.
>
> | Claim | Evidence | Verdict |
> |---|---|---|
> | Dark mode renders correctly | `shots/settings-dark.png` — labels readable against the panel, divider visible, focus ring intact | DONE |
> | Light mode unaffected | `shots/settings-light.png` — palette now defined on `:root`, border restored | DONE |
> | Empty state | — | **NOT DONE** |
> | Mobile width | — | **NOT DONE** |
>
> **NOT DONE.** I have not rendered the page with zero saved profiles, and I have not checked it at 400px. Both need the dev server running with a seeded empty account.

The second report is longer, and that is the point. It contains a bug that the first report would have shipped, and it ends with two specific things you now know are unverified — instead of a sentence that quietly assumes they are fine.

## What it does not do

It cannot make an agent verify something it has no access to. It can only stop the agent from pretending otherwise. When the tools are not there, the honest output is `NOT VERIFIED` plus the check you should run, not a smaller claim dressed as a finished one.
