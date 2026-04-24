import { useMemo, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import {
  getCommandModeMainQuestModel,
  COMMAND_MODE_LAYER_PRESENTATION,
} from '../content/commandModeMainQuest.ts';
import { PerkTreeScreen } from './PerkTreeScreen.jsx';

const NO_ACTIVE_SECTION = '__none__';

function QuestArtifactIcon() {
  return (
    <div className="cmd-main-quest__artifact-icon" aria-hidden="true">
      <span className="cmd-main-quest__artifact-ring cmd-main-quest__artifact-ring--outer" />
      <span className="cmd-main-quest__artifact-ring cmd-main-quest__artifact-ring--inner" />
      <span className="cmd-main-quest__artifact-core" />
    </div>
  );
}

function BranchGlyph({ name }) {
  const glyphs = {
    Awareness: 'A',
    Embodiment: 'E',
    Field: 'F',
    Mastery: 'M',
  };

  return <span className="cmd-main-quest__perk-glyph" aria-hidden="true">{glyphs[name] || 'Q'}</span>;
}

function QuestDataCard({
  id,
  title,
  tone = 'violet',
  imagePath,
  blocks = [],
  chips = [],
  livePrompt,
  preview,
  summary,
  summaryRows,
  footer,
  emphasis,
  collapsible = false,
  isOpen = true,
  isActive = false,
  hasActiveLayer = false,
  accent = 'indigo',
  onToggle,
  onDestinationActivate,
}) {
  const cardClassName = `cmd-main-quest__card cmd-main-quest__card--${tone}${emphasis ? ` cmd-main-quest__card--${emphasis}` : ''}${collapsible ? ' cmd-main-quest__card--accordion' : ''}${isOpen ? ' is-open' : ' is-collapsed'} quest-layer quest-layer--${id}${isActive ? ' quest-layer--active' : ''}${hasActiveLayer && !isActive ? ' quest-layer--inactive' : ''}`;

  return (
    <article className={cardClassName} data-layer-accent={accent}>
      {collapsible ? (
        <button
          type="button"
          className="cmd-main-quest__accordion-trigger"
          onClick={onToggle}
          aria-expanded={isOpen}
        >
          {imagePath ? (
            <div className="cmd-main-quest__section-image-wrap" aria-hidden="true">
              <img className="cmd-main-quest__section-image" src={imagePath} alt="" />
            </div>
          ) : null}
          <div className="cmd-main-quest__accordion-copy">
            <div className="cmd-main-quest__card-kicker">{title}</div>
            {preview ? <div className="cmd-main-quest__accordion-preview">{preview}</div> : null}
          </div>
          <div className={`cmd-main-quest__accordion-chevron${isOpen ? ' is-open' : ''}`} aria-hidden="true">
            ▾
          </div>
        </button>
      ) : (
        <div className="cmd-main-quest__card-head">
          <div className="cmd-main-quest__card-kicker">{title}</div>
        </div>
      )}

      <AnimatePresence initial={false}>
        {isOpen ? (
          <motion.div
            className="cmd-main-quest__card-content"
            initial={collapsible ? { height: 0, opacity: 0 } : false}
            animate={{ height: 'auto', opacity: 1 }}
            exit={collapsible ? { height: 0, opacity: 0 } : false}
            transition={{ duration: 0.34, ease: [0.22, 1, 0.36, 1] }}
          >
            <div className="cmd-main-quest__card-content-inner">
              {blocks.length > 0 ? (
                <div className="cmd-main-quest__block-stack">
                  {blocks.map((block) => (
                    <div key={`${title}-${block.label}`} className={`cmd-main-quest__block cmd-main-quest__block--${block.kind || 'body'}`}>
                      <div className="cmd-main-quest__block-label">{block.label}</div>
                      <p className="cmd-main-quest__block-copy">{block.body}</p>
                    </div>
                  ))}
                </div>
              ) : null}

              {livePrompt ? (
                <div className="cmd-main-quest__live-prompt" role="note">
                  <span className="cmd-main-quest__live-prompt-mark" aria-hidden="true">◦</span>
                  <span>{livePrompt}</span>
                </div>
              ) : null}

              {chips.length > 0 ? (
                <div className="cmd-main-quest__chip-wrap" aria-label="Behavioral tells">
                  {chips.map((chip) => (
                    <span key={chip} className="cmd-main-quest__chip">
                      {chip}
                    </span>
                  ))}
                </div>
              ) : null}

              {summary ? (
                <p className="cmd-main-quest__gateway-summary">{summary}</p>
              ) : null}

              {summaryRows?.length ? (
                <div className="cmd-main-quest__gateway-list" aria-label="Perk tree branches">
                  {summaryRows.map((item) => (
                    <div key={item} className="cmd-main-quest__gateway-row">
                      <span className="cmd-main-quest__gateway-dot" aria-hidden="true" />
                      <span>{item}</span>
                    </div>
                  ))}
                </div>
              ) : null}

              {footer ? (
                <button
                  type="button"
                  className="cmd-main-quest__destination-row"
                  onClick={onDestinationActivate}
                >
                  <div className="cmd-main-quest__destination-copy">
                    <div className="cmd-main-quest__destination-label">Perk Tree</div>
                    <div className="cmd-main-quest__destination-title">Open Perk Tree</div>
                  </div>
                  <div className="cmd-main-quest__destination-chevron" aria-hidden="true">›</div>
                </button>
              ) : null}
            </div>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </article>
  );
}

export function CommandModeMainQuest({
  gateLine,
}) {
  const model = getCommandModeMainQuestModel(gateLine ?? '59.2');
  const [isMainQuestCollapsed, setIsMainQuestCollapsed] = useState(false);
  const [activeAccordion, setActiveAccordion] = useState(NO_ACTIVE_SECTION);
  const [accordionResetVersion, setAccordionResetVersion] = useState(0);
  const [view, setView] = useState('quest');
  const accordionIds = new Set([
    'quest-brief',
    'field-briefing',
    'assets-friction',
    'grounding-effect',
    'unlock-condition',
    'mini-perk-preview',
  ]);
  const activeLayer = activeAccordion === NO_ACTIVE_SECTION ? null : activeAccordion;
  const hasActiveLayer = Boolean(activeLayer);
  const activeLayerAccent = activeLayer ? COMMAND_MODE_LAYER_PRESENTATION[activeLayer]?.accent || 'indigo' : 'none';
  const sectionMeta = useMemo(
    () =>
      Object.fromEntries(
        model.cards.map((card) => [card.id, { accent: COMMAND_MODE_LAYER_PRESENTATION[card.id]?.accent || 'indigo' }])
      ),
    [model.cards]
  );

  const handleAccordionToggle = (cardId) => {
    setActiveAccordion((current) => (current === cardId ? NO_ACTIVE_SECTION : cardId));
  };

  const collapseAllSections = () => {
    setActiveAccordion(NO_ACTIVE_SECTION);
    setAccordionResetVersion((current) => current + 1);
  };

  const handleHeroReset = () => {
    setIsMainQuestCollapsed((current) => {
      const nextCollapsed = !current;
      collapseAllSections();
      return nextCollapsed;
    });
  };

  if (view === 'perk-tree') {
    return <PerkTreeScreen tree={resolvedPerkTree} onBack={() => setView('quest')} />;
  }

  return (
    <section
      className={`cmd-main-quest${hasActiveLayer ? ' cmd-main-quest--layer-active' : ''}`}
      data-active-layer={activeLayer || 'none'}
      data-active-accent={activeLayerAccent}
      aria-labelledby="cmd-main-quest-title"
    >
      <div className="cmd-main-quest__section-label">{model.sectionLabel}</div>

      <button
        type="button"
        className="cmd-main-quest__hero cmd-main-quest__hero--resettable"
        onClick={handleHeroReset}
        aria-label="Collapse all Main Quest sections"
      >
        <div className="cmd-main-quest__hero-atmosphere" aria-hidden="true">
          <span className="cmd-main-quest__hero-haze" />
          <span className="cmd-main-quest__hero-grid" />
          <span className="cmd-main-quest__hero-orbit cmd-main-quest__hero-orbit--outer" />
          <span className="cmd-main-quest__hero-orbit cmd-main-quest__hero-orbit--inner" />
          <span className="cmd-main-quest__hero-stars" />
        </div>

        <div className="cmd-main-quest__hero-topline">
          <QuestArtifactIcon />
          <div className="cmd-main-quest__hero-copy">
            <div className="cmd-main-quest__world-label">{model.hero.worldLabel}</div>
            <h2 className="cmd-main-quest__hero-title" id="cmd-main-quest-title">
              {model.hero.mainQuest}
            </h2>
            <div className="cmd-main-quest__source-line">{model.hero.sourceLine}</div>
          </div>
          <div className="cmd-main-quest__state-pill">{model.hero.questState}</div>
        </div>

        <p className="cmd-main-quest__hero-subtitle">{model.hero.atmosphericSubtitle}</p>
      </button>

      <AnimatePresence initial={false}>
        {!isMainQuestCollapsed ? (
          <motion.div
            className="cmd-main-quest__stack"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.28, ease: [0.22, 1, 0.36, 1] }}
          >
            <div className="cmd-main-quest__stack-inner">
              {model.cards.map((card) => {
                const isAccordion = accordionIds.has(card.id);
                const isOpen = isAccordion ? activeAccordion === card.id : true;

                return (
                  <QuestDataCard
                    key={`${card.id}-${accordionResetVersion}`}
                    id={card.id}
                    title={card.title}
                    tone={card.tone}
                    imagePath={card.imagePath}
                    blocks={card.blocks}
                    chips={card.chips}
                    livePrompt={card.livePrompt}
                    preview={card.preview}
                    summary={card.summary}
                    summaryRows={card.summaryRows}
                    footer={card.footer}
                    emphasis={card.emphasis}
                    collapsible={isAccordion}
                    isOpen={isOpen}
                    isActive={activeLayer === card.id}
                    hasActiveLayer={hasActiveLayer}
                    accent={sectionMeta[card.id]?.accent}
                    onToggle={isAccordion ? () => handleAccordionToggle(card.id) : undefined}
                    onDestinationActivate={card.id === 'mini-perk-preview' ? () => setView('perk-tree') : undefined}
                  />
                );
              })}
            </div>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </section>
  );
}
