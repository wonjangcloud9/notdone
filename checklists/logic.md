# Logic and API evidence

"Tests pass" is a summary. The output is the evidence.

## Show the run, not the conclusion

Paste the command, the exit code, and the counts:

```
$ pnpm test auth
 ✓ src/auth/session.test.ts (11)
 ✓ src/auth/token.test.ts (3)
 Test Files  2 passed (2)
      Tests  14 passed (14)
$ echo $?
0
```

A summary hides the two failures that matter most: a suite that silently ran zero tests, and a suite that skipped the file you changed.

## Did the test run cover your change?

A green suite proves nothing if none of it touches the new code. Before claiming a test as evidence, be able to say which test exercises which change.

The cheap proof: break the change on purpose and watch the test fail. If it still passes, the test is not covering what you think it is, and it is not evidence.

## Zero is a suspicious number

`Tests  0 passed (0)` exits 0. So does a filter that matched no files, a config pointing at the wrong directory, and a suite that bailed early. Read the counts, not the exit code alone.

## A test you wrote in the same turn

Writing a test and running it once proves it passes against the code you just wrote. It does not prove it would have caught the bug. Run it against the old behaviour if you can — a quick stash or a reverted line — and show that it fails there.

## New behaviour needs its own row

If the change adds an API surface, the evidence is a call to it, with the response. Not the handler's source code.

```
$ curl -s -X POST localhost:3000/api/sessions -d '{"email":""}' -H 'content-type: application/json'
{"error":"email is required","code":"VALIDATION"}
```

## Errors are behaviour too

The path you added for failure is a claim. Trigger it. A validation branch nobody has executed is as untested as the feature itself.

## Flakes

If a test passed on the second run, say so. "Passing" and "passing sometimes" are different claims, and the second one is the more useful thing to report.
