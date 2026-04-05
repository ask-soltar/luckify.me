---
name: vs_avg Sign Convention (CRITICAL)
description: Golf scoring sign convention for vs_avg metric. Negative = beat field, Positive = lost to field.
type: feedback
---

## The Sign Convention (MUST MEMORIZE)

### Definition
```
vs_avg = player_score - course_avg
```

### Correct Interpretation
- **vs_avg < 0 (NEGATIVE)** = Player scored **LOWER** than field = **BEAT THE FIELD** ✓
- **vs_avg > 0 (POSITIVE)** = Player scored **HIGHER** than field = **LOST TO FIELD** ✗

### Example
- Player score: 68
- Course average: 70
- vs_avg = 68 - 70 = **-2**
- Meaning: Beat field by 2 strokes (shot 2 lower than average)

---

## What This Means for Signal Interpretation

When reading our validated signals:

| Signal | vs_avg Value | Correct Meaning |
|--------|--------------|-----------------|
| Red × Exec 50-75 × Closing | −0.936 | **Beats field** by 0.936 strokes |
| Orange × Exec 75-100 × Earth | −1.242 | **Beats field** by 1.242 strokes |
| Orange × Exec 50-75 × Open | +0.461 | **Loses to field** by 0.461 strokes (FADE) |
| Green × Exec 25-50 × Water | +0.707 | **Loses to field** by 0.707 strokes (FADE) |

---

## When Writing Code/Analysis

Always check:
1. **Column is vs_avg = score - course_avg** (not inverted)
2. **Negative signals are POSITIVE for betting** (beat field)
3. **Positive signals are NEGATIVE for betting** (lose to field)
4. **Never flip the sign without stating it explicitly**

---

## Historical Error (Documented for Learning)

On 2026-04-05, signal interpretation was initially backwards:
- Said "+0.936 = outperformance" ❌
- Correct: "-0.936 = outperformance" ✓

All 7 validated signals remain valid. Only the sign interpretation was inverted in the writeup.

---

**Rule:** When discussing vs_avg metrics in any future analysis, **always clarify whether you're talking about the raw vs_avg number or the betting interpretation.**

Example:
- "vs_avg = +0.5" (raw number, meaning underperform)
- "Beats field by 0.5" (betting interpretation, negative edge for opponent)
