# Git 02 - Commits et historique

## Objectif du module

Savoir preparer des commits propres et lire efficacement l'historique Git.

## Ajouter des fichiers

```bash
git add fichier.txt
git add .
```

## Voir les modifications

```bash
git diff
```

## Creer un commit

```bash
git commit -m "Add login page"
```

### Exemples de bons messages

```text
Add authentication
Fix navbar
Update README
```

### Exemples de mauvais messages

```text
test
aaa
modif
```

## Historique

```bash
git log
git log --oneline
git log --graph --oneline --all
git show
```

## Common mistakes

- Commits trop gros et heterogenes.
- Messages de commit non explicites.
- Ne pas inspecter l'historique avant rebase/merge.

## Best practices

- Commits petits et coherents.
- Messages a l'imperatif, explicites sur l'intention.
- Utiliser `git log --graph --oneline --all` pour visualiser rapidement l'etat du repo.

## Questions d'entretien

- Que montre `git show` ?
- Pourquoi un bon message de commit est important en equipe ?

## Suite

Module suivant: [03 - Branches et merge](03-branches-merge.md)
