# Git 01 - Fundamentals and Lifecycle

## Module Objective

Understand the basics of a Git repository and the Working Directory -> Staging -> Repository cycle.

## Initialize a Repository

### Create a folder

```bash
mkdir git-training
cd git-training
```

### Initialize Git

```bash
git init
```

Git creates the hidden folder:

```text
.git/
```

It contains the Git database.

## Check Status

```bash
git status
```

`git status` shows:

- the current branch
- modified files
- untracked files
- files ready to be committed

## File Lifecycle

```text
                git add             git commit
Working Dir  ------------->  Staging Area -------------> Repository
```

### Working Directory

Files present on your computer.

### Staging Area

Intermediate area containing what you want to include in the next commit.

### Repository

Permanent project history.

## Common mistakes

- Committing without checking `git status`.
- Not understanding the difference between Working Directory and Staging.

## Best practices

- Check `git status` very frequently.
- Stage only relevant changes.

## Interview Questions

- What is `.git/` for?
- Difference between Working Directory, Staging and Repository?

## Next

Next module: [02 - Commits and History](02-commits-historique.md)
