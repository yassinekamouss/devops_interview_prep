# Backtracking

Le backtracking, c'est essentiellement :

```text
DFS + Undo
```

## Phrases déclencheuses

- Générer tout
- Toutes les possibilités
- Toutes les combinaisons
- Toutes les permutations
- Tous les sous-ensembles
- Choisir K
- Construire toutes les configurations valides

## Exemple

```text
nums = [1, 2, 3]
```

Génère : `123, 132, 213, 231, 312, 321`

On explore un arbre de décision :

```text
             []
          /   |   \
         1    2    3
       /  \
      2    3
```

## Règle de reconnaissance

!!! tip "Règle"
    « Donne-moi TOUTES les... » → **Backtracking**

## Problèmes typiques

- Subsets
- Permutations
- Combination Sum
- Letter Combinations of a Phone Number
- N-Queens
- Sudoku Solver
- Word Search