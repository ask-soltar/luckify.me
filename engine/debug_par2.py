#!/usr/bin/env python3
"""Trace the exact par lookup for the first 3 combos."""

import os
import gspread
from google.oauth2.service_account import Credentials

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_FILE = os.path.join(BASE_DIR, "luckifyme-f6c83489cd24.json")
SHEET_ID   = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SCOPES     = ["https://www.googleapis.com/auth/spreadsheets"]
EV_YEAR    = 45
EV_ID      = 0
EV_NAME    = 7
EC_EVENT_ID = 0
EC_YEAR     = 2
EC_PAR      = 3
EC_PRIMARY  = 4

creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
ss     = client.open_by_key(SHEET_ID)

# Load data
print("Loading sheets...")
ga_data = ss.worksheet("Golf_Analytics").get_all_values()
ev_data = ss.worksheet("EVENTS").get_all_values()
ec_data = ss.worksheet("EVENTS_COURSES").get_all_values()

# Build lookups
event_id_lookup = {}
events_by_id    = {}
for row in ev_data[1:]:
    if len(row) > EV_YEAR:
        ev_id   = row[EV_ID].strip()
        ev_name = row[EV_NAME].strip()
        ev_year = str(row[EV_YEAR]).strip()
        if ev_id and ev_name and ev_year:
            event_id_lookup[(ev_name, ev_year)] = ev_id
            events_by_id[ev_id] = row

par_lookup = {}
for row in ec_data[1:]:
    if len(row) > EC_PRIMARY:
        ec_id      = row[EC_EVENT_ID].strip()
        ec_year    = str(row[EC_YEAR]).strip()
        ec_par     = row[EC_PAR].strip()
        ec_primary = row[EC_PRIMARY].strip()
        if ec_id and ec_year and ec_primary == "1":
            par_lookup[(ec_id, ec_year)] = ec_par

print(f"event_id_lookup: {len(event_id_lookup)} entries")
print(f"events_by_id:    {len(events_by_id)} entries")
print(f"par_lookup:      {len(par_lookup)} entries")

# Trace first 3 unique combos
seen = set()
count = 0
print("\n=== Tracing first 3 combos ===")
for row in ga_data[1:]:
    if len(row) < 3:
        continue
    year   = str(row[0]).strip()
    event  = row[1].strip()
    player = row[2].strip()
    key = (player, event, year)
    if key in seen or not (player and event and year):
        continue
    seen.add(key)

    event_id   = event_id_lookup.get((event, year), "")
    ev_row     = events_by_id.get(event_id, [])
    events_year = ev_row[EV_YEAR].strip() if len(ev_row) > EV_YEAR else ""
    par        = par_lookup.get((event_id, events_year), "")
    fallback   = par_lookup.get((event_id, year), "") if par == "" else "n/a"

    print(f"\nPlayer: {player}  Event: {event}  GA_year: {year}")
    print(f"  event_id:    {event_id!r}")
    print(f"  ev_row len:  {len(ev_row)}")
    print(f"  events_year: {events_year!r}")
    print(f"  par_lookup key tried: {(event_id, events_year)}")
    print(f"  par result:  {par!r}")
    print(f"  fallback:    {fallback!r}")
    print(f"  All EC keys for this event_id: {[k for k in par_lookup if k[0]==event_id]}")

    count += 1
    if count >= 3:
        break
