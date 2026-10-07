# Git 04 - Conflicts and Rebase

## Module Objective

Learn to resolve conflicts and correctly choose between merge and rebase.

## Merge Conflicts

A conflict appears when two branches modify the same line.

Example:

```text
<<<<<<< HEAD
Version main
=======
Version feature
>>>>>>> feature/login
```

Resolution:

1. Edit the file
2. Remove markers
3. Stage the file

```bash
git add README.md
git commit
```

Abort an ongoing merge:

```bash
git merge --abort
```

## Rebase

Update a branch:

```bash
git switch feature/login
git rebase main
```

Before:

```text
A ---- B ---- E ---- F
      \
       C ---- D
```

After:

```text
A ---- B ---- E ---- F ---- C' ---- D'
```

Commits are recreated, the SHA changes.

## Handling Conflicts During Rebase

```bash
git add README.md
git rebase --continue
git rebase --abort
git rebase --skip
```

## Interactive Rebase

```bash
git rebase -i HEAD~4
```

Actions:

```text
pick
reword
edit
squash
fixup
drop
```

## Merge vs Rebase

| Merge                      | Rebase               |
| -------------------------- | -------------------- |
| Preserves history          | Rewrites history     |
| May create a Merge Commit  | No Merge Commit      |
| Branched history           | Linear history       |

## Common mistakes

- Rebasing a branch already shared without coordination.
- Resolving a conflict too quickly without functional verification.

## Best practices

- Use rebase mainly on a personal branch.
- Keep merge when you want to preserve collective historical context.

## Interview Questions

- Difference between merge vs rebase?
- Why does the SHA change after a rebase?

## Next

Next module: [05 - Reset, Revert and Amend](05-reset-revert-amend.md)
