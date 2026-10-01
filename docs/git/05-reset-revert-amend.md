# Git 05 - Reset, revert et amend

## Objectif du module

Maitriser les operations de correction d'historique local et partager proprement ses changements.

## Git reset

Le reset deplace le pointeur d'une branche.

Avant:

```text
A ---- B ---- C ---- D
                     ▲
                    main
```

Apres:

```bash
git reset HEAD~1
```

```text
A ---- B ---- C
               ▲
              main
```

## Les 3 modes

### Soft

```bash
git reset --soft HEAD~1
```

Conserve Working Directory + Staging, supprime seulement le commit.

### Mixed (defaut)

```bash
git reset HEAD~1
```

Conserve Working Directory, vide le Staging.

### Hard

```bash
git reset --hard HEAD~1
```

Supprime commit + staging + modifications locales.

## Reset vs revert

### Reset

```text
A ---- B ---- C ---- D

->

A ---- B ---- C
```

Le commit disparait de l'historique local de la branche.

### Revert

```text
A ---- B ---- C ---- D ---- E
```

`E` annule `D`, l'historique reste intact.

## Commit amend

Modifier le dernier commit.

Changer le message:

```bash
git commit --amend -m "Correct message"
```

Ajouter un fichier oublie:

```bash
git add style.css
git commit --amend
```

Le commit est recree, SHA modifie. A eviter apres push partage.

## Common mistakes

- Utiliser `--hard` sans verifier l'impact.
- Faire `amend` apres publication d'un commit deja partage.

## Best practices

- Preferer `revert` sur branche partagee.
- Utiliser `reset` pour nettoyage local pre-push.

## Questions d'entretien

- Difference reset vs revert ?
- Quand utiliser `--soft` plutot que `--mixed` ?
- Pourquoi `amend` modifie le SHA ?

## Suite

Module suivant: [06 - Stash](06-stash.md)
