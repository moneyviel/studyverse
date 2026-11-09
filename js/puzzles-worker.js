/* StudyVerse Puzzles — Web Worker: runs the generators in js/puzzles-core.js off the main thread so the screen
   never freezes on slower phones. Same code and same seed as the main thread, so the same puzzle. */
importScripts('puzzles-core.js' + (self.location.search || ''));   // same ?v= as this worker's URL
self.onmessage = e => {
  const m = e.data || {};
  let res = null, err = null;
  try { const f = self.PuzzleCore[m.fn]; if (typeof f !== 'function') throw new Error('unknown ' + m.fn); res = f.apply(null, m.args || []); }
  catch (x) { err = String(x && x.message || x); }
  self.postMessage({ id: m.id, res, err });
};
