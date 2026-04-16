/**
 * DimensionCard — Expandable card for one profile dimension
 * Shared by Tithi, Element, and Life Path sections
 */

import { useState } from 'react';

export function DimensionCard({ icon, system, name, axiom, tabs, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen);
  const [activeTab, setActiveTab] = useState(tabs?.[0]?.key || null);

  const activeContent = tabs?.find(t => t.key === activeTab)?.principles || [];

  return (
    <div className={`dim-card${open ? ' open' : ''}`}>
      {/* Header — click to toggle */}
      <div className="dim-card-header" onClick={() => setOpen(o => !o)}>
        <div className="dim-card-icon">{icon}</div>
        <div className="dim-card-titles">
          <div className="dim-card-system">{system}</div>
          <div className="dim-card-name">{name}</div>
        </div>
        <div className={`dim-card-chevron${open ? ' rotated' : ''}`}>▼</div>
      </div>

      {/* Body — hidden when closed */}
      {open && (
        <div className="dim-card-body">
          {axiom && <p className="dim-card-axiom">{axiom}</p>}

          {/* Tabs */}
          {tabs && tabs.length > 1 && (
            <div className="tabs-header">
              {tabs.map(t => (
                <button
                  key={t.key}
                  className={`tab-btn${activeTab === t.key ? ' active' : ''}`}
                  onClick={() => setActiveTab(t.key)}
                >
                  {t.label}
                </button>
              ))}
            </div>
          )}

          {/* Principles */}
          <div className="principles-list">
            {activeContent.map((p, i) => (
              <div key={i} className="principle-item">
                <div className="principle-title">{p.title}</div>
                <div className="principle-body">{p.body}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
