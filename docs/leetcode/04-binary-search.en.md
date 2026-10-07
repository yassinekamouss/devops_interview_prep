# Binary Search

## Classic case

The obvious trigger: **sorted array**.

```text
[1, 2, 3, 4, 5, 6, 7, 8, 9]
              ↑
            target
```

Instead of checking each element (`O(n)`), we eliminate half of the search space at each step (`O(log n)`).

## More important case: Binary Search on the response

Binary Search is not limited to tables. Ask yourself:

> Can I search the space for possible answers?

**Exemple : Koko Eating Bananas**

Possible speeds: `1, 2, 3, ..., max(piles)`.

If speed `X` works, any speed higher than `X` also works → condition **monotonous** → **Binary Search on Answer**.

## Trigger phrases

- Sorted
- Find a target
- Minimum possible
- Maximum possible
- Smallest value satisfying a condition
- Largest value satisfying a condition
- Can we achieve X?
- Minimum capacity
- Minimum speed
- Maximum distance

## Recognition rule

!!! tip "Ruler"
Can I eliminate half of the possibilities? → **Binary Search**

## Typical problems

- Binary Search classique
- Koko Eating Bananas
- Search in Rotated Sorted Array