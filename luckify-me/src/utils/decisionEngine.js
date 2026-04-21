const DECISION_ENGINE_COPY = {
  emotional: {
    engineName: 'Wave Engine',
    microTag: 'Wait for the settle',
    essenceLine: 'Your clarity arrives when emotion settles into something steady enough to trust.',
    coreInstruction: 'Do not decide at the high or the low. Let the wave move, then choose from the calm.',
    recognitionTitle: 'How it tends to show up',
    recognitionText: 'You can feel sure in one moment and unsure in the next. What stays true after the wave passes is usually the real signal.',
    supportTitle: 'What this helps you do',
    supportText: 'This protects you from reacting to temporary intensity and helps you trust what still feels right once the charge has cleared.',
    expansionTitle: 'Build steadier clarity',
    expansionText: 'Give important decisions enough time to breathe. Your strongest choices come from emotional steadiness, not emotional speed.',
    iconDirection: ['Settling wave', 'Delayed confirm', 'Steady horizon'],
    keywords: ['timing', 'settling', 'clarity', 'steadiness'],
  },
  sacral: {
    engineName: 'Response Engine',
    microTag: 'Respond to what is real',
    essenceLine: 'Your clarity shows up as an immediate body response to what is actually in front of you.',
    coreInstruction: 'Wait for something concrete to respond to, then trust the body signal that follows.',
    recognitionTitle: 'How it tends to show up',
    recognitionText: 'You often know quickly whether something has energy for you. The response is simple, physical, and easier to feel than to explain.',
    supportTitle: 'What this helps you do',
    supportText: 'This keeps you from forcing decisions from the head and helps you trust where real energy, availability, and aliveness are present.',
    expansionTitle: 'Let the body answer first',
    expansionText: 'Give yourself real prompts, real options, and real choices to respond to. Your most reliable clarity is live, embodied, and immediate.',
    iconDirection: ['Pulse check', 'Body yes-no', 'Live prompt'],
    keywords: ['response', 'energy', 'gut', 'aliveness'],
  },
  splenic: {
    engineName: 'Instinct Engine',
    microTag: 'Trust the first clean hit',
    essenceLine: 'Your clarity arrives as a quick, quiet instinct that is strongest in the first moment.',
    coreInstruction: 'Catch the first clean signal before the mind starts negotiating with it.',
    recognitionTitle: 'How it tends to show up',
    recognitionText: 'The knowing is often subtle, immediate, and easy to miss if you are waiting for it to become louder.',
    supportTitle: 'What this helps you do',
    supportText: 'This protects you from overthinking a precise signal and helps you trust timing, instinct, and real-time discernment.',
    expansionTitle: 'Honor the quiet precision',
    expansionText: 'Your clarity does not need to be dramatic to be real. The more you respect the first clean signal, the easier it becomes to recognize.',
    iconDirection: ['Quick flash', 'Quiet ping', 'Precision lock'],
    keywords: ['instinct', 'timing', 'precision', 'signal'],
  },
  ego: {
    engineName: 'Will Engine',
    microTag: 'Back what you truly want',
    essenceLine: 'Your clarity comes from knowing what you genuinely want to commit your will and energy toward.',
    coreInstruction: 'Check whether you truly want to back it before you promise, push, or prove anything.',
    recognitionTitle: 'How it tends to show up',
    recognitionText: 'You feel clearer when desire and commitment are real. If the will is not there, forcing it usually creates strain.',
    supportTitle: 'What this helps you do',
    supportText: 'This protects you from overcommitting to what is not truly yours and helps you trust authentic desire, backing, and self-led commitment.',
    expansionTitle: 'Commit from truth, not pressure',
    expansionText: 'Your decisions get stronger when you stop spending willpower to satisfy expectation and start using it for what you genuinely want to stand behind.',
    iconDirection: ['Commit lock', 'Focused drive', 'Backed choice'],
    keywords: ['will', 'desire', 'commitment', 'backing'],
  },
  selfProjected: {
    engineName: 'Voice Engine',
    microTag: 'Hear yourself clearly',
    essenceLine: 'Your clarity emerges when you speak and hear your own truth out loud.',
    coreInstruction: 'Talk it through in a safe space and notice what feels true as you hear yourself say it.',
    recognitionTitle: 'How it tends to show up',
    recognitionText: 'You often discover alignment in the act of speaking. The right direction becomes clearer when your words sound true in real time.',
    supportTitle: 'What this helps you do',
    supportText: 'This protects you from outsourcing your direction and helps you trust identity, self-expression, and the truth in your own voice.',
    expansionTitle: 'Let your voice reveal direction',
    expansionText: 'You do not need outside answers as much as the right space to hear yourself clearly. Your own voice is often the doorway to alignment.',
    iconDirection: ['Open channel', 'Truth echo', 'Voice line'],
    keywords: ['voice', 'identity', 'expression', 'alignment'],
  },
  mental: {
    engineName: 'Resonance Engine',
    microTag: 'Use the right environment',
    essenceLine: 'Your clarity becomes visible through the right setting, perspective, and reflective conversation.',
    coreInstruction: 'Do not force certainty in the wrong context. Change the space, reflect aloud, and notice what becomes clear.',
    recognitionTitle: 'How it tends to show up',
    recognitionText: 'You often think more clearly when the environment feels right and when you can hear your thoughts reflected without pressure.',
    supportTitle: 'What this helps you do',
    supportText: 'This protects you from premature decisions in the wrong atmosphere and helps you trust resonance, perspective, and environmental fit.',
    expansionTitle: 'Let context do its work',
    expansionText: 'Your clarity is relational. The right room, rhythm, and sounding board can reveal what force never will.',
    iconDirection: ['Resonance ring', 'Space shift', 'Reflective loop'],
    keywords: ['resonance', 'context', 'reflection', 'perspective'],
  },
  lunar: {
    engineName: 'Cycle Engine',
    microTag: 'Move with the full cycle',
    essenceLine: 'Your clarity arrives over time as you experience a decision across different phases, moods, and environments.',
    coreInstruction: 'Sample the decision across time instead of locking it in too early.',
    recognitionTitle: 'How it tends to show up',
    recognitionText: 'What seems certain in one moment can shift as you move through different phases. The full picture appears by living with it longer.',
    supportTitle: 'What this helps you do',
    supportText: 'This protects you from premature certainty and helps you trust timing, perspective shifts, and a fuller decision cycle.',
    expansionTitle: 'Let time complete the picture',
    expansionText: 'You are not here for instant certainty. Your most reliable clarity comes from watching what remains true across the cycle.',
    iconDirection: ['Orbit path', 'Phase marker', 'Cycle track'],
    keywords: ['cycles', 'timing', 'patience', 'perspective'],
  },
};

function normalizeAuthorityType(authorityType = '') {
  switch (authorityType) {
    case 'Emotional Authority':
      return 'emotional';
    case 'Sacral Authority':
      return 'sacral';
    case 'Splenic Authority':
      return 'splenic';
    case 'Ego Manifested Authority':
    case 'Ego Projected Authority':
    case 'Ego Authority':
    case 'Will Authority':
      return 'ego';
    case 'Self-Projected Authority':
      return 'selfProjected';
    case 'Mental / Environmental Authority':
    case 'Mental Authority':
    case 'Environmental Authority':
      return 'mental';
    case 'Lunar Authority':
      return 'lunar';
    default:
      return null;
  }
}

export function getDecisionEnginePayload(authorityType) {
  const normalizedAuthority = normalizeAuthorityType(authorityType);

  if (!normalizedAuthority) {
    return {
      sectionLabel: 'Decision Engine',
      authorityType: authorityType || 'Unknown Authority',
      engineName: 'Decision Engine',
      microTag: 'Clarity not available',
      essenceLine: 'This decision pattern is not available yet.',
      coreInstruction: 'Confirm the authority type before generating this panel.',
      recognitionTitle: 'Status',
      recognitionText: 'A recognized authority type is required to build this payload.',
      supportTitle: 'What this affects',
      supportText: 'The decision engine depends on the chart’s resolved authority.',
      expansionTitle: 'Next step',
      expansionText: 'Provide a supported authority type and this section can be generated normally.',
      iconDirection: ['Pending signal', 'Unknown path', 'Hold state'],
      keywords: ['pending', 'clarity', 'mapping', 'authority'],
    };
  }

  const copy = DECISION_ENGINE_COPY[normalizedAuthority];

  return {
    sectionLabel: 'Decision Engine',
    authorityType,
    engineName: copy.engineName,
    microTag: copy.microTag,
    essenceLine: copy.essenceLine,
    coreInstruction: copy.coreInstruction,
    recognitionTitle: copy.recognitionTitle,
    recognitionText: copy.recognitionText,
    supportTitle: copy.supportTitle,
    supportText: copy.supportText,
    expansionTitle: copy.expansionTitle,
    expansionText: copy.expansionText,
    iconDirection: copy.iconDirection,
    keywords: copy.keywords,
  };
}
