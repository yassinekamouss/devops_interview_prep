# Backtracking

Backtracking is essentially:

```text
DFS + Undo
```

## Trigger phrases

- Generate all
- All the possibilities
- All combinations
- All permutations
- All subassemblies
- Choose K
- Build all valid configurations

## Example

```text
nums = [1, 2, 3]
```

Generates: `123, 132, 213, 231, 312, 321`

We explore a decision tree:

```text
             []
          /   |   \
         1    2    3
       /  \
      2    3
```

## Recognition rule

!!! tip "Ruler"
“Give me ALL the…” → **Backtracking**

## Typical problems

- Subsets
- Permutations
- Combination Sum
- Letter Combinations of a Phone Number
- N-Queens
- Sudoku Solver
- Word Search