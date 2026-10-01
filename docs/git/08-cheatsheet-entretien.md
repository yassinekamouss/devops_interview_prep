# Git 08 - Cheatsheet et questions d'entretien

## Objectif du module

Consolider rapidement les commandes et reponses classiques d'entretien DevOps.

## Tableau recapitulatif

| Commande              | Description                            |
| --------------------- | -------------------------------------- |
| git init              | Initialise un depot Git                |
| git status            | Affiche l'etat du depot                |
| git add               | Ajoute des fichiers au staging         |
| git diff              | Affiche les modifications              |
| git commit            | Cree un commit                         |
| git log               | Affiche l'historique                   |
| git show              | Detail d'un commit                     |
| git branch            | Liste les branches                     |
| git switch            | Change de branche                      |
| git merge             | Fusionne une branche                   |
| git merge --abort     | Annule un merge                        |
| git rebase            | Reecrit l'historique                   |
| git rebase -i         | Rebase interactif                      |
| git rebase --continue | Continue un rebase                     |
| git rebase --abort    | Annule un rebase                       |
| git reset             | Deplace HEAD                           |
| git reset --soft      | Annule le commit uniquement            |
| git reset --mixed     | Retire du staging                      |
| git reset --hard      | Revient exactement a un etat precedent |
| git commit --amend    | Modifie le dernier commit              |
| git stash             | Sauvegarde temporairement le travail   |
| git stash pop         | Restaure et supprime le stash          |
| git stash apply       | Restaure sans supprimer                |
| git stash list        | Liste les stashes                      |
| git stash clear       | Supprime tous les stashes              |

## Questions classiques d'entretien

### Difference Merge et Rebase

Merge conserve l'historique reel et peut creer un merge commit.
Rebase reecrit l'historique pour le rendre lineaire.

### Difference Reset et Revert

Reset reecrit l'historique.
Revert cree un nouveau commit qui annule un ancien.

### Quand utiliser Stash ?

Quand le travail n'est pas termine mais qu'il faut changer rapidement de branche.

### Quand utiliser Amend ?

Pour corriger le dernier commit (message ou contenu) avant partage.

### Quand utiliser Rebase ?

Pour mettre a jour une branche de travail ou nettoyer l'historique avant Pull Request.

## Conseils de revision entretien

1. Rejouer les commandes sur un depot de test.
2. Expliquer a voix haute chaque scenario (merge, rebase, reset, revert).
3. S'entrainer a lire les graphes de commits rapidement.
