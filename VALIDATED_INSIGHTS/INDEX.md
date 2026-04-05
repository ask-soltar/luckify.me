# VALIDATED INSIGHTS — Living Registry

**Status:** Foundation built, ready for first insights
**Purpose:** Central index for all tested theories (color rhythms, numerology, divination, player behavior)
**Owner:** Preston Lee / Claude (collaborative)
**Last Updated:** 2026-04-04

---

## 📊 Confidence Level System

Each insight is tracked by confidence level. Read left-to-right as progression:

| Level | Name | Status | Meaning |
|-------|------|--------|---------|
| 1️⃣ | **Live Theory** | 🔵 Untested | Intuited or channeled; not yet formally tested |
| 2️⃣ | **Needs Testing** | 🟡 Planned | Theory is clear; test plan exists; test not yet run |
| 3️⃣ | **Partially Backed** | 🟠 Mixed | Some tests pass; results inconclusive or weak; needs more data |
| 4️⃣ | **Fully Validated** | 🟢 Approved | Passes all rubber stamp gates; ready for application |
| 5️⃣ | **Rejected** | 🔴 Failed | Failed key tests; contradicts evidence; or abandoned |

---

## 🎯 How to Add an Insight

See [HOW_TO_ADD_INSIGHT.md](HOW_TO_ADD_INSIGHT.md) for complete workflow.

**Quick version:**
1. Create `[TOPIC_DATE].md` in `/LIVE_THEORY/`
2. Fill: Theory Name, Origin, Statement, Rationale, Next Steps
3. Once test planned → move to `/NEEDS_TESTING/` + link test script
4. After test runs → move to `/PARTIALLY_BACKED/` or `/VALIDATED/` based on results
5. Index updates automatically (or manually if you add files)

---

## 📋 Active Insights (by Confidence Level)

### 🔵 LIVE THEORY (Untested Insights)
*Intuited or channeled; not yet tested. Use as research direction.*

| # | Theory | Origin | Notes |
|---|--------|--------|-------|
| TBD | *To be filled as theories emerge* | — | — |

**Files:** `/LIVE_THEORY/`

---

### 🟡 NEEDS_TESTING (Test Plan Ready)
*Theory clear; test plan designed; test not yet run (or awaiting review).*

| # | Theory | Result | Status |
|---|--------|--------|--------|
| (none currently) | — | — | — |

**Files:** `/NEEDS_TESTING/`

---

### 🟠 PARTIALLY_BACKED (Mixed Results)
*Some tests pass; results inconclusive or weak; needs more data.*

| # | Theory | Result | Sample Size | Notes |
|---|--------|--------|-------------|-------|
| TBD | *To be filled after testing* | — | — | — |

**Files:** `/PARTIALLY_BACKED/`

---

### 🟢 VALIDATED (Approved for Use)
*Passes all rubber stamp gates; ready for application.*

| # | Theory | Effect | p-value | n (Test) | Confidence |
|---|--------|--------|---------|----------|------------|
| 1 | **Exec × Color × Element/Round** | +0.876 to −0.707 vs_avg (7 combos) | p<0.001 | 40–548 | HIGH (68.8% replication) |

**Files:** `/VALIDATED/exec_color_element_round_signals_20260405.md`

---

### 🟡 ARCHIVED (Shelved Pending Revalidation)
*Interesting patterns but need recent data validation; waiting for circumstances to change.*

| # | Theory | Why Archived | Review Date |
|---|--------|---|---|
| 1 | Master Numbers × Colors | Effect disappeared 2025-2026; was strong 2022-2024 | 2026-05-04 |

**Files:** `/ARCHIVED/master_numbers_colors_20260404_ARCHIVED.md`

---

### 🔴 REJECTED (Failed or Abandoned)
*Failed key tests; contradicts evidence; or abandoned.*

| # | Theory | Failure Reason | Sample Size | Date |
|---|--------|---|---|---|
| (none currently) | — | — | — | — |

**Files:** `/REJECTED/`

---

## 📂 Folder Structure

```
/VALIDATED_INSIGHTS/
├── INDEX.md (this file)
├── HOW_TO_ADD_INSIGHT.md (workflow guide)
├── RUBBER_STAMP_CHECKLIST.md (validation gates template)
│
├── /LIVE_THEORY/
│   ├── README.md
│   └── [theory_name_date].md (individual theories)
│
├── /NEEDS_TESTING/
│   ├── README.md
│   └── [theory_name_date].md (with test plan + script link)
│
├── /PARTIALLY_BACKED/
│   ├── README.md
│   └── [theory_name_date].md (with test results + analysis)
│
├── /VALIDATED/
│   ├── README.md
│   └── [theory_name_date].md (approved; includes rubber stamp checklist)
│
└── /REJECTED/
    ├── README.md
    └── [theory_name_date].md (failure analysis + why rejected)
```

---

## 🔬 Rubber Stamp Standards

For an insight to move to **VALIDATED**, it must pass all gates:

1. **Statistical Significance** — p < threshold (varies by analysis type; typically p < 0.10 for exploratory, p < 0.05 for primary)
2. **Adequate Sample Size** — n ≥ minimum (context-dependent: ≥50 for basic, ≥100 for high-confidence)
3. **Meaningful Effect Size** — Not just statistically significant; effect must be practically meaningful (varies by domain)
4. **Stability Across Contexts** — Holds in multiple conditions (e.g., across years, tournaments, player tiers)
5. **Excludes Luck** — Not explained by random chance; signal is repeatable

See [RUBBER_STAMP_CHECKLIST.md](RUBBER_STAMP_CHECKLIST.md) for detailed gate definitions and how to apply them.

---

## 📖 How to Use This System

**For adding new theories:**
- Read [HOW_TO_ADD_INSIGHT.md](HOW_TO_ADD_INSIGHT.md)
- Write theory in LIVE_THEORY
- Claude helps design test, move to NEEDS_TESTING
- Run test, document results, move to PARTIALLY_BACKED or VALIDATED

**For reading about a theory:**
- Check INDEX above for theory name + confidence level
- Read the `.md` file in that level's folder
- If VALIDATED, file includes rubber stamp checklist (proof it passed gates)
- If PARTIALLY_BACKED or REJECTED, file includes test results + why it didn't reach VALIDATED

**For understanding gates:**
- Read RUBBER_STAMP_CHECKLIST.md
- When submitting theory for validation, fill out this checklist
- Gates are relative (not absolute) — context determines thresholds

---

## 🎓 What Belongs Here

**Do Add:**
- Color rhythm patterns (theory + test results)
- Personal Day / Personal Year signals
- Element × Condition combinations
- Chakra-based player profiles (theory stage)
- Birth color intuitions (when channeled)
- Divination-based predictions (zodiac, moon phase, tithi, etc.)
- Player behavioral patterns (intuited + tested)
- Momentum/wave patterns (theory or tested)

**Don't Add:**
- Random data experiments (no theory backing)
- Failed tests without clear reason
- Contradictions to prior VALIDATED insights (without new evidence)
- Live betting results (goes in SIGNAL_DEPLOYMENT.md instead)

---

## 🔄 Maintenance

**Claude's role:**
- Keep folder structure organized
- Enforce naming conventions (theory_name_date.md)
- Move files between folders as confidence changes
- Update INDEX.md when new insights added/updated
- Maintain README.md in each subfolder
- Flag unclear or incomplete submissions

**User's role:**
- Provide intuitive theories (Live Theory)
- Decide which theories to test next
- Provide domain knowledge for interpreting results
- Review test results and decide on validation
- Reject theories that don't align with lived experience

---

## 📌 Quick Links

- **[How to Add an Insight](HOW_TO_ADD_INSIGHT.md)** — Step-by-step workflow
- **[Rubber Stamp Checklist](RUBBER_STAMP_CHECKLIST.md)** — Validation gates + how to apply
- **[Live Theory](LIVE_THEORY/README.md)** — Active theories waiting for tests
- **[Validated Insights](VALIDATED/README.md)** — Approved insights ready for use

---

**Foundation:** 2026-04-04
**Status:** Ready for first insight submissions
**Next Step:** User contributes first Live Theory → Claude designs test → test runs → results analyzed

