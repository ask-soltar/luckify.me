import { useState, useMemo } from 'react';
import { ALL_UNDERSTAND_FLOWS } from '../content/mainQuestUnderstandRegistry.ts';
import { MainQuestShareCard } from './MainQuestShareCard.jsx';

const WARN_CHARS = 70;
const CARD_MAX_CHARS = 120;

function cap(s) {
  if (!s) return '';
  return s.length > CARD_MAX_CHARS ? s.slice(0, CARD_MAX_CHARS - 1) + '…' : s;
}

function buildShareContent(flow) {
  const sc = flow.shareCard;
  return {
    badge: 'MAIN QUEST UNLOCKED',
    title: flow.intro?.questName ?? 'Unknown Quest',
    sections: [
      { id: 'gift',    icon: 'compass', heading: 'Your gift',    body: cap(sc?.giftLine    ?? flow.intro?.openingStatement) },
      { id: 'pattern', icon: 'spiral',  heading: 'Your pattern', body: cap(sc?.patternLine ?? flow.intro?.limitation) },
      { id: 'quest',   icon: 'portal',  heading: 'Your quest',   body: cap(sc?.questLine   ?? flow.intro?.purpose) },
    ],
  };
}

function hasWarning(flow) {
  const sc = flow.shareCard;
  const lines = sc
    ? [sc.giftLine, sc.patternLine, sc.questLine]
    : [flow.intro?.openingStatement, flow.intro?.limitation, flow.intro?.purpose];
  return lines.some(l => (l ?? '').length > WARN_CHARS);
}

function isExplicit(flow) {
  return !!(flow.shareCard?.giftLine && flow.shareCard?.patternLine && flow.shareCard?.questLine);
}

export function DevShareCardGallery({ onClose }) {
  const [filter, setFilter] = useState('explicit');
  const [search, setSearch] = useState('');

  const filtered = useMemo(() => {
    return ALL_UNDERSTAND_FLOWS.filter(flow => {
      const explicit = isExplicit(flow);
      if (filter === 'explicit' && !explicit) return false;
      if (filter === 'fallback' && explicit) return false;
      if (search) {
        const q = search.toLowerCase();
        if (!flow.gateLine.includes(q) && !(flow.intro?.questName ?? '').toLowerCase().includes(q)) return false;
      }
      return true;
    });
  }, [filter, search]);

  const counts = useMemo(() => ({
    explicit: ALL_UNDERSTAND_FLOWS.filter(isExplicit).length,
    fallback: ALL_UNDERSTAND_FLOWS.filter(f => !isExplicit(f)).length,
    all: ALL_UNDERSTAND_FLOWS.length,
  }), []);

  return (
    <div className="dev-gallery">
      {/* ── Header ── */}
      <div className="dev-gallery__header">
        <div className="dev-gallery__title-row">
          <div>
            <div className="dev-gallery__eyebrow">DEV ONLY · NOT IN PRODUCTION</div>
            <h1 className="dev-gallery__title">Share Card Gallery</h1>
            <p className="dev-gallery__subtitle">
              {counts.explicit} explicit · {counts.fallback} fallback · {counts.all} total
            </p>
          </div>
          {onClose && (
            <button type="button" className="dev-gallery__close" onClick={onClose} aria-label="Close gallery">
              ✕
            </button>
          )}
        </div>

        {/* ── Filters ── */}
        <div className="dev-gallery__filters">
          {['explicit', 'fallback', 'all'].map(f => (
            <button
              key={f}
              type="button"
              className={`dev-gallery__filter${filter === f ? ' dev-gallery__filter--active' : ''}`}
              onClick={() => setFilter(f)}
            >
              {f === 'explicit' ? `✓ Explicit (${counts.explicit})` :
               f === 'fallback' ? `⚠ Fallback (${counts.fallback})` :
               `All (${counts.all})`}
            </button>
          ))}

          <input
            type="text"
            className="dev-gallery__search"
            placeholder="Search gateLine or questName…"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>

        <div className="dev-gallery__results">
          Showing {filtered.length} card{filtered.length !== 1 ? 's' : ''}
        </div>
      </div>

      {/* ── Grid ── */}
      <div className="dev-gallery__grid">
        {filtered.map(flow => {
          const content = buildShareContent(flow);
          const explicit = isExplicit(flow);
          const warn = hasWarning(flow);
          const sc = flow.shareCard;

          return (
            <div key={flow.gateLine} className={`dev-gallery__item${warn ? ' dev-gallery__item--warn' : ''}`}>
              {/* Meta label */}
              <div className="dev-gallery__meta">
                <span className="dev-gallery__gate-label">{flow.gateLine}</span>
                <span className="dev-gallery__quest-label">{flow.intro?.questName}</span>
                <div className="dev-gallery__badges">
                  {explicit
                    ? <span className="dev-badge dev-badge--explicit">explicit</span>
                    : <span className="dev-badge dev-badge--fallback">fallback</span>}
                  {warn && <span className="dev-badge dev-badge--warn">⚠ &gt;70 chars</span>}
                </div>
              </div>

              {/* Line preview */}
              <div className="dev-gallery__lines">
                {[
                  { label: 'gift',    raw: sc?.giftLine    ?? flow.intro?.openingStatement },
                  { label: 'pattern', raw: sc?.patternLine ?? flow.intro?.limitation },
                  { label: 'quest',   raw: sc?.questLine   ?? flow.intro?.purpose },
                ].map(({ label, raw }) => (
                  <div key={label} className={`dev-gallery__line${(raw ?? '').length > WARN_CHARS ? ' dev-gallery__line--warn' : ''}`}>
                    <span className="dev-gallery__line-label">{label}</span>
                    <span className="dev-gallery__line-text">{raw ?? '—'}</span>
                    <span className="dev-gallery__line-chars">{(raw ?? '').length}ch</span>
                  </div>
                ))}
              </div>

              {/* Card preview */}
              <div className="dev-gallery__card-wrap">
                <MainQuestShareCard
                  cardId={`dev-gallery-${flow.gateLine}`}
                  content={content}
                />
              </div>
            </div>
          );
        })}

        {filtered.length === 0 && (
          <div className="dev-gallery__empty">No cards match this filter.</div>
        )}
      </div>
    </div>
  );
}
