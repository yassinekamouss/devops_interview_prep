# Intervals

## Phrases déclencheuses

- Intervals
- Ranges (plages)
- Overlap (chevauchement)
- Meetings (réunions)
- Schedule (planning)
- Start/end

## Exemple

```text
[1,3]
[2,6]
```

Ces intervalles se chevauchent, donc : `[1,6]`

## Approche standard

```text
Trier par début → Traiter les intervalles → Fusionner / compter / supprimer
```

## Règle de reconnaissance

!!! tip "Règle"
    Plages + Chevauchement → **Trier + Intervals**

## Problèmes typiques

- Merge Intervals
- Insert Interval
- Meeting Rooms
- Meeting Rooms II
- Non-overlapping Intervals