# Cheat sheet maintenance

## The interview decision tree

When faced with a new problem, go through this checklist.

### Step 1 — Is this a pair?

```text
Paire ?
 ├── Trié → Two Pointers
 └── Non trié → Hash Map
```

### Step 2 — Is it contiguous?

```text
Sous-tableau / Sous-chaîne ?
          ↓
Sliding Window ou Prefix Sum
```

- Optimization over a dynamic range → **Sliding Window**
- Subarray sums / range sums → **Prefix Sum**

### Step 3 — Is there a K?

```text
Kième / Top K / K plus proches
          ↓
     Heap candidat
```

### Step 4 — Is the search space sorted or monotonic?

```text
Oui → Binary Search
```

Particularly: “Can we do X?” », “What is the minimum X that works? », “What is the maximum X that works? »

### Step 5 — Is this a stack problem?

```text
Correspondance / Imbrication / Précédent → Stack
Prochain plus grand / plus petit → Monotonic Stack
```

### Step 6 — Is it a tree?

```text
Arbre
 ├── Niveau par niveau → BFS
 └── Structure récursive → DFS
```

### Step 7 — Is this a graph?

```text
Graphe
 ├── Connectivité → DFS / BFS / Union Find
 ├── Plus court chemin non pondéré → BFS
 ├── Plus court chemin pondéré → Dijkstra
 ├── Dépendances → Topological Sort
 └── Coût de connexion minimal → MST
```

### Step 8 — Are we asking all the possibilities?

```text
Toutes les combinaisons / permutations / sous-ensembles / configurations
             ↓
        Backtracking
```

### Step 9 — Is this an optimization problem?

```text
Maximum / Minimum / Nombre de façons
              ↓
       DP ou Greedy
```

Ask yourself: “Can I prove that a local choice is always optimal? » → **Greedy**. Otherwise, look for repeated subproblems + state → **DP**.

---

## The “20 seconds” cheat sheet

For those times when your brain temporarily becomes a potato:

| Signal | Pattern |
|---|---|
| Have I seen this before? | Hash Map / Set |
| Sorted + pair? | Two Pointers |
| Contiguous + longer/shorter? | Sliding Window |
| Sorted/monotonic search space? | Binary Search |
| Matching/nesting? | Stack |
| Next biggest/smallest? | Monotonic Stack |
| Kth / Top K / closest? | Heap |
| Level by level / shorter unweighted? | BFS |
| Explore a connected structure? | DFS |
| ALL the possibilities? | Backtracking |
| Cycle / middle of linked list? | Fast + Slow Pointers |
| Intervals/overlap/meetings? | Sort + Intervals |
| Sum of range/subarray? | Prefix Sum |
| Prefix / autocompletion? | Trie |
| Dependencies / prerequisites? | Topological Sort |
| Related components / merging groups? | Union Find |
| Shortest weighted path? | Dijkstra |
| Connecter tout à moindre coût ? | MST |
| Max / Min / Nombre de façons + états répétés ? | DP |
| Choix localement optimal prouvable ? | Greedy |

---

## Ordre de priorité pour la préparation

Ne cherchez pas à maîtriser tous les algorithmes en même temps.

### Tier 1 — À maîtriser absolument
- Hash Map / Set
- Two Pointers
- Sliding Window
- Binary Search
- Stack
- Linked List
- Fast & Slow Pointers
- Trees + DFS
- BFS
- Heap

### Tier 2 — Très important
- Intervals
- Prefix Sum
- Backtracking
- Graph DFS/BFS
- Dynamic Programming
- Greedy

### Tier 3 — Avancé
- Trie
- Union Find
- Topological Sort
- Dijkstra
- Minimum Spanning Tree
- Bit Manipulation

---

## L'objectif réel

Ce n'est **pas** :

> Mémoriser 500 solutions LeetCode

C'est :

```text
Reconnaître le pattern → Comprendre pourquoi il marche → Connaître le template → Adapter le template → Analyser la complexité
```

### Exemple 1

> « Trouver la plus longue sous-chaîne contenant au plus K caractères distincts. »

```text
Sous-chaîne → Contigu → Le plus long → Contrainte sur la fenêtre → Sliding Window → Hash Map / compteur de fréquence
```

### Exemple 2

> « Trouver les K points les plus proches de l'origine. »

```text
K plus proches → Heap candidat → Calcul de distance → Priority Queue
```

### Exemple 3

> « Vous avez des cours et des prérequis. Déterminez si tous les cours peuvent être complétés. »

```text
Prérequis → Dépendances → Graphe dirigé → Détection de cycle → Topological Sort
```

C'est la véritable compétence d'entretien : **traduire le langage naturel en pattern algorithmique**. Une fois cette traduction automatique, LeetCode cesse d'être une collection de puzzles aléatoires et devient un vocabulaire restreint de structures récurrentes.