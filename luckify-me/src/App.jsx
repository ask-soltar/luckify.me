import { useEffect, useMemo, useRef, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { ProfileForm } from './components/ProfileForm.jsx';
import { ProfileDisplay } from './components/ProfileDisplay.jsx';
import { ProfileMenu } from './components/ProfileMenu.jsx';
import { MainQuestRevealLoader } from './components/MainQuestRevealLoader.tsx';
import { DevShareCardGallery } from './components/DevShareCardGallery.jsx';
import { calculateProfile, generateId, resolveProfileName } from './utils/profileCalculator.js';
import { useProfileStorage } from './hooks/useProfileStorage.js';
import { calcTodayWindow } from './utils/luckyWindow.js';
import { MAIN_QUEST_ENTRIES, getMainQuestEntry } from './content/mainQuest.ts';
import './styles/pip-boy.css';
import './App.css';

// TODO: wire to actual purpose gate resolver when multi-gate support is ready
function resolveMainQuestGateLine(result) {
  const gate = result?.geneKeys?.purpose?.gate;
  const line = result?.geneKeys?.purpose?.line;
  if (Number.isFinite(gate) && Number.isFinite(line)) return { gate, line };
  return null;
}

function sampleQuestOptions(excludeGateLine, count = 20) {
  const pool = MAIN_QUEST_ENTRIES
    .filter(e => `${e.gate}.${e.line}` !== excludeGateLine)
    .map(e => ({ gateLine: `${e.gate}.${e.line}`, questName: e.mainQuest, subtitle: 'Purpose Signal' }));
  return pool.sort(() => Math.random() - 0.5).slice(0, count);
}

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

const IS_DEV_GALLERY = typeof window !== 'undefined' &&
  new URLSearchParams(window.location.search).get('dev') === 'gallery';

export default function App() {
  if (IS_DEV_GALLERY) {
    return (
      <DevShareCardGallery
        onClose={() => {
          const url = new URL(window.location.href);
          url.searchParams.delete('dev');
          window.location.href = url.toString();
        }}
      />
    );
  }

  const scrollAreaRef = useRef(null);
  const [page, setPage] = useState('calc');       // 'calc' | 'profile'
  const [menuOpen, setMenuOpen] = useState(false);
  const [activeProfile, setActiveProfile] = useState(null);
  const [activeProfileId, setActiveProfileId] = useState(null);
  const [shouldAnimateRhythmReveal, setShouldAnimateRhythmReveal] = useState(false);
  const [fullScreenRevealOpen, setFullScreenRevealOpen] = useState(false);
  const [veiled, setVeiled] = useState(false);    // full-screen threshold transition
  const [revealQuestData, setRevealQuestData] = useState(null); // { gateLine, questName, possibleQuests }

  const {
    profiles,
    currentProfileId,
    addProfile,
    updateProfile,
    deleteProfile,
    switchProfile,
    getCurrentProfile
  } = useProfileStorage();

  function scrollAppToTop() {
    const run = () => {
      scrollAreaRef.current?.scrollTo?.({ top: 0, behavior: 'auto' });
      window.scrollTo?.({ top: 0, behavior: 'auto' });
      if (typeof document !== 'undefined') {
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
      }
    };

    run();
    window.requestAnimationFrame(() => {
      run();
      window.requestAnimationFrame(run);
    });
  }

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

    // Resolve Main Quest for the reveal
    const resolved = resolveMainQuestGateLine(result);
    const questEntry = resolved ? getMainQuestEntry(resolved.gate, resolved.line) : null;
    const resolvedGateLine = resolved ? `${resolved.gate}.${resolved.line}` : '59.2';
    const resolvedQuestName = questEntry?.mainQuest ?? 'Your Main Quest is being prepared.';
    const possibleQuests = sampleQuestOptions(resolvedGateLine);

    // Threshold: fade to void, swap content at peak black, then reveal
    setVeiled(true);
    setTimeout(() => {
      setActiveProfile(result);
      setActiveProfileId(nextProfileId);
      setShouldAnimateRhythmReveal(false);
      if (animateReveal) {
        setRevealQuestData({ gateLine: resolvedGateLine, questName: resolvedQuestName, possibleQuests });
        setFullScreenRevealOpen(true);
      } else {
        setPage('profile');
        scrollAppToTop();
      }
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
      setFullScreenRevealOpen(false);
      setPage('profile');
      scrollAppToTop();
    } else {
      setActiveProfileId(null);
      setShouldAnimateRhythmReveal(false);
      setFullScreenRevealOpen(false);
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
    setFullScreenRevealOpen(false);
    setPage('calc');
    scrollAppToTop();
  }

  function handleResetRhythmReveal() {
    if (!activeProfileId || typeof window === 'undefined') return;
    window.localStorage.removeItem(getRevealStorageKey(activeProfileId));
    setShouldAnimateRhythmReveal(false);
    window.setTimeout(() => {
      setShouldAnimateRhythmReveal(true);
    }, 0);
  }

  function handleFirstRevealComplete() {
    window.setTimeout(() => {
      setPage('profile');
      setFullScreenRevealOpen(false);
      scrollAppToTop();
    }, 420);
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

  useEffect(() => {
    if (typeof document === 'undefined') return undefined;
    const previousOverflow = document.body.style.overflow;
    const previousTouchAction = document.body.style.touchAction;

    if (fullScreenRevealOpen) {
      document.body.style.overflow = 'hidden';
      document.body.style.touchAction = 'none';
      scrollAppToTop();
    }

    return () => {
      document.body.style.overflow = previousOverflow;
      document.body.style.touchAction = previousTouchAction;
    };
  }, [fullScreenRevealOpen]);

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
          <button
            type="button"
            className="header-chip"
            onClick={() => setMenuOpen(true)}
            aria-label="Open saved profiles"
          >
            <div className="header-chip-dot" />
            <span className="header-chip-name">{displayName}</span>
          </button>
        )}

        <button className="hamburger" onClick={() => setMenuOpen(true)} aria-label="Open menu">
          <span /><span /><span />
        </button>
      </header>

      {/* Main scroll area */}
      <main
        className={`scroll-area scroll-area--${page}`}
        ref={scrollAreaRef}
      >
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

      <AnimatePresence>
        {fullScreenRevealOpen && activeProfile && revealQuestData && (
          <motion.div
            className="first-reveal-overlay first-reveal-overlay--quest"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.35, ease: 'easeOut' }}
          >
            <motion.div
              className="first-reveal-shell first-reveal-shell--quest"
              initial={{ opacity: 0, y: 24, scale: 0.985 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 16, scale: 0.992 }}
              transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
            >
              <MainQuestRevealLoader
                resolvedGateLine={revealQuestData.gateLine}
                resolvedQuestName={revealQuestData.questName}
                possibleQuests={revealQuestData.possibleQuests}
                onComplete={handleFirstRevealComplete}
              />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

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
