# Graphs

Dès que vous voyez **Nœuds + Connexions**, pensez **Graph**.

Les connexions peuvent être :

- `A → B` (dirigée)
- `A ↔ B` (non dirigée)
- `A --5--> B` (pondérée)

## Identifier la question

| Question | Pattern |
|---|---|
| A est-il connecté à B ? | DFS / BFS |
| Combien de composantes ? | DFS / BFS / Union Find |
| Plus court chemin non pondéré ? | BFS |
| Plus court chemin pondéré ? | Dijkstra |
| Dépendances ? | Topological Sort |
| Coût minimal pour tout connecter ? | MST |
| Détecter un cycle ? | DFS / Union Find |

## Problèmes typiques

- Clone Graph
- Number of Provinces
- Course Schedule
- Network Delay Time