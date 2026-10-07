# Union Find

Also called **Disjoint Set Union (DSU)**.

## Trigger phrases

- Related components
- Merge groups
- Are these elements in the same group?
- Dynamic connectivity
- Connect two components

## Example

```text
{A, B, C}   {D, E}

connect(C, D)
   ↓
{A, B, C, D, E}
```

## Recognition rule

!!! tip "Ruler"
Are these two elements in the same connected group? → **Union Find**

## Typical problems

- Number of Provinces
- Redundant Connection
- Accounts Merge
- Kruskal's Minimum Spanning Tree