import mainQuestRows from './mainQuestData.json';

export type MainQuestEntry = {
  id: string
  sphere: "Purpose"
  gate: number
  line: number

  mainQuest: string
  questBrief: string
  whatThisQuestIsAbout: string
  naturalPower: string
  questTrap: string
  questKey: string
  questArena: string
  embodiedSignal: string
  alignmentReminder: string

  heroImage?: {
    src?: string
    alt: string
  }

  deep?: {
    understand_about?: string
    understand_arena?: string
    strength_power?: string
    strength_trap?: string
    alignment_key?: string
    alignment_signal?: string
  }
}

export type QuestPanelCard = {
  id: string
  label: string
  body: string
  depth: number
  icon?: string
  eyebrow?: string
  collapsible?: boolean
  defaultOpen?: boolean
  revealNextOnCta?: boolean
  ctaLabel?: string
  childDepth?: number
  collapseChildrenOnParentClose?: boolean
  nestedCards?: QuestPanelCard[]
}

export type QuestPanelSection = {
  id: string
  title: string
  depth: number
  icon?: string
  defaultOpen?: boolean
  cards: QuestPanelCard[]
}

export type QuestPanelData = {
  id: string
  eyebrow: string
  title: string
  metadata: string[]
  summary?: string
  introCard?: QuestPanelCard
  sections: QuestPanelSection[]
  reminderCard: QuestPanelCard
}

type MainQuestRow = {
  id: string
  sphere: string
  gate: string
  line: string
  mainQuest: string
  questBrief: string
  whatThisQuestIsAbout: string
  naturalPower: string
  questTrap: string
  questKey: string
  questArena: string
  embodiedSignal: string
  alignmentReminder: string
  heroImageAlt?: string
  deep_understand_about?: string
  deep_understand_arena?: string
  deep_strength_power?: string
  deep_strength_trap?: string
  deep_alignment_key?: string
  deep_alignment_signal?: string
}

function optionalText(value?: string) {
  const normalized = value?.trim();
  return normalized ? normalized : undefined;
}

function mapRowToEntry(row: MainQuestRow): MainQuestEntry {
  return {
    id: row.id,
    sphere: 'Purpose',
    gate: Number(row.gate),
    line: Number(row.line),
    mainQuest: row.mainQuest,
    questBrief: row.questBrief,
    whatThisQuestIsAbout: row.whatThisQuestIsAbout,
    naturalPower: row.naturalPower,
    questTrap: row.questTrap,
    questKey: row.questKey,
    questArena: row.questArena,
    embodiedSignal: row.embodiedSignal,
    alignmentReminder: row.alignmentReminder,
    heroImage: optionalText(row.heroImageAlt)
      ? { alt: row.heroImageAlt!.trim() }
      : undefined,
    deep: {
      understand_about: optionalText(row.deep_understand_about),
      understand_arena: optionalText(row.deep_understand_arena),
      strength_power: optionalText(row.deep_strength_power),
      strength_trap: optionalText(row.deep_strength_trap),
      alignment_key: optionalText(row.deep_alignment_key),
      alignment_signal: optionalText(row.deep_alignment_signal),
    },
  };
}

export const MAIN_QUEST_ENTRIES: MainQuestEntry[] = (mainQuestRows as MainQuestRow[]).map(mapRowToEntry);

const MAIN_QUEST_ENTRY_MAP = new Map(
  MAIN_QUEST_ENTRIES.map(entry => [`${entry.gate}.${entry.line}`, entry])
);

export function getMainQuestEntry(gate?: number | null, line?: number | null): MainQuestEntry | null {
  if (!Number.isFinite(gate) || !Number.isFinite(line)) return null;
  return MAIN_QUEST_ENTRY_MAP.get(`${gate}.${line}`) ?? null;
}

export function buildMainQuestPanel(entry: MainQuestEntry): QuestPanelData {
  function buildDeeperCard(id: string, label: string, body: string, depth: number): QuestPanelCard {
    return {
      id,
      label,
      body,
      depth,
      collapsible: true,
      defaultOpen: false,
      collapseChildrenOnParentClose: true,
    };
  }

  const understandNested = optionalText(entry.deep?.understand_about)
    ? [buildDeeperCard(
        `${entry.id}-understand-core`,
        'At Its Core',
        entry.deep!.understand_about!,
        3
      )]
    : [];

  const naturalPowerNested = optionalText(entry.deep?.strength_power)
    ? [buildDeeperCard(
        `${entry.id}-strength-power-deeper`,
        'Deeper Lens',
        entry.deep!.strength_power!,
        3
      )]
    : [];

  const questTrapNested = optionalText(entry.deep?.strength_trap)
    ? [buildDeeperCard(
        `${entry.id}-strength-trap-deeper`,
        'Deeper Lens',
        entry.deep!.strength_trap!,
        3
      )]
    : [];

  const questKeyNested = optionalText(entry.deep?.alignment_key)
    ? [buildDeeperCard(
        `${entry.id}-alignment-key-deeper`,
        'Deeper Lens',
        entry.deep!.alignment_key!,
        4
      )]
    : [];

  const embodiedSignalNested = optionalText(entry.deep?.alignment_signal)
    ? [buildDeeperCard(
        `${entry.id}-alignment-signal-deeper`,
        'Deeper Lens',
        entry.deep!.alignment_signal!,
        4
      )]
    : [];

  return {
    id: entry.id,
    eyebrow: 'Main Quest',
    title: entry.mainQuest,
    summary: entry.questBrief,
    metadata: [
      entry.sphere,
      'Design Earth',
      `I Ching ${entry.gate}.${entry.line}`,
    ],
    sections: [
      {
        id: `${entry.id}-understand`,
        title: 'Understand',
        depth: 1,
        icon: 'U',
        defaultOpen: true,
        cards: [
          {
            id: `${entry.id}-understand-about`,
            label: 'What This Quest Is About',
            body: entry.whatThisQuestIsAbout,
            depth: 2,
            nestedCards: understandNested,
          },
        ],
      },
      {
        id: `${entry.id}-strengths`,
        title: 'Strengths & Challenges',
        depth: 4,
        icon: 'S',
        cards: [
          {
            id: `${entry.id}-natural-power`,
            label: 'Natural Power',
            body: entry.naturalPower,
            depth: 4,
            nestedCards: naturalPowerNested,
          },
          {
            id: `${entry.id}-quest-trap`,
            label: 'Quest Trap',
            body: entry.questTrap,
            depth: 4,
            nestedCards: questTrapNested,
          },
        ],
      },
      {
        id: `${entry.id}-alignment`,
        title: 'Alignment',
        depth: 4,
        icon: 'A',
        cards: [
          {
            id: `${entry.id}-quest-key`,
            label: 'Quest Key',
            body: entry.questKey,
            depth: 4,
            nestedCards: questKeyNested,
          },
          {
            id: `${entry.id}-embodied-signal`,
            label: 'Embodied Signal',
            body: entry.embodiedSignal,
            depth: 4,
            nestedCards: embodiedSignalNested,
          },
        ],
      },
    ],
    reminderCard: {
      id: `${entry.id}-alignment-reminder`,
      label: 'Alignment Reminder',
      body: entry.alignmentReminder,
      depth: 5,
    },
  };
}

export const mainQuestExample592: MainQuestEntry =
  getMainQuestEntry(59, 2) ?? MAIN_QUEST_ENTRIES[0];
