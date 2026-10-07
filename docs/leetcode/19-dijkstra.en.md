# Dijkstra

## Trigger phrases

- Shortest path
- Weighted graph
- Positive edge weights
- Minimal cost/travel time

## Example

```text
A --4--> B
A --1--> C
C --2--> B
```

Shortest path: `A → C → B`, cost `1 + 2 = 3`.

Typical implementation: **Dijkstra + Min Heap**.

## Recognition rule

!!! tip "Ruler"
Shortest path + Positive weights → **Dijkstra**

## Typical problems

- Network Delay Time
- Cheapest Flights Within K Stops (variantes)
- Path With Minimum Effort