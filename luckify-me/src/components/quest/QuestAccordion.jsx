import { AnimatePresence, motion } from 'framer-motion';
import { getQuestDepthVars } from '../../constants/questDepthTheme.ts';
import { QuestIconBadge } from './QuestIconBadge.jsx';
import { QuestNestedCard } from './QuestNestedCard.jsx';

export function QuestAccordion({ section, open, onToggle, nestedState, setNestedState, sectionKey }) {
  const { id, title, depth = 1, icon, cards = [] } = section;

  return (
    <section
      className={`quest-accordion${open ? ' is-open' : ''}`}
      data-depth={depth}
      style={getQuestDepthVars(depth)}
    >
      <button
        type="button"
        className="quest-accordion__trigger"
        onClick={onToggle}
        aria-expanded={open}
        aria-controls={`quest-accordion-panel-${id}`}
      >
        <div className="quest-accordion__title-wrap">
          <QuestIconBadge depth={depth} symbol={icon} />
          <span className="quest-accordion__title">{title}</span>
        </div>
        <span className={`quest-accordion__chevron${open ? ' is-open' : ''}`} aria-hidden="true">
          ▼
        </span>
      </button>

      <AnimatePresence initial={false}>
        {open ? (
          <motion.div
            id={`quest-accordion-panel-${id}`}
            className="quest-accordion__body"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.26, ease: [0.22, 1, 0.36, 1] }}
          >
            <div className="quest-accordion__inner">
              {cards.map((card, index) => (
                <QuestNestedCard
                  key={card.id}
                  card={card}
                  index={index}
                  parentOpen={open}
                  sectionKey={sectionKey}
                  nestedState={nestedState}
                  setNestedState={setNestedState}
                />
              ))}
            </div>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </section>
  );
}
