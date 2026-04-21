const SAMPLE_PROPS = {
  dateLabel: 'Tuesday, April 21',
  locationLabel: 'Vancouver',
  rhythmName: 'BLUE',
  authorityEngineName: 'Wave Engine',
  authorityLabel: 'Emotional Authority',
  decisionCue: 'Check again before deciding.',
  supportText:
    "Your decision style stays the same. Today's rhythm affects how quickly feelings settle. Trust what still feels true after the charge passes.",
  bestUseText:
    'Check in more than once. What feels right at first may change later.',
  watchOutText: 'Treating one mood as the final answer.',
  dropdownLabel: "TODAY'S FREQUENCIES",
  ctaLabel: 'ASK ABOUT YOUR DAY',
  utilityLabel: 'ACTIVE RHYTHM',
};

function UtilityPill({ children, active = false }) {
  return (
    <button
      type="button"
      className={[
        'inline-flex items-center justify-center rounded-full border px-4 py-2 text-[10px] font-semibold uppercase tracking-[0.18em] transition-all duration-200',
        active
          ? 'border-white/18 bg-white/12 text-white shadow-[inset_0_1px_0_rgba(255,255,255,0.08),0_6px_18px_rgba(0,0,0,0.22)]'
          : 'border-white/10 bg-black/20 text-white/52 hover:border-white/16 hover:bg-white/[0.06] hover:text-white/80',
      ].join(' ')}
    >
      {children}
    </button>
  );
}

function GuidanceTile({ label, text, tone = 'best' }) {
  const toneClass =
    tone === 'watch'
      ? 'border-white/10 bg-gradient-to-b from-rose-300/10 to-black/10'
      : 'border-white/10 bg-gradient-to-b from-sky-300/10 to-black/10';

  return (
    <div className={`rounded-2xl border p-3.5 ${toneClass}`}>
      <div className="mb-2 text-[9px] font-semibold uppercase tracking-[0.18em] text-white/55">
        {label}
      </div>
      <p className="text-sm leading-6 text-white/88">{text}</p>
    </div>
  );
}

function FallbackArtwork() {
  return (
    <div className="absolute inset-0 overflow-hidden">
      <div className="absolute left-1/2 top-[16%] h-48 w-48 -translate-x-1/2 rounded-full bg-sky-400/14 blur-3xl" />
      <div className="absolute left-[14%] top-[40%] h-20 w-20 rounded-full bg-cyan-300/10 blur-2xl" />
      <div className="absolute right-[10%] top-[26%] h-24 w-24 rounded-full bg-indigo-300/10 blur-2xl" />
      <div className="absolute inset-x-[18%] top-[18%] h-[42%] rounded-[40px] border border-white/8 bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.08)_0%,transparent_58%)]" />
      <div className="absolute inset-x-[25%] top-[22%] h-[34%] rounded-[32px] border border-white/7" />
      <div className="absolute left-1/2 top-[39%] h-28 w-28 -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/10" />
      <div className="absolute left-1/2 top-[39%] h-16 w-16 -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/10" />
      <div className="absolute left-1/2 top-[39%] h-[2px] w-40 -translate-x-1/2 bg-gradient-to-r from-transparent via-white/16 to-transparent" />
      <div className="absolute left-1/2 top-[39%] h-40 w-[2px] -translate-x-1/2 -translate-y-1/2 bg-gradient-to-b from-transparent via-white/16 to-transparent" />
    </div>
  );
}

function ChevronDown() {
  return (
    <svg
      viewBox="0 0 20 20"
      fill="none"
      aria-hidden="true"
      className="h-4 w-4 opacity-70"
    >
      <path
        d="M5 7.5L10 12.5L15 7.5"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export default function ColorRhythmDecisionCard(props) {
  const {
    dateLabel,
    locationLabel,
    rhythmName,
    authorityEngineName,
    authorityLabel,
    decisionCue,
    supportText,
    bestUseText,
    watchOutText,
    imageUrl,
    dropdownLabel,
    ctaLabel,
    utilityLabel,
  } = {
    ...SAMPLE_PROPS,
    ...props,
  };

  return (
    <section className="w-full max-w-[420px] overflow-hidden rounded-[30px] border border-emerald-200/10 bg-[#07111b] text-white shadow-[0_24px_80px_rgba(0,0,0,0.48),inset_0_1px_0_rgba(255,255,255,0.04)]">
      <div className="relative isolate overflow-hidden px-5 pb-5 pt-4 sm:px-6 sm:pb-6">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(80,145,255,0.22)_0%,rgba(10,23,38,0.9)_48%,rgba(4,9,15,0.98)_100%)]" />
        <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.03)_0%,rgba(255,255,255,0)_26%,rgba(0,0,0,0.18)_100%)]" />

        <div className="relative z-[1] mb-4 flex items-start justify-between gap-4">
          <div className="min-w-0">
            <div className="text-[10px] uppercase tracking-[0.22em] text-white/56">
              {dateLabel}
            </div>
            <div className="mt-1 inline-flex items-center gap-2 text-[10px] uppercase tracking-[0.18em] text-white/44">
              <span className="text-white/36">◎</span>
              <span className="truncate">{locationLabel}</span>
            </div>
          </div>

          <div className="flex rounded-full border border-white/12 bg-black/20 p-1 shadow-[inset_0_1px_0_rgba(255,255,255,0.05)] backdrop-blur-md">
            <UtilityPill active>Character View</UtilityPill>
            <UtilityPill>Command Mode</UtilityPill>
          </div>
        </div>

        <div className="relative z-[1] mb-4 flex rounded-[18px] border border-white/10 bg-black/20 p-1 shadow-[inset_0_1px_0_rgba(255,255,255,0.04)] backdrop-blur-md">
          <button
            type="button"
            className="flex-1 rounded-[14px] border border-sky-200/12 bg-sky-400/10 px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-white shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]"
          >
            Color Rhythm
          </button>
          <button
            type="button"
            className="flex-1 rounded-[14px] px-4 py-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-white/46 transition-colors duration-200 hover:text-white/72"
          >
            Monthly Calendar
          </button>
        </div>

        <div className="relative z-[1] overflow-hidden rounded-[28px] border border-white/10 bg-[linear-gradient(180deg,rgba(7,19,31,0.84)_0%,rgba(6,12,19,0.92)_100%)] px-4 pb-4 pt-5 shadow-[inset_0_1px_0_rgba(255,255,255,0.04),0_18px_40px_rgba(0,0,0,0.24)] sm:px-5">
          <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.02)_0%,rgba(255,255,255,0)_28%,rgba(255,255,255,0.015)_100%)]" />

          <div className="relative z-[1]">
            <div className="text-[9px] font-semibold uppercase tracking-[0.2em] text-white/46">
              {utilityLabel || 'ACTIVE RHYTHM'}
            </div>

            <div className="mt-3">
              <h2 className="text-[52px] font-semibold uppercase leading-none tracking-[-0.04em] text-white [text-shadow:0_0_28px_rgba(168,212,255,0.34)]">
                {rhythmName}
              </h2>
            </div>

            <div className="mt-5 rounded-[20px] border border-white/9 bg-[linear-gradient(180deg,rgba(255,255,255,0.032)_0%,rgba(255,255,255,0.014)_100%)] px-4 py-3.5 shadow-[inset_0_1px_0_rgba(255,255,255,0.035)] backdrop-blur-md">
              <div className="text-[9px] font-semibold uppercase tracking-[0.18em] text-white/44">
                Your Decision Engine
              </div>

              <div className="mt-2 text-[24px] font-medium leading-tight text-white/94">
                {authorityEngineName}
              </div>
              <div className="mt-1 text-[12px] leading-5 text-white/62">
                {authorityLabel} · Always active
              </div>
            </div>
          </div>

          <div className="relative mt-5 h-[220px] overflow-hidden rounded-[22px] border border-white/6 bg-black/10">
            {imageUrl ? (
              <>
                <img
                  src={imageUrl}
                  alt=""
                  className="absolute inset-0 h-full w-full object-cover opacity-52"
                />
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_35%,rgba(120,180,255,0.2)_0%,transparent_35%),linear-gradient(180deg,rgba(3,8,14,0.12)_0%,rgba(3,8,14,0.64)_100%)]" />
              </>
            ) : (
              <FallbackArtwork />
            )}
            <div className="pointer-events-none absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-[#071019] via-[#071019]/70 to-transparent" />
          </div>

          <div className="relative z-[1] mt-6 rounded-[22px] border border-white/10 bg-[linear-gradient(180deg,rgba(10,18,28,0.82)_0%,rgba(6,11,18,0.9)_100%)] p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.04),0_14px_34px_rgba(0,0,0,0.18)] backdrop-blur-xl">
            <div className="text-[9px] font-semibold uppercase tracking-[0.18em] text-white/48">
              Today&apos;s Decision Guidance
            </div>

            <p className="mt-3 max-w-[18rem] text-[18px] font-medium italic leading-7 text-white/95 [text-shadow:0_0_18px_rgba(154,198,255,0.08)]">
              “{decisionCue}”
            </p>

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
            className="relative z-[1] mt-5 flex w-full items-center justify-between rounded-[16px] border border-white/12 bg-black/18 px-4 py-3 text-left shadow-[inset_0_1px_0_rgba(255,255,255,0.03)] transition-all duration-200 hover:border-white/16 hover:bg-white/[0.04]"
          >
            <span className="text-[10px] font-semibold uppercase tracking-[0.16em] text-white/76">
              {dropdownLabel || "TODAY'S FREQUENCIES"}
            </span>
            <ChevronDown />
          </button>

          <div className="relative z-[1] mt-4 flex items-center gap-3 rounded-[18px] border border-white/10 bg-black/14 px-4 py-3.5 text-white/50">
            <div className="text-sm text-white/42">✦</div>
            <div className="min-w-0 flex-1 text-[10px] font-semibold uppercase tracking-[0.18em]">
              {ctaLabel || 'ASK ABOUT YOUR DAY'}
            </div>
            <div className="rounded-md border border-white/10 px-2 py-1 text-[8px] font-semibold uppercase tracking-[0.14em] text-white/42">
              Coming Soon
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

ColorRhythmDecisionCard.previewProps = SAMPLE_PROPS;
