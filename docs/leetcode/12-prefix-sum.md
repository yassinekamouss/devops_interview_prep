# Prefix Sum

## Phrases déclencheuses

- Somme sur une plage (range sum)
- Somme de sous-tableau (subarray sum)
- Somme cumulative
- Somme entre i et j

## Exemple

```text
nums = [2, 4, 1, 3]
prefix = [0, 2, 6, 7, 10]
```

Alors :

```text
sum(i, j) = prefix[j + 1] - prefix[i]
```

## Combinaison puissante

**Prefix Sum + Hash Map**, particulièrement utile pour :

> Nombre de sous-tableaux dont la somme vaut K

Cette combinaison apparaît très fréquemment en entretien.

## Problèmes typiques

- Range Sum Query
- Subarray Sum Equals K
- Continuous Subarray Sum