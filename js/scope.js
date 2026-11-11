/* Knowtopia — 🎯 "What do you want to play?" chooser (js/scope.js)
   One chooser for puzzles, Arcade games and CA Group study: pick everything, one or more subjects / papers, chapters,
   or single topics (CA: units) — in any mix.
   The choice is a short list of TOKENS, each covering everything under it (prefix + '-'):
     school  'g6' (all subjects) · 'g6-science' · 'g6-science-02' (chapter) · 'g6-science-02-01' (topic id)
     CA      'fnd' (all papers)  · 'fnd-p1' · 'fnd-p1-ch05' (chapter) · 'fnd-p1-ch05-u02' (unit)
   ScopePick.open({ ca, grade, level, value: [tokens], title, cta, onDone(tokens, label) })
   ScopePick.resolve(tokens, { ca, grade, level }) → [{ sid, ci, c, topics: Set|null }]  (school)
                                                     [{ ch, c, p, units: Set|null }]    (CA, built units only)
   ScopePick.label(tokens, { ca, grade, level }) → "Science · Ch 2 + 3 more"  (async)
   Quick picks: ✨ Everything · 📍 My chapter · 📚 Studied this week · 🎲 Surprise me. */
(function () {
  'use strict';
  const D = document;
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const X = () => (window.Ca && Ca._) || null;
  const under = (id, tok) => id === tok || id.startsWith(tok + '-');
  const LV = { foundation: 'fnd', inter: 'int', final: 'fin' }, LVN = { fnd: 'Foundation', int: 'Intermediate', fin: 'Final' };
  const COLORS = ['#7646ea', '#ff7a45', '#12b886', '#228be6', '#e64980', '#fab005', '#15aabf', '#82c91e', '#be4bdb', '#fd7e14'];
  const chTok = (g, sid, c, ci) => { const t = (c.topics || [])[0]; return t && /-\d+$/.test(t.id) ? t.id.replace(/-\d+$/, '') : `g${g}-${sid}-c${ci}`; };
  const paperName = p => p.name || ('Paper ' + String(p.key || '').replace(/^p/, ''));

  /* ---------- the tree (children load when needed) ---------- */
  function tree(o) {
    const T = { nodes: {}, root: null };
    const add = (n, parent) => { n.parent = parent || null; T.nodes[n.id] = n; return n; };
    if (o.ca) {
      const lv = LV[o.level] || 'fnd';
      T.root = add({ id: lv, label: `All papers`, e: '✨', load: async () => {
        const x = X(); if (!x) return [];
        const st = await x.structure(o.level || 'foundation');
        return st.papers.filter(p => p.chapters.some(c => c.units.some(u => u.status === 'built'))).map((p, i) => ({
          id: p.chapters[0].id.split('-').slice(0, 2).join('-'), label: paperName(p), e: '📘', color: COLORS[i % COLORS.length], p,
          kids: p.chapters.filter(c => c.units.some(u => u.status === 'built')).map(c => ({ id: c.id, label: `Ch ${c.n}: ${c.title}`, c, p,
            kids: c.units.filter(u => u.status === 'built').map(u => ({ id: u.id, label: u.title, sub: `Unit ${u.n}`, u, leaf: true })) })) }));
      } });
    } else {
      const g = +o.grade;
      T.root = add({ id: 'g' + g, label: 'All subjects', e: '✨', load: async () => {
        let subs = []; try { subs = curSubjects(g) || []; } catch (e) {}
        return subs.map((s, i) => ({ id: `g${g}-${s.id}`, sid: s.id, label: s.name, e: ((window.Worlds && Worlds.SUBJECT_STYLE && Worlds.SUBJECT_STYLE[s.id]) || { e: '📘' }).e, color: COLORS[i % COLORS.length],
          load: async () => { const d = await subjectData(g, s.id); return ((d && d.chapters) || []).map((c, ci) => ({ id: chTok(g, s.id, c, ci), label: `Ch ${c.n}: ${c.title}`, c, ci, sid: s.id,
            kids: (c.topics || []).map(t => ({ id: t.id, label: t.title, leaf: true })) })); } }));
      } });
    }
    T.kids = async n => {
      if (n.kids && !n.kidsReady) { n.kids = n.kids.map(k => add(k, n)); n.kidsReady = true; }
      if (!n.kids && n.load) { if (!n.loading) n.loading = n.load().then(ks => { n.kids = ks.map(k => add(k, n)); n.kidsReady = true; return n.kids; }).catch(() => (n.kids = [])); await n.loading; }
      return n.kids || [];
    };
    return T;
  }

  /* ---------- selection maths on tokens ---------- */
  function Sel(T, init) {
    let set = new Set(init || []);
    const covered = id => [...set].some(t => under(id, t));
    const some = id => [...set].some(t => under(t, id));
    const state = n => covered(n.id) ? 'all' : some(n.id) ? 'some' : 'none';
    /* tick / untick a node (its parents' children are loaded: the student is looking at it) */
    function toggle(n) {
      if (state(n) === 'all') {
        // split the ticked ancestor into its children until n stands alone, then drop n
        let a = n; const path = []; while (a && !set.has(a.id)) { path.unshift(a); a = a.parent; }
        if (!a) return;
        set.delete(a.id);
        let cur = a;
        for (const step of path) { (cur.kids || []).forEach(k => { if (k !== step) set.add(k.id); }); cur = step; }
        if (cur !== n) (cur.kids || []).forEach(k => { if (k !== n) set.add(k.id); });
      } else {
        [...set].forEach(t => { if (under(t, n.id)) set.delete(t); });
        set.add(n.id);
      }
      compress(n.parent);
    }
    function compress(p) {      // every child ticked → tick the parent instead
      while (p && p.kids && p.kids.length && p.kids.every(k => set.has(k.id))) { p.kids.forEach(k => set.delete(k.id)); set.add(p.id); p = p.parent; }
    }
    return { state, toggle, get: () => [...set], set: v => { set = new Set(v || []); }, clear: () => set.clear(), size: () => set.size };
  }

  /* ---------- resolve tokens → chapters (+ topic / unit filter) ---------- */
  async function resolve(tokens, o) {
    tokens = (tokens || []).map(String); if (!tokens.length) return [];
    const T = tree(o), out = [];
    const subs = await T.kids(T.root);
    if (o.ca) {
      for (const P of subs) for (const C of await T.kids(P)) {
        if (!tokens.some(t => under(C.id, t) || under(t, C.id))) continue;
        const whole = tokens.some(t => under(C.id, t));
        const units = whole ? null : new Set(C.kids.filter(u => tokens.some(t => under(u.id, t))).map(u => u.id));
        if (whole || units.size) out.push({ ch: C.id, c: C.c, p: C.p, units });
      }
    } else {
      for (const Sb of subs) {
        if (!tokens.some(t => under(Sb.id, t) || under(t, Sb.id))) continue;
        for (const C of await T.kids(Sb)) {
          if (!tokens.some(t => under(C.id, t) || under(t, C.id))) continue;
          const whole = tokens.some(t => under(C.id, t));
          const topics = whole ? null : new Set(C.kids.filter(x => tokens.some(t => under(x.id, t))).map(x => x.id));
          if (whole || topics.size) out.push({ sid: C.sid, ci: C.ci, c: C.c, topics });
        }
      }
    }
    return out;
  }
  async function labelOf(tokens, o, T) {
    tokens = tokens || []; if (!tokens.length) return 'Nothing chosen';
    T = T || tree(o);
    const find = async id => { let n = T.root; if (n.id === id) return n;
      for (let guard = 0; guard < 4 && n; guard++) { const ks = await T.kids(n); const k = ks.find(x => under(id, x.id)); if (!k) return null; if (k.id === id) return k; n = k; } return null; };
    const n = await find(tokens[0]);
    let nm = tokens[0];
    if (n === T.root) nm = o.ca ? `All papers · CA ${LVN[n.id] || ''}` : `All subjects · Class ${o.grade}`;
    else if (n && n.parent === T.root) nm = n.label;
    else if (n && n.parent && n.parent.parent === T.root) nm = `${n.parent.label} · ${n.label}`;
    else if (n && n.parent && n.parent.parent) nm = `${n.parent.parent.label} · ${n.label}`;
    return nm + (tokens.length > 1 ? ` + ${tokens.length - 1} more` : '');
  }

  /* ---------- quick picks ---------- */
  async function myChapter(o, T) {
    try {
      const sc = window.Puzzles && Puzzles.curChapter ? await Puzzles.curChapter() : null; if (!sc) return null;
      if (sc.k === 'c') return [sc.ch];
      if (sc.k === 's') { const subs = await T.kids(T.root), Sb = subs.find(s => s.sid === sc.sid); if (!Sb) return null; const C = (await T.kids(Sb))[sc.ci]; return C ? [C.id] : null; }
    } catch (e) {}
    return null;
  }
  function thisWeek(o) {
    if (o.ca) return null;
    try { const wk = Date.now() - 7 * 864e5, g = 'g' + o.grade + '-';
      const ids = Object.entries(ST.topics || {}).filter(([id, v]) => id.startsWith(g) && v && v.last && new Date(v.last).getTime() >= wk).map(([id]) => id);
      return ids.length ? ids : null; } catch (e) { return null; }
  }
  async function surprise(o, T) {
    const subs = await T.kids(T.root); if (!subs.length) return null;
    const Sb = subs[Math.floor(Math.random() * subs.length)], cs = await T.kids(Sb); if (!cs.length) return null;
    return [cs[Math.floor(Math.random() * cs.length)].id];
  }

  /* ---------- the sheet ---------- */
  function open(o) {
    css();
    const T = tree(o), sel = Sel(T, o.value), opened = new Set();
    const sh = D.createElement('div'); sh.className = 'sheet show sp-sheet'; sh.setAttribute('role', 'dialog'); sh.setAttribute('aria-modal', 'true'); sh.setAttribute('aria-labelledby', 'spT');
    sh.innerHTML = `<div class="sheet-in sp-in"><div class="sheet-grab" aria-hidden="true"></div>
      <div class="sp-head"><span class="sp-hi" aria-hidden="true">🎯</span><div><h3 id="spT">${E(o.title || 'What do you want to play?')}</h3><p>Tick as much or as little as you like — everything, ${o.ca ? 'papers' : 'subjects'}, chapters or single ${o.ca ? 'units' : 'topics'}.</p></div></div>
      <div class="sp-quick" role="group" aria-label="Quick picks"></div>
      <div class="sp-body" id="spBody"><p class="sub">Loading…</p></div>
      <div class="sp-foot"><div class="sp-sum" id="spSum" role="status" aria-live="polite"></div>
        <div class="sp-fb"><button type="button" class="btn ghost" id="spClear">Clear</button><button type="button" class="btn mint" id="spGo">${E(o.cta || 'Done ✓')}</button></div></div></div>`;
    D.body.appendChild(sh);
    let closed = false;
    const close = () => { if (closed) return; closed = true; sh.classList.remove('show'); setTimeout(() => sh.remove(), 220); };
    const cancel = () => { close(); if (o.onCancel) o.onCancel(); };
    sh.addEventListener('click', e => { if (e.target === sh) cancel(); });
    const sb = document.createElement('button'); sb.hidden = true; sb.setAttribute('data-close', '1'); sb.onclick = cancel; sh.querySelector('.sp-in').appendChild(sb);
    const body = sh.querySelector('#spBody');

    const ring = (n, st) => { const kids = n.kids || [], tot = kids.length || 1, on = st === 'all' ? tot : kids.filter(k => sel.state(k) !== 'none').length, f = on / tot, r = 15, c = 2 * Math.PI * r;
      return `<svg class="sp-ring" viewBox="0 0 36 36" aria-hidden="true"><circle cx="18" cy="18" r="${r}" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="4"/><circle cx="18" cy="18" r="${r}" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-dasharray="${(f * c).toFixed(1)} ${c.toFixed(1)}" transform="rotate(-90 18 18)"/></svg>`; };
    const tick = st => `<span class="sp-tick ${st}" aria-hidden="true">${st === 'all' ? '✓' : st === 'some' ? '–' : ''}</span>`;
    const stTxt = st => (st === 'all' ? 'chosen' : st === 'some' ? 'partly chosen' : 'not chosen');

    async function draw() {
      const subs = await T.kids(T.root);
      for (const s of subs) if (opened.has(s.id)) { const cs = await T.kids(s); for (const c of cs) if (opened.has(c.id)) await T.kids(c); }
      const y = body.scrollTop, rs = sel.state(T.root);
      body.innerHTML = `<button type="button" class="sp-all ${rs}" data-t="${T.root.id}" aria-pressed="${rs === 'all'}"><span class="sp-alle" aria-hidden="true">✨</span><span><b>${E(o.ca ? 'All papers' : 'All subjects')}</b><small>Mix everything together</small></span>${tick(rs)}<span class="sr-only">${stTxt(rs)}</span></button>
        <div class="sp-grid">${subs.map(s => { const st = sel.state(s), op = opened.has(s.id);
          return `<div class="sp-card ${st}${op ? ' open' : ''}" style="--c:${s.color}"><div class="sp-ctop"><button type="button" class="sp-cmain" data-t="${s.id}" aria-pressed="${st === 'all'}"><span class="sp-ce" aria-hidden="true">${E(s.e)}</span><b>${E(s.label)}</b>${tick(st)}<span class="sr-only">${stTxt(st)}</span></button>
            <button type="button" class="sp-open" data-o="${s.id}" aria-expanded="${op}">${s.kids ? ring(s, st) : ''}<span>${op ? 'Hide' : 'Chapters'} ${op ? '▴' : '▾'}</span></button></div></div>`; }).join('')}</div>
        ${subs.filter(s => opened.has(s.id)).map(s => `<section class="sp-chs" style="--c:${s.color}" aria-label="${E(s.label)} chapters"><h4><span aria-hidden="true">${E(s.e)}</span> ${E(s.label)}</h4>${(s.kids || []).map(c => { const st = sel.state(c), op = opened.has(c.id), nk = (c.kids || []).length;
            return `<div class="sp-ch ${st}"><div class="sp-chrow"><button type="button" class="sp-chb" data-t="${c.id}" aria-pressed="${st === 'all'}">${tick(st)}<span>${E(c.label)}</span><span class="sr-only">${stTxt(st)}</span></button>${nk > 1 ? `<button type="button" class="sp-tg" data-o="${c.id}" aria-expanded="${op}">${op ? '▴' : `${nk} ${o.ca ? 'units' : 'topics'} ▾`}</button>` : ''}</div>
              ${op ? `<div class="sp-pills">${c.kids.map(t => { const s2 = sel.state(t); return `<button type="button" class="sp-pill ${s2}" data-t="${t.id}" aria-pressed="${s2 === 'all'}">${s2 === 'all' ? '✓ ' : ''}${E(t.label)}</button>`; }).join('')}</div>` : ''}</div>`; }).join('')}</section>`).join('')}`;
      body.scrollTop = y;
      body.querySelectorAll('[data-t]').forEach(b => b.onclick = async () => { S('tap'); const n = T.nodes[b.dataset.t]; if (!n) return; if (n.parent) await T.kids(n.parent); sel.toggle(n); await draw(); });
      body.querySelectorAll('[data-o]').forEach(b => b.onclick = async () => { S('tap'); const id = b.dataset.o; opened.has(id) ? opened.delete(id) : opened.add(id); await draw();
        if (opened.has(id)) { const t = body.querySelector(`.sp-chs h4, [data-t="${id}"]`); if (t && T.nodes[id] && T.nodes[id].parent === T.root) { const sec = [...body.querySelectorAll('.sp-chs')].find(x => x.getAttribute('aria-label') === T.nodes[id].label + ' chapters'); if (sec) sec.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); } } });
      const v = sel.get(), sum = sh.querySelector('#spSum');
      sum.innerHTML = v.length ? `<b>🎯 ${E(await labelOf(v, o, T))}</b>` : '<span>Nothing chosen yet</span>';
      sh.querySelector('#spGo').disabled = !v.length;
    }
    /* quick picks */
    const qk = sh.querySelector('.sp-quick');
    const quick = [['✨', 'Everything', async () => [T.root.id]], ['📍', 'My chapter', () => myChapter(o, T)], ['📚', 'Studied this week', async () => thisWeek(o)], ['🎲', 'Surprise me', () => surprise(o, T)]];
    qk.innerHTML = quick.map(([e, n], i) => `<button type="button" class="sp-q" data-q="${i}"><span aria-hidden="true">${e}</span> ${n}</button>`).join('');
    qk.querySelectorAll('[data-q]').forEach(b => b.onclick = async () => {
      S('tap'); const v = await quick[+b.dataset.q][2]();
      if (!v || !v.length) { try { toast(+b.dataset.q === 2 ? 'Nothing studied in the last 7 days yet' : 'Not available right now'); } catch (e) {} return; }
      sel.set(v);
      for (const t of v) { const n = Object.values(T.nodes).find(x => x !== T.root && under(t, x.id) && x.parent === T.root); if (n && t !== n.id) opened.add(n.id); }
      await draw(); try { qk.querySelectorAll('.sp-q').forEach(x => x.classList.toggle('on', x === b)); } catch (e) {}
    });
    sh.querySelector('#spClear').onclick = async () => { S('tap'); sel.clear(); qk.querySelectorAll('.sp-q').forEach(x => x.classList.remove('on')); await draw(); };
    sh.querySelector('#spGo').onclick = async () => { const v = sel.get(); if (!v.length) return; S('open'); const lb = await labelOf(v, o, T); close(); o.onDone && o.onDone(v, lb); };
    /* open the subjects that already hold the current choice */
    (async () => { await T.kids(T.root); for (const t of sel.get()) { const n = Object.values(T.nodes).find(x => x.parent === T.root && under(t, x.id) && t !== x.id); if (n) opened.add(n.id); } await draw(); const h = sh.querySelector('#spT'); if (h) { h.tabIndex = -1; try { h.focus(); } catch (e) {} } })();
  }

  function css() {
    if (D.getElementById('spCss')) return;
    const c = D.createElement('style'); c.id = 'spCss';
    c.textContent = `.sp-in{display:flex;flex-direction:column;max-height:calc(94vh / var(--z,1))!important;padding-bottom:0!important}
.sp-head,.sp-quick,.sp-foot{flex:none}.sp-tg{text-transform:none!important;letter-spacing:0!important}
.sp-head{display:flex;gap:12px;align-items:center;margin:2px 0 10px}.sp-hi{font-size:34px;width:52px;height:52px;border-radius:16px;display:grid;place-items:center;background:linear-gradient(135deg,#ffd43b,#ff922b);flex:none;box-shadow:0 6px 16px rgba(255,146,43,.35)}
.sp-head h3{margin:0;font-size:19px}.sp-head p{margin:2px 0 0;font-size:13px;color:var(--muted);line-height:1.35}
.sp-quick{display:flex;gap:6px;overflow-x:auto;padding:2px 0 10px;scrollbar-width:none}.sp-quick::-webkit-scrollbar{display:none}
.sp-q{flex:none;border:0;border-radius:999px;padding:8px 13px;background:#f1edff;color:#4b2bb8;font:800 13px Nunito,sans-serif;cursor:pointer;white-space:nowrap}
.sp-q.on{background:#7646ea;color:#fff}
.sp-body{flex:1;overflow-y:auto;min-height:120px;padding:2px 2px 12px;overscroll-behavior:contain}
.sp-all{width:100%;display:flex;align-items:center;gap:12px;border:0;border-radius:18px;padding:12px 14px;margin-bottom:10px;cursor:pointer;text-align:left;color:#fff;font:inherit;
  background:linear-gradient(120deg,#7646ea,#c850c0 60%,#ffcc70);box-shadow:0 8px 20px rgba(118,70,234,.28)}
.sp-all b{display:block;font-size:16px}.sp-all small{opacity:.9;font-size:12.5px}.sp-alle{font-size:26px}.sp-all .sp-tick{margin-left:auto;border-color:#fff}
.sp-all.all .sp-tick{background:#fff;color:#7646ea}
.sp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.sp-card{border-radius:18px;background:var(--c);color:#fff;position:relative;overflow:hidden;box-shadow:0 6px 16px rgba(0,0,0,.14);transition:transform .15s}
.sp-card::after{content:'';position:absolute;right:-18px;top:-18px;width:70px;height:70px;border-radius:50%;background:rgba(255,255,255,.14);pointer-events:none}
.sp-card.none{filter:saturate(.55) brightness(1.05);opacity:.86}.sp-card.all{transform:translateY(-1px)}
.sp-cmain{display:flex;flex-direction:column;align-items:flex-start;gap:2px;width:100%;border:0;background:none;color:inherit;font:inherit;text-align:left;padding:12px 12px 4px;cursor:pointer;position:relative;z-index:1}
.sp-cmain b{font-size:14.5px;line-height:1.2;padding-right:28px}.sp-ce{font-size:24px}
.sp-cmain .sp-tick{position:absolute;right:10px;top:10px;border-color:#fff}.sp-card.all .sp-tick{background:#fff;color:var(--c)}.sp-card.some .sp-tick{background:rgba(255,255,255,.5);color:#fff}
.sp-open{display:flex;align-items:center;gap:6px;border:0;background:rgba(0,0,0,.14);color:#fff;font:800 12px Nunito,sans-serif;padding:6px 10px;width:100%;cursor:pointer;position:relative;z-index:1}
.sp-ring{width:22px;height:22px}
.sp-tick{width:22px;height:22px;border-radius:50%;border:2px solid #b9b4d6;display:inline-grid;place-items:center;font:900 13px/1 Nunito,sans-serif;flex:none;background:transparent}
.sp-chs{margin-top:12px;border-radius:18px;padding:10px 10px 6px;background:color-mix(in srgb,var(--c) 9%,var(--card,#fff));border:1.5px solid color-mix(in srgb,var(--c) 30%,transparent)}
.sp-chs h4{margin:0 0 6px;font-size:15px;color:var(--c)}
.sp-ch{border-radius:12px;margin:4px 0;background:var(--card,#fff)}.sp-ch.all{box-shadow:inset 0 0 0 2px var(--c)}
.sp-chrow{display:flex;align-items:center}.sp-chb{flex:1;display:flex;gap:10px;align-items:center;border:0;background:none;color:var(--ink);font:700 14px/1.3 Nunito,sans-serif;text-align:left;padding:9px 8px;cursor:pointer}
.sp-ch.all .sp-tick{background:var(--c);border-color:var(--c);color:#fff}.sp-ch.some .sp-tick{border-color:var(--c);color:var(--c)}
.sp-tg{border:0;background:none;color:var(--c);font:800 12px Nunito,sans-serif;padding:8px;cursor:pointer;white-space:nowrap}
.sp-pills{display:flex;flex-wrap:wrap;gap:6px;padding:0 8px 10px 40px}
.sp-pill{border:1.5px solid color-mix(in srgb,var(--c) 45%,transparent);background:transparent;color:var(--ink);border-radius:999px;padding:6px 11px;font:700 12.5px/1.25 Nunito,sans-serif;cursor:pointer;text-align:left}
.sp-pill.all{background:var(--c);border-color:var(--c);color:#fff}
.sp-foot{position:sticky;bottom:0;background:var(--card,#fff);border-top:1px solid rgba(0,0,0,.07);padding:10px 0 calc(12px + env(safe-area-inset-bottom));margin:0 -2px}
.sp-sum{font-size:13.5px;margin-bottom:8px;min-height:18px;color:var(--ink)}.sp-sum span{color:var(--muted)}
.sp-fb{display:flex;gap:8px}.sp-fb .btn{margin:0}.sp-fb .btn.ghost{flex:0 0 32%}.sp-fb .btn.mint{flex:1}
html[data-age=pro] .sp-q{background:#eef1f7;color:#2c3e66}html[data-age=pro] .sp-q.on{background:#2c3e66;color:#fff}
html.sv-hc .sp-card{filter:none;opacity:1;outline:2px solid #000}
@media (prefers-reduced-motion:reduce){.sp-card{transition:none}}
/* the summary chip shown in pickers */
.sp-pick{display:flex;align-items:center;gap:12px;width:100%;border:0;border-radius:18px;padding:12px 14px;cursor:pointer;text-align:left;font:inherit;color:#fff;background:linear-gradient(120deg,#7646ea,#c850c0);box-shadow:0 6px 18px rgba(118,70,234,.25)}
.sp-pick .sp-pe{font-size:26px}.sp-pick b{display:block;font-size:15px;line-height:1.25}.sp-pick small{opacity:.9;font-size:12.5px}.sp-pick .sp-pc{margin-left:auto;background:rgba(255,255,255,.22);border-radius:999px;padding:6px 11px;font:800 12.5px Nunito,sans-serif;white-space:nowrap}`;
    D.head.appendChild(c);
  }
  /* a ready-made "🎯 chosen: … · Change" button */
  const pickHTML = (label, hint, id) => { css(); return `<button type="button" class="sp-pick" id="${id || 'spPick'}"><span class="sp-pe" aria-hidden="true">🎯</span><span><b>${E(label)}</b><small>${E(hint || 'Subjects, chapters or topics — any mix')}</small></span><span class="sp-pc">Change</span></button>`; };

  window.ScopePick = { open, resolve, label: labelOf, pickHTML, under };
})();
