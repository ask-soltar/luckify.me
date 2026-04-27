import type { MainQuestUnderstandFlow } from './mainQuestUnderstandSeed';

// ── Gate content imports ────────────────────────────────────────────────────
// Shapes: { content:[...] } | { entries:[...] } | [...] (direct array)
import gate1Raw   from './gates/understand/gate1_understand_flow_v2_score97';
import gate2Raw   from './gates/understand/gate2_understand_flow_v2_score97';
import gate3Raw   from './gates/understand/gate3_understand_flow_v2_score97';
import { gate4UnderstandFlow as gate4Raw } from './gates/understand/gate4_understand_flow_v2_score97';
import gate5Raw   from './gates/understand/gate5_understand_flow_v2_score97';
import gate6Raw   from './gates/understand/gate6_understand_flow_v2_score97';
import gate7Raw   from './gates/understand/gate7_understand_flow_v2_score97';
import gate8Raw   from './gates/understand/gate8_understand_flow_v2_score97';
import gate9Raw   from './gates/understand/gate9_understand_flow_v2_score97';
import gate10Raw  from './gates/understand/gate10_understand_flow_v2_score97';
import gate11Raw  from './gates/understand/gate11_understand_flow_v2_score97';
import gate12Raw  from './gates/understand/gate12_understand_flow_v2_score97';
import gate13Raw  from './gates/understand/gate13_understand_flow_v2_score97';
import gate14Raw  from './gates/understand/gate14_understand_flow_v2_score97';
import gate15Raw  from './gates/understand/gate15_understand_flow_v2_score97';
import gate16Raw  from './gates/understand/gate16_understand_flow_v2_score97';
import gate17Raw  from './gates/understand/gate17_understand_flow_v2_score97';
import gate18Raw  from './gates/understand/gate18_understand_flow_v2_score97';
import gate19Raw  from './gates/understand/gate19_understand_flow_v2_score97';
import gate20Raw  from './gates/understand/gate20_understand_flow_v2_score97';
import gate21Raw  from './gates/understand/gate21_understand_flow_v2_score97';
import gate22Raw  from './gates/understand/gate22_understand_flow_v2_score97';
import gate23Raw  from './gates/understand/gate23_understand_flow_v2_score97';
import gate24Raw  from './gates/understand/gate24_understand_flow_v2_score97';
import gate25Raw  from './gates/understand/gate25_understand_flow_v2_score97';
import gate26Raw  from './gates/understand/gate26_understand_flow_v2_score97';
import gate27Raw  from './gates/understand/gate27_understand_flow_v2_score97';
import gate28Raw  from './gates/understand/gate28_understand_flow_v2_score97';
import gate29Raw  from './gates/understand/gate29_understand_flow_v2_score97';
import gate34Raw  from './gates/understand/gate34_understand_flow_v2_score97';
import gate39Raw  from './gates/understand/gate39_understand_flow_v2_score97';
import gate40Raw  from './gates/understand/gate40_understand_flow_v2_score97';
import gate41Raw  from './gates/understand/gate41_understand_flow_v2_score97';
import gate44Raw  from './gates/understand/gate44_understand_flow_v2_score97';
import gate52Raw  from './gates/understand/gate52_understand_flow_v2_score97';
import gate59Raw  from './gates/understand/gate59_understand_flow_v2_score97';
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
  ...extractEntries(gate1Raw),
  ...extractEntries(gate2Raw),
  ...extractEntries(gate3Raw),
  ...extractEntries(gate4Raw),
  ...extractEntries(gate5Raw),
  ...extractEntries(gate6Raw),
  ...extractEntries(gate7Raw),
  ...extractEntries(gate8Raw),
  ...extractEntries(gate9Raw),
  ...extractEntries(gate10Raw),
  ...extractEntries(gate11Raw),
  ...extractEntries(gate12Raw),
  ...extractEntries(gate13Raw),
  ...extractEntries(gate14Raw),
  ...extractEntries(gate15Raw),
  ...extractEntries(gate16Raw),
  ...extractEntries(gate17Raw),
  ...extractEntries(gate18Raw),
  ...extractEntries(gate19Raw),
  ...extractEntries(gate20Raw),
  ...extractEntries(gate21Raw),
  ...extractEntries(gate22Raw),
  ...extractEntries(gate23Raw),
  ...extractEntries(gate24Raw),
  ...extractEntries(gate25Raw),
  ...extractEntries(gate26Raw),
  ...extractEntries(gate27Raw),
  ...extractEntries(gate28Raw),
  ...extractEntries(gate29Raw),
  ...extractEntries(gate34Raw),
  ...extractEntries(gate39Raw),
  ...extractEntries(gate40Raw),
  ...extractEntries(gate41Raw),
  ...extractEntries(gate44Raw),
  ...extractEntries(gate52Raw),
  ...extractEntries(gate59Raw),
  ...extractEntries(gate64Raw),
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
