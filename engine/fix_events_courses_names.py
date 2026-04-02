#!/usr/bin/env python3
"""
Fix EVENTS_COURSES for events where the name in EVENTS doesn't exactly match
the template name used in populate_events_courses.py.

Maps known aliases → template event_id (EVT_0001-0045).
"""

import os
import time
import gspread
from google.oauth2.service_account import Credentials

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_FILE = os.path.join(BASE_DIR, "luckifyme-f6c83489cd24.json")
SHEET_ID   = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SCOPES     = ["https://www.googleapis.com/auth/spreadsheets"]

# ─── Name alias map: EVENTS name → template event_id ─────────────────────────
# Key   = exact name as it appears in EVENTS col H
# Value = EVT_0001-0045 template to copy course/par from
ALIAS_MAP = {
    "Cognizant Classic in The Palm Beaches": "EVT_0008",
    "Cognizant Classic":                     "EVT_0008",
    "THE CJ CUP Byron Nelson":               "EVT_0019",
    "THE CJ CUP in South Carolina":          "EVT_0041",   # Mayakoba-style, confirm if needed
    "the Memorial Tournament pres. by Workday": "EVT_0022",
    "ISCO Championship":                     "EVT_0029",
    "The Open":                              "EVT_0030",
    "Procore Championship":                  "EVT_0037",
    "Sentry Tournament of Champions":        "EVT_0001",
    "World Wide Technology Championship at Mayakoba": "EVT_0041",
    "Cadence Bank Houston Open":             "EVT_0019",   # Houston = Byron Nelson course
    "Texas Children's Houston Open":         "EVT_0019",
    "Zurich Classic of New Orleans":         "EVT_0045",
    "Rocket Classic":                        "EVT_0026",   # Rocket Mortgage same course
    "Truist Championship":                   "EVT_0018",   # Quail Hollow = Wells Fargo course
}

# ─── Direct rows for new events with no matching template ────────────────────
# These events are new venues — par looked up, course_id is a placeholder
# Format: event_name → [course_id, par, sequence, notes]
DIRECT_COURSES = {
    "Myrtle Beach Classic":              ["COURSE_NEW_001", "71", "1", "Dunes Golf and Beach Club"],
    "ONEflight Myrtle Beach Classic":    ["COURSE_NEW_001", "71", "1", "Dunes Golf and Beach Club"],
    "Black Desert Championship":         ["COURSE_NEW_002", "71", "1", "Black Desert Resort"],
    "Bank of Utah Championship":         ["COURSE_NEW_002", "71", "1", "Black Desert Resort"],
    "Baycurrent Classic":                ["COURSE_NEW_003", "71", "1", "Yokohama Country Club West"],
}

# Events to skip entirely (not PGA Tour stroke play)
SKIP = {"Ryder Cup"}

EV_ID = 0; EV_NAME = 7; EV_YEAR = 45
EC_EVENT_ID = 0; EC_COURSE_ID = 1; EC_YEAR = 2
EC_PAR = 3; EC_SEQ = 4; EC_NOTES = 5


def event_num(eid):
    try: return int(eid.replace("EVT_", ""))
    except: return 9999


def main():
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)

    # ── Read EVENTS ───────────────────────────────────────────────────────────
    print("Reading EVENTS …")
    ev_data = ss.worksheet("EVENTS").get_all_values()

    # Events that need fixing: EVT_0046+ not yet handled
    missing_events = []
    for row in ev_data[1:]:
        if len(row) <= EV_YEAR: continue
        eid   = row[EV_ID].strip()
        ename = row[EV_NAME].strip()
        eyear = str(row[EV_YEAR]).strip()
        if not eid or not ename: continue
        if event_num(eid) > 45:
            missing_events.append((eid, ename, eyear))

    # ── Read EVENTS_COURSES ───────────────────────────────────────────────────
    print("Reading EVENTS_COURSES …")
    ec_sheet = ss.worksheet("EVENTS_COURSES")
    ec_data  = ec_sheet.get_all_values()

    existing_ids = {r[EC_EVENT_ID].strip() for r in ec_data[1:] if r[EC_EVENT_ID].strip()}

    # Build template courses: template_id → list of [course_id, par, seq, notes]
    template_courses: dict[str, list] = {}
    for row in ec_data[1:]:
        if len(row) < EC_SEQ + 1: continue
        eid = row[EC_EVENT_ID].strip()
        if event_num(eid) > 45: continue
        if eid not in template_courses:
            template_courses[eid] = []
        seq = row[EC_SEQ].strip()
        if not any(c[2] == seq for c in template_courses[eid]):
            template_courses[eid].append([
                row[EC_COURSE_ID].strip(),
                row[EC_PAR].strip(),
                seq,
                row[EC_NOTES].strip(),
            ])

    # ── Build new rows ────────────────────────────────────────────────────────
    print("Matching aliases …")
    new_rows = []
    skipped  = []
    unmatched = []

    for eid, ename, eyear in missing_events:
        if eid in existing_ids:
            continue
        if ename in SKIP:
            skipped.append((eid, ename, eyear))
            continue

        # Check direct course map first (new venues)
        if ename in DIRECT_COURSES:
            course_id, par, seq, notes = DIRECT_COURSES[ename]
            new_rows.append([eid, course_id, eyear, par, seq, notes, "Auto"])
            continue

        template_id = ALIAS_MAP.get(ename)
        if not template_id:
            unmatched.append((eid, ename, eyear))
            continue

        courses = template_courses.get(template_id, [])
        if not courses:
            unmatched.append((eid, ename, eyear))
            continue

        for course_id, par, seq, notes in courses:
            new_rows.append([eid, course_id, eyear, par, seq, notes, "Auto"])

    print(f"\n  {len(new_rows)} rows to add")

    if skipped:
        print(f"\n  Skipped (non-tour events):")
        for eid, ename, eyear in skipped:
            print(f"    {eid} | {eyear} | {ename}")

    if unmatched:
        print(f"\n  ⚠️  Still unmatched (add manually to EVENTS_COURSES):")
        for eid, ename, eyear in unmatched:
            print(f"    {eid} | {eyear} | {ename}")

    if not new_rows:
        print("Nothing to add.")
        return

    # ── Append ────────────────────────────────────────────────────────────────
    new_rows.sort(key=lambda r: (r[0], r[2]))
    print(f"\nAppending {len(new_rows)} rows to EVENTS_COURSES …")
    BATCH = 500
    for i in range(0, len(new_rows), BATCH):
        batch = new_rows[i:i+BATCH]
        ec_sheet.append_rows(batch, value_input_option="USER_ENTERED")
        print(f"  Appended {i+1}–{i+len(batch)} ✓")
        if i + BATCH < len(new_rows):
            time.sleep(1.2)

    print(f"\nDone! {len(new_rows)} rows added.")
    print("Par values used: Myrtle Beach=71, Black Desert/Bank of Utah=71, Baycurrent=71")


if __name__ == "__main__":
    main()
