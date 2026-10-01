# Git 03 - Branches et merge

## Objectif du module

Comprendre les branches comme pointeurs, puis maitriser les fusions de base.

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

Une branche est un pointeur:

```text
A ---- B ---- C
              ▲
             main
              ▲
        feature/login
```

Git ne copie pas les fichiers; il deplace des references vers des commits.

## Merge

Fusionner une branche:

```bash
git switch main
git merge feature/login
```

Regle: se placer sur la branche qui recoit les modifications.

### Fast-forward

```text
A ---- B ---- C ---- D
                     ▲
                    main
                    feature
```

Git deplace le pointeur.

### Merge commit

```text
A ---- B ---- E -------- M
      \                /
       C ---- D ------/
```

Git cree un commit de fusion.

## Common mistakes

- Lancer `git merge` depuis la mauvaise branche.
- Supprimer une branche non fusionnee sans verification.

## Best practices

- Utiliser une branche par fonctionnalite.
- Nettoyer les branches fusionnees.

## Questions d'entretien

- Qu'est-ce qu'un fast-forward ?
- Quand obtient-on un merge commit ?

## Suite

Module suivant: [04 - Conflits et rebase](04-conflits-rebase.md)
