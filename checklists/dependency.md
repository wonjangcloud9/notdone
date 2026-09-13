# Dependency and config evidence

A warm process is a liar. It is still holding the config you replaced, the environment it booted with, and the package you deleted from disk ten minutes ago.

## The proof is a cold start

Restart the thing. For a dependency change, the honest test is stronger still: a fresh clone into an empty directory, install, boot.

```
$ git clone <repo> /tmp/coldstart && cd /tmp/coldstart
$ pnpm install --frozen-lockfile
$ pnpm build
```

Anything that only works in your existing checkout is working because of something in that checkout — a stale `node_modules`, a local file you never committed, a variable exported in your shell months ago.

## An import is not a dependency

Adding `import x from 'y'` while `y` already sits in `node_modules` as somebody else's transitive dependency will run fine for you and fail for everyone else. The declaration in the manifest is the change; the import is only the usage.

```
$ pnpm why y     # is it yours, or are you borrowing it?
```

## The lockfile is part of the change

If you changed dependencies and the lockfile is not in the diff, the change is not reproducible. Install with the frozen-lockfile flag so a drifted lockfile fails loudly instead of being silently rewritten.

## Version bumps: check what installed, not what you asked for

A range in the manifest is a request. Show what resolved:

```
$ pnpm ls typescript
```

A caret range means the version you tested is not necessarily the version the next clean install gets.

## Removing a dependency

Two claims, both needing evidence: that it is gone from the lockfile, and that the app still boots without it. A removal that only passes because the package is still on disk is not a removal.

## Config and environment

A value added to `.env`, a dashboard, or a config file is not a value the running process has. Prove it from the process — a log line, an endpoint that reports its config — not from the file you edited.

New env values almost always need a restart. That is the same cold-start rule, and it is the step most often skipped.
