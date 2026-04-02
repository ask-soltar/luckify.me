# Birthday Verification — ESPN Lookup

## Files Updated/Created

- **00_config.gs** (updated) — Added BIRTHDAY_VERIFY sheet constants
- **07c_fetcher_espn_players.gs** (new) — ESPN API layer
- **09_writer_birthday_verify.gs** (new) — Birthday verification workflow

## How to Use

### Step 1: Copy files to Apps Script

Paste these three updated files into your Apps Script editor:
1. `00_config.gs`
2. `07c_fetcher_espn_players.gs`
3. `09_writer_birthday_verify.gs`

Then run:
```
clasp push
```

### Step 2: Run the fetcher

In Apps Script console:
```
FETCH_BIRTHDAYS_FROM_ESPN()
```

This will:
- Read all PLAYERS rows where `human_check` (col F) is FALSE/empty
- Search ESPN for each player
- Fetch their profile and extract birthday
- Write results to a new `BIRTHDAY_VERIFY` sheet
- Create the sheet automatically if needed

Output: `✓ Wrote X verification rows`

**Progress tracking:** Script handles 6-min timeout. If it times out, just run again — it resumes where it left off.

### Step 3: Review BIRTHDAY_VERIFY sheet

Columns:
| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| player_id | name | current_birthday | espn_birthday | status | espn_id | action | notes |

**Status values:**
- `MATCH` — ESPN matches your current data ✓ (probably fine)
- `CONFLICT` — ESPN differs from current data (review both, decide)
- `NEW` — You don't have a birthday, ESPN found one (check ESPN is correct)
- `NOT_FOUND` — ESPN couldn't find this player (manual lookup needed)

**In column G (action), fill in:**
- `UPDATE` — Use ESPN's birthday
- `KEEP` — Keep your current birthday
- `SKIP` — Don't touch this player
- (leave blank for rows you haven't reviewed yet)

### Step 4: Apply updates

Once you've reviewed and marked action = `UPDATE` for the birthdays you want to import, run:
```
APPLY_VERIFIED_BIRTHDAYS()
```

This will:
- Find all rows where action = `UPDATE`
- Update those birthdays in PLAYERS sheet
- Leave your current data alone for KEEP/SKIP rows

Output: `✓ Updated X birthdays in PLAYERS sheet`

### Step 5: Manual verification checkbox

Once you're confident a birthday is correct:
1. Go to PLAYERS sheet
2. Find the player row
3. Click the checkbox in column F (`human_check`)

**Note:** The script does NOT auto-check this box — you verify manually. This ensures you've actually reviewed each one.

---

## Limitations

- **Name matching:** ESPN search is name-based. Common names may return wrong player. Always review CONFLICT rows carefully.
- **Coverage:** ESPN won't have data for all players, especially non-PGA golfers (~20-30% estimated NOT_FOUND)
- **Privacy:** Some players may not have birthday data publicly available
- **Rate limiting:** Script respects ESPN's rate limits (100ms between requests). Large batches (~1600) will take ~30 min to complete.

---

## Example Workflow

1. **MATCH rows** → Check the birthdates match what you expect → Click human_check in PLAYERS
2. **CONFLICT rows** → Compare ESPN vs your current data. If ESPN is more recent, mark `UPDATE`. Otherwise mark `KEEP`.
3. **NEW rows** → Research the player to confirm ESPN's date is correct. If yes, mark `UPDATE`. If no confidence, leave blank.
4. **NOT_FOUND rows** → Manual lookup (Wikipedia, PGA Tour site, etc.)
5. Run `APPLY_VERIFIED_BIRTHDAYS()` to push `UPDATE` rows
6. Go to PLAYERS and click human_check for all reviewed rows

---

## If something goes wrong

**Script timed out:** Just run `FETCH_BIRTHDAYS_FROM_ESPN()` again. It picks up where it left off.

**Wrong ESPN ID fetched:** Delete the row from BIRTHDAY_VERIFY and mark it SKIP. Manually look up that player.

**Too many NOT_FOUND:** ESPN may have incomplete golf data. Consider supplementing with other sources for non-PGA players.
