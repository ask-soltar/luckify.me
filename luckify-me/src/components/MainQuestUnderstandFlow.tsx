import { useState, useEffect } from 'react';
import type { MainQuestUnderstandFlow } from '../content/mainQuestUnderstandSeed';

type Screen =
  | 'intro'
  | 'patternExpansion'
  | 'realLifeExamples'
  | 'responseReflection'
  | 'progressionTree';

type RecognitionResponse = 'i_do_this' | 'sometimes' | 'not_really_me' | null;

type PersistedState = {
  screen: Screen;
  response: RecognitionResponse;
  progressionTreePrev: Screen;
  activeIdx: number;
  visited: number[];
};

function loadState(key: string): PersistedState | null {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function MainQuestUnderstandFlow({ flow, profileId }: { flow: MainQuestUnderstandFlow; profileId?: string }) {
  const storageKey = `mq-flow-${profileId ?? 'default'}-${flow.gate}-${flow.line}`;
  const saved = loadState(storageKey);

  const [screen, setScreen] = useState<Screen>(saved?.screen ?? 'intro');
  const [response, setResponse] = useState<RecognitionResponse>(saved?.response ?? null);
  const [progressionTreePrev, setProgressionTreePrev] = useState<Screen>(saved?.progressionTreePrev ?? 'responseReflection');
  const [activeIdx, setActiveIdx] = useState(saved?.activeIdx ?? 0);
  const [visited, setVisited] = useState<Set<number>>(new Set(saved?.visited ?? [0]));

  useEffect(() => {
    const state: PersistedState = {
      screen,
      response,
      progressionTreePrev,
      activeIdx,
      visited: [...visited],
    };
    localStorage.setItem(storageKey, JSON.stringify(state));
  }, [screen, response, progressionTreePrev, activeIdx, visited, storageKey]);

  function handleRecognitionButton(id: 'i_do_this' | 'sometimes' | 'not_really_me') {
    setResponse(id);
    setScreen('responseReflection');
  }

  function goToProgressionTree(from: Screen) {
    setProgressionTreePrev(from);
    setActiveIdx(0);
    setVisited(new Set([0]));
    setScreen('progressionTree');
  }

  function goTo(idx: number) {
    setActiveIdx(idx);
    setVisited((prev) => new Set([...prev, idx]));
  }

  const backToIntro = () => setScreen('intro');

  return (
    <div className="mq-understand">
      {screen === 'intro' && (
        <IntroScreen flow={flow} onUnderstand={() => setScreen('patternExpansion')} />
      )}

      {screen === 'patternExpansion' && (
        <PatternExpansionScreen
          data={flow.understandFlow.patternExpansion}
          onCta={() => goToProgressionTree('patternExpansion')}
          onExplore={() => setScreen('realLifeExamples')}
          onBack={backToIntro}
          onBackToIntro={backToIntro}
        />
      )}

      {screen === 'realLifeExamples' && (
        <RealLifeExamplesScreen
          data={flow.understandFlow.realLifeExamples}
          onRecognition={handleRecognitionButton}
          onBack={() => setScreen('patternExpansion')}
          onBackToIntro={backToIntro}
        />
      )}

      {screen === 'responseReflection' && response && (
        <ResponseReflectionScreen
          data={flow.understandFlow.responseReflection[response]}
          onCta={() => goToProgressionTree('responseReflection')}
          onBack={() => setScreen('realLifeExamples')}
          onBackToIntro={backToIntro}
        />
      )}

      {screen === 'progressionTree' && (
        <ProgressionTreeScreen
          data={flow.understandFlow.recognitionProgressionTree}
          activeIdx={activeIdx}
          visited={visited}
          onGoTo={goTo}
          onBack={() => setScreen(progressionTreePrev)}
          onBackToIntro={backToIntro}
          backLabel={progressionTreePrev === 'patternExpansion' ? 'Field Briefing' : 'Reflection'}
        />
      )}
    </div>
  );
}

/* ── Shared nav ─────────────────────────────────────────────────────────── */

function BackNav({
  onBack,
  onBackToIntro,
  backLabel = 'Back',
}: {
  onBack: () => void;
  onBackToIntro: () => void;
  backLabel?: string;
}) {
  return (
    <div className="mq-understand__back-nav">
      <button type="button" className="mq-understand__back-btn" onClick={onBack}>
        ← {backLabel}
      </button>
      <button
        type="button"
        className="mq-understand__back-btn mq-understand__back-btn--ghost"
        onClick={onBackToIntro}
      >
        Main Quest
      </button>
    </div>
  );
}

/* ── Intro / Quest Brief ────────────────────────────────────────────────── */

function IntroScreen({
  flow,
  onUnderstand,
}: {
  flow: MainQuestUnderstandFlow;
  onUnderstand: () => void;
}) {
  const { intro } = flow;
  return (
    <div className="mq-understand__screen mq-understand__screen--intro">
      <div className="mq-intro__header">
        <div className="mq-intro__eyebrow">Main Quest</div>
        <div className="mq-intro__meta">{flow.gateLine} · Purpose</div>
      </div>

      <div className="mq-intro__title-wrap">
        <h2 className="mq-intro__title">{intro.questName}</h2>
      </div>

      <div className="mq-intro__blocks">
        <div className="mq-intro__block">
          <div className="mq-intro__block-label">Natural Gift</div>
          <p className="mq-intro__block-body">{intro.openingStatement}</p>
        </div>

        <div className="mq-intro__block">
          <div className="mq-intro__block-label">Field Signs</div>
          <ul className="mq-intro__block-list">
            {intro.evidence.map((line, i) => (
              <li key={i}>{line}</li>
            ))}
          </ul>
        </div>

        <div className="mq-intro__block mq-intro__block--shadow">
          <div className="mq-intro__block-label">Shadow Pattern</div>
          <p className="mq-intro__block-body">{intro.limitation}</p>
        </div>

        <div className="mq-intro__block mq-intro__block--objective">
          <div className="mq-intro__block-label">Quest Objective</div>
          <p className="mq-intro__block-body">{intro.purpose}</p>
        </div>
      </div>

      <div className="mq-intro__actions">
        <button type="button" className="mq-btn mq-btn--primary" onClick={onUnderstand}>
          Enter Field Briefing
          <span className="mq-btn__arrow" aria-hidden="true">→</span>
        </button>
      </div>
    </div>
  );
}

/* ── Field Briefing ─────────────────────────────────────────────────────── */

function PatternExpansionScreen({
  data,
  onCta,
  onExplore,
  onBack,
  onBackToIntro,
}: {
  data: MainQuestUnderstandFlow['understandFlow']['patternExpansion'];
  onCta: () => void;
  onExplore: () => void;
  onBack: () => void;
  onBackToIntro: () => void;
}) {
  return (
    <div className="mq-understand__screen mq-understand__screen--pattern">
      <BackNav onBack={onBack} onBackToIntro={onBackToIntro} backLabel="Quest Brief" />

      <div className="mq-screen__header">
        <div className="mq-screen__eyebrow">Field Briefing</div>
        <h3 className="mq-screen__title">{data.title}</h3>
      </div>

      <div className="mq-section">
        <div className="mq-section__label">The Pattern</div>
        <div className="mq-body-lines">
          {data.body.map((line, i) => (
            <p key={i}>{line}</p>
          ))}
        </div>
      </div>

      {data.recognitionLines.length > 0 && (
        <div className="mq-recognition-card">
          <div className="mq-recognition-card__label">Recognition Moment</div>
          {data.recognitionLines.map((line, i) => (
            <p key={i} className="mq-recognition-card__line">{line}</p>
          ))}
        </div>
      )}

      <button type="button" className="mq-btn mq-btn--primary" onClick={onExplore}>
        {data.exploreCtaLabel}
        <span className="mq-btn__arrow" aria-hidden="true">→</span>
      </button>
      <button type="button" className="mq-btn mq-btn--ghost" onClick={onCta}>
        {data.skipCtaLabel}
      </button>
    </div>
  );
}

/* ── Real-Life Examples ──────────────────────────────────────────────────── */

function RealLifeExamplesScreen({
  data,
  onRecognition,
  onBack,
  onBackToIntro,
}: {
  data: MainQuestUnderstandFlow['understandFlow']['realLifeExamples'];
  onRecognition: (id: 'i_do_this' | 'sometimes' | 'not_really_me') => void;
  onBack: () => void;
  onBackToIntro: () => void;
}) {
  return (
    <div className="mq-understand__screen mq-understand__screen--examples">
      <BackNav onBack={onBack} onBackToIntro={onBackToIntro} backLabel="Field Briefing" />

      <div className="mq-screen__header">
        <div className="mq-screen__eyebrow">Recognition</div>
        <h3 className="mq-screen__title">{data.title}</h3>
      </div>

      <ul className="mq-examples">
        {data.examples.map((ex, i) => (
          <li key={i}>{ex}</li>
        ))}
      </ul>

      <div className="mq-recognition-card mq-recognition-card--closing">
        <div className="mq-recognition-card__label">Recognition Moment</div>
        {data.closingLines.map((line, i) => (
          <p key={i} className="mq-recognition-card__line">{line}</p>
        ))}
      </div>

      <div className="mq-section">
        <div className="mq-section__label">How does this land?</div>
        <div className="mq-recognition-buttons">
          {data.buttons.map((btn) => (
            <button
              key={btn.id}
              type="button"
              className="mq-btn mq-btn--recognition"
              onClick={() => onRecognition(btn.id)}
            >
              {btn.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ── Response Reflection ─────────────────────────────────────────────────── */

function ResponseReflectionScreen({
  data,
  onCta,
  onBack,
  onBackToIntro,
}: {
  data: { title: string; body: string[]; ctaLabel: string };
  onCta: () => void;
  onBack: () => void;
  onBackToIntro: () => void;
}) {
  return (
    <div className="mq-understand__screen mq-understand__screen--reflection">
      <BackNav onBack={onBack} onBackToIntro={onBackToIntro} backLabel="Recognition" />

      <div className="mq-screen__header">
        <div className="mq-screen__eyebrow">Reflection</div>
        <h3 className="mq-screen__title">{data.title}</h3>
      </div>

      <div className="mq-body-lines mq-body-lines--spacious">
        {data.body.map((line, i) => (
          <p key={i}>{line}</p>
        ))}
      </div>

      <button type="button" className="mq-btn mq-btn--primary" onClick={onCta}>
        {data.ctaLabel}
        <span className="mq-btn__arrow" aria-hidden="true">→</span>
      </button>
    </div>
  );
}

/* ── Growth Path — interactive stepper ──────────────────────────────────── */

function stripThe(name: string) { return name.replace(/^The\s+/, ''); }

function ProgressionTreeScreen({
  data,
  activeIdx,
  visited,
  onGoTo,
  onBack,
  onBackToIntro,
  backLabel = 'Back',
}: {
  data: MainQuestUnderstandFlow['understandFlow']['recognitionProgressionTree'];
  activeIdx: number;
  visited: Set<number>;
  onGoTo: (idx: number) => void;
  onBack: () => void;
  onBackToIntro: () => void;
  backLabel?: string;
}) {
  const levels = data.levels;
  const active = levels[activeIdx];
  const isFirst = activeIdx === 0;
  const isLast = activeIdx === levels.length - 1;

  return (
    <div className="mq-understand__screen mq-understand__screen--tree">
      <BackNav onBack={onBack} onBackToIntro={onBackToIntro} backLabel={backLabel} />

      <div className="mq-screen__header mq-screen__header--compact">
        <div className="mq-screen__eyebrow">Growth Path</div>
        <h3 className="mq-screen__title">{data.title}</h3>
        <p className="mq-screen__subtitle">{data.introLine}</p>
      </div>

      {/* ── Stepper rail ── */}
      <div className="gp-stepper" role="tablist" aria-label="Growth path stages">
        {levels.map((lvl, idx) => {
          const isActive = idx === activeIdx;
          const isFinal = idx === levels.length - 1;
          return (
            <button
              key={lvl.level}
              type="button"
              role="tab"
              aria-current={isActive ? 'step' : undefined}
              className={[
                'gp-step',
                isActive ? 'gp-step--active' : '',
                visited.has(idx) ? 'gp-step--visited' : '',
                isFinal ? 'gp-step--final' : '',
              ].filter(Boolean).join(' ')}
              onClick={() => onGoTo(idx)}
            >
              <span className="gp-step__num">{lvl.level}</span>
              <span className="gp-step__label">{stripThe(lvl.universalName)}</span>
            </button>
          );
        })}
      </div>

      {/* ── Spotlight card ── */}
      <div
        key={activeIdx}
        className={['gp-spotlight', isLast ? 'gp-spotlight--final' : ''].filter(Boolean).join(' ')}
      >
        <div className="gp-spotlight__head">
          <span className="gp-spotlight__step">{active.level}</span>
          <span className="gp-spotlight__sep" aria-hidden="true">·</span>
          <span className="gp-spotlight__universal">{active.universalName}</span>
        </div>

        <h4 className="gp-spotlight__quest">{active.questName}</h4>

        <div className="gp-spotlight__preview">
          {active.body.map((line, i) => <p key={i}>{line}</p>)}
        </div>

        <div className="gp-nav">
          <button
            type="button"
            className="mq-btn mq-btn--secondary gp-nav__btn"
            onClick={() => onGoTo(activeIdx - 1)}
            disabled={isFirst}
          >
            ← Previous
          </button>
          <button
            type="button"
            className="mq-btn mq-btn--primary gp-nav__btn"
            onClick={() => onGoTo(activeIdx + 1)}
            disabled={isLast}
          >
            Next →
          </button>
        </div>
      </div>

      {/* ── Final completion card — appears at stage 5 ── */}
      {isLast && (
        <div className="gp-completion">
          <div className="gp-completion__badge">{data.finalCompletion.badge}</div>
          <h4 className="gp-completion__title">{data.finalCompletion.title}</h4>
          <div className="gp-completion__body-lines">
            {data.finalCompletion.body.map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>
          <div className="mq-btn-stack">
            <button
              type="button"
              className="mq-btn mq-btn--primary"
              disabled={!data.finalCompletion.cta.enabled}
            >
              {data.finalCompletion.cta.label}
              {data.finalCompletion.cta.enabled && (
                <span className="mq-btn__arrow" aria-hidden="true">→</span>
              )}
            </button>
            <button type="button" className="mq-btn mq-btn--tertiary" onClick={onBackToIntro}>
              {data.finalCompletion.secondaryAction.label}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
