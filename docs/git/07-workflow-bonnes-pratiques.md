# Git 07 - Workflow et bonnes pratiques

## Objectif du module

Appliquer un workflow professionnel de branchement et de synchronisation avant Pull Request.

## Workflow professionnel courant

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

## Regles d'or

- Faire des commits petits et coherents.
- Creer une branche par fonctionnalite.
- Utiliser `rebase` uniquement sur une branche personnelle.
- Utiliser `revert` plutot que `reset` sur une branche deja partagee.
- Verifier `git status` avant presque chaque commande importante.
- Utiliser `git log --graph --oneline --all` pour visualiser l'historique.
- Ne jamais faire un `git push --force` sur `main` sans savoir exactement ce que tu fais.

## Common mistakes

- Travailler longtemps sans synchroniser avec `main`.
- Commits vagues et volumineux.
- `push --force` non maitrise.

## Best practices

- Rebase regulier de la branche feature sur `origin/main`.
- Verification locale avant push.
- PRs petites et relues rapidement.

## Questions d'entretien

- Pourquoi preferer des commits petits ?
- Pourquoi rebaser avant PR ?

## Suite

Module suivant: [08 - Cheatsheet et questions d'entretien](08-cheatsheet-entretien.md)
