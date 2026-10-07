# Git 03 - Branches and Merge

## Module Objective

Understand branches as pointers, then master basic merges.

## Branches

```bash
git branch
git branch feature/login
git switch -c feature/login
git switch main
git checkout feature/login
git branch -d feature/login
git branch -D feature/login
```

## Concept

A branch is a pointer:

```text
A ---- B ---- C
              ▲
             main
              ▲
        feature/login
```

Git does not copy files; it moves references to commits.

## Merge

Merge a branch:

```bash
git switch main
git merge feature/login
```

Rule: position yourself on the branch that receives the changes.

### Fast-forward

```text
A ---- B ---- C ---- D
                     ▲
                    main
                    feature
```

Git moves the pointer.

### Merge commit

```text
A ---- B ---- E -------- M
      \                /
       C ---- D ------/
```

Git creates a merge commit.

## Common mistakes

- Running `git merge` from the wrong branch.
- Deleting an unmerged branch without checking.

## Best practices

- Use one branch per feature.
- Clean up merged branches.

## Interview Questions

- What is a fast-forward?
- When do you get a merge commit?

## Next

Next module: [04 - Conflicts and Rebase](04-conflits-rebase.md)
