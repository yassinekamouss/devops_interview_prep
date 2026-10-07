# Heap / Priority Queue

## When to think about it

Strong trigger phrases:

- Kth largest
- Kth smallest
- Top K
- K closer
- Smaller K
- Continuously obtain the minimum
- Continuously obtain the maximum
- Merge K sorted lists
- Process highest/lowest priority

## Exemple : Kth Largest

```text
[3, 2, 1, 5, 6, 4]
k = 2
```

Question: what is the 2nd largest element? → a heap is a good candidate.

## Recognition rule

!!! tip "Ruler"
Kth / Top K / Closest K → **Heap candidate**

!!! warning “Caution”
    “Kth” does not automatically mean “heap”. Quickselect, sort, or binary search may be more suitable depending on the problem. The heap is the first reflex to investigate, not an automatic conclusion.

## Typical problems

- Kth Largest Element
- Top K Frequent Elements
- K Closest Points to Origin
- Merge K Sorted Lists
- Find Median from Data Stream
- Task Scheduler