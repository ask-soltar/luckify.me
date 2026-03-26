# Phase 4 Implementation — Code Ready to Deploy

## What's Done (Code)

✅ **00_config.gs** — Updated with all column constants
- PLAYERS sheet mapping (A:P)
- EVENTS sheet mapping (A:AT)
- RESULTS_RAW sheet layout (A:K, ready for new sheet creation)
- GA (Golf_Analytics) mapping updated

✅ **99_helpers_id_gen.gs** — New file with ID generators
- `GENERATE_PLAYER_IDS()` — fills player_id column (A) in Birthdays sheet
- `GENERATE_EVENT_IDS()` — fills event_id column (A) in Event_Data sheet
- Run once each, then can be deleted

✅ **05_lookup_players.gs** — Fully implemented
- `getPlayerById(player_id)` — look up by PLY_XXXX
- `getPlayerByName(name)` — look up by player name
- `getAllPlayers()` — get all players
- In-memory cache to avoid repeated sheet reads

✅ **06_lookup_events.gs** — Fully implemented
- `getEventById(event_id)` — look up by EVT_XXXX
- `getEventByName(name)` — look up by event title
- `getAllEvents()` — get all events
- In-memory cache + conditions columns included

---

## What You Need to Do (Sheets)

### Step 1: Add Column Headers
**Birthdays sheet:**
- Cell A1: type `Player_ID`

**Event_Data sheet:**
- Cell A1: type `Event_ID`

### Step 2: Generate IDs (Run in Apps Script Console)
1. Copy the three updated files into Apps Script editor:
   - 00_config.gs (updated)
   - 99_helpers_id_gen.gs (new)
   - 05_lookup_players.gs (updated)
   - 06_lookup_events.gs (updated)

2. In Apps Script console, run:
   ```
   GENERATE_PLAYER_IDS()
   ```
   Wait for completion. Should see: `"Player IDs generated. Counter: X"`

3. Then run:
   ```
   GENERATE_EVENT_IDS()
   ```
   Wait for completion. Should see: `"Event IDs generated. Counter: X"`

### Step 3: Create RESULTS_RAW Sheet
Create a new sheet named `RESULTS_RAW` with these headers in row 1:

| A | B | C | D | E | F | G | H | I | J | K |
|---|---|---|---|---|---|---|---|---|---|---|
| result_id | player_id | event_id | r1_score | r2_score | r3_score | r4_score | total | status | notes | created_at |

Example data row:
```
RES_0001 | PLY_0001 | EVT_0001 | 68 | 71 | 69 | 70 | 278 | COMPLETED | | 2025-01-15
```

### Step 4 (Optional): Migrate Golf Score Data
If you have actual round scores in Golf_Analytics columns D:G (R1:R4), optionally move them to RESULTS_RAW:
- Get player_id from Golf_Analytics row
- Get event_id from Golf_Analytics row
- Create a new row in RESULTS_RAW with those scores

Or you can populate RESULTS_RAW manually over time as you add results.

---

## Implementation Order

1. ✅ Code is ready — copy to Apps Script
2. Add column headers (A1) to Birthdays and Event_Data
3. Run GENERATE_PLAYER_IDS() in console
4. Run GENERATE_EVENT_IDS() in console
5. Create RESULTS_RAW sheet with headers
6. (Optional) Migrate existing golf scores to RESULTS_RAW

---

## No Breaking Changes

The code changes are **purely additive**. Existing Golf_Analytics scoring logic works unchanged:
- Columns K:Q (inputs) stay in the same positions
- Columns R:AH (outputs) stay in the same positions
- Conditions are already at AH:AK in Event_Data
- All you're doing is adding new columns (A) and a new sheet (RESULTS_RAW)

---

## Next Steps After IDs Are Generated

Once IDs are in place, the lookup functions work. Golf_Analytics can then reference them via:
```
=getPlayerById(A2)  // returns player object for player_id in A2
=getEventById(B2)   // returns event object for event_id in B2
```

But that's Phase 4b — for now, just get the IDs in place and RESULTS_RAW created.
