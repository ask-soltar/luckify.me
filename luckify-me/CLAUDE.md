# Luckify Me — React App Reference

**Stack:** React 18 + Vite · `npm run dev` (port 5173) · `npm run build`
**Repo:** https://github.com/ask-soltar/luckify.me (work in `luckify-me/` subfolder)

---

## Product Stack

The app layers four identity systems on top of each other:

| Layer | Name | Source |
|-------|------|--------|
| Foundation Engine | Core Loadout / Core Configuration | Birth Tithi × Wu Xing Element × Life Path |
| Play Style | Life's Work | Gene Keys (Life's Work gate) |
| Power Source | Radiance | Gene Keys (Radiance gate) |
| Main Quest | Purpose | Gene Keys (Purpose gate) + PURPOSE_GATES content |
| Passive Traits | Tithi subtypes, Moon, etc. | Tithi, Moon phase |
| Dimensions IV–V | Gene Keys + Planetary Fix | Calculated from birth chart |

**Foundation Engine is the core layer** and must remain distinct from the others.

---

## Source Layout

```
src/
  App.jsx                    — Root: page routing, profile storage wiring
  App.css                    — All component styles (single file)
  index.css                  — CSS variables (colors, fonts, zone vars)
  styles/pip-boy.css         — Shared pip-boy utility classes

  components/
    ProfileForm.jsx          — Birth date + location input form
    ProfileDisplay.jsx       — Full profile render — all layers, wires CCE data
    CoreConfigCard.jsx       — Foundation Engine card (Standard/Operator dual mode)
    DimensionCard.jsx        — Expandable dimension card (tabs + principles) — Dims IV, V
    GateContentCard.jsx      — Purpose frame (Gene Keys purpose gate content)
    LocationInput.jsx        — City autocomplete + manual UTC fallback
    LuckyWindow.jsx          — Today's BaZi lucky window score strip (Layer 1)
    RhythmCalendar.jsx       — Monthly color rhythm calendar (Layer 3)
    ProfileMenu.jsx          — Profile switcher slide-out menu
    LunarDots.jsx            — Legacy lunar dots (unused, keep for reference)

  constants/
    coreConfig.js            — Foundation Engine V2: 4 tables + generation logic (SEE BELOW)
    tithi.js                 — TITHI_DATA, TITHI_AXIOMS, TITHI_SVGS, TITHI_NAMES
    element.js               — ELEMENT_CONFIG, ELEMENT_AXIOMS, CHINESE_ZODIAC
    lifePath.js              — LP_CONFIG (keys 1–9, 11, 22, 33)
    blends.js                — BLENDS keyed as 'Element × TithiType' (Foundation blend)
    colorRhythm.js           — COLOR_RHYTHM (8 zones), TITHI_COLOR_MAP, ZONE_MANTRAS
    geneKeys.js              — GENE_KEYS[gate] → { shadow, gift, siddhi }
    purposeGates.js          — PURPOSE_GATES[gate] → { overall, lines } content
    planetaryFix.js          — PLANETARY_FIX['gate.line'] → { exalt, detriment }

  hooks/
    useProfileStorage.js     — localStorage profiles list + CRUD
    useProfileForm.js        — Form state, validation, location handlers

  utils/
    profileCalculator.js     — calculateProfile(), generateProfileName(), generateId()
    tithi.js                 — calcTithi(), dateToSerial()
    element.js               — getChineseZodiac()
    lifePath.js              — calcLifePath()
    luckyWindow.js           — calcLuckyWindow(), calcTodayWindow(), colorZoneFromDelta()
    locationSearch.js        — searchCities() via GeoNames proxy, getOffsetForTZ()
    geneKeys.js              — calcGeneKeys(), calcAllActivations()
```

---

## Foundation Engine V2 — coreConfig.js

The core of the identity layer. Four tables, 300 modular profiles (25 dynamics × 12 life paths).

### Tables

**TITHI_CCE** (5 rows: nanda / bhadra / jaya / rikta / purna)
- `functional_name` — displayed in meta line
- `watchout_fragment`, `best_use_fragment` — used by generation fallbacks

**ELEMENT_CCE** (5 rows: Wood / Fire / Earth / Metal / Water)
- `functional_name` — displayed in meta line
- `watchout_fragment`, `best_use_fragment` — used by generation fallbacks

**LP_CCE** (12 rows: 1–9, 11, 22, 33)
- `outcome` — "Enduring Structures", "Deep Understanding", etc.
- `lp_tail` — Standard mode reveal tail: "so you can build something that lasts."
- `directional_vector` — Operator mode diagnostic: "Orients toward…"

**TITHI_ELEM_DYN** (25 rows: keyed as `'tithi:Element'` e.g. `'rikta:Fire'`)

Standard mode fields:
- `simple_reveal_stem` — continues "You're naturally wired to…"
- `recognition_line_simple` — "Often this shows up as…"
- `simple_natural_expression` — "What comes naturally…"
- `simple_developmental_force` — "What life teaches you…"
- `simple_pattern_statement` — "How it shows up…"

Operator mode fields:
- `operator_dynamic_pattern` — "Dynamic Pattern"
- `recognition_signal_operator` — "Recognition Signal"
- `operator_natural_expression` — "Natural Expression"
- `operator_developmental_pressure` — "Developmental Pressure"
- `operator_emergent_pattern` — "Emergent Pattern"

Shared across modes:
- `configuration_theme_name` — "The Structural Reformer", etc. (25 unique names)
- `watch_for` — Watch For override (per dynamic)
- `best_use` — Best Use override (per dynamic, parsed into 3 beats for display)

### Exported functions
- `getDynamic(tithi, element)` → TITHI_ELEM_DYN entry or null
- `generateWatchFor(tithi, element, lifePathNum)` → fallback Watch For string
- `generateBestUse(tithi, element, lifePathNum)` → fallback Best Use string

---

## CoreConfigCard — Dual-Mode UI

**Props:** `icon, tithi, element, dynamic, lifePathNum, watchFor, bestUse`

Where these come from in ProfileDisplay.jsx:
```js
const cceT    = TITHI_CCE[type];
const cceEl   = ELEMENT_CCE[element];
const cceLp   = LP_CCE[lifePathNum];
const dynamic = getDynamic(type, element);
const watchFor = dynamic?.watch_for  || generateWatchFor(type, element, lifePathNum);
const bestUse  = dynamic?.best_use   || generateBestUse(type, element, lifePathNum);
```

**Top-level STD | OPR toggle** in the card header switches the whole card.

### Standard mode ("CORE LOADOUT")
1. "You're naturally wired to…" + `simple_reveal_stem` + `lp_tail`
2. ✦ "Often this shows up as…" + `recognition_line_simple`
3. "Because of this, you may be drawn to cultivate…" + LP `outcome`
4. ▼ **Loadout Mechanics** (expandable): 3 simple fields with ①②③ numbers
5. ⚠ Watch For · 🛠 Best Use (3-beat parsed)

### Operator mode ("CORE CONFIGURATION")
1. **Dynamic Pattern** — `operator_dynamic_pattern`
2. **Directional Vector** — `directional_vector` (from LP_CCE)
3. **Recognition Signal** — `recognition_signal_operator`
4. "Because of this, you may be drawn to cultivate…" + LP `outcome`
5. ▼ **Configuration Logic** (expandable): 3 diagnostic fields
6. ⚠ Watch For · 🛠 Best Use (shared)

---

## ProfileDisplay — Layer Structure

```
Layer 1: LuckyWindow          — today's BaZi score strip (always visible)
Layer 2: FoundationSection    — who you are (always visible)
  └ blend statement           — Element × Tithi blend
  └ CoreConfigCard            — Foundation Engine (Dims I/II/III)
  └ DimensionCard (IV)        — Gene Keys (Life's Work, Evolution, Radiance, Purpose)
  └ DimensionCard (V)         — Planetary Fix (exalted / detriment activations)
Layer 3: RhythmCalendar       — monthly color rhythm (expandable)
Layer 4: GateContentCard      — Purpose frame (Gene Keys purpose gate)
```

---

## Key Data Flows

**Profile creation:**
`ProfileForm` → `useProfileForm.handleSubmit` → `calculateProfile()` → stored via `useProfileStorage.addProfile`

**Gene Keys (always recomputed):**
`calcGeneKeys({ year, month, day, birthTime, tzOffset })` → `{ lifeWork, evolution, radiance, purpose }` each with `{ gate, line }`

**Planetary Fix:**
`calcAllActivations(...)` → 24 activations → match against `PLANETARY_FIX['gate.line']` → exalted / detriment

**Lucky window (daily):**
`calcLuckyWindow({ birthDate, birthTime, birthGMT, eventDate, eventGMT })` → delta → `colorZoneFromDelta()` → zone name

**Calendar:**
`RhythmCalendar` calls `calcLuckyWindow` for every day in the month using the stored profile.

**Location:**
`LocationInput` → `searchCities()` → GeoNames proxy (`https://geonames-proxy.luckifyme.workers.dev`) → IANA tz → `getOffsetForTZ()` → DST-aware offset

---

## Profile Object Shape

```js
{
  id: 'PLY_xxxx',
  name: 'Element · TithiType',
  result: {
    type,           // tithi type: nanda|bhadra|jaya|rikta|purna
    element,        // Wu Xing: Wood|Fire|Earth|Metal|Water
    zodiac,         // Chinese zodiac animal
    lifePathNum,    // 1–9, 11, 22, 33
    y, mo, dy,      // birth year/month/day
    birthTime,      // 'HH:MM' string
    birthGMT,       // numeric UTC offset (birth location)
    birthTzId,      // IANA tz string
    currentGMT,     // numeric UTC offset (current location)
    currentTzId,    // IANA tz string
  }
}
```

Gene Keys and activations are **always recomputed at runtime** from stored birth data — they are not stored in the profile object.

---

## Design System

- **Fonts:** `Space Mono` (mono — labels, headers, data) · `DM Sans` (body — descriptions)
- **Palette:** Dark pip-boy terminal. Primary green `#00FF00`. Operator accents in amber/orange.
- **CSS vars:** `--pip-font-mono`, `--pip-font-body`, `--pip-bg`, `--pip-text`, `--pip-text-dim`, `--pip-primary` (#00FF00), `--pip-border`
- **Zone vars:** `--zc-{zone}-bg` + `--zc-{zone}-text` for all 8 zones
- **Zone classes:** `.zc-pink`, `.zc-orange`, etc.
- **Element accent vars:** `--el-text`, `--el-accent` — set inline on FoundationSection

---

## 8 Color Zones (Lucky Window)

| Zone   | Delta  | Identity         |
|--------|--------|------------------|
| Pink   | ≥ +14  | Peak Performance |
| Orange | ≥ +7   | Prime Flow       |
| Blue   | ≥ +4   | Sub-Prime        |
| Yellow | ≥ +2   | Edge             |
| Green  | ≥ −4   | Survivor         |
| Purple | ≥ −9   | Identity         |
| Red    | ≥ −29  | Unstable Swing   |
| Brown  | < −29  | Luck             |

---

## Conventions

- No Sheets, no GAS — pure React + browser APIs
- localStorage keys: `luckify_profiles`, `luckify_current`
- Old profiles without location fields get migrated on load in `useProfileStorage`
- Birth location optional — defaults to UTC+0
- `calcLuckyWindow` is canonical; `calcTodayWindow` is a thin wrapper for today
- Gene Keys + activations always recomputed at runtime — never trust stale stored values
- `dynamic?.watch_for` and `dynamic?.best_use` take priority; `generateWatchFor/BestUse` are fallbacks only
- Do NOT merge Standard and Operator content — they are always displayed as separate fields
