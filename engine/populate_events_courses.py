#!/usr/bin/env python3
"""
Populate EVENTS_COURSES for missing event_ids (EVT_0046+).

Strategy:
  1. Build event_name → template_event_id mapping from EVENTS (EVT_0001-0045)
  2. For each missing event_id (EVT_0046+):
     - Match event name to template
     - Copy course_id, par, course_sequence, notes from template rows
     - Add new row with the new event_id and correct year
  3. Append new rows to EVENTS_COURSES
  4. Print warnings for unmatched events
"""

import os
import time
import gspread
from google.oauth2.service_account import Credentials

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_FILE = os.path.join(BASE_DIR, "luckifyme-f6c83489cd24.json")
SHEET_ID   = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SCOPES     = ["https://www.googleapis.com/auth/spreadsheets"]

# EVENTS columns
EV_ID   = 0   # A
EV_NAME = 7   # H
EV_YEAR = 45  # AT

# EVENTS_COURSES columns
EC_EVENT_ID = 0   # A
EC_COURSE_ID = 1  # B
EC_YEAR      = 2  # C
EC_PAR       = 3  # D
EC_SEQ       = 4  # E
EC_NOTES     = 5  # F
EC_STATUS    = 6  # G

TEMPLATE_MAX_ID = 45   # EVT_0001 to EVT_0045 are the templates


def event_num(event_id: str) -> int:
    """Extract number from EVT_XXXX."""
    try:
        return int(event_id.replace("EVT_", ""))
    except:
        return 9999


def main():
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)

    # ── 1. Read EVENTS ────────────────────────────────────────────────────────
    print("Reading EVENTS …")
    ev_data = ss.worksheet("EVENTS").get_all_values()

    # template_events: event_name → event_id (EVT_0001-0045 only, latest year wins)
    template_events: dict[str, str] = {}
    # missing_events: list of (event_id, event_name, year) for EVT_0046+
    missing_events: list[tuple] = []

    for row in ev_data[1:]:
        if len(row) <= EV_YEAR:
            continue
        eid   = row[EV_ID].strip()
        ename = row[EV_NAME].strip()
        eyear = str(row[EV_YEAR]).strip()
        if not eid or not ename:
            continue

        num = event_num(eid)
        if num <= TEMPLATE_MAX_ID:
            template_events[ename] = eid
        else:
            missing_events.append((eid, ename, eyear))

    print(f"  {len(template_events)} template events (EVT_0001-{TEMPLATE_MAX_ID:04d})")
    print(f"  {len(missing_events)} missing events (EVT_0046+)")

    # ── 2. Read EVENTS_COURSES ────────────────────────────────────────────────
    print("Reading EVENTS_COURSES …")
    ec_sheet = ss.worksheet("EVENTS_COURSES")
    ec_data  = ec_sheet.get_all_values()

    # Build template rows: template_event_id → list of course rows
    # Each course row: [course_id, par, sequence, notes]
    template_courses: dict[str, list] = {}
    existing_ids: set[str] = set()

    for row in ec_data[1:]:
        if len(row) < EC_SEQ + 1:
            continue
        eid  = row[EC_EVENT_ID].strip()
        existing_ids.add(eid)
        num  = event_num(eid)
        if num <= TEMPLATE_MAX_ID:
            if eid not in template_courses:
                template_courses[eid] = []
            # Store one entry per course_sequence, using first year as template
            seq = row[EC_SEQ].strip()
            # Only store once per sequence (first year = 2022 is canonical)
            if not any(c[2] == seq for c in template_courses[eid]):
                template_courses[eid].append([
                    row[EC_COURSE_ID].strip(),  # course_id
                    row[EC_PAR].strip(),         # par
                    seq,                          # sequence
                    row[EC_NOTES].strip(),        # notes
                ])

    # ── 3. Build new rows ─────────────────────────────────────────────────────
    print("Building new EVENTS_COURSES rows …")
    new_rows = []
    unmatched = []

    for eid, ename, eyear in missing_events:
        if eid in existing_ids:
            continue   # already in EVENTS_COURSES, skip

        template_id = template_events.get(ename)
        if not template_id:
            unmatched.append((eid, ename, eyear))
            continue

        courses = template_courses.get(template_id, [])
        if not courses:
            unmatched.append((eid, ename, eyear))
            continue

        for course_id, par, seq, notes in courses:
            new_rows.append([
                eid,        # event_id
                course_id,  # course_id
                eyear,      # year
                par,        # par
                seq,        # course_sequence
                notes,      # notes
                "Auto"      # status
            ])

    print(f"  {len(new_rows)} new rows to add")

    if unmatched:
        print(f"\n  ⚠️  {len(unmatched)} events could not be matched (need manual entry):")
        for eid, ename, eyear in unmatched:
            print(f"    {eid} | {eyear} | {ename}")

    if not new_rows:
        print("Nothing to add.")
        return

    # ── 4. Append to EVENTS_COURSES ───────────────────────────────────────────
    print(f"\nAppending {len(new_rows)} rows to EVENTS_COURSES …")
    # Sort by event_id then year for clean ordering
    new_rows.sort(key=lambda r: (r[0], r[2]))

    # Append in batches
    BATCH = 500
    for i in range(0, len(new_rows), BATCH):
        batch = new_rows[i:i+BATCH]
        ec_sheet.append_rows(batch, value_input_option="USER_ENTERED")
        print(f"  Appended rows {i+1}–{i+len(batch)} ✓")
        if i + BATCH < len(new_rows):
            time.sleep(1.2)

    print(f"\nDone! Added {len(new_rows)} rows to EVENTS_COURSES.")
    print("Re-run build_analysis_v2.py after verifying the new rows.")


if __name__ == "__main__":
    main()
