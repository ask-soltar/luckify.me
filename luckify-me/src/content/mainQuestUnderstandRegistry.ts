import type { MainQuestUnderstandFlow } from './mainQuestUnderstandSeed';
import { mainQuestUnderstandSeed } from './mainQuestUnderstandSeed';

// ── Gate content imports ────────────────────────────────────────────────────
// Each file may use one of three shapes:
//   { content: [...] }   — gate11, gate34, gate39, gate41, gate44
//   { entries: [...] }   — gate9, gate40, gate52
//   [...] (direct array) — gate64
import gate9Raw   from './gates/understand/gate9_understand_flow_v2_score97';
import gate11Raw  from './gates/understand/gate11_understand_flow_v2_score97';
import gate34Raw  from './gates/understand/gate34_understand_flow_v2_score97';
import gate39Raw  from './gates/understand/gate39_understand_flow_v2_score97';
import gate40Raw  from './gates/understand/gate40_understand_flow_v2_score97';
import gate41Raw  from './gates/understand/gate41_understand_flow_v2_score97';
import gate44Raw  from './gates/understand/gate44_understand_flow_v2_score97';
import gate52Raw  from './gates/understand/gate52_understand_flow_v2_score97';
import gate64Raw  from './gates/understand/gate64_understand_flow_v2_precision_scored';

// ── Shape normalizer ────────────────────────────────────────────────────────
function extractEntries(raw: unknown): MainQuestUnderstandFlow[] {
  if (Array.isArray(raw)) return raw as MainQuestUnderstandFlow[];
  if (raw && typeof raw === 'object') {
    const r = raw as Record<string, unknown>;
    if (Array.isArray(r.content)) return r.content as MainQuestUnderstandFlow[];
    if (Array.isArray(r.entries)) return r.entries as MainQuestUnderstandFlow[];
  }
  return [];
}

// ── Build registry ──────────────────────────────────────────────────────────
const ALL_ENTRIES: MainQuestUnderstandFlow[] = [
  ...extractEntries(gate9Raw),
  ...extractEntries(gate11Raw),
  ...extractEntries(gate34Raw),
  ...extractEntries(gate39Raw),
  ...extractEntries(gate40Raw),
  ...extractEntries(gate41Raw),
  ...extractEntries(gate44Raw),
  ...extractEntries(gate52Raw),
  ...extractEntries(gate64Raw),
  // Seed always present as fallback entry
  mainQuestUnderstandSeed,
];

const REGISTRY = new Map<string, MainQuestUnderstandFlow>(
  ALL_ENTRIES.map(entry => [entry.gateLine, entry])
);

/**
 * Look up the Understand Flow content for a given gate.line string (e.g. "64.2").
 * Returns null if no content exists for that gateLine.
 */
export function getUnderstandFlow(gateLine: string | null | undefined): MainQuestUnderstandFlow | null {
  if (!gateLine) return null;
  return REGISTRY.get(gateLine) ?? null;
}

/** All registered gateLine keys — useful for debugging. */
export const REGISTERED_GATE_LINES = [...REGISTRY.keys()];
