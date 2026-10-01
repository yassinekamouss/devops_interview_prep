# Cheatsheet Entretien

## L'arbre de décision en entretien

Face à un nouveau problème, parcourez ce checklist.

### Étape 1 — S'agit-il d'une paire ?

```text
Paire ?
 ├── Trié → Two Pointers
 └── Non trié → Hash Map
```

### Étape 2 — Est-ce contigu ?

```text
Sous-tableau / Sous-chaîne ?
          ↓
Sliding Window ou Prefix Sum
```

- Optimisation sur une plage dynamique → **Sliding Window**
- Sommes de sous-tableaux / sommes de plages → **Prefix Sum**

### Étape 3 — Y a-t-il un K ?

```text
Kième / Top K / K plus proches
          ↓
     Heap candidat
```

### Étape 4 — L'espace de recherche est-il trié ou monotone ?

```text
Oui → Binary Search
```

Particulièrement : « Peut-on faire X ? », « Quel est le X minimum qui fonctionne ? », « Quel est le X maximum qui fonctionne ? »

### Étape 5 — S'agit-il d'un problème en forme de stack ?

```text
Correspondance / Imbrication / Précédent → Stack
Prochain plus grand / plus petit → Monotonic Stack
```

### Étape 6 — S'agit-il d'un arbre ?

```text
Arbre
 ├── Niveau par niveau → BFS
 └── Structure récursive → DFS
```

### Étape 7 — S'agit-il d'un graphe ?

```text
Graphe
 ├── Connectivité → DFS / BFS / Union Find
 ├── Plus court chemin non pondéré → BFS
 ├── Plus court chemin pondéré → Dijkstra
 ├── Dépendances → Topological Sort
 └── Coût de connexion minimal → MST
```

### Étape 8 — Demande-t-on toutes les possibilités ?

```text
Toutes les combinaisons / permutations / sous-ensembles / configurations
             ↓
        Backtracking
```

### Étape 9 — Est-ce un problème d'optimisation ?

```text
Maximum / Minimum / Nombre de façons
              ↓
       DP ou Greedy
```

Posez-vous la question : « Puis-je prouver qu'un choix local est toujours optimal ? » → **Greedy**. Sinon, cherchez des sous-problèmes répétés + un état → **DP**.

---

## La cheat sheet "20 secondes"

Pour les moments où votre cerveau devient temporairement une patate :

| Signal | Pattern |
|---|---|
| Ai-je déjà vu ceci ? | Hash Map / Set |
| Trié + paire ? | Two Pointers |
| Contigu + plus long/court ? | Sliding Window |
| Espace de recherche trié / monotone ? | Binary Search |
| Correspondance / imbrication ? | Stack |
| Prochain plus grand / plus petit ? | Monotonic Stack |
| Kième / Top K / plus proche ? | Heap |
| Niveau par niveau / plus court non pondéré ? | BFS |
| Explorer une structure connectée ? | DFS |
| TOUTES les possibilités ? | Backtracking |
| Cycle / milieu de liste chaînée ? | Fast + Slow Pointers |
| Intervalles / chevauchement / réunions ? | Sort + Intervals |
| Somme de plage / sous-tableau ? | Prefix Sum |
| Préfixe / autocomplétion ? | Trie |
| Dépendances / prérequis ? | Topological Sort |
| Composantes connexes / fusion de groupes ? | Union Find |
| Plus court chemin pondéré ? | Dijkstra |
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