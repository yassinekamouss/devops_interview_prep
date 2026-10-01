# Hash Map / Hash Set

## Quand y penser

Pensez **Hash Map / Hash Set** quand le problème demande :

- Ai-je déjà vu cette valeur ?
- Existe-t-il un doublon ?
- Combien de fois un élément apparaît-il ?
- Quelle est la fréquence de chaque élément ?
- Existe-t-il un complément / une valeur donnée ?
- Puis-je regrouper des éléments par une propriété ?

!!! tip "Phrase déclencheuse"
    « Ai-je déjà vu ceci ? »

    - Généralement → **Hash Set**
    - Si vous devez associer une valeur à une information → **Hash Map**

## Exemple : Two Sum

```text
nums = [2, 7, 11, 15]
target = 9
```

Pour chaque nombre : `complement = target - current`

1. Pour `2` : `9 - 2 = 7`. On n'a pas encore vu `7`. On stocke `2`.
2. On atteint `7` : `9 - 7 = 2`. `2` existe déjà.

Résultat : `[2, 7]`

## Complexité

- **Temps :** O(n)
- **Espace :** O(n)

## Problèmes typiques

- Two Sum
- Contains Duplicate
- Valid Anagram
- Group Anagrams
- Longest Consecutive Sequence
- Subarray Sum Equals K