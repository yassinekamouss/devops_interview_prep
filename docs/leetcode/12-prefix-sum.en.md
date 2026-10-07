# Prefix Sum

## Trigger phrases

- Range sum
- Subarray sum
- Cumulative sum
- Sum between i and j

## Example

```text
nums = [2, 4, 1, 3]
prefix = [0, 2, 6, 7, 10]
```

SO :

```text
sum(i, j) = prefix[j + 1] - prefix[i]
```

## Powerful combination

**Prefix Sum + Hash Map**, particularly useful for:

> Number of subarrays whose sum is K

This combination appears very frequently in interviews.

## Typical problems

- Range Sum Query
- Subarray Sum Equals K
- Continuous Subarray Sum