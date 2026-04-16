/**
 * LunarDots — 30-dot lunar cycle position visualizer
 * Renders 30 circles, active one colored by tithi type
 */

const TYPE_COLORS = {
  nanda:  '#7F77DD',
  bhadra: '#1D9E75',
  jaya:   '#BA7517',
  rikta:  '#D85A30',
  purna:  '#378ADD',
};

const LEGEND = [
  { type: 'nanda',  label: 'Nanda'  },
  { type: 'bhadra', label: 'Bhadra' },
  { type: 'jaya',   label: 'Jaya'   },
  { type: 'rikta',  label: 'Rikta'  },
  { type: 'purna',  label: 'Purna'  },
];

const TYPES_CYCLE = ['nanda', 'bhadra', 'jaya', 'rikta', 'purna'];

export function LunarDots({ tIdx }) {
  const dots = Array.from({ length: 30 }, (_, i) => {
    const dotType = TYPES_CYCLE[i % 5];
    const isActive = i === tIdx;
    return { i, dotType, isActive };
  });

  return (
    <div className="lunar-dots-container">
      <div className="lunar-dots">
        {dots.map(({ i, dotType, isActive }) => (
          <div
            key={i}
            className={`lunar-dot${isActive ? ' active' : ''}`}
            style={{
              background: isActive ? TYPE_COLORS[dotType] : 'rgba(0,255,0,0.08)',
              boxShadow: isActive
                ? `0 0 8px ${TYPE_COLORS[dotType]}, 0 0 2px ${TYPE_COLORS[dotType]}`
                : 'none',
              borderColor: isActive ? TYPE_COLORS[dotType] : 'rgba(0,255,0,0.2)',
            }}
            title={`Tithi ${i + 1}`}
          />
        ))}
      </div>
      <div className="lunar-legend">
        {LEGEND.map(({ type, label }) => (
          <div key={type} className="legend-item">
            <div className="legend-dot" style={{ background: TYPE_COLORS[type] }} />
            <span>{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
