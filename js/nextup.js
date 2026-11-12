/* ================= 🔭 Sneak peek: what comes next (js/nextup.js) =================
   Shows ONLY the course structure of the very next step, to keep students excited to continue:
     school Grade g → Grade g+1 subjects and chapter titles (Grade 11 → 12 uses the student's own subjects)
     CA Foundation → CA Intermediate + CA Final (as asked) · CA Intermediate → CA Final · CA Final / Grade 12 → nothing
   Read-only: titles only, nothing opens. A card sits in Me (📚 My learning) and at the end of World / CA Journey. */
(function () {
  'use strict';
  const D = document, $1 = (s, r) => (r || D).querySelector(s);
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const P = () => { try { return ST.profile || null; } catch (e) { return null; } };
  const isCA = () => !!(P() && P().course === 'ca');
  const caLevel = () => { try { return (ST.ca && ST.ca.level) || 'foundation'; } catch (e) { return 'foundation'; } };
  const NM = { foundation: 'CA Foundation', inter: 'CA Intermediate', final: 'CA Final' };
  function next() {
    const p = P(); if (!p) return null;
    if (isCA()) { const l = caLevel(); const L = l === 'foundation' ? ['inter', 'final'] : l === 'inter' ? ['final'] : []; return L.length ? { ca: L, title: L.map(x => NM[x]).join(' & ') } : null; }
    const g = +p.grade; return g >= 1 && g < 12 ? { g: g + 1, title: `Grade ${g + 1}` } : null;
  }
  const cardHTML = n => `<span class="nx-e" aria-hidden="true">🔭</span><span class="nx-t"><b>Sneak peek: ${E(n.title)}</b><small>See what you’ll explore next — keep going, it’s coming!</small></span><span class="nx-c" aria-hidden="true">›</span>`;
  function place() {
    const n = next(); style();
    const hosts = [D.getElementById('s-me'), D.getElementById('s-world')];
    const ca = D.getElementById('s-ca'); if (ca) hosts.push(ca);
    hosts.forEach(h => {
      if (!h || !h.firstElementChild) return;
      let c = h.querySelector(':scope > .nx-card');
      const ok = n && (h.id !== 's-ca' || (isCA() && !!h.querySelector(':scope > .ca-prof, .ca-top .ca-chip.lvl'))) && (h.id !== 's-world' || !isCA());
      if (!ok) { if (c) c.remove(); return; }
      if (!c) { c = D.createElement('button'); c.type = 'button'; c.className = 'card nx-card'; c.onclick = () => { S('open'); open(); }; h.appendChild(c); }
      const html = cardHTML(n); if (c.dataset.h !== html) { c.dataset.h = html; c.innerHTML = html; }
    });
  }
  let sh = null;
  /* the trailer: hero with the next world's name, live counters, "you'll discover" teasers, how close the unlock is,
     then EVERY subject → chapter → topic (searchable). Read-only: nothing opens early. */
  const count = (el, n) => { let i = 0; const st = Math.max(1, Math.ceil(n / 30)); const t = setInterval(() => { i = Math.min(n, i + st); el.textContent = i; if (i >= n) clearInterval(t); }, 30); };
  async function data(n) {
    const out = { secs: [] };
    if (n.ca) {
      for (const l of n.ca) {
        const st = await loadJSON(`content/ca/${l}/structure.json`);
        out.secs.push({ lv: NM[l], subs: (st.papers || []).map(p => ({ e: '📘', name: p.name, ch: (p.chapters || []).map(c => ({ t: c.title, tp: [].concat(...(c.units || []).map(u => (u.topics && u.topics.length ? u.topics : [u.title]))) })) })) });
      }
      const units = Object.keys((ST.ca && ST.ca.units) || {}).length, cur = await loadJSON(`content/ca/${caLevel()}/structure.json`).catch(() => null);
      const tot = cur ? [].concat(...(cur.papers || []).map(p => [].concat(...(p.chapters || []).map(c => c.units || [])))).length : 0;
      out.prog = tot ? { done: Math.min(units, tot), tot, what: 'units of ' + NM[caLevel()] } : null;
      out.world = NM[n.ca[0]];
    } else {
      const subs = typeof curSubjects === 'function' ? curSubjects(n.g) : ((CUR && CUR.grades && CUR.grades[n.g]) || {}).subjects || [];
      const SSt = (window.Worlds && Worlds.SUBJECT_STYLE) || {};
      out.secs.push({ subs: subs.map(sb => ({ e: (SSt[sb.id] || {}).e || '📘', name: sb.name, book: sb.book, ch: (sb.chapters || []).map(c => ({ t: c.title, tp: c.topics || [] })) })) });
      const cs = typeof curSubjects === 'function' ? curSubjects(n.g - 1) : [], tot = cs.reduce((a, sb) => a + (sb.chapters || []).reduce((x, c) => x + (c.topics || []).length, 0), 0);
      const done = Object.keys(ST.topics || {}).filter(k => k.startsWith(`g${n.g - 1}-`) && (ST.topics[k].stars || 0) >= 1).length;
      out.prog = tot ? { done: Math.min(done, tot), tot, what: `topics of Grade ${n.g - 1}` } : null;
      const th = window.Worlds && Worlds.THEMES && Worlds.THEMES[n.g]; out.world = th ? th.name : `Grade ${n.g}`; out.tag = th && th.tag;
    }
    return out;
  }
  async function open() {
    const n = next(); if (!n) return;
    if (!sh) { sh = D.createElement('div'); sh.className = 'sheet nx-sheet'; sh.setAttribute('role', 'dialog'); sh.setAttribute('aria-modal', 'true'); sh.setAttribute('aria-labelledby', 'nxT'); D.body.appendChild(sh); sh.onclick = e => { if (e.target === sh) sh.classList.remove('show'); }; }
    sh.innerHTML = `<div class="sheet-in"><div class="sheet-grab"></div><div class="nx-head"><span></span><button type="button" class="nx-x" data-close>Close ✕</button></div><p class="nx-load">🎬 Loading the trailer…</p></div>`;
    sh.classList.add('show'); $1('[data-close]', sh).onclick = () => sh.classList.remove('show');
    let d; try { d = await data(n); } catch (e) { $1('.nx-load', sh).textContent = 'Could not load. Check your internet and try again.'; return; }
    const all = [].concat(...d.secs.map(x => x.subs)), nCh = all.reduce((a, x) => a + x.ch.length, 0), nTp = all.reduce((a, x) => a + x.ch.reduce((y, c) => y + c.tp.length, 0), 0);
    const pool = [].concat(...all.map(x => [].concat(...x.ch.map(c => c.tp.map(t => ({ t, e: x.e })))))).filter(x => x.t && x.t.length > 8 && x.t.length < 70);
    const teas = []; for (let i = 0; i < 6 && pool.length; i++) teas.push(pool.splice(Math.floor(Math.random() * pool.length), 1)[0]);
    const pr = d.prog, pct = pr ? Math.round(pr.done / pr.tot * 100) : 0;
    const subHTML = (x, open) => `<details class="nx-sub"${open ? ' open' : ''}><summary><span class="nx-se">${x.e}</span><b>${E(x.name)}</b><small>${x.ch.length} chapters · ${x.ch.reduce((a, c) => a + c.tp.length, 0)} topics</small></summary>
      ${x.ch.map((c, i) => `<details class="nx-ch"><summary><i>${i + 1}</i>${E(c.t)}<small>${c.tp.length || ''}</small></summary>${c.tp.length ? `<ul>${c.tp.map(t => `<li>✨ ${E(t)}</li>`).join('')}</ul>` : ''}</details>`).join('')}</details>`;
    $1('.sheet-in', sh).innerHTML = `<div class="sheet-grab"></div><div class="nx-head"><span></span><button type="button" class="nx-x" data-close>Close ✕</button></div>
      <div class="nx-hero"><div class="nx-film">🎬 COMING NEXT</div><h3 id="nxT">${E(n.title)}</h3><p class="nx-world">${n.ca ? '🎓' : '🗺️'} ${E(d.world)}${d.tag ? ' — ' + E(d.tag) : ''}</p>
        <div class="nx-cnt"><div><b data-c="${all.length}">0</b><span>${n.ca ? 'papers' : 'subjects'}</span></div><div><b data-c="${nCh}">0</b><span>chapters</span></div><div><b data-c="${nTp}">0</b><span>topics</span></div></div></div>
      ${teas.length ? `<div class="nx-teas"><h4>🔮 You’ll discover…</h4><div class="nx-tg">${teas.map((x, i) => `<span style="--d:${i * .12}s">${x.e} ${E(x.t)}</span>`).join('')}</div></div>` : ''}
      ${pr ? `<div class="nx-key"><div class="nx-keyt"><span>🔐 Your key to ${E(n.title)}</span><b>${pct}%</b></div><div class="nx-bar"><i style="width:${pct}%"></i></div><small>${pr.done} of ${pr.tot} ${E(pr.what)} done. ${pct >= 100 ? 'Amazing — you’re ready for the next level!' : 'Every topic you finish now makes the next level easier!'}</small></div>` : ''}
      <input class="nx-q" type="search" placeholder="🔍 Search what’s coming…" aria-label="Search the next level’s topics">
      <div class="nx-list">${d.secs.map((sec, k) => `${sec.lv ? `<h4 class="nx-lv">🎓 ${E(sec.lv)}</h4>` : ''}${sec.subs.map((x, i) => subHTML(x, k === 0 && i === 0)).join('')}`).join('')}</div>
      <p class="nx-note">👀 Just a peek — this opens when you move up. Keep learning: you’re building the key!</p>`;
    $1('[data-close]', sh).onclick = () => sh.classList.remove('show');
    sh.querySelectorAll('[data-c]').forEach(el => count(el, +el.dataset.c));
    const q = $1('.nx-q', sh);
    q.oninput = () => { const v = q.value.trim().toLowerCase();
      sh.querySelectorAll('.nx-sub').forEach(sb => { let any = false;
        sb.querySelectorAll('.nx-ch').forEach(ch => { const hit = !v || ch.textContent.toLowerCase().includes(v); ch.hidden = !hit; if (v && hit) ch.open = true; any = any || hit; });
        sb.hidden = !any; if (v && any) sb.open = true; }); };
  }
  let css = false;
  function style() {
    if (css) return; css = true;
    D.head.insertAdjacentHTML('beforeend', `<style id="nxCss">
      .nx-card{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:0;cursor:pointer;font:inherit;background:linear-gradient(135deg,#1b2a6b,#5b3fd1);color:#fff}
      .nx-card .nx-e{font-size:34px;animation:nxB 3s ease-in-out infinite}.nx-card .nx-t{flex:1;display:flex;flex-direction:column}.nx-card small{opacity:.85}.nx-card .nx-c{font-size:22px}
      #s-me.me-lay>.nx-card{order:23}#s-ca.me-lay>.nx-card{order:23}
      .nx-head{display:flex;justify-content:space-between;align-items:center;gap:8px}
      .nx-hero{text-align:center;border-radius:20px;padding:16px;color:#fff;background:linear-gradient(135deg,#ff6a88,#7b5cff 55%,#20c4ff);background-size:200% 200%;animation:nxG 6s ease infinite}
      .nx-film{display:inline-block;font-weight:900;font-size:11px;letter-spacing:.2em;background:rgba(0,0,0,.25);border-radius:999px;padding:4px 10px}.nx-hero h3{margin:6px 0 2px;font-size:24px}.nx-world{margin:0 0 10px;opacity:.95}
      .nx-cnt{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.nx-cnt div{background:rgba(255,255,255,.18);border-radius:14px;padding:8px}.nx-cnt b{display:block;font-size:26px}.nx-cnt span{font-size:12px}
      .nx-teas h4{margin:14px 0 6px}.nx-tg{display:flex;flex-wrap:wrap;gap:6px}.nx-tg span{background:#fff4d6;border-radius:999px;padding:6px 10px;font-size:13px;font-weight:700;animation:mpPop .4s both;animation-delay:var(--d)}
      .nx-key{margin:14px 0;padding:12px;border-radius:16px;background:#f0fbf5}.nx-keyt{display:flex;justify-content:space-between;font-weight:800}.nx-bar{height:12px;border-radius:9px;background:#dfe9e3;margin:6px 0;overflow:hidden}.nx-bar i{display:block;height:100%;background:linear-gradient(90deg,#21b573,#ffc43d)}
      .nx-key small{color:#466}.nx-q{width:100%;box-sizing:border-box;padding:11px 12px;border-radius:12px;border:1.5px solid #ddd;font-size:15px;margin:6px 0}
      .nx-se{font-size:22px}.nx-sub summary b{flex:1}.nx-ch{margin:4px 0 4px 6px;border-left:3px solid #e2dbff;padding:2px 0 2px 10px}.nx-ch summary{display:flex;gap:8px;align-items:baseline;cursor:pointer;list-style:none;font-weight:600}
      .nx-ch summary i{font-style:normal;font-weight:900;color:#7b5cff;min-width:18px}.nx-ch summary small{margin-left:auto;color:#99a}.nx-ch ul{margin:4px 0 6px;padding-left:18px;list-style:none}.nx-ch li{font-size:14px;margin:2px 0}
      @keyframes nxG{50%{background-position:100% 50%}}.nx-x{border:0;background:transparent;font-weight:800;cursor:pointer;color:inherit;font-family:inherit}
      .nx-sheet .sheet-in{max-height:88vh;overflow:auto}.nx-note{background:#f3f0ff;border-radius:12px;padding:10px;font-size:14px}.nx-lv{margin:14px 0 6px}
      .nx-sub{border-radius:14px;background:#f7f7fb;margin:8px 0;padding:8px 12px}.nx-sub summary{display:flex;justify-content:space-between;gap:8px;cursor:pointer;list-style:none}.nx-sub summary::after{content:"▾";opacity:.6}
      .nx-sub summary small{color:#667;flex:1;text-align:right}.nx-sub ol{margin:8px 0 4px;padding-left:22px}.nx-sub li{margin:3px 0}.nx-sub li small{color:#778}
      @keyframes nxB{50%{transform:translateY(-4px) rotate(-6deg)}}
    </style>`);
  }
  let t = 0;
  function boot() { new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; try { place(); } catch (e) {} }); }).observe(D.querySelector('main') || D.body, { childList: true, subtree: true }); place(); }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
  window.NextUp = { open };
})();
