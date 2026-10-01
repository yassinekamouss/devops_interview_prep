# Git 06 - Stash

## Objectif du module

Sauvegarder temporairement un travail incomplet pour changer de contexte rapidement.

## Commandes principales

Creer un stash:

```bash
git stash
```

Inclure les fichiers non suivis:

```bash
git stash -u
git stash --include-untracked
```

Lister les stashes:

```bash
git stash list
```

Voir le contenu:

```bash
git stash show
git stash show -p
```

Restaurer et supprimer:

```bash
git stash pop
```

Restaurer sans supprimer:

```bash
git stash apply
```

Supprimer:

```bash
git stash drop
git stash clear
```

Stash nomme:

```bash
git stash push -m "Debut authentification"
```

## Quand utiliser ?

Quand le travail n'est pas termine mais qu'il faut changer rapidement de branche.

## Common mistakes

- Oublier les stashes anciens.
- Utiliser stash comme stockage long terme.

## Best practices

- Nommer les stashes importants.
- Nettoyer regulierement `git stash list`.

## Questions d'entretien

- Difference `pop` vs `apply` ?
- Pourquoi utiliser `-u` ?

## Suite

Module suivant: [07 - Workflow et bonnes pratiques](07-workflow-bonnes-pratiques.md)
