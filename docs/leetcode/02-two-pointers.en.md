# Two Pointers

## When to think about it

Think **Two Pointers** when:

- The table is sorted.
- Looking for a pair.
- You have to compare items from both ends.
- You must remove duplicates.
- You need to iterate through an array efficiently.

## Idea / Intuition

Typical structure:

```text
L →                 ← R
[1, 2, 3, 4, 6]
```

- Si `nums[L] + nums[R] < target` → `L++`
- Si `nums[L] + nums[R] > target` → `R--`

## Recognition rule

!!! tip "Ruler"
Sorted + Pair → **Two Pointers**

## Typical problems

- Two Sum II
- 3Sum
- Container With Most Water
- Valid Palindrome
- Remove Duplicates from Sorted Array