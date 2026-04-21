import { HUMAN_MODE_CONTENT_BY_THEME, getHumanModeContent as getHumanModeContentByTheme } from './foundationHumanModeContent.js';

/**
 * Core Configuration Engine — V2
 *
 * Four tables that power the "Core Loadout / Core Configuration" card:
 *   Table 1 — TITHI_CCE        (5 rows)
 *   Table 2 — ELEMENT_CCE      (5 rows)
 *   Table 3 — LP_CCE           (12 rows — includes lp_tail + directional_vector)
 *   Table 4 — TITHI_ELEM_DYN   (25 rows — Standard + Operator content per combo)
 *
 * Two modes:
 *   Standard  — "Core Loadout"      — human / intuitive / gamified
 *   Operator  — "Core Configuration"— diagnostic / systemic / technical
 *
 * Standard reveal: "You're naturally wired to…" + simple_reveal_stem + lp_tail
 * Operator fields: operator_dynamic_pattern  +  directional_vector (separate)
 *
 * Recognition — two fields per dynamic (not 300):
 *   recognition_line_simple    → Standard  "Often this shows up as…"
 *   recognition_signal_operator→ Operator  "Recognition Signal"
 */

// ── Table 1 — Tithi ────────────────────────────────────────────────────────

export const TITHI_CCE = {
  nanda: {
    functional_name:     'Initiation & Opportunity',
    watchout_fragment:   'rushing into too many things',
    best_use_fragment:   'start intentionally',
  },
  bhadra: {
    functional_name:     'Support & Favorable Conditions',
    watchout_fragment:   'holding on to what should evolve',
    best_use_fragment:   'strengthen what supports growth',
  },
  jaya: {
    functional_name:     'Challenge & Activation',
    watchout_fragment:   'turning struggle into your default',
    best_use_fragment:   'use challenge to sharpen you',
  },
  rikta: {
    functional_name:     'Clearing & Receptivity',
    watchout_fragment:   'over-clearing or withdrawing too far',
    best_use_fragment:   'clear strategically',
  },
  purna: {
    functional_name:     'Completion & Revelation',
    watchout_fragment:   'holding on past completion',
    best_use_fragment:   'complete fully, then let go',
  },
};

// ── Table 2 — Elements ─────────────────────────────────────────────────────

export const ELEMENT_CCE = {
  Wood: {
    functional_name:   'Growth & Expansion',
    watchout_fragment: 'growing faster than your foundation',
    best_use_fragment: 'pair growth with structure',
  },
  Fire: {
    functional_name:   'Transformation & Visibility',
    watchout_fragment: 'burning through energy too quickly',
    best_use_fragment: 'use intensity with purpose',
  },
  Earth: {
    functional_name:   'Stability & Integration',
    watchout_fragment: 'taking on too much until you stall',
    best_use_fragment: 'stay grounded while carrying what matters',
  },
  Metal: {
    functional_name:   'Precision & Refinement',
    watchout_fragment: 'becoming too rigid or corrective',
    best_use_fragment: 'refine what matters most',
  },
  Water: {
    functional_name:   'Depth & Adaptability',
    watchout_fragment: 'slowing into stagnation',
    best_use_fragment: 'keep depth in motion',
  },
};

// ── Table 3 — Life Paths ───────────────────────────────────────────────────

export const LP_CCE = {
  1:  {
    outcome:            'Independent Initiation',
    operator_outcome_name: 'Independent Initiation',
    human_outcome_name:    'Growing Through Independent Initiation',
    lp_tail:            'so you can open a path that didn\'t exist before.',
    directional_vector: 'Orients toward self-directed emergence through original action and autonomous development.',
  },
  2:  {
    outcome:            'Meaningful Connection',
    operator_outcome_name: 'Meaningful Connection',
    human_outcome_name:    'Deepening Meaningful Connection',
    lp_tail:            'so you can build something real with others.',
    directional_vector: 'Orients toward meaningful connection through collaboration and sensitive attunement to others.',
  },
  3:  {
    outcome:            'Creative Transformation',
    operator_outcome_name: 'Creative Transformation',
    human_outcome_name:    'Living Creative Transformation',
    lp_tail:            'so you can make something only you could make.',
    directional_vector: 'Orients toward creative expression through authentic communication and original contribution.',
  },
  4:  {
    outcome:            'Enduring Structures',
    operator_outcome_name: 'Enduring Structures',
    human_outcome_name:    'Building What Endures',
    lp_tail:            'so you can build something that lasts.',
    directional_vector: 'Orients toward enduring structures through disciplined formation and systematic development.',
  },
  5:  {
    outcome:            'Adaptive Mastery',
    operator_outcome_name: 'Adaptive Mastery',
    human_outcome_name:    'Growing Into Adaptive Mastery',
    lp_tail:            'so you can keep growing as long as you\'re moving.',
    directional_vector: 'Orients toward disciplined freedom through progressive experience and adaptive mastery.',
  },
  6:  {
    outcome:            'Protective Responsibility',
    operator_outcome_name: 'Protective Responsibility',
    human_outcome_name:    'Carrying What Matters Responsibly',
    lp_tail:            'so you can be there for what truly matters.',
    directional_vector: 'Orients toward sustained care through responsible nurturing and service to others.',
  },
  7:  {
    outcome:            'Deep Understanding',
    operator_outcome_name: 'Deep Understanding',
    human_outcome_name:    'Growing Into Deep Understanding',
    lp_tail:            'so you can understand what others can\'t quite reach.',
    directional_vector: 'Orients toward deep understanding through inner investigation and reflective inquiry.',
  },
  8:  {
    outcome:            'Systemic Influence',
    operator_outcome_name: 'Systemic Influence',
    human_outcome_name:    'Creating Meaningful Systemic Influence',
    lp_tail:            'so you can build something that makes a real difference.',
    directional_vector: 'Orients toward meaningful impact through resource mastery and large-scale influence.',
  },
  9:  {
    outcome:            'Cyclical Integration',
    operator_outcome_name: 'Cyclical Integration',
    human_outcome_name:    'Living Through Cyclical Integration',
    lp_tail:            'so you can help bring things toward a meaningful close.',
    directional_vector: 'Orients toward completion and renewal through universal compassion and wisdom integration.',
  },
  11: {
    outcome:            'Visionary Insight',
    operator_outcome_name: 'Visionary Insight',
    human_outcome_name:    'Growing Into Visionary Insight',
    lp_tail:            'so you can help others see what\'s possible.',
    directional_vector: 'Orients toward visionary insight through inspired transmission and elevated perception.',
  },
  22: {
    outcome:            'Structural Innovation',
    operator_outcome_name: 'Structural Innovation',
    human_outcome_name:    'Creating Structural Innovation',
    lp_tail:            'so you can build systems that change how things work.',
    directional_vector: 'Orients toward transformative systems through masterful architecture and practical vision.',
  },
  33: {
    outcome:            'Awakened Service',
    operator_outcome_name: 'Awakened Service',
    human_outcome_name:    'Living Awakened Service',
    lp_tail:            'so you can serve in a way that heals.',
    directional_vector: 'Orients toward awakened service through compassionate teaching and healing transmission.',
  },
};

// ── Table 4 — Tithi × Element Dynamics ────────────────────────────────────
//
// Standard mode:
//   simple_reveal_stem          — continues "You're naturally wired to…"
//   recognition_line_simple     — "Often this shows up as…"
//   simple_natural_expression   — "What comes naturally…"
//   simple_developmental_force  — "What life teaches you…"
//   simple_pattern_statement    — "How it shows up…"
//
// Operator mode:
//   operator_dynamic_pattern        — "Dynamic Pattern"
//   recognition_signal_operator     — "Recognition Signal"
//   operator_natural_expression     — "Natural Expression"
//   operator_developmental_pressure — "Developmental Pressure"
//   operator_emergent_pattern       — "Emergent Pattern"
//
// Shared:
//   configuration_theme_name, watch_for, best_use

export const TITHI_ELEM_DYN = {
  'nanda:Wood': {
    configuration_theme_name:        'The Pioneer',
    watch_for:                       'Rushing ahead can create movement faster than foundations can support.',
    best_use:                        'Start intentionally, support what has real potential, and give growth structure.',
    simple_reveal_stem:              'move toward possibility before others are ready,',
    recognition_line_simple:         'You often act before others are ready and help things move when others hesitate.',
    simple_natural_expression:       'You like getting things started.',
    simple_developmental_force:      'Life teaches you by helping you try things and learn as you go.',
    simple_pattern_statement:        'You help things move when others are stuck.',
    operator_dynamic_pattern:        'Initiatory momentum through self-generated activation.',
    recognition_signal_operator:     'Recurring early activation prior to collective movement.',
    operator_natural_expression:     'Begins movement prior to external certainty.',
    operator_developmental_pressure: 'Growth occurs through risk, uncertainty, and emergent adaptation.',
    operator_emergent_pattern:       'Creates progress by activating movement where inertia dominates.',
  },
  'nanda:Fire': {
    configuration_theme_name:        'The Catalyst',
    watch_for:                       'Impulsiveness and over-intensity can create disruption without direction.',
    best_use:                        'Act decisively, direct intensity wisely, and let change serve what matters.',
    simple_reveal_stem:              'bring energy into stuck situations and push things forward,',
    recognition_line_simple:         'You often bring movement into situations that feel stuck or stagnant.',
    simple_natural_expression:       'You bring energy when things feel stuck.',
    simple_developmental_force:      'Life teaches you through change and surprises.',
    simple_pattern_statement:        'You help get things moving again.',
    operator_dynamic_pattern:        'Change initiation through disruptive energetic activation.',
    recognition_signal_operator:     'Repeated catalytic disruption of stagnant conditions.',
    operator_natural_expression:     'Destabilizes stagnation through catalytic intervention.',
    operator_developmental_pressure: 'Growth occurs through volatility, intensity, and abrupt transformation.',
    operator_emergent_pattern:       'Generates movement through disruption that reopens possibility.',
  },
  'nanda:Earth': {
    configuration_theme_name:        'The Foundation Starter',
    watch_for:                       'Starting too much can create commitments that become difficult to sustain.',
    best_use:                        'Begin with intention, build from solid footing, and develop what can endure.',
    simple_reveal_stem:              'start things in a way that can actually hold,',
    recognition_line_simple:         'You often care about getting things started in a way that can actually hold.',
    simple_natural_expression:       'You like starting things the right way.',
    simple_developmental_force:      'Life teaches you why strong beginnings matter.',
    simple_pattern_statement:        'You help things begin on solid ground.',
    operator_dynamic_pattern:        'Initiation stabilized through grounded structural formation.',
    recognition_signal_operator:     'Recurring emphasis on viability and structural soundness at initiation.',
    operator_natural_expression:     'Begins systems with emphasis on viability and support.',
    operator_developmental_pressure: 'Growth occurs through responsibility, consequence, and foundational testing.',
    operator_emergent_pattern:       'Creates durable beginnings through stabilized initiation.',
  },
  'nanda:Metal': {
    configuration_theme_name:        'The Strategist',
    watch_for:                       'Overthinking can slow action, while impulsiveness can bypass necessary refinement.',
    best_use:                        'Act when timing is clear, refine what matters, and begin with purpose.',
    simple_reveal_stem:              'think ahead, find the right opening, and move at the right time,',
    recognition_line_simple:         'You often wait for the right opening rather than forcing action too early.',
    simple_natural_expression:       'You like thinking before you act.',
    simple_developmental_force:      'Life teaches you about timing and smart choices.',
    simple_pattern_statement:        'You help things begin at the right moment.',
    operator_dynamic_pattern:        'Initiatory precision through timing-mediated discernment.',
    recognition_signal_operator:     'Adaptive timing discernment preceding activation.',
    operator_natural_expression:     'Activates through calculated sequencing rather than impulse.',
    operator_developmental_pressure: 'Growth occurs through refinement of timing and strategic accuracy.',
    operator_emergent_pattern:       'Creates progress through precision in when and how action begins.',
  },
  'nanda:Water': {
    configuration_theme_name:        'The Timing Keeper',
    watch_for:                       'Waiting too long can turn discernment into hesitation.',
    best_use:                        'Trust timing, act when the opening appears, and keep momentum alive.',
    simple_reveal_stem:              'sense when the moment is right and move with it,',
    recognition_line_simple:         'You often sense when something is ready before others recognize the moment.',
    simple_natural_expression:       'You have a feel for when the time is right.',
    simple_developmental_force:      'Life teaches you patience and timing.',
    simple_pattern_statement:        'You help things happen when the moment is ready.',
    operator_dynamic_pattern:        'Initiation regulated through adaptive timing sensitivity.',
    recognition_signal_operator:     'Heightened readiness detection prior to collective awareness.',
    operator_natural_expression:     'Responds to conditions rather than forcing premature movement.',
    operator_developmental_pressure: 'Growth occurs through delay, timing correction, and recognition of readiness.',
    operator_emergent_pattern:       'Activates movement when conditions support successful emergence.',
  },

  'bhadra:Wood': {
    configuration_theme_name:        'The Cultivator',
    watch_for:                       'Supporting too much can enable what should mature through challenge.',
    best_use:                        'Strengthen what nourishes growth and allow what is weak to evolve.',
    simple_reveal_stem:              'help things grow by creating the conditions they need,',
    recognition_line_simple:         'You often help strengthen people or projects by supporting what has real potential.',
    simple_natural_expression:       'You like helping things grow.',
    simple_developmental_force:      'Life teaches you how to care for what matters.',
    simple_pattern_statement:        'You help people and things become stronger.',
    operator_dynamic_pattern:        'Growth reinforcement through supportive developmental conditions.',
    recognition_signal_operator:     'Repeated reinforcement of developmental potential through supportive conditions.',
    operator_natural_expression:     'Strengthens potential through nourishment and sustained support.',
    operator_developmental_pressure: 'Growth occurs through responsibility, care, and long-term maintenance.',
    operator_emergent_pattern:       'Develops strength by reinforcing what supports healthy growth.',
  },
  'bhadra:Fire': {
    configuration_theme_name:        'The Stabilizer',
    watch_for:                       'Trying to stabilize everything can resist necessary transformation.',
    best_use:                        'Support change without controlling it, and stabilize what truly matters.',
    simple_reveal_stem:              'hold things steady when the world around you gets messy,',
    recognition_line_simple:         'You often bring steadiness when others feel reactive or overwhelmed.',
    simple_natural_expression:       'You help calm things down when life feels messy.',
    simple_developmental_force:      'Life teaches you how to stay steady during change.',
    simple_pattern_statement:        'You help others feel grounded.',
    operator_dynamic_pattern:        'Transformational regulation through stabilizing intervention.',
    recognition_signal_operator:     'Recurring regulation of instability through stabilizing intervention.',
    operator_natural_expression:     'Moderates volatility by restoring coherence under change.',
    operator_developmental_pressure: 'Growth occurs through instability that tests structural resilience.',
    operator_emergent_pattern:       'Supports adaptation by preserving coherence during transformation.',
  },
  'bhadra:Earth': {
    configuration_theme_name:        'The Steward',
    watch_for:                       'Holding too much can turn care into burden.',
    best_use:                        'Support what matters, release what drains, and steward what can endure.',
    simple_reveal_stem:              'care for what matters and keep it strong,',
    recognition_line_simple:         'You often take responsibility for helping important things stay strong.',
    simple_natural_expression:       'You like taking care of what matters.',
    simple_developmental_force:      'Life teaches you responsibility.',
    simple_pattern_statement:        'You help things stay strong and supported.',
    operator_dynamic_pattern:        'Supportive stabilization through responsibility-based reinforcement.',
    recognition_signal_operator:     'Repeated preservation of long-term structural integrity.',
    operator_natural_expression:     'Strengthens systems through preservation and sustained support.',
    operator_developmental_pressure: 'Growth occurs through responsibility, burden, and discernment.',
    operator_emergent_pattern:       'Creates stability by reinforcing what holds long-term value.',
  },
  'bhadra:Metal': {
    configuration_theme_name:        'The Architect',
    watch_for:                       'Over-structuring can make support feel rigid instead of life-giving.',
    best_use:                        'Create order that strengthens life, not control that limits it.',
    simple_reveal_stem:              'see how things could work better and help make them work,',
    recognition_line_simple:         'You often see how things could be organized or designed better.',
    simple_natural_expression:       'You like making things work better.',
    simple_developmental_force:      'Life teaches you how structure helps things succeed.',
    simple_pattern_statement:        'You help improve how things are organized.',
    operator_dynamic_pattern:        'Structural intelligence through ordered systemic design.',
    recognition_signal_operator:     'Recurring detection of systemic inefficiency requiring restructuring.',
    operator_natural_expression:     'Identifies inefficiency and reorganizes toward greater coherence.',
    operator_developmental_pressure: 'Growth occurs through structural failure, redesign, and refinement.',
    operator_emergent_pattern:       'Improves systems through intelligent restructuring.',
  },
  'bhadra:Water': {
    configuration_theme_name:        'The Wise Guardian',
    watch_for:                       'Protectiveness can become over-caution or retreat.',
    best_use:                        'Protect what matters, trust timing, and let wisdom guide support.',
    simple_reveal_stem:              'protect what feels important before others realize it needs protecting,',
    recognition_line_simple:         'You often protect what feels important even when others overlook its value.',
    simple_natural_expression:       'You protect what feels important.',
    simple_developmental_force:      'Life teaches you what deserves care.',
    simple_pattern_statement:        'You help keep what matters safe.',
    operator_dynamic_pattern:        'Protective stabilization through depth-guided preservation.',
    recognition_signal_operator:     'Repeated preservation response toward high-value structures.',
    operator_natural_expression:     'Protects what carries enduring significance.',
    operator_developmental_pressure: 'Growth occurs through caution, vulnerability, and protective discernment.',
    operator_emergent_pattern:       'Creates support through intelligent preservation of what matters.',
  },

  'jaya:Wood': {
    configuration_theme_name:        'The Challenger',
    watch_for:                       'Constant struggle can become an identity instead of a catalyst.',
    best_use:                        'Use challenge to develop strength, not to define who you are.',
    simple_reveal_stem:              'grow by meeting hard things directly,',
    recognition_line_simple:         'You often grow stronger by facing what others avoid.',
    simple_natural_expression:       'You grow by facing hard things.',
    simple_developmental_force:      'Life teaches you strength through challenge.',
    simple_pattern_statement:        'You help turn struggle into growth.',
    operator_dynamic_pattern:        'Growth generation through resistance-mediated strengthening.',
    recognition_signal_operator:     'Recurring conversion of resistance into developmental engagement.',
    operator_natural_expression:     'Engages friction as developmental stimulus.',
    operator_developmental_pressure: 'Growth occurs through challenge, conflict, and adaptive strain.',
    operator_emergent_pattern:       'Creates development by converting resistance into strength.',
  },
  'jaya:Fire': {
    configuration_theme_name:        'The Forge',
    watch_for:                       'Pressure and intensity can keep you fighting when it is time to build.',
    best_use:                        'Channel pressure wisely, use intensity with purpose, and let challenge forge clarity.',
    simple_reveal_stem:              'get stronger through pressure,',
    recognition_line_simple:         'You often turn pressure into momentum rather than letting it stop you.',
    simple_natural_expression:       'Hard things often make you stronger.',
    simple_developmental_force:      'Life teaches you through pressure.',
    simple_pattern_statement:        'You turn challenge into strength.',
    operator_dynamic_pattern:        'Transformation through pressure-amplified strengthening.',
    recognition_signal_operator:     'Repeated transformation of sustained pressure into strengthening force.',
    operator_natural_expression:     'Uses intensity as a force for structural growth.',
    operator_developmental_pressure: 'Growth occurs through sustained pressure and transformational stress.',
    operator_emergent_pattern:       'Generates strength by converting pressure into transformative momentum.',
  },
  'jaya:Earth': {
    configuration_theme_name:        'The Stronghold',
    watch_for:                       'Strength can harden into defensiveness or carrying too much alone.',
    best_use:                        'Stand firm where needed, stay flexible where possible, and build through discipline.',
    simple_reveal_stem:              'hold firm when everything around you gets difficult,',
    recognition_line_simple:         'You often remain steady when others begin to lose footing.',
    simple_natural_expression:       'You stay steady when things get hard.',
    simple_developmental_force:      'Life teaches you resilience.',
    simple_pattern_statement:        'You help others feel strong when things are tested.',
    operator_dynamic_pattern:        'Stability generation through resilient structural endurance.',
    recognition_signal_operator:     'Recurring structural endurance under sustained stress.',
    operator_natural_expression:     'Maintains integrity under sustained pressure.',
    operator_developmental_pressure: 'Growth occurs through burden, endurance, and sustained testing.',
    operator_emergent_pattern:       'Creates strength through structural resilience under stress.',
  },
  'jaya:Metal': {
    configuration_theme_name:        'The Master',
    watch_for:                       'Perfectionism under pressure can turn growth into self-criticism.',
    best_use:                        'Let challenge sharpen skill, not narrow possibility.',
    simple_reveal_stem:              'get better at things through practice and challenge,',
    recognition_line_simple:         'You often use challenge to sharpen skill rather than be defeated by it.',
    simple_natural_expression:       'You like getting better through practice.',
    simple_developmental_force:      'Life teaches you through refinement.',
    simple_pattern_statement:        'You help turn pressure into skill.',
    operator_dynamic_pattern:        'Refinement through pressure-mediated precision development.',
    recognition_signal_operator:     'Repeated refinement response triggered by performance pressure.',
    operator_natural_expression:     'Sharpens capability through disciplined correction.',
    operator_developmental_pressure: 'Growth occurs through challenge exposing areas for refinement.',
    operator_emergent_pattern:       'Develops mastery through iterative pressure-driven improvement.',
  },
  'jaya:Water': {
    configuration_theme_name:        'The Resilient Sage',
    watch_for:                       'Reflection can become retreat when action is required.',
    best_use:                        'Let insight guide action, and let difficulty deepen wisdom.',
    simple_reveal_stem:              'stay thoughtful and clear even when life is hard,',
    recognition_line_simple:         'You often stay thoughtful even when life is difficult.',
    simple_natural_expression:       'You stay thoughtful even when life is hard.',
    simple_developmental_force:      'Life teaches you wisdom through difficulty.',
    simple_pattern_statement:        'You help bring perspective when things feel hard.',
    operator_dynamic_pattern:        'Adaptive wisdom through resilience-integrated reflection.',
    recognition_signal_operator:     'Adaptive reflective stability maintained under hardship.',
    operator_natural_expression:     'Maintains reflective awareness under difficulty.',
    operator_developmental_pressure: 'Growth occurs through hardship that deepens adaptive insight.',
    operator_emergent_pattern:       'Creates perspective by integrating resilience with wisdom.',
  },

  'rikta:Wood': {
    configuration_theme_name:        'The Pruner',
    watch_for:                       'Cutting back too much can remove what needed support, not removal.',
    best_use:                        'Clear what blocks growth, then protect what deserves development.',
    simple_reveal_stem:              'clear away what isn\'t working so something healthier can grow,',
    recognition_line_simple:         'You often see what needs to be cleared away before healthier growth can happen.',
    simple_natural_expression:       'You notice what needs to be cleared away.',
    simple_developmental_force:      'Life teaches you through letting go.',
    simple_pattern_statement:        'You help make room for healthier growth.',
    operator_dynamic_pattern:        'Development through reduction-based clearing.',
    recognition_signal_operator:     'Recurring detection of obstruction prior to developmental correction.',
    operator_natural_expression:     'Removes obstruction that impedes healthy growth.',
    operator_developmental_pressure: 'Growth occurs through release, loss, and necessary subtraction.',
    operator_emergent_pattern:       'Strengthens development by clearing what weakens growth.',
  },
  'rikta:Fire': {
    configuration_theme_name:        'The Structural Reformer',
    watch_for:                       'Over-clearing and burnout can keep you correcting when it\'s time to build.',
    best_use:                        'Clear strategically, use intensity with purpose, and build for endurance.',
    simple_reveal_stem:              'fix what is weak first, so you can build something strong that lasts,',
    recognition_line_simple:         'You often see what needs fixing before others see what needs rebuilding.',
    simple_natural_expression:       'You notice when something isn\'t working and want to fix it.',
    simple_developmental_force:      'Life helps you grow through hard changes.',
    simple_pattern_statement:        'You make things stronger by fixing what is weak first.',
    operator_dynamic_pattern:        'Structural correction through pressure-mediated transformation.',
    recognition_signal_operator:     'Recurring detection of structural weakness prior to collective recognition.',
    operator_natural_expression:     'Identifies weakness, instability, or inefficiency prior to intervention.',
    operator_developmental_pressure: 'Growth occurs through destabilization, adaptive pressure, and structural stress.',
    operator_emergent_pattern:       'Improves systems through corrective disruption before durable reconstruction.',
  },
  'rikta:Earth': {
    configuration_theme_name:        'The Grounded Seer',
    watch_for:                       'Over-analysis can delay the action clarity is meant to support.',
    best_use:                        'Use discernment to clarify what matters, then ground it in action.',
    simple_reveal_stem:              'see what needs to be cleared before the next move is made,',
    recognition_line_simple:         'You often help others find clarity when things feel uncertain.',
    simple_natural_expression:       'You notice what needs clarity before action.',
    simple_developmental_force:      'Life teaches you how to see clearly.',
    simple_pattern_statement:        'You help others find direction.',
    operator_dynamic_pattern:        'Clarification through stability-guided discernment.',
    recognition_signal_operator:     'Repeated clarification response under conditions of ambiguity.',
    operator_natural_expression:     'Perceives what requires clarity before effective action.',
    operator_developmental_pressure: 'Growth occurs through uncertainty that develops discernment.',
    operator_emergent_pattern:       'Creates direction through grounded clarification.',
  },
  'rikta:Metal': {
    configuration_theme_name:        'The Refiner',
    watch_for:                       'Correction can become criticism when refinement loses proportion.',
    best_use:                        'Refine what matters, remove what weakens it, and preserve what has value.',
    simple_reveal_stem:              'notice what could be better and quietly make it so,',
    recognition_line_simple:         'You often notice what could be improved before others recognize the issue.',
    simple_natural_expression:       'You notice how things could be improved.',
    simple_developmental_force:      'Life teaches you through correction and learning.',
    simple_pattern_statement:        'You help make things better.',
    operator_dynamic_pattern:        'Strengthening through precision-based reduction.',
    recognition_signal_operator:     'Recurring precision detection of integrity weaknesses requiring refinement.',
    operator_natural_expression:     'Removes distortion through corrective refinement.',
    operator_developmental_pressure: 'Growth occurs through error, correction, and precision development.',
    operator_emergent_pattern:       'Improves integrity through intelligent refinement.',
  },
  'rikta:Water': {
    configuration_theme_name:        'The Deep Seer',
    watch_for:                       'Withdrawal and stagnation can keep insight from becoming lived wisdom.',
    best_use:                        'Create space, keep depth in motion, and let insight become action.',
    simple_reveal_stem:              'see beneath the surface and bring clarity from what you notice,',
    recognition_line_simple:         'You often perceive deeper patterns beneath what others take at face value.',
    simple_natural_expression:       'You notice deeper things others may miss.',
    simple_developmental_force:      'Life teaches you through reflection.',
    simple_pattern_statement:        'You help bring clarity by seeing beneath the surface.',
    operator_dynamic_pattern:        'Insight generation through depth-mediated perception.',
    recognition_signal_operator:     'Recurring depth-pattern recognition beneath surface-level perception.',
    operator_natural_expression:     'Detects underlying patterns beneath surface appearance.',
    operator_developmental_pressure: 'Growth occurs through ambiguity, reflection, and perceptual deepening.',
    operator_emergent_pattern:       'Creates clarity through depth-informed insight.',
  },

  'purna:Wood': {
    configuration_theme_name:        'The Harvester',
    watch_for:                       'Pushing for completion too early can interrupt natural maturation.',
    best_use:                        'Bring growth to completion in its right season.',
    simple_reveal_stem:              'help things reach their full potential and see them through to the end,',
    recognition_line_simple:         'You often help bring things to completion when others leave them unfinished.',
    simple_natural_expression:       'You like helping things reach completion.',
    simple_developmental_force:      'Life teaches you through endings and fulfillment.',
    simple_pattern_statement:        'You help bring things to completion.',
    operator_dynamic_pattern:        'Completion through fulfillment-oriented integration.',
    recognition_signal_operator:     'Recurring orientation toward fulfillment and coherent completion.',
    operator_natural_expression:     'Brings development toward coherent completion.',
    operator_developmental_pressure: 'Growth occurs through cycles of fulfillment, release, and renewal.',
    operator_emergent_pattern:       'Creates wholeness by guiding processes toward completion.',
  },
  'purna:Fire': {
    configuration_theme_name:        'The Illuminator',
    watch_for:                       'Intensity can turn completion into exhaustion.',
    best_use:                        'Bring clarity to completion, and let revelation serve wisdom.',
    simple_reveal_stem:              'bring clarity to what matters most,',
    recognition_line_simple:         'You often help others see something clearly that was previously hard to understand.',
    simple_natural_expression:       'You help bring clarity to what matters.',
    simple_developmental_force:      'Life teaches you through insight.',
    simple_pattern_statement:        'You help others see more clearly.',
    operator_dynamic_pattern:        'Clarity generation through revelatory integration.',
    recognition_signal_operator:     'Repeated revelation of hidden coherence or overlooked significance.',
    operator_natural_expression:     'Reveals what carries significance or hidden coherence.',
    operator_developmental_pressure: 'Growth occurs through realization, insight shifts, and expanded understanding.',
    operator_emergent_pattern:       'Creates clarity by illuminating what was previously unseen.',
  },
  'purna:Earth': {
    configuration_theme_name:        'The Integrator',
    watch_for:                       'Trying to hold everything together can become overextension.',
    best_use:                        'Integrate what belongs together, and release what does not.',
    simple_reveal_stem:              'help different pieces fit together into something whole,',
    recognition_line_simple:         'You often help connect separate pieces into something more whole.',
    simple_natural_expression:       'You like helping things fit together.',
    simple_developmental_force:      'Life teaches you how separate things can work as one.',
    simple_pattern_statement:        'You help create wholeness.',
    operator_dynamic_pattern:        'Coherence generation through systemic integration.',
    recognition_signal_operator:     'Recurring synthesis of disparate elements into systemic coherence.',
    operator_natural_expression:     'Connects disparate elements into functional wholeness.',
    operator_developmental_pressure: 'Growth occurs through complexity requiring higher-order coordination.',
    operator_emergent_pattern:       'Creates strength by integrating separate parts into greater coherence.',
  },
  'purna:Metal': {
    configuration_theme_name:        'The Finisher',
    watch_for:                       'Over-refining can prevent something from ever being finished.',
    best_use:                        'Finish with care, not perfection.',
    simple_reveal_stem:              'bring things to completion with real care,',
    recognition_line_simple:         'You often strengthen things by helping them reach a better conclusion.',
    simple_natural_expression:       'You care about finishing things well.',
    simple_developmental_force:      'Life teaches you through bringing things to completion.',
    simple_pattern_statement:        'You help strengthen outcomes.',
    operator_dynamic_pattern:        'Completion through precision-guided closure.',
    recognition_signal_operator:     'Recurring correction and closure of incomplete processes.',
    operator_natural_expression:     'Strengthens outcomes through refined completion.',
    operator_developmental_pressure: 'Growth occurs through unfinished processes requiring closure or correction.',
    operator_emergent_pattern:       'Improves outcomes through intelligent completion.',
  },
  'purna:Water': {
    configuration_theme_name:        'The Wisdom Keeper',
    watch_for:                       'Too much reflection can delay the renewal that completion invites.',
    best_use:                        'Let completion deepen wisdom, then let wisdom open what comes next.',
    simple_reveal_stem:              'turn what you\'ve lived through into something that helps others,',
    recognition_line_simple:         'You often help others through what you\'ve learned from experience.',
    simple_natural_expression:       'You learn deeply from experience.',
    simple_developmental_force:      'Life teaches you wisdom over time.',
    simple_pattern_statement:        'You help others through what you\'ve learned.',
    operator_dynamic_pattern:        'Wisdom generation through experience-integrated reflection.',
    recognition_signal_operator:     'Repeated conversion of lived experience into applied wisdom.',
    operator_natural_expression:     'Extracts meaning from lived experience over time.',
    operator_developmental_pressure: 'Growth occurs through endings, reflection, and experiential deepening.',
    operator_emergent_pattern:       'Creates wisdom by integrating experience into practical understanding.',
  },
};

// ── Operator Tactical Layer ────────────────────────────────────────────────
//
// Standard mode continues to use per-dynamic watch_for / best_use.
// Operator mode gets a distinct diagnostic layer:
//   failure_mode_operator
//   optimization_step_1_operator
//   optimization_step_2_operator
//   optimization_step_3_operator

const OPERATOR_TACTICS_BY_THEME = {
  'The Pioneer': {
    failure_mode_operator:       'Premature activation can trigger movement before conditions can support continuity.',
    optimization_step_1_operator:'Initiate from viable openings.',
    optimization_step_2_operator:'Regulate speed against structural readiness.',
    optimization_step_3_operator:'Sustain momentum through adaptive correction.',
  },
  'The Catalyst': {
    failure_mode_operator:       'Catalytic disruption can generate instability without constructive reorganization.',
    optimization_step_1_operator:'Apply disruption selectively.',
    optimization_step_2_operator:'Channel intensity toward transformation.',
    optimization_step_3_operator:'Stabilize change after activation.',
  },
  'The Foundation Starter': {
    failure_mode_operator:       'Overemphasis on foundation can delay necessary initiation.',
    optimization_step_1_operator:'Build sufficient structure.',
    optimization_step_2_operator:'Avoid over-securing before action.',
    optimization_step_3_operator:'Let stability support movement.',
  },
  'The Strategist': {
    failure_mode_operator:       'Excessive optimization can produce paralysis through over-calculation.',
    optimization_step_1_operator:'Use timing to support action.',
    optimization_step_2_operator:'Avoid analysis replacing movement.',
    optimization_step_3_operator:'Convert precision into execution.',
  },
  'The Timing Keeper': {
    failure_mode_operator:       'Over-reliance on readiness can delay activation beyond the true opening.',
    optimization_step_1_operator:'Trust timing signals.',
    optimization_step_2_operator:'Distinguish patience from avoidance.',
    optimization_step_3_operator:'Activate when readiness is sufficient.',
  },
  'The Cultivator': {
    failure_mode_operator:       'Supportive reinforcement can sustain what should no longer be developed.',
    optimization_step_1_operator:'Strengthen viable growth.',
    optimization_step_2_operator:'Withdraw support from what weakens integrity.',
    optimization_step_3_operator:'Reinforce what can mature.',
  },
  'The Stabilizer': {
    failure_mode_operator:       'Stabilization can become resistance to necessary change.',
    optimization_step_1_operator:'Preserve coherence under stress.',
    optimization_step_2_operator:'Allow instability where transformation is needed.',
    optimization_step_3_operator:'Support adaptation without rigidity.',
  },
  'The Steward': {
    failure_mode_operator:       'Responsibility accumulation can turn preservation into burden fixation.',
    optimization_step_1_operator:'Reinforce what matters.',
    optimization_step_2_operator:'Release unnecessary load.',
    optimization_step_3_operator:'Stabilize around long-term value.',
  },
  'The Architect': {
    failure_mode_operator:       'Structural optimization can become correction without practical movement.',
    optimization_step_1_operator:'Improve what increases coherence.',
    optimization_step_2_operator:'Avoid redesign for its own sake.',
    optimization_step_3_operator:'Translate structure into function.',
  },
  'The Wise Guardian': {
    failure_mode_operator:       'Protective preservation can become over-guarding that constrains development.',
    optimization_step_1_operator:'Protect what carries value.',
    optimization_step_2_operator:'Distinguish caution from contraction.',
    optimization_step_3_operator:'Let preservation support growth.',
  },
  'The Challenger': {
    failure_mode_operator:       'Continuous resistance engagement can normalize conflict as the primary growth mechanism.',
    optimization_step_1_operator:'Engage challenge selectively.',
    optimization_step_2_operator:'Use resistance to strengthen, not harden.',
    optimization_step_3_operator:'Convert friction into development.',
  },
  'The Forge': {
    failure_mode_operator:       'Pressure amplification can turn strengthening into destabilizing overload.',
    optimization_step_1_operator:'Regulate intensity constructively.',
    optimization_step_2_operator:'Convert pressure into transformation.',
    optimization_step_3_operator:'Stabilize after catalytic strengthening.',
  },
  'The Stronghold': {
    failure_mode_operator:       'Endurance fixation can preserve strain beyond its developmental usefulness.',
    optimization_step_1_operator:'Hold where resilience matters.',
    optimization_step_2_operator:'Release unnecessary structural tension.',
    optimization_step_3_operator:'Let endurance support adaptation.',
  },
  'The Master': {
    failure_mode_operator:       'Refinement pressure can become endless correction without completion.',
    optimization_step_1_operator:'Refine what increases capability.',
    optimization_step_2_operator:'Avoid perfection replacing progress.',
    optimization_step_3_operator:'Convert pressure into mastery.',
  },
  'The Resilient Sage': {
    failure_mode_operator:       'Reflective resilience can become detachment from necessary engagement.',
    optimization_step_1_operator:'Use perspective under pressure.',
    optimization_step_2_operator:'Avoid reflection replacing response.',
    optimization_step_3_operator:'Integrate wisdom into action.',
  },
  'The Pruner': {
    failure_mode_operator:       'Excessive reduction can remove what growth still requires.',
    optimization_step_1_operator:'Clear true obstruction.',
    optimization_step_2_operator:'Avoid reduction beyond necessity.',
    optimization_step_3_operator:'Let clearing support development.',
  },
  'The Structural Reformer': {
    failure_mode_operator:       'Corrective overextension can lock the system into persistent disruption rather than reconstruction.',
    optimization_step_1_operator:'Apply correction selectively.',
    optimization_step_2_operator:'Regulate pressure toward constructive transformation.',
    optimization_step_3_operator:'Stabilize around long-range structural endurance.',
  },
  'The Grounded Seer': {
    failure_mode_operator:       'Discernment can become over-analysis that delays necessary direction.',
    optimization_step_1_operator:'Clarify what matters.',
    optimization_step_2_operator:'Avoid perpetual interpretation.',
    optimization_step_3_operator:'Translate insight into grounded movement.',
  },
  'The Refiner': {
    failure_mode_operator:       'Precision correction can become over-refinement that fragments functional integrity.',
    optimization_step_1_operator:'Improve what strengthens integrity.',
    optimization_step_2_operator:'Avoid correction becoming compulsion.',
    optimization_step_3_operator:'Let refinement serve function.',
  },
  'The Deep Seer': {
    failure_mode_operator:       'Depth perception can become withdrawal into endless interpretation.',
    optimization_step_1_operator:'Trust deeper pattern recognition.',
    optimization_step_2_operator:'Avoid reflection without application.',
    optimization_step_3_operator:'Convert insight into clear action.',
  },
  'The Harvester': {
    failure_mode_operator:       'Completion orientation can force closure before integration is mature.',
    optimization_step_1_operator:'Complete what is ready.',
    optimization_step_2_operator:'Avoid premature closure.',
    optimization_step_3_operator:'Let fulfillment arise through integration.',
  },
  'The Illuminator': {
    failure_mode_operator:       'Insight generation can become over-illumination without grounded application.',
    optimization_step_1_operator:'Reveal what brings clarity.',
    optimization_step_2_operator:'Avoid insight detached from function.',
    optimization_step_3_operator:'Translate illumination into guidance.',
  },
  'The Integrator': {
    failure_mode_operator:       'Coherence-seeking can overbind systems that require differentiation.',
    optimization_step_1_operator:'Integrate what belongs together.',
    optimization_step_2_operator:'Preserve distinctions where necessary.',
    optimization_step_3_operator:'Build coherence without over-fusion.',
  },
  'The Finisher': {
    failure_mode_operator:       'Completion refinement can become endless improvement beyond functional sufficiency.',
    optimization_step_1_operator:'Complete what strengthens outcomes.',
    optimization_step_2_operator:'Avoid over-correcting finished work.',
    optimization_step_3_operator:'Let closure support integrity.',
  },
  'The Wisdom Keeper': {
    failure_mode_operator:       'Experience integration can become over-reliance on reflection at the expense of adaptation.',
    optimization_step_1_operator:'Extract wisdom from experience.',
    optimization_step_2_operator:'Avoid wisdom becoming rigidity.',
    optimization_step_3_operator:'Apply understanding in living systems.',
  },
};

for (const dynamic of Object.values(TITHI_ELEM_DYN)) {
  const operatorTactics = OPERATOR_TACTICS_BY_THEME[dynamic.configuration_theme_name];
  if (operatorTactics) Object.assign(dynamic, operatorTactics);
  const humanContent = HUMAN_MODE_CONTENT_BY_THEME[dynamic.configuration_theme_name];
  if (humanContent?.stable) {
    dynamic.human_reveal_statement = humanContent.stable.reveal;
    dynamic.recognition_line_simple = humanContent.stable.recognition;
    dynamic.simple_natural_expression = humanContent.stable.howYouNaturallyOperate;
    dynamic.simple_developmental_force = null;
    dynamic.simple_pattern_statement = null;
    dynamic.watch_for = humanContent.stable.baseWatchForDrift;
    dynamic.best_use = null;
    dynamic.base_watch_for_drift = humanContent.stable.baseWatchForDrift;
  }
}

// ── Generation Logic ───────────────────────────────────────────────────────

export function getDynamic(tithi, element) {
  return TITHI_ELEM_DYN[`${tithi}:${element}`] || null;
}

export function getHumanModeContent(tithi, element, lifePathNum) {
  const dynamic = getDynamic(tithi, element);
  return getHumanModeContentByTheme(dynamic?.configuration_theme_name, lifePathNum);
}

export function generateWatchFor(tithi, element, lifePathNum) {
  const humanContent = getHumanModeContent(tithi, element, lifePathNum);
  if (humanContent?.watchForDrift) return humanContent.watchForDrift;
  if (humanContent?.baseWatchForDrift) return humanContent.baseWatchForDrift;
  const t  = TITHI_CCE[tithi];
  const el = ELEMENT_CCE[element];
  const lp = LP_CCE[lifePathNum];
  if (!t || !el || !lp) return null;
  return `${cap(t.watchout_fragment)} and ${el.watchout_fragment}. This can make it harder to reach ${(lp.human_outcome_name || lp.outcome).toLowerCase()}.`;
}

export function generateBestUse(tithi, element, lifePathNum) {
  const humanContent = getHumanModeContent(tithi, element, lifePathNum);
  if (humanContent?.bestUse?.length) return humanContent.bestUse;
  const t  = TITHI_CCE[tithi];
  const el = ELEMENT_CCE[element];
  const lp = LP_CCE[lifePathNum];
  if (!t || !el || !lp) return null;
  return `${cap(t.best_use_fragment)}, ${el.best_use_fragment}, and stay oriented toward ${(lp.human_outcome_name || lp.outcome).toLowerCase()}.`;
}

function cap(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}
