# Luckify Me — Working Reference

**Repo:** https://github.com/ask-soltar/luckify.me  
**App folder:** `luckify-me/`  
**Live app:** `https://luckify-me.pages.dev`  
**Marketing site:** `https://luckify.me`

This file is the fast internal map for the app as it exists now.

## What We Are Building

The app is a mobile-first profile system that combines:
- permanent identity systems
- daily field / rhythm systems
- experimental operator tools

The current product structure is intentional:

### Permanent layer
- Core Loadout
- Passive Skills
- Decision Engine

### Daily layer
- Active Rhythm
- Today's decision guidance
- Monthly rhythm calendar

### Experimental layer
- Command-mode tools
- prototype modules
- operator-style system views

The app should feel like:
- a real mobile app
- premium and atmospheric
- symbolic but practical
- system-based rather than page-based

## Current Navigation Model

There are exactly 3 bottom tabs:

1. `Loadout`
   - daily-facing tab
   - currently centered around the Color Rhythm / Active Rhythm module

2. `Engine`
   - permanent mechanics tab
   - Core Loadout + Passive Skills + Decision Engine

3. `Cmd`
   - experimental/operator tab
   - command-mode core card + experimental tools

Important:
- do not add competing top-level navigation lightly
- do not reintroduce redundant mode switches that fight the bottom tabs

## Current Intent By Tab

### Loadout

Purpose:
- show the user's current daily field
- help them understand today's rhythm
- keep the experience compact and readable on mobile

This tab should answer:
- what field am I in today?
- what does that mean for me today?

### Engine

Purpose:
- show stable identity and decision mechanics
- keep permanent systems separate from daily state

This tab should answer:
- who am I structurally?
- how do I naturally decide?

### Cmd

Purpose:
- hold experimental tools and operator-facing modules
- act as the sandbox / diagnostic / evolving systems area

This tab should answer:
- what tools or alternate system views are available?

## Key Files

### App shell / structure

- `src/components/ProfileDisplay.jsx`
  - bottom-tab app shell
  - routes between `Loadout`, `Engine`, and `Cmd`
  - wires together daily, permanent, and experimental modules

### Rhythm / daily system

- `src/components/LuckyWindow.jsx`
  - Active Rhythm card
  - daily decision guidance
  - one-time reveal animation
  - two-panel rhythm/calendar module

- `src/components/RhythmCalendar.jsx`
  - monthly rhythm calendar
  - embedded day detail behavior
  - month switching and selected-day details

### Foundation / permanent system

- `src/components/CoreConfigCard.jsx`
  - Foundation Engine card
  - Human mode + Operator mode rendering

- `src/components/PassiveSkillInlineCarousel.jsx`
  - inline expanded passive-skill module
  - now vertical full-width content, despite the older filename

### Profile setup and persistence

- `src/components/ProfileForm.jsx`
- `src/hooks/useProfileForm.js`
- `src/hooks/useProfileStorage.js`

### Styling

- `src/App.css`
  - main app styles
  - most layout and component styling still lives here
  - rhythm card sizing, panel behavior, tab shell, and mobile tuning are all controlled here

- `src/index.css`
  - shared variables and base styles

## Data / Content Sources

### Foundation Engine

- `src/constants/coreConfig.js`
- `src/constants/foundationHumanModeContent.js`

These define:
- dynamic identities
- human-mode content
- operator-mode content
- generated profile logic

### Human Design

- `src/utils/humanDesign.js`

This derives:
- defined channels
- defined centers
- type
- authority

Authority then powers:
- `src/constants/decisionEngine.js`
- `src/constants/authorityLoadouts.js`
- `src/constants/rhythmDecisionSupport.js`

### Rhythm system

- `src/utils/luckyWindow.js`
- `src/constants/colorRhythm.js`
- `src/constants/rhythmDecisionSupport.js`

These power:
- active rhythm
- monthly calendar
- daily guidance

## Symbol Systems

### Dynamic glyphs

- `src/components/foundation/foundationGlyphs.tsx`
- `src/lib/foundation/foundationGlyphRegistry.ts`

Purpose:
- compact operational identity emblems

### Life Path crests

- `src/components/foundation/lifePathCrests.tsx`
- `src/lib/foundation/lifePathCrestRegistry.ts`

Purpose:
- larger destination-oriented insignias

### Trajectory marker

- `src/components/foundation/TrajectoryMarker.jsx`

Purpose:
- life path number as directional marker
- element shapes the surrounding treatment

## Current UX Rules

### Permanent vs daily

Keep these distinct:
- Core Loadout and Decision Engine are permanent
- Active Rhythm is daily

Do not collapse them into one indistinct card hierarchy unless explicitly intended.

### Mobile-first

The app must behave like an app, not a long webpage.

Especially sensitive:
- `LuckyWindow`
- embedded `RhythmCalendar`
- tab shell height/width behavior
- panel slider behavior on mobile

### Command mode

`Cmd` is experimental.

It should:
- feel distinct
- keep consistent structural typography
- not hijack the default human-facing experience

## Known Sensitive Areas

### LuckyWindow panel sizing

Common regression types:
- card too tall on mobile
- card wider than the other cards
- calendar selection causing expansion
- panel slider showing split-screen / both panels at once

When debugging these, check:
- `ProfileDisplay.jsx`
- `LuckyWindow.jsx`
- `RhythmCalendar.jsx`
- `App.css`

### Deployment confusion

Important distinction:
- `luckify.me` is not the app
- `luckify-me.pages.dev` is the app

When verifying live UI changes, always compare against `luckify-me.pages.dev`.

## Current Design Direction

The visual system should be:
- premium dark
- symbolic
- coherent
- grounded
- cinematic but restrained

Avoid:
- accidental dashboard feel
- overly neon operator styling in human flows
- extra wrapper panels that make cards feel double-nested
- letting daily modules outgrow the card rail on mobile

## Development Commands

Run dev:

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

## Practical Debugging Order

If something is wrong:

1. Check the structure in `ProfileDisplay.jsx`
2. Check interaction/state in `LuckyWindow.jsx`
3. Check embedded calendar behavior in `RhythmCalendar.jsx`
4. Check actual width/height/overflow rules in `App.css`
5. Verify the deployed app at `luckify-me.pages.dev`

## Main Principle

The product should help the user feel:
- this is who I am
- this is how I naturally decide
- this is what today is doing
- this is how to work with today

That hierarchy should stay legible in both the code and the UI.
