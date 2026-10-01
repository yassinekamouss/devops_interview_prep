# Breadth-First Search (BFS)

## Quand y penser

Pensez **BFS** quand le problème implique :

- Une exploration niveau par niveau.
- Un nombre minimal de mouvements.
- Un plus court chemin.
- Le nœud le plus proche.
- Le moins d'étapes possible.

Particulièrement : **plus court chemin dans un graphe non pondéré**.

## Idée / Intuition

```text
Distance 0 → Distance 1 → Distance 2 → Distance 3
```

Donc, la première fois qu'on atteint un nœud, on a trouvé sa distance la plus courte.

## Règle de reconnaissance

!!! tip "Règle"
    Plus court chemin + Non pondéré → **BFS**

## Problèmes typiques

- Binary Tree Level Order Traversal
- Rotting Oranges
- Word Ladder
- Shortest Path in Binary Matrix
- Minimum Knight Moves