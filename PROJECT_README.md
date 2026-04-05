# Luckify Me — Golf Betting Analytics System

**Master index for the entire project.** Start here if you're lost.

---

## 🎯 Quick Navigation

### **Active Signals (Ready to Deploy)**
→ See `FINAL_BETTING_SIGNALS.md`

**Current validated signals:**
- Calm × Closing × Purple × Fire: **+4.6%** edge
- Calm × Closing × Green × Earth: **+5.9%** edge (best stability)
- Moderate × Closing × Blue × Water: **+5.5%** edge

---

### **Project Documentation**
- **`CLAUDE.md`** — Master project reference (architecture, sheets, engine, work log)
- **`GOLF_ANALYTICS_DATA_DICTIONARY.md`** — All 70+ column definitions
- **`AUDIT_FRAMEWORK.md`** — 5-layer verification system
- **`DATA_INTAKE_CHECKLIST.md`** — How to import new tournament data

---

### **Latest Analysis Work**
→ See `/ANALYSES/` folder

**Most recent (2026-04-04):**
- `20260404_color_personalday_*.md` — Color × Personal Day signal testing (FAILED out-of-sample)
- `20260404_backtest_summary.txt` — Backtest results
- `20260404_consistency_insight_expanded.md` — Why consistency matters more than raw edge
- `20260404_INDEX_color_personalday.md` — Full analysis index

---

### **Memory System (Decisions & Guidance)**
→ See `.claude/projects/.../memory/MEMORY.md`

Contains all:
- Prior analysis results (what we tested, what worked)
- Your working preferences (how you like structure)
- Betting signals (validated edges)
- Analysis methodology (how to structure work)

---

## 📁 Folder Structure

```
/d/Projects/luckify-me/
├── README.md (you are here)
├── CLAUDE.md (project master reference)
├── FINAL_BETTING_SIGNALS.md (live signals)
├── CONSISTENCY_INSIGHT_EXPANDED.md (key finding from latest analysis)
│
├── /engine/ (Google Apps Script code)
│   └── 00_config.gs, 01_menu.gs, 10_engine_lucky_day.gs, etc.
│
├── /ANALYSES/ (timestamped analysis outputs)
│   ├── 20260404_color_personalday_findings.md
│   ├── 20260404_backtest_summary.txt
│   ├── 20260404_color_personalday_combos.csv
│   └── INDEX.md (full index of all analyses)
│
├── /SCRIPTS/ (reusable Python analysis scripts)
│   ├── matchup_screener_v3.py (main betting screener)
│   ├── analyze_color_personalday_thresholds.py
│   ├── combo_analysis_4d_element.py
│   └── [165+ analysis scripts]
│
├── /DATA/ (reference data files)
│   ├── Golf Historics v3 - ANALYSIS (7).csv (main analysis sheet)
│   ├── ANALYSIS_v3_export.csv
│   ├── [120+ data exports]
│   └── REFERENCE.md (what each CSV contains)
│
├── /ARCHIVE/ (old/superseded analyses)
│   └── [older work, kept for reference]
│
└── /.claude/ (Claude-specific config)
    └── projects/.../memory/ (persistent memory system)
```

---

## 🔄 Workflow

**When you have a question or want to analyze something:**

1. **Check memory first** (`.claude/memory/MEMORY.md`)
   - Is it already analyzed?
   - What guidance exists?
   - What filters do you normally use?

2. **Read workflow guidance** (`.claude/memory/workflow_daily_analysis_structure.md`)
   - Follow 4-phase process: Setup → Analysis → Interpretation → Storage
   - Write charter before diving in
   - Write key insight after analyzing

3. **Run analysis** using:
   - Python scripts from `/SCRIPTS/`
   - Data from `/DATA/`
   - Standard filters from memory

4. **Store results** in `/ANALYSES/20260405_[topic]_*` with:
   - Timestamp in filename
   - INDEX.md with links
   - Update `.claude/memory/MEMORY.md` with pointer

---

## 📊 How to Use Each Folder

### `/SCRIPTS/`
**What:** Reusable Python analysis scripts

**Use when:** Need to analyze data, backtest signals, test hypotheses

**Example:**
```bash
python SCRIPTS/combo_analysis_4d_element.py
python SCRIPTS/matchup_screener_v3.py
```

**Contains:** 168 analysis scripts (not all active, many experimental)

---

### `/DATA/`
**What:** Reference data files (golf round data, analysis exports, etc.)

**Main file:** `Golf Historics v3 - ANALYSIS (7).csv` (61k+ rounds, 2022-2026)

**Use when:** Need raw data for analysis, reference lookups

---

### `/ANALYSES/`
**What:** Timestamped analysis outputs (results, findings, reports)

**Structure:** `YYYYMMDD_[topic]_[type].*`
- `20260404_color_personalday_findings.md` (report)
- `20260404_color_personalday_combos.csv` (data)
- `20260404_index_color_personalday.md` (index)

**Use when:** Looking up past analysis results, understanding what's been tested

---

## 🎓 Key Concepts

### **Standard Filters** (always apply these)
- **Condition:** Calm, Moderate, Tough
- **Round Type:** Open, Positioning, Closing, Survival
- **Tournament Type:** S, NS (stroke play only)
- Result: 62k+ records (79.5% of all golf data)

### **Metric Definition**
- **vs_avg** = `score - course_avg` (field-relative performance, not par-relative)
- **Negative** = beats field average (GOOD)
- **Positive** = underperforms field average (BAD)

### **Signal Validation**
1. Test on 2022-2024 training data
2. Validate on 2025-2026 out-of-sample data
3. Check variance/stability (>10% variance = unreliable)
4. Calculate Kelly sizing

---

## ⚠️ Current Status

**Active validated signals:** 3 (from 4D Element analysis)
- Deployment ready ✓
- Out-of-sample validated ✓

**Color × Personal Day signals:** Tested 2026-04-04
- Result: Failed out-of-sample (-5.2% edge)
- Status: Archived, reference only

**Next priority:** Expand 4D Element signals + test new divination dimensions

---

## 📞 How to Find Something

**"Where is X?"**

| Question | Answer |
|----------|--------|
| Validated betting signals | → `FINAL_BETTING_SIGNALS.md` |
| Column definitions | → `GOLF_ANALYTICS_DATA_DICTIONARY.md` |
| How to structure analysis | → `.claude/memory/reference_memory_navigation_guide.md` |
| Past analyses & results | → `/ANALYSES/` or `.claude/memory/MEMORY.md` |
| Raw golf data | → `/DATA/Golf Historics v3 - ANALYSIS (7).csv` |
| Analysis scripts | → `/SCRIPTS/` |
| Google Apps Script code | → `/engine/` |
| Old/archived work | → `/ARCHIVE/` |

---

## 🚀 Getting Started

**First time? Do this:**

1. Read `CLAUDE.md` (project architecture, sheets, engine)
2. Read `.claude/memory/MEMORY.md` (what's been analyzed, what works)
3. Read `.claude/memory/reference_memory_navigation_guide.md` (how to find things)
4. Read `.claude/memory/workflow_daily_analysis_structure.md` (how to run analysis)
5. Check `/ANALYSES/` for latest findings

**Have a hypothesis to test?**

1. Write 3-sentence charter (what, why, how)
2. Run analysis from `/SCRIPTS/` using `/DATA/`
3. Store results in `/ANALYSES/20260405_[topic]_*.csv|.md`
4. Update `.claude/memory/MEMORY.md`
5. Reference in CLAUDE.md work log

---

## 📝 Work Log

→ See `CLAUDE.md` for detailed work log (most recent entries at bottom)

**Latest milestone (2026-04-04):**
- Tested Color × Personal Day signals
- Result: Failed out-of-sample, high variance
- Learning: Consistency (low variance) > raw edge for Kelly sizing
- Next: Focus on validated 4D Element signals

---

**Questions? Check `CLAUDE.md` or `.claude/memory/MEMORY.md` first. Answers are there.**
