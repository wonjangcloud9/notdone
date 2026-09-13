# Bug fix evidence

The proof is a reproduction that failed, then passed. Both halves, in that order.

## The repro must have failed first

If you only ran it after the fix, a green result proves the code works — not that it ever broke. You have evidence of the current state and none of the bug.

Run it before you change anything. If it passes before your fix, you have not found the bug yet.

## "Cannot reproduce" is a finding, not a fix

It is a legitimate thing to report, and it belongs in the ledger as its own row with **NOT DONE**. Changing code to address a bug you never observed is guessing, and shipping it as a fix hides the real one.

## Symptom or cause

You should be able to say, in one sentence, why it broke. Not what you changed — why the old code produced the wrong result.

If the best you have is "adding this check makes the error go away", you patched the observation. That fix holds until the same cause surfaces somewhere else.

## Use the reporter's reproduction

A minimal repro you invented is a different program. It is useful for isolating the cause, but the evidence has to be the path that actually failed — the same input, the same sequence, the same entry point.

Fixing your simplification and declaring the report resolved is a common way to close a bug that is still open.

## Fixes that work by coincidence

Some changes make a bug disappear without addressing it: adding a delay that hides a race, reordering calls so the timing happens to work, clearing a cache that was masking stale reads.

The tell is that you cannot explain the mechanism. Run the repro several times before believing it — a race that fails one time in four looks fixed on the first green run.

## Leave a test behind

A fix without a regression test is a fix with an expiry date. Write the test so that it fails against the old behaviour — check that by reverting the fix — and keep it.

## The ledger row

Show both runs, not a summary:

```
$ pytest tests/test_export.py::test_empty_range   # before
FAILED — IndexError: list index out of range

$ pytest tests/test_export.py::test_empty_range   # after
PASSED
```
