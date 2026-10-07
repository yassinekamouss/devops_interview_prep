# Breadth-First Search (BFS)

## When to think about it

Think **BFS** when the problem involves:

- Level-by-level exploration.
- A minimum number of movements.
- A shorter path.
- The nearest node.
- As few steps as possible.

Particularly: **shortest path in an unweighted graph**.

## Idea / Intuition

```text
Distance 0 → Distance 1 → Distance 2 → Distance 3
```

So the first time we reach a node, we found its shortest distance.

## Recognition rule

!!! tip "Ruler"
Shortest path + Unweighted → **BFS**

## Typical problems

- Binary Tree Level Order Traversal
- Rotting Oranges
- Word Ladder
- Shortest Path in Binary Matrix
- Minimum Knight Moves