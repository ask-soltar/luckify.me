/**
 * Tithi (Lunar Cycle Position) and Type Configuration
 * Five types: Nanda, Bhadra, Jaya, Rikta, Purna
 */

export const TYPES = ['nanda', 'bhadra', 'jaya', 'rikta', 'purna'];

export const TITHI_NAMES = [
  'The Deal', 'The Hold', 'The Raise', 'The Fold', 'The Pot',
  'The Deal', 'The Hold', 'The Raise', 'The Fold', 'The Pot',
  'The Deal', 'The Hold', 'The Raise', 'The Fold', 'The Pot',
  'The Draw', 'The Check', 'The River', 'The Cut', 'The All-In',
  'The Draw', 'The Check', 'The River', 'The Cut', 'The All-In',
  'The Draw', 'The Check', 'The River', 'The Cut', 'The All-In'
];

export const TYPE_CONFIG = {
  nanda: {
    label: 'Nanda — The Initiator',
    tagline: 'You were born at the moment the universe said yes.',
    badgeBg: 'rgba(127,119,221,0.2)',
    badgeColor: '#AFA9EC',
    glow: 'rgba(127,119,221,0.12)',
    dotActive: 'var(--nanda-color)'
  },
  bhadra: {
    label: 'Bhadra — The Foundation',
    tagline: 'You are the ground others stand on.',
    badgeBg: 'rgba(29,158,117,0.2)',
    badgeColor: '#5DCAA5',
    glow: 'rgba(29,158,117,0.12)'
  },
  jaya: {
    label: 'Jaya — The Overcomer',
    tagline: 'Your greatest payday is always on the other side of the hardest moment.',
    badgeBg: 'rgba(186,117,23,0.2)',
    badgeColor: '#EF9F27',
    glow: 'rgba(186,117,23,0.12)'
  },
  rikta: {
    label: 'Rikta — The Channel',
    tagline: 'Your emptiness is not a lack. It is a portal.',
    badgeBg: 'rgba(216,90,48,0.2)',
    badgeColor: '#F0997B',
    glow: 'rgba(216,90,48,0.12)'
  },
  purna: {
    label: 'Purna — The Vessel',
    tagline: 'You were born full. Now let the world pay for what you carry.',
    badgeBg: 'rgba(55,138,221,0.2)',
    badgeColor: '#85B7EB',
    glow: 'rgba(55,138,221,0.12)'
  }
};

export const TITHI_AXIOMS = {
  nanda: 'Energy initiates at the threshold. The Nanda signal fires at the precise point where something begins. Everything Nanda does is most powerful at the first moment.',
  bhadra: "Energy creates the conditions in which other energies can thrive. Bhadra is the active force that makes the environment favorable. It creates and maintains the field in which others's work becomes possible.",
  jaya: 'Energy activates under resistance. The Jaya signal does not degrade under pressure — it sharpens. Friction and opposition are the operating conditions Jaya requires to run at full output.',
  rikta: 'Energy receives before it transmits, and the void is actively potent inward. The Rikta position marks the reset point. The void is not neutral — it moves inward with the same force that other types move outward.',
  purna: 'Energy completes at maximum illumination. Purna does not just complete things — it reveals them. At Purna, what was hidden becomes visible. What was partial becomes whole.'
};

export const TITHI_SVGS = {
  nanda: `<line x1="10" y1="32" x2="46" y2="32" stroke="#C9A84C" stroke-width="1.5" stroke-linecap="round"/><line x1="28" y1="44" x2="28" y2="14" stroke="#C9A84C" stroke-width="1.5" stroke-linecap="round"/><polyline points="20,22 28,12 36,22" stroke="#C9A84C" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="28" cy="44" r="2.5" fill="#C9A84C"/>`,
  bhadra: `<line x1="12" y1="32" x2="44" y2="32" stroke="#C9A84C" stroke-width="1.5" stroke-linecap="round"/><line x1="28" y1="32" x2="28" y2="44" stroke="#C9A84C" stroke-width="1.5" stroke-linecap="round"/><line x1="28" y1="38" x2="22" y2="43" stroke="#C9A84C" stroke-width="1" stroke-linecap="round" opacity="0.6"/><line x1="28" y1="38" x2="34" y2="43" stroke="#C9A84C" stroke-width="1" stroke-linecap="round" opacity="0.6"/><circle cx="28" cy="32" r="4" stroke="#C9A84C" stroke-width="1.5" fill="rgba(201,168,76,0.15)"/><line x1="28" y1="28" x2="28" y2="16" stroke="#C9A84C" stroke-width="1.5" stroke-linecap="round"/><path d="M28 20 Q34 16 36 12 Q30 13 28 20Z" stroke="#C9A84C" stroke-width="1" fill="rgba(201,168,76,0.2)" stroke-linejoin="round"/>`,
  jaya: `<line x1="8" y1="42" x2="48" y2="42" stroke="#C9A84C" stroke-width="1.5" stroke-linecap="round"/><polyline points="8,42 28,14 48,42" stroke="#C9A84C" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><polyline points="16,42 28,22 40,42" stroke="#C9A84C" stroke-width="0.75" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.35"/><line x1="28" y1="8" x2="28" y2="14" stroke="#C9A84C" stroke-width="1.5" stroke-linecap="round"/><line x1="24" y1="11" x2="32" y2="11" stroke="#C9A84C" stroke-width="1.5" stroke-linecap="round"/><circle cx="28" cy="11" r="2" fill="#C9A84C"/>`,
  rikta: `<circle cx="28" cy="28" r="16" stroke="#C9A84C" stroke-width="1.5" fill="rgba(201,168,76,0.05)"/><circle cx="28" cy="28" r="10" stroke="#C9A84C" stroke-width="0.75" fill="none" opacity="0.4"/><line x1="8" y1="28" x2="48" y2="28" stroke="#C9A84C" stroke-width="1.5" stroke-linecap="round"/><circle cx="8" cy="28" r="2" fill="#C9A84C"/><circle cx="48" cy="28" r="2" fill="#C9A84C"/><circle cx="28" cy="28" r="2.5" fill="rgba(201,168,76,0.6)" stroke="#C9A84C" stroke-width="1"/>`,
  purna: `<path d="M18 16 Q16 28 20 36 Q24 42 28 42 Q32 42 36 36 Q40 28 38 16Z" stroke="#C9A84C" stroke-width="1.5" fill="rgba(201,168,76,0.08)" stroke-linejoin="round"/><path d="M19.5 22 Q24 24 28 24 Q32 24 36.5 22" stroke="#C9A84C" stroke-width="1" stroke-linecap="round" opacity="0.5"/><line x1="28" y1="42" x2="28" y2="47" stroke="#C9A84C" stroke-width="1.5" stroke-linecap="round"/><line x1="22" y1="47" x2="34" y2="47" stroke="#C9A84C" stroke-width="1.5" stroke-linecap="round"/><circle cx="17" cy="17" r="1.5" fill="#C9A84C" opacity="0.6"/><circle cx="39" cy="17" r="1.5" fill="#C9A84C" opacity="0.6"/><line x1="18" y1="16" x2="38" y2="16" stroke="#C9A84C" stroke-width="1.5" stroke-linecap="round"/>`
};

// Complete type descriptions and principles
export const TITHI_DATA = {
  nanda: {
    operating: [
      { title: 'Peak signal output occurs at initiation.', body: 'Your lunar position falls in the early ascending phase — a configuration where elongation between the sun and moon is widening rapidly. Measured energetically, this produces maximum output at the point of entry. Your profile is not designed for maintenance — it is optimized for launch.' },
      { title: 'Excitement registers as a valid data input.', body: 'In the Luckify signal model, emotional resonance is not noise — it is signal. For ascending early-phase profiles, enthusiasm correlates with outcome alignment. When your excitement spikes, the data is telling you something the logic has not caught up to yet.' },
      { title: 'Early recognition is a measurable profile trait, not luck.', body: 'The ascending lunar arc produces a forward-leaning signal bias. You consistently perceive possibilities before supporting evidence exists. This is a calibration feature, not a coincidence. The market catches up to you — not the other way around.' },
      { title: 'The gap between ignition and structure is your primary risk variable.', body: 'Early-phase ascending profiles generate strong initiation energy with a natural decay curve past the launch window. Without a deliberate handoff system — a structure that captures what you start — momentum converts to lost output. Engineer the bridge.' },
      { title: 'Your signal broadcasts outward and influences field behavior.', body: 'High-frequency ascending profiles create measurable environmental effects. When you are operating at full signal strength, the people around you recalibrate — decisions accelerate, energy shifts, outcomes change. This is not personality. It is your profile running at capacity.' }
    ],
    intuitive: [
      { title: 'You start things other people only talk about.', body: 'The business idea, the trip, the conversation nobody else would have — you are the one who actually moves. That is not impulsiveness. That is your wiring doing exactly what it is supposed to do.' },
      { title: 'Your gut fires before your brain finishes the sentence.', body: 'You have probably made a decision before someone finished explaining the situation. And you were probably right. Stop waiting for the full briefing before you act on what you already know.' },
      { title: 'The first version of everything you make is usually the best one.', body: 'Your clearest output comes early — before editing, before doubt, before the committee weighs in. Protect the first draft. Revisit before you revise.' },
      { title: 'You get bored faster than almost everyone around you — and that is information.', body: 'When the excitement leaves, your signal is telling you the relevant work is done. The boredom is not laziness. It is your profile flagging that the next thing is ready.' },
      { title: 'Your energy is the room before you open your mouth.', body: 'People feel you walk in. Meetings shift. Conversations change direction. You probably underestimate how much of that is you and how little of it is what you said.' }
    ]
  },
  bhadra: {
    operating: [
      { title: 'Your profile is configured for sustained output, not peak bursts.', body: 'Bhadra positions in the lunar cycle sit at stable elongation intervals — points where the sun-moon relationship produces consistent, low-variance signal. Your output does not spike and crash. It compounds. That is a structural advantage most profiles cannot replicate.' },
      { title: 'Environmental alignment is a measurable performance variable.', body: 'Stable-phase lunar profiles are highly sensitive to coherence between internal values and external conditions. When misalignment exists, signal efficiency drops measurably. This is not a mood state — it is a performance condition. Treat it like one.' },
      { title: 'Trust accumulates in your profile the way interest accumulates in an account.', body: 'Relationship-based leverage is the primary output mechanism for stable lunar profiles. Every consistent action, every kept commitment, adds to a compounding trust asset. Most people cannot see it building. The data can.' },
      { title: 'Your invisible contributions hold the highest structural value.', body: 'Stable-phase profiles generate a category of output that is difficult to quantify in real time — the stability that makes other things possible. This value is systematically underpriced until it is absent. Document it. Name it. Price it correctly.' },
      { title: 'Depth compounds where speed cannot reach.', body: 'The lunar mechanics of your position reward long-cycle investment — in relationships, skills, and systems. Short-cycle profiles generate faster peaks but higher variance. Your signal is built for the return that takes time to arrive and does not leave.' }
    ],
    intuitive: [
      { title: 'You are the person people call when everything goes sideways.', body: 'Not because you always have the answer. Because your calm is more useful than most people\'s solutions. You have probably talked someone off a ledge without realizing that is what you were doing.' },
      { title: 'You notice the thing nobody else remembered to track.', body: 'The detail in the contract, the tone shift in the conversation, the thing that seemed minor three weeks ago. You filed it. Everyone else forgot. This is not overthinking — it is your signal doing its job.' },
      { title: 'Your best work looks effortless to everyone except you.', body: 'Because you built the foundation so carefully that the output looks inevitable. That invisibility is a feature. It is also something worth naming when the credit gets distributed.' },
      { title: 'You take longer to trust — and your trust means more because of it.', body: 'When you vouch for someone, people listen. When you commit to something, it gets done. That reputation is not accidental. It is the compound interest on every time you showed up when you said you would.' },
      { title: 'Chaos does not rattle you the way it rattles other people.', body: 'When things fall apart around you, you get quieter and clearer. Other people read that as calm. What it actually is — is your signal locking in.' }
    ]
  },
  jaya: {
    operating: [
      { title: 'Your profile activates under pressure — this is measurable, not metaphorical.', body: 'Jaya positions in the lunar cycle correspond to elongation values where the signal is in active transition — neither building nor completing, but pushing through. The data profile for this position shows elevated output under resistance conditions. Friction is not your enemy. It is your activation input.' },
      { title: 'Momentum is a quantifiable asset in your signal model.', body: 'Forward-motion lunar profiles show measurable signal compounding when velocity is maintained. Each completed action increases the output of the next. Stopping to recalibrate costs more than adjusting in motion. Your profile is built for moving corrections, not stationary ones.' },
      { title: 'Pressure-based decision making is a legitimate strategic mode for your profile.', body: 'High-variance, high-pressure environments produce degraded signal in most lunar profiles. Not yours. Jaya positions show signal clarification under load — the more is at stake, the cleaner your read becomes. This is a competitive moat most players do not know you have.' },
      { title: 'Your signal broadcasts dominance before logic confirms it.', body: 'Field-level effects in transition-phase profiles create measurable environmental influence. Before you have spoken, before you have acted, the field around you reconfigures. This is your profile establishing its position. It is not aggression — it is calibration.' },
      { title: 'Distinguish forward motion from displacement.', body: 'Transition-phase profiles carry a shadow variable — using motion as a substitute for resolution. True forward movement in your signal model creates pressure on outcomes and increases measurable progress. Displacement changes location but not trajectory. The data will tell you which one you are doing.' }
    ],
    intuitive: [
      { title: 'You have come back from things that would have ended other people.', body: 'Not once. Multiple times. And you probably do not even count them as comebacks — because for you, coming back is just what happens next. That is not resilience. That is your default setting.' },
      { title: 'You do your best work when the stakes are highest.', body: 'Big presentation, real money on the line, everyone watching — that is when you actually show up fully. The low-stakes version of you is half asleep. The high-stakes version is the real one.' },
      { title: 'Sitting still costs you more than making the wrong move.', body: 'You have probably made a decision just to end the feeling of being stuck — and it worked out fine. Because for you, movement creates clarity. Waiting for clarity before moving is backwards.' },
      { title: 'You root for the underdog because you have been the underdog.', body: 'And because you know something they do not yet — that being counted out is one of the cleanest setups available. You have cashed in on that more than once.' },
      { title: 'Rest feels like falling behind, and you have to keep relearning that it is not.', body: 'Your profile needs recovery to maintain output. But your instinct fights it every time. The solution is not to stop fighting — it is to schedule the rest before your signal forces it.' }
    ]
  },
  rikta: {
    operating: [
      { title: 'Your profile is positioned at the lunar cycle\'s reset point.', body: 'Rikta positions correspond to specific elongation intervals — 4th, 9th, and 14th tithis — where the sun-moon angular relationship produces a measurable signal gap. In the Luckify model, this gap is not a deficit. It is a reception window. Your profile is optimized for input, not output.' },
      { title: 'Stillness produces higher signal yield than activity for your configuration.', body: 'Standard productivity models assume output scales with effort. For Rikta profiles, the data inverts this. Forced output degrades signal quality. Controlled stillness increases it. Your ROI on quiet is measurably higher than your ROI on hustle. This is a profile characteristic, not a personality preference.' },
      { title: 'You operate at the information boundary other profiles cannot access.', body: 'The reset point in the lunar cycle is where pattern data from the descending phase and initiation data from the ascending phase converge simultaneously. Your profile sits at that intersection. The information available to you at that point is not available in any other position.' },
      { title: 'Initiation friction is a documented feature of your signal configuration.', body: 'Starting generates disproportionate resistance in Rikta profiles — this is consistent across the model and is not a personal failure. The friction occurs because your signal is calibrated to receive before it transmits. Acknowledge it as data, build systems that account for it, and move through it anyway.' },
      { title: 'Signal clarity is your primary performance variable.', body: 'Rikta profiles degrade faster under noise conditions than any other configuration — emotional noise, environmental noise, relational noise all measurably reduce output quality. Clarity is not optional for your profile. It is the operating condition everything else depends on.' }
    ],
    intuitive: [
      { title: 'You already know things you have not been told yet.', body: 'The call you were about to make when your phone rang. The thing someone needed to hear that you said without planning to say it. That is not coincidence. That is your profile doing what it does when it is clear.' },
      { title: 'Your best ideas arrive when you stop looking for them.', body: 'The shower. The drive. The moment between sleeping and waking. That is not random — that is the exact condition your signal needs to transmit. You are not avoiding work when you create space. You are doing your actual work.' },
      { title: 'People open up to you in ways they do not open up to others.', body: 'Strangers on planes. Friends who have never told anyone else. People who just met you. You did not earn that by being curious — you earned it by being clear enough that they could feel it was safe. That is a rare thing.' },
      { title: 'Certain people drain you completely and you cannot always explain why.', body: 'You can. Their noise is louder than your signal. It is not about them being bad — it is about the interference. Protecting your energy is not selfish for your profile. It is maintenance.' },
      { title: 'Sometimes the most productive thing you can do is nothing.', body: 'Not scroll. Not plan. Not organize. Nothing. That blank space is where your actual output comes from. Every time you have forced it, you know how that went. Every time you waited, you know what arrived.' }
    ]
  },
  purna: {
    operating: [
      { title: 'Your profile is calibrated at maximum elongation — the completion point.', body: 'Purna positions correspond to the 5th, 10th, and 15th tithis — the points in the lunar cycle where sun-moon elongation reaches its local maximum. In the Luckify signal model, this configuration produces a profile optimized for full-cycle output: you do not just start or sustain — you complete. That is the rarest signal position in the system.' },
      { title: 'Completion is a measurable competitive advantage, not a personality trait.', body: 'Most signal profiles initiate well and decay before full expression. Purna profiles show consistent terminal output — the ability to bring things to their fullest state. In any system where finishing matters — creative, financial, relational — your configuration holds disproportionate leverage at the close.' },
      { title: 'You hold a full-cycle view that other profiles access only partially.', body: 'Maximum elongation produces a panoramic signal — you can see the completed state of things that are still in progress. This is not optimism. It is a profile-level data capability. Other people are working with partial information. You are working with the completed picture.' },
      { title: 'Abundance in your model is an open-system function, not an accumulation function.', body: 'Purna profiles operating as closed systems — hoarding output, restricting flow — show measurable signal degradation. The configuration is designed for throughput, not storage. The more freely the signal moves through you, the stronger it gets. Restriction weakens it.' },
      { title: 'Discernment is the discipline that keeps your signal clean.', body: 'Maximum-elongation profiles carry a shadow variable — over-extension. Taking on completions that are not yours, finishing things that needed to remain unfinished, absorbing others\' output until your own degrades. Discernment is not a soft skill for your profile. It is a hard boundary that keeps the system running.' }
    ],
    intuitive: [
      { title: 'You walk into rooms and things settle — and you probably have no idea you are doing it.', body: 'The conversation that was getting heated. The energy that was scattered. The person who was about to leave. Something shifts when you arrive. People feel it before you say anything. That is not an accident.' },
      { title: 'You cannot leave things at 90 percent — it physically bothers you.', body: 'The tab still open. The conversation that ended without resolution. The project that got shelved at almost-done. You feel it. Most people can walk away. You carry it until it is finished. That is not a flaw. That is your profile doing its job.' },
      { title: 'People come to you when they need to feel like things are going to be okay.', body: 'And here is the thing — around you, they usually are. Not because you fix everything. Because your presence carries a frequency that makes resolution feel possible. That is not small. That is one of the most valuable things a person can offer.' },
      { title: 'Your generosity runs ahead of your replenishment and you have to watch for that.', body: 'You give before you are asked. You finish what others started. You hold space long after others have left. All of that costs something. The overflow is real. Build in the refill before the tank hits empty — not after.' },
      { title: 'The people who called you too much were just telling you about themselves.', body: 'Too generous. Too present. Too complete. That feedback was never about you being wrong. It was about them not being able to hold what you were carrying. Stay full. The right people will not ask you to be less.' }
    ]
  }
};
