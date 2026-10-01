# Fast and Slow Pointers

## Phrases déclencheuses

- Cycle
- Boucle (loop)
- Milieu d'une liste chaînée
- Détecter un état répété

## Idée / Intuition

Utiliser deux pointeurs :

- `slow` → avance d'1 pas
- `fast` → avance de 2 pas

Si les deux pointeurs se rencontrent → un cycle existe.

## Règle de reconnaissance

!!! tip "Règle"
    Cycle / Milieu → **Fast + Slow Pointers**

## Problèmes typiques

- Linked List Cycle
- Linked List Cycle II
- Middle of the Linked List
- Happy Number