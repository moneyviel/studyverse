/* Knowtopia — crossword word helpers (js/pz-words.js), used by js/puzzles.js.
   PzWords.source(sp, e)  → { path: [subject/paper, chapter, topic/unit], open() }  where the answer comes from;
                            open() shows a pop-up with that topic's lesson (school) or unit concepts (CA) and a Close button.
   PzWords.hints(sp, e)   → up to 5 hints, gentlest first: [{ ic, label, text }]
     Every hint is taken from the course files themselves (nothing is invented), so it is always correct:
       🔁 another clue for the same word (a quiz question / match pair / quick-reference line that has it as the answer)
       ⚖️ often compared with … ("X vs Y" in the lesson)   ·   🔤 short form / full form ("Goods and Services Tax (GST)")
       🌍 a real-life example or 📖 a lesson sentence with the word hidden as _____
       🧭 the topic it is from   ·   🔡 first and last letter   ·   🔀 the letters jumbled
   The answer is never shown inside a hint: any sentence that still contains a part of it is skipped. */
(function () {
  'use strict';
  const D = document;
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const X = () => (window.Ca && Ca._) || null;
  const sq = s => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
  const sentences = t => sq(t).replace(/([a-z0-9)\]'"’”][.!?])\s+(?=[A-Z“"‘'(])/g, '$1\u0000').split('\u0000').map(sq).filter(Boolean);
  const words = s => sq(s).split(' ').filter(Boolean).length;
  const reEsc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const subjName = (g, sid) => { try { return ((CUR.grades[g] || {}).subjects || []).find(s => s.id === sid).name; } catch (e) { return sid; } };

  /* the term behind an entry (its topic id / unit id) */
  async function termOf(sp, e) {
    try {
      const T = await Puzzles._terms(sp.sc), all = (T.own || []).concat(T.near || []);
      return all.find(t => t.a === e.a && t.clue === e.clue) || all.find(t => t.a === e.a) || null;
    } catch (x) { return null; }
  }
  /* where the word lives: school → { k:'s', subj, ch, topic } · CA → { k:'c', paper, ch, unit, data } */
  const SRC = {};
  async function where(sp, e) {
    const key = JSON.stringify(sp.sc) + '|' + e.a;
    if (SRC[key]) return SRC[key];
    const t = await termOf(sp, e); let r = null;
    try {
      if (sp.sc.k === 's') {
        const g = sp.sc.g, sid = sp.sc.sid, d = await subjectData(g, sid);
        const chs = (d && d.chapters) || [];
        const find = id => { for (const c of chs) for (const tp of c.topics || []) if (tp.id === id) return { c, tp }; return null; };
        let f = t && t.tid ? find(t.tid) : null;
        if (!f) { const c = chs[sp.sc.ci]; if (c) f = { c, tp: null }; }
        if (f) r = { k: 's', subj: subjName(g, sid), ch: f.c, topic: f.tp, chapters: chs, ci: chs.indexOf(f.c) };
      } else if (sp.sc.k === 'c') {
        const x = X(); if (x && t && t.uid) {
          const st = await x.structure(x.levelOf(t.uid)), f = x.findUnit(st, t.uid), data = await x.unitData(t.uid);
          if (f) r = { k: 'c', paper: f.p, ch: f.c, unit: f.u, data };
        }
        if (!r && x) {               // no unit known: at least the chapter
          const lvl = { fnd: 'foundation', int: 'inter', fin: 'final' }[String(sp.sc.ch).split('-')[0]] || 'foundation';
          const st = await x.structure(lvl);
          for (const p of st.papers) for (const c of p.chapters) if (c.id === sp.sc.ch) r = { k: 'c', paper: p, ch: c, unit: null, data: null };
        }
      }
    } catch (x) { console.warn('pz source', x); }
    return (SRC[key] = r);
  }
  const pathOf = r => !r ? [] : r.k === 's'
    ? [r.subj, `Ch ${r.ch.n || ''}: ${r.ch.title || ''}`.trim(), r.topic ? r.topic.title : ''].filter(Boolean)
    : [`${r.paper.name}`, `Ch ${r.ch.n || ''}: ${r.ch.title || ''}`.trim(), r.unit ? `Unit ${r.unit.n}: ${r.unit.title}` : ''].filter(Boolean);

  /* ---------- the pop-up: read the topic / unit, then Close ---------- */
  function sheet(title, sub, body) {
    const sh = D.createElement('div'); sh.className = 'sheet show pzw-sheet'; sh.setAttribute('role', 'dialog'); sh.setAttribute('aria-modal', 'true'); sh.setAttribute('aria-label', title);
    sh.innerHTML = `<div class="sheet-in"><div class="sheet-grab" aria-hidden="true"></div><div class="pzw-pop"><span class="tag">📍 Where this word is from</span><h3>${E(title)}</h3>${sub ? `<p class="sub">${sub}</p>` : ''}<div class="pzw-body">${body}</div>
      <button class="btn" type="button" data-close="1">Close</button></div></div>`;
    const close = () => { sh.classList.remove('show'); setTimeout(() => sh.remove(), 250); };
    sh.querySelector('[data-close]').onclick = close;
    sh.addEventListener('click', ev => { if (ev.target === sh) close(); });
    D.body.appendChild(sh); css();
    setTimeout(() => { const b = sh.querySelector('h3'); if (b) { b.tabIndex = -1; try { b.focus(); } catch (x) {} } }, 60);
  }
  const hiAns = (txt, e) => {          // highlight the answer inside the lesson text (the student already wrote it)
    let h = E(txt); const w = sq(e.disp || e.a); if (!w) return h;
    try { h = h.replace(new RegExp('(' + reEsc(E(w)) + ')', 'gi'), '<mark>$1</mark>'); } catch (x) {}
    return h;
  };
  function openSource(r, e) {
    if (!r) return;
    const path = pathOf(r).map(E).join(' <b>›</b> ');
    if (r.k === 's') {
      const tp = r.topic, L = (tp && tp.learn) || {}, rv = (tp && tp.revise) || {};
      let body = '';
      if (tp) {
        if (L.points && L.points.length) body += `<h4>📖 Learn</h4><ul>${L.points.map(p => `<li>${hiAns(p, e)}</li>`).join('')}</ul>`;
        if (L.example) body += `<h4>✏️ Example</h4><p>${hiAns(L.example, e)}</p>`;
        if (L.reallife) body += `<h4>🌍 In real life</h4><p>${hiAns(L.reallife, e)}</p>`;
        if (rv.remember && rv.remember.length) body += `<h4>🧠 Remember</h4><ul>${rv.remember.map(p => `<li>${hiAns(p, e)}</li>`).join('')}</ul>`;
      } else body = `<p>${E(r.ch.title)} — topics: ${(r.ch.topics || []).map(t => E(t.title)).join(', ')}</p>`;
      sheet(tp ? tp.title : r.ch.title, path, body || '<p class="sub">This topic has no notes yet.</p>');
    } else {
      const d = r.data, w = sq(e.disp || e.a).toLowerCase();
      let body = '';
      if (d && Array.isArray(d.concepts)) {
        const cs = d.concepts.filter(c => c && c.title).map(c => ({ c, hit: JSON.stringify(c.body || '').toLowerCase().includes(w) || String(c.title).toLowerCase().includes(w) }));
        cs.sort((a, b) => b.hit - a.hit);
        body += cs.map(({ c, hit }, j) => `<details${j === 0 && hit ? ' open' : ''}><summary>${hit ? '⭐ ' : ''}${E(c.title)}</summary>${(Array.isArray(c.body) ? c.body : [c.body]).filter(Boolean).map(p => `<p>${hiAns(p, e)}</p>`).join('')}</details>`).join('');
      }
      if (d && d.quickref && d.quickref.length) body += `<h4>⚡ Quick reference</h4><ul>${d.quickref.slice(0, 12).map(q => `<li><b>${E(q.k)}</b> — ${hiAns(q.v, e)}</li>`).join('')}</ul>`;
      sheet(r.unit ? r.unit.title : r.ch.title, path, body || `<p>${E(r.ch.title)}</p>`);
    }
  }
  async function source(sp, e) {
    const r = await where(sp, e);
    return { path: pathOf(r), open: () => openSource(r, e) };
  }

  /* ---------- hints ---------- */
  /* does s still give away the answer (the answer, or a word stem of it)? */
  function leak(s, e) {
    if (e.u) return s.includes(sq(e.disp || e.a)) || (e.u.length >= 3 && s.includes(e.u.slice(0, -1).join('')));
    const ws = sq(e.disp || e.a).split(/[\s\-]+/).filter(Boolean), U = ' ' + s.toUpperCase().replace(/[^A-Z]+/g, ' ') + ' ';
    return ws.some(w => { const W = w.toUpperCase(); return W.length >= 3 && (W.length <= 4 ? U.includes(' ' + W + ' ') : U.includes(' ' + W.slice(0, Math.max(4, W.length - 3)))); });
  }
  /* hide the answer as _____ ; null when the text does not contain it, or a part of it would still show */
  function mask(txt, e) {
    const ans = sq(e.disp || e.a);
    let s = sq(txt); if (!s) return null;
    if (e.u) { if (!s.includes(ans)) return null; s = s.split(ans).join('_____'); return leak(s, e) ? null : s; }
    const ws = ans.split(/[\s\-]+/).filter(Boolean);
    const re = new RegExp('\\b' + ws.map(reEsc).join('[\\s\\-]+') + "(?:s|es|'s)?\\b", 'gi');
    if (!re.test(s)) return null;
    s = s.replace(re, '_____');
    return leak(s, e) ? null : s;
  }
  /* a clue that may or may not contain the answer: hide it if it does; null if it would still leak */
  const safeClue = (txt, e) => { const m = mask(txt, e); if (m) return m; const s = sq(txt); return s && !leak(s, e) ? s : null; };
  const short = (s, n) => { s = sq(s); if (s.length <= n) return s; const c = s.slice(0, n), k = c.lastIndexOf(' '); return (k > n * 0.6 ? c.slice(0, k) : c) + '…'; };
  const sameText = (a, b) => sq(a).toLowerCase().replace(/[^a-z0-9ऀ-෿]+/g, '') === sq(b).toLowerCase().replace(/[^a-z0-9ऀ-෿]+/g, '');
  const normA = s => String(s || '').toUpperCase().replace(/[^A-Zऀ-෿]/g, '');
  /* seeded shuffle, never equal to the answer */
  function jumble(units, seed) {
    let h = 2166136261; for (const ch of String(seed)) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619); }
    const r = () => { h ^= h << 13; h ^= h >>> 17; h ^= h << 5; return ((h >>> 0) % 1e6) / 1e6; };
    for (let k = 0; k < 8; k++) {
      const a = units.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
      if (a.join('') !== units.join('')) return a;
    }
    const a = units.slice(); if (a.length > 1) a.push(a.shift()); return a;
  }

  async function hints(sp, e, inPuzzle) {
    const r = await where(sp, e), out = [], seen = new Set();
    const flat = x => sq(x).toLowerCase().replace(/_+/g, ' ').replace(/[^a-z0-9\u0900-\u0dff]+/g, '');
    const clueF = flat(e.clue);
    const add = (ic, label, text) => { text = sq(text); if (!text || seen.has(text.toLowerCase()) || sameText(text, e.clue) || (clueF.length > 12 && flat(text).includes(clueF))) return; seen.add(text.toLowerCase()); out.push({ ic, label, text }); };
    const A = e.a, alt = [], cmp = [], real = [], sent = [], groups = [], choiceSets = [];
    const isAns = s => normA(s) === A || normA(s) === A + 'S' || normA(s) + 'S' === A;
    if (r && r.k === 's') {
      const tps = r.topic ? [r.topic].concat((r.ch.topics || []).filter(t => t !== r.topic)) : (r.ch.topics || []);
      tps.forEach(tp => {
        (tp.games || []).forEach(gm => {
          if (!gm) return;
          if (gm.type === 'match') {
            const ps = (gm.pairs || []).filter(p => Array.isArray(p) && p.length >= 2);
            ps.forEach(p => { if (isAns(p[0])) { alt.push(p[1]); choiceSets.push(ps.map(q => q[0])); } else if (isAns(p[1])) { alt.push(p[0]); choiceSets.push(ps.map(q => q[1])); } });
          }
          if (gm.type === 'sort' && Array.isArray(gm.buckets)) (gm.items || []).forEach(it => { if (Array.isArray(it) && isAns(it[0]) && gm.buckets[it[1]] != null) groups.push(typeof gm.buckets[it[1]] === 'string' ? gm.buckets[it[1]] : (gm.buckets[it[1]].name || gm.buckets[it[1]].label || '')); });
          if (gm.type === 'fill') (gm.items || []).forEach(it => { if (it && isAns(it.answer) && typeof it.text === 'string') alt.push(it.text); });
          if (gm.type === 'speed') (gm.items || []).forEach(it => { if (it && isAns(it.a) && typeof it.q === 'string') alt.push(it.q); });
        });
        (tp.quiz || []).forEach(q => {
          if (!q || !Array.isArray(q.options)) return;
          if (isAns(q.options[q.answer])) { if (typeof q.q === 'string' && !/\b(which of the following|all of|none of)\b/i.test(q.q)) alt.push(q.q); choiceSets.push(q.options); }
          sentences(q.explain).forEach(x => sent.push(x));
        });
        const L = tp.learn || {}, rv = tp.revise || {};
        [L.example, L.reallife].forEach(x => sentences(x).forEach(s => real.push(s)));
        [].concat(L.points || [], rv.remember || [], rv.summary || [], rv.focus || []).forEach(x => sentences(x).forEach(s => sent.push(s)));
      });
    } else if (r && r.k === 'c' && r.data) {
      const d = r.data;
      (d.mcqs || []).forEach(q => {
        if (!q || !Array.isArray(q.options) || !isAns(q.options[q.answer])) return;
        if (typeof q.q === 'string' && q.q.length < 160 && !/\b(which of the following|all of|none of)\b/i.test(q.q)) alt.push(q.q);
        choiceSets.push(q.options);
      });
      (d.quickref || []).forEach(q => { if (!q) return; if (isAns(q.k)) alt.push(q.v); const m = /^(.+?)\s+(?:vs\.?|versus)\s+(.+)$/i.exec(String(q.k || '')); if (m) { if (isAns(m[1])) cmp.push(m[2]); else if (isAns(m[2])) cmp.push(m[1]); } });
      (d.concepts || []).forEach(c => {
        if (!c) return; const m = /^(.+?)\s+(?:vs\.?|versus)\s+(.+?)(?:\s*[—–(:].*)?$/i.exec(String(c.title || ''));
        if (m) { if (isAns(m[1])) cmp.push(m[2]); else if (isAns(m[2])) cmp.push(m[1]); }
        (Array.isArray(c.body) ? c.body : [c.body]).forEach(b => sentences(b).forEach(s => (/\b(for example|e\.g\.|example|suppose|if a|when a)\b/i.test(s) ? real : sent).push(s)));
      });
      ((d.revision && d.revision.summary) || []).forEach(x => sentences(x).forEach(s => sent.push(s)));
    }
    /* 🔁 another clue (best first: shortest clear one) */
    alt.map(a => safeClue(a, e)).filter(a => a && !/[=÷×]/.test(a) && words(a) >= 3 && a.length <= 170 && !/^[\d\s.,₹%]+$/.test(a)).sort((a, b) => a.length - b.length).slice(0, 2)
      .forEach(a => add('🔁', 'Another clue', a));
    /* ⚖️ compared with  ·  🔤 short form / full form */
    cmp.map(sq).filter(c => c && !leak(c, e) && words(c) <= 6).slice(0, 1).forEach(c => add('⚖️', 'Often compared with', `In the lesson it is compared with “${c}”.`));
    if (!e.u) {
      const ans = sq(e.disp || e.a), all = sent.concat(real).join(' ');
      try {
        const m1 = new RegExp('\\b' + reEsc(ans) + '\\s*\\(([A-Z][A-Za-z&]{1,7})\\)', 'i').exec(all);
        if (m1 && ans.split(' ').length > 1 && !leak(m1[1], e)) add('🔤', 'Short form', `Its short form is ${m1[1]}.`);
        const m2 = /^[A-Z]{2,6}$/.test(ans) ? new RegExp('([A-Z][a-z]+(?:\\s+(?:of|and|for|the|&|[A-Z][a-z]+)){1,6})\\s*\\(' + ans + '\\)').exec(all) : null;
        if (m2) add('🔤', 'Full form', `It is the short form of “${m2[1]}”.`);
      } catch (x) {}
    }
    /* 🌍 example / 📖 lesson sentence, answer hidden */
    const pickS = (list, n) => list.map(s => mask(s, e)).filter(s => s && words(s) >= 6 && words(s) <= 45 && (s.match(/_____/g) || []).length <= 2).sort((a, b) => a.length - b.length).slice(0, n);
    pickS(real, 1).forEach(s => add('🌍', 'Example', short(s, 220)));
    pickS(sent, 2).forEach(s => add('📖', 'From the lesson — fill the gap', short(s, 220)));
    groups.map(sq).filter(g => g && !leak(g, e)).slice(0, 1).forEach(g => add('🗂️', 'Group', `It belongs to the group “${g}”.`));
    if (r && r.k === 's' && r.topic && !leak(r.topic.title, e)) add('🧭', 'Topic', `This word is from the topic “${r.topic.title}”.`);
    if (r && r.k === 'c' && r.unit && !leak(r.unit.title, e)) add('🧭', 'Unit', `This word is from “${r.unit.title}”.`);
    /* always last: letters, then the jumble */
    const units = e.u ? e.u.slice() : e.a.split(''), unit = e.u ? 'akshara' : 'letter';
    /* 🎯 pick from a few: the answer with other options from the same quiz / match game (all short words) */
    const tail = [];
    const ans0 = sq(e.disp || e.a);
    for (const set of choiceSets) {
      const taken = new Set((inPuzzle || []).map(normA));   // never list another answer of this puzzle
      const others = [...new Set(set.map(sq))].filter(o => o && !isAns(o) && !taken.has(normA(o)) && words(o) <= 4 && !/\d|of the above|both|none|all of/i.test(o));
      if (others.length < 2) continue;
      const pickN = jumble(others, e.a).slice(0, 3);
      tail.push({ ic: '🎯', label: 'It is one of these', text: jumble(pickN.concat(ans0), e.a + 'c').join(' · ') }); break;
    }
    const meaning = out.slice(0, Math.max(2, 5 - 2 - tail.length));
    tail.push({ ic: '🔡', label: 'Letters', text: units.length > 2 ? `Starts with “${units[0]}” and ends with “${units[units.length - 1]}”.${e.enum && /,/.test(e.enum) ? ` It has ${e.enum.replace(/[()]/g, '').split(',').length} words ${e.enum}.` : ''}` : `Starts with “${units[0]}”.` });
    if (units.length >= 5) tail.push({ ic: '🧩', label: 'Some letters', text: units.map((c, i) => (i % 3 === 0 || i === units.length - 1 ? c : '_')).join(' ') + (e.enum && /,/.test(e.enum) ? `  ${e.enum}` : '') });
    tail.push({ ic: '🔀', label: `Jumbled ${unit}s`, text: jumble(units, e.a + '|' + e.n).join(' ') });
    /* gentlest first; at most 5: meaning hints, then the letter hints (the jumble always last) */
    const all = meaning.concat(tail.slice(0, -1)), jum = tail[tail.length - 1];
    return all.slice(0, 4).concat(jum);
  }

  function css() {
    if (D.getElementById('pzwCss')) return;
    const c = D.createElement('style'); c.id = 'pzwCss';
    c.textContent = `.pzw-pop h3{margin:6px 0 2px}.pzw-pop .sub b{opacity:.55}.pzw-body{text-align:left;margin:10px 0 14px;line-height:1.45;font-size:14.5px}
.pzw-body h4{margin:12px 0 4px;font-size:15px}.pzw-body ul{margin:0;padding-left:20px}.pzw-body li{margin:3px 0}
.pzw-body details{border:1px solid rgba(118,70,234,.25);border-radius:12px;padding:6px 10px;margin:6px 0}.pzw-body summary{font-weight:800;cursor:pointer}
.pzw-body mark{background:#fff0a8;border-radius:3px;padding:0 2px}`;
    D.head.appendChild(c);
  }

  window.PzWords = { source, hints, where };
})();
