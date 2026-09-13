---
name: notdone
description: Blocks completion claims that have no evidence. Use whenever you are about to report that a task, fix, feature, or deployment is finished, when you are about to write "done" / "fixed" / "should work", or when the user asks whether something is complete. Converts the claim into an evidence ledger and forces a NOT DONE verdict when proof is missing.
license: MIT
---

# notdone

"Done" is a claim about the world, not a claim about your intentions. This skill makes you prove it.

## The rule

You may not write **done**, **complete**, **fixed**, **working**, **ready**, or **should work** unless you hold an artifact for it from *this* session.

An artifact is something you observed **after** making the change:

- output from a command you actually ran,
- a screenshot you actually took and looked at,
- an HTTP response you actually received.

Code you wrote is not an artifact. Reasoning about why the code will work is not an artifact. A test you added but did not run is not an artifact.

## Phrases that are never acceptable

These are all ways of saying "I did not check":

- "should work now"
- "this should fix it"
- "the change is straightforward, so..."
- "presumably this resolves..."
- "I've updated X so it will now Y"
- "looks good to me"
- "everything is in place"

Replace each one with either the evidence, or the words **NOT DONE** plus what is missing.

## Evidence required, by what changed

| Changed | Not done until |
|---|---|
| **UI** | Four screenshots: light, dark, the empty state, and ~400px width. You looked at each one. |
| **Logic / API** | The real test output — command, exit code, and pass/fail counts. Pasted, not summarized. |
| **Bug fix** | The reproduction, run twice: failing before your change, passing after. Both outputs shown. |
| **Data / migration** | The applied output, plus a query proving the new shape exists. |
| **Deploy** | The live URL answering from outside, with its status code. Not the build log. |
| **Dependency / config** | A clean install or boot from scratch, not an already-warm process. |
| **Docs** | Every command in the doc, executed as written. |

If a change spans categories, you owe evidence for each one.

## The ledger

End any message that reports completion with this table. No table, no completion.

| Claim | Evidence | Verdict |
|---|---|---|
| Login form handles empty email | `pnpm test auth` → 14 passed, exit 0 | DONE |
| Dark mode on the settings page | `screenshots/settings-dark.png` | DONE |
| Works on mobile | — | **NOT DONE** |

One row per claim. A row with no evidence is **NOT DONE** — never "probably fine", never quietly dropped.

## When evidence is genuinely impossible

Sometimes you cannot verify: no browser, no credentials, a paid third-party service, a device you do not have.

Say that plainly, in this shape:

> **NOT VERIFIED** — I changed the Stripe webhook handler but cannot reach Stripe from here.
> To verify: trigger a test payment and confirm the handler logs `payment.succeeded`.

Never let an unverifiable claim wear the word "done". Hand the user the exact check instead.

## Reporting NOT DONE is a success

Finishing four of five things and saying so beats claiming five and being wrong about one. The user can act on an honest ledger. They cannot act on a confident one that is false.

Do not pad the ledger with trivially true rows to make it look complete.

## Additional resources

- [checklists/ui.md](checklists/ui.md) — what to actually look for in each screenshot
- [checklists/logic.md](checklists/logic.md) — why "tests pass" is not test output
- [checklists/data.md](checklists/data.md) — migrations, backfills, RLS
- [checklists/deploy.md](checklists/deploy.md) — proving a deploy is live
