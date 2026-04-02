#!/usr/bin/env python3
"""Build first 100 rows into ANALYSIS_test sheet for verification."""

import re
import time
import os
import sys
import gspread
from google.oauth2.service_account import Credentials

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_FILE   = os.path.join(BASE_DIR, "luckifyme-f6c83489cd24.json")
SHEET_ID     = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SOURCE_SHEET = "ANALYSIS"
TARGET_SHEET = "ANALYSIS_test"
SCOPES       = ["https://www.googleapis.com/auth/spreadsheets"]
ROW_LIMIT    = 100   # only build this many data rows

EV_YEAR=45; EV_ID=0; EV_NAME=7; EV_COND=[33,34,35,36]
EV_CALM=[46,47,48,49]; EV_MOD=[50,51,52,53]; EV_TOUGH=[54,55,56,57]
GA_YEAR=0; GA_EVENT=1; GA_PLAYER=2; GA_SCORES=[3,4,5,6]
GA_COLORS=[17,18,19,20]; GA_EXECS=[21,24,27,30]; GA_UPSIDES=[22,25,28,31]
GA_RT=[46,47,48,49]; GA_WITHDRAW=65
EC_EVENT_ID=0; EC_YEAR=2; EC_PAR=3; EC_PRIMARY=4

HEADER = ["player_id","player_name","event_id","year","event_name","round_num",
          "score","par","course_avg","diff_course_avg","condition","color",
          "exec","upside","player_hist_par","player_his_cnt","Off Par","Adj_his_par"]

def col_letter(n):
    result=""; n+=1
    while n:
        n,rem=divmod(n-1,26); result=chr(65+rem)+result
    return result

def safe_float(v):
    try: return float(v)
    except: return None

def get_col(row, idx, default=""):
    try:
        v = row[idx]
        v = v.strip() if isinstance(v,str) else v
        return v if v!="" else default
    except: return default

def adjust_row(f, fr, to):
    if not isinstance(f,str) or not f.startswith("="): return f
    return re.sub(r"(?<!\$)([A-Z]{1,3})"+str(fr)+r"(?!\d)", lambda m: m.group(1)+str(to), f)

def expand_locked_range(f, total):
    return re.sub(r"(\$[A-Z]{1,3}\$2:\$[A-Z]{1,3}\$)(\d+)", lambda m: m.group(1)+str(total), f)

def compute_score(row, rnd, ca):
    scores=[safe_float(get_col(row,c)) for c in GA_SCORES]
    wr=safe_float(get_col(row,GA_WITHDRAW)); wd=int(wr) if wr else 0
    actual=scores[rnd-1]
    if wd==0: return actual if actual is not None else ""
    if rnd>wd: return ""
    if rnd==wd:
        prior=[s for s in scores[:wd-1] if s is not None]
        if not prior:
            c=safe_float(ca); return (c+4) if c is not None else ""
        return min(prior)+4
    return actual if actual is not None else ""

def get_condition(ev, rnd): return get_col(ev, EV_COND[rnd-1])
def get_course_avg(ev, cond, rnd):
    m={"Calm":EV_CALM,"Moderate":EV_MOD,"Tough":EV_TOUGH}
    cols=m.get(cond); return get_col(ev,cols[rnd-1]) if cols else ""
def get_off_par(score, par, row, rnd):
    if score=="" or par=="": return ""
    if get_col(row,GA_RT[rnd-1])=="Remove": return ""
    s,p=safe_float(score),safe_float(par)
    return (s-p) if s is not None and p is not None else ""

def main():
    creds=Credentials.from_service_account_file(CREDS_FILE,scopes=SCOPES)
    client=gspread.authorize(creds)
    ss=client.open_by_key(SHEET_ID)

    print("Loading data...")
    ga_data=ss.worksheet("Golf_Analytics").get_all_values()
    ev_data=ss.worksheet("EVENTS").get_all_values()
    ec_data=ss.worksheet("EVENTS_COURSES").get_all_values()

    event_id_lookup={}; events_by_id={}
    for row in ev_data[1:]:
        if len(row)>EV_YEAR:
            eid=row[EV_ID].strip(); en=row[EV_NAME].strip(); ey=str(row[EV_YEAR]).strip()
            if eid and en and ey:
                event_id_lookup[(en,ey)]=eid; events_by_id[eid]=row

    par_lookup={}
    for row in ec_data[1:]:
        if len(row)>EC_PRIMARY:
            eid=row[EC_EVENT_ID].strip(); ey=str(row[EC_YEAR]).strip()
            ep=row[EC_PAR].strip(); eprim=row[EC_PRIMARY].strip()
            if eid and ey and eprim=="1": par_lookup[(eid,ey)]=ep

    tmpl=ss.worksheet(SOURCE_SHEET).row_values(2,value_render_option="FORMULA")
    while len(tmpl)<18: tmpl.append("")
    tmpl_a=tmpl[0]; tmpl_o=tmpl[14]; tmpl_p=tmpl[15]; tmpl_r=tmpl[17]

    # Get combos
    ga_lookup={}; combos=set()
    for row in ga_data[1:]:
        if len(row)>=3:
            y=str(row[GA_YEAR]).strip(); e=row[GA_EVENT].strip(); p=row[GA_PLAYER].strip()
            if p and e and y:
                ga_lookup[(p,e,y)]=row; combos.add((p,e,y))
    combos=sorted(combos)

    locked_end = min(ROW_LIMIT+1, len(combos)*4+1)

    # Create/clear test sheet
    try:
        v2=ss.worksheet(TARGET_SHEET); v2.clear()
    except: v2=ss.add_worksheet(TARGET_SHEET,rows=ROW_LIMIT+10,cols=18)
    v2.update("A1:R1",[HEADER],value_input_option="USER_ENTERED")

    print(f"Building first {ROW_LIMIT} rows...")
    all_rows=[]; row_num=2

    for player,event,year in combos:
        if len(all_rows)>=ROW_LIMIT: break
        eid=event_id_lookup.get((event,year),"")
        ev_row=events_by_id.get(eid,[])
        events_year=get_col(ev_row,EV_YEAR) if ev_row else year
        par=par_lookup.get((eid,events_year),"")
        if par=="" and year!=events_year:
            par=par_lookup.get((eid,year),"")
        ga_row=ga_lookup.get((player,event,year),[])

        for rnd in range(1,5):
            if len(all_rows)>=ROW_LIMIT: break
            cond=get_condition(ev_row,rnd) if ev_row else ""
            ca=get_course_avg(ev_row,cond,rnd) if ev_row else ""
            score=compute_score(ga_row,rnd,ca) if ga_row else ""
            s,c=safe_float(score),safe_float(ca)
            diff=(s-c) if s is not None and c is not None else ""
            def bf(t): return expand_locked_range(adjust_row(t,2,row_num),locked_end)
            all_rows.append([
                adjust_row(tmpl_a,2,row_num), player, eid, year, event, rnd,
                score, par, ca, diff, cond,
                get_col(ga_row,GA_COLORS[rnd-1]) if ga_row else "",
                get_col(ga_row,GA_EXECS[rnd-1]) if ga_row else "",
                get_col(ga_row,GA_UPSIDES[rnd-1]) if ga_row else "",
                bf(tmpl_o), bf(tmpl_p),
                get_off_par(score,par,ga_row,rnd) if ga_row else "",
                bf(tmpl_r)
            ])
            row_num+=1

    v2.update(f"A2:{col_letter(17)}{row_num-1}",all_rows,value_input_option="USER_ENTERED")
    print(f"Done! Check ANALYSIS_test tab ({len(all_rows)} rows)")

if __name__=="__main__":
    main()
