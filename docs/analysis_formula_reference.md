# ANALYSIS Sheet — Original Formula Reference

> These are the original Google Sheets formulas for each column.
> The build script now computes G-N and Q as **values** in Python for performance.
> To revert any column back to a formula, paste the formula below into row 2
> and fill down.

---

## Column A — player_id
```
=IFERROR(INDEX(PLAYERS!A:A, MATCH(B2, PLAYERS!B:B, 0)), "")
```
Looks up player_id by matching player_name (B) against PLAYERS!B.

---

## Column C — event_id
```
=IFERROR(INDEX(EVENTS!A:A, MATCH(E2, EVENTS!H:H, 0)), "")
```
⚠️ **Known issue:** MATCH returns first match only — breaks for events that repeat
across years. The build script fixes this by looking up (event_name + year) in Python.

---

## Column D — year
```
=IFERROR(INDEX(EVENTS!AT:AT, MATCH(C2, EVENTS!A:A, 0)), "")
```
⚠️ **Known issue:** Derived from event_id which itself had the MATCH bug above.
The build script writes year directly from Golf_Analytics col A.

---

## Column G — score (withdrawal-aware)
```
=IFERROR(
  LET(
    player, B2,
    event, E2,
    round_num, F2,
    course_avg, I2,
    scores, FILTER(Golf_Analytics!D:G, Golf_Analytics!C:C = player, Golf_Analytics!B:B = event),
    withdrawals, FILTER(Golf_Analytics!BN:BN, Golf_Analytics!C:C = player, Golf_Analytics!B:B = event),
    actual_score, INDEX(scores, 1, round_num),
    withdrawal_round, INDEX(withdrawals, 1),
    best_score, IF(withdrawal_round = 1, 0,
                  IF(withdrawal_round = 2, INDEX(scores, 1, 1),
                    IF(withdrawal_round = 3, MIN(INDEX(scores,1,1), INDEX(scores,1,2)),
                       MIN(INDEX(scores,1,1), INDEX(scores,1,2), INDEX(scores,1,3))))),
    penalty_score, IF(best_score = 0, course_avg + 4, best_score + 4),
    IF(round_num = withdrawal_round, penalty_score,
      IF(round_num > withdrawal_round, "", actual_score))
  ),
  ""
)
```
**Logic:**
- round = withdrawal_round → best prior score + 4 (or course_avg + 4 if withdrew in R1)
- round > withdrawal_round → blank
- otherwise → actual score from Golf_Analytics D-G

---

## Column H — par
```
=IFERROR(
  INDEX(FILTER(EVENTS_COURSES!D:D,
    EVENTS_COURSES!A:A = C2,
    EVENTS_COURSES!C:C = D2,
    EVENTS_COURSES!E:E = 1), 1),
  ""
)
```
Looks up par for the primary course (E=1) matching event_id (C) + year (D) in EVENTS_COURSES.

---

## Column I — course_avg (condition + round segmented)
```
=IFERROR(
  IF(K2="Calm",
    IF(F2=1, INDEX(EVENTS!AU:AU, MATCH(E2, EVENTS!H:H, 0)),
      IF(F2=2, INDEX(EVENTS!AV:AV, MATCH(E2, EVENTS!H:H, 0)),
        IF(F2=3, INDEX(EVENTS!AW:AW, MATCH(E2, EVENTS!H:H, 0)),
                 INDEX(EVENTS!AX:AX, MATCH(E2, EVENTS!H:H, 0))))),
    IF(K2="Moderate",
      IF(F2=1, INDEX(EVENTS!AY:AY, MATCH(E2, EVENTS!H:H, 0)),
        IF(F2=2, INDEX(EVENTS!AZ:AZ, MATCH(E2, EVENTS!H:H, 0)),
          IF(F2=3, INDEX(EVENTS!BA:BA, MATCH(E2, EVENTS!H:H, 0)),
                   INDEX(EVENTS!BB:BB, MATCH(E2, EVENTS!H:H, 0))))),
      IF(K2="Tough",
        IF(F2=1, INDEX(EVENTS!BC:BC, MATCH(E2, EVENTS!H:H, 0)),
          IF(F2=2, INDEX(EVENTS!BD:BD, MATCH(E2, EVENTS!H:H, 0)),
            IF(F2=3, INDEX(EVENTS!BE:BE, MATCH(E2, EVENTS!H:H, 0)),
                     INDEX(EVENTS!BF:BF, MATCH(E2, EVENTS!H:H, 0))))),
      ""))),
  ""
)
```
Looks up field average from EVENTS based on condition (K) and round (F).
Source columns: Calm=AU-AX, Moderate=AY-BB, Tough=BC-BF.

---

## Column J — diff_course_avg
```
=G2-I2
```

---

## Column K — condition
```
=IF(F2=1, INDEX(EVENTS!AH:AH, MATCH(E2, EVENTS!H:H, 0)),
  IF(F2=2, INDEX(EVENTS!AI:AI, MATCH(E2, EVENTS!H:H, 0)),
    IF(F2=3, INDEX(EVENTS!AJ:AJ, MATCH(E2, EVENTS!H:H, 0)),
             INDEX(EVENTS!AK:AK, MATCH(E2, EVENTS!H:H, 0)))))
```
Looks up round condition from EVENTS columns AH-AK (R1-R4).

---

## Column L — color (rhythm)
```
=IFERROR(
  LET(
    player, B2, event, E2, round_num, F2,
    rhythms, FILTER(
      {Golf_Analytics!R:R, Golf_Analytics!S:S, Golf_Analytics!T:T, Golf_Analytics!U:U},
      Golf_Analytics!C:C = player, Golf_Analytics!B:B = event),
    INDEX(rhythms, 1, round_num)
  ),
  ""
)
```
Pulls R1-R4 rhythm/color from Golf_Analytics cols R, S, T, U.

---

## Column M — exec
```
=IFERROR(
  LET(
    player, B2, event, E2, round_num, F2,
    execs, FILTER(
      {Golf_Analytics!V:V, Golf_Analytics!Y:Y, Golf_Analytics!AB:AB, Golf_Analytics!AE:AE},
      Golf_Analytics!C:C = player, Golf_Analytics!B:B = event),
    INDEX(execs, 1, round_num)
  ),
  ""
)
```
Pulls R1-R4 exec from Golf_Analytics cols V, Y, AB, AE.

---

## Column N — upside
```
=IFERROR(
  LET(
    player, B2, event, E2, round_num, F2,
    upsides, FILTER(
      {Golf_Analytics!W:W, Golf_Analytics!Z:Z, Golf_Analytics!AC:AC, Golf_Analytics!AF:AF},
      Golf_Analytics!C:C = player, Golf_Analytics!B:B = event),
    INDEX(upsides, 1, round_num)
  ),
  ""
)
```
Pulls R1-R4 upside from Golf_Analytics cols W, Z, AC, AF.

---

## Column O — player_hist_par  *(kept as formula)*
```
=IFERROR(
  AVERAGEIFS($Q$2:$Q$76737, $B$2:$B$76737, B2, $K$2:$K$76737, K2, $Q$2:$Q$76737, "<>"),
  ""
)
```
Player's historical average Off Par for this condition.
Requires full ANALYSIS dataset — kept as formula.

---

## Column P — player_his_cnt  *(kept as formula)*
```
=COUNTIFS($B$2:$B$76737, B2, $K$2:$K$76737, K2, $Q$2:$Q$76737, "<>")
```
Count of valid rounds used in player_hist_par.

---

## Column Q — Off Par
```
=LET(
  score, G2, par, H2, player, B2, event, E2, round_num, F2,
  round_types, FILTER(
    {Golf_Analytics!AU:AU, Golf_Analytics!AV:AV, Golf_Analytics!AW:AW, Golf_Analytics!AX:AX},
    Golf_Analytics!C:C = player, Golf_Analytics!B:B = event),
  round_type, INDEX(round_types, 1, round_num),
  IF(OR(score="", par="", round_type="Remove"), "", score - par)
)
```
Score minus par. Blank if score/par missing or round_type = "Remove".

---

## Column R — Adj_his_par  *(kept as formula)*
```
=IF(P2<2, "", (O2*P2 + VLOOKUP(K2, TOUR_STATS!$A$2:$B$4, 2, 0)*12) / (P2+12))
```
Empirical Bayes shrinkage: `(player_hist × n + tour_avg × 12) / (n + 12)`.
Shrinkage constant k=12. Blank if sample < 2.

---

## Data Source Map

| Column | Source |
|--------|--------|
| G scores | Golf_Analytics D-G (R1-R4) |
| G withdrawal | Golf_Analytics BN |
| H par | EVENTS_COURSES D (primary course, E=1) |
| I course_avg | EVENTS AU-BF (by condition + round) |
| K condition | EVENTS AH-AK (R1-R4) |
| L color | Golf_Analytics R-U (R1-R4) |
| M exec | Golf_Analytics V, Y, AB, AE (R1-R4) |
| N upside | Golf_Analytics W, Z, AC, AF (R1-R4) |
| Q round_type | Golf_Analytics AU-AX (R1-R4) |
| R tour avg | TOUR_STATS A-B (by condition) |
