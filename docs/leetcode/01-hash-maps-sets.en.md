# Hash Map / Hash Set

## When to think about it

Think **Hashmap / Hashset** when the problem asks:

- Have I seen this value before?
- Is there a duplicate?
- How many times does an item appear?
- What is the frequency of each element?
- Is there a complement / a given value?
- Can I group elements by a property?

!!! tip "Trigger phrase"
“Have I seen this before?” »

- Generally → **Hash Set**
    - If you need to associate a value with information → **Hash Map**

## Exemple : Two Sum

```text
nums = [2, 7, 11, 15]
target = 9
```

For each number: `complement = target - current`

1. For `2`: `9 - 2 = 7`. We haven't seen `7` yet. We store `2`.
2. We reach `7`: `9 - 7 = 2`. `2` already exists.

Result: `[2, 7]`

## Complexity

- **Time:** O(n)
- **Space:** Y(n)

## Typical problems

- Two Sum
- Contains Duplicate
- Valid Anagram
- Group Anagrams
- Longest Consecutive Sequence
- Subarray Sum Equals K