/* ================= CA Foundation — 📚 Key sections & rules (js/ca-keys.js) — loaded after js/ca-keys-data.js =================
   A review library: law sections Act by Act, accounting rules, QA formulas and economics laws (content: js/ca-keys-data.js).
   - search, filter by paper / Act or chapter, ★ saved list (ST.ca.keysSaved = {id: date}), "Mark as revised"
     (ST.ca.keysRev = {id: date}) with a "revise again" reminder after 7 days, read aloud (window.speak).
   - "Practise (n)": every item opens an MCQ run of the questions linked to it. Links (same code in node: tools/ca_keys_report.js):
       1. explicit tags on an MCQ: tags: ["ICA-s10"]
       2. a section cited in the MCQ (question / explanation / correct option) whose Act is known — named next to the
          section ("Section 10 of the Indian Contract Act"), or the MCQ belongs to that Act's chapter. A bare number in another
          chapter is never linked (no "Section 4" false links across Acts).
       3. keyword patterns of the item, only for MCQs inside the item's scope (its unit / chapters).
     Items with no linked question carry their own original MCQs (item.mcqs).
   - Chip "📚 Section 10 — ICA" inside every CA MCQ explanation (js/ca.js refChip → CaKeys.chips) opens the item in a sheet.
   Everything here is StudyVerse's own wording. */
(function () {
  'use strict';
  const DATA = (typeof window !== 'undefined' ? window.CaKeysData : null) || (typeof require === 'function' ? require('./ca-keys-data.js') : null);

  /* ================= pure matcher (also used by node: module.exports) ================= */
  const KM = (function () {
    const groups = {}, chAct = {}, acts = [];
    DATA.GROUPS.forEach(g => { groups[g.id] = g; if (g.act) { const re = new RegExp(g.act, 'i'); acts.push([g.id, re]); g.ch.forEach(c => { chAct[c] = g.id; }); } });
    const norm = s => String(s).toLowerCase().replace(/\s+/g, '');
    const baseOf = s => (String(s).match(/^\d+[a-z]?/) || [''])[0];
    const items = DATA.ITEMS.map(it => ({
      it, id: it.id, act: it.sec ? (it.act || it.g) : null, sec: (it.sec || []).map(norm),
      kw: (it.kw || []).map(k => new RegExp(k, 'i')), sc: it.sc || [it.u],
    }));
    const byId = Object.fromEntries(items.map(x => [x.id, x]));
    const chOf = uid => String(uid).replace(/-u\d+$/, '');
    /* "Section 10", "Sections 26 to 30", "s. 2(h)", "ss. 59–61", "u/s 138", "Sec. 64A", "Section 2(1)(n)" */
    const ONE = '\\d{1,3}[A-Za-z]?(?:\\s?\\([0-9a-z]{1,4}\\)){0,2}';
    const REF = new RegExp(`(?:\\bsections?|\\bsecs?\\.|\\bss?\\.|\\bu\\/s)\\s*(${ONE}(?:\\s*(?:,|and|to|&|–|—|-|or)\\s*${ONE})*)`, 'gi');
    function parseRefs(text) {
      const out = []; let m; REF.lastIndex = 0;
      while ((m = REF.exec(text))) {
        const list = m[1], start = m.index, end = m.index + m[0].length;
        const parts = list.split(/\s*(,|and|to|&|–|—|-|or)\s*/i); let prev = null, rangeNext = false;
        for (const p of parts) {
          if (!p) continue;
          if (/^(to|–|—|-)$/i.test(p)) { rangeNext = true; continue; }
          if (/^(,|and|&|or)$/i.test(p)) { rangeNext = false; continue; }
          const s = norm(p);
          if (rangeNext && prev && /^\d+$/.test(prev) && /^\d+$/.test(s) && +s > +prev && +s - +prev <= 15) { for (let k = +prev + 1; k <= +s; k++) out.push({ sec: String(k), base: String(k), start, end }); }
          else out.push({ sec: s, base: baseOf(s), start, end });
          prev = s; rangeNext = false;
        }
      }
      return out;
    }
    /* the Act a cited section belongs to: an Act named right after it ("Section 10 of the Indian Contract Act") or right
       before it in the same sentence ("Under the Partnership Act, 1932, section 13 …"); null if none */
    function actNear(text, start, end) {
      let after = text.slice(end, end + 80); const cut = after.search(/[;?!]|\.\s+[A-Z]/); if (cut >= 0) after = after.slice(0, cut);
      let best = null;
      for (const [id, re] of acts) { const m = re.exec(after); if (m && m.index <= 22 && !/section|\bs\.\s?\d/i.test(after.slice(0, m.index)) && (!best || m.index < best[1])) best = [id, m.index]; }
      if (best) return best[0];
      let before = text.slice(Math.max(0, start - 80), start); const bc = before.search(/[;?!][^;?!]*$|\.\s+[A-Z][^.]*$/); if (bc >= 0) before = before.slice(bc + 1);
      for (const [id, re] of acts) { const all = [...before.matchAll(new RegExp(re.source, 'gi'))]; const m = all[all.length - 1]; if (m) { const gap = before.length - (m.index + m[0].length); if (gap <= 30 && (!best || gap < best[1])) best = [id, gap]; } }
      return best ? best[0] : null;
    }
    /* What counts: the question, the correct option and the opening of the explanation. Later sentences of an explanation
       usually discuss the wrong options ("Section 148 defines bailment…"), so they are not used; neither is any section that
       appears in a wrong option. Keywords use the same text. */
    const sentences = t => String(t || '').split(/(?<=[.!?])\s+(?=[A-Z("“'])/);
    function info(uid, q) {
      q = q || {};
      const opts = Array.isArray(q.options) ? q.options.map(String) : [], ans = opts[q.answer] != null ? opts[q.answer] : '';
      const ex = sentences(q.explain), head = [q.q, ans].filter(Boolean).join(' \n ');
      const textSec = [head, ex[0] || ''].join(' \n '), text = textSec;
      const home = chAct[chOf(uid)] || null;
      const wrong = new Set(opts.filter((o, i) => i !== q.answer).flatMap(o => parseRefs(o).map(r => r.sec)));
      const inHead = new Set(parseRefs(head).map(r => r.sec));
      const refs = parseRefs(textSec).filter(r => inHead.has(r.sec) || !wrong.has(r.sec)).map(r => ({ ...r, act: actNear(textSec, r.start, r.end) || home }));
      return { uid: String(uid), text, refs, tags: Array.isArray(q.tags) ? q.tags : [] };
    }
    const secHit = (x, r) => x.sec.some(s => (s.includes('(') ? r.sec === s : r.base === s));
    function why(x, inf) {                       // how an MCQ links to an item: 'tag' | 'sec' | 'kw' | null
      if (inf.tags.includes(x.id)) return 'tag';
      if (x.act && inf.refs.some(r => r.act === x.act && secHit(x, r))) return 'sec';
      if (x.kw.length && x.sc.some(p => inf.uid === p || inf.uid.startsWith(p + '-'))) { for (const re of x.kw) if (re.test(inf.text)) return 'kw'; }
      return null;
    }
    /* pool: [{ uid, key, q, cs? }] → { id: [{ ...entry, why }] } — strongest links first */
    function index(pool) {
      const out = {}; items.forEach(x => { out[x.id] = []; });
      const rank = { tag: 0, sec: 1, kw: 2 };
      for (const e of pool) { const inf = info(e.uid, e.q); for (const x of items) { const w = why(x, inf); if (w) out[x.id].push({ ...e, why: w }); } }
      for (const id in out) out[id].sort((a, b) => rank[a.why] - rank[b.why]);
      return out;
    }
    /* items to show as chips under one MCQ: section / tag links first, then keyword links; at most n */
    function chipsFor(uid, q, n = 2) {
      const inf = info(uid, q), strong = [], weak = [];
      for (const x of items) { const w = why(x, inf); if (w === 'kw') weak.push(x); else if (w) strong.push(x); }
      return strong.concat(weak).slice(0, n).map(x => x.it);
    }
    const label = it => it.n || (it.sec ? `${it.sec.length > 1 ? 'Sections' : 'Section'} ${it.sec.map(s => s.replace(/^(\d+)([a-z])$/, (a, d, l) => d + l.toUpperCase())).join(', ')}` : 'Rule');
    const chipLabel = it => { const g = groups[it.g]; if (it.sec) return `Section ${String(it.sec[0]).replace(/^(\d+)([a-z])$/, (a, d, l) => d + l.toUpperCase())} — ${it.act ? groups[it.act].s : g.s}`; return `${it.t} — ${g.s}`; };
    const papersOf = it => { const s = new Set([groups[it.g].p]); (it.sc || []).forEach(p => { const m = String(p).match(/^fnd-p\d/); if (m) s.add(m[0]); }); if (it.sec) s.add('fnd-p2'); return [...s]; };
    return { groups, items, byId, parseRefs, info, why, index, chipsFor, label, chipLabel, papersOf, chOf };
  })();

  if (typeof window === 'undefined') { module.exports = { DATA, KM }; return; }

  /* ================= browser ================= */
  if (!window.Ca || !Ca._) return;
  const D = document, X = Ca._;
  const C = () => { const c = X.C(); c.keysSaved = c.keysSaved || {}; c.keysRev = c.keysRev || {}; return c; };
  const tap = k => { try { sfx(k); } catch (e) {} };
  const say = m => { try { if (window.A11Y) A11Y.announce(m); } catch (e) {} };
  const REVISE_DAYS = 7, RUN_MAX = 12;
  const PNAME = { 'fnd-p1': 'P1 Accounting', 'fnd-p2': 'P2 Law', 'fnd-p3': 'P3 QA', 'fnd-p4': 'P4 Economics' };
  const daysSince = d => { if (!d) return null; const a = new Date(d + 'T12:00:00'), b = new Date(X.todayISO() + 'T12:00:00'); return Math.round((b - a) / 864e5); };
  const isDue = id => { const n = daysSince(C().keysRev[id]); return n != null && n >= REVISE_DAYS; };
  const dueCount = () => DATA.ITEMS.filter(it => isDue(it.id)).length;
  const fmtD = d => { try { return new Date(d + 'T12:00:00').toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }); } catch (e) { return d; } };
  const addDays = (d, n) => { const x = new Date(d + 'T12:00:00'); x.setDate(x.getDate() + n); return `${x.getFullYear()}-${String(x.getMonth() + 1).padStart(2, '0')}-${String(x.getDate()).padStart(2, '0')}`; };
  const paperOf = it => KM.groups[it.g].p;
  const ownKey = (it, i) => `${it.u}#ky-${it.id}-${i + 1}`;
  const ownList = it => (it.mcqs || []).map((q, i) => ({ q: { topic: it.t, difficulty: 'core', ...q, id: `ky-${it.id}-${i + 1}`, tags: [it.id], own: true }, key: ownKey(it, i), uid: it.u }));

  /* ---------- question pool (loaded per paper, cached) ---------- */
  const pools = {}, idx = {};
  async function poolFor(pid) {
    if (pools[pid]) return pools[pid];
    return (pools[pid] = (async () => {
      const st = await X.structure('foundation'), p = st.papers.find(x => x.id === pid), out = [];
      if (!p) return out;
      const units = []; p.chapters.forEach(c => c.units.forEach(u => units.push(u)));
      await Promise.all(units.map(async u => {
        let d = null; try { d = await X.unitData(u.id); } catch (e) {}
        if (!d) return;
        const chTitle = `Ch ${(p.chapters.find(c => c.units.includes(u)) || {}).n}: ${(p.chapters.find(c => c.units.includes(u)) || {}).title || ''}`;
        (d.mcqs || []).forEach(q => out.push({ uid: u.id, key: `${u.id}#${q.id}`, q, chTitle }));
        (d.cases || []).forEach(cs => (cs.mcqs || []).forEach(q => out.push({ uid: u.id, key: `${u.id}#${q.id}`, q, cs, chTitle })));
      }));
      return out;
    })());
  }
  const allPids = ['fnd-p1', 'fnd-p2', 'fnd-p3', 'fnd-p4'];
  let idxAll = null;
  async function linkIndex(pids) {                // index over the pool of the given papers (cached per combination)
    const k = pids.slice().sort().join(',');
    if (!idx[k]) idx[k] = (async () => { const pool = (await Promise.all(pids.map(poolFor))).flat(); return KM.index(pool); })();
    return idx[k];
  }
  async function matchesFor(it) {
    const ix = idxAll ? await idxAll : await linkIndex(KM.papersOf(it));
    return ix[it.id] || [];
  }

  /* ---------- practise ---------- */
  async function practise(id, back) {
    const it = KM.byId[id] && KM.byId[id].it; if (!it) return;
    let m = []; try { m = await matchesFor(it); } catch (e) {}
    const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
    const seen = new Set(), list = [];
    const strong = m.filter(x => x.why !== 'kw'), weak = m.filter(x => x.why === 'kw');
    for (const e of [...ownList(it), ...shuffle(strong), ...shuffle(weak)]) { if (seen.has(e.key)) continue; seen.add(e.key); list.push(e); }
    const pick = shuffle(list.slice(0, Math.max(RUN_MAX, 0))).slice(0, RUN_MAX);
    if (!pick.length) { toast('No questions linked to this item yet'); return; }
    const items = pick.map(e => ({ q: e.q, key: e.key, uid: e.uid, cs: e.cs, ch: KM.chOf(e.uid), chTitle: e.chTitle || '' }));
    const T = window.CaTools;
    if (T && T.startSet) T.startSet(items, { mode: 'practice', perQ: 0, title: `📚 ${KM.label(it)} · ${it.t}`, again: back || (() => open({ focus: id })), againLabel: 'Back to key rules' });
  }

  /* ---------- read aloud ---------- */
  let speaking = null;
  function readAloud(it, btn) {
    try { if (speaking === it.id && window.speechSynthesis) { speechSynthesis.cancel(); speaking = null; if (btn) btn.textContent = '🔊 Read aloud'; return; } } catch (e) {}
    const clean = s => String(s || '').replace(/₹/g, 'rupees ').replace(/\bs\.(\d)/g, 'section $1').replace(/[·•]/g, ',').replace(/→/g, ' leads to ').replace(/≥/g, ' at least ').replace(/≤/g, ' at most ');
    const txt = [`${KM.label(it)}. ${it.t}.`, clean(it.r), it.tip ? 'Exam tip. ' + clean(it.tip) : '', it.hook ? 'Memory hook. ' + clean(it.hook) : ''].filter(Boolean).join(' ');
    try { if (window.speechSynthesis) speechSynthesis.cancel(); } catch (e) {}
    if (typeof window.speak === 'function') { window.speak(txt); speaking = it.id; if (btn) btn.textContent = '⏹ Stop reading'; say('Reading aloud'); }
    else toast('Read aloud is not available on this device');
  }

  /* ---------- item HTML ---------- */
  function bodyHTML(it, n) {
    const c = C(), saved = !!c.keysSaved[it.id], rev = c.keysRev[it.id], due = isDue(it.id), today = rev === X.todayISO();
    return `<p class="ky-rule">${esc(it.r)}</p>
      ${it.f ? `<div class="ky-f" role="note" aria-label="Formula"><span class="ca-k">Formula</span><code>${esc(it.f)}</code></div>` : ''}
      ${it.ex ? `<div class="ky-ex"><span class="ca-k">Worked example</span><p class="ca-p"><b>${esc(it.ex[0])}</b></p><ol class="ky-ol">${it.ex[1].map(s => `<li>${esc(s)}</li>`).join('')}</ol><p class="ky-ans">Answer: <b>${esc(it.ex[2])}</b></p></div>` : ''}
      <dl class="ky-dl">${it.tip ? `<dt>Exam tip · common trap</dt><dd>${esc(it.tip)}</dd>` : ''}${it.hook ? `<dt>Memory hook</dt><dd class="ky-hook">💡 ${esc(it.hook)}</dd>` : ''}</dl>
      <div class="ca-btns ky-btns">
        <button type="button" class="btn ky-go" data-kyp="${esc(it.id)}">▶ Practise${n == null ? '' : ` (${n})`}</button>
        <button type="button" class="btn ghost ky-save" data-kys="${esc(it.id)}" aria-pressed="${saved}">${saved ? '★ Saved to my revision' : '☆ Save to my revision'}</button>
        <button type="button" class="btn ghost ky-rev" data-kyr="${esc(it.id)}" aria-pressed="${!!today}">${today ? '✓ Revised today' : '✓ Mark as revised'}</button>
        <button type="button" class="btn ghost ky-say" data-kya="${esc(it.id)}">🔊 Read aloud</button>
        <button type="button" class="btn ghost" data-kyu="${esc(it.u)}">📖 Study the unit</button></div>
      <p class="ky-revnote" data-kyrn="${esc(it.id)}">${revNote(rev, due)}</p>`;
  }
  const revNote = (rev, due) => (rev ? (due ? `🔁 Last revised ${fmtD(rev)} — time to revise it again.` : `Last revised ${fmtD(rev)} · revise again after ${fmtD(addDays(rev, REVISE_DAYS))}.`) : 'Not revised yet.');
  function badges(it) {
    const c = C(), b = [];
    if (c.keysSaved[it.id]) b.push('<span class="ky-b sv" title="Saved">★</span>');
    if (isDue(it.id)) b.push('<span class="ky-b due">🔁 revise again</span>');
    else if (c.keysRev[it.id]) b.push(`<span class="ky-b ok">✓ ${esc(fmtD(c.keysRev[it.id]))}</span>`);
    return b.join('');
  }
  function itemHTML(it, n, openIt) {
    const g = KM.groups[it.g];
    return `<details class="card ky-item" id="ky-${esc(it.id)}" data-kyid="${esc(it.id)}"${openIt ? ' open' : ''}>
      <summary><span class="ky-lab">${esc(KM.label(it))}<i> · ${esc(g.s)}</i></span><b class="ky-t">${esc(it.t)}</b><span class="ky-bs">${badges(it)}</span></summary>
      <div class="ky-body">${openIt ? bodyHTML(it, n) : ''}</div></details>`;
  }

  /* ---------- library screen ---------- */
  const S = { paper: 'all', g: 'all', q: '', view: 'all', from: '' };
  let counts = {};
  function filtered() {
    const c = C(), q = S.q.trim().toLowerCase();
    const sm = q.match(/^(?:s|sec|section|u\/s)\.?\s*(\d+[a-z]?(?:\([0-9a-z]+\))*)$/);
    const toks = q.split(/\s+/).filter(Boolean);
    return DATA.ITEMS.filter(it => {
      if (S.paper !== 'all' && paperOf(it) !== S.paper) return false;
      if (S.g !== 'all' && it.g !== S.g) return false;
      if (S.view === 'saved' && !c.keysSaved[it.id]) return false;
      if (S.view === 'due' && !isDue(it.id)) return false;
      if (!q) return true;
      if (sm) return (it.sec || []).some(s => s === sm[1] || s.replace(/\(.*$/, '') === sm[1]);
      const hay = [it.id, KM.label(it), it.t, it.r, it.f, it.tip, it.hook, KM.groups[it.g].n, KM.groups[it.g].s, (it.ex || []).flat().join(' ')].join(' ').toLowerCase();
      return toks.every(t => hay.includes(t));
    });
  }
  function paintList() {
    const box = D.getElementById('kyList'); if (!box) return;
    const list = filtered(); let lastG = null, html = '';
    if (S.paper !== 'all' && S.view === 'all' && !S.q && S.g === 'all') { const P = DATA.PAPERS[S.paper]; if (P) html += `<div class="card ky-intro">${S.paper === 'fnd-p1' ? '<span class="ca-k">Standards at Foundation</span>' : `<span class="ca-k">${esc(P.n)}</span>`}${P.intro.map(t => `<p class="ca-p">${esc(t)}</p>`).join('')}${S.paper === 'fnd-p1' ? '<button type="button" class="btn ghost" data-kyu="fnd-p1-ch01-u07">📖 Study Unit 7: Accounting Standards</button>' : ''}</div>`; }
    for (const it of list) { if (it.g !== lastG) { html += `<h2 class="ky-gh ca-onDark">${esc(KM.groups[it.g].n)} <small>${esc(PNAME[paperOf(it)])}</small></h2>`; lastG = it.g; } html += itemHTML(it, counts[it.id], false); }
    if (!list.length) html += `<div class="card"><p class="ca-p">${S.view === 'saved' ? 'Nothing saved yet. Open any item and tap ☆ Save to my revision — it will appear here.' : S.view === 'due' ? 'Nothing is due. Items you mark as revised come back here after 7 days.' : 'No match. Try a section number like "s 73", or a word like "lien" or "multiplier".'}</p></div>`;
    box.innerHTML = html;
    const n = D.getElementById('kyN'); if (n) n.textContent = `${list.length} item${list.length === 1 ? '' : 's'}`;
  }
  function paintChips() {
    const c = C(), sv = Object.keys(c.keysSaved).filter(id => KM.byId[id]).length, due = dueCount();
    const pc = D.getElementById('kyPapers'); if (pc) pc.innerHTML = [['all', 'All papers']].concat(allPids.map(p => [p, PNAME[p]])).map(([k, n]) => `<button type="button" class="ca-cs" aria-pressed="${S.paper === k}" data-kypa="${k}">${esc(n)} <small>${k === 'all' ? DATA.ITEMS.length : DATA.ITEMS.filter(it => paperOf(it) === k).length}</small></button>`).join('');
    const gc = D.getElementById('kyGroups');
    if (gc) { const gs = DATA.GROUPS.filter(g => S.paper !== 'all' && g.p === S.paper); gc.hidden = !gs.length;
      gc.innerHTML = gs.length ? [['all', S.paper === 'fnd-p2' ? 'All Acts' : 'All chapters']].concat(gs.map(g => [g.id, g.s])).map(([k, n]) => `<button type="button" class="ca-cs" aria-pressed="${S.g === k}" data-kyg="${k}">${esc(n)}${k === 'all' ? '' : ` <small>${DATA.ITEMS.filter(it => it.g === k).length}</small>`}</button>`).join('') : ''; }
    const vc = D.getElementById('kyViews'); if (vc) vc.innerHTML = [['all', 'Everything'], ['saved', `★ My saved list (${sv})`], ['due', `🔁 Revise again (${due})`]].map(([k, n]) => `<button type="button" class="ca-cs" aria-pressed="${S.view === k}" data-kyv="${k}">${esc(n)}</button>`).join('');
    const bn = D.getElementById('kyDue'); if (bn) { bn.hidden = !(due && S.view !== 'due'); bn.innerHTML = due ? `<span>🔁 <b>${due}</b> item${due === 1 ? ' is' : 's are'} due for another look — you revised ${due === 1 ? 'it' : 'them'} ${REVISE_DAYS}+ days ago.</span><button type="button" class="btn ghost" data-kyv="due">Show them</button>` : ''; }
  }
  function repaint() { paintChips(); paintList(); }
  function backTo() {
    if (S.from === 'practice' && window.CaTools) return CaTools.practiceHub();
    if (S.from === 'focus' && window.CaSpeed) return CaSpeed.focusList();
    if (/^paper:/.test(S.from)) return Ca.paper('foundation', S.from.slice(6));
    return Ca.home();
  }
  /* opts: { paper, g, view: 'all'|'saved'|'due', q, focus: item id, from: 'home'|'practice'|'focus'|'paper:<pid>' } */
  async function open(opts = {}) {
    Object.assign(S, { paper: 'all', g: 'all', q: '', view: 'all', from: '' }, opts);
    if (opts.focus && KM.byId[opts.focus]) { const it = KM.byId[opts.focus].it; S.paper = paperOf(it); S.g = 'all'; S.view = 'all'; S.q = ''; }
    const el = X.open(S.from === 'practice' ? 'practice' : 'world');
    const bl = { practice: 'Practice', focus: 'Exam focus list' }[S.from] || (/^paper:/.test(S.from) ? 'Paper' : 'CA Journey');
    el.innerHTML = `<div id="kyRoot"><button class="back" id="kyBack">← ${esc(bl)}</button>
      <h1 class="ca-h1 ca-onDark">📚 Key sections &amp; rules</h1>
      <p class="ca-onDark2">CA Foundation · the sections, rules and formulas to revise again and again — each with an exam tip, a memory hook and linked MCQs.</p>
      <div class="card ky-tools"><div class="gsearch ca-search"><span aria-hidden="true">🔍</span><input id="kyQ" type="search" placeholder='Search: "s 73", "lien", "multiplier", "NRV"…' autocomplete="off" aria-label="Search key sections and rules" value="${esc(S.q)}"></div>
        <div class="ca-chipsel" role="group" aria-label="Paper" id="kyPapers"></div>
        <div class="ca-chipsel" role="group" aria-label="Act or chapter" id="kyGroups" hidden></div>
        <div class="ca-chipsel" role="group" aria-label="Show" id="kyViews"></div>
        <p class="ca-note"><span id="kyN"></span> · <span id="kyLink">linking questions…</span></p></div>
      <div class="card ky-due" id="kyDue" hidden></div>
      <div id="kyList" aria-live="off"></div>
      <p class="ca-note ca-onDark2">StudyVerse's own summaries — read the section or standard in your ICAI study material for the exact wording.</p></div>`;
    D.getElementById('kyBack').onclick = () => { tap('tap'); backTo(); };
    const qi = D.getElementById('kyQ'); qi.oninput = () => { clearTimeout(qi._t); qi._t = setTimeout(() => { S.q = qi.value; paintList(); }, 120); };
    const root = D.getElementById('kyRoot'); root.addEventListener('click', onClick); root.addEventListener('toggle', onToggle, true);
    repaint();
    if (S.focus) setTimeout(() => focusItem(S.focus), 30);
    loadCounts();
  }
  async function loadCounts() {
    const ln = D.getElementById('kyLink');
    try {
      idxAll = idxAll || linkIndex(allPids); const ix = await idxAll;
      counts = Object.fromEntries(DATA.ITEMS.map(it => [it.id, new Set((ix[it.id] || []).map(e => e.key).concat(ownList(it).map(e => e.key))).size]));
      const tot = Object.values(counts).reduce((a, b) => a + b, 0);
      if (ln && ln.isConnected) ln.textContent = `${tot.toLocaleString('en-IN')} question links`;
      D.querySelectorAll('.ky-go[data-kyp]').forEach(b => { const n = counts[b.dataset.kyp]; if (n != null) b.textContent = `▶ Practise (${n})`; });
    } catch (e) { if (ln) ln.textContent = 'questions load when you tap Practise'; }
  }
  function focusItem(id) {
    const d = D.getElementById('ky-' + id); if (!d) return;
    d.open = true; fillBody(d);
    d.scrollIntoView({ block: 'start', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    d.classList.add('ca-reflash'); setTimeout(() => d.classList.remove('ca-reflash'), 2400);
    const s = d.querySelector('summary'); if (s) s.focus({ preventScroll: true });
  }
  function fillBody(d) { const b = d.querySelector('.ky-body'); if (b && !b.firstChild) { const it = KM.byId[d.dataset.kyid].it; b.innerHTML = bodyHTML(it, counts[it.id]); } }
  function onToggle(e) { const d = e.target; if (d && d.classList && d.classList.contains('ky-item') && d.open) fillBody(d); }
  function refreshItem(id) {
    D.querySelectorAll(`[data-kyid="${CSS.escape(id)}"]`).forEach(d => { const it = KM.byId[id].it; const bs = d.querySelector('.ky-bs'); if (bs) bs.innerHTML = badges(it); const b = d.querySelector('.ky-body'); if (b && b.firstChild) b.innerHTML = bodyHTML(it, counts[id]); });
    const sh = D.getElementById('kySheet'); if (sh && sh.dataset.kyid === id) { const b = sh.querySelector('.ky-body'); if (b) b.innerHTML = bodyHTML(KM.byId[id].it, counts[id]); }
  }
  function toggleSave(id) {
    const c = C(); if (c.keysSaved[id]) { delete c.keysSaved[id]; toast('Removed from your saved list'); } else { c.keysSaved[id] = X.todayISO(); toast('★ Saved to your revision list'); }
    save(); tap('tap'); refreshItem(id); paintChips(); if (S.view === 'saved' && D.getElementById('kyList')) paintList();
  }
  function markRevised(id) {
    const c = C(); if (c.keysRev[id] === X.todayISO()) { toast('Already marked as revised today'); return; }
    c.keysRev[id] = X.todayISO(); save(); tap('correct'); toast(`Marked as revised — it comes back for revision after ${REVISE_DAYS} days`);
    refreshItem(id); paintChips(); if (S.view === 'due' && D.getElementById('kyList')) paintList();
  }
  function onClick(e) {
    const t = e.target.closest && e.target.closest('button'); if (!t) return;
    const ds = t.dataset;
    if (ds.kypa) { tap('tap'); S.paper = ds.kypa; S.g = 'all'; repaint(); return; }
    if (ds.kyg) { tap('tap'); S.g = ds.kyg; repaint(); return; }
    if (ds.kyv) { tap('tap'); S.view = ds.kyv; repaint(); window.scrollTo(0, 0); return; }
    if (actions(t)) e.preventDefault();
  }
  function actions(t) {          // buttons inside an item body (library or sheet)
    const ds = t.dataset;
    if (ds.kyp) { tap('open'); const sh = D.getElementById('kySheet'); if (sh) closeSheet(true); practise(ds.kyp); return true; }
    if (ds.kys) { toggleSave(ds.kys); return true; }
    if (ds.kyr) { markRevised(ds.kyr); return true; }
    if (ds.kya) { readAloud(KM.byId[ds.kya].it, t); return true; }
    if (ds.kyu) { tap('open'); const sh = D.getElementById('kySheet'); if (sh) closeSheet(true); Ca.unit(ds.kyu); return true; }
    return false;
  }

  /* ---------- chips inside MCQ explanations + the item sheet ---------- */
  function chips(uidOrKey, q) {
    try {
      const uid = String(uidOrKey || '').split('#')[0]; if (!/^fnd-p[1-4]-/.test(uid) || !q) return '';
      const its = KM.chipsFor(uid, q, 2); if (!its.length) return '';
      return `<span class="ky-chips">${its.map(it => `<button type="button" class="ky-chip" data-kychip="${esc(it.id)}" aria-label="Key rule: ${esc(KM.chipLabel(it))}. Opens the rule.">📚 ${esc(KM.chipLabel(it))}</button>`).join('')}</span>`;
    } catch (e) { return ''; }
  }
  let sheetClose = null;
  function closeSheet(now) { if (sheetClose) sheetClose(now); }
  function sheet(id) {
    const x = KM.byId[id]; if (!x) return; const it = x.it, g = KM.groups[it.g];
    const old = D.getElementById('kySheet'); if (old) old.remove();
    const back = D.activeElement;
    const sh = D.createElement('div'); sh.className = 'sheet ky-sheet'; sh.id = 'kySheet'; sh.dataset.kyid = id; sh.setAttribute('data-nonav', '');
    sh.setAttribute('role', 'dialog'); sh.setAttribute('aria-modal', 'true'); sh.setAttribute('aria-labelledby', 'kyShT');
    sh.innerHTML = `<div class="sheet-in"><div class="sheet-grab"></div>
      <div class="ca-refhead"><button type="button" class="btn ghost" data-kyclose>← Back to question</button></div>
      <p class="ca-k">📚 Key sections &amp; rules › ${esc(g.n)}</p>
      <article class="card ky-item ky-open"><span class="ky-lab">${esc(KM.label(it))}<i> · ${esc(g.s)}</i></span><h2 class="ca-h2s" id="kyShT">${esc(it.t)}</h2><div class="ky-body">${bodyHTML(it, counts[id])}</div></article>
      <div class="ca-btns"><button type="button" class="btn ghost" data-kylib="${esc(id)}">Open in Key sections &amp; rules</button><button type="button" class="btn" data-kyclose>Back to question</button></div></div>`;
    D.body.appendChild(sh);
    let closed = false;
    const finish = () => { if (closed) return; closed = true; sheetClose = null; window.removeEventListener('popstate', onPop, true); sh.classList.remove('show'); setTimeout(() => sh.remove(), 250); if (back && back.focus && back.isConnected) try { back.focus({ preventScroll: true }); } catch (e) {} };
    const onPop = e => { e.stopImmediatePropagation(); finish(); };
    try { history.pushState(Object.assign({}, history.state || {}, { kySheet: 1 }), ''); } catch (e) {}
    window.addEventListener('popstate', onPop, true);
    const close = () => { if (closed) return; try { history.back(); } catch (e) { finish(); } setTimeout(finish, 400); };
    const drop = () => { window.removeEventListener('popstate', onPop, true); closed = true; sheetClose = null; sh.classList.remove('show'); setTimeout(() => sh.remove(), 0); };   // drop .show first: js/a11y.js then lifts the background's inert
    sheetClose = now => { if (now) { drop(); try { history.back(); } catch (e) {} } else close(); };
    sh.addEventListener('click', e => {
      if (e.target === sh) { close(); return; }
      const b = e.target.closest('button'); if (!b) return;
      if (b.hasAttribute('data-kyclose')) { close(); return; }
      if (b.dataset.kylib) { const fid = b.dataset.kylib; drop(); setTimeout(() => open({ focus: fid }), 0); return; }
      actions(b);
    });
    sh.addEventListener('keydown', e => { if (e.key === 'Escape') { e.stopPropagation(); close(); } });
    requestAnimationFrame(() => { sh.classList.add('show'); const h = sh.querySelector('[data-kyclose]'); if (h) h.focus({ preventScroll: true }); });
    if (counts[id] == null) matchesFor(it).then(m => { counts[id] = new Set(m.map(e => e.key).concat(ownList(it).map(e => e.key))).size; const b = sh.querySelector('.ky-go'); if (b && b.isConnected) b.textContent = `▶ Practise (${counts[id]})`; }).catch(() => {});
  }
  D.addEventListener('click', e => { const b = e.target.closest && e.target.closest('.ky-chip'); if (!b) return; e.preventDefault(); e.stopPropagation(); tap('open'); sheet(b.dataset.kychip); }, true);

  /* own MCQs, looked up by key (speed drill and "Revise these" find questions by key) */
  function ownQ(key) {
    const m = String(key).match(/^([^#]+)#ky-(.+)-(\d+)$/); if (!m) return null;
    const x = KM.byId[m[2]]; if (!x) return null; const e = ownList(x.it)[+m[3] - 1];
    return e && e.key === key ? { q: e.q, uid: e.uid } : null;
  }

  /* ---------- styles (CA pro look) ---------- */
  const STYLE = `
.ky-tools .ca-chipsel{margin-top:8px}
.ky-gh{font-size:15px;margin:18px 4px 6px;font-weight:800;letter-spacing:.2px}.ky-gh small{font-weight:700;opacity:.75;font-size:12px;margin-left:6px}
.ky-item{padding:0;margin:0 0 8px}
.ky-item>summary{cursor:pointer;list-style:none;display:grid;grid-template-columns:1fr auto;gap:2px 8px;align-items:center;padding:12px 38px 12px 14px;min-height:44px;position:relative}
.ky-item>summary::-webkit-details-marker{display:none}
.ky-item>summary::after{content:'›';position:absolute;right:12px;top:50%;margin-top:-14px;font-size:24px;line-height:1;color:#74561F;transition:transform .2s}
.ky-item[open]>summary::after{transform:rotate(90deg)}
@media (prefers-reduced-motion:reduce){.ky-item>summary::after{transition:none}}
.ky-lab{grid-column:1;font-size:11.5px;font-weight:800;letter-spacing:.3px;text-transform:uppercase;color:#74561F}.ky-lab i{font-style:normal;opacity:.8;text-transform:none;letter-spacing:0}
.ky-t{grid-column:1;font-size:15.5px;line-height:1.3}
.ky-bs{grid-column:2;grid-row:1/3;display:flex;flex-direction:column;align-items:flex-end;gap:3px}
.ky-b{font-size:11.5px;font-weight:800;border-radius:999px;padding:2px 8px;white-space:nowrap}.ky-b.sv{color:#8a6100;background:#FFF3CF}.ky-b.ok{color:#1d5c3a;background:#E7F3EA}.ky-b.due{color:#8f1d1a;background:#FDE4E3}
.ky-body{padding:0 14px 12px}.ky-open .ky-body{padding:0}.ky-open{padding:14px}
.ky-rule{font-size:15px;line-height:1.5;margin:4px 0 8px}
.ky-f{background:#15161C;color:#F4EAD8;border-radius:8px;padding:8px 10px;margin:6px 0}.ky-f .ca-k{color:#E9D3A0}.ky-f code{display:block;white-space:pre-wrap;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:14px;line-height:1.5;margin-top:2px}
.ky-ex{background:#F7F3EA;border-radius:8px;padding:8px 10px;margin:8px 0}.ky-ol{margin:4px 0 6px;padding-left:22px;font-size:14px;line-height:1.45}.ky-ans{margin:4px 0 0;font-size:14px}
.ky-dl{margin:8px 0 6px}.ky-dl dt{font-size:11.5px;font-weight:800;letter-spacing:.3px;text-transform:uppercase;color:#74561F;margin-top:6px}.ky-dl dd{margin:2px 0 0;font-size:14.5px;line-height:1.45}
.ky-hook{background:#FBF4E4;border-radius:6px;padding:4px 8px}
.ky-btns .btn,.ky-due .btn{width:auto}.ky-btns .btn{min-height:44px;flex:0 1 auto;padding-left:14px;padding-right:14px;font-size:14px}.ky-btns .ky-go{flex:1 1 100%;font-size:15.5px}
@media (min-width:700px){.ky-btns .ky-go{flex:0 1 auto;min-width:180px}}.ky-save[aria-pressed=true]{background:#FFF3CF;border-color:#C9A76A}.ky-rev[aria-pressed=true]{background:#E7F3EA;border-color:#2E8B57;color:#1d5c3a}
.ky-revnote{font-size:12.5px;color:var(--muted);margin:6px 0 0}
.ky-due{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;border-left:4px solid #B71C2C}
.ky-intro .ca-p{margin:4px 0 8px}
.ky-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.ky-chip{position:relative;min-height:36px;border-radius:999px;border:1.5px solid var(--ca-gold,#C9A76A);background:#FBF4E4;color:#5B0F1B;font:inherit;font-size:12.5px;font-weight:800;padding:4px 12px;cursor:pointer;text-align:left}
.ky-chip::after{content:'';position:absolute;left:50%;top:50%;width:max(100%,44px);height:max(100%,44px);transform:translate(-50%,-50%)}
.ky-chip:focus-visible,.ky-item>summary:focus-visible{outline:3px solid #C9A76A;outline-offset:2px}
html.sv-hc .ky-chip,html.sv-hc .ky-hook,html.sv-hc .ky-ex,html.sv-hc .ky-b{background:#fff;color:#000;border:2px solid #000}html.sv-hc .ky-f{background:#000;color:#fff;border:2px solid #fff}
@media (forced-colors:active){.ky-chip,.ky-b,.ky-f{border:2px solid ButtonText}}`;
  const st = D.createElement('style'); st.id = 'caKeysCss'; st.textContent = STYLE; D.head.appendChild(st);

  if (window.Nav) open = Nav.route('ca.keys', open);
  window.CaKeys = { open, practise, chips, sheet, ownQ, dueCount, savedCount: () => Object.keys(C().keysSaved).filter(id => KM.byId[id]).length, KM, DATA };
})();
