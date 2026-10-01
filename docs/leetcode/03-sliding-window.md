# Sliding Window

## Quand y penser

Repérez les mots-clés :

- Sous-tableau
- Sous-chaîne
- Contigu
- Consécutif
- Le plus long
- Le plus court
- Fenêtre maximale/minimale
- Au plus K
- Exactement K

Le mot important est : **contigu**.

## Idée / Intuition

Plutôt que de recalculer chaque sous-chaîne possible, on maintient une fenêtre glissante :

```text
L             R
↓             ↓
[a b c d e f]
```

- Déplacer `R` pour agrandir la fenêtre.
- Déplacer `L` pour la réduire.

## Règle de reconnaissance

!!! tip "Règle"
    Contigu + Optimisation → **Sliding Window**

## Problèmes typiques

- Longest Substring Without Repeating Characters
- Minimum Window Substring
- Longest Repeating Character Replacement
- Maximum Average Subarray
- Permutation in String