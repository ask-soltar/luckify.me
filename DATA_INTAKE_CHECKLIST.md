# Data Intake Checklist

**Purpose:** Flag new raw golf data for import into Golf_Analytics sheet.
Every dataset that enters the system must be logged here and pass through a structured intake process.

---

## Import Status Codes

- 🔴 **FLAGGED** — New raw data detected, awaiting intake review
- 🟡 **IN_REVIEW** — Human is validating + mapping columns
- 🟢 **READY** — Validated, ready to paste into Golf_Analytics
- ✅ **IMPORTED** — Pasted into Golf_Analytics, spot-checked
- 🔒 **LOCKED** — Imported + audit passed; no further changes without re-audit

---

## Intake Checklist Template

When new raw data arrives, copy this template below and fill it out:

```
### [Date] — [Tournament Name] [Year]

**Status:** 🔴 FLAGGED

**Source:** [Where data came from — website, email, spreadsheet link, etc.]
**Format:** [CSV / Spreadsheet / Pasted table / API response / Other]
**Rows:** [Number of player-result rows]
**Date Range:** [Start date → End date of tournament]

#### Human Validation (fill as you go)
- [ ] Check for duplicates (cross-reference Dedupe_Key if exists)
- [ ] Verify player names match PLAYERS sheet exactly (case-sensitive)
- [ ] Verify event name matches EVENTS sheet (match key)
- [ ] Confirm all 4 rounds present (or mark withdrawn if applicable)
- [ ] Check scores are numeric, total matches R1+R2+R3+R4
- [ ] Verify GMT offsets for both player + venue match expected timezone
- [ ] Cross-check a sample of 3 scores against original source

#### Mapping (describe column alignment)
- Source Col A → Golf_Analytics Col ___
- Source Col B → Golf_Analytics Col ___
- [... etc ...]

#### Notes
[Any anomalies, missing data, source issues, decisions made]

**Approved by:** [Name/AI]
**Date approved:** [YYYY-MM-DD]
**Status transition:** FLAGGED → IN_REVIEW → READY → IMPORTED → LOCKED
```

---

## Examples

### Example 1: The Sentry 2023 (FLAGGED → IMPORTED)

```
### 2023-01-08 — The Sentry 2023

**Status:** ✅ IMPORTED

**Source:** PGA Tour website (espn.com golf scores)
**Format:** Manual copy-paste from 4 round leaderboards
**Rows:** 156 players
**Date Range:** 2023-01-05 → 2023-01-08

#### Human Validation
- [x] No duplicates; all player-result IDs unique
- [x] All 156 names match PLAYERS sheet
- [x] Event name = "The Sentry" matches EVENTS sheet row 1
- [x] All players have 4 rounds OR marked Withdrawn correctly
- [x] Spot-checked 5 scores (Schauffele R1=70, Ramey total=-2): ✓
- [x] GMT offsets: Hawaii -10 ✓, Player birthdays GMT stored ✓
- [x] Source totals match: 71+76+72+71 = 290 = -2 at par 72 × 4 ✓

#### Mapping
- Source R1 Score → Golf_Analytics D
- Source R2 Score → Golf_Analytics E
- ... (standard PGA format)

#### Notes
One player (withdrew after R2) — R3 + R4 marked empty, Status = "Withdrawn"

**Approved by:** Claude (human review: ✓)
**Date approved:** 2023-01-08
**Status transition:** FLAGGED → IN_REVIEW → READY → IMPORTED → LOCKED
```

---

## Automation Opportunity

**Future state (not yet built):**
- Webhook / API watch for new tournament results
- Auto-detect new tournaments in EVENTS sheet
- Trigger email alert or Slack message: "New data ready for intake"
- Auto-populate template above with source metadata
- Generate pre-filled mapping based on field names
- Flag deviations (missing rows, name mismatches) for human review

---

## Rules

1. **Never import directly.** Always fill checklist first.
2. **No partial imports.** A tournament is "READY" only when ALL rows are validated.
3. **Duplicates are fatal.** Any duplicate player-event-year is rejected until resolved.
4. **Names must match exactly.** PLAYERS sheet is source of truth for player name spelling.
5. **Withdrawn players stay.** Mark Status="Withdrawn", keep their rows, leave R3+R4 blank.
6. **One approval per import.** Checklist must be signed off before paste.
7. **Audit follows.** After IMPORTED status, data is spot-checked per AUDIT_FRAMEWORK.md.

---

## Current Data Imports (Running Log)

| Tournament | Year | Status | Rows | Intake Date | Audit Date | Notes |
|-----------|------|--------|------|-------------|-----------|-------|
| The Sentry | 2023 | 🔒 LOCKED | 156 | 2023-01-08 | 2023-01-09 | ✓ Spot-checked 5 scores |
| (next tournament) | | 🔴 FLAGGED | | | | |

---

## See Also

- [AUDIT_FRAMEWORK.md](AUDIT_FRAMEWORK.md) — QA process after import
- [CLAUDE.md](CLAUDE.md) — Main project reference; links here
