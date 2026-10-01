# Stack et Monotonic Stack

## Stack

### Quand y penser

- Correspondance (matching)
- Structures imbriquées
- Parenthèses
- Élément le plus récent
- Comportement de type « undo »
- Relations avec l'élément précédent

Une stack est **LIFO** (Last In → First Out). La structure ouverte le plus récemment doit être fermée en premier :

```text
( [ { } ] )
```

### Problèmes typiques

- Valid Parentheses
- Min Stack
- Evaluate Reverse Polish Notation
- Decode String
- Simplify Path

---

## Monotonic Stack

C'est un pattern d'entretien particulièrement important.

### Phrases déclencheuses

- Prochain élément plus grand
- Prochain élément plus petit
- Précédent plus grand
- Précédent plus petit
- Daily temperature
- Histogramme

### Exemple

```text
[73, 74, 75, 71, 69, 72, 76, 73]
```

Question : « Quand fera-t-il plus chaud ensuite ? » → **Monotonic Stack**

### Règle de reconnaissance

!!! tip "Règle"
    Prochain plus grand / plus petit → **Monotonic Stack**

### Problèmes typiques

- Daily Temperatures
- Next Greater Element
- Largest Rectangle in Histogram
- Stock Span