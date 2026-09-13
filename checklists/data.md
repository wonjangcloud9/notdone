# Data and migration evidence

A migration that ran is not a migration that did what you meant.

## Proving the shape changed

Show the applied output, then query the catalog — not your migration file, which only proves what you asked for:

```sql
select column_name, data_type, is_nullable
from information_schema.columns
where table_name = 'your_table';
```

## Proving the data is right

A backfill needs a count, on both sides:

```sql
select count(*) from orders where status is null;  -- expect 0 after
```

Run it before as well. A backfill that reports zero rows remaining is meaningless if there were zero rows to begin with.

## Row-level security

RLS enabled is not RLS working. The check is: connect as the restricted role and fail to read what it must not read.

A policy that returns your own rows when you are the owner proves nothing. Try it as a different user, and expect nothing back.

## Destructive steps

Before a `drop`, `truncate`, or a column rename, show that you looked at what is there — a count, a sample. Afterwards, show that what survived is what should have.

## Rollback

If you cannot state what undoes the change, the migration is not done, however cleanly it applied.
