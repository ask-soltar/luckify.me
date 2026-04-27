import { forwardRef, useLayoutEffect, useMemo, useRef, useState } from 'react';

function statusKey(node) {
  return node.state.toLowerCase();
}

function branchKey(node) {
  if (node.type === 'Root') return 'root';
  if (node.type === 'Mastery') return 'mastery';
  return (node.branch || 'field').toLowerCase();
}

function BranchGlyph({ label }) {
  const glyphs = {
    root: 'Q',
    awareness: 'A',
    embodiment: 'E',
    field: 'F',
    mastery: 'M',
  };

  return <span className="perk-tree__node-glyph" aria-hidden="true">{glyphs[label] || 'Q'}</span>;
}

function PerkProgressStrip({ progress }) {
  return (
    <div className="perk-tree__progress" aria-label={progress.title}>
      <div className="perk-tree__progress-title">{progress.title}</div>
      <div className="perk-tree__progress-items">
        {progress.items.map((item) => (
          <span key={item} className="perk-tree__progress-item">
            {item}
          </span>
        ))}
      </div>
    </div>
  );
}

const PerkNodeButton = forwardRef(function PerkNodeButton({ node, selected, layout, onSelect }, ref) {
  const branch = branchKey(node);
  const status = statusKey(node);

  return (
    <button
      ref={ref}
      type="button"
      className={`perk-tree__node perk-tree__node--${layout} perk-tree__node--${branch} perk-tree__node--${status}${selected ? ' is-selected' : ''}`}
      onClick={() => onSelect(node.id)}
      aria-pressed={selected}
    >
      <div className="perk-tree__node-shell">
        <div className="perk-tree__node-top">
          <BranchGlyph label={branch} />
          <span className="perk-tree__node-type">{node.branch || node.type}</span>
        </div>
        <div className="perk-tree__node-name">{node.shortLabel || node.name}</div>
        <div className={`perk-tree__node-status perk-tree__node-status--${status}`}>{node.state}</div>
      </div>
    </button>
  );
});

export function PerkTreeCanvas({ tree, selectedId, onSelect }) {
  const isMasterySelected = tree.masteryNode.id === selectedId;
  const branchNodes = tree.branchNodes || [];
  const awarenessNode = branchNodes.find((node) => node.branch === 'Awareness');
  const embodimentNode = branchNodes.find((node) => node.branch === 'Embodiment');
  const fieldNode = branchNodes.find((node) => node.branch === 'Field');
  const highlightNode = (nodeId) => selectedId === nodeId || isMasterySelected;

  const layoutRef = useRef(null);
  const rootRef = useRef(null);
  const awarenessRef = useRef(null);
  const embodimentRef = useRef(null);
  const fieldRef = useRef(null);
  const masteryRef = useRef(null);

  const [svgBox, setSvgBox] = useState({ width: 1, height: 1 });
  const [anchors, setAnchors] = useState(null);

  useLayoutEffect(() => {
    const measure = () => {
      const layoutEl = layoutRef.current;
      const rootEl = rootRef.current;
      const awarenessEl = awarenessRef.current;
      const embodimentEl = embodimentRef.current;
      const fieldEl = fieldRef.current;
      const masteryEl = masteryRef.current;

      if (!layoutEl || !rootEl || !awarenessEl || !embodimentEl || !fieldEl || !masteryEl) return;

      const layoutRect = layoutEl.getBoundingClientRect();
      const rectFor = (element) => element.getBoundingClientRect();
      const topCenter = (rect) => ({
        x: rect.left - layoutRect.left + rect.width / 2,
        y: rect.top - layoutRect.top,
      });
      const bottomCenter = (rect) => ({
        x: rect.left - layoutRect.left + rect.width / 2,
        y: rect.bottom - layoutRect.top,
      });

      const rootRect = rectFor(rootEl);
      const awarenessRect = rectFor(awarenessEl);
      const embodimentRect = rectFor(embodimentEl);
      const fieldRect = rectFor(fieldEl);
      const masteryRect = rectFor(masteryEl);

      setSvgBox({ width: layoutRect.width, height: layoutRect.height });
      setAnchors({
        rootBottom: bottomCenter(rootRect),
        awarenessTop: topCenter(awarenessRect),
        embodimentTop: topCenter(embodimentRect),
        fieldTop: topCenter(fieldRect),
        awarenessBottom: bottomCenter(awarenessRect),
        embodimentBottom: bottomCenter(embodimentRect),
        fieldBottom: bottomCenter(fieldRect),
        masteryTop: topCenter(masteryRect),
      });
    };

    measure();
    window.addEventListener('resize', measure);
    return () => window.removeEventListener('resize', measure);
  }, [tree]);

  return (
    <div className="perk-tree__canvas">
      <div className="perk-tree__layout" ref={layoutRef}>
        <svg
          className="perk-tree__connectors"
          viewBox={`0 0 ${svgBox.width} ${svgBox.height}`}
          preserveAspectRatio="none"
          aria-hidden="true"
        >
          {anchors ? (
            <>
              <line
                x1={anchors.rootBottom.x}
                y1={anchors.rootBottom.y}
                x2={anchors.awarenessTop.x}
                y2={anchors.awarenessTop.y}
                className={`perk-tree__connector${highlightNode(awarenessNode?.id) ? ' is-active' : ''}`}
              />
              <line
                x1={anchors.rootBottom.x}
                y1={anchors.rootBottom.y}
                x2={anchors.embodimentTop.x}
                y2={anchors.embodimentTop.y}
                className={`perk-tree__connector${highlightNode(embodimentNode?.id) ? ' is-active' : ''}`}
              />
              <line
                x1={anchors.rootBottom.x}
                y1={anchors.rootBottom.y}
                x2={anchors.fieldTop.x}
                y2={anchors.fieldTop.y}
                className={`perk-tree__connector${highlightNode(fieldNode?.id) ? ' is-active' : ''}`}
              />
              <line
                x1={anchors.awarenessBottom.x}
                y1={anchors.awarenessBottom.y}
                x2={anchors.masteryTop.x}
                y2={anchors.masteryTop.y}
                className={`perk-tree__connector${highlightNode(awarenessNode?.id) ? ' is-active' : ''}`}
              />
              <line
                x1={anchors.embodimentBottom.x}
                y1={anchors.embodimentBottom.y}
                x2={anchors.masteryTop.x}
                y2={anchors.masteryTop.y}
                className={`perk-tree__connector${highlightNode(embodimentNode?.id) ? ' is-active' : ''}`}
              />
              <line
                x1={anchors.fieldBottom.x}
                y1={anchors.fieldBottom.y}
                x2={anchors.masteryTop.x}
                y2={anchors.masteryTop.y}
                className={`perk-tree__connector${highlightNode(fieldNode?.id) ? ' is-active' : ''}`}
              />
            </>
          ) : null}
        </svg>

        <div className="perk-tree__slot perk-tree__slot--root">
          <PerkNodeButton
            ref={rootRef}
            node={tree.rootNode}
            layout="root"
            selected={selectedId === tree.rootNode.id}
            onSelect={onSelect}
          />
        </div>

        <div className="perk-tree__slot perk-tree__slot--awareness">
          {awarenessNode ? (
            <PerkNodeButton
              ref={awarenessRef}
              node={awarenessNode}
              layout="awareness"
              selected={selectedId === awarenessNode.id}
              onSelect={onSelect}
            />
          ) : null}
        </div>

        <div className="perk-tree__slot perk-tree__slot--embodiment">
          {embodimentNode ? (
            <PerkNodeButton
              ref={embodimentRef}
              node={embodimentNode}
              layout="embodiment"
              selected={selectedId === embodimentNode.id}
              onSelect={onSelect}
            />
          ) : null}
        </div>

        <div className="perk-tree__slot perk-tree__slot--field">
          {fieldNode ? (
            <PerkNodeButton
              ref={fieldRef}
              node={fieldNode}
              layout="field"
              selected={selectedId === fieldNode.id}
              onSelect={onSelect}
            />
          ) : null}
        </div>

        <div className="perk-tree__slot perk-tree__slot--mastery">
          <PerkNodeButton
            ref={masteryRef}
            node={tree.masteryNode}
            layout="mastery"
            selected={selectedId === tree.masteryNode.id}
            onSelect={onSelect}
          />
        </div>
      </div>
    </div>
  );
}

function PerkNodeDetailPanel({ node }) {
  const branch = node.branch || node.type;
  const status = statusKey(node);
  const isRoot = node.type === 'Root';
  const isMastery = node.type === 'Mastery';

  const thirdLabel = isRoot ? 'Path Role' : isMastery ? 'Integration Path' : 'Development Cue';
  const fourthLabel = isRoot ? 'Development Note' : 'Mastery Marker';
  const thirdBody = isRoot
    ? (node.pathRole || 'This capacity already forms the core of the quest path.')
    : isMastery
      ? (node.integrationPath || 'This path matures through deeper integration.')
      : (node.developmentCue || 'Stay with the next developmental edge of this branch.');
  const fourthBody = isRoot
    ? (node.developmentNote || 'This quest already anchors the developmental path.')
    : (node.masteryMarker || 'This branch becomes steadier through lived repetition.');

  return (
    <article className="perk-tree__detail">
      <div className="perk-tree__detail-topline">
        <div className="perk-tree__detail-kicker">{branch} · {node.type}</div>
        <div className={`perk-tree__detail-status perk-tree__detail-status--${status}`}>{node.state}</div>
      </div>
      <h3 className="perk-tree__detail-title">{node.name}</h3>

      <div className="perk-tree__detail-stack">
        <section className="perk-tree__detail-block">
          <div className="perk-tree__detail-label">Description</div>
          <p className="perk-tree__detail-copy">{node.description}</p>
        </section>
        <section className="perk-tree__detail-block">
          <div className="perk-tree__detail-label">Effect</div>
          <p className="perk-tree__detail-copy">{node.effect}</p>
        </section>
        <section className="perk-tree__detail-block">
          <div className="perk-tree__detail-label">{thirdLabel}</div>
          <p className="perk-tree__detail-copy">{thirdBody}</p>
        </section>
        <section className="perk-tree__detail-block">
          <div className="perk-tree__detail-label">{fourthLabel}</div>
          <p className="perk-tree__detail-copy">{fourthBody}</p>
        </section>
      </div>
    </article>
  );
}

export function PerkTreeScreen({ tree, onBack }) {
  const [selectedId, setSelectedId] = useState(tree.rootNode.id);

  const allNodes = useMemo(
    () => [tree.rootNode, ...(tree.branchNodes || []), tree.masteryNode],
    [tree],
  );

  const selectedNode = allNodes.find((node) => node.id === selectedId) || tree.rootNode;

  return (
    <section className="perk-tree" aria-labelledby="perk-tree-title">
      <div className="perk-tree__header-card">
        <button type="button" className="perk-tree__back" onClick={onBack}>
          <span aria-hidden="true">‹</span>
          <span>Back to Main Quest</span>
        </button>

        <div className="perk-tree__eyebrow">Perk Tree</div>
        <h2 className="perk-tree__title" id="perk-tree-title">{tree.mainQuestName}</h2>
        <div className="perk-tree__meta-row">
          <div className="perk-tree__source-line">{tree.sourceLine}</div>
          <div className="perk-tree__state-pill">{tree.questState}</div>
        </div>
        <p className="perk-tree__subtitle">{tree.subtitle}</p>
      </div>

      <PerkProgressStrip progress={tree.progress} />
      <PerkTreeCanvas tree={tree} selectedId={selectedId} onSelect={setSelectedId} />
      <PerkNodeDetailPanel node={selectedNode} />
    </section>
  );
}
