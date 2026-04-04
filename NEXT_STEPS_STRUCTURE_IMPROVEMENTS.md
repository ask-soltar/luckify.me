# NEXT STEPS — Structure Improvements (ACTION CHECKLIST)

**Status:** Ready to implement
**Priority:** High (blocks scaling beyond 100 analyses)
**Timeline:** 4-5 weeks total (Phase 1: 2-3 weeks, Phase 2-3: 2-3 weeks)

---

## PHASE 1: QUICK WINS (2-3 weeks, 4 hours work)

These are low-effort, high-impact. Do these **first** to unblock immediate friction.

### Task 1.1: Create Analysis Charter Template
**Effort:** 30 min
**Impact:** Enforces Phase 1 structure; 5 min saved per analysis × 50 analyses/year = 250 min saved

**Action:**
```bash
1. Create file: .claude/templates/ANALYSIS_CHARTER.md
2. Use template from AUDIT_PROJECT_STRUCTURE_20260404.md (Refinement 1 section)
3. Commit to git with message: "Template: Analysis Charter for Phase 1 framing"
```

**Verify:**
- [ ] File exists at `.claude/templates/ANALYSIS_CHARTER.md`
- [ ] Template has sections: Question, Data & Scope, Success Metric, Train/Test Split
- [ ] Can copy, fill out, commit in <5 min

---

### Task 1.2: Create Analysis Metadata YAML Template
**Effort:** 30 min
**Impact:** Machine-readable metadata enables automation; replicability guaranteed

**Action:**
```bash
1. Create file: .claude/templates/ANALYSIS_METADATA.yaml
2. Use template from AUDIT_PROJECT_STRUCTURE_20260404.md (Refinement 3 section)
3. Include fields: input (source, rows, filters, date_range), output (metrics), dependencies, verdict
4. Commit with message: "Template: Analysis Metadata for Phase 4 storage"
```

**Verify:**
- [ ] File exists at `.claude/templates/ANALYSIS_METADATA.yaml`
- [ ] All fields machine-parseable (YAML syntax correct)
- [ ] Can fill out in <5 min

---

### Task 1.3: Create Signal Deployment Ledger
**Effort:** 20 min
**Impact:** Audit trail for live signals; enables performance monitoring

**Action:**
```bash
1. Create file: /SIGNAL_DEPLOYMENT.md (root of project)
2. Copy structure from AUDIT_PROJECT_STRUCTURE_20260404.md (Refinement 4 section)
3. Add existing 3 signals (Calm×Closing×Purple×Fire, etc.) with:
   - Deployed: 2026-03-28
   - Initial metrics: from FINAL_BETTING_SIGNALS.md
   - Current metrics: mark as "To be tracked"
   - Next review: 2026-04-18 (2 weeks from now)
4. Commit with message: "Add Signal Deployment Ledger"
```

**Verify:**
- [ ] File exists at `/SIGNAL_DEPLOYMENT.md`
- [ ] All 3 live signals listed with deployment date + metrics
- [ ] "Weekly Performance Review" section created with empty rows (to be filled in weekly)
- [ ] Commit includes working reference for `/signal-deploy` skill

---

### Task 1.4: Migrate 3 Recent Analyses to New Folder Structure
**Effort:** 1 hour (do 3 analyses as examples)
**Impact:** Establishes pattern for future analyses; demonstrates new structure

**Action:**
```bash
1. Pick 3 recent analyses from /ANALYSES/ (e.g., 20260404_color_personalday_*, 20260401_element_*, 20260331_k_optimization_*)
2. For each analysis:
   a. Create folder: /ANALYSES/20260404_[topic]/
   b. Create METADATA.yaml (extract data, filters, metrics from existing files)
   c. Create README.md (charter + findings + verdict from existing findings.md)
   d. Move/copy analysis.py (if exists) to folder
   e. Move CSVs to folder
3. Delete old scattered files (or move to /ARCHIVE/)
4. Update /ANALYSES/INDEX.md to reference new folder structure
5. Commit with message: "Migrate 3 analyses to atomic folder structure"
```

**Verify:**
- [ ] 3 folders created: /ANALYSES/YYYYMMDD_[topic]/
- [ ] Each folder has: METADATA.yaml, README.md, data_output.csv
- [ ] Old scattered files moved or deleted
- [ ] INDEX.md updated with new folder links
- [ ] Can grep /ANALYSES/ and find all analysis results in <5 sec

---

### Task 1.5: Add Script Metadata Header Template
**Effort:** 30 min
**Impact:** Enables dependency tracking; clarifies script version + status

**Action:**
```bash
1. Create file: .claude/templates/SCRIPT_METADATA_HEADER.py
2. Include header (copy from AUDIT_PROJECT_STRUCTURE_20260404.md Quick Win #5):
   - title, version, status, last_updated, author
   - depends_on (data, columns)
   - produces (output files + columns)
   - parameters (train_rows, test_rows, filters)
3. Add comment: "Add this header to top of all SCRIPTS/*.py files"
4. Commit with message: "Template: Script Metadata header"
```

**Verify:**
- [ ] Template file exists and is syntactically correct Python
- [ ] All fields documented
- [ ] Example of "active" vs "experimental" vs "deprecated" scripts shown
- [ ] README added to template explaining how to use

---

### Task 1.6: Set Up Maintenance Folder
**Effort:** 15 min
**Impact:** Audit trail for maintenance actions; enables "when was this validated?" queries

**Action:**
```bash
1. Create folder structure:
   - /MAINTENANCE/README.md (explain what goes here)
   - /MAINTENANCE/dependency_log/ (for /dependency-check outputs)
   - /MAINTENANCE/rerun_log/ (for /rerun-analysis outputs)
   - /MAINTENANCE/data_quality/ (for data audits + backups)
2. Write /MAINTENANCE/README.md:
   - "This folder tracks all maintenance actions (dependency checks, re-runs, data audits)"
   - "Purpose: audit trail for debugging signal failures"
   - "Auto-populated by /dependency-check, /rerun-analysis skills"
3. Commit with message: "Add MAINTENANCE folder for audit trail"
```

**Verify:**
- [ ] Folder structure created
- [ ] README.md documents purpose
- [ ] Ready to receive outputs from future skills

---

### Task 1.7: Update CLAUDE.md Work Log
**Effort:** 10 min
**Impact:** Documents that structure is now in place; guides future analysts

**Action:**
```bash
1. Add section to CLAUDE.md work log:

### 2026-04-04 — Project Structure Audit & Quick Wins Phase 1
**Status:** Done
**What changed:**
- Created Analysis Charter template (enforce Phase 1 framing)
- Created Analysis Metadata YAML template (machine-readable output metadata)
- Created Signal Deployment Ledger (audit trail for live signals)
- Migrated 3 recent analyses to atomic folder structure (example pattern)
- Created Script Metadata header template (enable dependency tracking)
- Set up /MAINTENANCE/ folder (audit trail for maintenance actions)

**Why:** Current structure (working, but manual) breaks at 100+ analyses. Templates + folder restructuring enable automation via skills.

**Impact:**
- Phase 4 (Storage) friction reduced from 15 min to 5 min per analysis
- Metadata enables /analyze, /signal-deploy, /rerun-analysis skills
- Signal Deployment Ledger enables weekly performance reviews (detect drift early)

**Next step:** Implement Phase 2 skills (/analyze, /signal-deploy, /rerun-analysis) in 2-3 weeks.

2. Commit with message: "Audit: Phase 1 Quick Wins complete"
```

---

### Task 1.8: Test Phase 1 Setup
**Effort:** 30 min
**Impact:** Verify templates work before building skills

**Action:**
```bash
1. Create dummy analysis following Phase 1 workflow:
   a. Fill out ANALYSIS_CHARTER.md (question, data, metrics)
   b. Create /ANALYSES/YYYYMMDD_test_dummy/ folder
   c. Create METADATA.yaml with dummy data
   d. Create README.md with charter + findings
   e. Commit with message: "Test: Phase 1 workflow end-to-end"
2. Check: Can you go from charter → folder → metadata → git commit in <15 min?
3. If yes: Phase 1 complete. If no: iterate on templates.
4. Delete dummy analysis (or keep as template example)
```

---

### PHASE 1 COMPLETION CHECKLIST
- [ ] Task 1.1: Analysis Charter template created + committed
- [ ] Task 1.2: Analysis Metadata YAML template created + committed
- [ ] Task 1.3: Signal Deployment Ledger created + committed
- [ ] Task 1.4: 3 recent analyses migrated to new structure + committed
- [ ] Task 1.5: Script Metadata header template created + committed
- [ ] Task 1.6: /MAINTENANCE/ folder structure created + committed
- [ ] Task 1.7: CLAUDE.md work log updated + committed
- [ ] Task 1.8: End-to-end test successful

**Estimated completion:** 2-3 weeks
**Time to complete:** ~4 hours total implementation + testing

---

---

## PHASE 2: SKILL IMPLEMENTATION (2-3 weeks, ~10 hours work)

**Prerequisites:** Phase 1 complete

These skills automate repetitive work + enforce process. Builds on templates from Phase 1.

### Skill 2.1: `/analyze` (Priority 1 — use for every new analysis)
**What it does:** Interactive wizard to create new analysis with charter, folder, metadata

**How to implement:**
1. Create skill that:
   - Prompts user for: Question? Data source? Filters? Success metric?
   - Auto-creates: /ANALYSES/YYYYMMDD_[topic]/ folder
   - Auto-creates: METADATA.yaml (empty, to be filled)
   - Auto-creates: README.md (charter template, to be filled)
   - Auto-creates: analysis.py (copy of combo_analysis_4d_element.py as template)
   - Auto-updates: MEMORY.md (add entry under PROJECT section)
   - Auto-commits: git commit -m "Analysis charter: [topic]"
   - Returns: "Folder created at [path]. Next: edit analysis.py, run, commit results."

2. Design prompts to mirror Phase 1 Charter template

3. Test: Run `/analyze color_element_testing`, verify folder created, files generated, committed

---

### Skill 2.2: `/signal-deploy` (Priority 1 — guards production bets)
**What it does:** Validates signal metrics, adds to deployment ledger, sets reminder

**How to implement:**
1. Create skill that:
   - Prompts user for: Signal name? Metrics CSV file path?
   - Validates: WR >50%, variance <15%, samples >300 (configurable)
   - Validates: Signal not already deployed (check SIGNAL_DEPLOYMENT.md)
   - Updates: SIGNAL_DEPLOYMENT.md with new entry (Status=LIVE, dates, metrics)
   - Tests: Signal logic in matchup_screener_v3.py (smoke test)
   - Auto-commits: git commit -m "Deploy signal: [name], WR [X]%, edge [Y]%"
   - Sets reminder: "Re-validate [signal] in 14 days"
   - Returns: Ledger entry + reminder scheduled

2. Build validation checklist (see AUDIT_PROJECT_STRUCTURE_20260404.md)

3. Test: Try to deploy signal with WR=48% (should reject), then WR=54% (should accept)

---

### Skill 2.3: `/rerun-analysis` (Priority 2 — maintenance + validation)
**What it does:** Re-runs analysis with current data, compares to old results, flags drift

**How to implement:**
1. Create skill that:
   - Takes analysis topic name (e.g., "color_personalday")
   - Finds analysis folder: /ANALYSES/*color_personalday*/
   - Loads: METADATA.yaml (input data, filters, success metric)
   - Finds: analysis.py in folder
   - Runs: script with current data + same filters
   - Compares: old metrics (from METADATA.yaml) vs new metrics
   - Flags: if WR changed >5%, variance >2x, top combos reordered
   - Updates: METADATA.yaml (new results, last_tested date)
   - Logs: /MAINTENANCE/rerun_log/YYYYMMDD_[topic]_rerun.txt
   - Auto-commits: git commit -m "Re-run analysis: [topic]. WR [old]% → [new]%. Status: [stable|drifted]"
   - Returns: "Analysis re-run complete. [X] combos changed. Results [stable|drifted]. See [path]."

2. Build drift detection logic (>5% WR change = flag)

3. Test: Run on Color × Personal Day analysis, verify drift detection works

---

### Skill 2.4: `/dependency-check` (Priority 2 — prevents silent breakage)
**What it does:** Finds all scripts that use a given column/table, flags if change breaks them

**How to implement:**
1. Create skill that:
   - Takes change description (e.g., "Column AC (off_par) renamed to AC2")
   - Scans: all SCRIPTS/*.py + ANALYSES/*/*.py files
   - Parses: import statements, column references, hardcoded column indices
   - Builds: dependency graph (script → columns/tables)
   - Searches: "which scripts reference column AC?"
   - Returns: list of impacted scripts (e.g., "12 scripts found")
   - Prompts: "Mark these for re-run? (y/n)"
   - Logs: /MAINTENANCE/dependency_log/YYYYMMDD_[change]_check.txt (audit trail)
   - Auto-commits: git commit -m "Dependency check: [change]. 12 scripts flagged."

2. Build dependency parser (regex for column refs, import statements)

3. Test: Change column reference, run /dependency-check, verify scripts flagged

---

### Skill 2.5: `/memory-search` (Priority 3 — convenience)
**What it does:** Full-text search across MEMORY.md files, return ranked results

**How to implement:**
1. Create skill that:
   - Takes search query (e.g., "Color signal")
   - Searches: all memory/*.md files
   - Ranks: by relevance (file type matches query category?)
   - Returns: top 5 results with context (file, line, snippet)
   - Provides: clickable path to each result

2. Build search index (may cache for speed)

3. Test: Search for "Color", "element", "deployment", verify results returned

---

### Skill Implementation Sequence
1. **Week 1:** Build `/analyze` skill (2 hours)
2. **Week 1-2:** Build `/signal-deploy` skill (2.5 hours)
3. **Week 2:** Build `/rerun-analysis` skill (2 hours)
4. **Week 2-3:** Build `/dependency-check` skill (3 hours) — most complex
5. **Week 3:** Build `/memory-search` skill (45 min)
6. **Week 3:** Integration testing all skills together (1 hour)

---

---

## PHASE 3: SYSTEM HARDENING (1-2 weeks, ~5 hours work)

**Prerequisites:** Phase 1 + Phase 2 complete

### Task 3.1: Git Hooks for Auto-Commit
**Effort:** 1 hour
**Impact:** MEMORY.md, SIGNAL_DEPLOYMENT.md, analysis outputs auto-committed; audit trail guaranteed

**Action:**
```bash
1. Create .git/hooks/post-merge (auto-commit analysis outputs)
2. Create .git/hooks/post-commit (auto-update ANALYSES/INDEX.md)
3. Enable: git config core.hooksPath .git/hooks
4. Test: modify analysis, verify auto-commit happens
```

---

### Task 3.2: Auto-Regenerate ANALYSES/INDEX.md
**Effort:** 1 hour
**Impact:** INDEX.md never stales; always reflects current analyses

**Action:**
```bash
1. Create script: scripts/regenerate_analyses_index.py
2. Logic:
   a. Scan /ANALYSES/ folder
   b. For each YYYYMMDD_[topic]/ folder:
      - Read METADATA.yaml (extract status, key_insight, verdict)
      - List files in folder
      - Generate INDEX entry
   c. Sort by date (newest first)
   d. Write to ANALYSES/INDEX.md
3. Trigger: git hook post-commit or cron daily
4. Test: add new analysis, run script, verify INDEX.md updated
```

---

### Task 3.3: Auto-Regenerate SCRIPTS/_CATALOG.yaml
**Effort:** 1.5 hours
**Impact:** Know status of all 168 scripts; enable "find scripts by status/category" queries

**Action:**
```bash
1. Add metadata header to ~20 "high-value" scripts (30 min)
   - combo_analysis_4d_element.py (status: active, version: 1.0)
   - analyze_color_personalday_by_condition.py (status: experimental, version: 2.1)
   - matchup_screener_v3.py (status: active, version: 3.2)
   - etc. (focus on scripts mentioned in SCRIPTS/INDEX.md)

2. Create script: scripts/regenerate_scripts_catalog.py
3. Logic:
   a. Scan SCRIPTS/*.py
   b. For each file, parse YAML header (if exists)
   c. Extract: title, status, version, category, depends_on, produces, last_tested
   d. Generate catalog entry
   e. Write to SCRIPTS/_CATALOG.yaml
   f. For files without header: mark as "undocumented"
4. Trigger: cron daily
5. Test: modify one script header, run script, verify _CATALOG.yaml updated
```

---

### Task 3.4: Runbook — "If Golf_Analytics Columns Change"
**Effort:** 30 min
**Impact:** Clear process for handling data schema changes; prevents silent breakage

**Action:**
```bash
1. Create file: /MAINTENANCE/RUNBOOK_SCHEMA_CHANGE.md
2. Content:
   - "If columns are added/removed/renamed in Golf_Analytics or ANALYSIS sheet:"
   - Step 1: Run `/dependency-check "Column X renamed to Y"`
   - Step 2: Review flagged scripts + analyses
   - Step 3: For each flagged item: run `/rerun-analysis [topic]` to re-validate
   - Step 4: If results diverge, investigate data mapping + fix scripts
   - Step 5: Document change in /MAINTENANCE/dependency_log/ (auto-done by /dependency-check)
   - Step 6: Commit all fixes + re-run logs with message "Schema change: [columns]. 10 scripts re-validated."
3. Commit with message: "Runbook: Schema change handling"
```

---

### Task 3.5: Weekly Signal Performance Review Cadence
**Effort:** 15 min (setup) + 15 min/week (ongoing)
**Impact:** Early detection of signal drift; prevents live betting on bad signals

**Action:**
```bash
1. Add calendar reminder: Every Friday 9am "Update SIGNAL_DEPLOYMENT.md"
2. Weekly task:
   a. Open /SIGNAL_DEPLOYMENT.md
   b. For each LIVE signal:
      - Grab current WR from live betting data (screener output, or manual count)
      - Update "Current metrics" column
      - Check if WR drift >5% (if yes, flag: "NEEDS RE-ANALYSIS")
   c. Commit with message: "Weekly signal review: [date]"
3. Commit with message: "Add weekly signal performance review task"
```

---

### PHASE 3 COMPLETION CHECKLIST
- [ ] Task 3.1: Git hooks created + tested
- [ ] Task 3.2: ANALYSES/INDEX.md auto-regeneration script working
- [ ] Task 3.3: Script metadata headers added to ~20 scripts + _CATALOG.yaml auto-regeneration working
- [ ] Task 3.4: Schema change runbook created + documented
- [ ] Task 3.5: Weekly signal review task scheduled + first review done

**Estimated completion:** 1-2 weeks
**Time to complete:** ~5 hours total

---

---

## PHASE 4: DOCUMENTATION & ONBOARDING (1 week, ~3 hours)

**Prerequisites:** Phase 1-3 complete

### Task 4.1: Update CLAUDE.md with New Workflow
**Effort:** 1 hour
**Impact:** New analysts read updated workflow; know about templates + skills

**Action:**
```bash
1. Update "Data Workflow (The Full Loop)" diagram in CLAUDE.md:
   - Add "/" skill references (e.g., "/analyze → automatic folder creation")
   - Add METADATA.yaml step
   - Add Signal Deployment Ledger step
2. Update "Conventions" section to reference new templates
3. Add new section: "Structure Improvements (Phase 1-4 complete)"
   - Document templates + skills + changes
4. Update "Flagged for Later" section (remove structure items, add new items)
5. Commit with message: "Docs: Update CLAUDE.md with Phase 1-4 improvements"
```

---

### Task 4.2: Create Quickstart Guide — "Run Your First Analysis"
**Effort:** 1 hour
**Impact:** New analyst can run complete analysis in 1 hour (not 1 day)

**Action:**
```bash
1. Create file: /QUICKSTART_ANALYSIS.md
2. Content:
   - "5-step guide to running your first analysis using new structure"
   - Step 1: Use `/analyze` skill to create charter + folder
   - Step 2: Edit analysis.py (copy lines 20-50 from example script)
   - Step 3: Run: python ANALYSES/YYYYMMDD_[topic]/analysis.py
   - Step 4: Save results to ANALYSES/YYYYMMDD_[topic]/data_output.csv
   - Step 5: Fill out METADATA.yaml with results, run git commit
   - Estimated time: 1 hour
   - Example: walk-through of Color × Element analysis
3. Commit with message: "Docs: Quickstart guide for new analyses"
```

---

### Task 4.3: Troubleshooting Guide
**Effort:** 45 min
**Impact:** When things go wrong (script fails, skill errors), analyst can self-serve

**Action:**
```bash
1. Create file: /TROUBLESHOOTING.md
2. Content:
   Q: "Script failed: 'NameError: column X not found'"
   A: "Column names may have changed. Check GOLF_ANALYTICS_DATA_DICTIONARY.md line Y. Run `/dependency-check` to identify changes."

   Q: "METADATA.yaml format error"
   A: "Copy from .claude/templates/ANALYSIS_METADATA.yaml. Common mistakes: missing colons, wrong indentation."

   Q: "/analyze skill not found"
   A: "Ensure Phase 2 skills are installed. Check /dev/null for errors. Contact [owner]."

   Q: "Results changed after re-run. Which is correct?"
   A: "New data = new results. Check /MAINTENANCE/rerun_log/ for what changed. If unexpected, investigate data + re-run filters."

   ... (add 10+ common issues)
3. Commit with message: "Docs: Troubleshooting guide"
```

---

### PHASE 4 COMPLETION CHECKLIST
- [ ] Task 4.1: CLAUDE.md updated + committed
- [ ] Task 4.2: Quickstart guide created + tested
- [ ] Task 4.3: Troubleshooting guide created + committed

**Estimated completion:** 1 week
**Time to complete:** ~3 hours

---

---

## FULL PROJECT TIMELINE

| Phase | Tasks | Effort | Duration | Start | End |
|-------|-------|--------|----------|-------|-----|
| 1 | Quick Wins (templates, ledger, folder migration) | 4 hrs | 2-3 wks | 2026-04-05 | 2026-04-18 |
| 2 | Skills (/analyze, /signal-deploy, /rerun-analysis, /dependency-check, /memory-search) | 10 hrs | 2-3 wks | 2026-04-19 | 2026-05-02 |
| 3 | Hardening (git hooks, auto-regen, runbooks) | 5 hrs | 1-2 wks | 2026-05-03 | 2026-05-09 |
| 4 | Onboarding (docs, tutorials, troubleshooting) | 3 hrs | 1 wk | 2026-05-10 | 2026-05-16 |
| **Total** | **All phases** | **~22 hrs** | **6-9 weeks** | **2026-04-05** | **2026-05-16** |

---

## ESTIMATED VALUE (Annual Savings + Risk Mitigation)

| Metric | Current | With Structure | Savings |
|--------|---------|----------------|---------|
| Time per analysis (Phase 4) | 15 min | 5 min | 10 min × 50/yr = 500 min |
| Time to find past analysis | 10 min | 1 min | 9 min × 10/yr = 90 min |
| Duplicate work incidents | 20%/yr | 0% | 10 analyses × 2 hrs = 20 hrs |
| Signal drift undetected | 30+ days | <7 days | Risk mitigation (priceless) |
| Broken script detection | Manual | Automatic | 2+ hrs/incident × 5 = 10 hrs |
| **Total annual savings** | — | — | **40+ hours + critical risk mitigation** |

---

## SIGN-OFF CHECKLIST

- [ ] Read AUDIT_PROJECT_STRUCTURE_20260404.md (full analysis)
- [ ] Read NEXT_STEPS_STRUCTURE_IMPROVEMENTS.md (this file)
- [ ] Understand Phase 1 requirements (4 hours, 2-3 weeks)
- [ ] Decide: Start Phase 1 now? (Yes / No / When?)
- [ ] If yes: Create git issue or calendar block for Phase 1 start date
- [ ] If yes: Assign owner (self? team member?)

---

**Questions?** Reference sections in AUDIT_PROJECT_STRUCTURE_20260404.md:
- Why do we need this? → See "SCALABILITY ISSUES"
- How urgent? → See "FINDING 1-5"
- What's the ROI? → See "ESTIMATED VALUE"
- Can I skip steps? → See "PHASE 1 CRITICAL ITEMS"

