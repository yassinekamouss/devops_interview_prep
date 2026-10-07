# Trees et DFS

## Depth-First Search (DFS)

### When to think about it

Think **DFS** when you need to:

- Explore an entire structure.
- Find related components.
- Determine if a path exists.
- Browse a tree.
- Explore a graph in depth.

### Idea / Intuition

```text
Start → Go deep → Go deeper → Dead end → Backtrack
```

### Typical problems

- Number of Islands
- Clone Graph
- Path Sum
- Maximum Depth of Binary Tree
- Flood Fill

### Recognition rule

!!! tip "Ruler"
Explore a connected structure → **DFS**

---

## Trees

Tree problems often boil down to a small set of patterns: **DFS**, **BFS**, and the three classic paths.

### Course (Tree DFS)

- **Preorder**: Root → Left → Right
- **Inorder**: Left → Root → Right
- **Postorder**: Left → Right → Root

### Important property of BST

Pour un Binary Search Tree : `Gauche < Racine < Droite`

!!! note "Classic tip"
Traversing **inorder** of a BST produces sorted values. This is a very common maintenance tip.

### Trigger phrases

- Depth (depth)
- Height
- Subtree
- Ancestor
- Path
- Balanced
-Binary Search Tree
- Lowest Common Ancestor

### Typical problems

- Maximum Depth of Binary Tree
- Diameter of Binary Tree
- Validate BST
- Lowest Common Ancestor
- Serialize and Deserialize Binary Tree
- Binary Tree Level Order Traversal