import { useEffect } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import './PassiveSkillDetailScreen.css';

export const passiveSkillDetailTokens = {
  colors: {
    bgTop: '#040806',
    bgBottom: '#09110c',
    surface: 'rgba(16, 24, 18, 0.78)',
    surfaceStrong: 'rgba(18, 28, 21, 0.9)',
    border: 'rgba(118, 146, 112, 0.22)',
    borderStrong: 'rgba(150, 183, 126, 0.28)',
    olive: '#94936d',
    title: 'rgba(248, 244, 234, 0.96)',
    text: 'rgba(227, 232, 223, 0.88)',
    textDim: 'rgba(202, 208, 199, 0.7)',
    glow: 'rgba(102, 168, 112, 0.12)',
    glowGold: 'rgba(176, 162, 104, 0.1)',
  },
  spacing: {
    xs: 8,
    sm: 12,
    md: 16,
    lg: 20,
    xl: 24,
    xxl: 32,
  },
  radius: {
    sm: 18,
    md: 22,
    lg: 26,
  },
  typography: {
    display: '"Cormorant Garamond", "Iowan Old Style", "Times New Roman", serif',
    body: 'var(--pip-font-body, "Inter", "Segoe UI", sans-serif)',
    mono: 'var(--pip-font-mono, "SFMono-Regular", monospace)',
  },
};

function PassiveSkillIcon({ id }) {
  const common = {
    fill: 'none',
    stroke: 'currentColor',
    strokeLinecap: 'round',
    strokeLinejoin: 'round',
    strokeWidth: 1.6,
  };

  if (id === 'emotional-authority') {
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path {...common} d="M3 12c2.1-2.4 4.2-3.6 6.3-3.6 2.7 0 3.4 2.8 5.6 2.8 1.8 0 3.5-.9 5.1-2.7" />
        <path {...common} d="M3 17c2.1-2.4 4.2-3.6 6.3-3.6 2.7 0 3.4 2.8 5.6 2.8 1.8 0 3.5-.9 5.1-2.7" />
        <circle cx="8" cy="7" r="1.4" fill="currentColor" stroke="none" />
        <circle cx="16.8" cy="7.6" r="1.1" fill="currentColor" stroke="none" />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle {...common} cx="12" cy="12" r="7" />
      <path {...common} d="M12 6v12M6 12h12" />
    </svg>
  );
}

function BulletIcon({ kind = 'flow' }) {
  const common = {
    fill: 'none',
    stroke: 'currentColor',
    strokeLinecap: 'round',
    strokeLinejoin: 'round',
    strokeWidth: 1.6,
  };

  switch (kind) {
    case 'time':
      return (
        <svg viewBox="0 0 16 16" aria-hidden="true">
          <circle {...common} cx="8" cy="8" r="5.5" />
          <path {...common} d="M8 4.7v3.5l2.2 1.5" />
        </svg>
      );
    case 'check':
      return (
        <svg viewBox="0 0 16 16" aria-hidden="true">
          <path {...common} d="M3 8.4 6.2 11.2 13 4.8" />
        </svg>
      );
    case 'warning':
      return (
        <svg viewBox="0 0 16 16" aria-hidden="true">
          <path {...common} d="M8 2.8 13.5 12H2.5Z" />
          <path {...common} d="M8 6.2v2.8" />
          <circle cx="8" cy="11.1" r=".7" fill="currentColor" stroke="none" />
        </svg>
      );
    default:
      return (
        <svg viewBox="0 0 16 16" aria-hidden="true">
          <path {...common} d="M1.8 8c1.3-1.6 2.8-2.4 4.5-2.4 1.8 0 2.4 1.7 4 1.7 1.4 0 2.7-.7 3.9-2" />
          <path {...common} d="M1.8 11.2c1.3-1.6 2.8-2.4 4.5-2.4 1.8 0 2.4 1.7 4 1.7 1.4 0 2.7-.7 3.9-2" />
        </svg>
      );
  }
}

export function PassiveSkillHero({ loadout }) {
  return (
    <section className="passive-skill-hero">
      <div className="passive-skill-hero__icon">
        <PassiveSkillIcon id={loadout.id} />
      </div>
      <div>
        <div className="passive-skill-hero__eyebrow">Passive Skill</div>
        <h1 className="passive-skill-hero__title">{loadout.skillName}</h1>
        <div className="passive-skill-hero__subtitle">
          {loadout.authorityName} · {loadout.status}
        </div>
        <div className="passive-skill-hero__tag">{loadout.tag}</div>
        <p className="passive-skill-hero__description">{loadout.shortDescription}</p>
      </div>
    </section>
  );
}

export function PassiveSkillCard({ label, headline, body, children, highlight = false }) {
  return (
    <section className={`passive-skill-card${highlight ? ' passive-skill-card--highlight' : ''}`}>
      <div className="passive-skill-card__label">{label}</div>
      {headline && <h2 className="passive-skill-card__headline">{headline}</h2>}
      {body && <p className="passive-skill-card__body">{body}</p>}
      {children}
    </section>
  );
}

export function PassiveSkillBulletRow({ text, icon = 'flow' }) {
  return (
    <div className="passive-skill-detail-list__row">
      <span className="passive-skill-detail-list__icon">
        <BulletIcon kind={icon} />
      </span>
      <p className="passive-skill-detail-list__copy">{text}</p>
    </div>
  );
}

export default function PassiveSkillDetailScreen({ loadout, onBack, open = true }) {
  useEffect(() => {
    if (typeof document === 'undefined' || !open) return undefined;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = previousOverflow;
    };
  }, [open]);

  if (!loadout) return null;

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="passive-skill-screen"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.22, ease: 'easeOut' }}
        >
          <div className="passive-skill-screen__veil" aria-hidden="true" />
          <motion.div
            className="passive-skill-screen__body"
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 18 }}
            transition={{ duration: 0.32, ease: [0.22, 1, 0.36, 1] }}
          >
            <div className="passive-skill-screen__nav">
              <button type="button" className="passive-skill-screen__back" onClick={onBack} aria-label="Go back">
                ←
              </button>
              <div className="passive-skill-screen__nav-label">Passive Skills</div>
              <div />
            </div>

            <div className="passive-skill-screen__stack">
              <PassiveSkillHero loadout={loadout} />

              <PassiveSkillCard
                label={loadout.coreFunction.label}
                headline={loadout.coreFunction.headline}
                body={loadout.coreFunction.body}
              />

              <PassiveSkillCard label="HOW IT WORKS">
                <div className="passive-skill-detail-list">
                  {loadout.howItWorks.map((item, index) => (
                    <PassiveSkillBulletRow
                      key={item}
                      text={item}
                      icon={index === 1 ? 'time' : index === 2 ? 'check' : 'flow'}
                    />
                  ))}
                </div>
              </PassiveSkillCard>

              <PassiveSkillCard label="DISTORTIONS">
                <div className="passive-skill-detail-list">
                  {loadout.distortions.map((item) => (
                    <PassiveSkillBulletRow key={item} text={item} icon="warning" />
                  ))}
                </div>
              </PassiveSkillCard>

              <PassiveSkillCard label="DECISION CHECK" highlight>
                <div className="passive-skill-card__question">{loadout.decisionCheck}</div>
              </PassiveSkillCard>

              <PassiveSkillCard label="IN PRACTICE">
                <div className="passive-skill-detail-list">
                  {loadout.inPractice.map((item, index) => (
                    <PassiveSkillBulletRow
                      key={item}
                      text={item}
                      icon={index === 0 ? 'time' : index === 1 ? 'flow' : 'check'}
                    />
                  ))}
                </div>
              </PassiveSkillCard>
            </div>

            <div className="passive-skill-screen__footer">{loadout.footerNote}</div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
