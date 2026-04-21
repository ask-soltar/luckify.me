import { useState, useMemo } from 'react';
import { ProfileForm } from './components/ProfileForm.jsx';
import { ProfileDisplay } from './components/ProfileDisplay.jsx';
import { ProfileMenu } from './components/ProfileMenu.jsx';
import { calculateProfile, generateId, resolveProfileName } from './utils/profileCalculator.js';
import { useProfileStorage } from './hooks/useProfileStorage.js';
import { calcTodayWindow } from './utils/luckyWindow.js';
import './styles/pip-boy.css';
import './App.css';

// RGB triplets for the zone color CSS variable — used to tint the shell faintly
const ZONE_RGB = {
  Pink:   '200, 48, 150',
  Orange: '200, 110, 20',
  Blue:   '40, 110, 210',
  Yellow: '180, 155, 10',
  Green:  '20, 165, 50',
  Purple: '120, 55, 200',
  Red:    '205, 35, 25',
  Brown:  '130, 95, 60',
};

function getRevealStorageKey(profileId) {
  return `rhythmRevealSeen_${profileId}`;
}

export default function App() {
  const [page, setPage] = useState('calc');       // 'calc' | 'profile'
  const [menuOpen, setMenuOpen] = useState(false);
  const [activeProfile, setActiveProfile] = useState(null);
  const [activeProfileId, setActiveProfileId] = useState(null);
  const [shouldAnimateRhythmReveal, setShouldAnimateRhythmReveal] = useState(false);
  const [veiled, setVeiled] = useState(false);    // full-screen threshold transition

  const {
    profiles,
    currentProfileId,
    addProfile,
    updateProfile,
    deleteProfile,
    switchProfile,
    getCurrentProfile
  } = useProfileStorage();

  // Called when form submits — threshold transition before reveal
  function handleCalculate(formData) {
    const result = calculateProfile({
      year:     parseInt(formData.year),
      month:    parseInt(formData.month),
      day:      parseInt(formData.day),
      hour12:   formData.hour12,
      minute:   formData.minute,
      ampm:     formData.ampm,
      tzOffset: formData.birthGMT ?? 0,
      birthLat: formData.birthLat ?? null,
      birthLng: formData.birthLng ?? null,
    });

    // Store location data on result for LuckyWindow
    result.birthGMT    = formData.birthGMT;
    result.birthTzId   = formData.birthTzId;
    result.birthLat    = formData.birthLat ?? null;
    result.birthLng    = formData.birthLng ?? null;
    result.currentGMT  = formData.currentGMT;
    result.currentTzId = formData.currentTzId;
    const h = formData.ampm === 'PM' && formData.hour12 < 12
      ? formData.hour12 + 12
      : formData.ampm === 'AM' && formData.hour12 === 12
        ? 0
        : formData.hour12;
    result.birthTime = `${String(h).padStart(2,'0')}:${String(formData.minute).padStart(2,'0')}`;

    const currentP = getCurrentProfile();
    const resolvedName = resolveProfileName(formData.displayName, result);
    let nextProfileId = currentP?.id || null;
    let animateReveal = false;

    if (currentP) {
      updateProfile(currentP.id, {
        result,
        name: formData.displayName ? resolvedName : currentP.name || resolvedName
      });
      nextProfileId = currentP.id;
    } else {
      const id   = generateId();
      addProfile({ id, name: resolvedName, result });
      nextProfileId = id;
      animateReveal = true;
    }

    // Threshold: fade to void, swap content at peak black, then reveal
    setVeiled(true);
    setTimeout(() => {
      setActiveProfile(result);
      setActiveProfileId(nextProfileId);
      setShouldAnimateRhythmReveal(animateReveal);
      setPage('profile');
      setTimeout(() => setVeiled(false), 120);
    }, 480);
  }

  // Switch to an existing profile
  function handleSwitchProfile(id) {
    switchProfile(id);
    const p = profiles.find(x => x.id === id);
    if (p?.result) {
      setActiveProfile(p.result);
      setActiveProfileId(id);
      setShouldAnimateRhythmReveal(false);
      setPage('profile');
    } else {
      setActiveProfileId(null);
      setShouldAnimateRhythmReveal(false);
      setPage('calc');
    }
  }

  // Update current location (timezone) without recalculating
  function handleLocationChange({ offset, tzId }) {
    const updated = { ...activeProfile, currentGMT: offset, currentTzId: tzId };
    setActiveProfile(updated);
    const currentP = getCurrentProfile();
    if (currentP) updateProfile(currentP.id, { result: updated });
  }

  // Start a fresh reading
  function handleNewProfile() {
    switchProfile(null);
    setActiveProfile(null);
    setActiveProfileId(null);
    setShouldAnimateRhythmReveal(false);
    setPage('calc');
  }

  function handleResetRhythmReveal() {
    if (!activeProfileId || typeof window === 'undefined') return;
    window.localStorage.removeItem(getRevealStorageKey(activeProfileId));
    setShouldAnimateRhythmReveal(false);
    window.setTimeout(() => {
      setShouldAnimateRhythmReveal(true);
    }, 0);
  }

  const currentP = getCurrentProfile();
  const displayName = currentP?.name || null;

  // Compute today's zone from active profile — drives the shell tint
  const zoneColor = useMemo(() => {
    if (!activeProfile) return '200, 152, 42'; // default amber
    try {
      const { y, mo, dy } = activeProfile;
      if (!y || !mo || !dy) return '200, 152, 42';
      const pad = n => String(n).padStart(2, '0');
      const r = calcTodayWindow({
        birthDate:  `${y}-${pad(mo)}-${pad(dy)}`,
        birthTime:  activeProfile.birthTime  || '12:00',
        birthGMT:   activeProfile.birthGMT   ?? 0,
        currentGMT: activeProfile.currentGMT ?? activeProfile.birthGMT ?? 0,
      });
      return ZONE_RGB[r?.zone] || '200, 152, 42';
    } catch { return '200, 152, 42'; }
  }, [activeProfile]);

  return (
    <div className="app-shell" style={{ '--zone-color': zoneColor }}>
      {/* Threshold veil — full-screen fade for the reveal transition */}
      <div className={`threshold-veil${veiled ? ' active' : ''}`} aria-hidden="true" />

      {/* Scanlines overlay */}
      <div className="scanlines" aria-hidden="true" />

      {/* Header */}
      <header className="app-header">
        <div className="header-brand">
          <div className="header-orb" />
          <span className="header-title">LUCKIFY.ME</span>
        </div>

        {displayName && (
          <div className="header-chip" onClick={() => setMenuOpen(true)}>
            <div className="header-chip-dot" />
            <span className="header-chip-name">{displayName}</span>
          </div>
        )}

        <button className="hamburger" onClick={() => setMenuOpen(true)} aria-label="Open menu">
          <span /><span /><span />
        </button>
      </header>

      {/* Main scroll area */}
      <main className="scroll-area">
        {page === 'calc' ? (
          <ProfileForm onSubmit={handleCalculate} />
        ) : (
          activeProfile && (
            <ProfileDisplay
              profile={activeProfile}
              profileId={activeProfileId}
              shouldAnimateRhythmReveal={shouldAnimateRhythmReveal}
              onResetRhythmReveal={handleResetRhythmReveal}
              onNewProfile={handleNewProfile}
              onLocationChange={handleLocationChange}
            />
          )
        )}
      </main>

      {/* Profile menu drawer */}
      <ProfileMenu
        open={menuOpen}
        profiles={profiles}
        currentProfileId={currentProfileId}
        onSwitch={handleSwitchProfile}
        onDelete={id => deleteProfile(id)}
        onNew={handleNewProfile}
        onClose={() => setMenuOpen(false)}
      />
    </div>
  );
}
