# Git 04 - Conflits et rebase

## Objectif du module

Savoir resoudre les conflits et choisir correctement entre merge et rebase.

## Merge conflicts

Un conflit apparait quand deux branches modifient la meme ligne.

Exemple:

```text
<<<<<<< HEAD
Version main
=======
Version feature
>>>>>>> feature/login
```

Resolution:

1. Modifier le fichier
2. Supprimer les marqueurs
3. Ajouter le fichier

```bash
git add README.md
git commit
```

Annuler un merge en cours:

```bash
git merge --abort
```

## Rebase

Mettre une branche a jour:

```bash
git switch feature/login
git rebase main
```

Avant:

```text
A ---- B ---- E ---- F
      \
       C ---- D
```

Apres:

```text
A ---- B ---- E ---- F ---- C' ---- D'
```

Les commits sont recrees, le SHA change.

## Gestion des conflits en rebase

```bash
git add README.md
git rebase --continue
git rebase --abort
git rebase --skip
```

## Rebase interactif

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

## Merge vs rebase

| Merge                      | Rebase               |
| -------------------------- | -------------------- |
| Conserve l'historique      | Reecrit l'historique |
| Peut creer un Merge Commit | Aucun Merge Commit   |
| Historique ramifie         | Historique lineaire  |

## Common mistakes

- Rebase d'une branche deja partagee sans coordination.
- Resolution de conflit trop rapide sans verification fonctionnelle.

## Best practices

- Utiliser rebase surtout sur branche personnelle.
- Garder merge quand on veut preserver le contexte historique collectif.

## Questions d'entretien

- Difference merge vs rebase ?
- Pourquoi le SHA change apres rebase ?

## Suite

Module suivant: [05 - Reset, revert et amend](05-reset-revert-amend.md)
