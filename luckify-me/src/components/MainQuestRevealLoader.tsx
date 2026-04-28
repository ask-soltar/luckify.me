import { useState, useEffect } from 'react';

export type QuestRevealOption = {
  gateLine: string;
  questName: string;
  subtitle?: string;
};

type Phase = 'scanning' | 'roulette' | 'landing';

const SCAN_MESSAGES = [
  'Reading birth pattern…',
  'Locating Design Earth signal…',
  'Scanning possible quests…',
  'Main Quest found.',
];

const SCAN_DELAYS = [600, 700, 800, 900];

function buildRouletteSequence(
  options: QuestRevealOption[],
  resolved: QuestRevealOption,
): QuestRevealOption[] {
  const pool = options.filter(o => o.gateLine !== resolved.gateLine);
  const shuffled = [...pool].sort(() => Math.random() - 0.5);
  return [
    shuffled[0], shuffled[1], shuffled[2], shuffled[3],
    shuffled[4],
    resolved,
    shuffled[5], shuffled[6],
    resolved,
    shuffled[7],
    resolved,
  ].filter(Boolean);
}

function getRevealCadence(len: number): number[] {
  return Array.from({ length: len }, (_, i) => {
    const p = i / Math.max(len - 1, 1);
    if (p < 0.35) return 160;
    if (p < 0.7)  return 300;
    if (p < 0.88) return 560;
    return 900;
  });
}

export function MainQuestRevealLoader({
  resolvedGateLine,
  resolvedQuestName,
  possibleQuests,
  onComplete,
}: {
  resolvedGateLine: string;
  resolvedQuestName: string;
  possibleQuests: QuestRevealOption[];
  onComplete: () => void;
  durationMs?: number;
}) {
  const prefersReducedMotion =
    typeof window !== 'undefined' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const resolved: QuestRevealOption = {
    gateLine: resolvedGateLine,
    questName: resolvedQuestName,
    subtitle: 'Purpose Signal · Design Earth',
  };

  const [phase, setPhase] = useState<Phase>(prefersReducedMotion ? 'landing' : 'scanning');
  const [scanIdx, setScanIdx] = useState(0);
  const [displayQuest, setDisplayQuest] = useState<QuestRevealOption>(
    prefersReducedMotion ? resolved : (possibleQuests[0] ?? resolved),
  );

  // Phase 1: scan messages
  useEffect(() => {
    if (phase !== 'scanning') return;
    let i = 0;
    let t: ReturnType<typeof setTimeout>;
    function tick() {
      i++;
      if (i < SCAN_MESSAGES.length) {
        setScanIdx(i);
        t = setTimeout(tick, SCAN_DELAYS[i]);
      } else {
        t = setTimeout(() => setPhase('roulette'), 300);
      }
    }
    t = setTimeout(tick, SCAN_DELAYS[0]);
    return () => clearTimeout(t);
  }, [phase]);

  // Phase 2: roulette
  useEffect(() => {
    if (phase !== 'roulette') return;
    const sequence = buildRouletteSequence(possibleQuests, resolved);
    const cadence = getRevealCadence(sequence.length);
    let step = 0;
    let t: ReturnType<typeof setTimeout>;
    function tick() {
      if (step >= sequence.length) {
        setDisplayQuest(resolved);
        setPhase('landing');
        return;
      }
      setDisplayQuest(sequence[step]);
      t = setTimeout(tick, cadence[step]);
      step++;
    }
    tick();
    return () => clearTimeout(t);
  }, [phase]);

  // Phase 3: landing — ring emerges, then hand off to share card
  useEffect(() => {
    if (phase !== 'landing') return;
    const delay = prefersReducedMotion ? 400 : 2800;
    const t = setTimeout(onComplete, delay);
    return () => clearTimeout(t);
  }, [phase, onComplete, prefersReducedMotion]);

  const isLanding = phase === 'landing';

  return (
    <div className="mqrl">
      {/* Portal layer — mandala zooms inward like a black-hole pull */}
      <div className="mq-portal-layer" aria-hidden="true">
        <div className="mq-portal-image" />
        <div className="mq-portal-core" />
        <div className="mq-portal-vignette" />
      </div>
      <div className="mqrl__cosmos" aria-hidden="true" />

      {phase === 'scanning' && (
        <div className="mqrl__scan-phase" role="status" aria-live="polite">
          <div className="mqrl__scan-eyebrow">Main Quest</div>
          {SCAN_MESSAGES.map((msg, i) => (
            <div
              key={i}
              className={[
                'mqrl__scan-line',
                i === scanIdx ? 'mqrl__scan-line--active' : '',
                i < scanIdx  ? 'mqrl__scan-line--done'   : '',
                i > scanIdx  ? 'mqrl__scan-line--pending' : '',
              ].filter(Boolean).join(' ')}
            >
              <span className="mqrl__scan-pip" aria-hidden="true">
                {i < scanIdx ? '✓' : '·'}
              </span>
              <span>{msg}</span>
            </div>
          ))}
        </div>
      )}

      {(phase === 'roulette' || phase === 'landing') && (
        <div
          className={[
            'mqrl__roulette',
            isLanding ? 'mqrl__roulette--landing' : '',
            isLanding ? 'mqrl__roulette--unlocked' : '',
          ].filter(Boolean).join(' ')}
          role={isLanding ? 'status' : undefined}
          aria-live={isLanding ? 'polite' : undefined}
        >
          <div className={`mqrl__roulette-eyebrow${isLanding ? ' mqrl__roulette-eyebrow--unlocked' : ''}`}>
            {isLanding ? 'MAIN QUEST UNLOCKED' : 'Scanning possible quests'}
          </div>

          {/* Wrap card in mq-title-reveal during landing so ring positions correctly */}
          <div className={isLanding ? 'mq-title-reveal' : undefined}>
            {isLanding && (
              <div className="mq-emergence-ring" aria-hidden="true">
                <span className="mq-ring mq-ring-1" />
                <span className="mq-ring mq-ring-2" />
                <span className="mq-ring mq-ring-3" />
              </div>
            )}
            <div
              className="mqrl__roulette-card"
              key={displayQuest.gateLine + displayQuest.questName}
            >
              <div className="mqrl__roulette-gate">{displayQuest.gateLine}</div>
              <div className="mqrl__roulette-name">{displayQuest.questName}</div>
              <div className="mqrl__roulette-sub">
                {displayQuest.subtitle ?? 'Purpose Signal'}
              </div>
            </div>
          </div>

          {!isLanding && (
            <div className="mqrl__roulette-dots" aria-hidden="true">
              <span /><span /><span />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
