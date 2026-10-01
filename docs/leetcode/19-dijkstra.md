# Dijkstra

## Phrases déclencheuses

- Plus court chemin
- Graphe pondéré
- Poids d'arêtes positifs
- Coût/temps de trajet minimal

## Exemple

```text
A --4--> B
A --1--> C
C --2--> B
```

Plus court chemin : `A → C → B`, coût `1 + 2 = 3`.

Implémentation typique : **Dijkstra + Min Heap**.

## Règle de reconnaissance

!!! tip "Règle"
    Plus court chemin + Poids positifs → **Dijkstra**

## Problèmes typiques

- Network Delay Time
- Cheapest Flights Within K Stops (variantes)
- Path With Minimum Effort