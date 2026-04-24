import { getQuestDepthVars } from '../../constants/questDepthTheme.ts';
import { QuestIconBadge } from './QuestIconBadge.jsx';

export function QuestHero({ eyebrow, title, metadata = [], summary, depth = 0 }) {
  return (
    <header className="quest-hero" style={getQuestDepthVars(depth)}>
      <div className="quest-hero__motif" aria-hidden="true">
        <span className="quest-hero__sigil" />
        <span className="quest-hero__orbit quest-hero__orbit--outer" />
        <span className="quest-hero__orbit quest-hero__orbit--inner" />
        <span className="quest-hero__path" />
        <span className="quest-hero__constellation" />
      </div>
      <div className="quest-hero__header">
        <span className="quest-hero__crest">
          <QuestIconBadge depth={depth} symbol="Q" />
        </span>
        <div className="quest-hero__copy">
          <div className="quest-hero__eyebrow">{eyebrow}</div>
          <h2 className="quest-hero__title">{title}</h2>
        </div>
      </div>
      {metadata.length ? (
        <div className="quest-hero__meta">
          {metadata.map(item => (
            <span key={item} className="quest-hero__meta-item">
              {item}
            </span>
          ))}
        </div>
      ) : null}
      {summary ? (
        <p className="quest-hero__summary">{summary}</p>
      ) : null}
    </header>
  );
}
