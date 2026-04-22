# Luckify.me App

React + Vite app for the Luckify profile experience.

Live app:
- `https://luckify-me.pages.dev`

Marketing site:
- `https://luckify.me`

## What This App Is

This app is the interactive profile product, not the landing page.

It combines a few different systems into one mobile-first experience:
- Foundation Engine: the user's structural identity layer
- Decision Engine: the user's Human Design authority translated into a practical passive skill
- Active Rhythm: the user's current daily color field and guidance
- Command Mode: experimental / operator-facing tools and prototype interfaces

The current product direction is:
- premium dark UI
- mobile-first
- identity + daily context clearly separated
- app-like navigation rather than long webpage stacking

## Current App Architecture

The app shell is built around exactly 3 bottom tabs:

1. `Loadout`
   - primary daily experience
   - currently centered around the Color Rhythm / Active Rhythm card
   - includes the rhythm view and monthly calendar inside the same module

2. `Engine`
   - permanent identity and decision-support layer
   - Core Loadout
   - Passive Skills
   - Decision Engine inline expansion

3. `Cmd`
   - experimental and command-mode area
   - command-styled Core Loadout anchor
   - operator/debug/prototype modules

This separation is intentional:
- `Loadout` = what is active today
- `Engine` = what is always true
- `Cmd` = tools, experiments, structural/operator views

## Product Intent

The system is trying to make four truths legible:

1. `Core Loadout`
   - who the user fundamentally is
   - stable foundational identity

2. `Decision Engine`
   - how the user naturally arrives at clarity
   - always-on passive skill

3. `Active Rhythm`
   - the changing daily field
   - current environmental / timing layer

4. `Command Mode`
   - a more systemic or experimental lens
   - not the primary default experience

In practice:
- permanent systems should feel anchored
- daily systems should feel contextual
- experimental systems should be visually distinct but still coherent

## Repo Structure

```txt
src/
  App.jsx
  main.jsx
  App.css
  index.css

  components/
    ProfileForm.jsx
    ProfileDisplay.jsx
    ProfileMenu.jsx
    LuckyWindow.jsx
    RhythmCalendar.jsx
    CoreConfigCard.jsx
    PassiveSkillInlineCarousel.jsx
    DimensionCard.jsx
    GateContentCard.jsx
    LocationInput.jsx

    foundation/
      foundationGlyphs.tsx
      lifePathCrests.tsx
      TrajectoryMarker.jsx

  constants/
    coreConfig.js
    foundationHumanModeContent.js
    authorityLoadouts.js
    decisionEngine.js
    rhythmDecisionSupport.js
    colorRhythm.js
    tithi.js
    element.js
    lifePath.js
    blends.js
    geneKeys.js
    purposeGates.js
    planetaryFix.js

  lib/
    foundation/
      foundationGlyphRegistry.ts
      foundationGlyphTypes.ts
      lifePathCrestRegistry.ts
      lifePathCrestTypes.ts

  hooks/
    useProfileForm.js
    useProfileStorage.js

  utils/
    profileCalculator.js
    humanDesign.js
    geneKeys.js
    luckyWindow.js
    locationSearch.js
    tithi.js
    element.js
    lifePath.js
```

## Important Components

### `ProfileDisplay.jsx`

This is the app shell for the logged-in/profile state.

It owns:
- bottom-tab routing between `Loadout`, `Engine`, and `Cmd`
- composition of the main modules
- the split between permanent and daily layers
- Human Design and passive-skill wiring

If the product architecture changes, this file is usually the center of the work.

### `LuckyWindow.jsx`

This is the Active Rhythm card.

It owns:
- active rhythm presentation
- daily guidance
- one-time reveal animation
- rhythm/calendar panel switching
- reveal-state styling and transitions

Important:
- this component is both visually dense and stateful
- mobile overflow and panel behavior issues usually originate here or in `App.css`

### `RhythmCalendar.jsx`

This renders the monthly rhythm calendar and selected-day details.

It can run:
- standalone
- embedded inside `LuckyWindow`

Important:
- embedded behavior must stay contained inside the rhythm card
- selected-day details should not cause the whole mobile module to grow uncontrollably

### `CoreConfigCard.jsx`

This is the Foundation Engine card.

It supports:
- Human / character-facing presentation
- Operator / command-facing presentation

It is the anchor for:
- Foundation glyphs
- Life Path trajectory marker / crest area
- Human-mode guidance sections
- Operator-mode structural readout

### `PassiveSkillInlineCarousel.jsx`

Despite the filename, this is now the inline expanded passive-skill detail module.

Current behavior:
- tap a passive skill card
- reveal full-width vertical detail content beneath it
- no separate route required

### `foundation/`

These components hold the symbolic systems:
- 25 dynamic glyphs
- 12 Life Path crests
- trajectory marker logic

These systems should stay distinct:
- dynamic glyphs = compact operational emblems
- life path crests = larger destination/outcome insignias
- trajectory marker = numeric / directional life-path marker

## Data / Logic Layers

### Foundation Engine

Primary source:
- `src/constants/coreConfig.js`
- `src/constants/foundationHumanModeContent.js`

This powers:
- dynamic theme
- human-mode content
- operator-mode content
- loadout guidance

### Human Design

Primary logic:
- `src/utils/humanDesign.js`

This powers:
- defined channels
- defined centers
- type
- authority

The app uses authority to derive:
- decision engine label
- passive skill loadout
- rhythm-specific decision support

### Rhythm Support

Primary files:
- `src/components/LuckyWindow.jsx`
- `src/components/RhythmCalendar.jsx`
- `src/constants/rhythmDecisionSupport.js`
- `src/utils/luckyWindow.js`

This layer answers:
- what rhythm is active today
- how that rhythm affects the user's decision process
- what the best use / watch out is for today

## Styling System

Main styling lives in:
- `src/App.css`
- `src/index.css`

Important note:
- `App.css` is still the central style file for most of the app
- many recent layout and polish passes have been made there
- mobile card sizing, panel widths, rhythm slider behavior, and tab shell layout are all controlled there

If something looks wrong in production but correct locally, the first things to verify are:
- correct asset build deployed
- mobile-specific media query overrides
- width / height rules around `LuckyWindow`
- embedded `RhythmCalendar` overflow behavior

## Development

Install:

```bash
npm install
```

Run locally:

```bash
npm run dev
```

Build:

```bash
npm run build
```

Tests:

```bash
npm test
```

## Deployment Notes

Current known deployment split:
- `luckify.me` = marketing site
- `luckify-me.pages.dev` = app

That distinction matters when verifying fixes.

If localhost looks right but live does not, check:
1. are you looking at `luckify-me.pages.dev` or `luckify.me`
2. does the live app reference the latest `/assets/index-*.js` and `/assets/index-*.css`
3. is the issue only visible on mobile viewport/device state

## Current UX Principles

The product should feel:
- premium
- grounded
- symbolic
- mobile-first
- app-like, not webpage-like

It should avoid:
- noisy dashboards
- placeholder navigation
- overstuffed cards
- blending permanent identity with daily context in the same hierarchy layer

Current desired hierarchy:
- `Loadout` = daily field
- `Engine` = permanent mechanics
- `Cmd` = operator / experimental space

## Maintenance Guidance

When changing the app:
- preserve the distinction between permanent vs daily systems
- keep Human and Operator mode conceptually separate
- avoid adding extra nav patterns that compete with the bottom tabs
- prefer compact, contained mobile modules over long stacked layouts
- treat `LuckyWindow` as a high-sensitivity component for mobile regressions

If you are debugging a UI issue, start with:
- `ProfileDisplay.jsx` for structure
- `LuckyWindow.jsx` for rhythm interactions
- `RhythmCalendar.jsx` for embedded calendar growth
- `App.css` for width/height/overflow behavior
