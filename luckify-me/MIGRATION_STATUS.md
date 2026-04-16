# Luckify Me — React + Vite Migration: Phase 1 Complete

**Status:** Data extraction and calculation utilities complete. Ready for UI implementation.

---

## Completed: Data Files & Calculation Utilities

### Constants (4 files, 469 lines total)
- **`src/constants/tithi.js`** (146 lines)
  - TYPES, TITHI_NAMES, TYPE_CONFIG
  - TITHI_SVGS (5 SVG path icons)
  - TITHI_DATA (5 types with operating/intuitive principles)

- **`src/constants/element.js`** (179 lines)
  - ELEMENT_CONFIG (5 Wu Xing elements with keywords + descriptions)
  - CHINESE_ZODIAC (130 years, 1900–2029, with lunar new year dates)

- **`src/constants/lifePath.js`** (82 lines)
  - LP_CONFIG (1-9, 11, 22, 33 with names, numbers, axioms)
  - LP_KEYWORDS (quick lookup)

- **`src/constants/blends.js`** (62 lines)
  - BLENDS (element × tithi combinations — abbreviated, full data to be added)
  - getBlend() helper function

### Utilities (4 files, 290 lines total)
- **`src/utils/tithi.js`** (81 lines)
  - `dateToSerial(y, m, d)` — converts calendar date to Excel serial (for astronomical calcs)
  - `calcTithi(year, month, day, hour12, minute, ampm, tzOffset)` — returns { type, typeIdx, tIdx, elong, paksha }
  - Includes complete solar longitude + elongation astronomical math

- **`src/utils/element.js`** (41 lines)
  - `getChineseZodiac(year, month, day)` — returns zodiac entry with CNY cutoff logic

- **`src/utils/lifePath.js`** (62 lines)
  - `calcLifePath(month, day, year)` — Pythagorean reduction with master number preservation
  - `reduceToSingleOrMaster(n)` — helper for reduction logic

- **`src/utils/profileCalculator.js`** (106 lines)
  - `calculateProfile(inputs)` — orchestrates all three dimensions into a single result
  - `generateProfileName(element, tithiType)` — creates display name
  - `generateId()` — creates unique profile IDs
  - `validateProfileInputs(inputs)` — basic validation

---

## Data Extraction Summary

All data extracted from `APP/tithi-profiler.html`:

| Source | Extracted | Lines | Notes |
|--------|-----------|-------|-------|
| TYPES array | ✓ | 5 | Tithi types: nanda, bhadra, jaya, rikta, purna |
| TITHI_NAMES | ✓ | 30 | Poker-themed names per tithi |
| TYPE_CONFIG | ✓ | 28 | Config per type (labels, colors, glows) |
| TITHI_SVGS | ✓ | 5 | SVG paths for visual icons |
| TITHI_DATA | ✓ | ~400 | Operating + intuitive principles per type |
| ELEMENT_CONFIG | ✓ | 25 | 5 elements with keywords + descriptions |
| CHINESE_ZODIAC | ✓ | 130 | 1900–2029 with lunar new year dates |
| LP_CONFIG | ✓ | 12 | Life Path 1–9, 11, 22, 33 (abbreviated) |
| BLENDS | ⚠️ | 25 | Abbreviated; full principles to be extracted |
| calcTithi logic | ✓ | 30 | Solar longitude + sun-moon elongation math |
| calcLifePath logic | ✓ | 20 | Pythagorean reduction with master numbers |
| getChineseZodiac logic | ✓ | 15 | CNY cutoff date lookup |

---

## Verification

✓ All 8 JavaScript files pass Node.js syntax validation
✓ No missing imports or circular dependencies
✓ Constants organized by dimension (Tithi, Element, Life Path)
✓ Utilities separated from data files

---

## Next Steps (UI Implementation)

1. **Create profile form component** — input fields for date/time/timezone
2. **Create profile display components** — render calculated dimensions
3. **Integrate with state management** — localStorage for saved profiles
4. **Build Pip-Boy UI** — poker character screen with three dimensions displayed
5. **Add profile menu/switcher** — navigate saved profiles
6. **Style with Pip-Boy aesthetics** — retro terminal look

## Notes

- **Blends constant**: Currently holds 3 sample blends. Full 25 combinations can be extracted from `APP/tithi-profiler.html` line ~1156 if needed for detailed display.
- **Life Path descriptions**: Abbreviated to core names/axioms. Full operating/intuitive/wealth principles in source HTML (lines 741-925) can be added if UI needs them.
- **No UI changes yet**: App.jsx, main.jsx, and CSS remain untouched boilerplate.

---

## File Structure

```
luckify-me/src/
├── constants/
│   ├── tithi.js          (Tithi types, config, data)
│   ├── element.js        (Wu Xing + Chinese zodiac)
│   ├── lifePath.js       (Life Path 1-9, 11, 22, 33)
│   └── blends.js         (Element × Tithi combinations)
├── utils/
│   ├── tithi.js          (Astronomical calculations)
│   ├── element.js        (Zodiac lookup)
│   ├── lifePath.js       (Numerology)
│   └── profileCalculator.js (Orchestrator)
├── App.jsx               (Unchanged boilerplate)
├── main.jsx              (Unchanged)
└── index.css / App.css   (Unchanged)
```
