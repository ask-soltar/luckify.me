/**
 * Color Rhythm Framework — Lucky Window Color Zones
 * Source: Project Soltar / Lucky window calculator / *_rhythm_framework.html
 *
 * Each color zone represents a distinct energetic rhythm, activated by daily
 * lucky window scores. Colors can also be present as birth rhythms.
 *
 * Score mapping (BaZi delta from baseline):
 *   Pink   → +14 to +20  (Dominant Rhythm)
 *   Orange → +7  to +13  (Prime Rhythm)
 *   Blue   → +4  to +6   (Sub-Prime Rhythm)
 *   Yellow → +3  to −2   (Edge / Neutral Rhythm)
 *   Green  → pockets     (Stable Equilibrium)
 *   Purple → −5  to −9   (Identity Rhythm)
 *   Red    → −16 to −29  (Catalyst Rhythm)
 *   Brown  → −30 to −40  (Depth Rhythm)
 */

export const COLOR_RHYTHM = {
  pink: {
    name: 'Pink',
    scoreRange: '+14 to +20',
    zone: 'Dominant Rhythm',
    identity: 'The Sparkplug',
    hex: '#D030A0',
    description: 'Pink is the rhythm of self-expression at its most concentrated. It fires fast, moves first, and dominates its environment when fully activated. Its core identity is not performance — it is authentic energetic ignition. Pink does not build toward expression; Pink is expression. The burst is the nature, not a symptom of it.',
    categories: [
      { name: 'Short-Term Cycles', desc: 'Day-to-day and week-to-week rhythm expression. Pink manifests most visibly here — quick starts, fast relationship arcs, habitual momentum, and rapid opinion shifts.' },
      { name: 'Long-Term Cycles', desc: '12-year Zodiac cycles. Pink\'s burst nature plays out at macro scale — major life initiations, relationship chapters, and identity pivots follow the same fast-ignite pattern.' },
      { name: 'Dopamine Activation', desc: 'Dopamine is the primary fuel of Pink — not a byproduct. The rhythm is ignited by dopaminergic triggers and the cycle feeds back on itself, creating characteristic urgency and risk appetite.' },
      { name: 'Body Energy Adaptation', desc: 'Pink requires physical consistency to regulate its rhythm. Without body-cycle anchoring, the burst pattern overextends and exhausts. Consistency is the stabilizer — not restraint.' }
    ],
    traits: [
      { name: 'Manifestor / Quick Starter', nature: 'asset' },
      { name: 'Good Anticipator', nature: 'asset' },
      { name: 'Habitual', nature: 'dual' },
      { name: 'Constantly Changing Opinions', nature: 'dual' },
      { name: 'High Visibility', nature: 'asset' },
      { name: 'Easily Provoked', nature: 'liability' },
      { name: 'Physical Energy Reliant', nature: 'dual' }
    ],
    boostState: 'When birth rhythm is Pink AND in a Pink window — all traits intensify, dominance is amplified, and the full Sparkplug expression is available.'
  },

  orange: {
    name: 'Orange',
    scoreRange: '+7 to +13',
    zone: 'Prime Rhythm',
    identity: 'The Metaphysical Shield',
    hex: '#E07820',
    description: 'Orange is the rhythm of creative foundation. It does not create through inspiration or impulse — it creates by building something stable enough to create from. Stability is Orange\'s defense mechanism and its methodology. The shield protects the creative process by eliminating instability before it can interfere. Creativity is the output. Security is the engine.',
    categories: [
      { name: 'General Activities / Day-to-Day', desc: 'Orange windows are practical and productive. Best for building, repairing, completing, and steady problem-solving. The rhythm favors hands-on creation and gap-filling.' },
      { name: 'Problem Solving', desc: 'Orange applies creative intelligence to practical problems. It sees gaps and fills them — methodically, without drama. Not the flashiest approach, but the most durable.' },
      { name: 'Foundation Work', desc: 'Projects started in Orange windows tend to stabilize and persist. The rhythm creates the underlying structure that supports everything built on top of it.' },
      { name: 'Protective Action', desc: 'Orange windows favor actions that prevent future problems — maintenance, preparation, and proactive defense. The shield does not wait for the attack.' }
    ],
    traits: [
      { name: 'Steady Builder', nature: 'asset' },
      { name: 'Gap-Filler', nature: 'asset' },
      { name: 'Protective Instinct', nature: 'asset' },
      { name: 'Practical Intelligence', nature: 'asset' },
      { name: 'Slow to Change', nature: 'dual' },
      { name: 'Low Visibility', nature: 'dual' },
      { name: 'Foundation Dependency', nature: 'liability' }
    ],
    boostState: 'Orange birth rhythm holders in an Orange window experience maximum creative productivity. The Shield is fully activated — build aggressively in this state.'
  },

  blue: {
    name: 'Blue',
    scoreRange: '+4 to +6',
    zone: 'Sub-Prime Rhythm',
    identity: 'The Pursuer',
    hex: '#3080D0',
    description: 'Blue is the rhythm of curiosity in motion — capable of a fast rise to success and equally susceptible to great falls. The Pursuer is always moving toward something: an environment to read, a goal to chase, a puzzle to solve, a connection to make. Blue does not operate in a straight line — it operates in cycles that may connect across time itself, picking up where a previous arc left off across sessions, days, or years.',
    categories: [
      { name: 'Short Term', desc: 'Blue moves quickly through environments, reading them and extracting what\'s useful. Short sessions can be highly productive. Fatigue comes fast — exit before the peak breaks.' },
      { name: 'Long Term', desc: 'Blue arcs can span years. A Pursuer doesn\'t abandon goals — they pause them. The same cycle can be resumed after a gap of weeks, months, or longer.' },
      { name: 'Mental', desc: 'Blue is primarily a mental rhythm. Pattern recognition, environmental reading, and strategic curiosity are its primary tools. It thinks before it moves.' },
      { name: 'Environmental Reading', desc: 'Blue\'s most powerful skill is reading environments accurately and quickly. When the read is wrong, the fall is steep. Slow down when the environment is unfamiliar.' }
    ],
    traits: [
      { name: 'Fast Environmental Reader', nature: 'asset' },
      { name: 'Curious / Investigative', nature: 'asset' },
      { name: 'Cyclic Consistency', nature: 'asset' },
      { name: 'High Fall Risk', nature: 'liability' },
      { name: 'Mental Overload', nature: 'liability' },
      { name: 'Peak Hesitation', nature: 'dual' },
      { name: 'Re-entry Ability', nature: 'asset' }
    ],
    boostState: 'Blue birth rhythm in a Blue window: maximum pursuit capacity. Fast read, fast rise. Know when to exit — the Pursuer\'s weakness is staying past the peak.'
  },

  yellow: {
    name: 'Yellow',
    scoreRange: '+3 to −2',
    zone: 'Edge / Neutral Rhythm',
    identity: 'The Phoenix',
    hex: '#D4A820',
    description: 'Yellow is the berserker rhythm — an extreme approach to everything it touches. It does not operate on a moderate register. It detonates. The Phoenix identity names the core arc: destruction and rebirth are the same motion. Yellow doesn\'t recover from its extremes — it becomes through them. Yellow holds the system\'s true neutral at score 0, the baseline before any energetic filter is applied.',
    categories: [
      { name: 'Manifestation', desc: 'Yellow manifests through extremity. It doesn\'t nudge toward goals — it erupts into them. Clarity of intent is critical because the force cannot be recalled once released.' },
      { name: 'Mental', desc: 'Yellow\'s mental state is all-or-nothing. Laser focus or complete shutdown. There is rarely a middle register. This makes Yellow highly effective in bursts, dangerous in fatigue.' },
      { name: 'Emotional', desc: 'Emotional expression in Yellow is intense and unfiltered. What Yellow feels, it shows — often loudly. This is the rhythm\'s greatest vulnerability and its most authentic power.' },
      { name: 'Zero Point', desc: 'Yellow at score 0 is the system\'s true neutral. Not advantageous or disadvantageous — simply unfiltered. Whatever is already in motion expresses without dampening.' }
    ],
    traits: [
      { name: 'Extreme Manifestor', nature: 'asset' },
      { name: 'Laser Focus', nature: 'dual' },
      { name: 'Emotional Detonator', nature: 'dual' },
      { name: 'Phoenix Resilience', nature: 'asset' },
      { name: 'No Middle Register', nature: 'liability' },
      { name: 'Total Commitment', nature: 'dual' },
      { name: 'Burnout Susceptibility', nature: 'liability' }
    ],
    boostState: 'Yellow birth rhythm in a Yellow window: the extreme amplifies. Detonations are larger. Rebirths are faster. Maintain clarity of intent — the force is unregulated.'
  },

  green: {
    name: 'Green',
    scoreRange: 'Stable Pockets',
    zone: 'Equilibrium Rhythm',
    identity: 'Cosmic',
    hex: '#28A870',
    description: 'Green is the rhythm of balance and connection — the first rhythm in the system that operates primarily on others and on environments rather than on the self. Where Pink ignites, Orange builds, and Yellow detonates, Green attunes. It reads what is out of equilibrium and moves toward resolution. The core mechanism is not expression but projection and matching — transmitting stabilizing energy outward and synchronizing with what is present.',
    categories: [
      { name: 'Emotional Aura Projection', desc: 'Green projects a stabilizing emotional field into environments. People near a Green rhythm feel more balanced. This is not performed — it is an ambient transmission.' },
      { name: 'Manifestation Touch Projection', desc: 'Green activates through physical contact and spatial connection. It stabilizes what it touches — objects, spaces, people. Handshakes, physical presence, and environmental work are high-output modes.' },
      { name: 'Manifestation Adjustment Matching', desc: 'Green reads imbalance and adjusts to match it before resolving it. This empathic lock is its strongest tool and its greatest drain. Mismatched environments exhaust Green rapidly.' },
      { name: 'System Stabilization', desc: 'Green sits at the equilibrium pockets of the window score system — stabilizing the zones of highest turbulence. It is the system\'s relational intelligence, filling gaps between extremes.' }
    ],
    traits: [
      { name: 'Empathic Field Projector', nature: 'asset' },
      { name: 'Environmental Stabilizer', nature: 'asset' },
      { name: 'Physical Connector', nature: 'asset' },
      { name: 'Absorbs Imbalance', nature: 'liability' },
      { name: 'Boundary Vulnerability', nature: 'liability' },
      { name: 'Long-Range Relational Memory', nature: 'dual' },
      { name: 'Quiet Influence', nature: 'asset' }
    ],
    boostState: 'Green birth rhythm in a Green pocket: maximum stabilization capacity. Environments shift toward resolution in your presence. Be mindful of absorption drain.'
  },

  purple: {
    name: 'Purple',
    scoreRange: '−5 to −9',
    zone: 'Identity Rhythm',
    identity: 'The Cautious',
    hex: '#7850C8',
    description: 'Purple is the rhythm of purpose — slow-building, future-oriented, and deeply self-aware. Where Pink ignites in the present moment, Purple is already moving toward what\'s coming. It doesn\'t start fast — it builds until momentum is sufficient, then sustains with remarkable endurance. Its core identity is not caution for its own sake, but purposeful deliberation — knowing exactly what it\'s building toward before committing to the build.',
    categories: [
      { name: 'Manifestation', desc: 'Purple manifests through sustained effort over time. It does not sprint — it builds. Large goals are natural territory. Short-term thinking is the Purple rhythm\'s primary liability.' },
      { name: 'Mental', desc: 'Purple\'s mental architecture is future-focused and strategic. It models multiple futures simultaneously and selects paths by predicted outcome rather than present opportunity.' },
      { name: 'Emotional', desc: 'Emotionally, Purple runs deep and slow. It does not react quickly — it processes. Emotional expression, when it comes, carries the weight of everything held before it.' },
      { name: 'Long-Game Strategy', desc: 'Purple is the system\'s long-game player. It sacrifices short-term gains for positional advantage. Patience is not passivity — it is active preparation.' }
    ],
    traits: [
      { name: 'Long-Game Strategist', nature: 'asset' },
      { name: 'Future Modeler', nature: 'asset' },
      { name: 'Deep Emotional Reserves', nature: 'dual' },
      { name: 'Slow to Start', nature: 'dual' },
      { name: 'Endurance Runner', nature: 'asset' },
      { name: 'Short-Term Blind Spot', nature: 'liability' },
      { name: 'Deliberation Under Pressure', nature: 'asset' }
    ],
    boostState: 'Purple birth rhythm in a Purple window: the long-game operates at full power. Momentum is available. Commit now to what you have been building — the window sustains it.'
  },

  red: {
    name: 'Red',
    scoreRange: '−16 to −29',
    zone: 'Catalyst Rhythm',
    identity: 'The Catalyst',
    hex: '#D03820',
    description: 'Red is the weapon rhythm — dynamic, forceful, and direct. Its nature is rapid onset and equally fast dissipation. A Red firing leaves a residue bump that shifts the baseline — up or down — regardless of the direction of the original impact. A negative provocation can produce a positive field shift. Each firing shifts the ambient baseline slightly, and repeated firings compound that shift until the environment reaches a threshold — and detonates. The bomb is not the strike. It is the accumulation.',
    categories: [
      { name: 'Field Accumulation', desc: 'Red actions accumulate. Each firing adds to a running field baseline. The effects are not immediate — they compound. Plan Red windows knowing the residue will outlast the action.' },
      { name: 'Authority Mode', desc: 'Red requires authority to operate cleanly. Proceed with full commitment or not at all. Half-measures in Red windows are more dangerous than abstaining.' },
      { name: 'Rapid Onset', desc: 'Red fires fast and dissipates fast. The window of maximum impact is narrow. Those who catch it act decisively. Those who hesitate watch the moment pass.' },
      { name: 'Residue Effects', desc: 'Red always leaves a residue. Plan for aftermath — not just the action itself. The environment after a Red firing is different from the environment before it.' }
    ],
    traits: [
      { name: 'Catalytic Force', nature: 'asset' },
      { name: 'Field Accumulator', nature: 'dual' },
      { name: 'Authority Projector', nature: 'asset' },
      { name: 'Rapid Onset', nature: 'asset' },
      { name: 'Residue Risk', nature: 'liability' },
      { name: 'High Impact / High Aftermath', nature: 'dual' },
      { name: 'Compound Effect', nature: 'dual' }
    ],
    boostState: 'Red birth rhythm in a Red window: catalytic power is maximized. The accumulation is faster, the residue is stronger. Proceed with absolute authority or stand down entirely.'
  },

  brown: {
    name: 'Brown',
    scoreRange: '−30 to −40',
    zone: 'Depth Rhythm',
    identity: 'The Anchor',
    hex: '#8B5E3C',
    description: 'Brown is the rhythm of depth and grounding — the lowest zone in the scoring system and the most stabilized state. Where Red accumulates field energy and detonates, Brown absorbs it. Brown windows and birth rhythms operate in the deepest registers of the system: slow, heavy, gravitational. The Anchor does not move quickly, but what it holds, it holds permanently.',
    categories: [
      { name: 'Deep Grounding', desc: 'Brown provides the deepest grounding force in the system. Environments and individuals near a Brown rhythm become more anchored — sometimes against their will.' },
      { name: 'Absorption', desc: 'Brown absorbs energetic excess from surrounding zones. It is the system\'s pressure valve — pulling accumulated Red and other high-residue energies downward and neutralizing them.' },
      { name: 'Permanence', desc: 'What Brown builds or holds is meant to last. Brown windows are for decisions and structures intended to persist for years or decades. Not for short-term plays.' },
      { name: 'Gravitational Pull', desc: 'Brown exerts a gravitational effect on those around it. It does not announce — it draws. Those in a Brown rhythm\'s field often feel pulled toward stability without understanding why.' }
    ],
    traits: [
      { name: 'Deep Anchor', nature: 'asset' },
      { name: 'Energetic Absorber', nature: 'dual' },
      { name: 'Permanence Builder', nature: 'asset' },
      { name: 'Gravitational Presence', nature: 'asset' },
      { name: 'Slow to Initiate', nature: 'liability' },
      { name: 'Resistance to Change', nature: 'liability' },
      { name: 'Long-Duration Endurance', nature: 'asset' }
    ],
    boostState: 'Brown birth rhythm in a Brown window: maximum grounding. The field stabilizes completely. Use this window only for decisions you intend to carry for years.'
  }
};

/**
 * Map tithi types to their corresponding color rhythm zones.
 * Based on energetic archetype alignment.
 */
export const TITHI_COLOR_MAP = {
  nanda:  'pink',    // Initiator → Sparkplug (both ignite at the first moment)
  bhadra: 'green',   // Foundation → Cosmic (both create the field others operate in)
  jaya:   'orange',  // Overcomer → Metaphysical Shield (both build through resistance)
  rikta:  'purple',  // Channel → Cautious (both receive before they transmit, long-game)
  purna:  'blue'     // Vessel → Pursuer (both cycle through fullness and pursuit)
};

/**
 * Get color rhythm data for a tithi type
 */
export function getColorRhythm(tithiType) {
  const colorKey = TITHI_COLOR_MAP[tithiType];
  return colorKey ? COLOR_RHYTHM[colorKey] : null;
}
