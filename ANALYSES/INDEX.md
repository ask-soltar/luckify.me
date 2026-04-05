# /ANALYSES/ — Index of All Analyses

All timestamped analysis outputs. Organized by date (most recent first).

---

## 2026-04-04 — Color × Personal Day Signal Testing

**Topic:** Do Color (BaZi Rhythm) × Personal Day (numerology) combos predict field-relative win rate?

**Status:** ❌ FAILED (out-of-sample validation)

**Files:**
- `20260404_color_personalday_findings.md` — Technical findings
- `20260404_color_personalday_analysis_corrected.md` — Full corrected analysis
- `20260404_color_personalday_condition_summary.md` — Performance by Calm/Moderate/Tough
- `20260404_color_personalday_quick_stats.txt` — Quick reference tables
- `20260404_color_personalday_signals.txt` — Signal summary
- `20260404_color_personalday_combos.csv` — All 96 combos with metrics
- `20260404_color_personalday_by_condition.csv` — Combos × conditions breakdown
- `20260404_backtest_summary.txt` — Train (2022-2024) vs Test (2025-2026) comparison
- `20260404_backtest_detailed.csv` — Full backtest metrics
- `20260404_consistency_insight_expanded.md` — Key finding on signal consistency

**Key Insight:**
Color × Personal Day signals fail out-of-sample (test WR 44.8%, -5.2% edge). Most patterns were spurious. Only consistency matters: Purple×Day7 (49.2% WR, 2.1% variance) useful as Kelly multiplier, not standalone.

**Verdict:**
Abandon as primary signal. Use only as Kelly sizing conditioner with validated 4D Element signals.

**Next Step:**
Focus on validated 4D Element combos (+4.6-5.9% edges). Combine with Purple×Day7 for stability.

---

## Prior Analyses (Archive)

Older analyses moved to `/ARCHIVE/`. See `ARCHIVE/INDEX.md` for reference.

**Most relevant archived work:**
- `FINAL_BETTING_SIGNALS.md` — Current deployed signals (4D Element)
- `CONSISTENCY_INSIGHT_EXPANDED.md` — Why signal stability matters

---

## How Analyses Are Named

**Format:** `YYYYMMDD_[topic]_[type].md|csv|txt`

**Examples:**
- `20260404_color_personalday_findings.md` — Report
- `20260404_color_personalday_combos.csv` — Data
- `20260404_backtest_summary.txt` — Results

**Topic:** What was analyzed (color_personalday, element_testing, etc.)

**Type:** findings | combos | conditions | backtest_summary | index | etc.

---

## To Add New Analysis

1. Run analysis in `/SCRIPTS/` using `/DATA/`
2. Save outputs with timestamp: `YYYYMMDD_[topic]_*`
3. Create short summary entry above
4. Add findings to `.claude/memory/MEMORY.md`
5. Link to CLAUDE.md work log

---

**Last updated:** 2026-04-04
