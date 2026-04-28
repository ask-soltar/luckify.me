// Share card audit — reads all gate files and simulates buildShareContent
import { readFileSync, readdirSync } from 'fs';
import { join } from 'path';

const GATE_DIR = 'd:/Projects/luckify-me/luckify-me/src/content/gates/understand';
const CARD_MAX_CHARS = 120;
const WARN_CHARS = 90;

const BAD_STARTS = [
  /^But /i,
  /^Your purpose is/i,
  /^You're naturally good at/i,
  /^You are naturally good at/i,
];

function cap(s) {
  if (!s) return '';
  return s.length > CARD_MAX_CHARS ? s.slice(0, CARD_MAX_CHARS - 1) + '…' : s;
}

// Strip TypeScript wrappers and extract JSON-parseable content
function extractEntries(src) {
  let txt = src
    .replace(/^\/\/.*/gm, '')
    .replace(/\/\*[\s\S]*?\*\//g, '')
    .replace(/export\s+type\s+[^=]*?(?=\nexport|\nconst|$)/gs, '')
    .replace(/satisfies\s+\w+/g, '')
    .replace(/as\s+const/g, '')
    // Strip complex inline TS type annotation: `const foo: { ... } =` → `const foo =`
    .replace(/export\s+const\s+(\w+)\s*:\s*\{[^=]*\}\s*=/g, 'export const $1 =')
    // Strip simple TS type annotation: `const foo: SomeType =` → `const foo =`
    .replace(/export\s+const\s+(\w+)\s*:\s*[\w<>\[\]|&,\s]+\s*=/g, 'export const $1 =')
    .replace(/:\s*readonly\s+/g, ': ');

  // For files with multiple exports (e.g. gate64), prefer the one holding array/entries/content/flows
  // Try each export match in order
  const exportRe = /export\s+const\s+\w+\s*=\s*([\[\{])/g;
  let exportMatch;
  let found = null;
  while ((exportMatch = exportRe.exec(txt)) !== null) {

    const startChar = exportMatch[1];
    const startIdx = txt.indexOf(startChar, exportMatch.index + exportMatch[0].length - 1);
    let depth = 0, endIdx = startIdx;
    for (let i = startIdx; i < txt.length; i++) {
      if (txt[i] === '{' || txt[i] === '[') depth++;
      else if (txt[i] === '}' || txt[i] === ']') { depth--; if (depth === 0) { endIdx = i; break; } }
    }
    let rawJson = txt.slice(startIdx, endIdx + 1).replace(/,(\s*[}\]])/g, '$1');
    let parsed;
    try { parsed = JSON.parse(rawJson); } catch { continue; }

    let entries = null;
    if (Array.isArray(parsed)) entries = parsed;
    else if (Array.isArray(parsed?.entries)) entries = parsed.entries;
    else if (Array.isArray(parsed?.content)) entries = parsed.content;
    else if (Array.isArray(parsed?.flows))   entries = parsed.flows;

    if (entries && entries.length > 0 && entries[0]?.gateLine) { found = entries; break; }
  }

  return found ?? [];
}

function buildShareContent(flow) {
  const sc = flow.shareCard;
  const hasExplicit = !!(sc?.giftLine && sc?.patternLine && sc?.questLine);
  return {
    hasExplicit,
    gift:    cap(sc?.giftLine    ?? flow.intro?.openingStatement),
    pattern: cap(sc?.patternLine ?? flow.intro?.limitation),
    quest:   cap(sc?.questLine   ?? flow.intro?.purpose),
    rawGift:    sc?.giftLine    ?? flow.intro?.openingStatement ?? '',
    rawPattern: sc?.patternLine ?? flow.intro?.limitation ?? '',
    rawQuest:   sc?.questLine   ?? flow.intro?.purpose ?? '',
  };
}

function warnings(field, value) {
  const w = [];
  if ((value ?? '').length > WARN_CHARS) w.push(`>${WARN_CHARS}chars(${value.length})`);
  for (const rx of BAD_STARTS) {
    if (rx.test(value ?? '')) { w.push(`bad-start`); break; }
  }
  return w.length ? `[${field}: ${w.join(', ')}]` : '';
}

// ── Run audit ──────────────────────────────────────────────────────────────

const files = readdirSync(GATE_DIR).filter(f => f.endsWith('.ts')).sort((a, b) => {
  const na = parseInt(a.match(/gate(\d+)/)?.[1]);
  const nb = parseInt(b.match(/gate(\d+)/)?.[1]);
  return na - nb;
});

const rows = [];
const needsExplicit = [];
const parseErrors = [];

for (const file of files) {
  const src = readFileSync(join(GATE_DIR, file), 'utf8');
  const entries = extractEntries(src);

  if (!Array.isArray(entries)) {
    parseErrors.push({ file, error: entries?.error, hint: entries?.raw });
    continue;
  }

  for (const entry of entries) {
    if (!entry?.gateLine) continue;
    const sc = buildShareContent(entry);
    const w = [
      warnings('gift', sc.rawGift),
      warnings('pattern', sc.rawPattern),
      warnings('quest', sc.rawQuest),
    ].filter(Boolean).join(' ');

    rows.push({
      gateLine: entry.gateLine,
      questName: entry.intro?.questName ?? '?',
      source: sc.hasExplicit ? 'explicit' : 'fallback',
      gift: sc.rawGift,
      pattern: sc.rawPattern,
      quest: sc.rawQuest,
      warnings: w,
    });

    if (!sc.hasExplicit) needsExplicit.push(entry.gateLine);
  }
}

// ── Output ─────────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(120)}`);
console.log(`SHARE CARD AUDIT  —  ${rows.length} gate.lines across ${files.length} gates`);
console.log(`${'─'.repeat(120)}`);

// Full table — flag fallbacks and warnings
for (const r of rows) {
  const flag = r.source === 'fallback' ? '⚠ FALLBACK' : '✓ explicit';
  const hasWarn = r.warnings.length > 0;
  console.log(`\n${r.gateLine.padEnd(6)} ${flag}  "${r.questName}"`);
  console.log(`  gift:    ${r.gift.slice(0, 100)}${r.gift.length > 100 ? '…' : ''}`);
  console.log(`  pattern: ${r.pattern.slice(0, 100)}${r.pattern.length > 100 ? '…' : ''}`);
  console.log(`  quest:   ${r.quest.slice(0, 100)}${r.quest.length > 100 ? '…' : ''}`);
  if (hasWarn) console.log(`  WARNINGS: ${r.warnings}`);
}

// Summary
const explicitCount = rows.filter(r => r.source === 'explicit').length;
const fallbackCount = rows.filter(r => r.source === 'fallback').length;
const warnRows = rows.filter(r => r.warnings);

// String-level dedup count (explicit only)
const explicitStringMap = new Map();
for (const r of rows.filter(r => r.source === 'explicit')) {
  [r.gift, r.pattern, r.quest].forEach(s => explicitStringMap.set(s, (explicitStringMap.get(s) ?? 0) + 1));
}
const totalEmitted = explicitCount * 3;
const uniqueStrings = explicitStringMap.size;
const stringDups = [...explicitStringMap.entries()].filter(([, n]) => n > 1);

console.log(`\n${'═'.repeat(120)}`);
console.log(`SUMMARY`);
console.log(`${'═'.repeat(120)}`);
console.log(`Total gate.lines scanned:        ${rows.length}`);
console.log(`  With explicit shareCard:        ${explicitCount}`);
console.log(`  Using intro fallback:           ${fallbackCount}`);
console.log(`  Remaining to add shareCard:     ${fallbackCount}`);
console.log(`Explicit copy strings emitted:   ${totalEmitted}  (${explicitCount} × 3)`);
console.log(`Unique explicit strings:         ${uniqueStrings}${uniqueStrings !== totalEmitted ? '  ⚠ DUPLICATES: ' + (totalEmitted - uniqueStrings) : '  ✓ all unique'}`);
console.log(`With warnings:                   ${warnRows.length}`);

if (stringDups.length) {
  console.log(`\nDUPLICATE STRINGS (appear on multiple entries):`);
  stringDups.forEach(([s, n]) => console.log(`  [×${n}] "${s.slice(0, 80)}"`));
}

if (parseErrors.length) {
  console.log(`\nPARSE ERRORS (${parseErrors.length}):`);
  parseErrors.forEach(e => console.log(`  ${e.file}: ${e.error}`));
}

console.log(`\nFALLBACK gate.lines needing explicit shareCard wording:`);
// Group by gate
const byGate = {};
for (const gl of needsExplicit) {
  const g = gl.split('.')[0];
  (byGate[g] = byGate[g] || []).push(gl);
}
for (const [gate, lines] of Object.entries(byGate).sort((a,b) => +a[0] - +b[0])) {
  console.log(`  Gate ${gate}: ${lines.join(', ')}`);
}

if (warnRows.length) {
  console.log(`\nWARNING DETAIL:`);
  warnRows.forEach(r => console.log(`  ${r.gateLine.padEnd(6)} ${r.warnings}`));
}
