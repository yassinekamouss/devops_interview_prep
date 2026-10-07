# Git 05 - Reset, Revert and Amend

## Module Objective

Master local history correction operations and cleanly share your changes.

## Git Reset

Reset moves a branch pointer.

Before:

```text
A ---- B ---- C ---- D
                     ▲
                    main
```

After:

```bash
git reset HEAD~1
```

```text
A ---- B ---- C
               ▲
              main
```

## The 3 Modes

### Soft

```bash
git reset --soft HEAD~1
```

Keeps Working Directory + Staging, only removes the commit.

### Mixed (default)

```bash
git reset HEAD~1
```

Keeps Working Directory, clears Staging.

### Hard

```bash
git reset --hard HEAD~1
```

Removes commit + staging + local modifications.

## Reset vs Revert

### Reset

```text
A ---- B ---- C ---- D

->

A ---- B ---- C
```

The commit disappears from the branch's local history.

### Revert

```text
A ---- B ---- C ---- D ---- E
```

`E` undoes `D`, history remains intact.

## Commit Amend

Modify the last commit.

Change the message:

```bash
git commit --amend -m "Correct message"
```

Add a forgotten file:

```bash
git add style.css
git commit --amend
```

The commit is recreated, SHA changes. Avoid after shared push.

## Common mistakes

- Using `--hard` without checking impact.
- Doing `amend` after a commit has already been shared.

## Best practices

- Prefer `revert` on a shared branch.
- Use `reset` for local pre-push cleanup.

## Interview Questions

- Difference between reset vs revert?
- When to use `--soft` rather than `--mixed`?
- Why does `amend` change the SHA?

## Next

Next module: [06 - Stash](06-stash.md)
