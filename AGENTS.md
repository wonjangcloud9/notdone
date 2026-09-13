# Definition of done

Do not write **done**, **fixed**, **working**, **ready**, or **should work** unless you hold an artifact from this session: output from a command you ran, a screenshot you took and looked at, or an HTTP response you received.

Code you wrote is not evidence. Reasoning about why it will work is not evidence. A test you added but never ran is not evidence.

## Evidence required

| Changed | Not done until |
|---|---|
| UI | Light, dark, empty state, ~400px — four screenshots, each one looked at |
| Logic / API | Real test output: command, exit code, pass/fail counts |
| Bug fix | The reproduction failing before the change and passing after |
| Data / migration | Applied output plus a query proving the new shape |
| Deploy | The live URL answering from outside, with its status code |
| Dependency / config | A clean install or boot, not an already-warm process |
| Docs | Every command in the doc, run as written |

## End completion reports with a ledger

| Claim | Evidence | Verdict |
|---|---|---|
| ... | ... | DONE / **NOT DONE** |

A row with no evidence is **NOT DONE**. Never "probably fine", never quietly dropped.

## Never use these phrases

"should work now" · "this should fix it" · "the change is straightforward, so..." · "presumably this resolves..." · "I've updated X so it will now Y" · "looks good to me"

Replace each with the evidence, or with **NOT DONE** and what is missing.

## When verification is impossible

Say so in this shape, and hand over the exact check:

> **NOT VERIFIED** — I changed the Stripe webhook handler but cannot reach Stripe from here.
> To verify: trigger a test payment and confirm the handler logs `payment.succeeded`.

Reporting NOT DONE is a success. An honest partial report is actionable; a confident false one is not.
