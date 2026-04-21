function normalizeElement(element) {
  if (!element) return 'earth';
  const normalized = String(element).trim().toLowerCase();
  return ['fire', 'water', 'wood', 'metal', 'earth'].includes(normalized)
    ? normalized
    : 'earth';
}

function normalizeEmphasis(emphasis) {
  return emphasis === 'strong' ? 'strong' : 'soft';
}

export const TRAJECTORY_MARKER_ELEMENT_VARIANTS = ['wood', 'fire', 'earth', 'metal', 'water'];

export function TrajectoryMarker({
  lifePathNumber,
  element,
  size = 68,
  className = '',
  emphasis = 'soft',
}) {
  const displayValue = lifePathNumber == null ? '?' : String(lifePathNumber);
  const digitCount = Math.min(displayValue.length, 2);
  const elementVariant = normalizeElement(element);
  const emphasisVariant = normalizeEmphasis(emphasis);

  return (
    <div
      className={[
        'trajectory-marker',
        `trajectory-marker--${elementVariant}`,
        `trajectory-marker--${emphasisVariant}`,
        className,
      ].filter(Boolean).join(' ')}
      style={{ '--trajectory-size': `${size}px` }}
      aria-hidden="true"
    >
      <div className="trajectory-marker-shell">
        <span className="trajectory-marker-element trajectory-marker-element--primary" />
        <span className="trajectory-marker-element trajectory-marker-element--secondary" />
        <span className="trajectory-marker-ring trajectory-marker-ring--outer" />
        <span className="trajectory-marker-ring trajectory-marker-ring--inner" />
        <span className="trajectory-marker-path trajectory-marker-path--base" />
        <span className="trajectory-marker-path trajectory-marker-path--vector" />
        <span className="trajectory-marker-node trajectory-marker-node--origin" />
        <span className="trajectory-marker-node trajectory-marker-node--pivot" />
        <span className="trajectory-marker-node trajectory-marker-node--apex" />
        <span className={`trajectory-marker-value trajectory-marker-value--digits-${digitCount}`}>
          {displayValue}
        </span>
      </div>
    </div>
  );
}
