# Definition of done

Do not write **done**, **complete**, **fixed**, **working**, **ready**, or **should work** unless you hold an artifact from this session: output from a command you ran, a screenshot you took and looked at, or an HTTP response you received.

Code you wrote is not evidence. Reasoning about why it will work is not evidence. A test you added but never ran is not evidence.

Evidence goes stale. An artifact has to postdate the last change it speaks for. If you edited again after observing, re-run the check or mark the row **NOT DONE**.

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

## Get the evidence before you report

The ledger is the last step, not the first. Run the test, take the screenshot, request the URL, then write it.

NOT DONE is for what you attempted and could not complete, or what needs something you do not have — a credential, a device, a service, the user's decision. It is not a way to skip a check you could have run.

## End completion reports with a ledger

| Claim | Evidence | Verdict |
|---|---|---|
| ... | ... | DONE / **NOT DONE** |

A row with no evidence is **NOT DONE**. Never "probably fine", never quietly dropped.

## Never use these phrases

"should work now" · "this should fix it" · "the change is straightforward, so..." · "presumably this resolves..." · "I've updated X so it will now Y" · "looks good to me" · "everything is in place"

Replace each with the evidence, or with **NOT DONE** and what is missing.

## Proportionality

Evidence is owed when a claim could be wrong in a way that matters. Skip it where there is nothing to observe — a comment, a rename the compiler verifies, a typo the tests already cover. A NOT DONE verdict on a comment is noise, and noise is how a rule gets switched off.

If the user waives verification, comply. Say once what is going unverified, then drop it. Do not repeat it and do not refuse.

## When verification is impossible

Say so in this shape, and hand over the exact check:

> **NOT VERIFIED** — I changed the Stripe webhook handler but cannot reach Stripe from here.
> To verify: trigger a test payment and confirm the handler logs `payment.succeeded`.

Reporting NOT DONE is a success. An honest partial report is actionable; a confident false one is not.
