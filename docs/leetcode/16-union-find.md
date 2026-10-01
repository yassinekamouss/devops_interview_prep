# Union Find

Aussi appelé **Disjoint Set Union (DSU)**.

## Phrases déclencheuses

- Composantes connexes
- Fusionner des groupes
- Ces éléments sont-ils dans le même groupe ?
- Connectivité dynamique
- Connecter deux composantes

## Exemple

```text
{A, B, C}   {D, E}

connect(C, D)
   ↓
{A, B, C, D, E}
```

## Règle de reconnaissance

!!! tip "Règle"
    Ces deux éléments sont-ils dans le même groupe connecté ? → **Union Find**

## Problèmes typiques

- Number of Provinces
- Redundant Connection
- Accounts Merge
- Kruskal's Minimum Spanning Tree