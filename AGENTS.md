# Definition of done

Do not write **done**, **fixed**, **working**, **ready**, or **should work** unless you hold an artifact from this session: output from a command you ran, a screenshot you took and looked at, or an HTTP response you received.

Code you wrote is not evidence. Reasoning about why it will work is not evidence. A test you added but never ran is not evidence.

## Evidence required

| Changed | Not done until |
|---|---|
| **UI** | Four screenshots: light, dark, the empty state, and ~400px width. You looked at each one. |
| **Logic / API** | The real test output — command, exit code, and pass/fail counts. Pasted, not summarized. |
| **Bug fix** | The reproduction, run twice: failing before your change, passing after. Both outputs shown. |
| **Data / migration** | The applied output, plus a query proving the new shape exists. |
| **Deploy** | The live URL answering from outside, with its status code. Not the build log. |
| **Dependency / config** | A clean install or boot from scratch, not an already-warm process. |
| **Docs** | Every command in the doc, executed as written. |

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
