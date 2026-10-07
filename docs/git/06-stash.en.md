# Git 06 - Stash

## Module Objective

Temporarily save incomplete work to quickly switch context.

## Main Commands

Create a stash:

```bash
git stash
```

Include untracked files:

```bash
git stash -u
git stash --include-untracked
```

List stashes:

```bash
git stash list
```

View content:

```bash
git stash show
git stash show -p
```

Restore and delete:

```bash
git stash pop
```

Restore without deleting:

```bash
git stash apply
```

Delete:

```bash
git stash drop
git stash clear
```

Named stash:

```bash
git stash push -m "Debut authentification"
```

## When to Use?

When work is not finished but you need to quickly switch branches.

## Common mistakes

- Forgetting old stashes.
- Using stash as long-term storage.

## Best practices

- Name important stashes.
- Regularly clean `git stash list`.

## Interview Questions

- Difference between `pop` vs `apply`?
- Why use `-u`?

## Next

Next module: [07 - Workflow and Best Practices](07-workflow-bonnes-pratiques.md)
