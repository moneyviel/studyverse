// Pure logic of the "puzzle-key" Edge Function (no Deno / network APIs here, so tools can test it with Node).
// computeAnswer(core, spec, getJSON) → the canonical answer the race is checked against (PuzzleCore.answerOf form):
//   sdk / csdk / kak → grid string row by row · xw → answers in entry order · ws → words (sorted) · an → answers in order
// studyverse._puzzle_norm() in SQL then normalises both the key and every submitted answer (whitespace removed,
// upper-case, ws as a sorted set).
// Content (what PuzzleCore.contentPathOf(spec) lists), assembled exactly like js/puzzles.js terms():
//   number puzzles → null · school chapter → the subject JSON · CA chapter → { structure, units, banks, keyItems }
//   (CA: contentPathOf(spec) gives the structure, then contentPathOf(spec, structure) the unit + bank files; bank files
//    are optional; js/ca-keys-data.js is NOT fetched — it is bundled next to the function, keyItems = CaKeysData.ITEMS).
export const SITE = 'https://knowtopia.in/';
export const KEYS_JS = 'js/ca-keys-data.js';

// only the app's own content files may be fetched: content/…json, no "..", no query, no other host
export function safePath(p) {
  return typeof p === 'string' && p.length <= 200 && /^content\/[A-Za-z0-9_\-\/.]+\.json$/.test(p) && !p.includes('..') && !p.includes('//');
}
const okAnswer = a => (typeof a === 'string' && a.length > 0 && a.length <= 20000) ||
  (Array.isArray(a) && a.length > 0 && a.length <= 400 && a.every(x => typeof x === 'string' && x.length > 0 && x.length <= 200));

export class KeyError extends Error { constructor(code, msg) { super(msg); this.code = code; } }
const bad = () => new KeyError('path', 'This puzzle could not be prepared.');
const paths = (core, spec, st) => { const p = core.contentPathOf(spec, st); return p == null ? [] : Array.isArray(p) ? p : [p]; };

export async function contentFor(core, spec, getJSON, keyItems) {
  const sc = (spec && spec.sc) || { k: 'q' };
  const first = paths(core, spec).filter(p => p !== KEYS_JS);
  if (!first.length) return null;
  if (first.length > 60 || !first.every(safePath)) throw bad();
  if (sc.k === 's') return getJSON(first[0]);
  if (sc.k === 'c') {
    const sPath = first.find(p => /\/structure\.json$/.test(p)); if (!sPath) throw bad();
    const structure = await getJSON(sPath);
    const all = paths(core, spec, structure).filter(p => p !== KEYS_JS && p !== sPath);
    if (all.length > 120 || !all.every(safePath)) throw bad();
    const idOf = {}; (structure.papers || []).forEach(p => (p.chapters || []).forEach(c => (c.units || []).forEach(u => { if (u.file) idOf[u.file] = u.id; })));
    const units = {}, banks = {};
    await Promise.all(all.map(async p => {
      const m = /\/bank\/([^/]+)\.json$/.exec(p);
      if (m) { try { banks[m[1]] = await getJSON(p); } catch (e) { /* optional: no extra MCQs */ } return; }
      if (idOf[p]) units[idOf[p]] = await getJSON(p);
    }));
    return { structure, units, banks, keyItems: keyItems || [] };
  }
  return null;
}

export async function computeAnswer(core, spec, getJSON, keyItems) {
  if (!core || typeof core.solutionOf !== 'function' || typeof core.contentPathOf !== 'function') throw new KeyError('engine', 'The puzzle engine on the server is out of date.');
  if (!spec || typeof spec !== 'object' || Array.isArray(spec)) throw new KeyError('spec', 'Unknown puzzle.');
  // a spec made by a different engine version would build a different puzzle: refuse rather than mis-judge answers
  if (spec.v != null && core.VERSION != null && String(spec.v) !== String(core.VERSION)) throw new KeyError('version', 'Please update the app and pick the puzzle again.');
  const content = await contentFor(core, spec, getJSON, keyItems);
  let a = await core.solutionOf(spec, content);
  if (Array.isArray(a) && a.length && a.every(r => Array.isArray(r))) a = a.map(r => r.join('')).join('');   // grid given as rows of cells
  if (!okAnswer(a)) throw new KeyError('answer', 'This puzzle could not be made on the server. Please pick another one.');
  return a;
}
