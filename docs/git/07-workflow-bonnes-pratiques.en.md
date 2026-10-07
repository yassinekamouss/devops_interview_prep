# Git 07 - Workflow and Best Practices

## Module Objective

Apply a professional branching and synchronization workflow before Pull Request.

## Common Professional Workflow

```bash
git switch main
git pull origin main

git switch -c feature/authentication

# Developpement
git add .
git commit -m "Implement authentication"

git fetch origin
git rebase origin/main

# Resoudre les conflits si necessaire
git rebase --continue

git push origin feature/authentication

# Ouvrir une Pull Request
```

## Golden Rules

- Make small and coherent commits.
- Create one branch per feature.
- Use `rebase` only on a personal branch.
- Use `revert` rather than `reset` on an already shared branch.
- Check `git status` before almost every important command.
- Use `git log --graph --oneline --all` to visualize history.
- Never do `git push --force` on `main` without knowing exactly what you are doing.

## Common mistakes

- Working for a long time without syncing with `main`.
- Vague and bulky commits.
- Uncontrolled `push --force`.

## Best practices

- Regular rebase of the feature branch onto `origin/main`.
- Local verification before push.
- Small PRs reviewed quickly.

## Interview Questions

- Why prefer small commits?
- Why rebase before PR?

## Next

Next module: [08 - Cheatsheet and Interview Questions](08-cheatsheet-entretien.md)
