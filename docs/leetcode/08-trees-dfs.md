# Trees et DFS

## Depth-First Search (DFS)

### Quand y penser

Pensez **DFS** quand vous devez :

- Explorer une structure entière.
- Trouver des composantes connexes.
- Déterminer si un chemin existe.
- Parcourir un arbre.
- Explorer un graphe en profondeur.

### Idée / Intuition

```text
Start → Go deep → Go deeper → Dead end → Backtrack
```

### Problèmes typiques

- Number of Islands
- Clone Graph
- Path Sum
- Maximum Depth of Binary Tree
- Flood Fill

### Règle de reconnaissance

!!! tip "Règle"
    Explorer une structure connectée → **DFS**

---

## Trees

Les problèmes d'arbres se ramènent souvent à un petit ensemble de patterns : **DFS**, **BFS**, et les trois parcours classiques.

### Parcours (Tree DFS)

- **Preorder** : Racine → Gauche → Droite
- **Inorder** : Gauche → Racine → Droite
- **Postorder** : Gauche → Droite → Racine

### Propriété importante des BST

Pour un Binary Search Tree : `Gauche < Racine < Droite`

!!! note "Astuce classique"
    Le parcours **inorder** d'un BST produit des valeurs triées. C'est une astuce d'entretien très courante.

### Phrases déclencheuses

- Depth (profondeur)
- Height (hauteur)
- Subtree (sous-arbre)
- Ancestor (ancêtre)
- Path (chemin)
- Balanced (équilibré)
- Binary Search Tree
- Lowest Common Ancestor

### Problèmes typiques

- Maximum Depth of Binary Tree
- Diameter of Binary Tree
- Validate BST
- Lowest Common Ancestor
- Serialize and Deserialize Binary Tree
- Binary Tree Level Order Traversal