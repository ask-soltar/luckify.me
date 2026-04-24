import gate1Data from './gates/gate1_main_quest_v2_batch.json';
import gate2Data from './gates/gate2_main_quest_v2_batch.json';
import gate11Data from './gates/gate11_main_quest_v2_batch.json';
import gate34Data from './gates/gate34_main_quest_v2_batch.json';
import gate39Data from './gates/gate39_main_quest_v2_batch.json';
import gate40Data from './gates/gate40_main_quest_v2_batch.json';
import gate41Data from './gates/gate41_main_quest_v2_batch.json';
import gate44Data from './gates/gate44_main_quest_v2_batch.json';

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

export type MainQuestContentEntryV2 = {
  gate: number;
  line: number;
  gateLine: string;
  title: string;
  hero: {
    mainQuest: string;
    sourceLine: string;
    questState: string;
    atmosphericSubtitle: string;
  };
  questBrief: {
    collapsedPreview: string;
    mission: string;
    fieldPrompt: string;
    livePrompt: string;
  };
  fieldBriefing: {
    collapsedPreview: string;
    whatThisQuestIsAbout: string;
    whyThisMattersNow: string;
    primaryRecognitionTrigger: string;
    livePrompt: string;
  };
  assetsAndFriction: {
    collapsedPreview: string;
    questTrap: string;
    questAssets: string[];
    frictionSignals: string[];
    livePrompt: string;
  };
  groundingEffect: {
    collapsedPreview: string;
    groundingProtocol: string[];
    somaticShift: string;
    bodyCheckPrompt: string;
  };
  unlockCondition: {
    collapsedPreview: string;
    questKey: string;
    embodiedSignal: string;
    ritualPrompt: string;
    alignmentReminder: string;
    livePrompt: string;
  };
  driftPattern: string[];
};

export type MainQuestPerkNodeV2 = {
  branch: 'Root' | 'Awareness' | 'Embodiment' | 'Field' | 'Mastery';
  name: string;
  state: 'Core' | 'Emerging' | 'Mastery';
  description: string;
  effect: string;
  developmentCue: string;
  masteryMarker: string;
};

export type MainQuestPerkTreeV2 = {
  id: string;
  mainQuestId: string;
  mainQuestName: string;
  sourceLine: string;
  questState: string;
  subtitle: string;
  nodes: MainQuestPerkNodeV2[];
};

export type MainQuestContentEntry = {
  id: string;
  sphere: 'Purpose';
  gate: number;
  line: number;
  worldLabel: 'MAIN QUEST';
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
  v2?: MainQuestContentEntryV2;
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
  v2Nodes?: MainQuestPerkNodeV2[];
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

export type ContentType = 'identity' | 'behavioral' | 'capability' | 'somatic' | 'instructional';

export type FieldDescriptor = {
  path: string;
  value: string;
  contentType: ContentType;
};

export type DuplicateConflict = {
  contentType: ContentType;
  value: string;
  paths: string[];
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

export const mainQuest592V2: MainQuestContentEntryV2 = {
  gate: 59,
  line: 2,
  gateLine: '59.2',
  title: 'Natural Attraction / Effortless Pull',
  hero: {
    mainQuest: 'Transformative Connection',
    sourceLine: 'Purpose · Design Earth · I Ching 59.2',
    questState: 'Stirring',
    atmosphericSubtitle: 'Connection is already open. The test is not interrupting it.',
  },
  questBrief: {
    collapsedPreview: 'Connection opens before you manage it.',
    mission: 'Let the first clean opening become real contact.',
    fieldPrompt: 'Feel where the connection is already happening before you improve it.',
    livePrompt: 'Where is something real already open?',
  },
  fieldBriefing: {
    collapsedPreview: 'Notice the opening before control enters.',
    whatThisQuestIsAbout:
      'Connection happens instantly. There is no buildup—just an opening that either gets taken or lost. The body relaxes into it before the mind tries to manage the moment.',
    whyThisMattersNow:
      'The opportunity is not created by effort. It is lost when effort interrupts what is already working.',
    primaryRecognitionTrigger:
      'You let it get close, but not close enough to matter.',
    livePrompt: 'Where does connection stay warm but unchanged?',
  },
  assetsAndFriction: {
    collapsedPreview: 'Ease appears first. Interference follows.',
    questTrap: 'You question it the second it works.',
    questAssets: [
      'natural attraction',
      'immediate rapport',
      'effortless bonding',
    ],
    frictionSignals: [
      'overthinking a clean moment',
      'trying to control what was natural',
      'pulling back after initial connection',
    ],
    livePrompt: 'Watch for the moment ease turns into management.',
  },
  groundingEffect: {
    collapsedPreview: 'Drop the effort from your body.',
    groundingProtocol: [
      'drop breath into belly',
      'soften shoulders',
      'reduce unnecessary movement',
    ],
    somaticShift: 'The body stays open without reaching, gripping, or proving.',
    bodyCheckPrompt: 'Do you feel soft enough to stay, or braced enough to manage?',
  },
  unlockCondition: {
    collapsedPreview: 'Act before the mind edits it.',
    questKey: 'Feel the opening → act within the first impulse → do not add effort or delay',
    embodiedSignal: 'The body has already said yes before the mind starts negotiating.',
    ritualPrompt: 'Make one honest contact while the opening is still alive.',
    alignmentReminder: 'Do not turn natural connection into a performance.',
    livePrompt: 'Make the contact one degree more honest.',
  },
  driftPattern: [
    'interrupting natural connection',
    'replacing ease with control',
  ],
};

export const perkTree592V2: MainQuestPerkTreeV2 = {
  id: 'perk-tree-59-2-v2',
  mainQuestId: 'purpose-59-2',
  mainQuestName: 'Transformative Connection',
  sourceLine: 'Purpose · Design Earth · I Ching 59.2',
  questState: 'Stirring',
  subtitle: 'Develop the capacity to recognize, enter, and sustain natural connection.',
  nodes: [
    {
      branch: 'Root',
      name: 'Transformative Connection',
      state: 'Core',
      description: 'This path develops the ability to let connection become real before control interrupts it.',
      effect: 'Natural attraction becomes usable when it is acted on without added effort.',
      developmentCue: 'Notice where the opening already exists.',
      masteryMarker: 'Connection can begin without being managed first.',
    },
    {
      branch: 'Awareness',
      name: 'Instant Connection Recognition',
      state: 'Emerging',
      description: 'You learn to recognize the exact moment connection is already happening.',
      effect: 'Real openings become visible before doubt, analysis, or control takes over.',
      developmentCue: 'Catch the first clean signal of rapport.',
      masteryMarker: 'You can tell the difference between real openness and imagined potential.',
    },
    {
      branch: 'Embodiment',
      name: 'Acting Without Interference',
      state: 'Emerging',
      description: 'The body learns to stay open and move before the mind adds friction.',
      effect: 'Action becomes cleaner because it is not delayed by unnecessary adjustment.',
      developmentCue: 'Let the body respond before the mind edits.',
      masteryMarker: 'You act without tightening, proving, or rehearsing.',
    },
    {
      branch: 'Field',
      name: 'Natural Attraction',
      state: 'Emerging',
      description: 'The relational field opens without force when the moment is not interrupted.',
      effect: 'Connection has room to deepen instead of collapsing back into distance.',
      developmentCue: 'Stop managing the moment once it is already working.',
      masteryMarker: 'The field stays alive because you do not interfere with ease.',
    },
    {
      branch: 'Mastery',
      name: 'Sustaining Natural Intimacy Without Disruption',
      state: 'Mastery',
      description: 'The full path matures into the ability to let closeness continue without sabotage.',
      effect: 'Natural intimacy becomes stable because it is trusted, entered, and sustained.',
      developmentCue: 'Stay with the opening after contact begins.',
      masteryMarker: 'Connection becomes real without needing to be controlled.',
    },
  ],
};

export const mainQuest591V2: MainQuestContentEntryV2 = {
  gate: 59,
  line: 1,
  gateLine: '59.1',
  title: 'Controlled Entry / Testing the Waters',
  hero: {
    mainQuest: 'Bold Intimacy',
    sourceLine: 'Purpose · Design Earth · I Ching 59.1',
    questState: 'Stirring',
    atmosphericSubtitle: 'Intimacy opens when timing becomes entry, not endless calibration.',
  },
  questBrief: {
    collapsedPreview: 'Move closer before calibration kills the moment.',
    mission: 'Enter the opening cleanly once a real response is felt.',
    fieldPrompt: 'Notice where live permission is already present and stop hovering outside it.',
    livePrompt: 'Where is the response already real enough to enter?',
  },
  fieldBriefing: {
    collapsedPreview: 'Track the opening, then stop adjusting.',
    whatThisQuestIsAbout:
      'You approach connection by reading the space first. You move in slowly, adjusting distance and timing until the moment either stabilizes or disappears.',
    whyThisMattersNow:
      'Sensitivity becomes useful only when it ends in entry rather than endless calibration.',
    primaryRecognitionTrigger:
      'You get close enough to feel it, but stop right before you’re seen.',
    livePrompt: 'Where are you still calibrating instead of entering?',
  },
  assetsAndFriction: {
    collapsedPreview: 'Sensitivity helps until it becomes hesitation.',
    questTrap: 'You keep calibrating until the moment dies.',
    questAssets: [
      'signal sensitivity',
      'controlled entry',
      'boundary awareness',
    ],
    frictionSignals: [
      'waiting for perfect signals',
      'adjusting instead of entering',
      'hesitation disguised as timing',
    ],
    livePrompt: 'Catch the moment precision turns into delay.',
  },
  groundingEffect: {
    collapsedPreview: 'Settle the body before you approach.',
    groundingProtocol: [
      'slow breath into chest',
      'release tension in jaw',
      'hold body still instead of micro-adjusting',
    ],
    somaticShift: 'The body can move closer without scattering into hyper-vigilance.',
    bodyCheckPrompt: 'Are you steady enough to enter, or still managing every signal?',
  },
  unlockCondition: {
    collapsedPreview: 'Commit once the response is real.',
    questKey: 'Step forward once → hold position without adjusting → commit only after a real response, not imagined feedback',
    embodiedSignal: 'Your body stays steady after the first move instead of retreating into calculation.',
    ritualPrompt: 'Take one clear step toward contact without adding a second adjustment.',
    alignmentReminder: 'Timing serves intimacy only when it leads to entry.',
    livePrompt: 'Make one clean move before the moment goes cold.',
  },
  driftPattern: [
    'hovering at the edge of connection',
    'missing entry windows entirely',
  ],
};

export const perkTree591V2: MainQuestPerkTreeV2 = {
  id: 'perk-tree-59-1-v2',
  mainQuestId: 'purpose-59-1',
  mainQuestName: 'Bold Intimacy',
  sourceLine: 'Purpose · Design Earth · I Ching 59.1',
  questState: 'Stirring',
  subtitle: 'Develop the capacity to read timing accurately and enter connection without hesitation.',
  nodes: [
    {
      branch: 'Root',
      name: 'Bold Intimacy',
      state: 'Core',
      description: 'This path develops the ability to sense the right opening and move into it cleanly.',
      effect: 'Sensitivity becomes useful when it leads to real entry instead of endless adjustment.',
      developmentCue: 'Feel for the point where timing becomes action.',
      masteryMarker: 'You can step in without needing one more sign.',
    },
    {
      branch: 'Awareness',
      name: 'Controlled Approach Timing',
      state: 'Emerging',
      description: 'You learn to read live signals accurately without mistaking caution for wisdom.',
      effect: 'The body recognizes when permission is present before the moment closes.',
      developmentCue: 'Name the point when the response is already enough.',
      masteryMarker: 'You stop waiting for perfect certainty before moving.',
    },
    {
      branch: 'Embodiment',
      name: 'Reading Live Response Without Over-Adjusting',
      state: 'Emerging',
      description: 'The body stays steady enough to approach without micro-correcting every sensation.',
      effect: 'Movement becomes cleaner because it is not fragmented by constant recalibration.',
      developmentCue: 'Hold one clear position once you enter.',
      masteryMarker: 'You can stay near contact without fidgeting, tightening, or backing off.',
    },
    {
      branch: 'Field',
      name: 'Boundary Awareness',
      state: 'Emerging',
      description: 'The relational field becomes easier to enter because you can feel real thresholds without dramatizing them.',
      effect: 'Connection opens with more trust because entry respects the moment instead of circling around it.',
      developmentCue: 'Cross the threshold when the opening is real.',
      masteryMarker: 'The field responds because you enter directly and stop hovering.',
    },
    {
      branch: 'Mastery',
      name: 'Entering Connection Cleanly Without Hesitation',
      state: 'Mastery',
      description: 'The full path matures into clean entry that is responsive, grounded, and unafraid of being seen.',
      effect: 'Connection begins more reliably because timing and action finally work together.',
      developmentCue: 'Commit once the opening answers you back.',
      masteryMarker: 'Closeness can begin without stalling at the threshold.',
    },
  ],
};

export const mainQuest593V2: MainQuestContentEntryV2 = {
  gate: 59,
  line: 3,
  gateLine: '59.3',
  title: 'Trial and Error / Unstable Bonding',
  hero: {
    mainQuest: 'Playful Bonding',
    sourceLine: 'Purpose · Design Earth · I Ching 59.3',
    questState: 'Stirring',
    atmosphericSubtitle: 'The lesson is staying present long enough to learn from rupture.',
  },
  questBrief: {
    collapsedPreview: 'Stay long enough to learn from the break.',
    mission: 'Let friction teach you instead of forcing a full restart.',
    fieldPrompt: 'Notice where connection destabilizes and remain present long enough to see why.',
    livePrompt: 'What is this disruption trying to teach before you reset it?',
  },
  fieldBriefing: {
    collapsedPreview: 'Track the break instead of restarting.',
    whatThisQuestIsAbout:
      'Connection is unstable here. It forms quickly, breaks quickly, and repeats until something is actually learned in the disruption.',
    whyThisMattersNow:
      'The pattern matures only when rupture becomes information instead of an excuse to bail out.',
    primaryRecognitionTrigger:
      'You let it get real, then break it before it settles.',
    livePrompt: 'Where are you repeating instead of refining?',
  },
  assetsAndFriction: {
    collapsedPreview: 'Adaptation helps when repetition stops.',
    questTrap: 'You restart instead of refining.',
    questAssets: [
      'fast adaptation',
      'experiential learning',
      'resilience in connection',
    ],
    frictionSignals: [
      'repeating the same entry mistakes',
      'mistaking intensity for depth',
      'abandoning too early',
    ],
    livePrompt: 'Catch the instant repair turns into restart.',
  },
  groundingEffect: {
    collapsedPreview: 'Stabilize before reacting to friction.',
    groundingProtocol: [
      'stabilize spine',
      'slow breath after impact moments',
      'keep shoulders relaxed under tension',
    ],
    somaticShift: 'The body can absorb friction without collapsing into impulsive exit.',
    bodyCheckPrompt: 'Are you steady enough to learn here, or already preparing to escape?',
  },
  unlockCondition: {
    collapsedPreview: 'Refine the pattern before you leave.',
    questKey: 'Enter fully → stay through the first friction → only exit after observing what actually failed',
    embodiedSignal: 'You remain present through the first wobble instead of deciding the connection is over.',
    ritualPrompt: 'Name one thing that shifted before choosing whether to continue.',
    alignmentReminder: 'Disruption becomes growth only when it is studied, not dramatized.',
    livePrompt: 'Stay for one more beat after the first break.',
  },
  driftPattern: [
    'cycling through connections without learning',
    'breaking connection at the first discomfort',
  ],
};

export const perkTree593V2: MainQuestPerkTreeV2 = {
  id: 'perk-tree-59-3-v2',
  mainQuestId: 'purpose-59-3',
  mainQuestName: 'Playful Bonding',
  sourceLine: 'Purpose · Design Earth · I Ching 59.3',
  questState: 'Stirring',
  subtitle: 'Develop the capacity to learn from friction and stabilize connection through disruption.',
  nodes: [
    {
      branch: 'Root',
      name: 'Playful Bonding',
      state: 'Core',
      description: 'This path develops the ability to stay engaged when connection becomes unstable.',
      effect: 'Rupture becomes usable because it reveals how connection can be repaired and refined.',
      developmentCue: 'Treat the break as data instead of a verdict.',
      masteryMarker: 'You can remain present long enough to learn what actually happened.',
    },
    {
      branch: 'Awareness',
      name: 'Pattern Recognition Under Pressure',
      state: 'Emerging',
      description: 'You learn to see the repeated fault lines that show up when connection starts to wobble.',
      effect: 'Friction becomes more legible before it turns into another unnecessary exit.',
      developmentCue: 'Spot the recurring pattern inside the disruption.',
      masteryMarker: 'You can tell when the same mistake is trying to repeat itself.',
    },
    {
      branch: 'Embodiment',
      name: 'Adjusting Behavior Mid-Connection',
      state: 'Emerging',
      description: 'The body learns to stay adaptive during contact instead of hardening or fleeing.',
      effect: 'Repair becomes possible because your response can change without losing the connection entirely.',
      developmentCue: 'Stay soft enough to make one better move in real time.',
      masteryMarker: 'You can adapt while the interaction is still alive.',
    },
    {
      branch: 'Field',
      name: 'Resilience In Connection',
      state: 'Emerging',
      description: 'The relational field can hold more instability when you stop treating every rupture as failure.',
      effect: 'Connection lasts longer because experimentation no longer destroys the whole exchange.',
      developmentCue: 'Hold the field steady through the first imperfect moment.',
      masteryMarker: 'The field remains workable even when things get messy.',
    },
    {
      branch: 'Mastery',
      name: 'Stabilizing Connection Through Disruption',
      state: 'Mastery',
      description: 'The full path matures into resilient connection that can survive friction without collapsing.',
      effect: 'Depth becomes possible because interruption no longer automatically ends the process.',
      developmentCue: 'Refine the bond while it is still under stress.',
      masteryMarker: 'Connection can recover instead of resetting from zero.',
    },
  ],
};

export const mainQuest594V2: MainQuestContentEntryV2 = {
  gate: 59,
  line: 4,
  gateLine: '59.4',
  title: 'Influence / External Connection Networks',
  hero: {
    mainQuest: 'Trusted Openness',
    sourceLine: 'Purpose · Design Earth · I Ching 59.4',
    questState: 'Stirring',
    atmosphericSubtitle: 'Connection deepens through trusted pathways, not direct force.',
  },
  questBrief: {
    collapsedPreview: 'Use trust routes that already exist.',
    mission: 'Let access become real relationship instead of staying social and safe.',
    fieldPrompt: 'Notice where trust is already present through the network around you.',
    livePrompt: 'Which doorway into connection is already open through trust?',
  },
  fieldBriefing: {
    collapsedPreview: 'Move through trust, not pressure.',
    whatThisQuestIsAbout:
      'Connection moves indirectly here. Access is created through relationships, context, and trust that already exist around the moment.',
    whyThisMattersNow:
      'Direct force fails because this path opens through credibility and invitation rather than pressure.',
    primaryRecognitionTrigger:
      'You keep it social enough to avoid being truly known.',
    livePrompt: 'Where are you confusing access with actual closeness?',
  },
  assetsAndFriction: {
    collapsedPreview: 'Access means little without true entry.',
    questTrap: 'You stay in the circle but never step into the center.',
    questAssets: [
      'network leverage',
      'social influence',
      'relational awareness',
    ],
    frictionSignals: [
      'hiding in group dynamics',
      'avoiding direct vulnerability',
      'confusing access with connection',
    ],
    livePrompt: 'Notice when social fluency replaces real openness.',
  },
  groundingEffect: {
    collapsedPreview: 'Open the body for direct contact.',
    groundingProtocol: [
      'expand breath across chest',
      'keep posture open',
      'hold steady eye contact when engaging directly',
    ],
    somaticShift: 'The body stays available for closeness instead of disappearing into social performance.',
    bodyCheckPrompt: 'Are you open enough to be met directly, or still buffered by the group?',
  },
  unlockCondition: {
    collapsedPreview: 'Step through the invitation directly.',
    questKey: 'Engage through a trusted connection → build presence without pushing → enter only when invited forward',
    embodiedSignal: 'You remain visible in direct contact instead of retreating into role, network, or context.',
    ritualPrompt: 'Respond to one real invitation with direct presence instead of social deflection.',
    alignmentReminder: 'Trust networks matter only when they lead to genuine openness.',
    livePrompt: 'Take one step from access into actual connection.',
  },
  driftPattern: [
    'maintaining surface-level relationships',
    'avoiding deeper entry',
  ],
};

export const perkTree594V2: MainQuestPerkTreeV2 = {
  id: 'perk-tree-59-4-v2',
  mainQuestId: 'purpose-59-4',
  mainQuestName: 'Trusted Openness',
  sourceLine: 'Purpose · Design Earth · I Ching 59.4',
  questState: 'Stirring',
  subtitle: 'Develop the capacity to convert trusted access into direct, meaningful connection.',
  nodes: [
    {
      branch: 'Root',
      name: 'Trusted Openness',
      state: 'Core',
      description: 'This path develops the ability to move through trust structures without hiding behind them.',
      effect: 'Access becomes meaningful because it is converted into real closeness instead of social safety.',
      developmentCue: 'Follow the trust route all the way into direct contact.',
      masteryMarker: 'You can become personally present after the door opens.',
    },
    {
      branch: 'Awareness',
      name: 'Indirect Connection Building',
      state: 'Emerging',
      description: 'You learn to recognize the relational pathways through which connection naturally opens.',
      effect: 'The right doorway becomes clearer because you can sense where trust already lives.',
      developmentCue: 'Identify the route where invitation is already present.',
      masteryMarker: 'You know when context is creating a real opening.',
    },
    {
      branch: 'Embodiment',
      name: 'Leveraging Trust Networks',
      state: 'Emerging',
      description: 'The body learns to remain personally available even while moving through indirect channels.',
      effect: 'Presence stays intact because social access does not erase personal vulnerability.',
      developmentCue: 'Stay open while you move from network to contact.',
      masteryMarker: 'You can remain direct without losing relational finesse.',
    },
    {
      branch: 'Field',
      name: 'Relational Awareness',
      state: 'Emerging',
      description: 'The field becomes easier to enter because you can sense who, what, and where creates trust.',
      effect: 'Connection deepens more smoothly when the social environment is read accurately and used cleanly.',
      developmentCue: 'Use the field to support closeness rather than avoid it.',
      masteryMarker: 'The field carries you toward intimacy instead of keeping you on the edge.',
    },
    {
      branch: 'Mastery',
      name: 'Converting Access Into Real Connection',
      state: 'Mastery',
      description: 'The full path matures into trustworthy openness that can move from invitation into real relationship.',
      effect: 'Connection stabilizes because access, trust, and direct presence are no longer split apart.',
      developmentCue: 'Let the invitation become genuine openness.',
      masteryMarker: 'You can be fully present once the door is open.',
    },
  ],
};

export const mainQuest595V2: MainQuestContentEntryV2 = {
  gate: 59,
  line: 5,
  gateLine: '59.5',
  title: 'Projection / Universal Attraction',
  hero: {
    mainQuest: 'Unifying Influence',
    sourceLine: 'Purpose · Design Earth · I Ching 59.5',
    questState: 'Stirring',
    atmosphericSubtitle: 'Attraction must be corrected into truth before it becomes entanglement.',
  },
  questBrief: {
    collapsedPreview: 'Correct projection before it hardens.',
    mission: 'Let attraction become honest contact instead of borrowed expectation.',
    fieldPrompt: 'Feel where people are responding to an image of you rather than your actual presence.',
    livePrompt: 'Where does attraction need truth before it goes further?',
  },
  fieldBriefing: {
    collapsedPreview: 'Name projection before it binds.',
    whatThisQuestIsAbout:
      'People project onto you here. The field of attraction forms quickly, often before truth has been clarified or confirmed.',
    whyThisMattersNow:
      'If projection is not corrected early, connection turns into obligation, distortion, and entanglement.',
    primaryRecognitionTrigger:
      'You let them believe it, just long enough to stay.',
    livePrompt: 'Where are expectations being mistaken for connection?',
  },
  assetsAndFriction: {
    collapsedPreview: 'Influence needs correction to stay clean.',
    questTrap: 'You carry expectations that were never yours.',
    questAssets: [
      'strong attraction field',
      'influence over perception',
      'unifying presence',
    ],
    frictionSignals: [
      'letting misalignment continue',
      'avoiding confrontation',
      'becoming what’s expected',
    ],
    livePrompt: 'Notice when attraction is asking you to perform an identity.',
  },
  groundingEffect: {
    collapsedPreview: 'Anchor before speaking the truth.',
    groundingProtocol: [
      'anchor breath in belly',
      'stabilize stance',
      'speak without softening the message',
    ],
    somaticShift: 'The body stays grounded enough to tell the truth without collapsing into appeasement.',
    bodyCheckPrompt: 'Are you grounded enough to correct the field, or still adapting to it?',
  },
  unlockCondition: {
    collapsedPreview: 'Clarify reality while attraction is live.',
    questKey: 'Notice projection early → correct it directly → disengage if reality is rejected',
    embodiedSignal: 'You can stay grounded while naming what is true instead of becoming what is wanted.',
    ritualPrompt: 'Offer one clean correction before the projection gains more momentum.',
    alignmentReminder: 'Influence is clean only when it remains aligned with truth.',
    livePrompt: 'Tell one truth that restores reality to the interaction.',
  },
  driftPattern: [
    'losing identity in connection',
    'maintaining false alignment',
  ],
};

export const perkTree595V2: MainQuestPerkTreeV2 = {
  id: 'perk-tree-59-5-v2',
  mainQuestId: 'purpose-59-5',
  mainQuestName: 'Unifying Influence',
  sourceLine: 'Purpose · Design Earth · I Ching 59.5',
  questState: 'Stirring',
  subtitle: 'Develop the capacity to correct projection and align attraction with reality.',
  nodes: [
    {
      branch: 'Root',
      name: 'Unifying Influence',
      state: 'Core',
      description: 'This path develops the ability to hold attraction and truth together without distortion.',
      effect: 'Influence becomes trustworthy because projection is corrected before it becomes entanglement.',
      developmentCue: 'Recognize where the field is responding to image instead of reality.',
      masteryMarker: 'You can remain yourself while strong attraction is present.',
    },
    {
      branch: 'Awareness',
      name: 'Projection Awareness',
      state: 'Emerging',
      description: 'You learn to detect when people are relating to expectation, fantasy, or idealization instead of what is real.',
      effect: 'Misalignment becomes visible earlier, before it hardens into obligation or confusion.',
      developmentCue: 'Catch the moment perception stops matching reality.',
      masteryMarker: 'You can tell when the field is projecting onto you.',
    },
    {
      branch: 'Embodiment',
      name: 'Real-Time Correction Of Perception',
      state: 'Emerging',
      description: 'The body learns to stay grounded enough to offer correction without over-explaining or appeasing.',
      effect: 'Truth can enter the interaction while attraction is still alive.',
      developmentCue: 'Speak the correction before the story grows stronger.',
      masteryMarker: 'You can correct perception without losing your center.',
    },
    {
      branch: 'Field',
      name: 'Unifying Presence',
      state: 'Emerging',
      description: 'The field becomes more coherent because attraction is aligned with truth instead of distortion.',
      effect: 'Connection deepens with greater integrity because false expectations are not allowed to lead it.',
      developmentCue: 'Hold the field steady while reality is named.',
      masteryMarker: 'The field stays connected without depending on illusion.',
    },
    {
      branch: 'Mastery',
      name: 'Aligning Attraction With Truth',
      state: 'Mastery',
      description: 'The full path matures into influence that attracts, clarifies, and unifies without distortion.',
      effect: 'Intimacy becomes cleaner because attraction no longer depends on projection to sustain itself.',
      developmentCue: 'Keep reality present from first attraction through deeper contact.',
      masteryMarker: 'Connection holds because truth was present from the start.',
    },
  ],
};

export const mainQuest596V2: MainQuestContentEntryV2 = {
  gate: 59,
  line: 6,
  gateLine: '59.6',
  title: 'Withdrawal / Selective Intimacy',
  hero: {
    mainQuest: 'Free Intimacy',
    sourceLine: 'Purpose · Design Earth · I Ching 59.6',
    questState: 'Stirring',
    atmosphericSubtitle: 'Discernment serves intimacy only when it still leads to entry.',
  },
  questBrief: {
    collapsedPreview: 'Let discernment end in participation.',
    mission: 'Choose clean connection without hiding behind endless evaluation.',
    fieldPrompt: 'Feel where your standards are protecting integrity versus blocking entry altogether.',
    livePrompt: 'Where is discernment becoming avoidance instead of guidance?',
  },
  fieldBriefing: {
    collapsedPreview: 'Filter clearly, then actually enter.',
    whatThisQuestIsAbout:
      'Connection is filtered heavily here. You observe, assess, and withhold until enough alignment is proven to justify entry.',
    whyThisMattersNow:
      'Discernment protects integrity only when it eventually becomes contact instead of permanent distance.',
    primaryRecognitionTrigger:
      'You keep it distant enough to never have to risk it.',
    livePrompt: 'Where are you still observing instead of participating?',
  },
  assetsAndFriction: {
    collapsedPreview: 'High standards help until entry disappears.',
    questTrap: 'You wait until it’s perfect, then it’s gone.',
    questAssets: [
      'high discernment',
      'selective intimacy',
      'clarity in bonding',
    ],
    frictionSignals: [
      'over-filtering connection',
      'staying in observation mode',
      'avoiding entry altogether',
    ],
    livePrompt: 'Notice when discernment is delaying a clean yes.',
  },
  groundingEffect: {
    collapsedPreview: 'Release the body from guarded distance.',
    groundingProtocol: [
      'relax back of neck',
      'deepen breath into lower spine',
      'release chest tension',
    ],
    somaticShift: 'The body can stay discerning without armoring itself against contact.',
    bodyCheckPrompt: 'Are you clear enough to choose, or just defended enough to stay away?',
  },
  unlockCondition: {
    collapsedPreview: 'Enter before over-evaluation takes over.',
    questKey: 'Hold distance → identify one clear signal of alignment → enter before over-evaluating',
    embodiedSignal: 'Your body can stay calm while moving toward a clean yes instead of retreating into distance.',
    ritualPrompt: 'Respond to one clear sign of alignment before you add another filter.',
    alignmentReminder: 'Discernment is complete only when it permits real participation.',
    livePrompt: 'Take one step into the connection you already know is clean.',
  },
  driftPattern: [
    'observing without participating',
    'missing connection windows repeatedly',
  ],
};

export const perkTree596V2: MainQuestPerkTreeV2 = {
  id: 'perk-tree-59-6-v2',
  mainQuestId: 'purpose-59-6',
  mainQuestName: 'Free Intimacy',
  sourceLine: 'Purpose · Design Earth · I Ching 59.6',
  questState: 'Stirring',
  subtitle: 'Develop the capacity to discern cleanly and enter high-integrity connection without delay.',
  nodes: [
    {
      branch: 'Root',
      name: 'Free Intimacy',
      state: 'Core',
      description: 'This path develops the ability to let discernment protect connection without preventing it.',
      effect: 'Closeness becomes cleaner because standards guide entry instead of replacing it.',
      developmentCue: 'Recognize when alignment is already sufficient.',
      masteryMarker: 'You can choose contact without needing perfect certainty.',
    },
    {
      branch: 'Awareness',
      name: 'Selective Engagement',
      state: 'Emerging',
      description: 'You learn to distinguish genuine misalignment from the habit of over-filtering connection.',
      effect: 'Signals of real integrity become easier to notice before they are analyzed into distance.',
      developmentCue: 'Name the difference between caution and withdrawal.',
      masteryMarker: 'You can tell when discernment has already done its job.',
    },
    {
      branch: 'Embodiment',
      name: 'Fast Alignment Detection',
      state: 'Emerging',
      description: 'The body learns to feel trustworthy alignment quickly without freezing in protective distance.',
      effect: 'Decision-making becomes more fluid because the body is not locked in perpetual observation.',
      developmentCue: 'Let the body register the clean signal and move.',
      masteryMarker: 'You can enter while still staying deeply discerning.',
    },
    {
      branch: 'Field',
      name: 'Clarity In Bonding',
      state: 'Emerging',
      description: 'The relational field becomes clearer because intimacy is filtered by integrity instead of fear.',
      effect: 'Connection holds more truth because what is chosen has already been felt and verified.',
      developmentCue: 'Allow the clean field to form once alignment is known.',
      masteryMarker: 'The field can open because you stop withholding after clarity arrives.',
    },
    {
      branch: 'Mastery',
      name: 'Entering Only High-Integrity Connections Without Delay',
      state: 'Mastery',
      description: 'The full path matures into discernment that is selective, free, and capable of true participation.',
      effect: 'Intimacy becomes trustworthy because alignment and entry are no longer split apart.',
      developmentCue: 'Move once the connection has already proven itself clean.',
      masteryMarker: 'You can say yes to integrity without staying trapped in distance.',
    },
  ],
};

// ─── Gate 64 ────────────────────────────────────────────────────────────────

export const mainQuest641V2: MainQuestContentEntryV2 = {
  gate: 64,
  line: 1,
  gateLine: '64.1',
  title: 'Pressure at the Threshold',
  hero: {
    mainQuest: 'Pattern Resolution',
    sourceLine: 'Purpose · Design Earth · I Ching 64.1',
    questState: 'Unsorted',
    atmosphericSubtitle: 'The pattern is not ready. The pressure still wants an answer.',
  },
  questBrief: {
    collapsedPreview: 'The pieces are present, but not placed.',
    mission: 'Hold the first layer of confusion without rushing it into certainty.',
    fieldPrompt: 'Look for the one piece that keeps demanding premature closure.',
    livePrompt: 'What are you trying to solve too early?',
  },
  fieldBriefing: {
    collapsedPreview: 'Stay with the first incomplete signal.',
    whatThisQuestIsAbout: 'This quest begins before the pattern has enough structure to reveal itself. Information arrives in pieces, but the mind wants to seal it into an answer before the foundation is stable.',
    whyThisMattersNow: 'Early certainty creates a false base. The work is to hold the beginning without letting pressure choose the conclusion.',
    primaryRecognitionTrigger: 'You grab the first explanation because not knowing feels exposed.',
    livePrompt: 'Where are you treating one clue like the whole answer?',
  },
  assetsAndFriction: {
    collapsedPreview: 'Foundation comes before interpretation.',
    questTrap: 'You mistake relief for clarity.',
    questAssets: ['first-signal detection', 'mental containment', 'pattern patience'],
    frictionSignals: [
      'locking onto the first reason',
      'asking for certainty before enough is visible',
      'building a conclusion from one fragment',
    ],
    livePrompt: 'Watch where relief arrives faster than truth.',
  },
  groundingEffect: {
    collapsedPreview: 'Let the pressure drop lower.',
    groundingProtocol: ['soften the forehead', 'drop breath into belly', 'release the grip in your hands'],
    somaticShift: 'The body stops chasing the answer and settles under the question.',
    bodyCheckPrompt: 'Is your head reaching forward, or can your belly hold the unknown?',
  },
  unlockCondition: {
    collapsedPreview: 'Do not crown the first answer.',
    questKey: 'Name the first fragment → refuse final meaning → wait for a second confirming signal',
    embodiedSignal: 'The body feels less urgent even though the question remains open.',
    ritualPrompt: 'Write the first clue down without deciding what it means yet.',
    alignmentReminder: 'A fragment is not a pattern.',
    livePrompt: 'Wait for one more piece before naming the truth.',
  },
  driftPattern: ['using one clue as proof', 'ending inquiry before the pattern forms'],
};

export const perkTree641V2: MainQuestPerkTreeV2 = {
  id: 'perk-tree-64-1-v2',
  mainQuestId: 'purpose-64-1',
  mainQuestName: 'Pattern Resolution',
  sourceLine: 'Purpose · Design Earth · I Ching 64.1',
  questState: 'Unsorted',
  subtitle: 'Develop the capacities behind Pressure at the Threshold.',
  nodes: [
    {
      branch: 'Root',
      name: 'Pattern Resolution',
      state: 'Core',
      description: 'This path develops the ability to turn incomplete mental pressure into usable clarity through pressure at the threshold.',
      effect: 'Confusion becomes workable when the pattern is not forced into false certainty.',
      developmentCue: 'Notice the difference between pressure and real pattern.',
      masteryMarker: 'Unfinished information can be held without rushing into closure.',
    },
    {
      branch: 'Awareness',
      name: 'Seeing the First Fragment',
      state: 'Emerging',
      description: 'You learn to notice which part of the pattern is actually visible.',
      effect: 'Fragments stop pretending to be the whole picture.',
      developmentCue: 'Identify the clearest piece without enlarging it.',
      masteryMarker: 'You can separate a real signal from a completed story.',
    },
    {
      branch: 'Embodiment',
      name: 'Holding Initial Uncertainty',
      state: 'Emerging',
      description: 'The body learns to stay steady while the mind has not finished sorting.',
      effect: 'Action slows enough for real structure to appear.',
      developmentCue: 'Let the body settle before naming the answer.',
      masteryMarker: 'You remain physically steady without needing instant resolution.',
    },
    {
      branch: 'Field',
      name: 'Foundational Sorting',
      state: 'Emerging',
      description: 'The surrounding field becomes easier to read when the pattern is not forced.',
      effect: 'Confusion becomes organized through timing, response, and visible feedback.',
      developmentCue: 'Let the field show which pieces belong together.',
      masteryMarker: 'The pattern can clarify without being mentally cornered.',
    },
    {
      branch: 'Mastery',
      name: 'Waiting for the Pattern to Form',
      state: 'Mastery',
      description: 'The full path matures into clean resolution without premature closure.',
      effect: 'Clarity arrives with enough structure to support action.',
      developmentCue: 'Wait until the pattern can carry the next move.',
      masteryMarker: 'You complete the thought only when the form is ready.',
    },
  ],
};

export const mainQuest642V2: MainQuestContentEntryV2 = {
  gate: 64,
  line: 2,
  gateLine: '64.2',
  title: 'Natural Pattern Recognition',
  hero: {
    mainQuest: 'Pattern Resolution',
    sourceLine: 'Purpose · Design Earth · I Ching 64.2',
    questState: 'Glimmering',
    atmosphericSubtitle: 'The answer appears sideways before the mind can justify it.',
  },
  questBrief: {
    collapsedPreview: 'The pattern flashes before it explains itself.',
    mission: 'Trust the clean recognition without forcing it into a full argument.',
    fieldPrompt: 'Notice where the answer arrives as shape, not proof.',
    livePrompt: 'What do you recognize before you can explain?',
  },
  fieldBriefing: {
    collapsedPreview: 'Let recognition arrive before reasoning.',
    whatThisQuestIsAbout: 'This line sees the pattern before the details have organized. The insight is real, but it is delicate; too much explanation too soon can distort the signal.',
    whyThisMattersNow: 'The gift is early recognition. The danger is trying to prove the recognition before it has matured.',
    primaryRecognitionTrigger: 'You know what it is, then ruin it trying to justify why.',
    livePrompt: 'Where does your knowing get weaker when you over-explain it?',
  },
  assetsAndFriction: {
    collapsedPreview: 'Recognition is faster than proof.',
    questTrap: 'You explain the signal until it loses shape.',
    questAssets: ['intuitive pattern sight', 'early signal recognition', 'quiet mental accuracy'],
    frictionSignals: [
      'over-explaining a clean read',
      'doubting the first true shape',
      'forcing proof before timing supports it',
    ],
    livePrompt: 'Watch where clarity turns into performance.',
  },
  groundingEffect: {
    collapsedPreview: 'Keep the knowing quiet in the body.',
    groundingProtocol: ['relax the jaw', 'let breath settle behind the ribs', 'soften the eyes before speaking'],
    somaticShift: 'The insight stays intact because the body does not rush to defend it.',
    bodyCheckPrompt: 'Does your throat tighten when you try to prove what you already see?',
  },
  unlockCondition: {
    collapsedPreview: 'Recognize first, explain later.',
    questKey: 'Notice the pattern → hold it without defending → speak only the part that is clear',
    embodiedSignal: 'The body stays quiet even while the mind sees the shape.',
    ritualPrompt: 'Say only the cleanest sentence and leave the rest unfinished.',
    alignmentReminder: 'Over-proof can break an accurate read.',
    livePrompt: 'Speak the shape, not the whole theory.',
  },
  driftPattern: ['weakening recognition through explanation', 'turning a clean insight into a case to defend'],
};

export const perkTree642V2: MainQuestPerkTreeV2 = {
  id: 'perk-tree-64-2-v2',
  mainQuestId: 'purpose-64-2',
  mainQuestName: 'Pattern Resolution',
  sourceLine: 'Purpose · Design Earth · I Ching 64.2',
  questState: 'Glimmering',
  subtitle: 'Develop the capacities behind Natural Pattern Recognition.',
  nodes: [
    {
      branch: 'Root',
      name: 'Pattern Resolution',
      state: 'Core',
      description: 'This path develops the ability to turn incomplete mental pressure into usable clarity through natural pattern recognition.',
      effect: 'Confusion becomes workable when the pattern is not forced into false certainty.',
      developmentCue: 'Notice the difference between pressure and real pattern.',
      masteryMarker: 'Unfinished information can be held without rushing into closure.',
    },
    {
      branch: 'Awareness',
      name: 'Early Pattern Recognition',
      state: 'Emerging',
      description: 'You learn to notice which part of the pattern is actually visible.',
      effect: 'Fragments stop pretending to be the whole picture.',
      developmentCue: 'Identify the clearest piece without enlarging it.',
      masteryMarker: 'You can separate a real signal from a completed story.',
    },
    {
      branch: 'Embodiment',
      name: 'Quiet Knowing',
      state: 'Emerging',
      description: 'The body learns to stay steady while the mind has not finished sorting.',
      effect: 'Action slows enough for real structure to appear.',
      developmentCue: 'Let the body settle before naming the answer.',
      masteryMarker: 'You remain physically steady without needing instant resolution.',
    },
    {
      branch: 'Field',
      name: 'Signal Preservation',
      state: 'Emerging',
      description: 'The surrounding field becomes easier to read when the pattern is not forced.',
      effect: 'Confusion becomes organized through timing, response, and visible feedback.',
      developmentCue: 'Let the field show which pieces belong together.',
      masteryMarker: 'The pattern can clarify without being mentally cornered.',
    },
    {
      branch: 'Mastery',
      name: 'Recognizing Without Over-Proving',
      state: 'Mastery',
      description: 'The full path matures into clean resolution without premature closure.',
      effect: 'Clarity arrives with enough structure to support action.',
      developmentCue: 'Wait until the pattern can carry the next move.',
      masteryMarker: 'You complete the thought only when the form is ready.',
    },
  ],
};

export const mainQuest643V2: MainQuestContentEntryV2 = {
  gate: 64,
  line: 3,
  gateLine: '64.3',
  title: 'Confusion Through Collision',
  hero: {
    mainQuest: 'Pattern Resolution',
    sourceLine: 'Purpose · Design Earth · I Ching 64.3',
    questState: 'Scrambling',
    atmosphericSubtitle: 'The pieces collide until the false order breaks.',
  },
  questBrief: {
    collapsedPreview: 'The wrong fit teaches the real pattern.',
    mission: 'Use the failed interpretation as feedback instead of proof that nothing makes sense.',
    fieldPrompt: 'Track which explanation collapses the moment it touches reality.',
    livePrompt: 'What keeps breaking when tested?',
  },
  fieldBriefing: {
    collapsedPreview: 'The pattern forms through failed fits.',
    whatThisQuestIsAbout: 'This line learns by trying to connect pieces that do not always belong together. Confusion intensifies when the mind keeps forcing a fit instead of noticing what the failure reveals.',
    whyThisMattersNow: 'The breakdown is useful when it exposes the wrong structure. It becomes costly when the same false pattern is rebuilt again.',
    primaryRecognitionTrigger: 'You keep rearranging the same pieces and calling it progress.',
    livePrompt: 'Where is the same failed answer wearing a new shape?',
  },
  assetsAndFriction: {
    collapsedPreview: 'Bad fits reveal the structure.',
    questTrap: 'You keep testing what already failed.',
    questAssets: ['error detection', 'adaptive sorting', 'friction-based learning'],
    frictionSignals: [
      'forcing unrelated pieces together',
      'restarting the same interpretation',
      'ignoring what the failed fit exposed',
    ],
    livePrompt: 'Watch the part of the pattern that keeps rejecting your answer.',
  },
  groundingEffect: {
    collapsedPreview: 'Stop solving from the skull.',
    groundingProtocol: ['lengthen the spine', 'release tension behind the eyes', 'exhale before choosing the next piece'],
    somaticShift: 'The body stops bracing against confusion and begins sorting one contact point at a time.',
    bodyCheckPrompt: 'Are you tightening around the answer, or feeling where the fit fails?',
  },
  unlockCondition: {
    collapsedPreview: 'Use the failure as data.',
    questKey: 'Test one connection → mark the failure honestly → change the next attempt',
    embodiedSignal: 'The body feels clearer after admitting what does not fit.',
    ritualPrompt: 'Remove one false link before adding another idea.',
    alignmentReminder: 'A failed fit is information, not defeat.',
    livePrompt: 'Let the broken connection teach the next move.',
  },
  driftPattern: ['rebuilding the same false explanation', 'treating confusion as a reason to force harder'],
};

export const perkTree643V2: MainQuestPerkTreeV2 = {
  id: 'perk-tree-64-3-v2',
  mainQuestId: 'purpose-64-3',
  mainQuestName: 'Pattern Resolution',
  sourceLine: 'Purpose · Design Earth · I Ching 64.3',
  questState: 'Scrambling',
  subtitle: 'Develop the capacities behind Confusion Through Collision.',
  nodes: [
    {
      branch: 'Root',
      name: 'Pattern Resolution',
      state: 'Core',
      description: 'This path develops the ability to turn incomplete mental pressure into usable clarity through confusion through collision.',
      effect: 'Confusion becomes workable when the pattern is not forced into false certainty.',
      developmentCue: 'Notice the difference between pressure and real pattern.',
      masteryMarker: 'Unfinished information can be held without rushing into closure.',
    },
    {
      branch: 'Awareness',
      name: 'Failure-Based Sorting',
      state: 'Emerging',
      description: 'You learn to notice which part of the pattern is actually visible.',
      effect: 'Fragments stop pretending to be the whole picture.',
      developmentCue: 'Identify the clearest piece without enlarging it.',
      masteryMarker: 'You can separate a real signal from a completed story.',
    },
    {
      branch: 'Embodiment',
      name: 'Adaptive Reassembly',
      state: 'Emerging',
      description: 'The body learns to stay steady while the mind has not finished sorting.',
      effect: 'Action slows enough for real structure to appear.',
      developmentCue: 'Let the body settle before naming the answer.',
      masteryMarker: 'You remain physically steady without needing instant resolution.',
    },
    {
      branch: 'Field',
      name: 'Friction Testing',
      state: 'Emerging',
      description: 'The surrounding field becomes easier to read when the pattern is not forced.',
      effect: 'Confusion becomes organized through timing, response, and visible feedback.',
      developmentCue: 'Let the field show which pieces belong together.',
      masteryMarker: 'The pattern can clarify without being mentally cornered.',
    },
    {
      branch: 'Mastery',
      name: 'Learning Through Broken Fits',
      state: 'Mastery',
      description: 'The full path matures into clean resolution without premature closure.',
      effect: 'Clarity arrives with enough structure to support action.',
      developmentCue: 'Wait until the pattern can carry the next move.',
      masteryMarker: 'You complete the thought only when the form is ready.',
    },
  ],
};

export const mainQuest644V2: MainQuestContentEntryV2 = {
  gate: 64,
  line: 4,
  gateLine: '64.4',
  title: 'Shared Mental Framework',
  hero: {
    mainQuest: 'Pattern Resolution',
    sourceLine: 'Purpose · Design Earth · I Ching 64.4',
    questState: 'Arranging',
    atmosphericSubtitle: 'The pattern sharpens when it is placed into a shared frame.',
  },
  questBrief: {
    collapsedPreview: 'Clarity improves when the frame is shared.',
    mission: 'Bring the scattered pieces into a structure others can respond to.',
    fieldPrompt: 'Find the frame that makes the confusion discussable.',
    livePrompt: 'Who needs the pattern made visible?',
  },
  fieldBriefing: {
    collapsedPreview: 'Make the confusion shareable.',
    whatThisQuestIsAbout: 'This line organizes uncertainty through relationship, language, and shared framing. The pattern becomes clearer when it is placed where others can see, test, and respond to it.',
    whyThisMattersNow: 'Private confusion loops. Shared structure reveals gaps, support, and next steps.',
    primaryRecognitionTrigger: 'You keep it in your head so no one can challenge the frame.',
    livePrompt: 'Where would clarity improve if someone else could see the map?',
  },
  assetsAndFriction: {
    collapsedPreview: 'The frame needs witnesses.',
    questTrap: 'You organize alone until the pattern goes stale.',
    questAssets: ['shared framing', 'collaborative sorting', 'communicable structure'],
    frictionSignals: [
      'withholding the unfinished map',
      'asking for input too late',
      'protecting a private interpretation',
    ],
    livePrompt: 'Watch where secrecy keeps the confusion intact.',
  },
  groundingEffect: {
    collapsedPreview: 'Open the chest before explaining.',
    groundingProtocol: ['expand breath across chest', 'relax the tongue', 'plant both feet before presenting'],
    somaticShift: 'The body becomes available for response instead of defending the private map.',
    bodyCheckPrompt: 'Can your chest stay open while someone tests your frame?',
  },
  unlockCondition: {
    collapsedPreview: 'Expose the frame before it hardens.',
    questKey: 'Draft the pattern → share the unfinished frame → revise from real response',
    embodiedSignal: 'The body stays steady while the structure is questioned.',
    ritualPrompt: 'Show the current map before polishing it.',
    alignmentReminder: 'A shared frame can reveal what private certainty hides.',
    livePrompt: 'Let one trusted person test the pattern.',
  },
  driftPattern: ['protecting unfinished thoughts from feedback', 'staying private until the structure becomes rigid'],
};

export const perkTree644V2: MainQuestPerkTreeV2 = {
  id: 'perk-tree-64-4-v2',
  mainQuestId: 'purpose-64-4',
  mainQuestName: 'Pattern Resolution',
  sourceLine: 'Purpose · Design Earth · I Ching 64.4',
  questState: 'Arranging',
  subtitle: 'Develop the capacities behind Shared Mental Framework.',
  nodes: [
    {
      branch: 'Root',
      name: 'Pattern Resolution',
      state: 'Core',
      description: 'This path develops the ability to turn incomplete mental pressure into usable clarity through shared mental framework.',
      effect: 'Confusion becomes workable when the pattern is not forced into false certainty.',
      developmentCue: 'Notice the difference between pressure and real pattern.',
      masteryMarker: 'Unfinished information can be held without rushing into closure.',
    },
    {
      branch: 'Awareness',
      name: 'Shared Framing',
      state: 'Emerging',
      description: 'You learn to notice which part of the pattern is actually visible.',
      effect: 'Fragments stop pretending to be the whole picture.',
      developmentCue: 'Identify the clearest piece without enlarging it.',
      masteryMarker: 'You can separate a real signal from a completed story.',
    },
    {
      branch: 'Embodiment',
      name: 'Collaborative Sorting',
      state: 'Emerging',
      description: 'The body learns to stay steady while the mind has not finished sorting.',
      effect: 'Action slows enough for real structure to appear.',
      developmentCue: 'Let the body settle before naming the answer.',
      masteryMarker: 'You remain physically steady without needing instant resolution.',
    },
    {
      branch: 'Field',
      name: 'Communicable Structure',
      state: 'Emerging',
      description: 'The surrounding field becomes easier to read when the pattern is not forced.',
      effect: 'Confusion becomes organized through timing, response, and visible feedback.',
      developmentCue: 'Let the field show which pieces belong together.',
      masteryMarker: 'The pattern can clarify without being mentally cornered.',
    },
    {
      branch: 'Mastery',
      name: 'Making Confusion Discussable',
      state: 'Mastery',
      description: 'The full path matures into clean resolution without premature closure.',
      effect: 'Clarity arrives with enough structure to support action.',
      developmentCue: 'Wait until the pattern can carry the next move.',
      masteryMarker: 'You complete the thought only when the form is ready.',
    },
  ],
};

export const mainQuest645V2: MainQuestContentEntryV2 = {
  gate: 64,
  line: 5,
  gateLine: '64.5',
  title: 'Projected Resolution',
  hero: {
    mainQuest: 'Pattern Resolution',
    sourceLine: 'Purpose · Design Earth · I Ching 64.5',
    questState: 'Pressurized',
    atmosphericSubtitle: 'People expect the answer before the pattern is complete.',
  },
  questBrief: {
    collapsedPreview: 'Others look to you for closure.',
    mission: 'Hold projected certainty without pretending the answer is finished.',
    fieldPrompt: 'Separate the pressure to resolve from the pattern actually resolving.',
    livePrompt: 'Who is asking you to know before you know?',
  },
  fieldBriefing: {
    collapsedPreview: 'Pressure is not proof.',
    whatThisQuestIsAbout: 'This line attracts expectation. Others may treat your partial clarity as final truth, and the mind feels pulled to deliver resolution before the pattern has fully arrived.',
    whyThisMattersNow: 'False certainty spreads quickly here. The real power is naming what is clear without pretending the rest is complete.',
    primaryRecognitionTrigger: 'You sound certain because they need you to be.',
    livePrompt: 'Where are you performing closure for someone else\'s anxiety?',
  },
  assetsAndFriction: {
    collapsedPreview: 'Influence requires honest limits.',
    questTrap: 'You become the answer before the answer exists.',
    questAssets: ['public synthesis', 'pressure steadiness', 'responsible clarification'],
    frictionSignals: [
      'speaking past the evidence',
      'absorbing others\' urgency',
      'turning partial insight into a final call',
    ],
    livePrompt: 'Watch where being trusted becomes pressure to overstate.',
  },
  groundingEffect: {
    collapsedPreview: 'Hold your center under expectation.',
    groundingProtocol: ['anchor breath in belly', 'relax the sternum', 'slow the first sentence'],
    somaticShift: 'The body stops rising into performance and returns to measured truth.',
    bodyCheckPrompt: 'Are you speaking from clarity, or from the pressure to relieve the room?',
  },
  unlockCondition: {
    collapsedPreview: 'Separate clarity from performance.',
    questKey: 'Name what is clear → mark what is unfinished → refuse finality under pressure',
    embodiedSignal: 'The body stays grounded even when others want certainty.',
    ritualPrompt: 'Say the boundary of the answer before giving the answer.',
    alignmentReminder: 'Authority collapses when certainty is borrowed.',
    livePrompt: 'Tell the truth without completing the pattern for them.',
  },
  driftPattern: ['performing certainty for others', 'overstating clarity to reduce pressure'],
};

export const perkTree645V2: MainQuestPerkTreeV2 = {
  id: 'perk-tree-64-5-v2',
  mainQuestId: 'purpose-64-5',
  mainQuestName: 'Pattern Resolution',
  sourceLine: 'Purpose · Design Earth · I Ching 64.5',
  questState: 'Pressurized',
  subtitle: 'Develop the capacities behind Projected Resolution.',
  nodes: [
    {
      branch: 'Root',
      name: 'Pattern Resolution',
      state: 'Core',
      description: 'This path develops the ability to turn incomplete mental pressure into usable clarity through projected resolution.',
      effect: 'Confusion becomes workable when the pattern is not forced into false certainty.',
      developmentCue: 'Notice the difference between pressure and real pattern.',
      masteryMarker: 'Unfinished information can be held without rushing into closure.',
    },
    {
      branch: 'Awareness',
      name: 'Projected Clarity',
      state: 'Emerging',
      description: 'You learn to notice which part of the pattern is actually visible.',
      effect: 'Fragments stop pretending to be the whole picture.',
      developmentCue: 'Identify the clearest piece without enlarging it.',
      masteryMarker: 'You can separate a real signal from a completed story.',
    },
    {
      branch: 'Embodiment',
      name: 'Pressure Boundaries',
      state: 'Emerging',
      description: 'The body learns to stay steady while the mind has not finished sorting.',
      effect: 'Action slows enough for real structure to appear.',
      developmentCue: 'Let the body settle before naming the answer.',
      masteryMarker: 'You remain physically steady without needing instant resolution.',
    },
    {
      branch: 'Field',
      name: 'Responsible Synthesis',
      state: 'Emerging',
      description: 'The surrounding field becomes easier to read when the pattern is not forced.',
      effect: 'Confusion becomes organized through timing, response, and visible feedback.',
      developmentCue: 'Let the field show which pieces belong together.',
      masteryMarker: 'The pattern can clarify without being mentally cornered.',
    },
    {
      branch: 'Mastery',
      name: 'Speaking Partial Truth Cleanly',
      state: 'Mastery',
      description: 'The full path matures into clean resolution without premature closure.',
      effect: 'Clarity arrives with enough structure to support action.',
      developmentCue: 'Wait until the pattern can carry the next move.',
      masteryMarker: 'You complete the thought only when the form is ready.',
    },
  ],
};

export const mainQuest646V2: MainQuestContentEntryV2 = {
  gate: 64,
  line: 6,
  gateLine: '64.6',
  title: 'Completion Without Closure',
  hero: {
    mainQuest: 'Pattern Resolution',
    sourceLine: 'Purpose · Design Earth · I Ching 64.6',
    questState: 'Suspended',
    atmosphericSubtitle: 'The pattern is visible, but the final move has not arrived.',
  },
  questBrief: {
    collapsedPreview: 'Completion waits past the answer.',
    mission: 'Let the pattern remain unfinished until timing, evidence, and readiness align.',
    fieldPrompt: 'Notice where almost-complete still wants one more condition.',
    livePrompt: 'What is clear, but not ready?',
  },
  fieldBriefing: {
    collapsedPreview: 'Do not force the final seal.',
    whatThisQuestIsAbout: 'This line stands near completion but cannot force the last piece into place. The pattern may be mostly visible, yet the final movement depends on timing rather than mental pressure.',
    whyThisMattersNow: 'Premature closure reduces the intelligence of the whole process. Waiting becomes active when it protects the final form.',
    primaryRecognitionTrigger: 'You call it done because waiting one more step feels unbearable.',
    livePrompt: 'Where is the almost-finished thing asking not to be sealed yet?',
  },
  assetsAndFriction: {
    collapsedPreview: 'The last piece has timing.',
    questTrap: 'You finish the pattern to escape the pressure.',
    questAssets: ['completion discernment', 'timing awareness', 'final-stage restraint'],
    frictionSignals: [
      'sealing the answer too soon',
      'mistaking exhaustion for completion',
      'forcing closure because the pattern is almost clear',
    ],
    livePrompt: 'Watch where impatience disguises itself as readiness.',
  },
  groundingEffect: {
    collapsedPreview: 'Let the spine hold the pause.',
    groundingProtocol: ['lengthen the back of the neck', 'settle breath down the spine', 'release the chest from urgency'],
    somaticShift: 'The body can hold almost-complete without collapsing into a final move.',
    bodyCheckPrompt: 'Can your spine stay steady while the answer remains unfinished?',
  },
  unlockCondition: {
    collapsedPreview: 'Wait until completion is real.',
    questKey: 'See the near-complete pattern → pause before closure → act only when the last condition arrives',
    embodiedSignal: 'The body feels steady enough to leave the ending open.',
    ritualPrompt: 'Name the missing condition before calling it complete.',
    alignmentReminder: 'Almost finished is not finished.',
    livePrompt: 'Protect the final step from premature closure.',
  },
  driftPattern: ['forcing closure at the edge of completion', 'mistaking relief for readiness'],
};

export const perkTree646V2: MainQuestPerkTreeV2 = {
  id: 'perk-tree-64-6-v2',
  mainQuestId: 'purpose-64-6',
  mainQuestName: 'Pattern Resolution',
  sourceLine: 'Purpose · Design Earth · I Ching 64.6',
  questState: 'Suspended',
  subtitle: 'Develop the capacities behind Completion Without Closure.',
  nodes: [
    {
      branch: 'Root',
      name: 'Pattern Resolution',
      state: 'Core',
      description: 'This path develops the ability to turn incomplete mental pressure into usable clarity through completion without closure.',
      effect: 'Confusion becomes workable when the pattern is not forced into false certainty.',
      developmentCue: 'Notice the difference between pressure and real pattern.',
      masteryMarker: 'Unfinished information can be held without rushing into closure.',
    },
    {
      branch: 'Awareness',
      name: 'Final-Stage Discernment',
      state: 'Emerging',
      description: 'You learn to notice which part of the pattern is actually visible.',
      effect: 'Fragments stop pretending to be the whole picture.',
      developmentCue: 'Identify the clearest piece without enlarging it.',
      masteryMarker: 'You can separate a real signal from a completed story.',
    },
    {
      branch: 'Embodiment',
      name: 'Completion Restraint',
      state: 'Emerging',
      description: 'The body learns to stay steady while the mind has not finished sorting.',
      effect: 'Action slows enough for real structure to appear.',
      developmentCue: 'Let the body settle before naming the answer.',
      masteryMarker: 'You remain physically steady without needing instant resolution.',
    },
    {
      branch: 'Field',
      name: 'Timing Protection',
      state: 'Emerging',
      description: 'The surrounding field becomes easier to read when the pattern is not forced.',
      effect: 'Confusion becomes organized through timing, response, and visible feedback.',
      developmentCue: 'Let the field show which pieces belong together.',
      masteryMarker: 'The pattern can clarify without being mentally cornered.',
    },
    {
      branch: 'Mastery',
      name: 'Completing Only When Ready',
      state: 'Mastery',
      description: 'The full path matures into clean resolution without premature closure.',
      effect: 'Clarity arrives with enough structure to support action.',
      developmentCue: 'Wait until the pattern can carry the next move.',
      masteryMarker: 'You complete the thought only when the form is ready.',
    },
  ],
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
  return `Purpose · Design Earth · I Ching ${gate}.${line}`;
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

function mapV2ContentToEntry(content: MainQuestContentEntryV2, perkTreeId: string): MainQuestContentEntry {
  return {
    id: createMainQuestId(content.gate, content.line),
    sphere: 'Purpose',
    gate: content.gate,
    line: content.line,
    worldLabel: 'MAIN QUEST',
    mainQuest: content.hero.mainQuest,
    sourceLine: content.hero.sourceLine,
    questState: content.hero.questState,
    atmosphericSubtitle: content.hero.atmosphericSubtitle,
    questBrief: content.questBrief.mission,
    fieldPrompt: content.questBrief.fieldPrompt,
    whatThisQuestIsAbout: content.fieldBriefing.whatThisQuestIsAbout,
    questArena: content.fieldBriefing.whyThisMattersNow,
    naturalPower: content.assetsAndFriction.questAssets.join(' · '),
    questTrap: content.assetsAndFriction.questTrap,
    behavioralTells: content.assetsAndFriction.frictionSignals,
    groundingEffect: content.groundingEffect.somaticShift,
    supportsSunExpression: content.groundingEffect.bodyCheckPrompt,
    somaticAnchor: content.groundingEffect.groundingProtocol[0] || content.groundingEffect.somaticShift,
    questKey: content.unlockCondition.questKey,
    embodiedSignal: content.unlockCondition.embodiedSignal,
    ritualPrompt: content.unlockCondition.ritualPrompt,
    alignmentReminder: content.unlockCondition.alignmentReminder,
    collapsedPreviews: {
      questBrief: content.questBrief.collapsedPreview,
      fieldBriefing: content.fieldBriefing.collapsedPreview,
      assetsFriction: content.assetsAndFriction.collapsedPreview,
      groundingEffect: content.groundingEffect.collapsedPreview,
      unlockCondition: content.unlockCondition.collapsedPreview,
      perkTree: 'Explore the capacities developing inside this Main Quest.',
    },
    livePrompts: {
      questBrief: content.questBrief.livePrompt,
      fieldBriefing: content.fieldBriefing.livePrompt,
      assetsFriction: content.assetsAndFriction.livePrompt,
      groundingEffect: content.groundingEffect.bodyCheckPrompt,
      unlockCondition: content.unlockCondition.livePrompt,
    },
    perkTreeId,
    gateLine: content.gateLine,
    fieldBriefing: {
      whatThisQuestIsAbout: content.fieldBriefing.whatThisQuestIsAbout,
      primaryRecognitionTrigger: content.fieldBriefing.primaryRecognitionTrigger,
      whyThisMattersNow: content.fieldBriefing.whyThisMattersNow,
    },
    assetsAndFriction: {
      questAssets: content.assetsAndFriction.questAssets,
      questTrap: content.assetsAndFriction.questTrap,
      frictionSignals: content.assetsAndFriction.frictionSignals,
    },
    groundingProtocol: content.groundingEffect.groundingProtocol,
    driftPattern: content.driftPattern,
    v2: content,
  };
}

export function mapV2PerkTreeToTree(content: MainQuestPerkTreeV2): MainQuestPerkTree {
  const rootNode = content.nodes.find((node) => node.branch === 'Root');
  const awarenessNode = content.nodes.find((node) => node.branch === 'Awareness');
  const embodimentNode = content.nodes.find((node) => node.branch === 'Embodiment');
  const fieldNode = content.nodes.find((node) => node.branch === 'Field');
  const masteryNode = content.nodes.find((node) => node.branch === 'Mastery');

  if (!rootNode || !awarenessNode || !embodimentNode || !fieldNode || !masteryNode) {
    throw new Error(`Perk Tree V2 is missing a required node for ${content.id}`);
  }

  return {
    id: content.id,
    mainQuestId: content.mainQuestId,
    mainQuestName: content.mainQuestName,
    sourceLine: content.sourceLine,
    questState: content.questState,
    subtitle: content.subtitle,
    progress: {
      title: 'Quest Path',
      items: ['3 emerging capacities', '1 mastery path'],
    },
    rootNode: {
      id: `root-${content.mainQuestId}`,
      name: rootNode.name,
      shortLabel: rootNode.name,
      type: 'Root',
      state: 'Core',
      description: rootNode.description,
      effect: rootNode.effect,
      pathRole: rootNode.developmentCue,
      developmentNote: rootNode.masteryMarker,
    },
    branchNodes: [
      {
        id: `perk-awareness-${content.mainQuestId}`,
        name: awarenessNode.name,
        shortLabel: awarenessNode.name,
        branch: 'Awareness',
        type: 'Perk',
        state: 'Emerging',
        description: awarenessNode.description,
        effect: awarenessNode.effect,
        developmentCue: awarenessNode.developmentCue,
        masteryMarker: awarenessNode.masteryMarker,
      },
      {
        id: `perk-embodiment-${content.mainQuestId}`,
        name: embodimentNode.name,
        shortLabel: embodimentNode.name,
        branch: 'Embodiment',
        type: 'Perk',
        state: 'Emerging',
        description: embodimentNode.description,
        effect: embodimentNode.effect,
        developmentCue: embodimentNode.developmentCue,
        masteryMarker: embodimentNode.masteryMarker,
      },
      {
        id: `perk-field-${content.mainQuestId}`,
        name: fieldNode.name,
        shortLabel: fieldNode.name,
        branch: 'Field',
        type: 'Perk',
        state: 'Emerging',
        description: fieldNode.description,
        effect: fieldNode.effect,
        developmentCue: fieldNode.developmentCue,
        masteryMarker: fieldNode.masteryMarker,
      },
    ],
    masteryNode: {
      id: `mastery-${content.mainQuestId}`,
      name: masteryNode.name,
      shortLabel: masteryNode.name,
      type: 'Mastery',
      state: 'Mastery',
      description: masteryNode.description,
      effect: masteryNode.effect,
      integrationPath: masteryNode.developmentCue,
      masteryMarker: masteryNode.masteryMarker,
    },
    v2Nodes: content.nodes,
  };
}

function countWords(value: string): number {
  return value.trim().split(/\s+/).filter(Boolean).length;
}

function isDistinct(left: string, right: string): boolean {
  return left.trim() !== right.trim();
}

function hasQuestKeyStructure(value: string): boolean {
  const segments = value.split(/->|→/).map((segment) => segment.trim()).filter(Boolean);
  return segments.length >= 3;
}

// Pairs that share an identity string by design and must not be flagged as duplicates.
const EXPLICIT_ALLOW_PAIRS: Array<[string, string]> = [
  ['hero.mainQuest', 'perkTree.root.name'],
];

function isAllowedPair(path1: string, path2: string): boolean {
  return EXPLICIT_ALLOW_PAIRS.some(
    ([a, b]) => (a === path1 && b === path2) || (a === path2 && b === path1),
  );
}

const PERK_BRANCH_PREFIX: Record<string, string> = {
  Root: 'root',
  Awareness: 'awareness',
  Embodiment: 'embodiment',
  Field: 'field',
  Mastery: 'mastery',
};

export function extractV2Fields(
  content: MainQuestContentEntryV2,
  perkTree: MainQuestPerkTreeV2,
): FieldDescriptor[] {
  const fields: FieldDescriptor[] = [];

  function add(path: string, value: string | undefined, contentType: ContentType) {
    const v = value?.trim();
    if (v) fields.push({ path, value: v, contentType });
  }

  add('hero.mainQuest', content.hero.mainQuest, 'identity');
  add('hero.questState', content.hero.questState, 'identity');
  add('hero.atmosphericSubtitle', content.hero.atmosphericSubtitle, 'behavioral');

  add('questBrief.mission', content.questBrief.mission, 'instructional');
  add('questBrief.fieldPrompt', content.questBrief.fieldPrompt, 'instructional');
  add('questBrief.livePrompt', content.questBrief.livePrompt, 'instructional');

  add('fieldBriefing.whatThisQuestIsAbout', content.fieldBriefing.whatThisQuestIsAbout, 'behavioral');
  add('fieldBriefing.whyThisMattersNow', content.fieldBriefing.whyThisMattersNow, 'behavioral');
  add('fieldBriefing.primaryRecognitionTrigger', content.fieldBriefing.primaryRecognitionTrigger, 'behavioral');
  add('fieldBriefing.livePrompt', content.fieldBriefing.livePrompt, 'instructional');

  add('assetsAndFriction.questTrap', content.assetsAndFriction.questTrap, 'behavioral');
  content.assetsAndFriction.questAssets.forEach((a, i) =>
    add(`assetsAndFriction.questAssets[${i}]`, a, 'capability'),
  );
  content.assetsAndFriction.frictionSignals.forEach((s, i) =>
    add(`assetsAndFriction.frictionSignals[${i}]`, s, 'behavioral'),
  );
  add('assetsAndFriction.livePrompt', content.assetsAndFriction.livePrompt, 'instructional');

  content.groundingEffect.groundingProtocol.forEach((p, i) =>
    add(`groundingEffect.groundingProtocol[${i}]`, p, 'somatic'),
  );
  add('groundingEffect.somaticShift', content.groundingEffect.somaticShift, 'somatic');
  add('groundingEffect.bodyCheckPrompt', content.groundingEffect.bodyCheckPrompt, 'somatic');

  add('unlockCondition.questKey', content.unlockCondition.questKey, 'instructional');
  add('unlockCondition.embodiedSignal', content.unlockCondition.embodiedSignal, 'somatic');
  add('unlockCondition.ritualPrompt', content.unlockCondition.ritualPrompt, 'instructional');
  add('unlockCondition.alignmentReminder', content.unlockCondition.alignmentReminder, 'behavioral');
  add('unlockCondition.livePrompt', content.unlockCondition.livePrompt, 'instructional');

  content.driftPattern.forEach((d, i) =>
    add(`driftPattern[${i}]`, d, 'behavioral'),
  );

  for (const node of perkTree.nodes) {
    const prefix = `perkTree.${PERK_BRANCH_PREFIX[node.branch] ?? node.branch.toLowerCase()}`;
    add(`${prefix}.name`, node.name, 'identity');
    const descType: ContentType = node.branch === 'Embodiment' ? 'somatic' : 'behavioral';
    add(`${prefix}.description`, node.description, descType);
    add(`${prefix}.effect`, node.effect, 'capability');
    const cueType: ContentType = node.branch === 'Embodiment' ? 'somatic' : 'instructional';
    add(`${prefix}.developmentCue`, node.developmentCue, cueType);
    add(`${prefix}.masteryMarker`, node.masteryMarker, 'capability');
  }

  return fields;
}

export function detectContentTypeDuplicates(fields: FieldDescriptor[]): DuplicateConflict[] {
  const conflicts: DuplicateConflict[] = [];
  const byTypeAndValue = new Map<string, FieldDescriptor[]>();

  for (const field of fields) {
    const key = `${field.contentType}::${field.value.toLowerCase()}`;
    const group = byTypeAndValue.get(key) ?? [];
    group.push(field);
    byTypeAndValue.set(key, group);
  }

  for (const [key, group] of byTypeAndValue) {
    if (group.length < 2) continue;

    const conflictPaths: string[] = [];
    for (let i = 0; i < group.length; i++) {
      for (let j = i + 1; j < group.length; j++) {
        if (!isAllowedPair(group[i].path, group[j].path)) {
          if (!conflictPaths.includes(group[i].path)) conflictPaths.push(group[i].path);
          if (!conflictPaths.includes(group[j].path)) conflictPaths.push(group[j].path);
        }
      }
    }

    if (conflictPaths.length >= 2) {
      const contentType = key.split('::')[0] as ContentType;
      conflicts.push({ contentType, value: group[0].value, paths: conflictPaths });
    }
  }

  return conflicts;
}

export function validateMainQuestV2Content(
  content: MainQuestContentEntryV2,
  perkTree: MainQuestPerkTreeV2,
): string[] {
  const issues: string[] = [];
  const trigger = content.fieldBriefing.primaryRecognitionTrigger;
  const previews = [
    content.questBrief.collapsedPreview,
    content.fieldBriefing.collapsedPreview,
    content.assetsAndFriction.collapsedPreview,
    content.groundingEffect.collapsedPreview,
    content.unlockCondition.collapsedPreview,
  ];

  if (!isDistinct(content.questBrief.collapsedPreview, trigger)) {
    issues.push('questBrief.collapsedPreview must not equal fieldBriefing.primaryRecognitionTrigger');
  }

  if (!isDistinct(content.hero.atmosphericSubtitle, trigger)) {
    issues.push('hero.atmosphericSubtitle must not equal fieldBriefing.primaryRecognitionTrigger');
  }

  if (!isDistinct(content.unlockCondition.embodiedSignal, trigger)) {
    issues.push('unlockCondition.embodiedSignal must not equal fieldBriefing.primaryRecognitionTrigger');
  }

  if (content.groundingEffect.groundingProtocol.some((item) => content.driftPattern.includes(item))) {
    issues.push('groundingEffect.groundingProtocol must not reuse driftPattern');
  }

  if (!trigger.trim()) {
    issues.push('fieldBriefing.primaryRecognitionTrigger must exist');
  }

  if (!hasQuestKeyStructure(content.unlockCondition.questKey)) {
    issues.push('unlockCondition.questKey must contain Action + Constraint + Consequence');
  }

  if (previews.some((preview) => countWords(preview) >= 14)) {
    issues.push('all collapsed previews must be under 14 words');
  }

  for (const node of perkTree.nodes) {
    if (!isDistinct(node.description, content.assetsAndFriction.questTrap)) {
      issues.push(`perk node "${node.name}" description must not equal questTrap`);
    }

    if (!isDistinct(node.effect, trigger)) {
      issues.push(`perk node "${node.name}" effect must not equal primaryRecognitionTrigger`);
    }

    if (content.groundingEffect.groundingProtocol.includes(node.masteryMarker)) {
      issues.push(`perk node "${node.name}" masteryMarker must not equal groundingProtocol`);
    }
  }

  // Content-type duplicate check: flag same-type exact matches not covered by allow pairs.
  const fields = extractV2Fields(content, perkTree);
  const duplicates = detectContentTypeDuplicates(fields);
  for (const dup of duplicates) {
    const snippet = dup.value.length > 60 ? `${dup.value.substring(0, 60)}…` : dup.value;
    issues.push(
      `[${dup.contentType}] duplicate: "${snippet}" found at ${dup.paths.join(' and ')}`,
    );
  }

  return issues;
}

function mapIntegrationSeedToEntry(seed: GateLineIntegrationSeed): MainQuestContentEntry {
  const schemaPrimaryHeader =
    COMMAND_MODE_SCHEMA_PRIMARY_HEADERS[seed.gateLine] || seed.title;

  return {
    id: createMainQuestId(seed.gate, seed.line),
    sphere: 'Purpose',
    gate: seed.gate,
    line: seed.line,
    worldLabel: 'MAIN QUEST',
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

const gate1 = gate1Data as unknown as { mainQuestContent: MainQuestContentEntryV2[]; perkTrees: MainQuestPerkTreeV2[] };
const gate2 = gate2Data as unknown as { mainQuestContent: MainQuestContentEntryV2[]; perkTrees: MainQuestPerkTreeV2[] };
const gate11 = gate11Data as unknown as { mainQuestContent: MainQuestContentEntryV2[]; perkTrees: MainQuestPerkTreeV2[] };
const gate34 = gate34Data as unknown as { mainQuestContent: MainQuestContentEntryV2[]; perkTrees: MainQuestPerkTreeV2[] };
const gate39 = gate39Data as unknown as { mainQuestContent: MainQuestContentEntryV2[]; perkTrees: MainQuestPerkTreeV2[] };
const gate40 = gate40Data as unknown as { mainQuestContent: MainQuestContentEntryV2[]; perkTrees: MainQuestPerkTreeV2[] };
const gate41 = gate41Data as unknown as { mainQuestContent: MainQuestContentEntryV2[]; perkTrees: MainQuestPerkTreeV2[] };
const gate44 = gate44Data as unknown as { mainQuestContent: MainQuestContentEntryV2[]; perkTrees: MainQuestPerkTreeV2[] };

export const mainQuestV2Registry: Record<string, MainQuestContentEntryV2> = {
  '59.1': mainQuest591V2,
  '59.2': mainQuest592V2,
  '59.3': mainQuest593V2,
  '59.4': mainQuest594V2,
  '59.5': mainQuest595V2,
  '59.6': mainQuest596V2,
  '64.1': mainQuest641V2,
  '64.2': mainQuest642V2,
  '64.3': mainQuest643V2,
  '64.4': mainQuest644V2,
  '64.5': mainQuest645V2,
  '64.6': mainQuest646V2,
  '1.1': gate1.mainQuestContent[0],
  '1.2': gate1.mainQuestContent[1],
  '1.3': gate1.mainQuestContent[2],
  '1.4': gate1.mainQuestContent[3],
  '1.5': gate1.mainQuestContent[4],
  '1.6': gate1.mainQuestContent[5],
  '2.1': gate2.mainQuestContent[0],
  '2.2': gate2.mainQuestContent[1],
  '2.3': gate2.mainQuestContent[2],
  '2.4': gate2.mainQuestContent[3],
  '2.5': gate2.mainQuestContent[4],
  '2.6': gate2.mainQuestContent[5],
  '11.1': gate11.mainQuestContent[0],
  '11.2': gate11.mainQuestContent[1],
  '11.3': gate11.mainQuestContent[2],
  '11.4': gate11.mainQuestContent[3],
  '11.5': gate11.mainQuestContent[4],
  '11.6': gate11.mainQuestContent[5],
  '34.1': gate34.mainQuestContent[0],
  '34.2': gate34.mainQuestContent[1],
  '34.3': gate34.mainQuestContent[2],
  '34.4': gate34.mainQuestContent[3],
  '34.5': gate34.mainQuestContent[4],
  '34.6': gate34.mainQuestContent[5],
  '39.1': gate39.mainQuestContent[0],
  '39.2': gate39.mainQuestContent[1],
  '39.3': gate39.mainQuestContent[2],
  '39.4': gate39.mainQuestContent[3],
  '39.5': gate39.mainQuestContent[4],
  '39.6': gate39.mainQuestContent[5],
  '40.1': gate40.mainQuestContent[0],
  '40.2': gate40.mainQuestContent[1],
  '40.3': gate40.mainQuestContent[2],
  '40.4': gate40.mainQuestContent[3],
  '40.5': gate40.mainQuestContent[4],
  '40.6': gate40.mainQuestContent[5],
  '41.1': gate41.mainQuestContent[0],
  '41.2': gate41.mainQuestContent[1],
  '41.3': gate41.mainQuestContent[2],
  '41.4': gate41.mainQuestContent[3],
  '41.5': gate41.mainQuestContent[4],
  '41.6': gate41.mainQuestContent[5],
  '44.1': gate44.mainQuestContent[0],
  '44.2': gate44.mainQuestContent[1],
  '44.3': gate44.mainQuestContent[2],
  '44.4': gate44.mainQuestContent[3],
  '44.5': gate44.mainQuestContent[4],
  '44.6': gate44.mainQuestContent[5],
};

export const perkTreeV2Registry: Record<string, MainQuestPerkTreeV2> = {
  '59.1': perkTree591V2,
  '59.2': perkTree592V2,
  '59.3': perkTree593V2,
  '59.4': perkTree594V2,
  '59.5': perkTree595V2,
  '59.6': perkTree596V2,
  '64.1': perkTree641V2,
  '64.2': perkTree642V2,
  '64.3': perkTree643V2,
  '64.4': perkTree644V2,
  '64.5': perkTree645V2,
  '64.6': perkTree646V2,
  '1.1': gate1.perkTrees[0],
  '1.2': gate1.perkTrees[1],
  '1.3': gate1.perkTrees[2],
  '1.4': gate1.perkTrees[3],
  '1.5': gate1.perkTrees[4],
  '1.6': gate1.perkTrees[5],
  '2.1': gate2.perkTrees[0],
  '2.2': gate2.perkTrees[1],
  '2.3': gate2.perkTrees[2],
  '2.4': gate2.perkTrees[3],
  '2.5': gate2.perkTrees[4],
  '2.6': gate2.perkTrees[5],
  '11.1': gate11.perkTrees[0],
  '11.2': gate11.perkTrees[1],
  '11.3': gate11.perkTrees[2],
  '11.4': gate11.perkTrees[3],
  '11.5': gate11.perkTrees[4],
  '11.6': gate11.perkTrees[5],
  '34.1': gate34.perkTrees[0],
  '34.2': gate34.perkTrees[1],
  '34.3': gate34.perkTrees[2],
  '34.4': gate34.perkTrees[3],
  '34.5': gate34.perkTrees[4],
  '34.6': gate34.perkTrees[5],
  '39.1': gate39.perkTrees[0],
  '39.2': gate39.perkTrees[1],
  '39.3': gate39.perkTrees[2],
  '39.4': gate39.perkTrees[3],
  '39.5': gate39.perkTrees[4],
  '39.6': gate39.perkTrees[5],
  '40.1': gate40.perkTrees[0],
  '40.2': gate40.perkTrees[1],
  '40.3': gate40.perkTrees[2],
  '40.4': gate40.perkTrees[3],
  '40.5': gate40.perkTrees[4],
  '40.6': gate40.perkTrees[5],
  '41.1': gate41.perkTrees[0],
  '41.2': gate41.perkTrees[1],
  '41.3': gate41.perkTrees[2],
  '41.4': gate41.perkTrees[3],
  '41.5': gate41.perkTrees[4],
  '41.6': gate41.perkTrees[5],
  '44.1': gate44.perkTrees[0],
  '44.2': gate44.perkTrees[1],
  '44.3': gate44.perkTrees[2],
  '44.4': gate44.perkTrees[3],
  '44.5': gate44.perkTrees[4],
  '44.6': gate44.perkTrees[5],
};

export const COMMAND_MODE_MAIN_QUEST_ENTRIES: MainQuestContentEntry[] = gate59MainQuestContent.map(
  (seed) => {
    const v2Content = mainQuestV2Registry[seed.gateLine];
    const v2PerkTree = perkTreeV2Registry[seed.gateLine];

    if (v2Content && v2PerkTree) {
      return mapV2ContentToEntry(v2Content, v2PerkTree.id);
    }

    return mapIntegrationSeedToEntry(seed);
  },
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
    const v2PerkTree = perkTreeV2Registry[perkSeed.gateLine];

    if (v2PerkTree) {
      const tree = mapV2PerkTreeToTree(v2PerkTree);
      return [tree.id, tree];
    }
    const entry = COMMAND_MODE_MAIN_QUEST_ENTRY_MAP_BY_GATE_LINE.get(gateLineKey(perkSeed.gate, perkSeed.line))
      || mainQuest592Seed;
    const tree = mapPerkSeedToTree(perkSeed, entry);
    return [tree.id, tree];
  }),
);

export const perkTree592Mvp: MainQuestPerkTree =
  COMMAND_MODE_PERK_TREES[perkTree592V2.id];

export const mainQuest592V2ValidationIssues = validateMainQuestV2Content(
  mainQuest592V2,
  perkTree592V2,
);

export const mainQuestV2ValidationByGateLine: Record<string, string[]> = Object.fromEntries(
  Object.entries(mainQuestV2Registry).map(([gateLine, content]) => {
    const perkTree = perkTreeV2Registry[gateLine];

    if (!perkTree) {
      return [gateLine, ['Missing V2 perk tree']];
    }

    return [gateLine, validateMainQuestV2Content(content, perkTree)];
  }),
);

export const mainQuestV2RegistryValidationIssues = Object.entries(mainQuestV2ValidationByGateLine).flatMap(
  ([gateLine, issues]) => issues.map((issue) => `${gateLine}: ${issue}`),
);

if (mainQuestV2RegistryValidationIssues.length > 0) {
  console.warn(
    `Main Quest V2 registry validation warnings: ${mainQuestV2RegistryValidationIssues.join('; ')}`,
  );
}

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
  if (seed.v2) {
    return [
      { label: 'Mission', body: seed.v2.questBrief.mission, kind: 'primary' },
      { label: 'Field Prompt', body: seed.v2.questBrief.fieldPrompt, kind: 'prompt' },
    ];
  }

  return [
    { label: 'Mission', body: seed.questBrief, kind: 'primary' },
    { label: 'Field Prompt', body: seed.fieldPrompt, kind: 'prompt' },
  ];
}

function buildFieldBriefingBlocks(seed: MainQuestContentEntry): CommandModeQuestCardBlock[] {
  if (seed.v2) {
    return [
      {
        label: 'What This Quest Is About',
        body: seed.v2.fieldBriefing.whatThisQuestIsAbout,
        kind: 'primary',
      },
      {
        label: 'Why This Matters Now',
        body: seed.v2.fieldBriefing.whyThisMattersNow,
      },
      {
        label: 'Recognition Trigger',
        body: seed.v2.fieldBriefing.primaryRecognitionTrigger,
        kind: 'threshold',
      },
    ];
  }

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
  if (seed.v2) {
    return [
      { label: 'Quest Trap', body: seed.v2.assetsAndFriction.questTrap, kind: 'primary' },
      { label: 'Quest Assets', body: seed.v2.assetsAndFriction.questAssets.join(' · ') },
    ];
  }

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
  if (seed.v2) {
    return seed.v2.assetsAndFriction.frictionSignals;
  }

  if (seed.assetsAndFriction) {
    return [...seed.assetsAndFriction.frictionSignals, ...(seed.driftPattern || [])];
  }

  return seed.behavioralTells;
}

function buildGroundingBlocks(seed: MainQuestContentEntry): CommandModeQuestCardBlock[] {
  if (seed.v2) {
    return [
      {
        label: 'Grounding Protocol',
        body: seed.v2.groundingEffect.groundingProtocol.join(' · '),
        kind: 'primary',
      },
      {
        label: 'Somatic Shift',
        body: seed.v2.groundingEffect.somaticShift,
      },
      {
        label: 'Body Check Prompt',
        body: seed.v2.groundingEffect.bodyCheckPrompt,
        kind: 'prompt',
      },
    ];
  }

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

export function buildCommandModeMainQuestModelV2(
  contentV2: MainQuestContentEntryV2,
  perkTreeV2: MainQuestPerkTreeV2,
): CommandModeMainQuestModel {
  const questBriefPresentation = COMMAND_MODE_LAYER_PRESENTATION['quest-brief'];
  const fieldBriefingPresentation = COMMAND_MODE_LAYER_PRESENTATION['field-briefing'];
  const assetsFrictionPresentation = COMMAND_MODE_LAYER_PRESENTATION['assets-friction'];
  const groundingEffectPresentation = COMMAND_MODE_LAYER_PRESENTATION['grounding-effect'];
  const unlockConditionPresentation = COMMAND_MODE_LAYER_PRESENTATION['unlock-condition'];
  const perkTreePresentation = COMMAND_MODE_LAYER_PRESENTATION['mini-perk-preview'];
  const gatewayRows = [
    ...perkTreeV2.nodes
      .filter((node) => node.branch === 'Awareness' || node.branch === 'Embodiment' || node.branch === 'Field')
      .map((node) => `${node.branch} · ${node.name}`),
    `Mastery · ${perkTreeV2.nodes.find((node) => node.branch === 'Mastery')?.name || 'Mastery'}`,
  ];

  return {
    id: createMainQuestId(contentV2.gate, contentV2.line),
    sectionLabel: 'Main Quest',
    hero: {
      worldLabel: 'MAIN QUEST',
      mainQuest: contentV2.hero.mainQuest,
      sourceLine: contentV2.hero.sourceLine,
      questState: contentV2.hero.questState,
      atmosphericSubtitle: contentV2.hero.atmosphericSubtitle,
    },
    cards: [
      {
        id: 'quest-brief',
        title: questBriefPresentation.title,
        tone: questBriefPresentation.tone,
        imagePath: questBriefPresentation.imagePath,
        preview: contentV2.questBrief.collapsedPreview,
        livePrompt: contentV2.questBrief.livePrompt,
        blocks: [
          { label: 'Mission', body: contentV2.questBrief.mission, kind: 'primary' },
          { label: 'Field Prompt', body: contentV2.questBrief.fieldPrompt, kind: 'prompt' },
        ],
      },
      {
        id: 'field-briefing',
        title: fieldBriefingPresentation.title,
        tone: fieldBriefingPresentation.tone,
        imagePath: fieldBriefingPresentation.imagePath,
        preview: contentV2.fieldBriefing.collapsedPreview,
        livePrompt: contentV2.fieldBriefing.livePrompt,
        blocks: [
          {
            label: 'What This Quest Is About',
            body: contentV2.fieldBriefing.whatThisQuestIsAbout,
            kind: 'primary',
          },
          {
            label: 'Why This Matters Now',
            body: contentV2.fieldBriefing.whyThisMattersNow,
          },
          {
            label: 'Recognition Trigger',
            body: contentV2.fieldBriefing.primaryRecognitionTrigger,
            kind: 'threshold',
          },
        ],
      },
      {
        id: 'assets-friction',
        title: assetsFrictionPresentation.title,
        tone: assetsFrictionPresentation.tone,
        imagePath: assetsFrictionPresentation.imagePath,
        preview: contentV2.assetsAndFriction.collapsedPreview,
        livePrompt: contentV2.assetsAndFriction.livePrompt,
        blocks: [
          { label: 'Quest Trap', body: contentV2.assetsAndFriction.questTrap, kind: 'primary' },
          { label: 'Quest Assets', body: contentV2.assetsAndFriction.questAssets.join(' · ') },
        ],
        chips: contentV2.assetsAndFriction.frictionSignals,
      },
      {
        id: 'grounding-effect',
        title: groundingEffectPresentation.title,
        tone: groundingEffectPresentation.tone,
        imagePath: groundingEffectPresentation.imagePath,
        preview: contentV2.groundingEffect.collapsedPreview,
        blocks: [
          {
            label: 'Grounding Protocol',
            body: contentV2.groundingEffect.groundingProtocol.join(' · '),
            kind: 'primary',
          },
          {
            label: 'Somatic Shift',
            body: contentV2.groundingEffect.somaticShift,
          },
          {
            label: 'Body Check Prompt',
            body: contentV2.groundingEffect.bodyCheckPrompt,
            kind: 'prompt',
          },
        ],
      },
      {
        id: 'unlock-condition',
        title: unlockConditionPresentation.title,
        tone: unlockConditionPresentation.tone,
        imagePath: unlockConditionPresentation.imagePath,
        emphasis: unlockConditionPresentation.emphasis,
        preview: contentV2.unlockCondition.collapsedPreview,
        livePrompt: contentV2.unlockCondition.livePrompt,
        blocks: [
          { label: 'Quest Key', body: contentV2.unlockCondition.questKey, kind: 'threshold' },
          { label: 'Embodied Signal', body: contentV2.unlockCondition.embodiedSignal },
          { label: 'Ritual Prompt', body: contentV2.unlockCondition.ritualPrompt, kind: 'prompt' },
          { label: 'Alignment Reminder', body: contentV2.unlockCondition.alignmentReminder, kind: 'reminder' },
        ],
      },
      {
        id: 'mini-perk-preview',
        title: perkTreePresentation.title,
        tone: perkTreePresentation.tone,
        imagePath: perkTreePresentation.imagePath,
        preview: 'Explore the capacities developing inside this Main Quest.',
        summary: perkTreeV2.subtitle,
        summaryRows: gatewayRows,
        footer: 'Open Perk Tree',
      },
    ],
  };
}

// Legacy fallback path.
// This may reuse content across UI layers.
// Do not use this path for newly migrated Main Quest entries.
export function buildCommandModeMainQuestModelLegacy(
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

export function getCommandModeMainQuestModel(gateLine: string): CommandModeMainQuestModel {
  const v2Content = mainQuestV2Registry[gateLine];
  const v2PerkTree = perkTreeV2Registry[gateLine];

  if (v2Content && v2PerkTree) {
    return buildCommandModeMainQuestModelV2(v2Content, v2PerkTree);
  }

  const legacyEntry = COMMAND_MODE_MAIN_QUEST_ENTRY_MAP_BY_GATE_LINE.get(gateLine);

  if (legacyEntry) {
    return buildCommandModeMainQuestModelLegacy(legacyEntry, getCommandModePerkTree(legacyEntry));
  }

  return buildCommandModeMainQuestModelLegacy(mainQuest592Seed, getCommandModePerkTree(mainQuest592Seed));
}

export function buildCommandModeMainQuestModel(
  seed: MainQuestContentEntry = mainQuest592Seed,
  perkTree: MainQuestPerkTree = getCommandModePerkTree(mainQuest592Seed),
): CommandModeMainQuestModel {
  const gateLine = seed.gateLine || `${seed.gate}.${seed.line}`;

  if (mainQuestV2Registry[gateLine] && perkTreeV2Registry[gateLine]) {
    return buildCommandModeMainQuestModelV2(mainQuestV2Registry[gateLine], perkTreeV2Registry[gateLine]);
  }

  return buildCommandModeMainQuestModelLegacy(seed, perkTree);
}
