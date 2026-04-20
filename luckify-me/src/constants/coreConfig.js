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
 * Standard reveal generation:
 *   "You're naturally wired to…"
 *   + dynamic.simple_reveal_stem
 *   + cceLp.lp_tail
 *
 * Operator fields displayed separately (never merged):
 *   dynamic.operator_dynamic_pattern
 *   cceLp.directional_vector
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
// lp_tail:           completes the Standard reveal stem sentence
// directional_vector: Operator mode — separate diagnostic field

export const LP_CCE = {
  1:  {
    outcome:             'New Pathways',
    lp_tail:             'so you can open a path that didn\'t exist before.',
    directional_vector:  'Orients toward pioneering new pathways through individual initiative and independent action.',
  },
  2:  {
    outcome:             'Meaningful Connection',
    lp_tail:             'so you can build something real with others.',
    directional_vector:  'Orients toward meaningful connection through collaboration and sensitive attunement to others.',
  },
  3:  {
    outcome:             'Creative Expression',
    lp_tail:             'so you can make something only you could make.',
    directional_vector:  'Orients toward creative expression through authentic communication and original contribution.',
  },
  4:  {
    outcome:             'Enduring Structures',
    lp_tail:             'so you can build something that lasts.',
    directional_vector:  'Orients toward enduring structures through disciplined formation and systematic development.',
  },
  5:  {
    outcome:             'Disciplined Freedom',
    lp_tail:             'so you can keep growing as long as you\'re moving.',
    directional_vector:  'Orients toward disciplined freedom through progressive experience and adaptive mastery.',
  },
  6:  {
    outcome:             'Sustained Care',
    lp_tail:             'so you can be there for what truly matters.',
    directional_vector:  'Orients toward sustained care through responsible nurturing and service to others.',
  },
  7:  {
    outcome:             'Deep Understanding',
    lp_tail:             'so you can understand what others can\'t quite reach.',
    directional_vector:  'Orients toward deep understanding through inner investigation and reflective inquiry.',
  },
  8:  {
    outcome:             'Meaningful Impact',
    lp_tail:             'so you can build something that makes a real difference.',
    directional_vector:  'Orients toward meaningful impact through resource mastery and large-scale influence.',
  },
  9:  {
    outcome:             'Completion and Renewal',
    lp_tail:             'so you can help bring things toward a meaningful close.',
    directional_vector:  'Orients toward completion and renewal through universal compassion and wisdom integration.',
  },
  11: {
    outcome:             'Visionary Insight',
    lp_tail:             'so you can help others see what\'s possible.',
    directional_vector:  'Orients toward visionary insight through inspired transmission and elevated perception.',
  },
  22: {
    outcome:             'Transformative Systems',
    lp_tail:             'so you can build systems that change how things work.',
    directional_vector:  'Orients toward transformative systems through masterful architecture and practical vision.',
  },
  33: {
    outcome:             'Awakened Service',
    lp_tail:             'so you can serve in a way that heals.',
    directional_vector:  'Orients toward awakened service through compassionate teaching and healing transmission.',
  },
};

// ── Table 4 — Tithi × Element Dynamics ────────────────────────────────────
//
// Standard mode fields:
//   simple_reveal_stem          — continues "You're naturally wired to…"
//   simple_natural_expression   — "What comes naturally…"
//   simple_developmental_force  — "What life teaches you…"
//   simple_pattern_statement    — "How it shows up…"
//
// Operator mode fields:
//   operator_dynamic_pattern        — "Dynamic Pattern"
//   operator_natural_expression     — "Natural Expression"
//   operator_developmental_pressure — "Developmental Pressure"
//   operator_emergent_pattern       — "Emergent Pattern"
//
// Shared across modes:
//   configuration_theme_name, recognition_line, watch_for, best_use

export const TITHI_ELEM_DYN = {
  'nanda:Wood': {
    configuration_theme_name:        'The Pioneer',
    recognition_line:                'You may have noticed you often move toward possibility before others are ready to act.',
    watch_for:                       'Rushing ahead can create movement faster than foundations can support.',
    best_use:                        'Start intentionally, support what has real potential, and give growth structure.',
    simple_reveal_stem:              'move toward possibility before others are ready,',
    simple_natural_expression:       'You like getting things started.',
    simple_developmental_force:      'Life teaches you by helping you try things and learn as you go.',
    simple_pattern_statement:        'You help things move when others are stuck.',
    operator_dynamic_pattern:        'Initiatory momentum through self-generated activation.',
    operator_natural_expression:     'Begins movement prior to external certainty.',
    operator_developmental_pressure: 'Growth occurs through risk, uncertainty, and emergent adaptation.',
    operator_emergent_pattern:       'Creates progress by activating movement where inertia dominates.',
  },
  'nanda:Fire': {
    configuration_theme_name:        'The Catalyst',
    recognition_line:                'You may have noticed movement often begins around you when you decide to engage.',
    watch_for:                       'Impulsiveness and over-intensity can create disruption without direction.',
    best_use:                        'Act decisively, direct intensity wisely, and let change serve what matters.',
    simple_reveal_stem:              'bring energy into stuck situations and push things forward,',
    simple_natural_expression:       'You bring energy when things feel stuck.',
    simple_developmental_force:      'Life teaches you through change and surprises.',
    simple_pattern_statement:        'You help get things moving again.',
    operator_dynamic_pattern:        'Change initiation through disruptive energetic activation.',
    operator_natural_expression:     'Destabilizes stagnation through catalytic intervention.',
    operator_developmental_pressure: 'Growth occurs through volatility, intensity, and abrupt transformation.',
    operator_emergent_pattern:       'Generates movement through disruption that reopens possibility.',
  },
  'nanda:Earth': {
    configuration_theme_name:        'The Foundation Starter',
    recognition_line:                'You may have noticed you care not just about starting, but about starting on solid footing.',
    watch_for:                       'Starting too much can create commitments that become difficult to sustain.',
    best_use:                        'Begin with intention, build from solid footing, and develop what can endure.',
    simple_reveal_stem:              'start things in a way that can actually hold,',
    simple_natural_expression:       'You like starting things the right way.',
    simple_developmental_force:      'Life teaches you why strong beginnings matter.',
    simple_pattern_statement:        'You help things begin on solid ground.',
    operator_dynamic_pattern:        'Initiation stabilized through grounded structural formation.',
    operator_natural_expression:     'Begins systems with emphasis on viability and support.',
    operator_developmental_pressure: 'Growth occurs through responsibility, consequence, and foundational testing.',
    operator_emergent_pattern:       'Creates durable beginnings through stabilized initiation.',
  },
  'nanda:Metal': {
    configuration_theme_name:        'The Strategist',
    recognition_line:                'You may have noticed you often sense both when to act and what needs refining first.',
    watch_for:                       'Overthinking can slow action, while impulsiveness can bypass necessary refinement.',
    best_use:                        'Act when timing is clear, refine what matters, and begin with purpose.',
    simple_reveal_stem:              'think ahead, find the right opening, and move at the right time,',
    simple_natural_expression:       'You like thinking before you act.',
    simple_developmental_force:      'Life teaches you about timing and smart choices.',
    simple_pattern_statement:        'You help things begin at the right moment.',
    operator_dynamic_pattern:        'Initiatory precision through timing-mediated discernment.',
    operator_natural_expression:     'Activates through calculated sequencing rather than impulse.',
    operator_developmental_pressure: 'Growth occurs through refinement of timing and strategic accuracy.',
    operator_emergent_pattern:       'Creates progress through precision in when and how action begins.',
  },
  'nanda:Water': {
    configuration_theme_name:        'The Timing Keeper',
    recognition_line:                'You may have noticed your best moves often come from sensing when the moment is right.',
    watch_for:                       'Waiting too long can turn discernment into hesitation.',
    best_use:                        'Trust timing, act when the opening appears, and keep momentum alive.',
    simple_reveal_stem:              'sense when the moment is right and move with it,',
    simple_natural_expression:       'You have a feel for when the time is right.',
    simple_developmental_force:      'Life teaches you patience and timing.',
    simple_pattern_statement:        'You help things happen when the moment is ready.',
    operator_dynamic_pattern:        'Initiation regulated through adaptive timing sensitivity.',
    operator_natural_expression:     'Responds to conditions rather than forcing premature movement.',
    operator_developmental_pressure: 'Growth occurs through delay, timing correction, and recognition of readiness.',
    operator_emergent_pattern:       'Activates movement when conditions support successful emergence.',
  },

  'bhadra:Wood': {
    configuration_theme_name:        'The Cultivator',
    recognition_line:                'You may have noticed you often focus on what allows people or systems to thrive.',
    watch_for:                       'Supporting too much can enable what should mature through challenge.',
    best_use:                        'Strengthen what nourishes growth and allow what is weak to evolve.',
    simple_reveal_stem:              'help things grow by creating the conditions they need,',
    simple_natural_expression:       'You like helping things grow.',
    simple_developmental_force:      'Life teaches you how to care for what matters.',
    simple_pattern_statement:        'You help people and things become stronger.',
    operator_dynamic_pattern:        'Growth reinforcement through supportive developmental conditions.',
    operator_natural_expression:     'Strengthens potential through nourishment and sustained support.',
    operator_developmental_pressure: 'Growth occurs through responsibility, care, and long-term maintenance.',
    operator_emergent_pattern:       'Develops strength by reinforcing what supports healthy growth.',
  },
  'bhadra:Fire': {
    configuration_theme_name:        'The Stabilizer',
    recognition_line:                'You may have noticed you often hold steady while others move through volatility.',
    watch_for:                       'Trying to stabilize everything can resist necessary transformation.',
    best_use:                        'Support change without controlling it, and stabilize what truly matters.',
    simple_reveal_stem:              'hold things steady when the world around you gets messy,',
    simple_natural_expression:       'You help calm things down when life feels messy.',
    simple_developmental_force:      'Life teaches you how to stay steady during change.',
    simple_pattern_statement:        'You help others feel grounded.',
    operator_dynamic_pattern:        'Transformational regulation through stabilizing intervention.',
    operator_natural_expression:     'Moderates volatility by restoring coherence under change.',
    operator_developmental_pressure: 'Growth occurs through instability that tests structural resilience.',
    operator_emergent_pattern:       'Supports adaptation by preserving coherence during transformation.',
  },
  'bhadra:Earth': {
    configuration_theme_name:        'The Steward',
    recognition_line:                'You may have noticed you often feel responsible for preserving what truly matters.',
    watch_for:                       'Holding too much can turn care into burden.',
    best_use:                        'Support what matters, release what drains, and steward what can endure.',
    simple_reveal_stem:              'care for what matters and keep it strong,',
    simple_natural_expression:       'You like taking care of what matters.',
    simple_developmental_force:      'Life teaches you responsibility.',
    simple_pattern_statement:        'You help things stay strong and supported.',
    operator_dynamic_pattern:        'Supportive stabilization through responsibility-based reinforcement.',
    operator_natural_expression:     'Strengthens systems through preservation and sustained support.',
    operator_developmental_pressure: 'Growth occurs through responsibility, burden, and discernment.',
    operator_emergent_pattern:       'Creates stability by reinforcing what holds long-term value.',
  },
  'bhadra:Metal': {
    configuration_theme_name:        'The Architect',
    recognition_line:                'You may have noticed you often see how things could be organized to work better.',
    watch_for:                       'Over-structuring can make support feel rigid instead of life-giving.',
    best_use:                        'Create order that strengthens life, not control that limits it.',
    simple_reveal_stem:              'see how things could work better and help make them work,',
    simple_natural_expression:       'You like making things work better.',
    simple_developmental_force:      'Life teaches you how structure helps things succeed.',
    simple_pattern_statement:        'You help improve how things are organized.',
    operator_dynamic_pattern:        'Structural intelligence through ordered systemic design.',
    operator_natural_expression:     'Identifies inefficiency and reorganizes toward greater coherence.',
    operator_developmental_pressure: 'Growth occurs through structural failure, redesign, and refinement.',
    operator_emergent_pattern:       'Improves systems through intelligent restructuring.',
  },
  'bhadra:Water': {
    configuration_theme_name:        'The Wise Guardian',
    recognition_line:                'You may have noticed you often sense what needs protection before others do.',
    watch_for:                       'Protectiveness can become over-caution or retreat.',
    best_use:                        'Protect what matters, trust timing, and let wisdom guide support.',
    simple_reveal_stem:              'protect what feels important before others realize it needs protecting,',
    simple_natural_expression:       'You protect what feels important.',
    simple_developmental_force:      'Life teaches you what deserves care.',
    simple_pattern_statement:        'You help keep what matters safe.',
    operator_dynamic_pattern:        'Protective stabilization through depth-guided preservation.',
    operator_natural_expression:     'Protects what carries enduring significance.',
    operator_developmental_pressure: 'Growth occurs through caution, vulnerability, and protective discernment.',
    operator_emergent_pattern:       'Creates support through intelligent preservation of what matters.',
  },

  'jaya:Wood': {
    configuration_theme_name:        'The Challenger',
    recognition_line:                'You may have noticed challenge often pushes you forward rather than shutting you down.',
    watch_for:                       'Constant struggle can become an identity instead of a catalyst.',
    best_use:                        'Use challenge to develop strength, not to define who you are.',
    simple_reveal_stem:              'grow by meeting hard things directly,',
    simple_natural_expression:       'You grow by facing hard things.',
    simple_developmental_force:      'Life teaches you strength through challenge.',
    simple_pattern_statement:        'You help turn struggle into growth.',
    operator_dynamic_pattern:        'Growth generation through resistance-mediated strengthening.',
    operator_natural_expression:     'Engages friction as developmental stimulus.',
    operator_developmental_pressure: 'Growth occurs through challenge, conflict, and adaptive strain.',
    operator_emergent_pattern:       'Creates development by converting resistance into strength.',
  },
  'jaya:Fire': {
    configuration_theme_name:        'The Forge',
    recognition_line:                'You may have noticed difficult conditions often sharpen you instead of breaking you.',
    watch_for:                       'Pressure and intensity can keep you fighting when it is time to build.',
    best_use:                        'Channel pressure wisely, use intensity with purpose, and let challenge forge clarity.',
    simple_reveal_stem:              'get stronger through pressure,',
    simple_natural_expression:       'Hard things often make you stronger.',
    simple_developmental_force:      'Life teaches you through pressure.',
    simple_pattern_statement:        'You turn challenge into strength.',
    operator_dynamic_pattern:        'Transformation through pressure-amplified strengthening.',
    operator_natural_expression:     'Uses intensity as a force for structural growth.',
    operator_developmental_pressure: 'Growth occurs through sustained pressure and transformational stress.',
    operator_emergent_pattern:       'Generates strength by converting pressure into transformative momentum.',
  },
  'jaya:Earth': {
    configuration_theme_name:        'The Stronghold',
    recognition_line:                'You may have noticed others may rely on you most when things become difficult.',
    watch_for:                       'Strength can harden into defensiveness or carrying too much alone.',
    best_use:                        'Stand firm where needed, stay flexible where possible, and build through discipline.',
    simple_reveal_stem:              'hold firm when everything around you gets difficult,',
    simple_natural_expression:       'You stay steady when things get hard.',
    simple_developmental_force:      'Life teaches you resilience.',
    simple_pattern_statement:        'You help others feel strong when things are tested.',
    operator_dynamic_pattern:        'Stability generation through resilient structural endurance.',
    operator_natural_expression:     'Maintains integrity under sustained pressure.',
    operator_developmental_pressure: 'Growth occurs through burden, endurance, and sustained testing.',
    operator_emergent_pattern:       'Creates strength through structural resilience under stress.',
  },
  'jaya:Metal': {
    configuration_theme_name:        'The Master',
    recognition_line:                'You may have noticed pressure often pushes you toward precision, not retreat.',
    watch_for:                       'Perfectionism under pressure can turn growth into self-criticism.',
    best_use:                        'Let challenge sharpen skill, not narrow possibility.',
    simple_reveal_stem:              'get better at things through practice and challenge,',
    simple_natural_expression:       'You like getting better through practice.',
    simple_developmental_force:      'Life teaches you through refinement.',
    simple_pattern_statement:        'You help turn pressure into skill.',
    operator_dynamic_pattern:        'Refinement through pressure-mediated precision development.',
    operator_natural_expression:     'Sharpens capability through disciplined correction.',
    operator_developmental_pressure: 'Growth occurs through challenge exposing areas for refinement.',
    operator_emergent_pattern:       'Develops mastery through iterative pressure-driven improvement.',
  },
  'jaya:Water': {
    configuration_theme_name:        'The Resilient Sage',
    recognition_line:                'You may have noticed you often become clearer when difficulty forces deeper reflection.',
    watch_for:                       'Reflection can become retreat when action is required.',
    best_use:                        'Let insight guide action, and let difficulty deepen wisdom.',
    simple_reveal_stem:              'stay thoughtful and clear even when life is hard,',
    simple_natural_expression:       'You stay thoughtful even when life is hard.',
    simple_developmental_force:      'Life teaches you wisdom through difficulty.',
    simple_pattern_statement:        'You help bring perspective when things feel hard.',
    operator_dynamic_pattern:        'Adaptive wisdom through resilience-integrated reflection.',
    operator_natural_expression:     'Maintains reflective awareness under difficulty.',
    operator_developmental_pressure: 'Growth occurs through hardship that deepens adaptive insight.',
    operator_emergent_pattern:       'Creates perspective by integrating resilience with wisdom.',
  },

  'rikta:Wood': {
    configuration_theme_name:        'The Pruner',
    recognition_line:                'You may have noticed you often see what needs cutting back before others do.',
    watch_for:                       'Cutting back too much can remove what needed support, not removal.',
    best_use:                        'Clear what blocks growth, then protect what deserves development.',
    simple_reveal_stem:              'clear away what isn\'t working so something healthier can grow,',
    simple_natural_expression:       'You notice what needs to be cleared away.',
    simple_developmental_force:      'Life teaches you through letting go.',
    simple_pattern_statement:        'You help make room for healthier growth.',
    operator_dynamic_pattern:        'Development through reduction-based clearing.',
    operator_natural_expression:     'Removes obstruction that impedes healthy growth.',
    operator_developmental_pressure: 'Growth occurs through release, loss, and necessary subtraction.',
    operator_emergent_pattern:       'Strengthens development by clearing what weakens growth.',
  },
  'rikta:Fire': {
    configuration_theme_name:        'The Structural Reformer',
    recognition_line:                'You may have noticed you often see what needs removing before others see what needs rebuilding.',
    watch_for:                       'Over-clearing and burnout can keep you correcting when it\'s time to build.',
    best_use:                        'Clear strategically, use intensity with purpose, and build for endurance.',
    simple_reveal_stem:              'fix what is weak first, so you can build something strong that lasts,',
    simple_natural_expression:       'You notice when something isn\'t working and want to fix it.',
    simple_developmental_force:      'Life helps you grow through hard changes.',
    simple_pattern_statement:        'You make things stronger by fixing what is weak first.',
    operator_dynamic_pattern:        'Structural correction through pressure-mediated transformation.',
    operator_natural_expression:     'Identifies weakness, instability, or inefficiency prior to intervention.',
    operator_developmental_pressure: 'Growth occurs through destabilization, adaptive pressure, and structural stress.',
    operator_emergent_pattern:       'Improves systems through corrective disruption before durable reconstruction.',
  },
  'rikta:Earth': {
    configuration_theme_name:        'The Grounded Seer',
    recognition_line:                'You may have noticed you often perceive underlying weaknesses others overlook.',
    watch_for:                       'Over-analysis can delay the action clarity is meant to support.',
    best_use:                        'Use discernment to clarify what matters, then ground it in action.',
    simple_reveal_stem:              'see what needs to be cleared before the next move is made,',
    simple_natural_expression:       'You notice what needs clarity before action.',
    simple_developmental_force:      'Life teaches you how to see clearly.',
    simple_pattern_statement:        'You help others find direction.',
    operator_dynamic_pattern:        'Clarification through stability-guided discernment.',
    operator_natural_expression:     'Perceives what requires clarity before effective action.',
    operator_developmental_pressure: 'Growth occurs through uncertainty that develops discernment.',
    operator_emergent_pattern:       'Creates direction through grounded clarification.',
  },
  'rikta:Metal': {
    configuration_theme_name:        'The Refiner',
    recognition_line:                'You may have noticed you often improve things by clarifying rather than adding.',
    watch_for:                       'Correction can become criticism when refinement loses proportion.',
    best_use:                        'Refine what matters, remove what weakens it, and preserve what has value.',
    simple_reveal_stem:              'notice what could be better and quietly make it so,',
    simple_natural_expression:       'You notice how things could be improved.',
    simple_developmental_force:      'Life teaches you through correction and learning.',
    simple_pattern_statement:        'You help make things better.',
    operator_dynamic_pattern:        'Strengthening through precision-based reduction.',
    operator_natural_expression:     'Removes distortion through corrective refinement.',
    operator_developmental_pressure: 'Growth occurs through error, correction, and precision development.',
    operator_emergent_pattern:       'Improves integrity through intelligent refinement.',
  },
  'rikta:Water': {
    configuration_theme_name:        'The Deep Seer',
    recognition_line:                'You may have noticed insight often comes when you create space rather than force answers.',
    watch_for:                       'Withdrawal and stagnation can keep insight from becoming lived wisdom.',
    best_use:                        'Create space, keep depth in motion, and let insight become action.',
    simple_reveal_stem:              'see beneath the surface and bring clarity from what you notice,',
    simple_natural_expression:       'You notice deeper things others may miss.',
    simple_developmental_force:      'Life teaches you through reflection.',
    simple_pattern_statement:        'You help bring clarity by seeing beneath the surface.',
    operator_dynamic_pattern:        'Insight generation through depth-mediated perception.',
    operator_natural_expression:     'Detects underlying patterns beneath surface appearance.',
    operator_developmental_pressure: 'Growth occurs through ambiguity, reflection, and perceptual deepening.',
    operator_emergent_pattern:       'Creates clarity through depth-informed insight.',
  },

  'purna:Wood': {
    configuration_theme_name:        'The Harvester',
    recognition_line:                'You may have noticed you often care about bringing things all the way through.',
    watch_for:                       'Pushing for completion too early can interrupt natural maturation.',
    best_use:                        'Bring growth to completion in its right season.',
    simple_reveal_stem:              'help things reach their full potential and see them through to the end,',
    simple_natural_expression:       'You like helping things reach completion.',
    simple_developmental_force:      'Life teaches you through endings and fulfillment.',
    simple_pattern_statement:        'You help bring things to completion.',
    operator_dynamic_pattern:        'Completion through fulfillment-oriented integration.',
    operator_natural_expression:     'Brings development toward coherent completion.',
    operator_developmental_pressure: 'Growth occurs through cycles of fulfillment, release, and renewal.',
    operator_emergent_pattern:       'Creates wholeness by guiding processes toward completion.',
  },
  'purna:Fire': {
    configuration_theme_name:        'The Illuminator',
    recognition_line:                'You may have noticed clarity often emerges for you at the point others reach overwhelm.',
    watch_for:                       'Intensity can turn completion into exhaustion.',
    best_use:                        'Bring clarity to completion, and let revelation serve wisdom.',
    simple_reveal_stem:              'bring clarity to what matters most,',
    simple_natural_expression:       'You help bring clarity to what matters.',
    simple_developmental_force:      'Life teaches you through insight.',
    simple_pattern_statement:        'You help others see more clearly.',
    operator_dynamic_pattern:        'Clarity generation through revelatory integration.',
    operator_natural_expression:     'Reveals what carries significance or hidden coherence.',
    operator_developmental_pressure: 'Growth occurs through realization, insight shifts, and expanded understanding.',
    operator_emergent_pattern:       'Creates clarity by illuminating what was previously unseen.',
  },
  'purna:Earth': {
    configuration_theme_name:        'The Integrator',
    recognition_line:                'You may have noticed you often see how separate pieces belong together.',
    watch_for:                       'Trying to hold everything together can become overextension.',
    best_use:                        'Integrate what belongs together, and release what does not.',
    simple_reveal_stem:              'help different pieces fit together into something whole,',
    simple_natural_expression:       'You like helping things fit together.',
    simple_developmental_force:      'Life teaches you how separate things can work as one.',
    simple_pattern_statement:        'You help create wholeness.',
    operator_dynamic_pattern:        'Coherence generation through systemic integration.',
    operator_natural_expression:     'Connects disparate elements into functional wholeness.',
    operator_developmental_pressure: 'Growth occurs through complexity requiring higher-order coordination.',
    operator_emergent_pattern:       'Creates strength by integrating separate parts into greater coherence.',
  },
  'purna:Metal': {
    configuration_theme_name:        'The Finisher',
    recognition_line:                'You may have noticed you often focus on finishing well, not just finishing fast.',
    watch_for:                       'Over-refining can prevent something from ever being finished.',
    best_use:                        'Finish with care, not perfection.',
    simple_reveal_stem:              'bring things to completion with real care,',
    simple_natural_expression:       'You care about finishing things well.',
    simple_developmental_force:      'Life teaches you through bringing things to completion.',
    simple_pattern_statement:        'You help strengthen outcomes.',
    operator_dynamic_pattern:        'Completion through precision-guided closure.',
    operator_natural_expression:     'Strengthens outcomes through refined completion.',
    operator_developmental_pressure: 'Growth occurs through unfinished processes requiring closure or correction.',
    operator_emergent_pattern:       'Improves outcomes through intelligent completion.',
  },
  'purna:Water': {
    configuration_theme_name:        'The Wisdom Keeper',
    recognition_line:                'You may have noticed deeper meaning often arrives for you after experience has fully unfolded.',
    watch_for:                       'Too much reflection can delay the renewal that completion invites.',
    best_use:                        'Let completion deepen wisdom, then let wisdom open what comes next.',
    simple_reveal_stem:              'turn what you\'ve lived through into something that helps others,',
    simple_natural_expression:       'You learn deeply from experience.',
    simple_developmental_force:      'Life teaches you wisdom over time.',
    simple_pattern_statement:        'You help others through what you\'ve learned.',
    operator_dynamic_pattern:        'Wisdom generation through experience-integrated reflection.',
    operator_natural_expression:     'Extracts meaning from lived experience over time.',
    operator_developmental_pressure: 'Growth occurs through endings, reflection, and experiential deepening.',
    operator_emergent_pattern:       'Creates wisdom by integrating experience into practical understanding.',
  },
};

// ── Generation Logic ───────────────────────────────────────────────────────

export function getDynamic(tithi, element) {
  return TITHI_ELEM_DYN[`${tithi}:${element}`] || null;
}

export function generateWatchFor(tithi, element, lifePathNum) {
  const t  = TITHI_CCE[tithi];
  const el = ELEMENT_CCE[element];
  const lp = LP_CCE[lifePathNum];
  if (!t || !el || !lp) return null;
  return `${cap(t.watchout_fragment)} and ${el.watchout_fragment}. This can make it harder to reach ${lp.outcome.toLowerCase()}.`;
}

export function generateBestUse(tithi, element, lifePathNum) {
  const t  = TITHI_CCE[tithi];
  const el = ELEMENT_CCE[element];
  const lp = LP_CCE[lifePathNum];
  if (!t || !el || !lp) return null;
  return `${cap(t.best_use_fragment)}, ${el.best_use_fragment}, and stay oriented toward ${lp.outcome.toLowerCase()}.`;
}

function cap(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}
