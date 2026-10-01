# Two Pointers

## Quand y penser

Pensez **Two Pointers** quand :

- Le tableau est trié.
- Vous cherchez une paire.
- Vous devez comparer des éléments depuis les deux extrémités.
- Vous devez supprimer des doublons.
- Vous devez parcourir un tableau efficacement.

## Idée / Intuition

Structure typique :

```text
L →                 ← R
[1, 2, 3, 4, 6]
```

- Si `nums[L] + nums[R] < target` → `L++`
- Si `nums[L] + nums[R] > target` → `R--`

## Règle de reconnaissance

!!! tip "Règle"
    Trié + Paire → **Two Pointers**

## Problèmes typiques

- Two Sum II
- 3Sum
- Container With Most Water
- Valid Palindrome
- Remove Duplicates from Sorted Array