# Sliding Window

## When to think about it

Locate the keywords:

- Sub-table
- Substring
- Contiguous
- Consecutive
- Longest
- The shortest
- Maximum/minimum window
- At most K
- Exactly K

The important word is: **contiguous**.

## Idea / Intuition

Rather than recalculating each possible substring, we maintain a sliding window:

```text
L             R
↓             ↓
[a b c d e f]
```

- Move `R` to enlarge the window.
- Move `L` to reduce it.

## Recognition rule

!!! tip "Ruler"
Contigu + Optimisation → **Sliding Window**

## Typical problems

- Longest Substring Without Repeating Characters
- Minimum Window Substring
- Longest Repeating Character Replacement
- Maximum Average Subarray
- Permutation in String