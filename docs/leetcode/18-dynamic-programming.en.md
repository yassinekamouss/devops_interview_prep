# Dynamic Programming

This is one of the most important maintenance patterns.

!!! warning "Don't think"
“DP means complicated table. »

!!! tip "Think instead"
A problem has repeated subproblems, and previous decisions can be represented as a state.

## Trigger phrases

- Maximum
- Minimum
- Number of ways
- Can we achieve X?
- Choose / not choose
- Previous decisions affect future decisions

## Exemple : House Robber

To each house: **burglary** or **not to burglarize**.

```text
dp[i] = argent maximum obtenable avec les maisons 0..i

dp[i] = max(
    dp[i - 1],
    dp[i - 2] + nums[i]
)
```

## Typical problems

- Climbing Stairs
- House Robber
- Coin Change
- Longest Increasing Subsequence
- Longest Common Subsequence
- Word Break
- Partition Equal Subset Sum