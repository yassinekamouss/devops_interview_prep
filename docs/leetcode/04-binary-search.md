# Binary Search

## Cas classique

Le déclencheur évident : **tableau trié**.

```text
[1, 2, 3, 4, 5, 6, 7, 8, 9]
              ↑
            target
```

Au lieu de vérifier chaque élément (`O(n)`), on élimine la moitié de l'espace de recherche à chaque étape (`O(log n)`).

## Cas plus important : Binary Search sur la réponse

Le Binary Search ne se limite pas aux tableaux. Posez-vous la question :

> Puis-je chercher sur l'espace des réponses possibles ?

**Exemple : Koko Eating Bananas**

Vitesses possibles : `1, 2, 3, ..., max(piles)`.

Si la vitesse `X` fonctionne, toute vitesse supérieure à `X` fonctionne aussi → condition **monotone** → **Binary Search on Answer**.

## Phrases déclencheuses

- Trié
- Trouver une cible
- Minimum possible
- Maximum possible
- Plus petite valeur satisfaisant une condition
- Plus grande valeur satisfaisant une condition
- Peut-on atteindre X ?
- Capacité minimale
- Vitesse minimale
- Distance maximale

## Règle de reconnaissance

!!! tip "Règle"
    Puis-je éliminer la moitié des possibilités ? → **Binary Search**

## Problèmes typiques

- Binary Search classique
- Koko Eating Bananas
- Search in Rotated Sorted Array