# Documentation evidence

A command in a README is a claim that it works. Writing it is not running it.

## Run every command, as written

Not a variation you know works — the exact line a reader will copy. In a fresh shell, from the directory the document says to be in.

The failure is ordinary: the command was correct when it was written, the flag was renamed two releases ago, and nobody has pasted it since.

## The reader does not have your state

Your shell has an exported variable, a logged-in CLI, a cloned repo, a running service. The reader has none of it. Either the document says to set that up, or the command is only true for you.

The cheap version of this check is a new terminal. The honest version is a fresh clone in an empty directory.

## Placeholders must look like placeholders

`<project-ref>` and `your-app.example.com` are fine. A real-looking value someone will paste unchanged is not.

And the command has to work once the placeholder is substituted — verify it with a real value, then put the placeholder back.

## Pasted output goes stale

Version numbers, row counts, timings, and directory listings in a document are a snapshot. If you paste output, it should be output you just produced, and it should still be true of the current version.

## Install instructions deserve the fresh clone

The install block is the one command every reader runs and the author never does, because the author already has the thing installed. Test it the way a stranger meets it: empty directory, no prior state.

## Documenting something you did not run

If a step cannot be verified from here — it needs an account, a paid service, hardware you lack — say so in the document rather than presenting it as tested. An untested step written in the same confident voice as a tested one is the documentation version of "should work".
