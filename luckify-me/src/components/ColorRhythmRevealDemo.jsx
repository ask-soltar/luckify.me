import { useEffect, useMemo, useRef, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';

const RHYTHMS = ['PINK', 'ORANGE', 'BLUE', 'YELLOW', 'GREEN', 'PURPLE', 'RED'];

const RHYTHM_STYLES = {
  PINK: {
    glow: 'rgba(234, 72, 153, 0.28)',
    line: 'rgba(244, 114, 182, 0.34)',
    chip: 'rgba(244, 114, 182, 0.12)',
    title: 'text-pink-200',
    aura: 'from-pink-400/24 via-fuchsia-300/10 to-transparent',
  },
  ORANGE: {
    glow: 'rgba(249, 115, 22, 0.26)',
    line: 'rgba(251, 146, 60, 0.34)',
    chip: 'rgba(251, 146, 60, 0.12)',
    title: 'text-orange-200',
    aura: 'from-orange-400/24 via-amber-300/10 to-transparent',
  },
  BLUE: {
    glow: 'rgba(96, 165, 250, 0.3)',
    line: 'rgba(125, 182, 255, 0.34)',
    chip: 'rgba(125, 182, 255, 0.12)',
    title: 'text-sky-100',
    aura: 'from-sky-400/26 via-blue-300/12 to-transparent',
  },
  YELLOW: {
    glow: 'rgba(250, 204, 21, 0.22)',
    line: 'rgba(250, 204, 21, 0.32)',
    chip: 'rgba(250, 204, 21, 0.12)',
    title: 'text-yellow-100',
    aura: 'from-yellow-300/22 via-amber-200/10 to-transparent',
  },
  GREEN: {
    glow: 'rgba(74, 222, 128, 0.22)',
    line: 'rgba(110, 231, 183, 0.3)',
    chip: 'rgba(110, 231, 183, 0.12)',
    title: 'text-emerald-100',
    aura: 'from-emerald-400/24 via-green-300/10 to-transparent',
  },
  PURPLE: {
    glow: 'rgba(168, 85, 247, 0.24)',
    line: 'rgba(196, 181, 253, 0.32)',
    chip: 'rgba(196, 181, 253, 0.12)',
    title: 'text-violet-100',
    aura: 'from-violet-400/24 via-purple-300/10 to-transparent',
  },
  RED: {
    glow: 'rgba(248, 113, 113, 0.24)',
    line: 'rgba(252, 165, 165, 0.32)',
    chip: 'rgba(252, 165, 165, 0.12)',
    title: 'text-rose-100',
    aura: 'from-rose-400/24 via-red-300/10 to-transparent',
  },
};

const SAMPLE_CARD = {
  rhythmName: 'BLUE',
  authorityEngineName: 'Wave Engine',
  authorityLabel: 'Emotional Authority',
  decisionCue: 'Check again before deciding.',
  supportText:
    "Your decision style stays the same. Today's rhythm affects how quickly feelings settle. Trust what still feels true after the charge passes.",
  bestUseText: 'Check in more than once. What feels right at first may change later.',
  watchOutText: 'Treating one mood as the final answer.',
};

function getRevealStorageKey(profileId) {
  return `rhythmRevealSeen_${profileId}`;
}

// Builds a reveal path that feels like a calibration scan: broad coverage first,
// then a smaller orbit around the destination, always ending on the actual rhythm.
export function buildRevealSequence(finalRhythm) {
  const filtered = RHYTHMS.filter(rhythm => rhythm !== finalRhythm);
  const forwardSweep = [...RHYTHMS];
  const echoSweep = [filtered[1], filtered[4], filtered[0], filtered[2], finalRhythm].filter(Boolean);
  const finalApproach = [filtered[3], finalRhythm, filtered[5], finalRhythm].filter(Boolean);

  return [...forwardSweep, ...echoSweep, ...finalApproach];
}

function getRevealCadence(sequenceLength) {
  return Array.from({ length: sequenceLength }, (_, index) => {
    const progress = index / Math.max(sequenceLength - 1, 1);
    if (progress < 0.35) return 130;
    if (progress < 0.7) return 220;
    if (progress < 0.9) return 340;
    return 560;
  });
}

function SignalChip({ children, tint }) {
  return (
    <div
      className="inline-flex items-center rounded-full border px-3 py-1 text-[8px] font-semibold uppercase tracking-[0.18em] text-white/72 backdrop-blur-md"
      style={{ borderColor: tint, background: 'rgba(255,255,255,0.04)' }}
    >
      {children}
    </div>
  );
}

function GuidanceTile({ label, text, tone = 'best' }) {
  return (
    <div
      className={`rounded-2xl border p-3.5 ${
        tone === 'watch'
          ? 'bg-gradient-to-b from-rose-300/10 to-black/10'
          : 'bg-gradient-to-b from-sky-300/10 to-black/10'
      }`}
      style={{ borderColor: 'rgba(255,255,255,0.08)' }}
    >
      <div className="mb-2 text-[9px] font-semibold uppercase tracking-[0.18em] text-white/54">
        {label}
      </div>
      <p className="text-sm leading-6 text-white/88">{text}</p>
    </div>
  );
}

function RevealCard({
  rhythmName,
  authorityEngineName,
  authorityLabel,
  decisionCue,
  supportText,
  bestUseText,
  watchOutText,
  revealState,
}) {
  const style = RHYTHM_STYLES[rhythmName] || RHYTHM_STYLES.BLUE;
  const isRevealing = revealState === 'revealing';
  const isLanding = revealState === 'landing';

  return (
    <motion.section
      layout
      className="relative w-full max-w-[420px] overflow-hidden rounded-[30px] border bg-[#07111b] text-white shadow-[0_24px_80px_rgba(0,0,0,0.48),inset_0_1px_0_rgba(255,255,255,0.04)]"
      style={{ borderColor: style.line }}
      animate={{
        boxShadow: isLanding
          ? `0 0 0 1px ${style.line}, 0 26px 88px rgba(0,0,0,0.52), 0 0 52px ${style.glow}`
          : `0 24px 80px rgba(0,0,0,0.48), 0 0 30px ${style.glow}`,
      }}
      transition={{ duration: isLanding ? 0.6 : 0.25, ease: 'easeOut' }}
    >
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <motion.div
          className={`absolute inset-0 bg-gradient-to-b ${style.aura}`}
          animate={{ opacity: isRevealing ? [0.55, 0.8, 0.6] : isLanding ? [0.75, 1, 0.82] : 0.62 }}
          transition={{ duration: isRevealing ? 0.55 : 0.9, repeat: isRevealing ? Infinity : 0 }}
        />
        <motion.div
          className="absolute inset-x-[14%] top-[19%] h-[38%] rounded-[34px] border border-white/8"
          animate={{
            scale: isLanding ? [1, 1.035, 1] : 1,
            opacity: isRevealing ? [0.24, 0.38, 0.26] : [0.28, 0.32, 0.28],
          }}
          transition={{ duration: isRevealing ? 0.7 : 1.2, repeat: isRevealing ? Infinity : 0 }}
        />
        <div className="absolute inset-x-0 bottom-0 h-28 bg-gradient-to-t from-[#071019] via-[#071019]/68 to-transparent" />
      </div>

      <div className="relative z-[1] px-5 pb-5 pt-4 sm:px-6 sm:pb-6">
        <div className="mb-4 flex items-start justify-between gap-4">
          <div className="min-w-0">
            <div className="text-[10px] uppercase tracking-[0.22em] text-white/56">
              Tuesday, April 21
            </div>
            <div className="mt-1 inline-flex items-center gap-2 text-[10px] uppercase tracking-[0.18em] text-white/44">
              <span className="text-white/36">◎</span>
              <span className="truncate">Vancouver</span>
            </div>
          </div>

          <SignalChip tint={style.line}>
            {isRevealing ? 'CALIBRATING SIGNAL' : isLanding ? 'SIGNAL REVEALED' : 'SIGNAL LOCKED'}
          </SignalChip>
        </div>

        <div className="mb-4 flex rounded-[18px] border border-white/10 bg-black/20 p-1 shadow-[inset_0_1px_0_rgba(255,255,255,0.04)] backdrop-blur-md">
          <button
            type="button"
            className="flex-1 rounded-[14px] border border-white/12 bg-white/10 px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-white"
          >
            Color Rhythm
          </button>
          <button
            type="button"
            className="flex-1 rounded-[14px] px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-white/46"
          >
            Monthly Calendar
          </button>
        </div>

        <div
          className="overflow-hidden rounded-[28px] border px-4 pb-4 pt-5 shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]"
          style={{
            borderColor: style.line,
            background: 'linear-gradient(180deg, rgba(7,19,31,0.84) 0%, rgba(6,12,19,0.92) 100%)',
          }}
        >
          <div className="text-[9px] font-semibold uppercase tracking-[0.2em] text-white/46">
            ACTIVE RHYTHM
          </div>

          <motion.h2
            key={rhythmName}
            className={`mt-3 text-[54px] font-semibold uppercase leading-none tracking-[-0.04em] ${style.title}`}
            initial={{ opacity: 0.35, y: 10, scale: 0.985 }}
            animate={{
              opacity: 1,
              y: 0,
              scale: isLanding ? [1, 1.04, 1] : 1,
              textShadow: isLanding
                ? [`0 0 22px ${style.glow}`, `0 0 40px ${style.glow}`, `0 0 26px ${style.glow}`]
                : `0 0 24px ${style.glow}`,
            }}
            transition={{
              duration: isLanding ? 0.7 : 0.22,
              ease: 'easeOut',
            }}
          >
            {rhythmName}
          </motion.h2>

          <div
            className="mt-5 rounded-[20px] border border-white/9 bg-[linear-gradient(180deg,rgba(255,255,255,0.032)_0%,rgba(255,255,255,0.014)_100%)] px-4 py-3.5 shadow-[inset_0_1px_0_rgba(255,255,255,0.035)] backdrop-blur-md"
          >
            <div className="text-[9px] font-semibold uppercase tracking-[0.18em] text-white/44">
              YOUR DECISION ENGINE
            </div>
            <div className="mt-2 text-[24px] font-medium leading-tight text-white/94">
              {authorityEngineName}
            </div>
            <div className="mt-1 text-[12px] leading-5 text-white/62">
              {authorityLabel} · Always active
            </div>
          </div>

          <div
            className="mt-6 rounded-[22px] border border-white/10 bg-[linear-gradient(180deg,rgba(10,18,28,0.82)_0%,rgba(6,11,18,0.9)_100%)] p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.04),0_14px_34px_rgba(0,0,0,0.18)] backdrop-blur-xl"
          >
            <div className="text-[9px] font-semibold uppercase tracking-[0.18em] text-white/48">
              TODAY&apos;S DECISION GUIDANCE
            </div>

            <motion.p
              key={`${rhythmName}-cue`}
              className="mt-3 max-w-[18rem] text-[18px] font-medium italic leading-7 text-white/95"
              initial={{ opacity: 0.3, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.28, ease: 'easeOut' }}
            >
              “{decisionCue}”
            </motion.p>

            <p className="mt-3 max-w-[19rem] text-[13px] leading-6 text-white/82">
              {supportText}
            </p>

            <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
              <GuidanceTile label="Best Use" text={bestUseText} />
              <GuidanceTile label="Watch Out" text={watchOutText} tone="watch" />
            </div>
          </div>

          <button
            type="button"
            className="mt-5 flex w-full items-center justify-between rounded-[16px] border border-white/12 bg-black/18 px-4 py-3 text-left shadow-[inset_0_1px_0_rgba(255,255,255,0.03)]"
          >
            <span className="text-[10px] font-semibold uppercase tracking-[0.16em] text-white/76">
              TODAY&apos;S FREQUENCIES
            </span>
            <span className="text-white/68">▾</span>
          </button>

          <div className="mt-4 flex items-center gap-3 rounded-[18px] border border-white/10 bg-black/14 px-4 py-3.5 text-white/50">
            <div className="text-sm text-white/42">✦</div>
            <div className="min-w-0 flex-1 text-[10px] font-semibold uppercase tracking-[0.18em]">
              ASK ABOUT YOUR DAY
            </div>
            <div className="rounded-md border border-white/10 px-2 py-1 text-[8px] font-semibold uppercase tracking-[0.14em] text-white/42">
              Coming Soon
            </div>
          </div>
        </div>
      </div>
    </motion.section>
  );
}

export default function ColorRhythmRevealDemo({
  finalRhythm = 'BLUE',
  shouldAnimateReveal = true,
  onRevealComplete,
  profileId = 'demo-profile-blue',
}) {
  const [currentRhythm, setCurrentRhythm] = useState(finalRhythm);
  const [revealState, setRevealState] = useState('settled');
  const timeoutRef = useRef(null);
  const mountedRef = useRef(false);

  const storageKey = useMemo(() => getRevealStorageKey(profileId), [profileId]);
  const sequence = useMemo(() => buildRevealSequence(finalRhythm), [finalRhythm]);
  const cadence = useMemo(() => getRevealCadence(sequence.length), [sequence.length]);

  useEffect(() => {
    mountedRef.current = true;

    const revealSeen =
      typeof window !== 'undefined' && profileId
        ? window.localStorage.getItem(storageKey)
        : null;

    if (!shouldAnimateReveal || revealSeen) {
      setCurrentRhythm(finalRhythm);
      setRevealState('settled');
      return () => {
        mountedRef.current = false;
      };
    }

    let stepIndex = 0;
    setRevealState('revealing');
    setCurrentRhythm(sequence[0]);

    const runStep = () => {
      if (!mountedRef.current) return;

      setCurrentRhythm(sequence[stepIndex]);

      if (stepIndex === sequence.length - 1) {
        setRevealState('landing');
        timeoutRef.current = window.setTimeout(() => {
          if (!mountedRef.current) return;
          setRevealState('settled');
          if (profileId) {
            window.localStorage.setItem(storageKey, 'true');
          }
          onRevealComplete?.();
        }, 820);
        return;
      }

      const delay = cadence[stepIndex];
      stepIndex += 1;
      timeoutRef.current = window.setTimeout(runStep, delay);
    };

    timeoutRef.current = window.setTimeout(runStep, 120);

    return () => {
      mountedRef.current = false;
      if (timeoutRef.current) window.clearTimeout(timeoutRef.current);
    };
  }, [cadence, finalRhythm, onRevealComplete, profileId, sequence, shouldAnimateReveal, storageKey]);

  function resetReveal() {
    if (typeof window !== 'undefined' && profileId) {
      window.localStorage.removeItem(storageKey);
      window.location.reload();
    }
  }

  return (
    <main className="min-h-screen bg-[#040814] px-4 py-8 text-white">
      <div className="mx-auto flex max-w-[440px] flex-col gap-4">
        <div className="rounded-[24px] border border-white/10 bg-white/[0.03] p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.04)] backdrop-blur-md">
          <div className="text-[10px] uppercase tracking-[0.18em] text-white/48">
            Rhythm Reveal Demo
          </div>
          <p className="mt-2 text-sm leading-6 text-white/76">
            This demo reveals the rhythm once per profile, then persists the settled state using localStorage.
          </p>
          <div className="mt-4 flex items-center gap-3">
            <button
              type="button"
              onClick={resetReveal}
              className="rounded-full border border-white/12 bg-white/[0.05] px-4 py-2 text-[10px] font-semibold uppercase tracking-[0.18em] text-white/84 transition hover:bg-white/[0.08]"
            >
              Reset Reveal
            </button>
            <span className="text-[10px] uppercase tracking-[0.18em] text-white/42">
              profile: {profileId}
            </span>
          </div>
        </div>

        <AnimatePresence mode="wait">
          <RevealCard
            key={currentRhythm}
            rhythmName={currentRhythm}
            authorityEngineName={SAMPLE_CARD.authorityEngineName}
            authorityLabel={SAMPLE_CARD.authorityLabel}
            decisionCue={SAMPLE_CARD.decisionCue}
            supportText={SAMPLE_CARD.supportText}
            bestUseText={SAMPLE_CARD.bestUseText}
            watchOutText={SAMPLE_CARD.watchOutText}
            revealState={revealState}
          />
        </AnimatePresence>
      </div>
    </main>
  );
}
