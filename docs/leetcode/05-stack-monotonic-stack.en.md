# Stack et Monotonic Stack

## Stack

### When to think about it

- Correspondence (matching)
- Nested structures
- Parentheses
- Most recent item
- “Undo” type behavior
- Relations with the previous element

A stack is **LIFO** (Last In → First Out). The most recently opened structure must be closed first:

```text
( [ { } ] )
```

### Typical problems

- Valid Parentheses
- Min Stack
- Evaluate Reverse Polish Notation
- Decode String
- Simplify Path

---

## Monotonic Stack

This is a particularly important interview pattern.

### Trigger phrases

- Next larger element
- Next smaller element
- Previous larger
- Previous smaller
-Daily temperature
- Histogram

### Example

```text
[73, 74, 75, 71, 69, 72, 76, 73]
```

Question: “When will it be warmer next?” » → **Monotonic Stack**

### Recognition rule

!!! tip "Ruler"
Next largest/smallest → **Monotonic Stack**

### Typical problems

- Daily Temperatures
- Next Greater Element
- Largest Rectangle in Histogram
- Stock Span