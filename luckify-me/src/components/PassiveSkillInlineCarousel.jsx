import { AnimatePresence, motion } from 'framer-motion';

function BulletGlyph({ kind = 'flow' }) {
  const common = {
    fill: 'none',
    stroke: 'currentColor',
    strokeLinecap: 'round',
    strokeLinejoin: 'round',
    strokeWidth: 1.55,
  };

  switch (kind) {
    case 'time':
      return (
        <svg viewBox="0 0 16 16" aria-hidden="true">
          <circle {...common} cx="8" cy="8" r="5.4" />
          <path {...common} d="M8 4.8v3.2l2.1 1.6" />
        </svg>
      );
    case 'warning':
      return (
        <svg viewBox="0 0 16 16" aria-hidden="true">
          <path {...common} d="M8 2.8 13.3 12H2.7Z" />
          <path {...common} d="M8 6.1v2.8" />
          <circle cx="8" cy="11.1" r=".7" fill="currentColor" stroke="none" />
        </svg>
      );
    case 'check':
      return (
        <svg viewBox="0 0 16 16" aria-hidden="true">
          <path {...common} d="M3 8.4 6.1 11.1 13 4.8" />
        </svg>
      );
    default:
      return (
        <svg viewBox="0 0 16 16" aria-hidden="true">
          <path {...common} d="M1.8 8c1.3-1.5 2.7-2.3 4.4-2.3 1.8 0 2.4 1.6 3.9 1.6 1.3 0 2.7-.6 4.1-1.9" />
          <path {...common} d="M1.8 11.1c1.3-1.5 2.7-2.3 4.4-2.3 1.8 0 2.4 1.6 3.9 1.6 1.3 0 2.7-.6 4.1-1.9" />
        </svg>
      );
  }
}

function DetailList({ items, iconKinds, iconKind }) {
  return (
    <div className="passive-skill-inline-section-list">
      {items.map((item, index) => (
        <div key={item} className="passive-skill-inline-section-row">
          <span className="passive-skill-inline-section-icon">
            <BulletGlyph kind={iconKinds?.[index] || iconKind || 'flow'} />
          </span>
          <span className="passive-skill-inline-section-copy">{item}</span>
        </div>
      ))}
    </div>
  );
}

function DetailSection({ label, headline, body, items, iconKinds, iconKind, highlight = false }) {
  return (
    <section className={`passive-skill-inline-section${highlight ? ' passive-skill-inline-section--highlight' : ''}`}>
      <div className="passive-skill-inline-section-label">{label}</div>
      {headline ? <h4 className="passive-skill-inline-section-headline">{headline}</h4> : null}
      {body ? <p className="passive-skill-inline-section-body">{body}</p> : null}
      {items?.length ? (
        <DetailList items={items} iconKinds={iconKinds} iconKind={iconKind} />
      ) : null}
    </section>
  );
}

export default function PassiveSkillInlineCarousel({ loadout, open, onToggle }) {
  return (
    <div className={`passive-skill-inline${open ? ' open' : ''}`}>
      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            className="passive-skill-inline-panel"
            initial={{ opacity: 0, height: 0, y: -8 }}
            animate={{ opacity: 1, height: 'auto', y: 0 }}
            exit={{ opacity: 0, height: 0, y: -8 }}
            transition={{ duration: 0.28, ease: [0.22, 1, 0.36, 1] }}
          >
            <div className="passive-skill-inline-panel-head">
              <div className="passive-skill-inline-panel-head-copy">
                <div className="passive-skill-inline-panel-title">{loadout.skillName}</div>
                <div className="passive-skill-inline-panel-subtitle">{loadout.authorityName}</div>
              </div>
              <button type="button" className="passive-skill-inline-close" onClick={onToggle}>
                Collapse
              </button>
            </div>

            <div className="passive-skill-inline-sections">
              <DetailSection
                label={loadout.coreFunction.label}
                headline={loadout.coreFunction.headline}
                body={loadout.coreFunction.body}
              />

              <DetailSection
                label="HOW IT WORKS"
                items={loadout.howItWorks}
                iconKinds={['flow', 'time', 'check']}
              />

              <DetailSection
                label="DISTORTIONS"
                items={loadout.distortions}
                iconKind="warning"
              />

              <DetailSection
                label="DECISION CHECK"
                headline={loadout.decisionCheck}
                highlight
              />

              <DetailSection
                label="IN PRACTICE"
                items={loadout.inPractice}
                iconKinds={['time', 'flow', 'check']}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
