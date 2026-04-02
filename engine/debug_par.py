#!/usr/bin/env python3
"""Debug par lookup — prints first 10 combos with full lookup details."""

import os
import gspread
from google.oauth2.service_account import Credentials

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_FILE = os.path.join(BASE_DIR, "luckifyme-f6c83489cd24.json")
SHEET_ID   = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SCOPES     = ["https://www.googleapis.com/auth/spreadsheets"]

creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
ss     = client.open_by_key(SHEET_ID)

# 1. Sample Golf_Analytics — first 5 unique (player, event, year)
print("=== Golf_Analytics sample (col A=year, B=event, C=player) ===")
ga_data = ss.worksheet("Golf_Analytics").get_all_values()
seen = set()
samples = []
for row in ga_data[1:]:
    if len(row) >= 3:
        key = (row[0].strip(), row[1].strip(), row[2].strip())
        if key not in seen:
            seen.add(key)
            samples.append(key)
        if len(samples) >= 5:
            break
for s in samples:
    print(f"  year={s[0]!r}  event={s[1]!r}  player={s[2]!r}")

# 2. EVENTS — show first 5 rows (col A=id, H=name, AT=year)
print("\n=== EVENTS sample (col A=event_id, H=name, AT=year) ===")
ev_data = ss.worksheet("EVENTS").get_all_values()
for row in ev_data[1:6]:
    ev_id   = row[0]  if len(row) > 0  else ""
    ev_name = row[7]  if len(row) > 7  else ""
    ev_year = row[45] if len(row) > 45 else ""
    print(f"  id={ev_id!r}  name={ev_name!r}  year={ev_year!r}")

# 3. EVENTS_COURSES — show first 5 rows
print("\n=== EVENTS_COURSES sample ===")
ec_data = ss.worksheet("EVENTS_COURSES").get_all_values()
print(f"  Header: {ec_data[0][:7]}")
for row in ec_data[1:6]:
    print(f"  {row[:7]}")

# 4. Try a specific lookup end-to-end
print("\n=== End-to-end lookup for first sample ===")
if samples:
    ga_year, ga_event, ga_player = samples[0]
    print(f"  Looking up event_id for ({ga_event!r}, {ga_year!r}) ...")

    # Find in EVENTS
    match = None
    for row in ev_data[1:]:
        ev_name = row[7].strip()  if len(row) > 7  else ""
        ev_year = row[45].strip() if len(row) > 45 else ""
        ev_id   = row[0].strip()
        if ev_name == ga_event and ev_year == ga_year:
            match = (ev_id, ev_year)
            break
        # Also show near-misses
    if match:
        print(f"  Found: event_id={match[0]!r} events_year={match[1]!r}")
        # Now look in EVENTS_COURSES
        print(f"  Looking in EVENTS_COURSES for event_id={match[0]!r} ...")
        ec_matches = [r for r in ec_data[1:] if r[0].strip() == match[0]]
        if ec_matches:
            for r in ec_matches[:5]:
                print(f"    {r[:7]}")
        else:
            print(f"    NOT FOUND in EVENTS_COURSES")
    else:
        print(f"  NOT FOUND in EVENTS")
        # Show what's in EVENTS for this event name
        name_matches = [r for r in ev_data[1:] if r[7].strip() == ga_event]
        print(f"  EVENTS rows with name={ga_event!r}: {[r[0]+'/'+r[45] for r in name_matches[:5]]}")
