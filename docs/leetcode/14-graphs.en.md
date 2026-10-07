# Graphs

As soon as you see **Nodes + Connections**, think **Graph**.

Connections can be:

- `A → B` (directed)
- `A ↔ B` (undirected)
- `A --5--> B` (weighted)

## Identify the question

| Question | Pattern |
|---|---|
| Is A connected to B? | DFS / BFS |
| How many components? | DFS / BFS / Union Find |
| Unweighted shortest path? | BFS |
| Shortest weighted path? | Dijkstra |
| Dependencies? | Topological Sort |
| Minimum cost to connect everything? | MST |
| Detect a cycle? | DFS / Union Find |

## Typical problems

- Clone Graph
- Number of Provinces
- Course Schedule
- Network Delay Time