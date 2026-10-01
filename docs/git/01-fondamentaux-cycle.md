# Git 01 - Fondamentaux et cycle de vie

## Objectif du module

Comprendre la base d'un depot Git et le cycle Working Directory -> Staging -> Repository.

## Initialiser un depot

### Creer un dossier

```bash
mkdir git-training
cd git-training
```

### Initialiser Git

```bash
git init
```

Git cree le dossier cache:

```text
.git/
```

Il contient la base de donnees Git.

## Verifier l'etat

```bash
git status
```

`git status` indique:

- la branche actuelle
- les fichiers modifies
- les fichiers non suivis
- les fichiers prets a etre commites

## Cycle de vie d'un fichier

```text
                git add             git commit
Working Dir  ------------->  Staging Area -------------> Repository
```

### Working Directory

Fichiers presents sur ton ordinateur.

### Staging Area

Zone intermediaire contenant ce que tu veux inclure dans le prochain commit.

### Repository

Historique permanent du projet.

## Common mistakes

- Commiter sans verifier `git status`.
- Ne pas comprendre la difference entre Working Directory et Staging.

## Best practices

- Verifier `git status` tres frequemment.
- Ajouter au staging uniquement les changements pertinents.

## Questions d'entretien

- A quoi sert `.git/` ?
- Difference entre Working Directory, Staging et Repository ?

## Suite

Module suivant: [02 - Commits et historique](02-commits-historique.md)
