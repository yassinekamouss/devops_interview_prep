# Git 02 - Commits and History

## Module Objective

Learn to prepare clean commits and efficiently read Git history.

## Add Files

```bash
git add fichier.txt
git add .
```

## View Changes

```bash
git diff
```

## Create a Commit

```bash
git commit -m "Add login page"
```

### Examples of good messages

```text
Add authentication
Fix navbar
Update README
```

### Examples of bad messages

```text
test
aaa
modif
```

## History

```bash
git log
git log --oneline
git log --graph --oneline --all
git show
```

## Common mistakes

- Commits that are too large and heterogeneous.
- Non-explicit commit messages.
- Not inspecting history before rebase/merge.

## Best practices

- Small and coherent commits.
- Imperative, explicit messages about intent.
- Use `git log --graph --oneline --all` to quickly visualize repo state.

## Interview Questions

- What does `git show` display?
- Why is a good commit message important in a team?

## Next

Next module: [03 - Branches and Merge](03-branches-merge.md)
