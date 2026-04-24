export function QuestRail({ depth = 0 }) {
  return (
    <div className="quest-rail" data-depth={depth} aria-hidden="true">
      <span className="quest-rail__node" />
      <span className="quest-rail__line" />
    </div>
  );
}
