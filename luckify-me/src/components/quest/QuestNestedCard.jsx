import { motion } from 'framer-motion';
import { getQuestDepthVars } from '../../constants/questDepthTheme.ts';
import { QuestIconBadge } from './QuestIconBadge.jsx';
import { QuestRail } from './QuestRail.jsx';
import { QuestNestedAccordion } from './QuestNestedAccordion.jsx';

function clearNestedSubtreeState(card, state) {
  const nextOpenMap = { ...state.openMap };
  const nextRevealedMap = { ...state.revealedMap };
  const defaultRevealedCount = (card.nestedCards || []).filter(
    nestedCard => nestedCard.defaultOpen
  ).length;

  nextRevealedMap[card.id] = defaultRevealedCount;

  function visit(node) {
    delete nextOpenMap[node.id];
    delete nextRevealedMap[node.id];
    node.nestedCards?.forEach(visit);
  }

  card.nestedCards?.forEach(visit);

  return {
    openMap: nextOpenMap,
    revealedMap: nextRevealedMap,
  };
}

export function QuestNestedCard({
  card,
  index = 0,
  parentOpen = true,
  sectionKey,
  nestedState,
  setNestedState,
}) {
  const {
    label,
    body,
    depth = 2,
    icon,
    nestedCards = [],
    eyebrow,
    collapsible = false,
    defaultOpen = true,
    revealNextOnCta = false,
    childDepth,
    collapseChildrenOnParentClose = false,
  } = card;
  const isOpen = collapsible
    ? (nestedState?.openMap?.[card.id] ?? Boolean(defaultOpen))
    : true;

  function handleToggle() {
    if (!setNestedState) return;

    setNestedState(current => {
      const currentlyOpen = current.openMap?.[card.id] ?? Boolean(defaultOpen);
      const nextState = {
        openMap: {
          ...current.openMap,
          [card.id]: !currentlyOpen,
        },
        revealedMap: {
          ...current.revealedMap,
        },
      };

      if (currentlyOpen && collapseChildrenOnParentClose) {
        return clearNestedSubtreeState(card, nextState);
      }

      return nextState;
    });
  }

  if (collapsible) {
    return (
      <QuestNestedAccordion
        card={card}
        index={index}
        isOpen={isOpen}
        onToggle={handleToggle}
        revealNextOnCta={revealNextOnCta}
        depth={depth}
        childDepth={childDepth}
        collapseChildrenOnParentClose={collapseChildrenOnParentClose}
        nestedState={nestedState}
        setNestedState={setNestedState}
        sectionKey={sectionKey}
      />
    );
  }

  return (
    <motion.article
      className="quest-card"
      data-depth={depth}
      style={getQuestDepthVars(depth)}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.24, delay: index * 0.045, ease: [0.22, 1, 0.36, 1] }}
    >
      <QuestRail depth={depth} />
      <div className="quest-card__body">
        <div className="quest-card__topline">
          <QuestIconBadge depth={depth} symbol={icon} />
          <div>
            {eyebrow ? <div className="quest-card__eyebrow">{eyebrow}</div> : null}
            <div className="quest-card__label">{label}</div>
          </div>
        </div>
        <p className="quest-card__copy">{body}</p>
        {nestedCards.length ? (
          <div className="quest-card__nested">
            {nestedCards.map((nestedCard, nestedIndex) => (
              <QuestNestedCard
                key={nestedCard.id}
                card={nestedCard}
                index={nestedIndex}
                parentOpen={parentOpen}
                sectionKey={sectionKey}
                nestedState={nestedState}
                setNestedState={setNestedState}
              />
            ))}
          </div>
        ) : null}
      </div>
    </motion.article>
  );
}
