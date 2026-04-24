import { useMemo, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { getQuestThemeVars } from '../../constants/questDepthTheme.ts';
import { QuestAccordion } from './QuestAccordion.jsx';
import { QuestBackground } from './QuestBackground.jsx';
import { QuestHero } from './QuestHero.jsx';
import { QuestNestedCard } from './QuestNestedCard.jsx';

function buildInitialNestedState(cards = []) {
  const openMap = {};
  const revealedMap = {};

  cards.forEach(card => {
    if (card.collapsible) {
      openMap[card.id] = Boolean(card.defaultOpen);
      revealedMap[card.id] = Math.max(
        0,
        (card.nestedCards || []).filter(nestedCard => nestedCard.defaultOpen).length
      );
    }

    if (card.nestedCards?.length) {
      const childState = buildInitialNestedState(card.nestedCards);
      Object.assign(openMap, childState.openMap);
      Object.assign(revealedMap, childState.revealedMap);
    }
  });

  return { openMap, revealedMap };
}

export function QuestShell({ panel }) {
  const sectionMap = useMemo(
    () => new Map(panel.sections.map(section => [section.id, section])),
    [panel.sections]
  );
  const initialTopLevel = panel.sections.find(section => section.defaultOpen)?.id ?? null;
  const [isOpen, setIsOpen] = useState(true);
  const [activeTopLevel, setActiveTopLevel] = useState(initialTopLevel);
  const [nestedState, setNestedState] = useState(() =>
    initialTopLevel
      ? buildInitialNestedState(sectionMap.get(initialTopLevel)?.cards || [])
      : { openMap: {}, revealedMap: {} }
  );

  function toggleSection(id) {
    if (activeTopLevel === id) {
      setActiveTopLevel(null);
      setNestedState({ openMap: {}, revealedMap: {} });
      return;
    }

    setActiveTopLevel(id);
    setNestedState(buildInitialNestedState(sectionMap.get(id)?.cards || []));
  }

  return (
    <section className="quest-shell" style={getQuestThemeVars()}>
      <QuestBackground />
      <div className="quest-shell__inner">
        <button
          type="button"
          className="quest-shell__trigger"
          onClick={() => setIsOpen(open => !open)}
          aria-expanded={isOpen}
          aria-controls={`quest-shell-panel-${panel.id}`}
        >
          <QuestHero
            eyebrow={panel.eyebrow}
            title={panel.title}
            metadata={panel.metadata}
            summary={panel.summary}
            depth={0}
          />
          <span className={`quest-shell__chevron${isOpen ? ' is-open' : ''}`} aria-hidden="true">
            ▼
          </span>
        </button>

        <AnimatePresence initial={false}>
          {isOpen ? (
            <motion.div
              id={`quest-shell-panel-${panel.id}`}
              className="quest-shell__content"
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.28, ease: [0.22, 1, 0.36, 1] }}
            >
              <div className="quest-shell__content-inner">
                {panel.introCard ? (
                  <QuestNestedCard card={panel.introCard} />
                ) : null}

                <div className="quest-shell__section-list">
                  {panel.sections.map(section => (
                    <QuestAccordion
                      key={section.id}
                      section={section}
                      open={activeTopLevel === section.id}
                      onToggle={() => toggleSection(section.id)}
                      nestedState={nestedState}
                      setNestedState={setNestedState}
                      sectionKey={section.id}
                    />
                  ))}
                </div>

                {panel.reminderCard ? (
                  <QuestNestedCard card={panel.reminderCard} />
                ) : null}
              </div>
            </motion.div>
          ) : null}
        </AnimatePresence>
      </div>
    </section>
  );
}
