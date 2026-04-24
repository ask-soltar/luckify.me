export type MainQuestLayerId =
  | 'quest-brief'
  | 'field-briefing'
  | 'assets-friction'
  | 'grounding-effect'
  | 'unlock-condition'
  | 'mini-perk-preview';

export type DevelopmentalState = 'Core' | 'Emerging' | 'Mastery';

export type MainQuestCollapsedPreviews = {
  questBrief: string;
  fieldBriefing: string;
  assetsFriction: string;
  groundingEffect: string;
  unlockCondition: string;
  perkTree: string;
};

export type MainQuestLivePrompts = {
  questBrief: string;
  fieldBriefing: string;
  assetsFriction: string;
  groundingEffect: string;
  unlockCondition: string;
};

export type MainQuestFieldBriefing = {
  whatThisQuestIsAbout: string;
  primaryRecognitionTrigger: string;
  whyThisMattersNow: string;
};

export type MainQuestAssetsAndFriction = {
  questAssets: string[];
  questTrap: string;
  frictionSignals: string[];
};

export type MainQuestContentEntry = {
  id: string;
  sphere: 'Purpose';
  gate: number;
  line: number;
  worldLabel: 'ACTIVE QUEST';
  mainQuest: string;
  sourceLine: string;
  questState: string;
  atmosphericSubtitle: string;
  questBrief: string;
  fieldPrompt: string;
  whatThisQuestIsAbout: string;
  questArena: string;
  naturalPower: string;
  questTrap: string;
  behavioralTells: string[];
  groundingEffect: string;
  supportsSunExpression: string;
  somaticAnchor: string;
  questKey: string;
  embodiedSignal: string;
  ritualPrompt: string;
  alignmentReminder: string;
  collapsedPreviews: MainQuestCollapsedPreviews;
  livePrompts: MainQuestLivePrompts;
  perkTreeId: string;
  gateLine?: string;
  fieldBriefing?: MainQuestFieldBriefing;
  assetsAndFriction?: MainQuestAssetsAndFriction;
  groundingProtocol?: string[];
  driftPattern?: string[];
  heroImage?: {
    alt: string;
  };
  deep?: {
    understand_about: string;
    understand_arena: string;
    strength_power: string;
    strength_trap: string;
    grounding_mechanic: string;
    alignment_key: string;
    alignment_signal: string;
  };
};

// Intentional compatibility alias while the app transitions to the V2.3/V2.4 content name.
export type MainQuestSeed = MainQuestContentEntry;

export type PerkBranch = 'Awareness' | 'Embodiment' | 'Field';

export type PerkTreeNodeBase = {
  id: string;
  name: string;
  shortLabel: string;
  type: 'Root' | 'Perk' | 'Mastery';
  state: DevelopmentalState;
  description: string;
  effect: string;
};

export type RootPerkNode = PerkTreeNodeBase & {
  type: 'Root';
  state: 'Core';
  pathRole: string;
  developmentNote: string;
};

export type BranchPerkNode = PerkTreeNodeBase & {
  type: 'Perk';
  state: 'Emerging';
  branch: PerkBranch;
  developmentCue: string;
  masteryMarker: string;
};

export type MasteryPerkNode = PerkTreeNodeBase & {
  type: 'Mastery';
  state: 'Mastery';
  integrationPath: string;
  masteryMarker: string;
};

export type MainQuestPerkTree = {
  id: string;
  mainQuestId: string;
  mainQuestName: string;
  sourceLine: string;
  questState: string;
  subtitle: string;
  progress: {
    title: string;
    items: string[];
  };
  rootNode: RootPerkNode;
  branchNodes: BranchPerkNode[];
  masteryNode: MasteryPerkNode;
};

export type CommandModeLayerPresentation = {
  title: string;
  tone: 'violet' | 'indigo' | 'steel' | 'earth' | 'ember';
  imagePath: string;
  accent: 'indigo' | 'signal' | 'violet' | 'teal' | 'amber' | 'cosmic';
  emphasis?: 'climax';
};

export type CommandModeQuestCardBlock = {
  label: string;
  body: string;
  kind?: 'body' | 'primary' | 'prompt' | 'threshold' | 'reminder';
};

export type CommandModeQuestCardModel = {
  id: MainQuestLayerId;
  title: string;
  tone: 'violet' | 'indigo' | 'steel' | 'earth' | 'ember';
  imagePath: string;
  preview: string;
  livePrompt?: string;
  blocks?: CommandModeQuestCardBlock[];
  chips?: string[];
  summary?: string;
  summaryRows?: string[];
  footer?: string;
  emphasis?: 'climax';
};

export type CommandModeMainQuestModel = {
  id: string;
  sectionLabel: string;
  hero: {
    worldLabel: string;
    mainQuest: string;
    sourceLine: string;
    questState: string;
    atmosphericSubtitle: string;
  };
  cards: CommandModeQuestCardModel[];
};

type GateLineIntegrationSeed = {
  gate: number;
  line: number;
  gateLine: string;
  title: string;
  collapsedPreview: string;
  fieldBriefing: MainQuestFieldBriefing;
  questKey: string;
  assetsAndFriction: MainQuestAssetsAndFriction;
  groundingProtocol: string[];
  driftPattern: string[];
};

type GateLinePerkSeed = {
  gate: number;
  line: number;
  gateLine: string;
  core: string;
  emerging: string;
  mastery: string;
};

const COMMAND_MODE_SCHEMA_PRIMARY_HEADERS: Record<string, string> = {
  '59.1': 'Bold Intimacy',
  '59.2': 'Transformative Connection',
  '59.3': 'Playful Bonding',
  '59.4': 'Trusted Openness',
  '59.5': 'Unifying Influence',
  '59.6': 'Free Intimacy',
};

// Production schema rules for Main Quest V2.3/V2.4:
// - no section should restate another section
// - collapsed previews should signal the layer, not summarize the full content
// - Unlock Condition is the most important layer after the header
// - perks describe real capacities, not vague emotional states
// - if content could apply to multiple gate.lines, it fails specificity
// - body-based grounding is required
// - behavioral drift is required
// - Perk Tree is developmental, not real unlock tracking
export const MAIN_QUEST_IMMERSION_RULES_V23 = {
  avoidSectionRestatement: true,
  collapsedPreviewsAreSignals: true,
  unlockConditionIsPrimarySecondaryLayer: true,
  perksMustBeConcreteCapabilities: true,
  gateLineSpecificityRequired: true,
  bodyGroundingRequired: true,
  behavioralDriftRequired: true,
  perkTreeIsDevelopmentalOnly: true,
} as const;

const DEFAULT_LIVE_PROMPTS: MainQuestLivePrompts = {
  questBrief: 'Feel for this: where is something real trying to happen?',
  fieldBriefing: 'Notice: where does connection stay warm but unchanged?',
  assetsFriction: 'Watch for: closeness without entry.',
  groundingEffect: 'Body check: do you feel softer or more braced?',
  unlockCondition: 'Try now: make the contact one degree more honest.',
};

export const gate59MainQuestContent: GateLineIntegrationSeed[] = [
  {
    gate: 59,
    line: 1,
    gateLine: '59.1',
    title: 'Controlled Entry / Testing the Waters',
    collapsedPreview: 'You get close enough to feel it, but stop right before you’re seen.',
    fieldBriefing: {
      whatThisQuestIsAbout:
        'You approach connection by reading the space first. You move in slowly, adjusting distance, watching for permission before fully entering. The moment is delicate—too early breaks it, too late loses it.',
      primaryRecognitionTrigger:
        'You get close enough to feel it, but stop right before you’re seen.',
      whyThisMattersNow:
        'This is where connection either opens or never starts.',
    },
    questKey:
      'Step forward once → hold position without adjusting → commit only after a real response, not imagined feedback',
    assetsAndFriction: {
      questAssets: ['signal sensitivity', 'controlled entry', 'boundary awareness'],
      questTrap: 'You keep calibrating until the moment dies.',
      frictionSignals: [
        'waiting for perfect signals',
        'adjusting instead of entering',
        'hesitation disguised as timing',
      ],
    },
    groundingProtocol: [
      'slow breath into chest',
      'release tension in jaw',
      'hold body still instead of micro-adjusting',
    ],
    driftPattern: [
      'hovering at the edge of connection',
      'missing entry windows entirely',
    ],
  },
  {
    gate: 59,
    line: 2,
    gateLine: '59.2',
    title: 'Natural Attraction / Effortless Pull',
    collapsedPreview: 'You let it get close, but not close enough to matter.',
    fieldBriefing: {
      whatThisQuestIsAbout:
        'Connection happens instantly. There’s no buildup—just an opening that either gets taken or lost. The body relaxes into it before the mind interferes.',
      primaryRecognitionTrigger:
        'You let it get close, but not close enough to matter.',
      whyThisMattersNow:
        'This only works when you trust what’s already happening.',
    },
    questKey:
      'Feel the opening → act within the first impulse → do not add effort or delay',
    assetsAndFriction: {
      questAssets: ['natural attraction', 'immediate rapport', 'effortless bonding'],
      questTrap: 'You question it the second it works.',
      frictionSignals: [
        'overthinking a clean moment',
        'trying to control what was natural',
        'pulling back after initial connection',
      ],
    },
    groundingProtocol: [
      'drop breath into belly',
      'soften shoulders',
      'reduce unnecessary movement',
    ],
    driftPattern: [
      'interrupting natural connection',
      'replacing ease with control',
    ],
  },
  {
    gate: 59,
    line: 3,
    gateLine: '59.3',
    title: 'Trial and Error / Unstable Bonding',
    collapsedPreview: 'You let it get real, then break it before it settles.',
    fieldBriefing: {
      whatThisQuestIsAbout:
        'Connection is unstable here. It forms fast, breaks fast, and repeats until something actually lands. You push into closeness, then hit friction and pull out.',
      primaryRecognitionTrigger:
        'You let it get real, then break it before it settles.',
      whyThisMattersNow:
        'The pattern only improves if the break is studied—not repeated.',
    },
    questKey:
      'Enter fully → stay through the first friction → only exit after observing what actually failed',
    assetsAndFriction: {
      questAssets: ['fast adaptation', 'experiential learning', 'resilience in connection'],
      questTrap: 'You restart instead of refining.',
      frictionSignals: [
        'repeating the same entry mistakes',
        'mistaking intensity for depth',
        'abandoning too early',
      ],
    },
    groundingProtocol: [
      'stabilize spine',
      'slow breath after impact moments',
      'keep shoulders relaxed under tension',
    ],
    driftPattern: [
      'cycling through connections without learning',
      'breaking connection at the first discomfort',
    ],
  },
  {
    gate: 59,
    line: 4,
    gateLine: '59.4',
    title: 'Influence / External Connection Networks',
    collapsedPreview: 'You keep it social enough to avoid being truly known.',
    fieldBriefing: {
      whatThisQuestIsAbout:
        'Connection doesn’t come directly—it moves through people. You gain access through relationships, not force. The entry point is indirect.',
      primaryRecognitionTrigger:
        'You keep it social enough to avoid being truly known.',
      whyThisMattersNow:
        'Direct attempts fail here. The path is always through others.',
    },
    questKey:
      'Engage through a trusted connection → build presence without pushing → enter only when invited forward',
    assetsAndFriction: {
      questAssets: ['network leverage', 'social influence', 'relational awareness'],
      questTrap: 'You stay in the circle but never step into the center.',
      frictionSignals: [
        'hiding in group dynamics',
        'avoiding direct vulnerability',
        'confusing access with connection',
      ],
    },
    groundingProtocol: [
      'expand breath across chest',
      'keep posture open',
      'hold steady eye contact when engaging directly',
    ],
    driftPattern: [
      'maintaining surface-level relationships',
      'avoiding deeper entry',
    ],
  },
  {
    gate: 59,
    line: 5,
    gateLine: '59.5',
    title: 'Projection / Universal Attraction',
    collapsedPreview: 'You let them believe it, just long enough to stay.',
    fieldBriefing: {
      whatThisQuestIsAbout:
        'People project onto you. They see what they want, and it pulls them in. The connection starts before truth is established.',
      primaryRecognitionTrigger:
        'You let them believe it, just long enough to stay.',
      whyThisMattersNow:
        'Uncorrected projection turns into entanglement.',
    },
    questKey:
      'Notice projection early → correct it directly → disengage if reality is rejected',
    assetsAndFriction: {
      questAssets: ['strong attraction field', 'influence over perception', 'unifying presence'],
      questTrap: 'You carry expectations that were never yours.',
      frictionSignals: [
        'letting misalignment continue',
        'avoiding confrontation',
        'becoming what’s expected',
      ],
    },
    groundingProtocol: [
      'anchor breath in belly',
      'stabilize stance',
      'speak without softening the message',
    ],
    driftPattern: [
      'losing identity in connection',
      'maintaining false alignment',
    ],
  },
  {
    gate: 59,
    line: 6,
    gateLine: '59.6',
    title: 'Withdrawal / Selective Intimacy',
    collapsedPreview: 'You keep it distant enough to never have to risk it.',
    fieldBriefing: {
      whatThisQuestIsAbout:
        'Connection is filtered heavily. You observe first, engage later—if at all. Distance becomes control.',
      primaryRecognitionTrigger:
        'You keep it distant enough to never have to risk it.',
      whyThisMattersNow:
        'Too much filtering blocks connection entirely.',
    },
    questKey:
      'Hold distance → identify one clear signal of alignment → enter before over-evaluating',
    assetsAndFriction: {
      questAssets: ['high discernment', 'selective intimacy', 'clarity in bonding'],
      questTrap: 'You wait until it’s perfect, then it’s gone.',
      frictionSignals: [
        'over-filtering connection',
        'staying in observation mode',
        'avoiding entry altogether',
      ],
    },
    groundingProtocol: [
      'relax back of neck',
      'deepen breath into lower spine',
      'release chest tension',
    ],
    driftPattern: [
      'observing without participating',
      'missing connection windows repeatedly',
    ],
  },
];

export const gate59PerkTrees: GateLinePerkSeed[] = [
  {
    gate: 59,
    line: 1,
    gateLine: '59.1',
    core: 'controlled approach timing',
    emerging: 'reading live response without over-adjusting',
    mastery: 'entering connection cleanly without hesitation',
  },
  {
    gate: 59,
    line: 2,
    gateLine: '59.2',
    core: 'instant connection recognition',
    emerging: 'acting without interference',
    mastery: 'sustaining natural intimacy without disruption',
  },
  {
    gate: 59,
    line: 3,
    gateLine: '59.3',
    core: 'pattern recognition under pressure',
    emerging: 'adjusting behavior mid-connection',
    mastery: 'stabilizing connection through disruption',
  },
  {
    gate: 59,
    line: 4,
    gateLine: '59.4',
    core: 'indirect connection building',
    emerging: 'leveraging trust networks',
    mastery: 'converting access into real connection',
  },
  {
    gate: 59,
    line: 5,
    gateLine: '59.5',
    core: 'projection awareness',
    emerging: 'real-time correction of perception',
    mastery: 'aligning attraction with truth',
  },
  {
    gate: 59,
    line: 6,
    gateLine: '59.6',
    core: 'selective engagement',
    emerging: 'fast alignment detection',
    mastery: 'entering only high-integrity connections without delay',
  },
];

function toTitleCase(value: string): string {
  return value
    .split(' ')
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

function gateLineKey(gate: number, line: number): string {
  return `${gate}.${line}`;
}

function createSourceLine(gate: number, line: number): string {
  return `Purpose · Design Earth · Gene Key ${gate}.${line}`;
}

function createMainQuestId(gate: number, line: number): string {
  return `purpose-${gate}-${line}`;
}

function createPerkTreeId(gate: number, line: number): string {
  return `perk-tree-${gate}-${line}-mvp`;
}

function createCollapsedPreviews(seed: GateLineIntegrationSeed): MainQuestCollapsedPreviews {
  return {
    questBrief: seed.collapsedPreview,
    fieldBriefing: seed.fieldBriefing.primaryRecognitionTrigger,
    assetsFriction: seed.assetsAndFriction.questTrap,
    groundingEffect: seed.groundingProtocol[0] || seed.collapsedPreview,
    unlockCondition: seed.questKey,
    perkTree: 'Explore the capacities developing inside this Main Quest.',
  };
}

function mapIntegrationSeedToEntry(seed: GateLineIntegrationSeed): MainQuestContentEntry {
  const schemaPrimaryHeader =
    COMMAND_MODE_SCHEMA_PRIMARY_HEADERS[seed.gateLine] || seed.title;

  return {
    id: createMainQuestId(seed.gate, seed.line),
    sphere: 'Purpose',
    gate: seed.gate,
    line: seed.line,
    worldLabel: 'ACTIVE QUEST',
    mainQuest: schemaPrimaryHeader,
    sourceLine: createSourceLine(seed.gate, seed.line),
    questState: 'Stirring',
    atmosphericSubtitle: seed.collapsedPreview,
    questBrief: seed.fieldBriefing.whyThisMattersNow,
    fieldPrompt: seed.fieldBriefing.primaryRecognitionTrigger,
    whatThisQuestIsAbout: seed.fieldBriefing.whatThisQuestIsAbout,
    questArena: seed.fieldBriefing.whyThisMattersNow,
    naturalPower: seed.assetsAndFriction.questAssets.join(' · '),
    questTrap: seed.assetsAndFriction.questTrap,
    behavioralTells: seed.assetsAndFriction.frictionSignals,
    groundingEffect: seed.groundingProtocol.join(' · '),
    supportsSunExpression: seed.driftPattern.join(' · '),
    somaticAnchor: seed.groundingProtocol[0] || seed.fieldBriefing.whyThisMattersNow,
    questKey: seed.questKey,
    embodiedSignal: seed.fieldBriefing.primaryRecognitionTrigger,
    ritualPrompt: seed.fieldBriefing.whyThisMattersNow,
    alignmentReminder: seed.driftPattern[0] || seed.assetsAndFriction.questTrap,
    collapsedPreviews: createCollapsedPreviews(seed),
    livePrompts: DEFAULT_LIVE_PROMPTS,
    perkTreeId: createPerkTreeId(seed.gate, seed.line),
    gateLine: seed.gateLine,
    fieldBriefing: seed.fieldBriefing,
    assetsAndFriction: seed.assetsAndFriction,
    groundingProtocol: seed.groundingProtocol,
    driftPattern: seed.driftPattern,
  };
}

function mapPerkSeedToTree(
  perkSeed: GateLinePerkSeed,
  entry: MainQuestContentEntry,
): MainQuestPerkTree {
  const awarenessName = toTitleCase(perkSeed.core);
  const embodimentName = toTitleCase(perkSeed.emerging);
  const fieldName = toTitleCase(entry.assetsAndFriction?.questAssets[0] || 'Field Read');
  const masteryName = toTitleCase(perkSeed.mastery);
  const fieldBriefing = entry.fieldBriefing;
  const frictionSignals = entry.assetsAndFriction?.frictionSignals || [];
  const driftPattern = entry.driftPattern || [];
  const groundingProtocol = entry.groundingProtocol || [];

  return {
    id: createPerkTreeId(perkSeed.gate, perkSeed.line),
    mainQuestId: createMainQuestId(perkSeed.gate, perkSeed.line),
    mainQuestName: entry.mainQuest,
    sourceLine: createSourceLine(perkSeed.gate, perkSeed.line),
    questState: entry.questState,
    subtitle: 'Explore the capacities developing inside your Main Quest.',
    progress: {
      title: 'Quest Path',
      items: ['3 emerging capacities', '1 mastery path'],
    },
    rootNode: {
      id: `root-${perkSeed.gate}-${perkSeed.line}`,
      name: entry.mainQuest,
      shortLabel: entry.mainQuest,
      type: 'Root',
      state: 'Core',
      description: fieldBriefing?.whatThisQuestIsAbout || entry.whatThisQuestIsAbout,
      effect: fieldBriefing?.whyThisMattersNow || entry.questArena,
      pathRole: entry.questKey,
      developmentNote: entry.collapsedPreviews.questBrief,
    },
    branchNodes: [
      {
        id: `perk-awareness-${perkSeed.gate}-${perkSeed.line}`,
        name: awarenessName,
        shortLabel: awarenessName,
        branch: 'Awareness',
        type: 'Perk',
        state: 'Emerging',
        description: perkSeed.core,
        effect: fieldBriefing?.primaryRecognitionTrigger || entry.fieldPrompt,
        developmentCue: frictionSignals[0] || entry.questKey,
        masteryMarker: driftPattern[0] || entry.alignmentReminder,
      },
      {
        id: `perk-embodiment-${perkSeed.gate}-${perkSeed.line}`,
        name: embodimentName,
        shortLabel: embodimentName,
        branch: 'Embodiment',
        type: 'Perk',
        state: 'Emerging',
        description: perkSeed.emerging,
        effect: groundingProtocol.join(' · ') || entry.groundingEffect,
        developmentCue: entry.questKey,
        masteryMarker: groundingProtocol[0] || entry.somaticAnchor,
      },
      {
        id: `perk-field-${perkSeed.gate}-${perkSeed.line}`,
        name: fieldName,
        shortLabel: fieldName,
        branch: 'Field',
        type: 'Perk',
        state: 'Emerging',
        description: entry.assetsAndFriction?.questTrap || entry.questTrap,
        effect: frictionSignals.join(' · ') || entry.supportsSunExpression,
        developmentCue: driftPattern[0] || entry.alignmentReminder,
        masteryMarker: driftPattern[1] || frictionSignals[1] || entry.alignmentReminder,
      },
    ],
    masteryNode: {
      id: `mastery-${perkSeed.gate}-${perkSeed.line}`,
      name: masteryName,
      shortLabel: masteryName,
      type: 'Mastery',
      state: 'Mastery',
      description: perkSeed.mastery,
      effect: fieldBriefing?.whyThisMattersNow || entry.questArena,
      integrationPath: entry.questKey,
      masteryMarker: groundingProtocol[0] || entry.somaticAnchor,
    },
  };
}

export const COMMAND_MODE_MAIN_QUEST_ENTRIES: MainQuestContentEntry[] = gate59MainQuestContent.map(
  mapIntegrationSeedToEntry,
);

const COMMAND_MODE_MAIN_QUEST_ENTRY_MAP_BY_GATE_LINE = new Map(
  COMMAND_MODE_MAIN_QUEST_ENTRIES.map((entry) => [gateLineKey(entry.gate, entry.line), entry]),
);

const COMMAND_MODE_MAIN_QUEST_ENTRY_MAP_BY_ID = new Map(
  COMMAND_MODE_MAIN_QUEST_ENTRIES.map((entry) => [entry.id, entry]),
);

export const mainQuest592Seed: MainQuestContentEntry =
  COMMAND_MODE_MAIN_QUEST_ENTRY_MAP_BY_GATE_LINE.get('59.2') || COMMAND_MODE_MAIN_QUEST_ENTRIES[0];

export const COMMAND_MODE_PERK_TREES: Record<string, MainQuestPerkTree> = Object.fromEntries(
  gate59PerkTrees.map((perkSeed) => {
    const entry = COMMAND_MODE_MAIN_QUEST_ENTRY_MAP_BY_GATE_LINE.get(gateLineKey(perkSeed.gate, perkSeed.line))
      || mainQuest592Seed;
    const tree = mapPerkSeedToTree(perkSeed, entry);
    return [tree.id, tree];
  }),
);

export const perkTree592Mvp: MainQuestPerkTree =
  COMMAND_MODE_PERK_TREES[createPerkTreeId(59, 2)];

export const COMMAND_MODE_LAYER_PRESENTATION: Record<MainQuestLayerId, CommandModeLayerPresentation> = {
  'quest-brief': {
    title: 'Quest Brief',
    tone: 'violet',
    imagePath: '/questbrief.png',
    accent: 'indigo',
  },
  'field-briefing': {
    title: 'Field Briefing',
    tone: 'indigo',
    imagePath: '/fieldbrief.png',
    accent: 'signal',
  },
  'assets-friction': {
    title: 'Assets & Friction',
    tone: 'steel',
    imagePath: '/assetsandfriction.png',
    accent: 'violet',
  },
  'grounding-effect': {
    title: 'Grounding Effect',
    tone: 'earth',
    imagePath: '/groundingeffect.png',
    accent: 'teal',
  },
  'unlock-condition': {
    title: 'Unlock Condition',
    tone: 'ember',
    imagePath: '/unlockcondition.png',
    accent: 'amber',
    emphasis: 'climax',
  },
  'mini-perk-preview': {
    title: 'Perk Tree',
    tone: 'violet',
    imagePath: '/perktree-card.png',
    accent: 'cosmic',
  },
};

export function getCommandModeMainQuestEntry(gate?: number | null, line?: number | null): MainQuestContentEntry | null {
  if (!Number.isFinite(gate) || !Number.isFinite(line)) return null;
  return COMMAND_MODE_MAIN_QUEST_ENTRY_MAP_BY_GATE_LINE.get(gateLineKey(gate, line)) || null;
}

export function getCommandModeMainQuestEntryById(id?: string | null): MainQuestContentEntry | null {
  if (!id) return null;
  return COMMAND_MODE_MAIN_QUEST_ENTRY_MAP_BY_ID.get(id) || null;
}

export function buildPerkGatewayRows(perkTree: MainQuestPerkTree): string[] {
  return [
    ...perkTree.branchNodes.map((node) => `${node.branch} · ${node.name}`),
    `Mastery · ${perkTree.masteryNode.name}`,
  ];
}

export function buildPerkGatewaySummary(perkTree: MainQuestPerkTree): string {
  return perkTree.subtitle || 'Explore the capacities developing inside this Main Quest.';
}

export function getCommandModePerkTree(
  entry: MainQuestContentEntry,
  perkTrees: Record<string, MainQuestPerkTree> = COMMAND_MODE_PERK_TREES,
): MainQuestPerkTree {
  return perkTrees[entry.perkTreeId] || perkTree592Mvp;
}

function buildQuestBriefBlocks(seed: MainQuestContentEntry): CommandModeQuestCardBlock[] {
  return [
    { label: 'Mission', body: seed.questBrief, kind: 'primary' },
    { label: 'Field Prompt', body: seed.fieldPrompt, kind: 'prompt' },
  ];
}

function buildFieldBriefingBlocks(seed: MainQuestContentEntry): CommandModeQuestCardBlock[] {
  if (seed.fieldBriefing) {
    return [
      {
        label: 'What This Quest Is About',
        body: seed.fieldBriefing.whatThisQuestIsAbout,
        kind: 'primary',
      },
      {
        label: 'Why This Matters Now',
        body: seed.fieldBriefing.whyThisMattersNow,
      },
      {
        label: 'Recognition Trigger',
        body: seed.fieldBriefing.primaryRecognitionTrigger,
        kind: 'threshold',
      },
    ];
  }

  return [
    { label: 'What This Quest Is About', body: seed.whatThisQuestIsAbout, kind: 'primary' },
    { label: 'Quest Arena', body: seed.questArena },
  ];
}

function buildAssetsAndFrictionBlocks(seed: MainQuestContentEntry): CommandModeQuestCardBlock[] {
  if (seed.assetsAndFriction) {
    return [
      { label: 'Quest Trap', body: seed.assetsAndFriction.questTrap, kind: 'primary' },
      { label: 'Quest Assets', body: seed.assetsAndFriction.questAssets.join(' · ') },
    ];
  }

  return [
    { label: 'Natural Power', body: seed.naturalPower, kind: 'primary' },
    { label: 'Quest Trap', body: seed.questTrap },
  ];
}

function buildAssetsAndFrictionChips(seed: MainQuestContentEntry): string[] {
  if (seed.assetsAndFriction) {
    return [...seed.assetsAndFriction.frictionSignals, ...(seed.driftPattern || [])];
  }

  return seed.behavioralTells;
}

function buildGroundingBlocks(seed: MainQuestContentEntry): CommandModeQuestCardBlock[] {
  if (seed.groundingProtocol?.length || seed.driftPattern?.length) {
    return [
      {
        label: 'Grounding Protocol',
        body: (seed.groundingProtocol || []).join(' · '),
        kind: 'primary',
      },
      {
        label: 'Drift Pattern',
        body: (seed.driftPattern || []).join(' · '),
      },
    ];
  }

  return [
    { label: 'Grounding Effect', body: seed.groundingEffect, kind: 'primary' },
    { label: 'Supports Sun Expression', body: seed.supportsSunExpression },
    { label: 'Somatic Anchor', body: seed.somaticAnchor },
  ];
}

export function buildCommandModeMainQuestModel(
  seed: MainQuestContentEntry = mainQuest592Seed,
  perkTree: MainQuestPerkTree = getCommandModePerkTree(mainQuest592Seed),
): CommandModeMainQuestModel {
  const questBriefPresentation = COMMAND_MODE_LAYER_PRESENTATION['quest-brief'];
  const fieldBriefingPresentation = COMMAND_MODE_LAYER_PRESENTATION['field-briefing'];
  const assetsFrictionPresentation = COMMAND_MODE_LAYER_PRESENTATION['assets-friction'];
  const groundingEffectPresentation = COMMAND_MODE_LAYER_PRESENTATION['grounding-effect'];
  const unlockConditionPresentation = COMMAND_MODE_LAYER_PRESENTATION['unlock-condition'];
  const perkTreePresentation = COMMAND_MODE_LAYER_PRESENTATION['mini-perk-preview'];

  return {
    id: seed.id,
    sectionLabel: 'Main Quest',
    hero: {
      worldLabel: seed.worldLabel,
      mainQuest: seed.mainQuest,
      sourceLine: seed.sourceLine,
      questState: seed.questState,
      atmosphericSubtitle: seed.atmosphericSubtitle,
    },
    cards: [
      {
        id: 'quest-brief',
        title: questBriefPresentation.title,
        tone: questBriefPresentation.tone,
        imagePath: questBriefPresentation.imagePath,
        preview: seed.collapsedPreviews.questBrief,
        livePrompt: seed.livePrompts.questBrief,
        blocks: buildQuestBriefBlocks(seed),
      },
      {
        id: 'field-briefing',
        title: fieldBriefingPresentation.title,
        tone: fieldBriefingPresentation.tone,
        imagePath: fieldBriefingPresentation.imagePath,
        preview: seed.collapsedPreviews.fieldBriefing,
        livePrompt: seed.livePrompts.fieldBriefing,
        blocks: buildFieldBriefingBlocks(seed),
      },
      {
        id: 'assets-friction',
        title: assetsFrictionPresentation.title,
        tone: assetsFrictionPresentation.tone,
        imagePath: assetsFrictionPresentation.imagePath,
        preview: seed.collapsedPreviews.assetsFriction,
        livePrompt: seed.livePrompts.assetsFriction,
        blocks: buildAssetsAndFrictionBlocks(seed),
        chips: buildAssetsAndFrictionChips(seed),
      },
      {
        id: 'grounding-effect',
        title: groundingEffectPresentation.title,
        tone: groundingEffectPresentation.tone,
        imagePath: groundingEffectPresentation.imagePath,
        preview: seed.collapsedPreviews.groundingEffect,
        livePrompt: seed.livePrompts.groundingEffect,
        blocks: buildGroundingBlocks(seed),
      },
      {
        id: 'unlock-condition',
        title: unlockConditionPresentation.title,
        tone: unlockConditionPresentation.tone,
        imagePath: unlockConditionPresentation.imagePath,
        emphasis: unlockConditionPresentation.emphasis,
        preview: seed.collapsedPreviews.unlockCondition,
        livePrompt: seed.livePrompts.unlockCondition,
        blocks: [
          { label: 'Quest Key', body: seed.questKey, kind: 'threshold' },
          { label: 'Embodied Signal', body: seed.embodiedSignal },
          { label: 'Ritual Prompt', body: seed.ritualPrompt, kind: 'prompt' },
          { label: 'Alignment Reminder', body: seed.alignmentReminder, kind: 'reminder' },
        ],
      },
      {
        id: 'mini-perk-preview',
        title: perkTreePresentation.title,
        tone: perkTreePresentation.tone,
        imagePath: perkTreePresentation.imagePath,
        preview: seed.collapsedPreviews.perkTree,
        summary: buildPerkGatewaySummary(perkTree),
        summaryRows: buildPerkGatewayRows(perkTree),
        footer: 'Open Perk Tree',
      },
    ],
  };
}
