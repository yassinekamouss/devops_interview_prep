# Heap / Priority Queue

## Quand y penser

Phrases déclencheuses fortes :

- Kième plus grand (Kth largest)
- Kième plus petit (Kth smallest)
- Top K
- K plus proches
- K plus petits
- Obtenir en continu le minimum
- Obtenir en continu le maximum
- Fusionner K listes triées
- Traiter la priorité la plus haute/basse

## Exemple : Kth Largest

```text
[3, 2, 1, 5, 6, 4]
k = 2
```

Question : quel est le 2ᵉ plus grand élément ? → un heap est un bon candidat.

## Règle de reconnaissance

!!! tip "Règle"
    Kième / Top K / K plus proches → **Heap candidat**

!!! warning "Attention"
    « Kième » ne signifie pas automatiquement « heap ». Quickselect, tri, ou binary search peuvent être plus adaptés selon le problème. Le heap est le premier réflexe à investiguer, pas une conclusion automatique.

## Problèmes typiques

- Kth Largest Element
- Top K Frequent Elements
- K Closest Points to Origin
- Merge K Sorted Lists
- Find Median from Data Stream
- Task Scheduler