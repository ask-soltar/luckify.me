# Luckify Me — React App Reference

**Stack:** React 18 + Vite · `npm run dev` (port 5173) · `npm run build`

---

## Source Layout

```
src/
  App.jsx                    — Root: page routing, profile storage wiring
  App.css                    — All component styles
  index.css                  — CSS variables (colors, fonts, zone vars)
  styles/pip-boy.css         — Shared pip-boy utility classes

  components/
    ProfileForm.jsx          — Birth date + location input form
    ProfileDisplay.jsx       — Full profile render (3 dimensions + calendar)
    DimensionCard.jsx        — Expandable dimension card (tabs + principles)
    LocationInput.jsx        — City autocomplete + manual UTC fallback
    LuckyWindow.jsx          — Today's BaZi lucky window score strip
    RhythmCalendar.jsx       — Monthly color rhythm calendar
    ProfileMenu.jsx          — Profile switcher slide-out menu
    LunarDots.jsx            — Legacy lunar dots (unused, keep for reference)

  constants/
    tithi.js                 — TITHI_DATA, TITHI_AXIOMS, TITHI_SVGS, TITHI_NAMES
    element.js               — ELEMENT_CONFIG, ELEMENT_AXIOMS, CHINESE_ZODIAC
    lifePath.js              — LP_CONFIG (keys 1–9, 11, 22, 33)
    blends.js                — BLENDS object keyed as 'Element × TithiType'
    colorRhythm.js           — COLOR_RHYTHM (8 zones), TITHI_COLOR_MAP, ZONE_MANTRAS

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
```

---

## Key Data Flows

**Profile creation:**
`ProfileForm` → `useProfileForm.handleSubmit` → `calculateProfile()` → stored via `useProfileStorage.addProfile`

**Lucky window (daily):**
`calcLuckyWindow({ birthDate, birthTime, birthGMT, eventDate, eventGMT })` → delta → `colorZoneFromDelta()` → zone name

**Calendar:**
`RhythmCalendar` calls `calcLuckyWindow` for every day in the displayed month using the stored profile's `birthDate`, `birthTime`, `birthGMT`, `currentGMT`.

**Location:**
`LocationInput` → `searchCities()` → GeoNames proxy (`https://geonames-proxy.luckifyme.workers.dev`) → IANA tz → `getOffsetForTZ()` → DST-aware numeric offset → `onSelect({ label, offset, tzId })`

---

## Profile Object Shape

```js
{
  id: 'PLY_xxxx',
  name: 'Element · TithiType',
  result: {
    type,           // tithi type: nanda|bhadra|jaya|rikta|purna
    cfg,            // tithi config object
    paksha,         // 'Shukla' | 'Krishna'
    tIdx,           // 0–29
    elong,          // degrees
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

---

## Design System

- **Fonts:** `Space Mono` (mono — labels, headers, data) · `DM Sans` (body — descriptions)
- **CSS vars:** `--pip-font-mono`, `--pip-font-body`, `--pip-bg`, `--pip-text`, `--pip-primary` (#00FF00), `--pip-border`
- **Zone vars:** `--zc-{zone}-bg` + `--zc-{zone}-text` for all 8 zones (pink/orange/blue/yellow/green/purple/red/brown)
- **Zone classes:** `.zc-pink`, `.zc-orange`, etc. — apply background + text color from zone vars

---

## 8 Color Zones (Lucky Window)

| Zone   | Delta range | Identity         |
|--------|-------------|------------------|
| Pink   | ≥ +14       | Peak Performance |
| Orange | ≥ +7        | Prime Flow       |
| Blue   | ≥ +4        | Sub-Prime        |
| Yellow | ≥ +2        | Edge             |
| Green  | ≥ −4        | Survivor         |
| Purple | ≥ −9        | Identity         |
| Red    | ≥ −29       | Unstable Swing   |
| Brown  | < −29       | Luck             |

---

## Conventions

- No Sheets, no GAS — pure React + browser APIs
- localStorage keys: `luckify_profiles`, `luckify_current`
- Old profiles without location fields get migrated on load in `useProfileStorage`
- Birth location is optional — defaults to UTC+0 if not set
- `calcLuckyWindow` is the canonical scoring function; `calcTodayWindow` is a thin wrapper for today's date
