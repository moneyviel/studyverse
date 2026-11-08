/* ================= CA tools (js/ca-tools.js) — loaded after js/ca.js =================
   1. CA Dashboard          (bottom-nav tab + home tile)   — uses Insights.dashboardFor(host,{mode:'ca',data}) when present
   2. Viva — speak & revise (unit tab + practice hub)       — speechSynthesis (en-IN) asks, SpeechRecognition answers (or typing),
                                                              offline key-point matching (twin of tools/ca_vivamatch.py)
   3. MCQ practice builder  (level → papers → chapters → difficulty → count → timer → mode), case-study sets, results, "Revise these"
   4. Mock papers           (ICAI pattern, StudyVerse practice paper — not an ICAI paper), timer, automatic marking (js/ca-check.js)
   5. Notes library         (save cards, highlight text, personal notes per unit, My notes) + one smart search
   New state lives in ST.ca: mlog, viva, tests, revise, notes, time, mockDraft (see content/ca/README.md). */
(function () {
  'use strict';
  if (!window.Ca || !Ca._) return;
  const D = document, X = Ca._;
  const C = () => { const c = X.C(); c.viva = c.viva || {}; c.tests = c.tests || []; c.revise = c.revise || {}; c.time = c.time || {}; c.mlog = c.mlog || [];
    c.notes = c.notes || {}; c.notes.saved = c.notes.saved || {}; c.notes.hl = c.notes.hl || {}; c.notes.mine = c.notes.mine || {}; c.mockDraft = c.mockDraft || {}; return c; };
  const fmt = X.fmt, tap = X.tap, say = X.say;
  const secsTxt = s => { s = Math.max(0, Math.round(s || 0)); const h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60; return h ? `${h}:${String(m).padStart(2, '0')}:${String(x).padStart(2, '0')}` : `${String(m).padStart(2, '0')}:${String(x).padStart(2, '0')}`; };
  const durTxt = s => { const m = Math.round((s || 0) / 60); return m < 60 ? `${m} min` : `${Math.floor(m / 60)} h ${m % 60 ? (m % 60) + ' min' : ''}`.trim(); };
  const pct = (a, b) => b ? Math.round(a / b * 100) : 0;
  const DIFF = [['core', 'Easy'], ['moderate', 'Moderate'], ['hard', 'ICAI-level']];
  const diffName = k => (DIFF.find(d => d[0] === k) || [k, k])[1];
  const chOf = uid => String(uid).replace(/-u\d+$/, '');
  const shuffle = (a, r = Math.random) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

  /* ================= offline matcher (keep identical to tools/ca_vivamatch.py) ================= */
  const STOP = new Set('a an the of is are was were be been being to in on at for with as that this it its by from or and which who whom will shall can may into than so such also has have had do does did there their they he she his her them we our you your i me my am'.split(' '));
  const ABBR = { dr: 'debit', cr: 'credit', tb: 'trial balance', rs: 'rupees', inr: 'rupees', sec: 'section', pl: 'profit loss', amt: 'amount', gst: 'gst', itc: 'input tax credit', cd: 'cash discount', td: 'trade discount', bal: 'balance', jf: 'jf', lf: 'lf' };
  const SMALL = { zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10, eleven: 11, twelve: 12, fifteen: 15, twenty: 20, thirty: 30, forty: 40, fifty: 50, hundred: 100 };
  const MULT = { thousand: 1e3, lakh: 1e5, lakhs: 1e5, lac: 1e5, lacs: 1e5, crore: 1e7, crores: 1e7 };
  const PROTECT = new Set('drawee drawer payee bailee bailor lessee lessor mortgagee mortgagor guarantee guarantor'.split(' '));   // CA terms never stemmed
  const ORDER = new Set(['then']);   // kept as a token; inside a phrase gap it does not count as a word
  const SUFFIX = [['ational', 'ate'], ['ations', 'ate'], ['ation', 'ate'], ['ings', ''], ['ities', 'ity'], ['ies', 'y'], ['ied', 'y'], ['ing', ''], ['edly', ''], ['ed', ''], ['ers', 'er'], ['es', ''], ['ly', ''], ['s', '']];
  function stem(w) {
    if (w.length <= 3 || /^\d/.test(w)) return w;
    if (PROTECT.has(w)) return w;
    if (w === 'willing' || w === 'willingly') return 'willing';   // not 'will'
    if (w.endsWith('s') && PROTECT.has(w.slice(0, -1))) return w.slice(0, -1);
    for (const [suf, rep] of SUFFIX) {
      if (w.endsWith(suf) && w.length - suf.length >= 3) {
        if (suf === 'ed' && w.endsWith('eed')) break;          // exceed, proceed: not a past tense
        if (suf === 's' && w.endsWith('ss')) break;
        if (suf === 'es' && !/(ss|sh|ch|x|z)es$/.test(w)) continue;
        w = w.slice(0, -suf.length) + rep; break;
      }
    }
    const l = w[w.length - 1];
    if (w.length > 3 && l === w[w.length - 2] && !'lsz'.includes(l) && !/\d/.test(l)) w = w.slice(0, -1);
    if (w.endsWith('e') && w.length > 4) w = w.slice(0, -1);
    return w;
  }
  const fmtnum = v => { v = Math.round(v * 1e4) / 1e4; return String(v); };
  const NEG = new Set('not no never cannot neither nor without cant dont doesnt isnt wont didnt arent wasnt shouldnt couldnt'.split(' '));
  const NEGX = new Set('less more exceed exceeds exceeding later earlier only just merely fewer greater'.split(' '));   // raw words
  function pairs(text) {          // [raw word, stem] after normalisation, stop-words removed
    let t = String(text || '').toLowerCase();
    t = t.split('नहीं').join(' not ');
    t = t.replace(/n['’]t\b/g, ' not');
    t = t.replace(/₹/g, ' rs ').replace(/&/g, ' and ').replace(/%/g, ' percent ');
    t = t.replace(/\ba\/c\b|\ba\/cs\b/g, ' account ');
    t = t.replace(/\bu\/s\b|\bs\.\s*(?=\d)/g, ' section ');
    t = t.replace(/(?<=\d),(?=\d{2,3}(?!\d))/g, '');   // 4,20,000 / 420,000 are one number; (4,2) is two
    t = t.replace(/(?<![a-z0-9.])[\u2212\-](?=\d)/g, ' minus ');   // −7 / -7 keep their sign (10-15 is a range)
    t = t.replace(/[^a-z0-9.\s]/g, ' ');
    t = t.replace(/(?<!\d)\.|\.(?!\d)/g, ' ');
    const raw = t.split(/\s+/).filter(Boolean), out = [];
    for (let i = 0; i < raw.length; i++) {
      const w = raw[i]; let num = null;
      if (w === 'minus' && i + 1 < raw.length && (/^\d+(\.\d+)?$/.test(raw[i + 1]) || Object.prototype.hasOwnProperty.call(SMALL, raw[i + 1]))) { i++; num = -(Object.prototype.hasOwnProperty.call(SMALL, raw[i]) ? SMALL[raw[i]] : parseFloat(raw[i])); }
      else if (/^\d+(\.\d+)?$/.test(w)) num = parseFloat(w); else if (w in SMALL) num = SMALL[w];
      if (num != null && i + 1 < raw.length && raw[i + 1] in MULT) { num *= MULT[raw[i + 1]]; i++; }
      if (num != null) { const n = fmtnum(num); out.push([n, n]); continue; }
      if (w in MULT) { const n = fmtnum(MULT[w]); out.push([n, n]); continue; }
      if (Object.prototype.hasOwnProperty.call(ABBR, w)) { ABBR[w].split(' ').forEach(x => out.push([x, stem(x)])); continue; }
      if (w === 'as' && i + 1 < raw.length && /^\d+(\.\d+)?$/.test(raw[i + 1])) { out.push(['as', 'astd']); continue; }   // AS 10 (Accounting Standard)
      if (!STOP.has(w)) out.push([w, stem(w)]);
    }
    return out.filter(x => !STOP.has(x[1]));
  }
  const tokens = text => pairs(text).map(x => x[1]);
  const isNum = w => /^-?\d+(\.\d+)?$/.test(w);
  function lev1(a, b) {
    if (Math.abs(a.length - b.length) > 1) return false;
    if (a.length === b.length) { let d = 0; for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) d++; return d <= 1; }
    if (a.length > b.length) [a, b] = [b, a];
    let i = 0; while (i < a.length && a[i] === b[i]) i++;
    return a.slice(i) === b.slice(i + 1);
  }
  function same(a, b) {
    if (a === b) return true;
    if (isNum(a) || isNum(b)) { if (isNum(a) && isNum(b)) { const x = +a, y = +b; return Math.abs(x - y) <= Math.max(Math.abs(y) * (a.includes('.') || b.includes('.') ? 0.005 : 0.0005), 0.01); } return false; }   // numbers: 0.05%, or 0.5% when decimals are written
    if (PROTECT.has(a) || PROTECT.has(b)) return false;   // party words (drawee/drawer, lessee/lessor…) must match exactly
    let n = 0; const m = Math.min(a.length, b.length); while (n < m && a[n] === b[n]) n++;
    if (n >= 5 && n >= 0.75 * m) return true;
    return m >= 6 && a[0] === b[0] && lev1(a, b);
  }
  /* negation: a hit does not count when a negator (raw word) stands within 3 words before a matched word in the same clause,
     unless the keyword phrase itself contains a negator. Phrases match inside one sentence, crossing at most two commas or colons. (see tools/ca_vivamatch.py) */
  function clauses(text) {   // clause = split at . , ; : ! ? new line; sentence = split at . ; ! ? new line
    const toks = [], raws = [], cl = [], sn = [], nc = []; let c = 0, k = 0;
    const t0 = String(text || '').replace(/(?<![a-z])no\.(?=\s*\d)/gi, 'number ').replace(/(?<![a-z])(sec|viz|cf|rs)\./gi, '$1 ').replace(/(?<![a-z])e\.g\./gi, 'eg ').replace(/(?<![a-z])i\.e\./gi, 'ie ');   // 'Sec. 37', 'No.', 'e.g.' are not sentence ends
    t0.split(/[;!?\n]|(?<!\d)\.|\.(?!\d)/).forEach((sent, n) => { sent.split(/(?<!\d):|:(?!\d)|(?<!\d),|,(?!\d)/).forEach(part => {
      part.split(/[\u2014\u2013()[\]]|\s-\s/).forEach(piece => { pairs(piece).forEach(([r, w]) => { toks.push(w); raws.push(r); cl.push(c); sn.push(n); nc.push(k); }); k++; });   // dashes and brackets end a negation window
      c++; }); });
    return { toks, raws, cl: [cl, sn, nc] };
  }
  function negated(idx, raws, cs) {
    const cl = cs.length > 2 ? cs[2] : cs[0];
    for (const x of idx) for (let y = Math.max(0, x - 3); y < x; y++) if (!idx.includes(y) && cl[y] === cl[x] && NEG.has(raws[y]) && !(y + 1 < raws.length && NEGX.has(raws[y + 1]))) return true;
    return false;
  }
  const kwSame = (p, w) => same(p[1], w) || (p[0] !== p[1] && same(p[0], w));
  function phraseIn(ph, toks, raws, cl) {
    if (!ph.length) return false;
    const check = !!raws && !ph.some(p => NEG.has(p[0]));
    for (let s = 0; s < toks.length; s++) {
      if (!kwSame(ph[0], toks[s])) continue;
      let j = s, ok = true; const idx = [s];
      for (const w of ph.slice(1)) {
        let k = -1, cnt = 0, x = j + 1;
        while (x < toks.length && cnt < 3) { if (cl && (cl[1][x] !== cl[1][s] || cl[0][x] - cl[0][s] > 2)) break; if (kwSame(w, toks[x])) { k = x; break; } if (!ORDER.has(toks[x])) cnt++; x++; }
        if (k < 0) { ok = false; break; } j = k; idx.push(k);
      }
      if (ok && !(check && negated(idx, raws, cl))) return true;
    }
    return false;
  }
  const pointHit = (p, toks, raws, cl) => p.kw.filter(g => g.split('|').some(alt => alt.trim() && phraseIn(pairs(alt), toks, raws, cl))).length >= (p.min || p.kw.length);
  function vivaScore(v, answer) {
    const { toks, raws, cl } = clauses(answer), tot = v.points.reduce((a, p) => a + p.w, 0);
    const hit = v.points.filter(p => pointHit(p, toks, raws, cl)).map(p => p.id);
    const got = v.points.filter(p => hit.includes(p.id)).reduce((a, p) => a + p.w, 0);
    return { pct: tot ? Math.round(got / tot * 100) : 0, hit };
  }

  /* ================= content helpers ================= */
  async function builtList() {
    const sts = await X.allStructures(), out = [];
    sts.forEach((st, li) => st && st.papers.forEach(p => p.chapters.forEach(c => c.units.forEach(u => { if (u.status === 'built') out.push({ level: X.LEVELS[li][0], st, p, c, u }); }))));
    return out;
  }
  async function loadAll(list) { const r = []; for (const b of list) { const d = await X.unitData(b.u.id); if (d) r.push({ ...b, d }); } return r; }
  async function findQ(key) {
    const [uid, mid] = key.split('#'); const d = await X.unitData(uid); if (!d) return null;
    const q = d.mcqs.find(x => x.id === mid); if (q) return { q, uid, d };
    for (const cs of d.cases || []) { const m = cs.mcqs.find(x => x.id === mid); if (m) return { q: m, uid, d, cs }; }
    return null;
  }
  const back = (label, fn) => { const b = D.createElement('button'); b.className = 'back'; b.textContent = '← ' + label; b.onclick = fn; return b; };
  const speakOK = () => 'speechSynthesis' in window;
  const sayQ = t => { try { if (window.A11Y && A11Y.say) return A11Y.say(t, { force: true }); if (window.speak) speak(t); } catch (e) {} return Promise.resolve(); };
  const hush = () => { try { speechSynthesis.cancel(); } catch (e) {} };
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;

  /* ================= 📷 PHOTO ANSWERS — written answers on paper, photographed =================
     Photos are compressed on the phone (longest side ≤ 1600 px, JPEG ~0.7) and kept in IndexedDB "sv_photos"
     (store "photos": { id, ref, blob, w, h, bytes, ts, kept }). Attempts keep only references: photos: [{ id, w, h, bytes }],
     so an attempt can later be sent, with its photos, to an AI checker. Photos picked but never saved are cleaned up. */
  const photos = (() => {
    let dbp = null; const urls = new Map();
    const db = () => dbp || (dbp = new Promise((res, rej) => { if (!window.indexedDB) return rej(new Error('no indexedDB'));
      const r = indexedDB.open('sv_photos', 1); r.onupgradeneeded = () => { const s = r.result.createObjectStore('photos', { keyPath: 'id' }); s.createIndex('ref', 'ref'); };
      r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); }));
    const req = (mode, fn) => db().then(d => new Promise((res, rej) => { const t = d.transaction('photos', mode), s = t.objectStore('photos'); let out; const q = fn(s); if (q) q.onsuccess = () => { out = q.result; }; t.oncomplete = () => res(out); t.onerror = t.onabort = () => rej(t.error); }));
    function compress(file, max = 1600, quality = 0.7) {
      return new Promise((res, rej) => {
        const u = URL.createObjectURL(file), img = new Image();
        img.onload = () => { try { let w = img.naturalWidth, h = img.naturalHeight; const k = Math.min(1, max / Math.max(w, h)); w = Math.round(w * k); h = Math.round(h * k);
          const c = D.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); g.drawImage(img, 0, 0, w, h); URL.revokeObjectURL(u);
          c.toBlob(b => b ? res({ blob: b, w, h }) : rej(new Error('compress failed')), 'image/jpeg', quality); } catch (e) { rej(e); } };
        img.onerror = () => { URL.revokeObjectURL(u); rej(new Error('not an image')); }; img.src = u;
      });
    }
    async function add(file, ref) {
      const { blob, w, h } = await compress(file), id = 'ph' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
      await req('readwrite', s => s.put({ id, ref, blob, w, h, bytes: blob.size, ts: Date.now(), kept: false }));
      return { id, w, h, bytes: blob.size };
    }
    const get = id => req('readonly', s => s.get(id));
    async function url(id) { if (urls.has(id)) return urls.get(id); const r = await get(id).catch(() => null); if (!r) return null; const u = URL.createObjectURL(r.blob); urls.set(id, u); return u; }
    const del = id => { const u = urls.get(id); if (u) { URL.revokeObjectURL(u); urls.delete(id); } return req('readwrite', s => s.delete(id)).catch(() => {}); };
    const keep = ids => Promise.all(ids.map(id => req('readwrite', s => { const g = s.get(id); g.onsuccess = () => { if (g.result) { g.result.kept = true; s.put(g.result); } }; return null; }))).catch(() => {});
    const all = () => req('readonly', s => s.getAll()).then(l => l || []).catch(() => []);
    async function usage() { const l = await all(); return { n: l.filter(x => x.kept).length, bytes: l.reduce((a, x) => a + (x.bytes || 0), 0), loose: l.filter(x => !x.kept && Date.now() - x.ts > 864e5) }; }
    async function clear() { const l = await all(); for (const x of l) await del(x.id); const c = C(); [c.writes, c.viva].forEach(o => Object.values(o || {}).forEach(h => h.forEach(a => { if (a.photos) a.photos = []; }))); save(); }
    const mb = b => b >= 1048576 ? `${(b / 1048576).toFixed(1)} MB` : `${Math.max(1, Math.round(b / 1024))} KB`;
    /* picker: take a photo or choose from the gallery, several pages, reorder by removing; onChange(list of {id,w,h,bytes}) */
    function picker(host, ref, onChange) {
      const list = [];
      host.innerHTML = `<p class="ca-p">Write the answer on paper as in the exam, then add a photo of each page. Good light, the whole page in view.</p>
        <div class="ca-btns"><label class="btn ca-phbtn"><input type="file" accept="image/*" capture="environment" id="phCam" hidden>📷 Take a photo</label><label class="btn ghost ca-phbtn"><input type="file" accept="image/*" multiple id="phGal" hidden>🖼 Choose from gallery</label></div>
        <p class="ca-note" id="phSt" role="status" aria-live="polite">No pages yet.</p><div class="ca-phgrid" id="phGrid"></div>`;
      const st = host.querySelector('#phSt'), grid = host.querySelector('#phGrid');
      const draw = () => {
        grid.innerHTML = list.map((p, i) => `<figure class="ca-phfig"><button class="ca-phth" data-i="${i}" aria-label="Page ${i + 1} — open large"><img data-ph="${p.id}" alt="Page ${i + 1} of your answer"></button><figcaption>Page ${i + 1} · ${mb(p.bytes)}</figcaption><button class="ca-x" data-rm="${i}" aria-label="Remove page ${i + 1}">✕</button></figure>`).join('');
        hydrate(grid); st.textContent = list.length ? `${list.length} page${list.length > 1 ? 's' : ''} added (${mb(list.reduce((a, p) => a + p.bytes, 0))}). Add more pages or tap “Check my answer”.` : 'No pages yet.';
        grid.querySelectorAll('[data-rm]').forEach(b => b.onclick = () => { const [p] = list.splice(+b.dataset.rm, 1); del(p.id); draw(); onChange(list.slice()); });
        grid.querySelectorAll('.ca-phth').forEach(b => b.onclick = () => viewer(list, +b.dataset.i));
      };
      const take = async files => {
        for (const f of files) { if (!/^image\//.test(f.type || 'image/')) continue; st.textContent = 'Compressing the photo…';
          try { list.push(await add(f, ref)); } catch (e) { toast('That photo could not be read — try another'); } }
        draw(); onChange(list.slice());
      };
      ['#phCam', '#phGal'].forEach(id => { const i = host.querySelector(id); i.onchange = () => { take([...i.files]); i.value = ''; }; });
      draw();
      return list;
    }
    function hydrate(root) { root.querySelectorAll('img[data-ph]').forEach(async im => { const u = await url(im.dataset.ph); if (u) im.src = u; else im.closest('figure, button')?.classList.add('ca-phgone'); }); }
    function strip(host, list) {
      if (!host) return; list = list || [];
      host.innerHTML = list.map((p, i) => `<button class="ca-phth" data-i="${i}" aria-label="Page ${i + 1} of your answer — open large"><img data-ph="${p.id}" alt="Page ${i + 1}"></button>`).join('');
      hydrate(host); host.querySelectorAll('.ca-phth').forEach(b => b.onclick = () => viewer(list, +b.dataset.i));
    }
    /* full-screen viewer: pinch / wheel / buttons to zoom, drag to pan, double-tap to toggle, swipe pages with ◀ ▶ */
    function viewer(list, at = 0) {
      D.getElementById('caPhView')?.remove();
      D.body.insertAdjacentHTML('beforeend', `<div class="sheet show ca-phview" id="caPhView" role="dialog" aria-modal="true" aria-labelledby="caPhVT"><div class="ca-phvbar"><b id="caPhVT">Page 1</b><span class="ca-phvtools"><button id="phZo" aria-label="Zoom out">−</button><button id="phZr" aria-label="Fit to screen">Fit</button><button id="phZi" aria-label="Zoom in">+</button><button id="phX" data-close aria-label="Close">Close</button></span></div>
        <div class="ca-phvstage" id="phStage"><img id="phImg" alt=""></div><div class="ca-phvnav"><button class="btn ghost" id="phPrev">◀ Previous page</button><button class="btn ghost" id="phNext">Next page ▶</button></div></div>`);
      const sh = D.getElementById('caPhView'), img = D.getElementById('phImg'), stage = D.getElementById('phStage');
      let sc = 1, tx = 0, ty = 0; const pts = new Map(); let pinch = null, drag = null, lastTap = 0;
      const apply = () => { img.style.transform = `translate(${tx}px, ${ty}px) scale(${sc})`; };
      const zoom = (k, cx, cy) => { const r = stage.getBoundingClientRect(); cx = cx == null ? r.width / 2 : cx - r.left; cy = cy == null ? r.height / 2 : cy - r.top; const n = Math.max(1, Math.min(6, sc * k)); tx = cx - (cx - tx) * n / sc; ty = cy - (cy - ty) * n / sc; sc = n; if (sc === 1) { tx = 0; ty = 0; } apply(); };
      const show_ = async i => { at = (i + list.length) % list.length; sc = 1; tx = ty = 0; apply(); D.getElementById('caPhVT').textContent = `Page ${at + 1} of ${list.length}`; img.alt = `Page ${at + 1} of your answer`; img.src = (await url(list[at].id)) || '';
        D.getElementById('phPrev').disabled = D.getElementById('phNext').disabled = list.length < 2; };
      stage.addEventListener('pointerdown', e => { stage.setPointerCapture(e.pointerId); pts.set(e.pointerId, [e.clientX, e.clientY]);
        if (pts.size === 2) { const [a, b] = [...pts.values()]; pinch = { d: Math.hypot(a[0] - b[0], a[1] - b[1]), s: sc }; drag = null; }
        else { drag = { x: e.clientX - tx, y: e.clientY - ty }; const t = Date.now(); if (t - lastTap < 300) zoom(sc > 1 ? 1 / sc : 2.5, e.clientX, e.clientY); lastTap = t; } });
      stage.addEventListener('pointermove', e => { if (!pts.has(e.pointerId)) return; pts.set(e.pointerId, [e.clientX, e.clientY]);
        if (pinch && pts.size === 2) { const [a, b] = [...pts.values()]; const d = Math.hypot(a[0] - b[0], a[1] - b[1]); zoom(pinch.s * d / pinch.d / sc, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2); }
        else if (drag && sc > 1) { tx = e.clientX - drag.x; ty = e.clientY - drag.y; apply(); } });
      const up = e => { pts.delete(e.pointerId); if (pts.size < 2) pinch = null; if (!pts.size) drag = null; };
      stage.addEventListener('pointerup', up); stage.addEventListener('pointercancel', up);
      stage.addEventListener('wheel', e => { e.preventDefault(); zoom(e.deltaY < 0 ? 1.2 : 1 / 1.2, e.clientX, e.clientY); }, { passive: false });
      const close = () => { sh.classList.remove('show'); setTimeout(() => sh.remove(), 50); };
      D.getElementById('phZi').onclick = () => zoom(1.5); D.getElementById('phZo').onclick = () => zoom(1 / 1.5); D.getElementById('phZr').onclick = () => { sc = 1; tx = ty = 0; apply(); };
      D.getElementById('phX').onclick = close; D.getElementById('phPrev').onclick = () => show_(at - 1); D.getElementById('phNext').onclick = () => show_(at + 1);
      sh.addEventListener('keydown', e => { if (e.key === 'Escape') close(); if (e.key === 'ArrowRight') show_(at + 1); if (e.key === 'ArrowLeft') show_(at - 1); if (e.key === '+' || e.key === '=') zoom(1.5); if (e.key === '-') zoom(1 / 1.5); });
      show_(at); setTimeout(() => D.getElementById('phX').focus(), 60);
    }
    async function usageCard(box) {
      if (!box) return; const u = await usage(); const t = box.querySelector('#caPhUseT'); if (!t) return;
      for (const x of u.loose) await del(x.id);      // pages picked but never saved, older than a day
      t.textContent = u.n ? `${u.n} photo${u.n > 1 ? 's' : ''} of your answers are stored on this device (${mb(u.bytes)}). They stay with your attempts in each question's history.` : 'No answer photos stored yet. In any written question, choose “📷 Photo of my answer”.';
      if (u.n && !box.querySelector('#caPhClr')) { box.insertAdjacentHTML('beforeend', '<button class="btn ghost" id="caPhClr">Delete all answer photos</button>');
        box.querySelector('#caPhClr').onclick = async function () { if (!this.dataset.sure) { this.dataset.sure = 1; this.textContent = 'Tap again — your marks stay, the photos go'; return; } await clear(); toast('All answer photos deleted'); this.remove(); usageCard(box); }; }
      try { if (navigator.storage && navigator.storage.estimate) { const e = await navigator.storage.estimate(); if (e.quota) t.insertAdjacentHTML('afterend', `<p class="ca-note">Space used by StudyVerse on this phone: ${mb(e.usage || 0)} of ${mb(e.quota)} available to it.</p>`); } } catch (e) {}
    }
    return { add, get, url, del, keep, all, usage, clear, picker, strip, viewer, usageCard, compress, mb };
  })();

  /* ================= 2. VIVA ================= */
  const vivaHist = (uid, vid) => (C().viva[`${uid}#${vid}`] || []).filter(a => a.status !== 'waiting');   // photo answers waiting for the AI examiners carry no marks yet
  const vivaScored = () => Object.values(C().viva).map(h => h.filter(a => a.status !== 'waiting')).filter(h => h.length);
  const vivaBest = (uid, vid) => { const h = vivaHist(uid, vid); return h.length ? Math.max(...h.map(a => a.pct)) : null; };
  const vivaBestMarks = (uid, v) => { const h = vivaHist(uid, v.id), mx = v.points.reduce((a, p) => a + p.w, 0); return h.length ? Math.max(...h.map(a => a.marks != null ? a.marks : Math.round(a.pct * mx / 100))) : null; };
  const mk1 = n => `${fmt(n)} mark${n === 1 ? '' : 's'}`;
  const qm = q => (q && +q.marks) || 1;
  function vivaDone(uid) { return Object.keys(C().viva).some(k => k.startsWith(uid + '#')); }
  function vivaTab(P, uid, d) {
    const list = d.viva || [];
    const best = list.map(v => vivaBest(uid, v.id)), ready = best.filter(b => b != null && b >= 80).length;
    P.innerHTML = `<div class="card ca-vintro"><span class="ca-k">Viva · speak &amp; revise</span><h2 class="ca-h2s">Answer out loud, like an oral exam</h2>
        <p class="ca-p">The app reads each question aloud. Answer by voice${SR ? '' : ' (voice input is not available in this browser — type instead)'}, type, or write on paper and add a 📷 photo — then see your marks for each key point. 80% of the marks or more is viva-ready.</p>
        <div class="ca-vstat"><b>${ready}/${list.length}</b><span>questions viva-ready</span></div>
        <button class="btn" id="cvAll">🎙️ Start viva — ${list.length} questions</button></div>
      <div class="card"><h3 class="ca-h3">Questions</h3><ol class="ca-vlist">${list.map((v, i) => `<li><button class="ca-vrow" data-i="${i}"><span>${esc(v.q)}</span><small class="ca-qmk">${vivaMax(v)} marks</small>${best[i] == null ? '<em class="ca-band">Not tried</em>' : `<em class="ca-band ${best[i] >= 80 ? 's' : best[i] >= 50 ? 'm' : 'w'}">${best[i] >= 80 ? '✓ ' : ''}Best ${vivaBestMarks(uid, v)}/${vivaMax(v)}</em>`}</button></li>`).join('')}</ol></div>`;
    D.getElementById('cvAll').onclick = () => vivaRun(P, list.map(v => ({ uid, v, title: d.title })), { back: () => vivaTab(P, uid, d) });
    P.querySelectorAll('.ca-vrow').forEach(b => b.onclick = () => vivaRun(P, [{ uid, v: list[+b.dataset.i], title: d.title }], { back: () => vivaTab(P, uid, d) }));
  }
  /* ---------- voice input: robust against Android Chrome's cumulative / repeated results ----------
     Android sends each result again and again as it grows ("an agreement", "an agreement when", …), sometimes as new
     result indexes, sometimes re-finalised, and it restarts the session after every pause. So the transcript is rebuilt
     from FINAL results only (kept per result index from event.resultIndex on), consecutive pieces are merged by removing
     overlapping words, each session is merged into the committed text when it ends, and interim words are only shown
     (greyed), never written into the answer. */
  const wnorm = w => w.toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');
  function speechMerge(a, b) {
    const A = String(a || '').trim().split(/\s+/).filter(Boolean), B = String(b || '').trim().split(/\s+/).filter(Boolean);
    if (!B.length) return A.join(' '); if (!A.length) return B.join(' ');
    const a2 = A.map(wnorm), b2 = B.map(wnorm), bs = b2.join(' ');
    if (B.length <= A.length && a2.slice(-(B.length + 2)).join(' ').includes(bs)) return A.join(' ');     // b repeats what we already have
    for (let s = 0; s < A.length; s++) { const k = A.length - s; if (k > B.length) continue; if (a2.slice(s).join(' ') === b2.slice(0, k).join(' ')) return A.slice(0, s).concat(B).join(' '); }   // overlap / cumulative
    return A.concat(B).join(' ');
  }
  let REC = null;
  function stopRec() { if (REC) { const r = REC; REC = null; r.want = false; try { r.stop(); } catch (e) {} } }
  D.addEventListener('sv:back', () => { stopRec(); hush(); });
  function vivaMax(v) { return v.points.reduce((a, p) => a + p.w, 0); }
  function vivaRun(host, items, opts = {}) {
    let i = 0; const results = []; let hide = false;
    if (opts.back && window.Nav) Nav.sub(() => { stopRec(); hush(); opts.back(); });
    const render = () => {
      stopRec(); hush();
      const { uid, v, title } = items[i]; let secs = 0, timer = null, mode = 'say', photosNow = [];
      const max = vivaMax(v);
      host.innerHTML = `<div class="card ca-viva"><div class="ca-mtop"><span class="ca-k">Viva · question ${i + 1} of ${items.length} · ${max} marks</span><span class="ca-timer" id="cvT" aria-label="Time">00:00</span></div>
          <p class="ca-vunit">${esc(title)}</p>
          <h2 class="ca-vq" id="cvQ" ${hide ? 'hidden' : ''}>${esc(v.q)} <span class="ca-qmk">(${max} marks)</span></h2><p class="ca-vhid" id="cvQh" ${hide ? '' : 'hidden'}>🎧 Listening mode — the question is hidden. Tap “Hear question” to replay it.</p>
          <div class="ca-btns">${speakOK() ? '<button class="btn ghost" id="cvSay">🔊 Hear question</button>' : ''}<button class="btn ghost" id="cvHide" aria-pressed="${hide}">${hide ? '👁 Show text' : '🙈 Hide text'}</button></div>
          <div class="ca-amode" role="radiogroup" aria-label="How will you answer?"><button role="radio" aria-checked="true" data-mode="say">${SR ? '🎙️ Speak or type' : '✍️ Type'}</button><button role="radio" aria-checked="false" data-mode="photo">📷 Photo of my answer</button></div>
          <div id="cvSayBox">
          ${SR ? `<button class="ca-micb" id="cvMic" aria-pressed="false"><span class="ca-micdot" aria-hidden="true">🎙️</span><span id="cvMicL">Tap and answer out loud</span></button>` : ''}
          <p class="ca-note" id="cvMicSt" role="status" aria-live="polite">${SR ? 'Speak naturally — technical words are matched with synonyms and stems. Your words appear below; correct them if needed.' : 'Voice input is not available in this browser. Type your answer.'}</p>
          <label class="ca-lab" for="cvA">Your answer</label><textarea id="cvA" class="ca-ta ca-vta" rows="5" placeholder="${SR ? 'Your spoken answer appears here — or type it' : 'Type your answer as you would say it in a viva'}"></textarea>
          <p class="ca-interim" id="cvInt" aria-hidden="true"></p>
          <button class="btn" id="cvCheck">Check my marks ▶</button></div>
          <div id="cvPhotoBox" hidden></div><button class="btn" id="cvPhCheck" hidden>Save photo ▶</button></div><div id="cvRes"></div>`;
      const ta = D.getElementById('cvA'), st = D.getElementById('cvMicSt'), intEl = D.getElementById('cvInt');
      const tick = () => { secs++; const t = D.getElementById('cvT'); if (!t) { clearInterval(timer); return; } t.textContent = secsTxt(secs); };
      const startT = () => { if (!timer) timer = setInterval(tick, 1000); };
      const stopT = () => { clearInterval(timer); timer = null; };
      const ask = () => { if (speakOK()) { stopRec(); sayQ(v.q); } startT(); };
      if (D.getElementById('cvSay')) D.getElementById('cvSay').onclick = ask;
      D.getElementById('cvHide').onclick = () => { hide = !hide; D.getElementById('cvQ').hidden = hide; D.getElementById('cvQh').hidden = !hide; const b = D.getElementById('cvHide'); b.setAttribute('aria-pressed', String(hide)); b.textContent = hide ? '👁 Show text' : '🙈 Hide text'; if (hide) ask(); };
      host.querySelectorAll('.ca-amode [data-mode]').forEach(b => b.onclick = () => {
        mode = b.dataset.mode; host.querySelectorAll('.ca-amode [data-mode]').forEach(x => x.setAttribute('aria-checked', String(x === b))); stopRec();
        D.getElementById('cvSayBox').hidden = mode === 'photo'; const pb = D.getElementById('cvPhotoBox'); pb.hidden = mode !== 'photo'; D.getElementById('cvPhCheck').hidden = mode !== 'photo';
        if (mode === 'photo' && !pb.dataset.on) { pb.dataset.on = 1; photos.picker(pb, `${uid}#${v.id}`, l => { photosNow = l; startT(); }); }
      });
      let how = 'type', S = null;          // S = live speech state
      ta.oninput = () => { startT(); if (S) { S.base = ta.value.replace(/\s*$/, ' '); S.committed = ''; S.finals = {}; S.ignoreBelow = S.len; intEl.textContent = ''; } };
      const mic = D.getElementById('cvMic');
      if (mic) mic.onclick = () => {
        if (REC) { stopRec(); return; }
        hush(); try { window.A11Y && A11Y.stopRec && A11Y.stopRec(); } catch (e) {}
        const android = /android/i.test(navigator.userAgent);
        S = { base: ta.value ? ta.value.replace(/\s*$/, ' ') : '', committed: '', finals: {}, len: 0, ignoreBelow: 0, restarts: 0, empty: 0, got: false };
        const ui = on => { if (!D.getElementById('cvMic')) return; mic.classList.toggle('on', on); mic.setAttribute('aria-pressed', String(on)); D.getElementById('cvMicL').textContent = on ? 'Listening… tap to stop' : 'Tap and answer out loud'; if (!on) intEl.textContent = ''; };
        const sessionText = () => Object.keys(S.finals).map(Number).sort((a, b) => a - b).reduce((acc, k) => speechMerge(acc, S.finals[k]), '');
        const startSession = () => {
          let r; try { r = new SR(); } catch (e) { st.textContent = 'Voice input could not start. Please type your answer.'; return false; }
          REC = r; r.want = true; r.lang = 'en-IN'; r.continuous = !android; r.interimResults = true; r.maxAlternatives = 1; S.finals = {}; S.len = 0; S.ignoreBelow = 0; S.got = false;
          r.onresult = e => {
            if (REC !== r || !D.getElementById('cvA')) return;
            S.len = e.results.length; let interim = '';
            for (let k = Math.max(e.resultIndex || 0, S.ignoreBelow); k < e.results.length; k++) { const res = e.results[k], tx = (res[0] && res[0].transcript || '').trim(); if (!tx) continue;
              if (res.isFinal) S.finals[k] = tx; else interim = speechMerge(interim, tx); }
            const full = speechMerge(S.committed, sessionText());
            ta.value = (S.base + full).replace(/\s+/g, ' ').trimStart(); how = 'voice'; S.got = true; startT();
            const extra = speechMerge(full, interim), fw = full.split(/\s+/).filter(Boolean).length;
            intEl.textContent = interim ? extra.split(/\s+/).slice(fw).join(' ') : '';
          };
          r.onerror = e => { if (e.error === 'not-allowed' || e.error === 'service-not-allowed') { r.want = false; st.textContent = 'Microphone permission was refused — you can type your answer instead.'; } else if (e.error === 'network') { r.want = false; st.textContent = 'Voice recognition needs a connection in this browser. Type your answer instead — checking still works offline.'; } else if (e.error === 'no-speech') S.empty++; };
          r.onend = () => {
            if (REC !== r) return;
            S.committed = speechMerge(S.committed, sessionText()); S.finals = {}; S.len = 0; S.ignoreBelow = 0;   // commit this session once
            if (!S.got) S.empty++; else S.empty = 0;
            if (r.want && S.restarts++ < 60 && S.empty < 3 && D.getElementById('cvA')) { setTimeout(() => { if (REC === r && r.want) startSession(); }, android ? 120 : 60); return; }
            REC = null; ui(false); if (S.empty >= 3) st.textContent = 'Stopped listening after a long pause. Tap the mic to continue.';
          };
          try { r.start(); return true; } catch (e) { REC = null; st.textContent = 'Voice input could not start. Please type your answer.'; return false; }
        };
        if (startSession()) { ui(true); st.textContent = 'Listening… speak your answer. Tap the mic again when you finish.'; startT(); tap('tap'); }
      };
      const finish = (rec, hitIds) => {
        const c = C(), key = `${uid}#${v.id}`, h = c.viva[key] = c.viva[key] || []; h.push(rec);
        while (h.length > 5) { const old = h.shift(); (old.photos || []).forEach(x => photos.del(x.id)); }
        if ((rec.photos || []).length) photos.keep(rec.photos.map(x => x.id));
        save(); try { bumpStreak(); addXP(Math.max(3, Math.round(rec.pct / 10))); } catch (e) {}
        results[i] = { uid, v, pct: rec.pct, marks: rec.marks, max };
        const ok = rec.pct >= 80;
        D.getElementById('cvRes').innerHTML = `<div class="card ca-vres ${ok ? 'ok' : ''}"><div class="ca-vhead">${X.ring(rec.pct / 100, 64, `${rec.marks} of ${max} marks`)}<div><h2 class="ca-h2s">You scored ${fmt(rec.marks)}/${max} marks</h2><p class="sub">${ok ? '✓ Viva-ready (80% or more)' : rec.pct >= 50 ? 'Good start — fill the gaps' : 'Keep going — revise the missed points'}${secs ? ` · ${secsTxt(secs)}` : ''}</p></div></div>
            ${(rec.photos || []).length ? '<div class="ca-phstrip" id="cvPhStrip"></div>' : ''}
            <h3 class="ca-h3">Key points</h3><ul class="ca-kp">${v.points.map(p => { const hit = hitIds.includes(p.id); return `<li class="${hit ? 'hit' : 'miss'}"><span aria-hidden="true">${hit ? '✓' : '✗'}</span><span class="sr-only">${hit ? 'Covered:' : 'Missed:'}</span> ${esc(p.pt)} <em>${hit ? p.w : 0}/${p.w}</em></li>`; }).join('')}</ul>
            <h3 class="ca-h3">Model answer</h3><p class="ca-p ca-vmodel">${esc(v.model)}</p>
            <div class="ca-btns">${speakOK() ? '<button class="btn ghost" id="cvHear">🔊 Hear model answer</button>' : ''}<button class="btn ghost" id="cvAgain">↻ Answer again</button><button class="btn" id="cvNext">${i < items.length - 1 ? 'Next question ▶' : 'Finish ▶'}</button></div>
            <p class="ca-note">Checked on this device: words are compared by stem, with synonyms, number tolerance and negation (“not”, “never” …). It checks coverage of the key points, not grammar or delivery.</p></div>`;
        if (D.getElementById('cvPhStrip')) photos.strip(D.getElementById('cvPhStrip'), rec.photos);
        say(`${rec.marks} out of ${max} marks. ${ok ? 'Viva ready.' : ''}`);
        if (D.getElementById('cvHear')) D.getElementById('cvHear').onclick = () => sayQ(v.model);
        D.getElementById('cvAgain').onclick = () => render();
        D.getElementById('cvNext').onclick = () => { hush(); i++; if (i < items.length) { render(); window.scrollTo(0, 0); } else summary(); };
        D.getElementById('cvRes').scrollIntoView({ behavior: 'smooth', block: 'start' }); D.getElementById('cvNext').focus({ preventScroll: true });
      };
      D.getElementById('cvCheck').onclick = () => {
        stopRec(); stopT(); hush(); intEl.textContent = '';
        const ans = ta.value.trim();
        if (!ans) { toast('Say or type an answer first'); ta.focus(); return; }
        const r = vivaScore(v, ans), marks = v.points.filter(p => r.hit.includes(p.id)).reduce((a, p) => a + p.w, 0);
        finish({ d: today(), pct: r.pct, marks, max, hit: r.hit, secs, how, text: ans.slice(0, 2000) }, r.hit);
      };
      D.getElementById('cvPhCheck').onclick = () => {   // students do not mark themselves: a photo waits for the AI examiners
        if (!photosNow.length) { toast('Add a photo of your answer first'); return; }
        stopT(); const c = C(), key = `${uid}#${v.id}`, h = c.viva[key] = c.viva[key] || [];
        h.push({ d: today(), pct: null, marks: null, max, hit: [], secs, how: 'photo', text: '', status: 'waiting', photos: photosNow.map(x => ({ id: x.id, w: x.w, h: x.h, bytes: x.bytes })) });
        while (h.length > 5) { const old = h.shift(); (old.photos || []).forEach(x => photos.del(x.id)); }
        photos.keep(photosNow.map(x => x.id)); save();
        D.getElementById('cvRes').innerHTML = `<div class="ca-cmp"><aside class="ca-cmp-ph" aria-label="Photos of your answer"><div class="ca-k">Your answer — tap to zoom</div><div class="ca-phstrip" id="cvPhS"></div></aside><div class="ca-cmp-main"><div class="card ca-rep ca-rep-wait"><div class="ca-rep-top"><span class="ca-rep-big" aria-hidden="true">📷</span><div><h2 class="ca-h2s">Photo saved — not marked</h2><p class="sub">Handwriting can't be read automatically, so a photo alone gets no score.</p></div></div>
          <p class="ca-p">Want marks now? Switch to “Speak or type” and say or type the same answer — it is checked at once.</p>
          <h3 class="ca-h3">Key points the examiners look for</h3><ul class="ca-ul">${v.points.map(p => `<li>${esc(p.pt)} <em class="ca-qmk">${mk1(p.w)}</em></li>`).join('')}</ul>
          <details class="ca-given"><summary>Model answer</summary><p class="ca-p">${esc(v.model)}</p></details>
          <div class="ca-btns"><button class="btn" id="cvPNext">${i < items.length - 1 ? 'Next question ▶' : 'Finish ▶'}</button></div></div></div></div>`;
        photos.strip(D.getElementById('cvPhS'), photosNow); say('Saved. To get a score, say or type the same answer.');
        D.getElementById('cvPNext').onclick = () => { hush(); i++; if (i < items.length) { render(); window.scrollTo(0, 0); } else summary(); };
        D.getElementById('cvRes').scrollIntoView({ behavior: 'smooth', block: 'start' });
      };
      if (speakOK() && opts.autoRead !== false) setTimeout(() => { if (D.getElementById('cvQ')) ask(); }, 350);
    };
    const summary = () => {
      const done = results.filter(Boolean), got = done.reduce((a, r) => a + r.marks, 0), mx = done.reduce((a, r) => a + r.max, 0);
      host.innerHTML = `<div class="card ca-res"><span class="ca-k">Viva finished</span><h2 class="ca-h2s">You scored ${fmt(got)}/${mx} marks</h2><p class="sub">${done.filter(r => r.pct >= 80).length} of ${done.length} answers viva-ready (80%+).</p>
        <ul class="ca-kp">${done.map(r => `<li class="${r.pct >= 80 ? 'hit' : 'miss'}"><span aria-hidden="true">${r.pct >= 80 ? '✓' : '✗'}</span> ${esc(r.v.q)} <em>${fmt(r.marks)}/${r.max}</em></li>`).join('')}</ul>
        <div class="ca-btns"><button class="btn ghost" id="cvRe">↻ Again</button><button class="btn" id="cvBack">Done</button></div></div>`;
      D.getElementById('cvRe').onclick = () => vivaRun(host, items, opts);
      D.getElementById('cvBack').onclick = () => (window.Nav && opts.back ? history.back() : (opts.back || practiceHub)());
    };
    render();
  }
  async function vivaHub() {
    const el = X.open('practice'); const list = await loadAll(await builtList()); const withV = list.filter(b => (b.d.viva || []).length);
    el.innerHTML = ''; el.appendChild(back('Practice', practiceHub));
    el.insertAdjacentHTML('beforeend', `<h1 class="ca-h1 ca-onDark">🎙️ Viva — speak &amp; revise</h1>
      <div class="card"><p class="ca-p">Hear an ICAI-style question, answer out loud, and see the key points you covered and missed — with the model answer.</p>
        <label class="ca-lab" for="cvU">Unit</label><select id="cvU" class="ca-in"><option value="__mix">Mixed — weakest and untried first</option>${withV.map(b => `<option value="${b.u.id}">${esc(X.paperLabel(b.p))} · Ch ${b.c.n} · ${esc(b.u.title)}</option>`).join('')}</select>
        <label class="ca-lab" for="cvN">Questions</label><select id="cvN" class="ca-in"><option>3</option><option selected>5</option><option>10</option></select>
        <button class="btn" id="cvGo">Start viva ▶</button></div><div id="cvHost"></div>`);
    D.getElementById('cvGo').onclick = () => {
      const u = D.getElementById('cvU').value, n = +D.getElementById('cvN').value;
      let items = [];
      withV.forEach(b => { if (u === '__mix' || b.u.id === u) b.d.viva.forEach(v => items.push({ uid: b.u.id, v, title: b.u.title, best: vivaBest(b.u.id, v.id) })); });
      items = u === '__mix' ? shuffle(items).sort((a, b) => (a.best ?? -1) - (b.best ?? -1)) : items;
      items = items.slice(0, n); const host = D.getElementById('cvHost'); el.querySelector('.card').remove();
      vivaRun(host, items, { back: vivaHub });
    };
  }

  /* ================= 3. MCQ builder · runner · results · revise ================= */
  const reviseMark = (key, ok) => { const r = C().revise; if (ok) { if (r[key]) { delete r[key]; save(); } } else { r[key] = { d: today(), n: (r[key]?.n || 0) + 1 }; save(); } };
  let B = null;   // builder draft (kept for the session)
  async function builder(preset = {}) {
    const el = X.open('practice'), all = await builtList();
    const levels = X.LEVELS.map(([k, n]) => ({ k, n, n_b: all.filter(b => b.level === k).length }));
    B = B && !preset.reset ? B : { level: (levels.find(l => l.k === C().level && l.n_b) || levels.find(l => l.n_b) || levels[0]).k, papers: [], chapters: [], diff: ['core', 'moderate', 'hard'], count: 10, timer: 'off', custom: 45, mode: 'practice', singles: true, cases: true };
    Object.assign(B, preset); delete B.reset;
    const draw = async () => {
      const inL = all.filter(b => b.level === B.level);
      const papers = [...new Map(inL.map(b => [b.p.id, b.p])).values()];
      if (!B.papers.length || !B.papers.every(id => papers.some(p => p.id === id))) B.papers = papers.map(p => p.id);
      const chs = [...new Map(inL.filter(b => B.papers.includes(b.p.id)).map(b => [b.c.id, { c: b.c, p: b.p }])).values()];
      B.chapters = B.chapters.filter(id => chs.some(x => x.c.id === id)); if (!B.chapters.length) B.chapters = chs.map(x => x.c.id);
      const pool = await poolFor(inL);
      const avail = pool.reduce((a, bl) => a + bl.items.length, 0);
      const seg = (name, key, opts, multi) => `<fieldset class="ca-fs"><legend>${name}</legend><div class="ca-chipsel">${opts.map(o => { const on = key === 'inc' ? !!B[o.v] : multi ? B[key].includes(o.v) : B[key] === o.v; return `<button type="button" class="ca-cs" ${multi ? `aria-pressed="${on}"` : `role="radio" aria-checked="${on}"`} data-k="${key}" data-v="${esc(o.v)}" ${o.dis ? 'disabled' : ''}>${esc(o.n)}${o.sub ? `<small>${esc(o.sub)}</small>` : ''}</button>`; }).join('')}</div></fieldset>`;
      el.innerHTML = '';
      el.appendChild(back('Practice', practiceHub));
      el.insertAdjacentHTML('beforeend', `<h1 class="ca-h1 ca-onDark">Build an MCQ set</h1><div class="card ca-builder">
        ${seg('1 · Level', 'level', levels.map(l => ({ v: l.k, n: 'CA ' + l.n, dis: !l.n_b, sub: l.n_b ? '' : 'soon' })), false)}
        ${seg('2 · Papers', 'papers', papers.map(p => ({ v: p.id, n: `${X.paperLabel(p)} · ${p.name}` })), true)}
        ${seg('3 · Chapters', 'chapters', chs.map(x => ({ v: x.c.id, n: `${X.paperLabel(x.p).replace('Paper ', 'P')} Ch ${x.c.n}: ${x.c.title}` })), true)}
        ${seg('4 · Difficulty', 'diff', DIFF.map(([v, n]) => ({ v, n })), true)}
        ${seg('Include', 'inc', [{ v: 'singles', n: 'Single MCQs' }, { v: 'cases', n: 'Case-study sets', sub: 'a short case + linked MCQs' }], true)}
        ${seg('5 · Number of questions', 'count', [5, 10, 20, 30].map(n => ({ v: n, n: String(n) })), false)}
        ${seg('6 · Timer', 'timer', [{ v: 'off', n: 'Off' }, { v: '60', n: '60 s per question' }, { v: 'custom', n: 'Custom' }], false)}
        <div id="cbCustom" ${B.timer === 'custom' ? '' : 'hidden'}><label class="ca-lab" for="cbSec">Seconds per question (15–300)</label><input id="cbSec" class="ca-in" type="number" min="15" max="300" step="5" value="${B.custom}" inputmode="numeric"></div>
        ${seg('7 · Mode', 'mode', [{ v: 'practice', n: 'Practice', sub: 'instant feedback' }, { v: 'test', n: 'Test', sub: 'review at the end' }], false)}
        <p class="ca-avail" role="status">${avail} question${avail === 1 ? '' : 's'} match your choices${avail < B.count ? ` — the set will have ${avail}` : ''}.</p>
        <button class="btn" id="cbGo" ${avail ? '' : 'disabled'}>Start ${Math.min(avail, B.count)} questions ▶</button></div>`);
      el.querySelectorAll('.ca-cs').forEach(b => b.onclick = () => {
        const k = b.dataset.k; let v = b.dataset.v; if (k === 'count') v = +v;
        if (k === 'inc') { B[v] = !B[v]; if (!B.singles && !B.cases) B[v === 'singles' ? 'cases' : 'singles'] = true; }
        else if (Array.isArray(B[k])) { const s = new Set(B[k]); s.has(v) ? s.delete(v) : s.add(v); if (!s.size) { toast('Keep at least one selected'); return; } B[k] = [...s]; }
        else { B[k] = v; if (k === 'level') { B.papers = []; B.chapters = []; } if (k === 'papers') B.chapters = []; }
        tap('tap'); draw();
      });
      const cs = D.getElementById('cbSec'); if (cs) cs.onchange = () => { B.custom = Math.max(15, Math.min(300, +cs.value || 45)); cs.value = B.custom; };
      D.getElementById('cbGo').onclick = () => { const set = pickSet(pool, B.count, 'builder:' + B.level); startSet(set, { mode: B.mode, perQ: B.timer === 'off' ? 0 : B.timer === '60' ? 60 : B.custom, title: 'Custom MCQ set', again: () => builder() }); };
    };
    draw();
  }
  async function poolFor(inL) {
    const blocks = [];
    for (const b of inL) {
      if (!B.papers.includes(b.p.id) || !B.chapters.includes(b.c.id)) continue;
      const d = await X.unitData(b.u.id); if (!d) continue;
      const meta = { uid: b.u.id, ch: b.c.id, chTitle: `Ch ${b.c.n}: ${b.c.title}`, unitTitle: b.u.title, paper: b.p };
      if (B.singles) d.mcqs.filter(q => B.diff.includes(q.difficulty || 'core')).forEach(q => blocks.push({ items: [{ q, key: `${b.u.id}#${q.id}`, ...meta }] }));
      if (B.cases) (d.cases || []).forEach(cs => { if (B.diff.includes(cs.difficulty) || cs.mcqs.some(m => B.diff.includes(m.difficulty))) blocks.push({ cs, items: cs.mcqs.map(q => ({ q, key: `${b.u.id}#${q.id}`, cs, ...meta })) }); });
    }
    return blocks;
  }
  /* fresh sets: unseen questions first, the ones answered wrong come back sooner, recently right ones later,
     options are shuffled per attempt, and the same set is never served twice in a row (C().lastSets) */
  function lastOk(key) { const l = C().mlog || []; for (let i = l.length - 1; i >= 0; i--) if (l[i][1] === key) return !!l[i][2]; return null; }
  function priority(key) { const r = C().mcq[key]; if (!r) return 3 + Math.random(); const lo = lastOk(key); return (lo === false ? 2.2 : 0) + r.w * .4 - Math.min(r.s, 4) * .35 + Math.random() * 1.4; }
  function sig(items) { return items.map(it => it.key).sort().join(',') + '|' + items.map(it => it.key).join(','); }
  function freshOrder(list, tag) {
    const c = C(); c.lastSets = c.lastSets || {}; const prev = c.lastSets[tag]; let out, k = 0;
    do { out = list.map(x => [priority(x.key), x]).sort((a, b) => b[0] - a[0]).map(x => x[1]); } while (prev && out.length > 1 && sig(out) === prev && ++k < 6);
    if (prev && out.length > 1 && sig(out) === prev) out = out.slice(1).concat(out[0]);
    c.lastSets[tag] = sig(out); save(); return out;
  }
  function genItems(units, n, diff) {      // numeric variants from js/ca-gen.js (another module), when present
    if (!window.CAGen || !n) return [];
    try {
      const ids = units.filter(u => { try { return CAGen.has(u.uid); } catch (e) { return false; } }); if (!ids.length) return [];
      const raw = CAGen.mix(ids.map(u => u.uid), n, { difficulty: diff }) || [];
      return raw.filter(g => g && g.q && Array.isArray(g.options) && g.options.length >= 2 && g.answer != null).map((g, i) => { const u = ids.find(x => x.uid === g.unit || x.uid === g.uid) || ids[i % ids.length];
        return { q: g, key: `${u.uid}#gen-${g.id || Date.now().toString(36) + i}`, gen: true, uid: u.uid, ch: u.ch, chTitle: u.chTitle, unitTitle: u.unitTitle, paper: u.paper }; });
    } catch (e) { console.warn('CAGen failed', e); return []; }
  }
  function pickSet(pool, n, tag = 'builder') {
    const c = C(); c.lastSets = c.lastSets || {}; const prev = c.lastSets[tag];
    const metas = [...new Map(pool.flatMap(bl => bl.items).map(it => [it.uid, it])).values()];
    const gen = window.CAGen ? genItems(metas, Math.min(Math.round(n * .3), Math.max(0, n - 1)), B && B.diff && B.diff.length === 1 ? B.diff[0] : undefined) : [];
    const room = n - gen.length; let out, k = 0;
    do {
      const order = pool.map(bl => [bl.items.reduce((a, it) => a + priority(it.key), 0) / bl.items.length + (bl.cs ? .3 : 0), bl]).sort((a, b) => b[0] - a[0]).map(x => x[1]);
      const blocks = []; let m = 0;
      for (const bl of order) { if (m + bl.items.length <= room) { blocks.push(bl); m += bl.items.length; } if (m >= room) break; }
      out = shuffle(blocks).flatMap(bl => bl.items);
    } while (prev && sig(out) === prev && ++k < 6);
    if (gen.length) out = shuffle(out.concat(gen)).slice(0, n);
    c.lastSets[tag] = sig(out); save(); return out;
  }
  const cgRecord = (key, ok) => { try { if (window.CAGen && CAGen.record) CAGen.record(key, ok); } catch (e) {} };
  const stepsHTML = q => (q.steps || []).length ? `<ol class="ca-steps">${q.steps.map(x => `<li>${esc(x)}</li>`).join('')}</ol>` : '';
  /* ♾️ Endless practice for one unit: generated questions (js/ca-gen.js) with steps and marks; Previous / Next */
  function endless(P, uid, d, back) {
    if (window.Nav) Nav.sub(() => { if (P.isConnected) back(); else Ca.unit(uid, 'mcq'); });
    const hist = []; let at = -1, diff = 'core', right = 0, done = 0;
    const own = shuffle(d.mcqs);
    const next = () => {
      let q = null;
      try { if (window.CAGen && CAGen.has(uid)) q = CAGen.next(uid, { difficulty: diff }); } catch (e) { q = null; }
      if (!q || !q.q || !Array.isArray(q.options)) { const pool = own.filter(x => (x.difficulty || 'core') === diff); const src = pool.length ? pool : own; q = src[(hist.length) % src.length]; }
      return { q, ord: X.order(q.options.length, 'e' + Date.now() + hist.length), pick: null };
    };
    const draw = () => {
      const h = hist[at], q = h.q, locked = h.pick != null;
      P.innerHTML = `<div class="card ca-mcq ca-endless"><div class="ca-mtop"><span class="ca-k">♾️ Endless practice · question ${at + 1} · <span class="ca-qmk">${mk1(qm(q))}</span></span><span class="ca-k">${right}/${done} correct</span></div>
        <div class="ca-chipsel" role="radiogroup" aria-label="Difficulty">${DIFF.map(([k, n]) => `<button type="button" class="ca-cs" role="radio" aria-checked="${k === diff}" data-df="${k}">${n}</button>`).join('')}</div>
        <h2 class="qtext ca-mq">${esc(q.q)}</h2>${q.given ? X.blocks(q.given) : ''}<div class="ca-opts">${h.ord.map((k, j) => `<button class="opt ${locked && k === q.answer ? 'right' : ''} ${locked && k === h.pick && k !== q.answer ? 'wrong' : ''}" data-k="${k}" ${locked ? 'disabled' : ''}><span class="ca-ol">${'ABCD'[j]}</span> ${esc(q.options[k])}</button>`).join('')}</div>
        <div id="enFb">${locked ? `<div class="explain ${h.pick === q.answer ? 'good' : 'bad'}"><div class="verdict">${h.pick === q.answer ? `Correct · +${mk1(qm(q))}` : `Not quite — answer: ${esc(q.options[q.answer])}`}</div><div class="why">${esc(q.explain || '')}</div>${stepsHTML(q)}${X.refChip ? X.refChip(q.unit || uid, q) : ''}</div>` : ''}</div>
        <div class="ca-btns ca-setnav"><button class="btn ghost" id="enPrev" ${at ? '' : 'disabled'}>◀ Previous</button><button class="btn" id="enNext" ${locked ? '' : 'disabled'}>Next ▶</button></div>
        <button class="ca-link" id="enEnd">Stop practising</button></div>`;
      P.querySelectorAll('.opt').forEach(b => b.onclick = () => { h.pick = +b.dataset.k; done++; if (h.pick === q.answer) right++; if (q.key || q.gen) cgRecord(q.key || ('gen:' + q.gen + ':' + q.id), h.pick === q.answer); tap(h.pick === q.answer ? 'correct' : 'wrong'); draw(); D.getElementById('enNext').focus({ preventScroll: true }); });
      P.querySelectorAll('[data-df]').forEach(b => b.onclick = () => { diff = b.dataset.df; if (!locked) { hist[at] = next(); } draw(); });
      D.getElementById('enPrev').onclick = () => { at--; draw(); };
      D.getElementById('enNext').onclick = () => { at++; if (at >= hist.length) hist.push(next()); draw(); window.scrollTo(0, 0); };
      D.getElementById('enEnd').onclick = () => { if (window.Nav) history.back(); else back(); };
    };
    hist.push(next()); at = 0; draw();
  }
  /* topic reference: Paper › Chapter › Unit › Topic on every question, results grouped / filtered by paper, chapter, topic */
  const refOf = it => (X.refInfo ? X.refInfo(it.uid || it.q.unit || it.key, it.q) : { paper: '', ch: it.chTitle || '', topic: '', pn: '', chn: '' });
  const tagOf = it => { const r = refOf(it); return r.paper ? `${r.paper} · ${r.chn} · Topic: ${r.topic}` : (it.chTitle || ''); };
  const chipOf = it => (X.refChip ? X.refChip(it.uid || it.q.unit || it.key, it.q) : '');
  const grpKey = (r, g) => (g === 'p' ? r.ref.paper || '—' : g === 't' ? `${r.ref.topic || '—'}` : r.ref.pn ? `${r.ref.pn} · ${r.ref.ch}` : (r.it.chTitle || '—'));
  function filterOpts(res) {
    const o = []; const add = (k, lab) => { if (!o.some(x => x[0] === k)) o.push([k, lab]); };
    ['p', 'c', 't'].forEach(g => res.forEach(r => add(`${g}:${grpKey(r, g)}`, `${{ p: 'Paper', c: 'Chapter', t: 'Topic' }[g]}: ${grpKey(r, g)}`)));
    const byG = g => o.filter(x => x[0][0] === g);
    return ['p', 'c', 't'].map(g => byG(g).length > 1 || g === 't' ? `<optgroup label="${{ p: 'By paper', c: 'By chapter', t: 'By topic' }[g]}">${byG(g).map(([k, l]) => `<option value="${esc(k)}">${esc(l)}</option>`).join('')}</optgroup>` : '').join('');
  }
  function wireGroups(res) {
    const sel = D.getElementById('csGrp'), box = D.getElementById('csAcc'), fil = D.getElementById('csFil'); if (!sel || !box) return;
    const papers = new Set(res.map(r => r.ref.paper)); sel.value = papers.size > 1 ? 'p' : 'c';
    const draw = () => { const g = sel.value, m = new Map(); res.forEach(r => { const k = grpKey(r, g); const b = m.get(k) || { n: 0, r: 0 }; b.n++; if (r.ok) b.r++; m.set(k, b); });
      box.innerHTML = [...m.entries()].sort((a, b) => a[1].r / a[1].n - b[1].r / b[1].n).map(([k, b]) => `<div class="ca-skill"><span>${esc(k)} <small class="ca-note">${b.r}/${b.n}</small></span>${X.bar(b.r / b.n)}<b>${pct(b.r, b.n)}%</b></div>`).join(''); };
    sel.onchange = draw; draw();
    if (fil) fil.onchange = () => { const v = fil.value; let n = 0;
      D.querySelectorAll('.ca-rv[data-j]').forEach(d => { const r = res[+d.dataset.j]; const show = !v || (v === 'w' ? !r.ok : grpKey(r, v[0]) === v.slice(2)); d.hidden = !show; if (show) n++; });
      D.getElementById('csFilN').textContent = v ? `${n} question${n === 1 ? '' : 's'} shown` : ''; };
  }
  function startSet(items, opts) { if (window.Nav && opts.again) Nav.sub(() => opts.again()); const el = X.open('practice'); el.innerHTML = '<div id="csHost"></div>'; runSet(D.getElementById('csHost'), items, opts); }
  function runSet(host, items, opts) {
    const N = items.length, st = items.map(it => ({ pick: null, ms: 0, out: false, left: opts.perQ || 0, ord: X.order(it.q.options.length, 'b' + it.key + Date.now().toString(36).slice(-3)) }));
    let i = 0, t0 = Date.now(), tm = null; const started = Date.now(), test = opts.mode === 'test', graded = {};
    const leave = () => { if (test || !graded[i]) st[i].ms += Date.now() - t0; t0 = Date.now(); clearInterval(tm); tm = null; };
    const answered = s => s.pick != null || s.out;
    const render = () => {
      t0 = Date.now(); const it = items[i], s = st[i], q = it.q, locked = !test && answered(s);
      const caseHTML = it.cs ? `<details class="ca-case" ${i === 0 || items[i - 1].cs !== it.cs ? 'open' : ''}><summary>📄 Case: ${esc(it.cs.title)}</summary><p class="ca-p">${esc(it.cs.case)}</p>${X.blocks(it.cs.given)}</details>` : '';
      host.innerHTML = `<div class="card ca-mcq ca-set"><div class="ca-mtop"><span class="ca-k">${test ? 'Test' : 'Practice'} · Q ${i + 1} of ${N}</span>${opts.perQ ? `<span class="ca-timer" id="csT" role="timer" aria-label="Seconds left">${s.left}s</span>` : `<span class="ca-timer" id="csT" aria-hidden="true">${secsTxt((Date.now() - started) / 1000)}</span>`}</div>${X.bar(i / N)}
        ${test ? `<div class="ca-pal" role="group" aria-label="Question palette">${st.map((x, j) => `<button class="${j === i ? 'cur' : ''} ${answered(x) ? 'ans' : ''}" data-j="${j}" aria-label="Question ${j + 1}${answered(x) ? ', answered' : ''}">${j + 1}</button>`).join('')}</div>` : ''}
        ${caseHTML}<p class="ca-k ca-chtag">${esc(tagOf(it))} · ${esc(diffName(q.difficulty || 'core'))} · <span class="ca-qmk">${mk1(qm(q))}</span>${it.gen ? ' · <span class="ca-gentag">♾️ new variant</span>' : ''}</p>
        <h2 class="qtext ca-mq">${esc(q.q)}</h2><div class="ca-opts" role="group" aria-label="Options">${s.ord.map((k, j) => `<button class="opt ${test && s.pick === k ? 'sel' : ''}" data-k="${k}" ${test ? `aria-pressed="${s.pick === k}"` : ''} ${locked || (test && s.out) ? 'disabled' : ''}><span class="ca-ol">${'ABCD'[j]}</span> ${esc(q.options[k])}</button>`).join('')}</div>
        <div id="csFb"></div>
        <div class="ca-btns ca-setnav">${test ? `<button class="btn ghost" id="csPrev" ${i ? '' : 'disabled'}>◀ Previous</button>` : ''}${test || locked ? `<button class="btn" id="csNext">${i < N - 1 ? 'Next ▶' : test ? 'Finish test ✓' : 'See results ▶'}</button>` : ''}</div>
        ${test ? '<button class="ca-link" id="csEnd">Finish test now</button>' : ''}</div>`;
      if (locked) feedback();
      host.querySelectorAll('.opt').forEach(b => b.onclick = () => {
        const k = +b.dataset.k;
        if (test) { s.pick = k; host.querySelectorAll('.opt').forEach(x => { const on = +x.dataset.k === k; x.classList.toggle('sel', on); x.setAttribute('aria-pressed', String(on)); }); const pb = host.querySelector(`.ca-pal [data-j="${i}"]`); if (pb) pb.classList.add('ans'); tap('tap'); return; }
        s.pick = k; leave(); grade(i); tap(k === q.answer ? 'correct' : 'wrong'); render(); D.getElementById('csNext').focus({ preventScroll: true });
      });
      const nx = D.getElementById('csNext'); if (nx) nx.onclick = () => { leave(); i++; if (i < N) render(); else finish(); window.scrollTo(0, 0); };
      const pv = D.getElementById('csPrev'); if (pv) pv.onclick = () => { leave(); i--; render(); };
      const en = D.getElementById('csEnd'); if (en) en.onclick = () => { const un = st.filter(x => !answered(x)).length; if (un && !en.dataset.sure) { en.dataset.sure = 1; en.textContent = `${un} unanswered — tap again to finish`; return; } leave(); finish(); };
      host.querySelectorAll('.ca-pal button').forEach(b => b.onclick = () => { leave(); i = +b.dataset.j; render(); });
      if (opts.perQ && !(locked || (test && s.out))) tm = setInterval(() => {
        s.left--; const t = D.getElementById('csT'); if (!t) { clearInterval(tm); return; }
        t.textContent = `${Math.max(0, s.left)}s`; t.classList.toggle('over', s.left <= 10);
        if (s.left <= 0) { clearInterval(tm); s.out = true; tap('wrong'); say('Time is up for this question'); if (test) { leave(); i++; if (i < N) render(); else finish(); } else { leave(); grade(i); render(); } }
      }, 1000);
      else if (!opts.perQ) tm = setInterval(() => { const t = D.getElementById('csT'); if (!t) { clearInterval(tm); return; } t.textContent = secsTxt((Date.now() - started) / 1000); }, 1000);
    };
    const grade = j => { if (graded[j]) return; graded[j] = 1; const it = items[j], s = st[j], ok = s.pick === it.q.answer; if (it.gen) { if (s.pick != null) cgRecord(it.q.key || it.key, ok); return; } if (s.pick == null && !s.out) { reviseMark(it.key, false); return; } X.recordAns(it.key, ok, s.ms); reviseMark(it.key, ok); };
    const feedback = () => {
      const it = items[i], s = st[i], q = it.q, ok = s.pick === q.answer;
      host.querySelectorAll('.opt').forEach(x => { if (+x.dataset.k === q.answer) x.classList.add('right'); if (+x.dataset.k === s.pick && !ok) x.classList.add('wrong'); });
      D.getElementById('csFb').innerHTML = `<div class="explain ${ok ? 'good' : 'bad'}"><div class="verdict">${ok ? `Correct · +${mk1(qm(q))}` : s.out && s.pick == null ? `Time up — answer: ${esc(q.options[q.answer])}` : `Not quite — answer: ${esc(q.options[q.answer])}`}</div><div class="why">${esc(q.explain || '')}</div>${stepsHTML(q)}${chipOf(it)}</div>`;
    };
    const finish = () => {
      clearInterval(tm); if (test) items.forEach((_, j) => grade(j));
      const res = items.map((it, j) => ({ it, s: st[j], ok: st[j].pick === it.q.answer, skip: st[j].pick == null, ref: refOf(it) }));
      const right = res.filter(r => r.ok).length, wrong = res.filter(r => !r.ok && !r.skip).length, skip = res.filter(r => r.skip).length, ms = res.reduce((a, r) => a + r.s.ms, 0);
      const neg = items.some(it => /^fnd-p[34]-/.test(it.uid || it.key)), maxM = res.reduce((a, r) => a + qm(r.it.q), 0);
      const gotM = Math.round(res.reduce((a, r) => a + (r.ok ? qm(r.it.q) : !r.skip && neg ? -qm(r.it.q) / 4 : 0), 0) * 100) / 100;
      const byCh = {}; res.forEach(r => { const k = r.it.ch; const b = byCh[k] = byCh[k] || { t: r.it.chTitle, n: 0, r: 0 }; b.n++; if (r.ok) b.r++; });
      const c = C(); c.tests.push({ id: 't' + Date.now().toString(36), kind: 'mcq', d: today(), ts: Date.now(), title: opts.title || 'MCQ set', mode: opts.mode, n: N, right, wrong, skip, ms, pct: pct(right, N), marks: gotM, maxMarks: maxM, keys: items.map(it => it.key), byCh: Object.fromEntries(Object.entries(byCh).map(([k, v]) => [k, [v.n, v.r]])) });
      while (c.tests.length > 80) c.tests.shift(); save(); try { bumpStreak(); addXP(Math.max(5, right * 2)); } catch (e) {}
      const mx = Math.max(1, ...res.map(r => r.s.ms));
      host.innerHTML = `<div class="card ca-res ca-setres"><span class="ca-k">${esc(opts.title || 'MCQ set')} · ${test ? 'Test' : 'Practice'} mode</span><h2 class="ca-h2s">You scored ${fmt(gotM)} / ${mk1(maxM)}</h2><p class="sub">${right} of ${N} correct · ${pct(right, N)}%${neg ? ' · −¼ of the marks for each wrong answer, as in the exam' : ''}</p>
          <div class="ca-kpis"><div><b>${right}</b><span>Correct</span></div><div><b>${wrong}</b><span>Wrong</span></div><div><b>${skip}</b><span>Unanswered</span></div><div><b>${Math.round(ms / N / 1000)}s</b><span>Avg per Q</span></div></div>
          <p class="sub">Total time ${secsTxt(ms / 1000)}.${wrong + skip ? ` ${wrong + skip} question${wrong + skip > 1 ? 's' : ''} added to “Revise these”.` : ''}</p></div>
        <div class="card"><div class="ca-mtop"><h3 class="ca-h3">Accuracy by</h3><label class="sr-only" for="csGrp">Group results by</label><select id="csGrp" class="ca-in ca-rgsel"><option value="c">Chapter</option><option value="p">Paper</option><option value="t">Topic</option></select></div><div id="csAcc"></div></div>
        <div class="card"><h3 class="ca-h3">Time per question</h3><div class="ca-scroll" role="region" tabindex="0" aria-label="Time per question"><table class="ca-t ca-tpq"><thead><tr><th scope="col">Q</th><th scope="col">Chapter</th><th scope="col">Result</th><th scope="col" class="n">Seconds</th><th scope="col"><span class="sr-only">Bar</span></th></tr></thead><tbody>
          ${res.map((r, j) => `<tr><td>${j + 1}</td><td>${esc(r.ref.pn ? `${r.ref.pn.replace('Paper ', 'P')} · ${r.ref.chn}` : String(r.it.chTitle || '').replace(/^Ch (\d+):.*/, 'Ch $1'))}</td><td>${r.ok ? '✓ Correct' : r.skip ? '– Skipped' : '✗ Wrong'}</td><td class="n">${Math.round(r.s.ms / 1000)}</td><td class="ca-tbar"><i style="width:${Math.round(r.s.ms / mx * 100)}%" class="${r.ok ? 'ok' : 'no'}"></i></td></tr>`).join('')}</tbody></table></div></div>
        <div class="card"><div class="ca-mtop"><h3 class="ca-h3">Review with explanations</h3><label class="sr-only" for="csFil">Show questions from</label><select id="csFil" class="ca-in ca-rgsel"><option value="">All questions</option><option value="w">Wrong or skipped</option>${filterOpts(res)}</select></div><p class="ca-note" id="csFilN" role="status" aria-live="polite"></p>${res.map((r, j) => `<details class="ca-rv ${r.ok ? 'ok' : 'no'}" data-j="${j}" ${r.ok ? '' : 'open'}><summary><span aria-hidden="true">${r.ok ? '✓' : r.skip ? '–' : '✗'}</span> Q${j + 1} (${mk1(qm(r.it.q))}). ${esc(r.it.q.q)} <em class="ca-qmk">${r.ok ? qm(r.it.q) : 0}/${qm(r.it.q)}</em></summary>
          <p class="ca-note ca-rvtag">${esc(tagOf(r.it))}</p>${r.it.cs ? `<p class="ca-note">Case: ${esc(r.it.cs.title)}</p>` : ''}<p class="ca-p">Your answer: <b>${r.skip ? 'not answered' : esc(r.it.q.options[r.s.pick])}</b>${r.ok ? '' : `<br>Correct answer: <b>${esc(r.it.q.options[r.it.q.answer])}</b>`}</p><p class="ca-p ca-why">${esc(r.it.q.explain)}</p>${chipOf(r.it)}</details>`).join('')}</div>
        <div class="ca-btns"><button class="btn ghost" id="csRev">Revise these (${Object.keys(C().revise).length})</button><button class="btn" id="csAgain">${opts.againLabel || 'New set'}</button></div>`;
      wireGroups(res);
      say(`${right} of ${N} correct`);
      D.getElementById('csRev').onclick = revise;
      D.getElementById('csAgain').onclick = () => (opts.again || builder)();
      window.scrollTo(0, 0);
    };
    render();
  }
  async function revise() {
    const el = X.open('practice'); const keys = Object.keys(C().revise);
    const found = []; for (const k of keys) { const f = await findQ(k); if (f) found.push({ k, ...f }); else delete C().revise[k]; }
    const sts = {}; for (const f of found) { const st = await X.structure(X.levelOf(f.uid)); const x = X.findUnit(st, f.uid); if (x) sts[f.uid] = x; }
    el.innerHTML = ''; el.appendChild(back('Practice', practiceHub));
    el.insertAdjacentHTML('beforeend', `<h1 class="ca-h1 ca-onDark">Revise these</h1><div class="card"><p class="ca-p">${found.length ? `${found.length} question${found.length > 1 ? 's' : ''} you got wrong or ran out of time on. A question leaves this list when you answer it correctly.` : 'Nothing to revise — mistakes from any MCQ set appear here.'}</p>
      ${found.length ? '<button class="btn" id="crGo">Practise all ▶</button>' : '<button class="btn" id="crB">Build an MCQ set</button>'}</div>
      ${found.length ? `<div class="card"><ul class="ca-rvl">${found.map(f => `<li><span><b>${esc(f.q.q)}</b><small>${esc(sts[f.uid] ? `${X.paperLabel(sts[f.uid].p)} · Ch ${sts[f.uid].c.n} · ${sts[f.uid].u.title}` : f.uid)}${C().revise[f.k].n > 1 ? ` · missed ${C().revise[f.k].n}×` : ''}</small>${X.refChip ? X.refChip(f.uid, f.q) : ''}</span><button class="ca-x" data-k="${esc(f.k)}" aria-label="Remove from revise list">✕</button></li>`).join('')}</ul></div>` : ''}`);
    const g = D.getElementById('crGo'); if (g) g.onclick = () => startSet(freshOrder(found.map(f => ({ key: f.k, f })), 'revise').map(({ f }) => f).map(f => { const x = sts[f.uid]; return { q: f.q, key: f.k, uid: f.uid, cs: f.cs, ch: chOf(f.uid), chTitle: x ? `Ch ${x.c.n}: ${x.c.title}` : '' }; }), { mode: 'practice', perQ: 0, title: 'Revise these', again: revise, againLabel: 'Back to list' });
    const b = D.getElementById('crB'); if (b) b.onclick = () => builder();
    el.querySelectorAll('.ca-x[data-k]').forEach(x => x.onclick = () => { delete C().revise[x.dataset.k]; save(); revise(); });
  }
  function casesBlock(uid, d) {
    return `<div class="card ca-cases"><h2 class="ca-h2s">Case studies</h2><p class="sub">A short business case with linked questions — the way ICAI increasingly tests application.</p>
      ${d.cases.map((cs, i) => { const done = cs.mcqs.filter(m => C().mcq[`${uid}#${m.id}`]).length; return `<button class="ca-qrow ca-caserow" data-i="${i}"><span class="ca-qm">${cs.mcqs.length}<small>MCQs</small></span><span class="ca-qb"><b>${esc(cs.title)}</b><small>${esc(diffName(cs.difficulty))}${done ? ` · ${done}/${cs.mcqs.length} answered before` : ''}</small></span><span class="ca-chev" aria-hidden="true">›</span></button>`; }).join('')}</div>`;
  }
  function wireCases(P, uid, d) {
    P.querySelectorAll('.ca-caserow').forEach(b => b.onclick = async () => {
      const cs = d.cases[+b.dataset.i], st = await X.structure(X.levelOf(uid)), f = X.findUnit(st, uid);
      const host = D.getElementById('caMhost'); P.querySelectorAll(':scope > .card').forEach(x => x.remove());
      runSet(host, cs.mcqs.map(q => ({ q, key: `${uid}#${q.id}`, uid, cs, ch: chOf(uid), chTitle: `Ch ${f.c.n}: ${f.c.title}` })), { mode: 'practice', perQ: 0, title: 'Case study: ' + cs.title, again: () => Ca.unit(uid, 'mcq'), againLabel: 'Back to the unit' });
    });
  }

  /* ================= 4. MOCK PAPERS ================= */
  const MOCKS = { foundation: ['fnd-p1-m1'] };
  const mockCache = {};
  async function mockData(id) { if (!mockCache[id]) mockCache[id] = await loadJSON(`content/ca/foundation/mocks/${id}.json`); return mockCache[id]; }
  async function partQ(p) { if (p.kind === 'q') return p.question; if (p.kind === 'ref') { const [uid, qid] = p.ref.split('#'); const d = await X.unitData(uid); return d && d.questions.find(q => q.id === qid); } return null; }
  async function mocks() {
    const el = X.open('practice'); const list = []; for (const id of MOCKS.foundation) { try { list.push(await mockData(id)); } catch (e) {} }
    el.innerHTML = ''; el.appendChild(back('Practice', practiceHub));
    el.insertAdjacentHTML('beforeend', `<h1 class="ca-h1 ca-onDark">Mock papers</h1>${list.map(m => { const h = C().tests.filter(t => t.kind === 'mock' && t.mock === m.id), dr = C().mockDraft[m.id];
      return `<div class="card ca-mockc"><span class="ca-label">${esc(m.label)}</span><h2 class="ca-h2s">CA Foundation · Paper 1 · ${esc(m.title)}</h2>
        <div class="ca-chips"><span class="ca-chip">${m.marks} marks</span><span class="ca-chip">${m.hours} hours</span><span class="ca-chip">${m.questions.length} questions · answer ${m.compulsory.length + m.choose}</span></div>
        <p class="sub">${esc(m.scope)}</p><ul class="ca-ul">${m.rules.map(r => `<li>${esc(r)}</li>`).join('')}</ul>
        ${h.length ? `<p class="ca-p">Your attempts: ${h.slice(-3).reverse().map(t => `<b>${fmt(t.score)}/${t.max}</b> (${esc(t.d)})`).join(' · ')}</p>` : ''}
        <button class="btn" data-m="${m.id}">${dr ? `Resume (${secsTxt(dr.secs)} used) ▶` : 'Start the paper ▶'}</button>${dr ? `<button class="ca-link" data-new="${m.id}">Start again from a blank paper</button>` : ''}</div>`; }).join('')}
      <div class="card"><p class="ca-note">These are StudyVerse practice papers written in the pattern of ICAI's papers — they are not ICAI papers and are not endorsed by ICAI. Pilot scope: the chapters already built.</p></div>`);
    el.querySelectorAll('[data-m]').forEach(b => b.onclick = () => mockPaper(b.dataset.m));
    el.querySelectorAll('[data-new]').forEach(b => b.onclick = () => { delete C().mockDraft[b.dataset.new]; save(); mockPaper(b.dataset.new); });
  }
  async function mockPaper(id) {
    const el = X.open('practice'), m = await mockData(id), c = C();
    const dr = c.mockDraft[id] = c.mockDraft[id] || { secs: 0, ans: {}, tf: {}, chosen: [] };
    const qs = {}; for (const q of m.questions) for (const p of q.parts) if (p.kind !== 'tf') qs[`${q.id}${p.id}`] = await partQ(p);
    let cur = 0, tm = null;
    const limit = m.hours * 3600;
    const isComp = q => m.compulsory.includes(q.id);
    const attempting = q => isComp(q) || dr.chosen.includes(q.id);
    const hasAns = q => q.parts.some(p => p.kind === 'tf' ? p.items.some(it => dr.tf[it.id] && dr.tf[it.id].v != null) : (dr.ans[q.id + p.id] || '').trim());
    const store = () => { dr.secs = dr.secs || 0; save(); };
    const draw = () => {
      const q = m.questions[cur];
      el.innerHTML = `<div class="ca-mbar"><span class="ca-label">${esc(m.label)}</span><div class="ca-mrow"><b>${esc(m.title)}</b><span class="ca-timer" id="cmT" role="timer" aria-label="Time left">${secsTxt(limit - dr.secs)}</span><button class="btn ca-msub" id="cmSub">Submit</button></div>
          <div class="ca-pal" role="group" aria-label="Questions">${m.questions.map((x, j) => `<button class="${j === cur ? 'cur' : ''} ${hasAns(x) ? 'ans' : ''} ${attempting(x) ? 'att' : ''}" data-j="${j}" aria-label="${esc(x.id)}${isComp(x) ? ' compulsory' : attempting(x) ? ' attempting' : ''}${hasAns(x) ? ', answered' : ''}">${esc(x.id)}</button>`).join('')}</div></div>
        <div class="card ca-mq1"><div class="ca-mtop"><h2 class="ca-h2s">Question ${esc(q.id.slice(1))} <small>(${q.marks} marks)</small></h2>${isComp(q) ? '<span class="ca-chip">Compulsory</span>' : `<label class="ca-att"><input type="checkbox" id="cmAtt" ${attempting(q) ? 'checked' : ''}> Attempting (${dr.chosen.length}/${m.choose})</label>`}</div>
          ${q.parts.map(p => partHTML(q, p)).join('')}</div>
        <div class="ca-btns"><button class="btn ghost" id="cmPrev" ${cur ? '' : 'disabled'}>◀ ${cur ? esc(m.questions[cur - 1].id) : ''}</button><button class="btn ghost" id="cmNext" ${cur < m.questions.length - 1 ? '' : 'disabled'}>${cur < m.questions.length - 1 ? esc(m.questions[cur + 1].id) : ''} ▶</button></div>
        <button class="ca-link" id="cmLeave">Save and leave — resume later</button>`;
      el.querySelectorAll('.ca-pal button').forEach(b => b.onclick = () => { cur = +b.dataset.j; draw(); window.scrollTo(0, 0); });
      D.getElementById('cmPrev').onclick = () => { cur--; draw(); window.scrollTo(0, 0); };
      D.getElementById('cmNext').onclick = () => { cur++; draw(); window.scrollTo(0, 0); };
      D.getElementById('cmLeave').onclick = () => { clearInterval(tm); store(); mocks(); };
      const att = D.getElementById('cmAtt');
      if (att) att.onchange = () => { if (att.checked) { if (dr.chosen.length >= m.choose) { att.checked = false; toast(`Only ${m.choose} of the optional questions are marked — untick another first`); return; } dr.chosen.push(q.id); } else dr.chosen = dr.chosen.filter(x => x !== q.id); store(); draw(); };
      el.querySelectorAll('textarea[data-a]').forEach(t => t.oninput = () => { dr.ans[t.dataset.a] = t.value; if (!isComp(q) && !dr.chosen.includes(q.id) && dr.chosen.length < m.choose) { dr.chosen.push(q.id); const a = D.getElementById('cmAtt'); if (a) { a.checked = true; a.parentElement.lastChild.textContent = ` Attempting (${dr.chosen.length}/${m.choose})`; } } clearTimeout(t._s); t._s = setTimeout(store, 600); });
      el.querySelectorAll('[data-tf]').forEach(b => b.onclick = () => { const it = b.dataset.tf; dr.tf[it] = dr.tf[it] || {}; dr.tf[it].v = b.dataset.v === '1'; b.parentElement.querySelectorAll('button').forEach(x => { const on = x === b; x.setAttribute('aria-checked', String(on)); x.tabIndex = on ? 0 : -1; }); store(); });
      el.querySelectorAll('input[data-tfr]').forEach(t => t.oninput = () => { const it = t.dataset.tfr; dr.tf[it] = dr.tf[it] || {}; dr.tf[it].r = t.value; clearTimeout(t._s); t._s = setTimeout(store, 600); });
      D.getElementById('cmSub').onclick = function () {
        const opt = dr.chosen.length;
        if (!this.dataset.sure) { this.dataset.sure = 1; this.textContent = opt < m.choose ? `Only ${opt} of ${m.choose} chosen — submit?` : 'Tap again to submit'; setTimeout(() => { if (this.isConnected) { delete this.dataset.sure; this.textContent = 'Submit'; } }, 4000); return; }
        clearInterval(tm); store(); markPaper(m, dr, qs);
      };
    };
    const partHTML = (q, p) => {
      const head = `<div class="ca-mpart"><div class="ca-mph"><b>(${p.id})</b><em>${p.marks} marks</em></div>`;
      if (p.kind === 'tf') return `${head}<p class="ca-q">${esc(p.q)}</p><ol class="ca-tf">${p.items.map((it, k) => { const a = dr.tf[it.id] || {}; return `<li><p>${esc(it.s)}</p><div class="ca-seg" role="radiogroup" aria-label="Statement ${k + 1}: true or false">${[[1, 'True'], [0, 'False']].map(([v, n]) => `<button role="radio" data-tf="${it.id}" data-v="${v}" aria-checked="${a.v === !!v}" tabindex="${a.v === !!v || (a.v == null && v) ? 0 : -1}">${n}</button>`).join('')}</div><label class="sr-only" for="cmR${it.id}">Reason for statement ${k + 1}</label><input class="ca-in ca-tfr" id="cmR${it.id}" data-tfr="${it.id}" placeholder="Reason…" value="${esc(a.r || '')}" autocomplete="off"></li>`; }).join('')}</ol></div>`;
      const bq = qs[q.id + p.id]; if (!bq) return `${head}<p class="ca-note">This part could not be loaded.</p></div>`;
      return `${head}<p class="ca-q">${esc(bq.q)}</p>${bq.given ? `<details class="ca-given" open><summary>Given</summary>${X.blocks(bq.given)}</details>` : ''}
        <label class="ca-lab" for="cmA${q.id}${p.id}">Your answer to ${q.id}(${p.id})</label><textarea class="ca-ta" id="cmA${q.id}${p.id}" data-a="${q.id}${p.id}" rows="6" placeholder="Write the answer as in the exam — journal, ledger or table rows can be typed line by line">${esc(dr.ans[q.id + p.id] || '')}</textarea></div>`;
    };
    tm = setInterval(() => { dr.secs++; const t = D.getElementById('cmT'); if (!t) { clearInterval(tm); save(); return; } const left = limit - dr.secs; t.textContent = left >= 0 ? secsTxt(left) : '+' + secsTxt(-left); t.classList.toggle('over', left < 600); if (left === 0) { toast('Time is up — finish the line and submit'); say('Time is up'); } if (dr.secs % 30 === 0) save(); }, 1000);
    draw();
  }
  /* Marking a submitted paper — automatic, like the unit Write tab (js/ca-check.js): no self-marking.
     True/false: the verdict is checked, the reason is matched against the model reason's key points; 2 marks only when both are right. */
  function markPaper(m, dr, qs) {
    const el = X.open('practice'), K = window.CA, c = C();
    const qlist = m.questions.filter(q => m.compulsory.includes(q.id) || dr.chosen.includes(q.id));
    let html = '', total = 0, checked = 0, pend = 0; const wskills = [], refRecs = [];
    for (const q of qlist) {
      let qt = 0, qp = 0, body = '';
      for (const p of q.parts) {
        body += `<div class="ca-mpart"><div class="ca-mph"><b>(${p.id})</b><em>${p.marks} marks</em></div>`;
        if (p.kind === 'tf') {
          body += `<p class="ca-q">${esc(p.q)}</p><ol class="ca-tf">${p.items.map((it, k) => {
            const a = dr.tf[it.id] || {}, vOk = a.v === it.answer, rr = K ? K.tfReason(it, a.r) : { ok: false, how: 'none' }, got = vOk && rr.ok ? 2 : 0;
            qt += got; checked += 2;
            const vTxt = a.v == null ? '⚠️ No verdict given' : `${vOk ? '✅' : '❌'} You said ${a.v ? 'True' : 'False'} — verdict ${vOk ? 'correct' : 'wrong'}`;
            const rTxt = !(a.r || '').trim() ? '⚠️ No reason given — a bare True/False earns nothing' : rr.ok ? `✅ Your reason covers the key point${rr.how === 'overlap' ? ' (approximate check)' : ''}` : `❌ Your reason does not cover the key point${rr.how === 'overlap' && rr.key.length ? ` — look for: ${rr.key.filter(w => !rr.hits.includes(w)).slice(0, 4).join(', ')}` : ''}`;
            return `<li class="ca-tfm ${got ? 'ok' : 'no'}"><p>${esc(it.s)}</p><p class="ca-tfv ${vOk ? 'ok' : 'no'}">${vTxt}</p>${a.r ? `<p class="ca-note">Your reason: ${esc(a.r)}</p>` : ''}<p class="ca-tfv ${rr.ok ? 'ok' : 'no'}">${rTxt}</p>
              <p class="ca-p"><b>Model:</b> ${esc(it.reason)}</p><p class="ca-tfmk"><b>${got} / 2 marks</b>${got ? '' : vOk ? ' — the verdict alone earns no marks' : ''}</p></li>`; }).join('')}</ol>`;
        } else {
          const bq = qs[q.id + p.id]; if (!bq) { body += '<p class="ca-note">This part could not be loaded.</p></div>'; continue; }
          const pref = q.id + p.id, text = dr.ans[pref] || '', uid = p.kind === 'ref' ? p.ref.split('#')[0] : null;
          const res = K ? K.checkAnswer({ question: bq, answer: { text, table: null }, unit: uid, qid: bq.id }) : null;
          if (res) { qt += res.total; checked += res.max; qp += res.pendingMarks; }
          body += `<details class="ca-given"><summary>Question and your answer</summary><p class="ca-q">${esc(bq.q)}</p><pre class="ca-myans">${esc(text || '(not answered)')}</pre></details>
            ${res ? K.reportHTML(res, bq, { h: 'h3' }) : ''}
            <details class="ca-given"><summary>Model answer</summary>${X.blocks(bq.model)}${X.checksHTML(bq.checks)}</details>${p.kind === 'ref' && X.refChip ? X.refChip(uid, bq) : ''}`;
          if (res && p.kind === 'ref' && text.trim()) refRecs.push([p.ref, Object.assign({ d: today(), secs: 0, words: (text.match(/\S+/g) || []).length, text: text.slice(0, 6000), table: null, photos: [], src: m.id }, K.record(res))]);
          if (res && p.kind === 'q' && text.trim()) wskills.push(...K.record(res).skills);
        }
        body += `</div>`;
      }
      total += qt; pend += qp;
      html += `<div class="card ca-mk"><div class="ca-mtop"><h2 class="ca-h2s">Question ${esc(q.id.slice(1))} <small>(${q.marks} marks)</small></h2><span class="ca-chip">${fmt(Math.round(qt * 100) / 100)} / ${q.marks}${qp ? ` · ${fmt(qp)} pending` : ''}</span></div>${body}</div>`;
    }
    total = Math.round(total * 100) / 100; pend = Math.round(pend * 100) / 100;
    /* saved at once — nothing for the student to rate */
    for (const [key, rec] of refRecs) { const h = c.writes[key] = c.writes[key] || []; h.push(rec); while (h.length > 5) h.shift(); }
    c.tests.push({ id: 'm' + Date.now().toString(36), kind: 'mock', mock: m.id, d: today(), ts: Date.now(), title: m.title, score: total, max: m.marks, pend, pct: pct(total, m.marks), secs: dr.secs, qs: qlist.map(q => q.id), wskills, auto: 1 });
    delete c.mockDraft[m.id]; save(); try { bumpStreak(); addXP(Math.max(10, Math.round(total / 5))); } catch (e) {}
    el.innerHTML = `<div class="ca-mbar"><span class="ca-label">${esc(m.label)}</span><div class="ca-mrow"><b>Result: ${esc(m.title)}</b><span class="ca-score" aria-live="polite"><b id="cmScore">${fmt(total)}</b> / ${m.marks}</span></div></div>
      <div class="card ca-mres"><h2 class="ca-h2s">${fmt(total)} / ${m.marks} marks${pend ? ` <small>· ${fmt(pend)} not auto-marked (presentation / judgement)</small>` : ''}</h2>
        <p class="ca-p">Every answer was checked automatically against the marking scheme — no self-marking. True/false: 2 marks only for a correct verdict with a correct reason, as in ICAI marking. Time used: ${secsTxt(dr.secs)}${dr.secs > m.hours * 3600 ? ' (over time)' : ''}.</p>
        <p class="ca-note">Result saved${refRecs.length ? ` · ${refRecs.length} answer${refRecs.length > 1 ? 's' : ''} added to your question history` : ''}.</p>
        <div class="ca-btns"><button class="btn ghost" id="cmDash">Open dashboard</button><button class="btn ghost" id="cmList">Mock papers</button></div></div>
      ${html}`;
    toast(`Checked: ${fmt(total)} / ${m.marks}`); say(`Paper checked: ${total} out of ${m.marks}`);
    D.getElementById('cmDash').onclick = dashboard; D.getElementById('cmList').onclick = mocks;
  }

  /* ================= 5. NOTES library: save · highlight · my notes ================= */
  const savedKey = (uid, kind, id) => `${uid}|${kind}:${id}`;
  function saveBtn(uid, kind, id, title) { const on = !!C().notes.saved[savedKey(uid, kind, id)]; return `<button class="ca-save" aria-pressed="${on}" data-u="${esc(uid)}" data-kind="${kind}" data-id="${esc(id)}" data-title="${esc(title)}" aria-label="${on ? 'Saved to My notes' : 'Save to My notes'}: ${esc(title)}">${on ? '★ Saved' : '☆ Save'}</button>`; }
  D.addEventListener('click', e => {
    const b = e.target.closest && e.target.closest('.ca-save'); if (!b) return;
    const k = savedKey(b.dataset.u, b.dataset.kind, b.dataset.id), s = C().notes.saved;
    if (s[k]) delete s[k]; else s[k] = { uid: b.dataset.u, kind: b.dataset.kind, id: b.dataset.id, title: b.dataset.title, d: today() };
    save(); const on = !!s[k]; b.setAttribute('aria-pressed', String(on)); b.textContent = on ? '★ Saved' : '☆ Save'; b.setAttribute('aria-label', `${on ? 'Saved to My notes' : 'Save to My notes'}: ${b.dataset.title}`);
    toast(on ? 'Saved to My notes' : 'Removed from My notes'); tap('tap');
  });
  const hasNote = uid => !!(C().notes.mine[uid] && C().notes.mine[uid].text.trim());
  /* highlights: select text inside a concept / illustration / revision card → "Highlight" button */
  let hlSel = null;
  const hlBtn = () => { let b = D.getElementById('caHLBtn'); if (!b) { D.body.insertAdjacentHTML('beforeend', '<button id="caHLBtn" class="ca-hlbtn" hidden>🖍 Highlight</button>'); b = D.getElementById('caHLBtn');
    b.addEventListener('pointerdown', e => e.preventDefault()); b.onclick = addHL; } return b; };
  D.addEventListener('selectionchange', () => {
    clearTimeout(hlBtn._t); hlBtn._t = setTimeout(() => {
      const sel = D.getSelection(), b = hlBtn(); hlSel = null;
      if (!sel || sel.isCollapsed || !sel.rangeCount) { b.hidden = true; return; }
      const r = sel.getRangeAt(0), a = r.commonAncestorContainer, host = (a.nodeType === 1 ? a : a.parentElement).closest('#s-ca .ca-hl');
      const txt = sel.toString().replace(/\s+/g, ' ').trim();
      if (!host || txt.length < 3 || txt.length > 400 || !Ca.isCA()) { b.hidden = true; return; }
      const uid = (D.querySelector('#s-ca [data-unit]') || {}).dataset?.unit || hlUid;
      hlSel = { uid, ref: host.dataset.ref, text: txt }; b.hidden = false;
    }, 120);
  });
  let hlUid = null;
  function addHL() {
    if (!hlSel || !hlSel.uid) return; const L = C().notes.hl[hlSel.uid] = C().notes.hl[hlSel.uid] || [];
    if (!L.some(h => h.ref === hlSel.ref && h.text === hlSel.text)) L.push({ ref: hlSel.ref, text: hlSel.text, d: today() });
    save(); try { D.getSelection().removeAllRanges(); } catch (e) {} hlBtn().hidden = true;
    const host = D.querySelector(`#s-ca .ca-hl[data-ref="${CSS.escape(hlSel.ref)}"]`); if (host) markText(host, hlSel.text);
    toast('Highlighted — find it in My notes'); tap('tap');
  }
  function markText(el, text) {
    const BLK = 'P,LI,TD,TH,DIV,H1,H2,H3,DT,DD,SUMMARY,ARTICLE,SECTION';
    const nodes = []; const w = D.createTreeWalker(el, NodeFilter.SHOW_TEXT, { acceptNode: n => n.parentElement.closest('button,mark,.ca-khead,script,style') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
    while (w.nextNode()) nodes.push(w.currentNode);
    let full = '', map = [], prevBlock = null;
    const blockOf = n => { let p = n.parentElement; while (p && p !== el && !BLK.split(',').includes(p.tagName)) p = p.parentElement; return p; };
    nodes.forEach(n => { const bl = blockOf(n); if (prevBlock && bl !== prevBlock && full && !/\s$/.test(full)) { full += ' '; map.push(null); } prevBlock = bl;
      const s = n.nodeValue; for (let i = 0; i < s.length; i++) { const ch = /\s/.test(s[i]) ? ' ' : s[i]; if (ch === ' ' && (!full || full.endsWith(' '))) continue; full += ch; map.push([n, i]); } });
    const at = full.indexOf(text); if (at < 0) return false;
    const segs = new Map(); for (let k = at; k < at + text.length; k++) { const m = map[k]; if (!m) continue; const sg = segs.get(m[0]) || [m[1], m[1]]; sg[1] = m[1]; segs.set(m[0], sg); }
    [...segs.entries()].reverse().forEach(([n, [a, b]]) => { try { const r = D.createRange(); r.setStart(n, a); r.setEnd(n, b + 1); const mk = D.createElement('mark'); mk.className = 'ca-mark'; r.surroundContents(mk); } catch (e) {} });
    return true;
  }
  function applyHL(root, uid) {
    hlUid = uid; root.dataset.unit = uid;
    (C().notes.hl[uid] || []).forEach(h => { const host = root.querySelector(`.ca-hl[data-ref="${CSS.escape(h.ref)}"]`); if (host) markText(host, h.text); });
  }
  function noteSheet(uid, title) {
    D.getElementById('caNoteSheet')?.remove();
    const prev = D.activeElement, cur = (C().notes.mine[uid] || {}).text || '';
    D.body.insertAdjacentHTML('beforeend', `<div class="sheet show ca-sheet" id="caNoteSheet" role="dialog" aria-modal="true" aria-labelledby="caNoteT"><div class="sheet-in"><div class="sheet-grab"></div>
      <h2 id="caNoteT" class="ca-h2s">📝 My notes</h2><p class="sub">${esc(title)}</p><label class="sr-only" for="caNoteTa">Your notes for this unit</label>
      <textarea id="caNoteTa" class="ca-ta" rows="9" placeholder="Your own words, mnemonics, doubts to ask your teacher…">${esc(cur)}</textarea>
      <div class="ca-padbar"><span id="caNoteSt" role="status">${cur ? 'Saved' : ''}</span><span>Saved on this device</span></div>
      <div class="ca-btns"><button class="btn ghost" id="caNoteAll">All my notes</button><button class="btn" id="caNoteX">Done</button></div></div></div>`);
    const sh = D.getElementById('caNoteSheet'), ta = D.getElementById('caNoteTa');
    const close = () => { sh.classList.remove('show'); setTimeout(() => sh.remove(), 40); const b = D.getElementById('caMyNote'); if (b) b.textContent = '📝 My notes' + (hasNote(uid) ? ' ✓' : ''); try { prev && prev.focus(); } catch (e) {} };
    ta.oninput = () => { clearTimeout(ta._t); D.getElementById('caNoteSt').textContent = 'Saving…'; ta._t = setTimeout(() => { if (ta.value.trim()) C().notes.mine[uid] = { text: ta.value.slice(0, 10000), d: today() }; else delete C().notes.mine[uid]; save(); const s = D.getElementById('caNoteSt'); if (s) s.textContent = 'Saved'; }, 400); };
    D.getElementById('caNoteX').onclick = () => { ta.oninput(); setTimeout(close, 450); };
    D.getElementById('caNoteAll').onclick = () => { ta.oninput(); setTimeout(() => { close(); notes(); }, 450); };
    sh.addEventListener('click', e => { if (e.target === sh) D.getElementById('caNoteX').click(); });
    sh.addEventListener('keydown', e => { if (e.key === 'Escape') D.getElementById('caNoteX').click(); if (e.key === 'Tab') { const f = [...sh.querySelectorAll('textarea,button')]; const i = f.indexOf(D.activeElement); if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); } else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); } } });
    ta.focus();
  }
  async function notes() {
    const el = X.open('me'), n = C().notes;
    const uids = new Set([...Object.values(n.saved).map(s => s.uid), ...Object.keys(n.hl).filter(u => n.hl[u].length), ...Object.keys(n.mine)]);
    const rows = []; for (const uid of uids) { try { const st = await X.structure(X.levelOf(uid)); const f = X.findUnit(st, uid); if (f) rows.push({ uid, ...f, level: X.levelOf(uid) }); } catch (e) {} }
    rows.sort((a, b) => a.uid.localeCompare(b.uid));
    const kindN = { concept: 'Concept card', illus: 'Illustration', rev: 'Revision page' }, tabOf = { concept: 'learn', illus: 'illus', rev: 'revise' };
    let html = '', lastP = null, lastC = null;
    rows.forEach(r => {
      if (r.p.id !== lastP) { html += `<h2 class="ca-group">CA ${esc(X.levelName(r.level))} · ${esc(X.paperLabel(r.p))} · ${esc(r.p.name)}</h2>`; lastP = r.p.id; lastC = null; }
      if (r.c.id !== lastC) { html += `<h3 class="ca-nch">Chapter ${r.c.n}: ${esc(r.c.title)}</h3>`; lastC = r.c.id; }
      const sv = Object.entries(n.saved).filter(([, s]) => s.uid === r.uid), hl = n.hl[r.uid] || [], mine = n.mine[r.uid];
      html += `<div class="card ca-nunit"><div class="ca-mtop"><h4 class="ca-h3">Unit ${r.u.n}: ${esc(r.u.title)}</h4><button class="ca-link" data-open="${r.uid}">Open ›</button></div>
        ${mine ? `<div class="ca-nmine"><b>My note</b><p>${esc(mine.text).replace(/\n/g, '<br>')}</p><button class="ca-link" data-edit="${r.uid}" data-t="${esc(r.u.title)}">Edit note</button></div>` : `<button class="ca-link" data-edit="${r.uid}" data-t="${esc(r.u.title)}">+ Add a note</button>`}
        ${sv.length ? `<ul class="ca-nlist">${sv.map(([k, s]) => `<li><button class="ca-nopen" data-u="${s.uid}" data-tab="${tabOf[s.kind]}" data-ref="${s.kind}:${esc(s.id)}"><span class="ca-chip">★ ${kindN[s.kind] || s.kind}</span> ${esc(s.title)}</button><button class="ca-x" data-unsave="${esc(k)}" aria-label="Remove saved item: ${esc(s.title)}">✕</button></li>`).join('')}</ul>` : ''}
        ${hl.length ? `<ul class="ca-nlist">${hl.map((h, i) => `<li><button class="ca-nopen" data-u="${r.uid}" data-tab="${tabOf[h.ref.split(':')[0]]}" data-ref="${esc(h.ref)}"><mark class="ca-mark">${esc(h.text)}</mark></button><button class="ca-x" data-unhl="${r.uid}" data-i="${i}" aria-label="Remove highlight">✕</button></li>`).join('')}</ul>` : ''}</div>`;
    });
    el.innerHTML = `<h1 class="ca-h1 ca-onDark">📚 My notes</h1>
      <div class="gsearch ca-search"><span aria-hidden="true">🔍</span><input id="cnQ" placeholder="Search notes, ICAI topics and lessons…" autocomplete="off" aria-label="Smart search"></div>
      ${rows.length ? html : `<div class="card"><p class="ca-p">Nothing saved yet. In any unit, tap <b>☆ Save</b> on a concept card, illustration or revision page; select text to <b>🖍 highlight</b> it; or use <b>📝 My notes</b> to write your own notes.</p></div>`}`;
    const q = D.getElementById('cnQ'); q.onkeydown = e => { if (e.key === 'Enter' && q.value.trim()) search(q.value); }; q.oninput = () => { clearTimeout(q._t); q._t = setTimeout(() => { if (q.value.trim().length >= 3) search(q.value); }, 900); };
    el.querySelectorAll('[data-open]').forEach(b => b.onclick = () => Ca.unit(b.dataset.open));
    el.querySelectorAll('[data-edit]').forEach(b => b.onclick = () => { noteSheet(b.dataset.edit, b.dataset.t); const x = D.getElementById('caNoteX'), a = D.getElementById('caNoteAll'); const re = () => setTimeout(notes, 500); x.addEventListener('click', re); a.remove(); });
    el.querySelectorAll('.ca-nopen').forEach(b => b.onclick = () => goRef(b.dataset.u, b.dataset.tab, b.dataset.ref));
    el.querySelectorAll('[data-unsave]').forEach(b => b.onclick = () => { delete n.saved[b.dataset.unsave]; save(); notes(); });
    el.querySelectorAll('[data-unhl]').forEach(b => b.onclick = () => { n.hl[b.dataset.unhl].splice(+b.dataset.i, 1); save(); notes(); });
  }
  async function goRef(uid, tab, ref) {
    await Ca.unit(uid, tab || 'learn');
    if (ref) setTimeout(() => { const t = D.querySelector(`#s-ca [data-ref="${CSS.escape(ref)}"]`); if (t) { t.scrollIntoView({ behavior: 'smooth', block: 'start' }); t.classList.add('ca-flash'); setTimeout(() => t.classList.remove('ca-flash'), 1600); } }, 120);
  }

  /* ---------- smart search: ICAI structure + built content + my notes (ranked, typo-tolerant) ---------- */
  let IDX = null;
  const stoks = s => String(s || '').toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/).filter(w => w && !STOP.has(w)).map(stem);
  function levN(a, b, max) { if (Math.abs(a.length - b.length) > max) return max + 1; let p = Array.from({ length: b.length + 1 }, (_, i) => i); for (let i = 1; i <= a.length; i++) { const c = [i]; let mn = i; for (let j = 1; j <= b.length; j++) { c[j] = Math.min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)); if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) c[j] = Math.min(c[j], p[j - 2 < 0 ? 0 : j - 2] + 1); mn = Math.min(mn, c[j]); } if (mn > max) return max + 1; p = c; } return p[b.length]; }
  async function buildIndex() {
    const docs = [], sts = await X.allStructures();
    const add = (o, title, body) => docs.push({ ...o, title, body: body || '', tt: stoks(title), bt: stoks(body) });
    sts.forEach((st, li) => st && st.papers.forEach(p => { const L = X.LEVELS[li][0];
      add({ type: 'paper', level: L, pid: p.id, path: `CA ${X.levelName(L)}` }, `${X.paperLabel(p)}: ${p.name}`);
      p.chapters.forEach(c => { add({ type: 'chapter', level: L, pid: p.id, path: `CA ${X.levelName(L)} · ${X.paperLabel(p)}` }, `Chapter ${c.n}: ${c.title}`, [c.module, c.part].filter(Boolean).join(' '));
        c.units.forEach(u => { if (!u.implicit) add({ type: 'unit', level: L, pid: p.id, uid: u.id, built: u.status === 'built', path: `${X.paperLabel(p)} · Ch ${c.n}` }, `Unit ${u.n}: ${u.title}`, (u.topics || []).join(' · '));
          else if (u.topics) add({ type: 'unit', level: L, pid: p.id, uid: u.id, built: u.status === 'built', path: `${X.paperLabel(p)} · Ch ${c.n}` }, c.title, u.topics.join(' · ')); }); }); }));
    const built = await loadAll(await builtList());
    built.forEach(b => { const d = b.d, path = `${X.paperLabel(b.p)} · Ch ${b.c.n} · ${b.u.title}`, uid = b.u.id;
      d.concepts.forEach(c => add({ type: 'concept', uid, tab: 'learn', ref: 'concept:' + c.id, path }, c.title, [...c.body, c.analogy, c.work].join(' ')));
      d.illustrations.forEach(x => add({ type: 'illus', uid, tab: 'illus', ref: 'illus:' + x.id, path }, x.title, x.q));
      d.mcqs.forEach(q => add({ type: 'mcq', uid, tab: 'mcq', path }, q.q, q.explain));
      (d.cases || []).forEach(cs => add({ type: 'case', uid, tab: 'mcq', path }, cs.title, cs.case));
      (d.viva || []).forEach(v => add({ type: 'viva', uid, tab: 'viva', path }, v.q, v.model));
      d.questions.forEach(q => add({ type: 'question', uid, tab: 'write', path }, q.q.slice(0, 160), q.q));
      d.quickref.forEach(r => add({ type: 'quickref', uid, tab: 'revise', ref: 'rev:page', path }, r.k, r.v));
      add({ type: 'revision', uid, tab: 'revise', ref: 'rev:page', path }, 'Revision: ' + d.title, [...d.revision.summary, ...d.revision.remember, ...d.revision.traps].join(' ')); });
    IDX = docs; return docs;
  }
  function noteDocs() {
    const n = C().notes, out = [], mk = (o, title, body) => out.push({ ...o, title, body, tt: stoks(title), bt: stoks(body) });
    Object.entries(n.mine).forEach(([uid, m]) => mk({ type: 'note', uid, path: 'My note' }, (m.text.split('\n')[0] || 'My note').slice(0, 80), m.text));
    Object.entries(n.hl).forEach(([uid, L]) => L.forEach(h => mk({ type: 'highlight', uid, tab: { concept: 'learn', illus: 'illus', rev: 'revise' }[h.ref.split(':')[0]], ref: h.ref, path: 'Highlight' }, h.text, '')));
    Object.values(n.saved).forEach(s => mk({ type: 'saved', uid: s.uid, tab: { concept: 'learn', illus: 'illus', rev: 'revise' }[s.kind], ref: `${s.kind}:${s.id}`, path: 'Saved' }, s.title, ''));
    return out;
  }
  function rank(q, docs) {
    const qt = stoks(q); if (!qt.length) return [];
    const ql = q.toLowerCase().trim(), TW = { note: 1.5, highlight: 1.4, saved: 1.4, unit: 1.25, chapter: 1.2, concept: 1.15, paper: 1.1 };
    const tokScore = (t, list) => { let best = 0; for (const w of list) { let s = 0; if (w === t) s = 1; else if (t.length >= 3 && w.startsWith(t)) s = .85; else if (t.length >= 4 && w.length >= 4) { const d = levN(t, w, t.length >= 7 ? 2 : 1); if (d <= (t.length >= 7 ? 2 : 1)) s = d === 1 ? .62 : .42; } if (s > best) best = s; if (best === 1) break; } return best; };
    const out = [];
    for (const d of docs) {
      let sc = 0, hits = 0;
      for (const t of qt) { const a = tokScore(t, d.tt) * 3, b = tokScore(t, d.bt); const s = Math.max(a, b); if (s > 0) hits++; sc += s; }
      if (hits < Math.ceil(qt.length * 0.67)) continue;
      if (d.title.toLowerCase().includes(ql)) sc += 3; else if (d.body.toLowerCase().includes(ql)) sc += 1;
      sc = sc * (TW[d.type] || 1) * (hits / qt.length) - (d.type === 'unit' && !d.built ? .3 : 0);
      out.push([sc, d]);
    }
    return out.sort((a, b) => b[0] - a[0]).map(x => x[1]);
  }
  const TYPEN = { paper: 'Paper', chapter: 'ICAI chapter', unit: 'ICAI unit', concept: 'Concept', illus: 'Illustration', mcq: 'MCQ', case: 'Case study', viva: 'Viva', question: 'Written Q', quickref: 'Quick ref', revision: 'Revision', note: 'My note', highlight: 'Highlight', saved: 'Saved' };
  async function search(q0 = '') {
    const el = X.open('world');
    el.innerHTML = '';
    el.appendChild(back('CA Journey', Ca.home));
    el.insertAdjacentHTML('beforeend', `<h1 class="ca-h1 ca-onDark">Search</h1><div class="gsearch ca-search"><span aria-hidden="true">🔍</span><input id="csQ" placeholder="e.g. suspense account, contra entry, Section 4…" autocomplete="off" aria-label="Search ICAI structure, lessons and your notes" value="${esc(q0)}"></div>
      <p class="ca-note ca-onDark2" id="csInfo" role="status">Searches every ICAI chapter and unit (Foundation, Intermediate, Final), all lessons built so far and your notes. Spelling slips are fine.</p><div id="csRes"></div>`);
    const inp = D.getElementById('csQ'), box = D.getElementById('csRes'), info = D.getElementById('csInfo');
    if (!IDX) { info.textContent = 'Preparing search…'; await buildIndex(); info.textContent = 'Searches every ICAI chapter and unit (Foundation, Intermediate, Final), all lessons built so far and your notes. Spelling slips are fine.'; }
    const go = () => {
      const v = inp.value.trim(); if (v.length < 2) { box.innerHTML = ''; return; }
      const r = rank(v, noteDocs().concat(IDX)).slice(0, 30);
      info.textContent = r.length ? `${r.length === 30 ? 'Top 30' : r.length} result${r.length === 1 ? '' : 's'} for “${v}”` : `No results for “${v}”. Try fewer or different words.`;
      box.innerHTML = r.length ? `<ul class="ca-sres">${r.map((d, i) => `<li><button class="ca-shit" data-i="${i}"><span class="ca-chip ca-t-${d.type}">${TYPEN[d.type]}${d.type === 'unit' && !d.built ? ' · soon' : ''}</span><b>${esc(d.title.length > 140 ? d.title.slice(0, 137) + '…' : d.title)}</b>${snippet(d, v)}<small>${esc(d.path || '')}</small></button></li>`).join('')}</ul>` : '';
      box.querySelectorAll('.ca-shit').forEach(b => b.onclick = () => { const d = r[+b.dataset.i]; tap('open');
        if (d.type === 'paper' || d.type === 'chapter') return Ca.paper(d.level, d.pid, d.type === 'chapter' ? d.title.replace(/^Chapter \d+:\s*/, '') : '');
        if (d.type === 'unit') return d.built ? Ca.unit(d.uid) : Ca.paper(d.level, d.pid, d.title.replace(/^Unit \d+:\s*/, ''));
        if (d.type === 'note') return noteSheet(d.uid, 'My note');
        return goRef(d.uid, d.tab, d.ref); });
    };
    let t; inp.oninput = () => { clearTimeout(t); t = setTimeout(go, 200); }; go(); inp.focus();
  }
  function snippet(d, q) {
    if (!d.body) return ''; const words = stoks(q), b = d.body; let at = -1;
    for (const w of words) { const m = b.toLowerCase().indexOf(w.slice(0, Math.max(3, w.length - 1))); if (m >= 0) { at = m; break; } }
    if (at < 0) return d.type === 'unit' ? `<span class="ca-snip">${esc(b.slice(0, 110))}${b.length > 110 ? '…' : ''}</span>` : '';
    let s = Math.max(0, at - 50); if (s) { const sp = b.indexOf(' ', s); if (sp > 0 && sp < at) s = sp + 1; } return `<span class="ca-snip">${s ? '…' : ''}${esc(b.slice(s, at + 90))}${at + 90 < b.length ? '…' : ''}</span>`;
  }

  /* ================= 1. DASHBOARD ================= */
  function dayList(n) { const out = []; const d0 = new Date(X.todayISO() + 'T12:00:00'); for (let i = n - 1; i >= 0; i--) { const d = new Date(d0 - i * 864e5); out.push(`${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`); } return out; }
  const isoOfMin = m => { const d = new Date(m * 6e4); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
  function activity() {
    const c = C(), act = {}; const bump = (d, k, v = 1) => { if (!d) return; const a = act[d] = act[d] || { secs: 0, ans: 0, right: 0, ms: 0, viva: 0, units: 0 }; a[k] += v; };
    Object.entries(c.time).forEach(([d, s]) => bump(d, 'secs', s));
    c.mlog.forEach(([m, , ok, s]) => { const d = isoOfMin(m); bump(d, 'ans'); if (ok) bump(d, 'right'); bump(d, 'ms', s * 1000); });
    Object.values(c.viva).forEach(h => h.forEach(a => bump(a.d, 'viva')));
    Object.values(c.units).forEach(u => X.TABS.forEach(([k]) => { if (u[k]) bump(u[k], 'units'); }));
    const activeDay = d => act[d] && (act[d].secs >= 60 || act[d].ans || act[d].viva || act[d].units);
    const days = dayList(400); let cur = 0; for (let i = days.length - 1; i >= 0; i--) { if (activeDay(days[i])) cur++; else if (i === days.length - 1) continue; else break; }
    let best = 0, run = 0; days.forEach(d => { if (activeDay(d)) { run++; best = Math.max(best, run); } else run = 0; });
    return { act, activeDay, cur, best };
  }
  async function dashData() {
    const c = C(), sts = await X.allStructures(), { act, activeDay, cur, best } = activity();
    const d14 = dayList(14), d56 = dayList(56);
    const totalSecs = Object.values(c.time).reduce((a, b) => a + b, 0);
    /* progress tree */
    const papers = []; sts.forEach((st, li) => st && st.papers.forEach(p => { if (!X.builtCount(p)) return;
      papers.push({ id: p.id, level: X.LEVELS[li][0], label: X.paperLabel(p), name: p.name, pct: X.paperProg(p), built: X.builtCount(p), units: X.unitCount(p),
        chapters: p.chapters.filter(ch => ch.units.some(u => u.status === 'built')).map(ch => ({ id: ch.id, n: ch.n, title: ch.title, pct: ch.units.reduce((a, u) => a + X.unitProg(u.id), 0) / ch.units.length,
          units: ch.units.map(u => ({ id: u.id, n: u.n, title: u.title, status: u.status, pct: X.unitProg(u.id), tabs: X.TABS.filter(([k]) => (c.units[u.id] || {})[k]).map(([k]) => k) })) })) }); }));
    /* MCQ */
    let ms = 0, mr = 0, mt = 0; Object.values(c.mcq).forEach(v => { ms += v.s; mr += v.s - v.w; mt += v.ms || 0; });
    const timed = c.mlog.length ? c.mlog.reduce((a, x) => a + x[3], 0) / c.mlog.length : null;
    const byCh = {}; Object.entries(c.mcq).forEach(([k, v]) => { const ch = chOf(k.split('#')[0]); const b = byCh[ch] = byCh[ch] || { n: 0, r: 0 }; b.n += v.s; b.r += v.s - v.w; });
    const chName = {}; sts.forEach(st => st && st.papers.forEach(p => p.chapters.forEach(ch => { chName[ch.id] = `${X.paperLabel(p).replace('Paper ', 'P')} Ch ${ch.n}: ${ch.title}`; })));
    /* written skills */
    const { skills } = X.weakData();
    /* viva */
    const vu = {}; Object.entries(c.viva).forEach(([k, h0]) => { const h = h0.filter(a => a.status !== 'waiting'); if (!h.length) return; const uid = k.split('#')[0]; const u = vu[uid] = vu[uid] || { n: 0, sum: 0, best: [], ready: 0 }; const b = Math.max(...h.map(a => a.pct)); u.n += h.length; u.sum += h.reduce((a, x) => a + x.pct, 0); u.best.push(b); if (b >= 80) u.ready++; });
    const names = {}; for (const st of sts) st && st.papers.forEach(p => p.chapters.forEach(ch => ch.units.forEach(u => { names[u.id] = u.title; })));
    const vAll = vivaScored().flat();
    const { qs: wq } = X.weakData(), wAll = wq.flatMap(x => x.hist);
    return {
      mode: 'ca', schema: 'ca-dashboard/1', student: ST.profile?.name || '', level: c.level, levelName: X.levelName(c.level),
      exam: { date: c.exam || null, daysLeft: X.daysLeft() },
      streak: { current: cur, best, today: !!activeDay(X.todayISO()) },
      time: { today: (c.time[X.todayISO()] || 0), week: dayList(7).reduce((a, d) => a + (c.time[d] || 0), 0), total: totalSecs, byDay: d14.map(d => ({ d, secs: c.time[d] || 0 })) },
      activity: d56.map(d => ({ d, secs: act[d]?.secs || 0, answers: act[d]?.ans || 0, active: !!activeDay(d) })),
      progress: { papers },
      mcq: { answered: ms, right: mr, accuracy: ms ? mr / ms : null, avgSecs: timed, byDay: d14.map(d => ({ d, n: act[d]?.ans || 0, right: act[d]?.right || 0, avgSecs: act[d]?.ans ? act[d].ms / act[d].ans / 1000 : null })),
        byChapter: Object.entries(byCh).map(([id, b]) => ({ id, title: chName[id] || id, n: b.n, accuracy: b.r / b.n })).sort((a, b) => a.accuracy - b.accuracy) },
      skills: Object.entries(skills).map(([k, s]) => ({ key: k, label: X.SKILL[k] || k, marks: s.m, got: s.g, lost: Math.round((s.m - s.g) * 100) / 100, n: s.n || 0, pct: s.m ? s.g / s.m : null })).filter(s => s.marks > 0).sort((a, b) => a.pct - b.pct),
      written: { checked: wAll.filter(a => a.status === 'auto').length, waiting: wAll.filter(a => a.status === 'waiting').length, pending: wq.reduce((a, x) => { const l = x.hist[x.hist.length - 1]; return a + (l && l.status === 'auto' ? l.pend || 0 : 0); }, 0),
        questions: wq.map(x => ({ key: x.key, uid: x.uid, qid: x.qid, title: names[x.uid] || x.uid, hist: x.hist })) },
      viva: { attempts: vAll.length, avg: vAll.length ? vAll.reduce((a, x) => a + x.pct, 0) / vAll.length : null, ready: Object.values(vu).reduce((a, u) => a + u.ready, 0),
        byUnit: Object.entries(vu).map(([uid, u]) => ({ uid, title: names[uid] || uid, avg: u.sum / u.n, bestAvg: u.best.reduce((a, b) => a + b, 0) / u.best.length, tried: u.best.length, ready: u.ready })) },
      tests: c.tests.filter(t => t.kind === 'mcq').slice(-12).map(t => ({ d: t.d, title: t.title, mode: t.mode, n: t.n, right: t.right, pct: t.pct, secs: Math.round(t.ms / 1000) })),
      mocks: c.tests.filter(t => t.kind === 'mock').map(t => ({ d: t.d, title: t.title, score: t.score, max: t.max, pct: t.pct, secs: t.secs })),
      revise: Object.keys(c.revise).length,
    };
  }
  const svgBars = (vals, labels, o = {}) => {
    const W = 320, H = o.h || 110, n = vals.length, mx = Math.max(o.max || 0, ...vals, 1), bw = (W - 8) / n;
    return `<svg class="ca-chart" viewBox="0 0 ${W} ${H + 18}" role="img" aria-label="${esc(o.label)}"><line x1="0" y1="${H}" x2="${W}" y2="${H}" class="ca-axis"/>${vals.map((v, i) => { const h = v ? Math.max(3, v / mx * (H - 6)) : 0, x = 4 + i * bw + 1; return `<g><rect x="${x.toFixed(1)}" y="${(H - h).toFixed(1)}" width="${Math.max(2, bw - 3).toFixed(1)}" height="${h.toFixed(1)}" rx="3" class="${o.cls ? o.cls(i) : 'ca-b1'}"><title>${esc(labels[i])}: ${esc(o.fmt ? o.fmt(v, i) : v)}</title></rect><rect x="${(4 + i * bw).toFixed(1)}" y="0" width="${bw.toFixed(1)}" height="${H}" fill="transparent"><title>${esc(labels[i])}: ${esc(o.fmt ? o.fmt(v, i) : v)}</title></rect>${o.vlabels ? `<text x="${(x + (bw - 3) / 2).toFixed(1)}" y="${Math.max(10, H - h - 4).toFixed(1)}" text-anchor="middle" class="ca-vlab">${esc(o.vlabels(v, i))}</text>` : ''}</g>`; }).join('')}
      ${o.ticks ? o.ticks.map(([i, t]) => `<text x="${(4 + i * bw + bw / 2).toFixed(1)}" y="${H + 14}" text-anchor="middle" class="ca-tick">${esc(t)}</text>`).join('') : ''}</svg>`;
  };
  const dlab = d => new Date(d + 'T12:00:00').toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });
  const tableOf = (head, rows) => `<details class="ca-tview"><summary>Show as table</summary><div class="ca-scroll" role="region" tabindex="0" aria-label="Data table"><table class="ca-t"><thead><tr>${head.map(h => `<th scope="col">${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(r => `<tr>${r.map(x => `<td>${esc(x)}</td>`).join('')}</tr>`).join('')}</tbody></table></div></details>`;
  const band = p => p == null ? ['', '—'] : p < .6 ? ['w', 'Weak'] : p >= .8 ? ['s', 'Strong'] : ['m', 'Getting there'];
  function renderDash(host, D_, engine) {
    const m = D_.mcq, v = D_.viva, t = D_.time;
    const kpi = (val, lab, sub, cls = '') => `<div class="ca-kpi ${cls}"><b>${val}</b><span>${lab}</span>${sub ? `<small>${sub}</small>` : ''}</div>`;
    const lastMock = D_.mocks[D_.mocks.length - 1];
    host.innerHTML = `
      <div class="ca-dhero"><div><span class="ca-k">CA ${esc(D_.levelName)} · Dashboard</span><h1 class="ca-h1">${esc(D_.student ? D_.student + '’s progress' : 'Your progress')}</h1></div>
        <div class="ca-dcount">${D_.exam.daysLeft == null ? '<button class="ca-link" id="cdExam">Set exam date</button>' : `<b>${Math.max(0, D_.exam.daysLeft)}</b><span>days to exam</span>`}</div></div>
      <div class="ca-kpis ca-kpis6${engine ? ' ca-kpis3' : ''}">
        ${engine ? '' : kpi(D_.streak.current + (D_.streak.current === 1 ? ' day' : ' days'), 'Consistency streak', `Best ${D_.streak.best}${D_.streak.today ? ' · today ✓' : ' · study today to keep it'}`)}
        ${engine ? '' : kpi(durTxt(t.week), 'Studied this week', `Today ${durTxt(t.today)} · total ${durTxt(t.total)}`)}
        ${engine ? '' : kpi(m.accuracy == null ? '—' : Math.round(m.accuracy * 100) + '%', 'MCQ accuracy', `${m.answered} answered`)}
        ${kpi(m.avgSecs == null ? '—' : Math.round(m.avgSecs) + ' s', 'Speed per MCQ', 'average time to answer')}
        ${kpi(v.avg == null ? '—' : Math.round(v.avg) + '%', 'Viva coverage', `${v.ready} question${v.ready === 1 ? '' : 's'} viva-ready`)}
        ${kpi(lastMock ? `${fmt(lastMock.score)}/${lastMock.max}` : '—', 'Latest mock', lastMock ? esc(dlab(lastMock.d)) : 'not attempted yet')}
      </div>
      ${engine ? '<div id="cdEngine" class="ca-engine"></div><h2 class="ca-h2">More for CA</h2>' : ''}
      <div class="ca-dgrid">
      ${engine ? '' : `<section class="card ca-dcard"><h2 class="ca-h2s">Consistency — last 8 weeks</h2><p class="sub">${D_.activity.filter(a => a.active).length} active days out of 56.</p>
        <div class="ca-heat" role="img" aria-label="Activity calendar: ${D_.activity.filter(a => a.active).length} active days in the last 8 weeks">${D_.activity.map(a => { const lv = !a.active ? 0 : a.secs >= 3600 ? 4 : a.secs >= 1800 ? 3 : a.secs >= 600 ? 2 : 1; return `<i class="h${lv}" title="${esc(dlab(a.d))}: ${a.active ? durTxt(a.secs) + (a.answers ? `, ${a.answers} MCQs` : '') : 'no study'}"></i>`; }).join('')}</div>
        <div class="ca-hkey" aria-hidden="true">Less <i class="h0"></i><i class="h1"></i><i class="h2"></i><i class="h3"></i><i class="h4"></i> More</div>
        ${tableOf(['Date', 'Time studied', 'MCQs'], D_.activity.filter(a => a.active).map(a => [dlab(a.d), durTxt(a.secs), a.answers]))}</section>`}
      ${engine ? '' : `<section class="card ca-dcard"><h2 class="ca-h2s">Time studied — last 14 days</h2><p class="sub">${durTxt(t.byDay.reduce((a, x) => a + x.secs, 0))} in 14 days.</p>
        ${svgBars(t.byDay.map(x => Math.round(x.secs / 60)), t.byDay.map(x => dlab(x.d)), { label: 'Minutes studied per day, last 14 days', fmt: v => v + ' min', ticks: [[0, dlab(t.byDay[0].d)], [13, 'Today']] })}
        ${tableOf(['Date', 'Minutes'], t.byDay.map(x => [dlab(x.d), Math.round(x.secs / 60)]))}</section>`}
      <section class="card ca-dcard"><h2 class="ca-h2s">MCQs — accuracy &amp; speed</h2><p class="sub">${m.answered ? `${Math.round(m.accuracy * 100)}% correct overall${m.avgSecs != null ? `, ${Math.round(m.avgSecs)} s per question` : ''}.` : 'Answer MCQs to see your accuracy and speed.'}</p>
        ${svgBars(m.byDay.map(x => x.n ? Math.round(x.right / x.n * 100) : 0), m.byDay.map(x => dlab(x.d)), { label: 'MCQ accuracy per day, last 14 days', max: 100, fmt: (v, i) => m.byDay[i].n ? `${v}% of ${m.byDay[i].n}${m.byDay[i].avgSecs ? `, ${Math.round(m.byDay[i].avgSecs)} s each` : ''}` : 'no MCQs', cls: i => m.byDay[i].n && m.byDay[i].right / m.byDay[i].n < .6 ? 'ca-b2' : 'ca-b1', ticks: [[0, dlab(m.byDay[0].d)], [13, 'Today']] })}
        ${m.byChapter.length ? `<h3 class="ca-h3">By chapter</h3>${m.byChapter.map(ch => { const [cl, lb] = band(ch.accuracy); return `<div class="ca-skill"><span>${esc(ch.title)}</span>${X.bar(ch.accuracy)}<b class="${cl}">${Math.round(ch.accuracy * 100)}%</b></div>`; }).join('')}` : ''}
        ${tableOf(['Date', 'MCQs', 'Correct', 'Avg seconds'], m.byDay.filter(x => x.n).map(x => [dlab(x.d), x.n, x.right, x.avgSecs ? Math.round(x.avgSecs) : '–']))}</section>
      <section class="card ca-dcard ca-dwrit"><h2 class="ca-h2s">Written answers — marks lost by skill</h2><p class="sub">${D_.written.checked ? `From ${D_.written.checked} automatically checked answer${D_.written.checked === 1 ? '' : 's'} (latest attempt of each question; unit Write tab, question bank and mock papers).` : 'Check a written answer to see which kinds of marks you win and lose — journal entries, quoting the provision, computations…'}${D_.written.waiting ? ` ⏳ ${D_.written.waiting} photo answer${D_.written.waiting === 1 ? '' : 's'} not marked (photo only — type the key points to get marks).` : ''}${D_.written.pending ? ` ${fmt(D_.written.pending)} mark${D_.written.pending === 1 ? '' : 's'} not auto-marked (presentation / judgement) are not counted.` : ''}</p>
        ${D_.skills.map(s => { const [cl, lb] = band(s.pct); return `<div class="ca-skill"><span>${esc(s.label)}<small> lost ${fmt(s.lost)} of ${fmt(Math.round(s.marks * 100) / 100)} marks · ${lb}</small></span>${X.bar(s.pct)}<b class="${cl}">${Math.round(s.pct * 100)}%</b></div>`; }).join('')}
        ${D_.skills.length ? tableOf(['Skill', 'Marks checked', 'Marks won', 'Marks lost'], D_.skills.map(s => [s.label, fmt(Math.round(s.marks * 100) / 100), fmt(Math.round(s.got * 100) / 100), fmt(s.lost)])) : ''}
        ${D_.written.questions.length ? `<h3 class="ca-h3">History per question</h3><ul class="ca-qhist">${D_.written.questions.slice(-8).reverse().map(x => `<li><button class="ca-qh" data-u="${esc(x.uid)}" data-q="${esc(x.qid)}"><span><b>${esc(x.qid.toUpperCase())}</b><small>${esc(x.title)}</small></span><span class="ca-qhs">${x.hist.map(a => a.status === 'waiting' ? '<i class="pend" title="Photo only — not marked">📷</i>' : `<i class="${a.max && a.score / a.max >= .8 ? 's' : a.max && a.score / a.max < .5 ? 'w' : 'm'}">${fmt(a.score)}</i>`).join('<span aria-hidden="true">→</span>')}<em>/ ${fmt((x.hist[x.hist.length - 1] || {}).full || '')}</em></span></button></li>`).join('')}</ul><button class="btn ghost" id="cdWeak">Weak spots — full analysis</button>` : ''}</section>
      <section class="card ca-dcard"><h2 class="ca-h2s">🎙️ Viva scores</h2><p class="sub">${v.attempts ? `${v.attempts} spoken answers · average ${Math.round(v.avg)}% coverage.` : 'Try a viva — answer out loud and see your coverage.'}</p>
        ${v.byUnit.map(u => `<div class="ca-skill"><span>${esc(u.title)}<small> ${u.ready}/${u.tried} viva-ready</small></span>${X.bar(u.bestAvg / 100)}<b class="${u.bestAvg >= 80 ? 's' : u.bestAvg < 50 ? 'w' : 'm'}">${Math.round(u.bestAvg)}%</b></div>`).join('')}
        <button class="btn ghost" id="cdViva">Practise viva</button></section>
      <section class="card ca-dcard"><h2 class="ca-h2s">Mock papers &amp; tests</h2>
        ${D_.mocks.length ? `<h3 class="ca-h3">Mock papers</h3><ul class="ca-ul">${D_.mocks.slice().reverse().map(x => `<li><b>${fmt(x.score)}/${x.max}</b> (${x.pct}%) — ${esc(x.title)}, ${esc(x.d)}, ${durTxt(x.secs)}</li>`).join('')}</ul>` : '<p class="ca-p">No mock paper yet. A full 3-hour paper in ICAI pattern is waiting.</p>'}
        ${D_.tests.length ? `<h3 class="ca-h3">MCQ sets</h3>${svgBars(D_.tests.map(x => x.pct), D_.tests.map(x => `${dlab(x.d)} ${x.title}`), { label: 'Score of recent MCQ sets', max: 100, h: 80, vlabels: v => v + '%', fmt: (v, i) => `${D_.tests[i].right}/${D_.tests[i].n} (${v}%)` })}${tableOf(['Date', 'Set', 'Mode', 'Score', 'Seconds'], D_.tests.slice().reverse().map(x => [dlab(x.d), x.title, x.mode, `${x.right}/${x.n}`, x.secs]))}` : ''}
        <div class="ca-btns"><button class="btn ghost" id="cdMock">Mock papers</button><button class="btn ghost" id="cdRev">Revise these (${D_.revise})</button></div></section>
      <section class="card ca-dcard ca-dwide"><h2 class="ca-h2s">Progress — paper › chapter › unit</h2>
        ${D_.progress.papers.map(p => `<details class="ca-dp" open><summary><span>${esc(p.label)} · ${esc(p.name)}<small>${p.built}/${p.units} units live</small></span>${X.bar(p.pct)}<b>${Math.round(p.pct * 100)}%</b></summary>
          ${p.chapters.map(ch => `<details class="ca-dc"><summary><span>Ch ${ch.n}: ${esc(ch.title)}</span>${X.bar(ch.pct)}<b>${Math.round(ch.pct * 100)}%</b></summary><ul class="ca-du">${ch.units.map(u => `<li><button class="ca-dun" data-u="${u.id}" ${u.status === 'built' ? '' : 'disabled'}><span>Unit ${u.n}: ${esc(u.title)}<small>${u.status === 'built' ? (u.tabs.length ? `Done: ${u.tabs.map(k => (X.TABS.find(x => x[0] === k) || [k, k])[1]).join(', ')}` : 'Not started') : 'Coming soon'}</small></span><b>${Math.round(u.pct * 100)}%</b></button></li>`).join('')}</ul></details>`).join('')}</details>`).join('')}</section>
      </div>`;
    const on = (id, fn) => { const b = host.querySelector('#' + id); if (b) b.onclick = fn; };
    on('cdViva', vivaHub); on('cdMock', mocks); on('cdRev', revise); on('cdExam', () => Ca.profile());
    host.querySelectorAll('.ca-dun').forEach(b => b.onclick = () => Ca.unit(b.dataset.u));
    host.querySelectorAll('.ca-qh').forEach(b => b.onclick = () => Ca.openQuestion(b.dataset.u, b.dataset.q)); on('cdWeak', X.weakScreen);
  }
  /* adapter → the shared dashboard engine's data shape (documented at the top of js/insights.js) */
  async function insData(D_) {
    const c = C(), built = await loadAll(await builtList()), path = {}, tree = [];
    built.forEach(b => {
      let P = tree.find(x => x.id === b.p.id); if (!P) tree.push(P = { id: b.p.id, name: `${X.paperLabel(b.p)} · ${b.p.name}`, children: [] });
      let Ch = P.children.find(x => x.id === b.c.id); if (!Ch) P.children.push(Ch = { id: b.c.id, name: `Ch ${b.c.n}: ${b.c.title}`, children: [] });
      const qs = {}; b.d.mcqs.forEach(q => { qs[`${b.u.id}#${q.id}`] = { q: q.q, a: q.options[q.answer], explain: q.explain }; });
      (b.d.cases || []).forEach(cs => cs.mcqs.forEach(q => { qs[`${b.u.id}#${q.id}`] = { q: `[Case: ${cs.title}] ${q.q}`, a: q.options[q.answer], explain: q.explain }; }));
      Ch.children.push({ id: b.u.id, name: `Unit ${b.u.n}: ${b.u.title}`, note: `${Math.round(X.unitProg(b.u.id) * 100)}% of the unit done`, questions: qs });
      path[b.u.id] = [b.p.id, b.c.id, b.u.id];
    });
    const events = [];
    c.mlog.forEach(([m, key, ok, secs]) => { const pa = path[key.split('#')[0]]; if (pa) events.push({ t: m * 6e4, path: pa, qid: key, ok: ok ? 1 : 0, secs, kind: 'mcq' }); });
    /* written answers: one event per checked attempt (marks checked now / checkable marks); skills = the scheme skills of its points.
       Photo answers waiting for the AI examiners carry no score and are left out. */
    Object.entries(c.writes).forEach(([key, h]) => { const pa = path[key.split('#')[0]]; if (pa) X.scored(h).forEach(a => { if (a.max) events.push({ t: Date.parse(a.d + 'T12:00:00Z'), path: pa, qid: key, ok: null, kind: 'write', score: a.score, max: a.max, secs: a.secs || 0, skills: [...new Set((a.skills || []).map(x => x[0]))] }); }); });
    Object.entries(c.viva).forEach(([key, h]) => { const pa = path[key.split('#')[0]]; if (pa) h.filter(a => a.status !== 'waiting').forEach(a => events.push({ t: Date.parse(a.d + 'T12:00:00Z'), path: pa, qid: key, ok: null, kind: 'write', score: a.pct / 10, max: 10, secs: a.secs || 0, skills: ['viva'] })); });
    events.sort((a, b) => a.t - b.t);
    const days = {}; Object.entries(c.time).forEach(([d, secs]) => { days[d] = { secs }; });
    const tests = c.tests.map(t => ({ d: t.d, name: t.kind === 'mock' ? `Mock: ${t.title}` : `${t.title} (${t.mode})`, pct: t.pct }));
    return { title: 'Dashboard', subtitle: `CA ${D_.levelName}`, rootName: 'All papers', levels: ['Paper', 'Chapter', 'Unit'], tree, events, days, tests,
      testLabel: 'Mock papers & MCQ sets', skills: { ...X.SKILL, viva: 'Viva — spoken answers' }, streak: { n: D_.streak.current, best: D_.streak.best },
      nextTest: c.exam ? { name: 'CA exam', date: c.exam } : undefined, minEvents: 8, answered: D_.mcq.answered };
  }
  async function dashboard() {
    const el = X.open('cadash'); el.innerHTML = '<p class="ca-load">Loading your dashboard…</p>';
    const data = await dashData();
    el.innerHTML = '<div id="cdHost" class="ca-dash"></div>'; const host = D.getElementById('cdHost');
    if (window.Insights && typeof Insights.dashboardFor === 'function' && window.SVDash) {
      try {
        const idata = await insData(data);
        renderDash(host, data, true);
        const sub = D.getElementById('cdEngine');
        Insights.dashboardFor(sub, { mode: 'ca', data: idata, onStart: () => builder(), startLabel: 'Build an MCQ set', onLeaf: p => Ca.unit(p[2]), leafLabel: 'Open unit' });
        return;
      } catch (e) { console.warn('Shared dashboard engine failed — using the CA dashboard', e); }
    }
    renderDash(host, data, false);
  }

  /* ---------- Question bank by marks: every written question of your course, grouped 2 / 3 / 4 / 5 / 6 / 8 / 10 marks ---------- */
  async function bank(fm = 'all', pid = 'all') {
    const el = X.open('practice'); el.innerHTML = '<p class="ca-load">Loading the question bank…</p>';
    const list = await loadAll(await builtList()), qs = [], mcqN = list.reduce((a, b) => a + b.d.mcqs.length, 0);
    list.forEach(b => b.d.questions.forEach((q, i) => qs.push({ b, q, i })));
    const papers = [...new Map(list.map(b => [b.p.id, b.p])).values()];
    const inP = qs.filter(x => pid === 'all' || x.b.p.id === pid), marks = [...new Set(inP.map(x => x.q.marks))].sort((a, b) => a - b);
    if (fm !== 'all' && !marks.includes(+fm)) fm = 'all';
    const show = inP.filter(x => fm === 'all' || x.q.marks === +fm), p0 = pid !== 'all' ? papers.find(p => p.id === pid) : (show[0] && show[0].b.p);
    el.innerHTML = ''; el.appendChild(back('Practice', practiceHub));
    el.insertAdjacentHTML('beforeend', `<h1 class="ca-h1 ca-onDark">Question bank — by marks</h1>
      <div class="card"><p class="ca-p">${qs.length} written questions from the units built so far, plus ${mcqN} one-mark MCQs. Learn what a 4-mark answer needs compared with an 8-mark one.</p>
        ${papers.length > 1 ? `<div class="ca-chipsel" role="group" aria-label="Paper"><button type="button" class="ca-cs" aria-pressed="${pid === 'all'}" data-pid="all">All papers</button>${papers.map(p => `<button type="button" class="ca-cs" aria-pressed="${pid === p.id}" data-pid="${p.id}">${esc(X.paperLabel(p))}</button>`).join('')}</div>` : ''}
        <div class="ca-chipsel" role="group" aria-label="Marks"><button type="button" class="ca-cs" aria-pressed="${fm === 'all'}" data-bm="all">All</button>${marks.map(m => `<button type="button" class="ca-cs" aria-pressed="${String(fm) === String(m)}" data-bm="${m}">${m}-mark <small>${inP.filter(x => x.q.marks === m).length}</small></button>`).join('')}<button type="button" class="ca-cs" data-bm="mcq">1-mark MCQs <small>${mcqN}</small></button></div>
        ${fm !== 'all' ? X.markGuide(+fm, p0 && p0, show.some(x => x.q.pad === 'legal')) : ''}</div>
      ${show.length ? `<div class="card"><ul class="ca-rvl ca-bank">${show.map(x => { const h = C().writes[`${x.b.u.id}#${x.q.id}`] || [], best = X.bestOf(h);
        return `<li><button class="ca-nopen" data-u="${x.b.u.id}" data-q="${esc(x.q.id)}"><span class="ca-qm">${x.q.marks}<small>marks</small></span><span><b>${esc(x.q.q.length > 150 ? x.q.q.slice(0, 147) + '…' : x.q.q)}</b><small>${esc(X.paperLabel(x.b.p))} · Ch ${x.b.c.n} · ${esc(x.b.u.title)} · ~${x.q.minutes} min${best != null ? ` · best ${fmt(best)}/${x.q.marks}` : ''}</small></span></button>${X.refChip ? X.refChip(x.b.u.id, x.q) : ''}</li>`; }).join('')}</ul></div>` : '<div class="card"><p class="ca-p">No questions with these marks yet.</p></div>'}`);
    el.querySelectorAll('[data-bm]').forEach(b => b.onclick = () => { tap('tap'); if (b.dataset.bm === 'mcq') return builder(); bank(b.dataset.bm, pid); });
    el.querySelectorAll('[data-pid]').forEach(b => b.onclick = () => { tap('tap'); bank(fm, b.dataset.pid); });
    el.querySelectorAll('.ca-bank [data-q]').forEach(b => b.onclick = () => { tap('open'); Ca.openQuestion(b.dataset.u, b.dataset.q); });
  }

  /* ---------- home tiles + practice hub ---------- */
  function homeTiles() {
    const c = C(); let ms = 0, mr = 0; Object.values(c.mcq).forEach(v => { ms += v.s; mr += v.s - v.w; });
    const vAll = vivaScored().flat(), wk = dayList(7).reduce((a, d) => a + (c.time[d] || 0), 0), rv = Object.keys(c.revise).length;
    return `<button class="card ca-dtile" id="caDashTile" aria-label="Open your CA dashboard"><span class="ca-k">📊 Your dashboard</span>
        <span class="ca-dmini"><span><b>${ms ? Math.round(mr / ms * 100) + '%' : '—'}</b><small>MCQ accuracy</small></span><span><b>${vAll.length ? Math.round(vAll.reduce((a, x) => a + x.pct, 0) / vAll.length) + '%' : '—'}</b><small>Viva</small></span><span><b>${durTxt(wk)}</b><small>This week</small></span><span><b>${activity().cur}</b><small>Day streak</small></span></span>
        <span class="ca-go">Open dashboard ▶</span></button>
      <div class="gsearch ca-search ca-hsearch"><span aria-hidden="true">🔍</span><input id="caHomeQ" placeholder="Search ICAI topics, lessons, your notes…" autocomplete="off" aria-label="Smart search" enterkeyhint="search"></div>
      <div class="ca-quick"><button class="ca-qt" id="caQViva"><b aria-hidden="true">🎙️</b>Viva</button><button class="ca-qt" id="caQMcq"><b aria-hidden="true">🧩</b>MCQ set</button><button class="ca-qt" id="caQMock"><b aria-hidden="true">📝</b>Mock paper</button><button class="ca-qt" id="caQNotes"><b aria-hidden="true">📚</b>My notes</button>${rv ? `<button class="ca-qt" id="caQRev"><b aria-hidden="true">🔁</b>Revise (${rv})</button>` : ''}</div>`;
  }
  function wireHome(el) {
    const on = (id, fn) => { const b = D.getElementById(id); if (b) b.onclick = () => { tap('open'); fn(); }; };
    on('caDashTile', dashboard); on('caQViva', vivaHub); on('caQMcq', () => builder()); on('caQMock', mocks); on('caQNotes', notes); on('caQRev', revise);
    const q = D.getElementById('caHomeQ'); if (q) { q.onkeydown = e => { if (e.key === 'Enter') search(q.value); }; q.onfocus = () => { if (!IDX) buildIndex(); }; q.oninput = () => { clearTimeout(q._t); if (q.value.trim().length >= 3) q._t = setTimeout(() => search(q.value), 700); }; }
  }
  function practiceHub() {
    const el = X.open('practice'), rv = Object.keys(C().revise).length;
    const tile = (id, e, t, s) => `<button class="card ca-hub" id="${id}"><b class="ca-hube" aria-hidden="true">${e}</b><span><b>${t}</b><small>${s}</small></span><span class="ca-chev" aria-hidden="true">›</span></button>`;
    el.innerHTML = `<h1 class="ca-h1 ca-onDark">Practice</h1><div class="ca-hubs">
      ${tile('phDaily', '🎯', 'Daily mix', '10 MCQs from units you opened — missed ones first')}
      ${tile('phBuild', '🧩', 'Build an MCQ set', 'Level › papers › chapters › difficulty · timer · practice or test')}
      ${tile('phCase', '📄', 'Case-study sets', 'A short case with 3–5 linked MCQs')}
      ${tile('phViva', '🎙️', 'Viva — speak & revise', 'Hear a question, answer out loud, see the key points you covered')}
      ${tile('phBank', '🧮', 'Question bank — by marks', '2, 4, 5, 8-mark questions and how to write each')}
      ${tile('phMock', '📝', 'Mock papers', 'Foundation Paper 1 in ICAI pattern — 3 hours, 100 marks')}
      ${tile('phRev', '🔁', `Revise these${rv ? ` (${rv})` : ''}`, 'Every MCQ you got wrong, until you get it right')}
      ${tile('phWeak', '📈', 'Weak spots & strengths', 'By unit and by examiner skill')}</div>`;
    const on = (id, fn) => { D.getElementById(id).onclick = () => { tap('open'); fn(); }; };
    on('phDaily', X.practiceDaily); on('phBuild', () => builder()); on('phCase', () => builder({ singles: false, cases: true }));
    on('phViva', vivaHub); on('phBank', () => bank()); on('phMock', mocks); on('phRev', revise); on('phWeak', X.weakScreen);
  }

  /* screens are history routes (Back returns to them — see Nav in js/app.js) */
  if (window.Nav) { dashboard = Nav.route('ca.dash', dashboard); vivaHub = Nav.route('ca.vivahub', vivaHub); builder = Nav.route('ca.builder', builder); revise = Nav.route('ca.revise', revise);
    mocks = Nav.route('ca.mocks', mocks); mockPaper = Nav.route('ca.mock', mockPaper); notes = Nav.route('ca.notes', notes); search = Nav.route('ca.search', search); practiceHub = Nav.route('ca.practicehub', practiceHub); bank = Nav.route('ca.bank', bank); }
  window.CaTools = { photos, _speechMerge: speechMerge, freshOrder, endless, bank, pickSet, dashboard, dashData, vivaTab, vivaHub, vivaDone, vivaScore, builder, revise, reviseMark, casesBlock, wireCases, mocks, mockPaper,
    saveBtn, applyHL, noteSheet, notes, hasNote, search, homeTiles, wireHome, practiceHub, _tokens: tokens,
    _m: { pairs, tokens, clauses, phraseIn, same, kwSame, pointHit, isNum } };   // matcher for js/ca-check.js
})();
