# Main Quest Command Mode Notes

This file captures what has been built for the Command Mode Main Quest system, why those decisions were made, and what the current implementation is intended to support.

## Purpose

The Command Mode Main Quest experience is meant to act as a focused quest interface inside the existing `Cmd` tab.

It is intended to feel:

- immersive
- premium
- mobile-readable
- guided
- developmental rather than game-mechanical

It is not intended to feel like:

- a long article
- a generic accordion list
- a fake RPG unlock system
- a disconnected side page

The Main Quest screen is the narrative hub.
The Perk Tree screen is the progression hub.

## Core Intent

The Main Quest system is designed to do four jobs at once:

1. Give the user a strong identity-level quest artifact.
2. Break that quest into readable embodied layers.
3. Show a developmental path through a Perk Tree without pretending unlock logic exists yet.
4. Keep the whole experience lightweight enough to scale to all purpose gate.line entries.

## Current User Experience

In Command Mode:

- the Main Quest hero/header is always visible
- lower layers are collapsed by default
- only one lower layer can be open at a time
- opening a layer sets it as the active layer
- closing the active layer clears active state
- clicking the hero collapses all lower sections
- the Perk Tree gateway opens the dedicated Perk Tree screen

This was intentional so the experience feels like:

- "here is your quest"
- "open deeper layers when ready"

rather than a fully expanded content dump.

## Main Quest Layer Roles

The current Command Mode Main Quest preserves these roles:

- `Quest Brief`: orientation and mission
- `Field Briefing`: pattern recognition and recognition trigger
- `Assets & Friction`: gift, drift, and confrontation mechanics
- `Grounding Effect`: embodiment and body-based regulation
- `Unlock Condition`: strongest actionable rule after the header
- `Perk Tree`: progression destination, not duplicated system

These roles matter because each layer must do a different job.
One of the core rules is that no section should restate another section.

## Schema Direction

The current content layer is normalized around:

- `MainQuestContentEntry`
- `MainQuestPerkTree`
- `MainQuestLayerId`

There is also a compatibility alias:

- `MainQuestSeed = MainQuestContentEntry`

That alias exists only to avoid breaking older references while the app transitions fully to the normalized naming.

## Why Content And Presentation Are Separated

We intentionally separated core content from UI presentation metadata.

Content owns things like:

- quest meaning
- prompts
- collapsed previews
- field briefing content
- friction signals
- grounding actions
- perk linkage

Presentation config owns things like:

- section titles
- tones
- image paths
- accent names
- emphasis flags

This separation matters because the content needs to scale to all gate.line entries without dragging UI concerns into the data model.

## Current Content Rules

The implementation includes a rules block in the content layer to preserve the intended quality bar.

Those rules exist because Main Quest content should not become generic or repetitive as the library grows.

Current rules:

- no section should restate another section
- collapsed previews should signal the layer, not summarize everything
- Unlock Condition is the strongest section after the header
- perks must describe real capacities, not vague emotional moods
- if content could fit multiple gate.lines, it fails specificity
- body-based grounding is required
- behavioral drift is required
- Perk Tree is developmental, not real unlock tracking

## Gate 59 Integration

We integrated Gate 59 into the Command Mode system using the content provided in:

- `D:\Projects\luckify-me\Content\purpose\App integration`

That integration pack supplied:

- six Gate 59 line entries
- six linked perk tree seeds

The app now has Gate 59 line coverage for:

- `59.1`
- `59.2`
- `59.3`
- `59.4`
- `59.5`
- `59.6`

## Important Naming Decision

The integration pack had line titles such as:

- `Controlled Entry / Testing the Waters`
- `Natural Attraction / Effortless Pull`

But the active Main Quest names are now intentionally sourced from the canonical schema master file:

- `D:\Projects\luckify-me\Content\purpose\Schema\command_mode_purpose_master.csv`

Specifically, the hero title / active Main Quest name now follows the matching `primary_header` for the active gate.line.

For Gate 59 this means:

- `59.1` → `Bold Intimacy`
- `59.2` → `Transformative Connection`
- `59.3` → `Playful Bonding`
- `59.4` → `Trusted Openness`
- `59.5` → `Unifying Influence`
- `59.6` → `Free Intimacy`

This decision was made because the schema master should be the naming source of truth.
The app-integration file is treated as a detailed content source, not the naming authority.

## Why Gate 59 Was Mapped Into The Existing Schema

The Gate 59 app integration document used a simpler content shape than the current app runtime.

Instead of replacing the live schema, we mapped the Gate 59 pack into the normalized app schema.

That allowed us to preserve:

- the existing UI
- the existing active-layer behavior
- the current Perk Tree screen
- the current collapsed/expanded flow

while still bringing the Gate 59 content in cleanly.

## Extra Fields Added For Richer Integration

To hold the integration-pack structure without losing meaning, `MainQuestContentEntry` now supports optional richer fields:

- `gateLine`
- `fieldBriefing`
- `assetsAndFriction`
- `groundingProtocol`
- `driftPattern`

These fields allow the content layer to preserve more structured quest meaning while still supporting the current screen layout.

## Perk Tree Intent

The Perk Tree is intentionally framed as developmental.

It currently uses only:

- `Core`
- `Emerging`
- `Mastery`

It does not currently pretend to support:

- unlock tracking
- XP
- levels
- persistence

This was intentional because the product is not ready for backend progression logic yet, but it still benefits from a progression-shaped visualization.

## Perk Tree Gateway Intent

The Main Quest screen no longer duplicates the full perk UI.
Instead, it uses a lightweight Perk Tree gateway card.

That was done to keep:

- Main Quest = meaning / pattern / embodiment
- Perk Tree = progression destination

This reduces duplication and keeps the Main Quest screen from turning into a dense system page.

## Command Mode Registry Direction

The Command Mode system now includes:

- `COMMAND_MODE_MAIN_QUEST_ENTRIES`
- `COMMAND_MODE_PERK_TREES`
- `getCommandModeMainQuestEntry(gate, line)`
- `getCommandModeMainQuestEntryById(id)`
- `getCommandModePerkTree(entry)`

This was added so Command Mode is no longer structurally tied to one hardcoded `59.2` content object.

## Current Command Mode Resolution

The `Cmd` tab now resolves the active Main Quest entry from the current profile’s purpose gate.line and passes that entry into the Command Mode Main Quest component.

This means Command Mode now follows the active purpose line for the currently integrated content set.

Right now, Gate 59 is the integrated set in this system.

## Why The Hero Is Always Open

The Main Quest hero is intentionally always visible because it is the quest artifact.

It is the anchor for:

- identity
- framing
- emotional priority
- orientation

The lower cards are optional layers of depth.
The hero is not.

## Why The Hero Can Collapse All Lower Layers

Clicking the hero collapses the lower layers because the hero functions like a "return to base state" interaction.

That was intentional to support:

- fast reset
- reduced mobile fatigue
- a cleaner re-entry point

It lets the user get back to the quest artifact without manually closing multiple rows.

## Why Active Layer State Exists

The active layer behavior was added so the interface feels less like an accordion list and more like a live quest console.

When a layer is active:

- border emphasis changes
- section tone responds subtly
- icon treatment strengthens
- header can respond with a faint accent shift

This was done to make each opened layer feel entered, not merely expanded.

## Asset / Image Integration

Section header images were added for:

- Quest Brief
- Field Briefing
- Assets & Friction
- Grounding Effect
- Unlock Condition
- Perk Tree

These are treated as system thumbnails, not decorative posters.
They help each layer feel distinct while keeping the screen compact and scannable.

## Perk Tree Canvas Notes

The Perk Tree canvas went through several layout fixes because a tree diagram is not a normal flexbox layout problem.

The current implementation uses:

- a controlled centered tree frame
- measured node anchors
- SVG connectors drawn from actual node geometry

This was done so the root, branches, and mastery node feel mathematically centered instead of visually skewed.

## Dedicated Tree Background Motif

A dedicated perk tree background motif was added behind the tree canvas only.

This was done so:

- the tree feels more like a contained quest artifact
- the background supports the diagram
- the detail panel and page background stay unaffected

The motif sits behind the tree frame, not behind the whole screen.

## What Still Needs To Happen

The system is more scalable now, but it is not fully complete for all 384 entries yet.

Remaining likely next steps:

- source all primary headers from the schema master in a generalized way, not only Gate 59
- add more gate.line entries into the Command Mode registry
- add multi-gate perk tree coverage
- formalize special-case override support for rare line behaviors
- optionally rename remaining compatibility types/constants to the final schema names

## Special-Case Strategy

Special-case line behavior is not fully implemented yet.

The clean path for that is to keep the normalized schema stable and add optional override fields instead of branching inside components.

That would support things like:

- title exceptions
- alternate prompts
- alternate perk naming
- rare line-specific handling

without breaking the common model.

## Files Most Relevant To This System

Core content:

- [src/content/commandModeMainQuest.ts](/d:/Projects/luckify-me/luckify-me/src/content/commandModeMainQuest.ts)

Main Quest UI:

- [src/components/CommandModeMainQuest.jsx](/d:/Projects/luckify-me/luckify-me/src/components/CommandModeMainQuest.jsx)

Perk Tree UI:

- [src/components/PerkTreeScreen.jsx](/d:/Projects/luckify-me/luckify-me/src/components/PerkTreeScreen.jsx)

Command Mode host view:

- [src/components/ProfileDisplay.jsx](/d:/Projects/luckify-me/luckify-me/src/components/ProfileDisplay.jsx)

Schema naming source:

- `D:\Projects\luckify-me\Content\purpose\Schema\command_mode_purpose_master.csv`

Gate 59 integration source:

- `D:\Projects\luckify-me\Content\purpose\App integration\Gate_59_Main_Quest_App_Integration (1).docx`

## Summary

The Main Quest Command Mode system is now a structured, schema-driven quest layer that prioritizes:

- strong narrative framing
- embodied guidance
- clear progression direction
- separation of content and presentation
- future scaling to all gate.line entries

The guiding intention behind all of this work has been:

- make the experience feel alive
- keep it grounded
- preserve premium restraint
- avoid fake progression
- and build a content system strong enough to scale cleanly.
