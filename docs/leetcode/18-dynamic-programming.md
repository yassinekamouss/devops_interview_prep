# Dynamic Programming

C'est l'un des patterns d'entretien les plus importants.

!!! warning "Ne pensez pas"
    « DP veut dire tableau compliqué. »

!!! tip "Pensez plutôt"
    Un problème a des sous-problèmes répétés, et les décisions précédentes peuvent être représentées comme un état.

## Phrases déclencheuses

- Maximum
- Minimum
- Nombre de façons
- Peut-on atteindre X ?
- Choisir / ne pas choisir
- Les décisions précédentes affectent les décisions futures

## Exemple : House Robber

À chaque maison : **cambrioler** ou **ne pas cambrioler**.

```text
dp[i] = argent maximum obtenable avec les maisons 0..i

dp[i] = max(
    dp[i - 1],
    dp[i - 2] + nums[i]
)
```

## Problèmes typiques

- Climbing Stairs
- House Robber
- Coin Change
- Longest Increasing Subsequence
- Longest Common Subsequence
- Word Break
- Partition Equal Subset Sum