/**
 * Core Configuration Engine — V1
 *
 * Four tables that power the "Core Configuration" profile section:
 *   Table 1 — TITHI_CCE        (5 rows: Nanda, Bhadra, Jaya, Rikta, Purna)
 *   Table 2 — ELEMENT_CCE      (5 rows: Wood, Fire, Earth, Metal, Water)
 *   Table 3 — LP_CCE           (12 rows: Life Paths 1–9, 11, 22, 33)
 *   Table 4 — TITHI_ELEM_DYN   (25 rows: every Tithi × Element pair)
 *
 * Generation logic:
 *   generateWatchFor(tithi, element, lifePathNum) → string
 *   generateBestUse(tithi, element, lifePathNum)  → string
 *
 * Cascade doctrine (read in sequence):
 *   Operate → Move Through → Build Toward
 *
 * How This Works — two modes per entry:
 *   Simple (how_like / how_teaches / how_shows)
 *   Operator (op_naturally / op_develops / op_together)
 */

// ── Table 1 — Tithi ────────────────────────────────────────────────────────

export const TITHI_CCE = {
  nanda: {
    functional_name:        'Initiation & Opportunity',
    naturally_statement:    'Start movement and sense openings.',
    gift_phrase:            'Your instinct for recognizing and acting on opportunity.',
    shadow_phrase:          'Starting too quickly or scattering your energy.',
    best_use_fragment:      'start intentionally',
    watchout_fragment:      'rushing into too many things',
  },
  bhadra: {
    functional_name:        'Support & Favorable Conditions',
    naturally_statement:    'Create conditions where growth can happen.',
    gift_phrase:            'Your ability to create supportive conditions for growth.',
    shadow_phrase:          'Holding in place what needs to change.',
    best_use_fragment:      'strengthen what supports growth',
    watchout_fragment:      'holding on to what should evolve',
  },
  jaya: {
    functional_name:        'Challenge & Activation',
    naturally_statement:    'Grow through pressure.',
    gift_phrase:            'Your ability to grow stronger through challenge.',
    shadow_phrase:          'Turning struggle into your default operating mode.',
    best_use_fragment:      'use challenge to sharpen you',
    watchout_fragment:      'turning struggle into your default',
  },
  rikta: {
    functional_name:        'Clearing & Receptivity',
    naturally_statement:    'Clear what obstructs growth.',
    gift_phrase:            'Your instinct for clearing what weakens the whole.',
    shadow_phrase:          'Withdrawing too far or removing what still has value.',
    best_use_fragment:      'clear strategically',
    watchout_fragment:      'over-clearing or withdrawing too far',
  },
  purna: {
    functional_name:        'Completion & Revelation',
    naturally_statement:    'Bring things to fulfillment.',
    gift_phrase:            'Your ability to bring things to fulfillment.',
    shadow_phrase:          'Holding on after something is complete.',
    best_use_fragment:      'complete fully, then let go',
    watchout_fragment:      'holding on past completion',
  },
};

// ── Table 2 — Elements ─────────────────────────────────────────────────────

export const ELEMENT_CCE = {
  Wood: {
    functional_name:            'Growth & Expansion',
    shapes_you_through:         'Development and possibility.',
    gift_phrase:                'Growth with vision and forward movement.',
    shadow_phrase:              'Pushing growth before the foundation is ready.',
    best_use_fragment:          'pair growth with structure',
    watchout_fragment:          'growing faster than your foundation',
  },
  Fire: {
    functional_name:            'Transformation & Visibility',
    shapes_you_through:         'Intensity and catalytic change.',
    gift_phrase:                'Transformation through intensity and engagement.',
    shadow_phrase:              'Burning through energy too quickly.',
    best_use_fragment:          'use intensity with purpose',
    watchout_fragment:          'burning through energy too quickly',
  },
  Earth: {
    functional_name:            'Stability & Integration',
    shapes_you_through:         'Grounding and coherence.',
    gift_phrase:                'Stability, coherence, and integration.',
    shadow_phrase:              'Becoming stuck by holding too much.',
    best_use_fragment:          'stay grounded while carrying what matters',
    watchout_fragment:          'taking on too much until you stall',
  },
  Metal: {
    functional_name:            'Precision & Refinement',
    shapes_you_through:         'Discernment and reduction.',
    gift_phrase:                'Precision, discernment, and intelligent structure.',
    shadow_phrase:              'Becoming overly rigid or corrective.',
    best_use_fragment:          'refine what matters most',
    watchout_fragment:          'becoming too rigid or corrective',
  },
  Water: {
    functional_name:            'Depth & Adaptability',
    shapes_you_through:         'Timing, wisdom, responsiveness.',
    gift_phrase:                'Depth, timing, and adaptive wisdom.',
    shadow_phrase:              'Slowing into stagnation or retreat.',
    best_use_fragment:          'keep depth in motion',
    watchout_fragment:          'slowing into stagnation',
  },
};

// ── Table 3 — Life Paths ───────────────────────────────────────────────────

export const LP_CCE = {
  1:  { outcome: 'New Pathways' },
  2:  { outcome: 'Meaningful Connection' },
  3:  { outcome: 'Creative Expression' },
  4:  { outcome: 'Enduring Structures' },
  5:  { outcome: 'Disciplined Freedom' },
  6:  { outcome: 'Sustained Care' },
  7:  { outcome: 'Deep Understanding' },
  8:  { outcome: 'Meaningful Impact' },
  9:  { outcome: 'Completion and Renewal' },
  11: { outcome: 'Visionary Insight' },
  22: { outcome: 'Transformative Systems' },
  33: { outcome: 'Awakened Service' },
};

// ── Table 4 — Tithi × Element Dynamics ────────────────────────────────────

export const TITHI_ELEM_DYN = {
  'nanda:Wood': {
    dynamic_type:             'Starting growth quickly',
    configuration_theme_name: 'The Pioneer',
    reveal_statement:         'Your pattern is to create momentum by initiating growth before others see what\'s possible.',
    recognition_line:         'You may have noticed you often move toward possibility before others are ready to act.',
    pattern_statement:        'You generate momentum by acting early and helping growth move before it stalls.',
    watch_for:                'Rushing ahead can create movement faster than foundations can support.',
    best_use:                 'Start intentionally, support what has real potential, and give growth structure.',
    how_like:                 'You like getting things started.',
    how_teaches:              'Life teaches you by helping you try things and learn as you go.',
    how_shows:                'You help things move when others are stuck.',
    op_naturally:             'You naturally initiate movement and often act before others are ready to begin.',
    op_develops:              'Life often teaches you through risk, uncertainty, and learning as you go.',
    op_together:              'You often help create momentum by getting things moving when others hesitate.',
  },
  'nanda:Fire': {
    dynamic_type:             'Initiating transformation',
    configuration_theme_name: 'The Catalyst',
    reveal_statement:         'Your pattern is to trigger change by acting before stagnation takes hold.',
    recognition_line:         'You may have noticed movement often begins around you when you decide to engage.',
    pattern_statement:        'You initiate change by bringing movement where stagnation has taken hold.',
    watch_for:                'Impulsiveness and over-intensity can create disruption without direction.',
    best_use:                 'Act decisively, direct intensity wisely, and let change serve what matters.',
    how_like:                 'You bring energy when things feel stuck.',
    how_teaches:              'Life teaches you through change and surprises.',
    how_shows:                'You help get things moving again.',
    op_naturally:             'You naturally bring energy into stagnant situations and push for change.',
    op_develops:              'Life often teaches you through intensity, disruption, and sudden shifts.',
    op_together:              'You often create progress by helping movement happen where things have stalled.',
  },
  'nanda:Earth': {
    dynamic_type:             'Building durable beginnings',
    configuration_theme_name: 'The Foundation Starter',
    reveal_statement:         'Your pattern is to create durable beginnings by grounding momentum early.',
    recognition_line:         'You may have noticed you care not just about starting, but about starting on solid footing.',
    pattern_statement:        'You create strong beginnings by grounding momentum in stability early.',
    watch_for:                'Starting too much can create commitments that become difficult to sustain.',
    best_use:                 'Begin with intention, build from solid footing, and develop what can endure.',
    how_like:                 'You like starting things the right way.',
    how_teaches:              'Life teaches you why strong beginnings matter.',
    how_shows:                'You help things begin on solid ground.',
    op_naturally:             'You naturally want to begin things in a way that feels solid and workable.',
    op_develops:              'Life often teaches you through responsibility and the consequences of weak beginnings.',
    op_together:              'You often help create strong beginnings by combining initiative with practical grounding.',
  },
  'nanda:Metal': {
    dynamic_type:             'Beginning with discernment',
    configuration_theme_name: 'The Strategist',
    reveal_statement:         'Your pattern is to begin well by combining initiative with discernment.',
    recognition_line:         'You may have noticed you often sense both when to act and what needs refining first.',
    pattern_statement:        'You combine initiative with discernment, helping action begin with greater precision.',
    watch_for:                'Overthinking can slow action, while impulsiveness can bypass necessary refinement.',
    best_use:                 'Act when timing is clear, refine what matters, and begin with purpose.',
    how_like:                 'You like thinking before you act.',
    how_teaches:              'Life teaches you about timing and smart choices.',
    how_shows:                'You help things begin at the right moment.',
    op_naturally:             'You naturally think ahead before acting and look for the right opening.',
    op_develops:              'Life often teaches you through timing, refinement, and learning when action matters most.',
    op_together:              'You often create progress by knowing when and how to begin effectively.',
  },
  'nanda:Water': {
    dynamic_type:             'Acting with timing',
    configuration_theme_name: 'The Timing Keeper',
    reveal_statement:         'Your pattern is to recognize opportunity through timing rather than force.',
    recognition_line:         'You may have noticed your best moves often come from sensing when the moment is right.',
    pattern_statement:        'You recognize opportunity through timing, knowing when movement is ready.',
    watch_for:                'Waiting too long can turn discernment into hesitation.',
    best_use:                 'Trust timing, act when the opening appears, and keep momentum alive.',
    how_like:                 'You have a feel for when the time is right.',
    how_teaches:              'Life teaches you patience and timing.',
    how_shows:                'You help things happen when the moment is ready.',
    op_naturally:             'You naturally sense when conditions are ready and when they are not.',
    op_develops:              'Life often teaches you through waiting, missed timing, and recognizing the right moment.',
    op_together:              'You often help movement happen by acting when the opening is real.',
  },

  'bhadra:Wood': {
    dynamic_type:             'Supporting development',
    configuration_theme_name: 'The Cultivator',
    reveal_statement:         'Your pattern is to help growth happen by strengthening the conditions that support it.',
    recognition_line:         'You may have noticed you often focus on what allows people or systems to thrive.',
    pattern_statement:        'You help growth happen by strengthening the conditions that support development.',
    watch_for:                'Supporting too much can enable what should mature through challenge.',
    best_use:                 'Strengthen what nourishes growth and allow what is weak to evolve.',
    how_like:                 'You like helping things grow.',
    how_teaches:              'Life teaches you how to care for what matters.',
    how_shows:                'You help people and things become stronger.',
    op_naturally:             'You naturally support growth and strengthen what has genuine potential.',
    op_develops:              'Life often teaches you through responsibility, care, and supporting others.',
    op_together:              'You often help things flourish by creating conditions where growth can take hold.',
  },
  'bhadra:Fire': {
    dynamic_type:             'Stabilizing change',
    configuration_theme_name: 'The Stabilizer',
    reveal_statement:         'Your pattern is to help change happen without losing what creates coherence.',
    recognition_line:         'You may have noticed you often hold steady while others move through volatility.',
    pattern_statement:        'You help change happen while preserving the coherence needed to sustain it.',
    watch_for:                'Trying to stabilize everything can resist necessary transformation.',
    best_use:                 'Support change without controlling it, and stabilize what truly matters.',
    how_like:                 'You help calm things down when life feels messy.',
    how_teaches:              'Life teaches you how to stay steady during change.',
    how_shows:                'You help others feel grounded.',
    op_naturally:             'You naturally bring steadiness into situations that feel reactive or unstable.',
    op_develops:              'Life often teaches you through change that tests what can hold together.',
    op_together:              'You often help others navigate change by bringing stability where it is needed.',
  },
  'bhadra:Earth': {
    dynamic_type:             'Creating enduring foundations',
    configuration_theme_name: 'The Steward',
    reveal_statement:         'Your pattern is to create enduring strength by supporting what has real long-term value.',
    recognition_line:         'You may have noticed you often feel responsible for preserving what truly matters.',
    pattern_statement:        'You create lasting strength by supporting what has genuine long-term value.',
    watch_for:                'Holding too much can turn care into burden.',
    best_use:                 'Support what matters, release what drains, and steward what can endure.',
    how_like:                 'You like taking care of what matters.',
    how_teaches:              'Life teaches you responsibility.',
    how_shows:                'You help things stay strong and supported.',
    op_naturally:             'You naturally support what has long-term value and want to strengthen what can endure.',
    op_develops:              'Life often puts you in situations where responsibility teaches discernment.',
    op_together:              'You often help create stability by strengthening what matters and carrying things carefully.',
  },
  'bhadra:Metal': {
    dynamic_type:             'Supporting through intelligent structure',
    configuration_theme_name: 'The Architect',
    reveal_statement:         'Your pattern is to strengthen systems by bringing support and structure together.',
    recognition_line:         'You may have noticed you often see how things could be organized to work better.',
    pattern_statement:        'You strengthen systems by combining support with intelligent structure.',
    watch_for:                'Over-structuring can make support feel rigid instead of life-giving.',
    best_use:                 'Create order that strengthens life, not control that limits it.',
    how_like:                 'You like making things work better.',
    how_teaches:              'Life teaches you how structure helps things succeed.',
    how_shows:                'You help improve how things are organized.',
    op_naturally:             'You naturally see how things could be organized or structured more intelligently.',
    op_develops:              'Life often teaches you through systems that succeed or fail based on design.',
    op_together:              'You often improve things by bringing structure where disorder creates friction.',
  },
  'bhadra:Water': {
    dynamic_type:             'Supporting through wisdom',
    configuration_theme_name: 'The Wise Guardian',
    reveal_statement:         'Your pattern is to support wisely by combining care with depth and timing.',
    recognition_line:         'You may have noticed you often sense what needs protection before others do.',
    pattern_statement:        'You support wisely by combining protection, depth, and timing.',
    watch_for:                'Protectiveness can become over-caution or retreat.',
    best_use:                 'Protect what matters, trust timing, and let wisdom guide support.',
    how_like:                 'You protect what feels important.',
    how_teaches:              'Life teaches you what deserves care.',
    how_shows:                'You help keep what matters safe.',
    op_naturally:             'You naturally protect what feels meaningful or worth preserving.',
    op_develops:              'Life often teaches you through caution, depth, and learning what deserves protection.',
    op_together:              'You often help others feel supported by protecting what truly matters.',
  },

  'jaya:Wood': {
    dynamic_type:             'Growing through challenge',
    configuration_theme_name: 'The Challenger',
    reveal_statement:         'Your pattern is to develop strength by using resistance as a force for growth.',
    recognition_line:         'You may have noticed challenge often pushes you forward rather than shutting you down.',
    pattern_statement:        'You turn resistance into development by allowing challenge to fuel growth.',
    watch_for:                'Constant struggle can become an identity instead of a catalyst.',
    best_use:                 'Use challenge to develop strength, not to define who you are.',
    how_like:                 'You grow by facing hard things.',
    how_teaches:              'Life teaches you strength through challenge.',
    how_shows:                'You help turn struggle into growth.',
    op_naturally:             'You naturally meet resistance directly and often grow through challenge.',
    op_develops:              'Life often teaches you through conflict, pressure, and situations that demand strength.',
    op_together:              'You often help create growth by turning challenge into development.',
  },
  'jaya:Fire': {
    dynamic_type:             'Transforming through pressure',
    configuration_theme_name: 'The Forge',
    reveal_statement:         'Your pattern is to transform through pressure, using intensity to create strength.',
    recognition_line:         'You may have noticed difficult conditions often sharpen you instead of breaking you.',
    pattern_statement:        'You transform through pressure, using intensity to create strength and change.',
    watch_for:                'Pressure and intensity can keep you fighting when it is time to build.',
    best_use:                 'Channel pressure wisely, use intensity with purpose, and let challenge forge clarity.',
    how_like:                 'Hard things often make you stronger.',
    how_teaches:              'Life teaches you through pressure.',
    how_shows:                'You turn challenge into strength.',
    op_naturally:             'You naturally meet pressure directly and often respond by pushing for growth.',
    op_develops:              'Life often puts you through challenges that strengthen you through intensity.',
    op_together:              'You often turn pressure into momentum and use challenge to create change.',
  },
  'jaya:Earth': {
    dynamic_type:             'Channeling pressure constructively',
    configuration_theme_name: 'The Stronghold',
    reveal_statement:         'Your pattern is to turn pressure into stability by holding firm under challenge.',
    recognition_line:         'You may have noticed others may rely on you most when things become difficult.',
    pattern_statement:        'You turn pressure into stability by holding firm under challenge.',
    watch_for:                'Strength can harden into defensiveness or carrying too much alone.',
    best_use:                 'Stand firm where needed, stay flexible where possible, and build through discipline.',
    how_like:                 'You stay steady when things get hard.',
    how_teaches:              'Life teaches you resilience.',
    how_shows:                'You help others feel strong when things are tested.',
    op_naturally:             'You naturally hold steady under pressure and resist collapse.',
    op_develops:              'Life often teaches you through burdens that require discipline and resilience.',
    op_together:              'You often help create strength by remaining steady when things are being tested.',
  },
  'jaya:Metal': {
    dynamic_type:             'Developing mastery through challenge',
    configuration_theme_name: 'The Master',
    reveal_statement:         'Your pattern is to develop mastery by allowing challenge to refine your strengths.',
    recognition_line:         'You may have noticed pressure often pushes you toward precision, not retreat.',
    pattern_statement:        'You develop mastery by allowing challenge to refine your strengths.',
    watch_for:                'Perfectionism under pressure can turn growth into self-criticism.',
    best_use:                 'Let challenge sharpen skill, not narrow possibility.',
    how_like:                 'You like getting better through practice.',
    how_teaches:              'Life teaches you through refinement.',
    how_shows:                'You help turn pressure into skill.',
    op_naturally:             'You naturally refine skill through challenge and push toward mastery.',
    op_develops:              'Life often teaches you through pressure that exposes what still needs development.',
    op_together:              'You often grow by allowing challenge to sharpen capability.',
  },
  'jaya:Water': {
    dynamic_type:             'Tempering challenge with depth',
    configuration_theme_name: 'The Resilient Sage',
    reveal_statement:         'Your pattern is to temper challenge with wisdom, creating strength that adapts.',
    recognition_line:         'You may have noticed you often become clearer when difficulty forces deeper reflection.',
    pattern_statement:        'You temper challenge with wisdom, creating strength that adapts rather than hardens.',
    watch_for:                'Reflection can become retreat when action is required.',
    best_use:                 'Let insight guide action, and let difficulty deepen wisdom.',
    how_like:                 'You stay thoughtful even when life is hard.',
    how_teaches:              'Life teaches you wisdom through difficulty.',
    how_shows:                'You help bring perspective when things feel hard.',
    op_naturally:             'You naturally stay reflective even when facing difficulty.',
    op_develops:              'Life often teaches you through hardship that deepens perspective.',
    op_together:              'You often bring wisdom to difficult situations by combining resilience with insight.',
  },

  'rikta:Wood': {
    dynamic_type:             'Clearing what blocks growth',
    configuration_theme_name: 'The Pruner',
    reveal_statement:         'Your pattern is to help growth by removing what obstructs development.',
    recognition_line:         'You may have noticed you often see what needs cutting back before others do.',
    pattern_statement:        'You help growth by removing what obstructs development.',
    watch_for:                'Cutting back too much can remove what needed support, not removal.',
    best_use:                 'Clear what blocks growth, then protect what deserves development.',
    how_like:                 'You notice what needs to be cleared away.',
    how_teaches:              'Life teaches you through letting go.',
    how_shows:                'You help make room for healthier growth.',
    op_naturally:             'You naturally notice what isn\'t serving growth and feel compelled to remove it.',
    op_develops:              'Life often teaches you through letting go, endings, and necessary reduction.',
    op_together:              'You often help growth happen by clearing what gets in the way.',
  },
  'rikta:Fire': {
    dynamic_type:             'Removing weakness before building strength',
    configuration_theme_name: 'The Structural Reformer',
    reveal_statement:         'Your pattern is to remove what weakens a foundation before building what can endure.',
    recognition_line:         'You may have noticed you often see what needs removing before others see what needs rebuilding.',
    pattern_statement:        'You improve systems by removing structural weakness before strengthening what can endure.',
    watch_for:                'Over-clearing and burnout can keep you correcting when it\'s time to build.',
    best_use:                 'Clear strategically, use intensity with purpose, and build for endurance.',
    how_like:                 'You notice when something isn\'t working and want to fix it.',
    how_teaches:              'Life helps you grow through hard changes.',
    how_shows:                'You make things stronger by fixing what is weak first.',
    op_naturally:             'You naturally notice what isn\'t working and feel compelled to address it.',
    op_develops:              'Life often pushes you through periods of pressure or rapid change that force growth.',
    op_together:              'You often improve things by seeing what needs fixing first, then helping build something stronger.',
  },
  'rikta:Earth': {
    dynamic_type:             'Grounding discernment',
    configuration_theme_name: 'The Grounded Seer',
    reveal_statement:         'Your pattern is to create clarity by combining discernment with stability.',
    recognition_line:         'You may have noticed you often perceive underlying weaknesses others overlook.',
    pattern_statement:        'You create clarity by combining discernment with stability.',
    watch_for:                'Over-analysis can delay the action clarity is meant to support.',
    best_use:                 'Use discernment to clarify what matters, then ground it in action.',
    how_like:                 'You notice what needs clarity before action.',
    how_teaches:              'Life teaches you how to see clearly.',
    how_shows:                'You help others find direction.',
    op_naturally:             'You naturally perceive what needs clarity before action can move forward.',
    op_develops:              'Life often teaches you through uncertainty that strengthens discernment.',
    op_together:              'You often help bring direction by clarifying what others cannot yet see.',
  },
  'rikta:Metal': {
    dynamic_type:             'Refining through precise reduction',
    configuration_theme_name: 'The Refiner',
    reveal_statement:         'Your pattern is to strengthen what matters by removing what does not belong.',
    recognition_line:         'You may have noticed you often improve things by clarifying rather than adding.',
    pattern_statement:        'You strengthen what matters by removing what does not belong.',
    watch_for:                'Correction can become criticism when refinement loses proportion.',
    best_use:                 'Refine what matters, remove what weakens it, and preserve what has value.',
    how_like:                 'You notice how things could be improved.',
    how_teaches:              'Life teaches you through correction and learning.',
    how_shows:                'You help make things better.',
    op_naturally:             'You naturally notice what could be improved and feel drawn to refine it.',
    op_develops:              'Life often teaches you through correction, precision, and learning through mistakes.',
    op_together:              'You often strengthen things by removing what weakens their integrity.',
  },
  'rikta:Water': {
    dynamic_type:             'Deepening wisdom through receptivity',
    configuration_theme_name: 'The Deep Seer',
    reveal_statement:         'Your pattern is to discover truth through receptivity, depth, and intelligent release.',
    recognition_line:         'You may have noticed insight often comes when you create space rather than force answers.',
    pattern_statement:        'You discover truth through receptivity, depth, and intelligent release.',
    watch_for:                'Withdrawal and stagnation can keep insight from becoming lived wisdom.',
    best_use:                 'Create space, keep depth in motion, and let insight become action.',
    how_like:                 'You notice deeper things others may miss.',
    how_teaches:              'Life teaches you through reflection.',
    how_shows:                'You help bring clarity by seeing beneath the surface.',
    op_naturally:             'You naturally perceive deeper patterns others may overlook.',
    op_develops:              'Life often teaches you through periods of withdrawal, reflection, or uncertainty.',
    op_together:              'You often bring clarity by seeing beneath the surface before acting.',
  },

  'purna:Wood': {
    dynamic_type:             'Bringing growth to fulfillment',
    configuration_theme_name: 'The Harvester',
    reveal_statement:         'Your pattern is to bring growth to fulfillment and help development reach completion.',
    recognition_line:         'You may have noticed you often care about bringing things all the way through.',
    pattern_statement:        'You bring growth to fulfillment and help development reach completion.',
    watch_for:                'Pushing for completion too early can interrupt natural maturation.',
    best_use:                 'Bring growth to completion in its right season.',
    how_like:                 'You like helping things reach completion.',
    how_teaches:              'Life teaches you through endings and fulfillment.',
    how_shows:                'You help bring things to completion.',
    op_naturally:             'You naturally bring things toward completion and want growth to bear fruit.',
    op_develops:              'Life often teaches you through cycles of fulfillment and release.',
    op_together:              'You often help bring processes to completion in a way that feels whole.',
  },
  'purna:Fire': {
    dynamic_type:             'Revealing through completion',
    configuration_theme_name: 'The Illuminator',
    reveal_statement:         'Your pattern is to reveal what matters by bringing intensity to completion.',
    recognition_line:         'You may have noticed clarity often emerges for you at the point others reach overwhelm.',
    pattern_statement:        'You reveal what matters by bringing intensity to completion.',
    watch_for:                'Intensity can turn completion into exhaustion.',
    best_use:                 'Bring clarity to completion, and let revelation serve wisdom.',
    how_like:                 'You help bring clarity to what matters.',
    how_teaches:              'Life teaches you through insight.',
    how_shows:                'You help others see more clearly.',
    op_naturally:             'You naturally bring clarity to what matters and reveal what others may miss.',
    op_develops:              'Life often teaches you through moments of realization that change understanding.',
    op_together:              'You often help others see more clearly by bringing insight at the right moment.',
  },
  'purna:Earth': {
    dynamic_type:             'Creating lasting integration',
    configuration_theme_name: 'The Integrator',
    reveal_statement:         'Your pattern is to create wholeness by bringing many parts into lasting coherence.',
    recognition_line:         'You may have noticed you often see how separate pieces belong together.',
    pattern_statement:        'You create wholeness by bringing many parts into lasting coherence.',
    watch_for:                'Trying to hold everything together can become overextension.',
    best_use:                 'Integrate what belongs together, and release what does not.',
    how_like:                 'You like helping things fit together.',
    how_teaches:              'Life teaches you how separate things can work as one.',
    how_shows:                'You help create wholeness.',
    op_naturally:             'You naturally connect pieces into a larger whole.',
    op_develops:              'Life often teaches you through complexity that demands coherence.',
    op_together:              'You often create strength by helping separate parts work together.',
  },
  'purna:Metal': {
    dynamic_type:             'Completing with precision',
    configuration_theme_name: 'The Finisher',
    reveal_statement:         'Your pattern is to strengthen outcomes through precision at the point of completion.',
    recognition_line:         'You may have noticed you often focus on finishing well, not just finishing fast.',
    pattern_statement:        'You strengthen outcomes through precision at the point of completion.',
    watch_for:                'Over-refining can prevent something from ever being finished.',
    best_use:                 'Finish with care, not perfection.',
    how_like:                 'You care about finishing things well.',
    how_teaches:              'Life teaches you through bringing things to completion.',
    how_shows:                'You help strengthen outcomes.',
    op_naturally:             'You naturally want to bring things to completion with care and precision.',
    op_develops:              'Life often teaches you through unfinished things that require closure or refinement.',
    op_together:              'You often strengthen outcomes by helping things reach a more complete form.',
  },
  'purna:Water': {
    dynamic_type:             'Deepening fulfillment through wisdom',
    configuration_theme_name: 'The Wisdom Keeper',
    reveal_statement:         'Your pattern is to deepen fulfillment through reflection, timing, and lived understanding.',
    recognition_line:         'You may have noticed deeper meaning often arrives for you after experience has fully unfolded.',
    pattern_statement:        'You deepen fulfillment through reflection, timing, and lived understanding.',
    watch_for:                'Too much reflection can delay the renewal that completion invites.',
    best_use:                 'Let completion deepen wisdom, then let wisdom open what comes next.',
    how_like:                 'You learn deeply from experience.',
    how_teaches:              'Life teaches you wisdom over time.',
    how_shows:                'You help others through what you\'ve learned.',
    op_naturally:             'You naturally reflect deeply on what experience has taught.',
    op_develops:              'Life often teaches you through endings, reflection, and deeper understanding over time.',
    op_together:              'You often help others by turning lived experience into practical wisdom.',
  },
};

// ── Generation Logic ───────────────────────────────────────────────────────

/**
 * getDynamic — look up the Tithi × Element dynamic pattern.
 * @param {string} tithi   — 'nanda' | 'bhadra' | 'jaya' | 'rikta' | 'purna'
 * @param {string} element — 'Wood' | 'Fire' | 'Earth' | 'Metal' | 'Water'
 * @returns {{ dynamic_type: string, pattern_statement: string } | null}
 */
export function getDynamic(tithi, element) {
  return TITHI_ELEM_DYN[`${tithi}:${element}`] || null;
}

/**
 * generateWatchFor
 * Formula: [Tithi risk] and [Element risk]. This can make it harder to reach [LP outcome].
 * Example: "Over-clearing and burnout can make it harder to reach enduring structures."
 */
export function generateWatchFor(tithi, element, lifePathNum) {
  const t  = TITHI_CCE[tithi];
  const el = ELEMENT_CCE[element];
  const lp = LP_CCE[lifePathNum];
  if (!t || !el || !lp) return null;

  const tWatch  = capitalize(t.watchout_fragment);
  const elWatch = el.watchout_fragment;
  const outcome = lp.outcome.toLowerCase();

  return `${tWatch} and ${elWatch}. This can make it harder to reach ${outcome}.`;
}

/**
 * generateBestUse
 * Formula: [Tithi fragment], [Element fragment], and stay oriented toward [LP outcome].
 * Example: "Clear strategically, use intensity with purpose, and stay oriented toward enduring structures."
 */
export function generateBestUse(tithi, element, lifePathNum) {
  const t  = TITHI_CCE[tithi];
  const el = ELEMENT_CCE[element];
  const lp = LP_CCE[lifePathNum];
  if (!t || !el || !lp) return null;

  const tUse    = capitalize(t.best_use_fragment);
  const elUse   = el.best_use_fragment;
  const outcome = lp.outcome.toLowerCase();

  return `${tUse}, ${elUse}, and stay oriented toward ${outcome}.`;
}

// ── Helpers ────────────────────────────────────────────────────────────────

function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}
