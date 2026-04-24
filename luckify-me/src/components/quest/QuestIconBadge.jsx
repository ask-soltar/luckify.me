export function QuestIconBadge({ depth = 0, symbol }) {
  return (
    <span className="quest-icon-badge" data-depth={depth} aria-hidden="true">
      <span className="quest-icon-badge__core">{symbol || ''}</span>
    </span>
  );
}
