import { useState, useEffect } from 'react';
import './QuestRevealOverlay.css';

const MESSAGES = [
  'Decoding your pattern\u2026',
  'Mapping your path\u2026',
];

// Timing constants (ms)
const MSG_SWAP_AT = 1200;  // swap label text
const EXIT_START  = 2350;  // begin exit animation
const COMPLETE_AT = 2950;  // call onComplete (after exit transition)

interface Props {
  onComplete: () => void;
}

export function QuestRevealOverlay({ onComplete }: Props) {
  const [msgIdx, setMsgIdx]   = useState(0);
  const [exiting, setExiting] = useState(false);

  useEffect(() => {
    const t1 = setTimeout(() => setMsgIdx(1),    MSG_SWAP_AT);
    const t2 = setTimeout(() => setExiting(true), EXIT_START);
    const t3 = setTimeout(() => onComplete(),     COMPLETE_AT);
    return () => { clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); };
  }, [onComplete]);

  return (
    <div
      className={`mqr-overlay${exiting ? ' mqr-overlay--exiting' : ''}`}
      aria-live="polite"
      aria-label="Reading your profile"
    >
      {/* Mandala as faint zooming background — not a separate reveal step */}
      <div className="mqr-bg" aria-hidden="true" />

      {/* Foreground: radial ambient glow + cycling text */}
      <div className="mqr-glow-ring" aria-hidden="true" />
      <p className="mqr-message" key={msgIdx}>
        {MESSAGES[msgIdx]}
      </p>
    </div>
  );
}
