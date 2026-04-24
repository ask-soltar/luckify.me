import { useRef } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { getQuestDepthVars } from '../../constants/questDepthTheme.ts';
import { QuestIconBadge } from './QuestIconBadge.jsx';
import { QuestRail } from './QuestRail.jsx';
import { QuestNestedCard } from './QuestNestedCard.jsx';

export function QuestNestedAccordion({
  card,
  index = 0,
  isOpen,
  onToggle,
  revealNextOnCta = false,
  depth,
  childDepth,
  collapseChildrenOnParentClose = false,
  nestedState,
  setNestedState,
  sectionKey,
}) {
  const {
    id,
    label,
    body,
    icon,
    eyebrow,
    nestedCards = [],
    ctaLabel = 'Go Deeper',
  } = card;

  const childRefs = useRef([]);
  const revealedChildCount = nestedState?.revealedMap?.[id] ?? 0;
  const visibleNestedCards = revealNextOnCta
    ? nestedCards.slice(0, revealedChildCount)
    : nestedCards;

  function scrollToChild(indexToFocus) {
    if (typeof window !== 'undefined') {
      window.requestAnimationFrame(() => {
        window.requestAnimationFrame(() => {
          childRefs.current[indexToFocus]?.scrollIntoView?.({
            behavior: 'smooth',
            block: 'nearest',
          });
        });
      });
    }
  }

  function revealNextChild() {
    if (!setNestedState || !nestedCards.length) return;

    const targetIndex = Math.min(revealedChildCount, nestedCards.length - 1);
    const targetCard = nestedCards[targetIndex];
    const targetAlreadyRevealed = revealedChildCount > targetIndex;
    const targetAlreadyOpen = nestedState?.openMap?.[targetCard.id] ?? Boolean(targetCard.defaultOpen);

    setNestedState(current => ({
      openMap: {
        ...current.openMap,
        [targetCard.id]: true,
      },
      revealedMap: {
        ...current.revealedMap,
        [id]: Math.max(current.revealedMap?.[id] ?? 0, targetIndex + 1),
      },
    }));

    if (targetAlreadyRevealed || targetAlreadyOpen) {
      scrollToChild(targetIndex);
      return;
    }

    scrollToChild(targetIndex);
  }

  return (
    <motion.article
      className={`quest-card quest-card--accordion${isOpen ? ' is-open' : ' is-collapsed'}`}
      data-depth={depth}
      style={getQuestDepthVars(depth)}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.24, delay: index * 0.045, ease: [0.22, 1, 0.36, 1] }}
    >
      <QuestRail depth={depth} />
      <div className="quest-card__body">
        <button
          type="button"
          className="quest-card__trigger"
          onClick={onToggle}
          aria-expanded={isOpen}
          aria-controls={`quest-card-panel-${id}`}
        >
          <div className="quest-card__topline">
            <QuestIconBadge depth={depth} symbol={icon} />
            <div>
              {eyebrow ? <div className="quest-card__eyebrow">{eyebrow}</div> : null}
              <div className="quest-card__label">{label}</div>
            </div>
          </div>
          <span className={`quest-card__chevron${isOpen ? ' is-open' : ''}`} aria-hidden="true">
            ▼
          </span>
        </button>

        <AnimatePresence initial={false}>
          {isOpen ? (
            <motion.div
              id={`quest-card-panel-${id}`}
              className="quest-card__content"
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.24, ease: [0.22, 1, 0.36, 1] }}
            >
              <p className="quest-card__copy">{body}</p>

              {revealNextOnCta && nestedCards.length ? (
                <button
                  type="button"
                  className="quest-card__cta"
                  onClick={revealNextChild}
                >
                  <span>{ctaLabel}</span>
                  <span className="quest-card__cta-chevron" aria-hidden="true">▼</span>
                </button>
              ) : null}

              {nestedCards.length ? (
                <div className="quest-card__nested">
                  {visibleNestedCards.map((nestedCard, nestedIndex) => (
                    <div
                      key={nestedCard.id}
                      ref={node => {
                        childRefs.current[nestedIndex] = node;
                      }}
                      className="quest-card__nested-slot"
                    >
                      <QuestNestedCard
                        card={{
                          ...nestedCard,
                          depth: nestedCard.depth ?? childDepth ?? depth + 1,
                        }}
                        index={nestedIndex}
                        parentOpen={isOpen}
                        sectionKey={sectionKey}
                        nestedState={nestedState}
                        setNestedState={setNestedState}
                      />
                    </div>
                  ))}
                </div>
              ) : null}
            </motion.div>
          ) : null}
        </AnimatePresence>
      </div>
    </motion.article>
  );
}
