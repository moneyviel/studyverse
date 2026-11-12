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
  async function open() {
    const n = next(); if (!n) return;
    if (!sh) { sh = D.createElement('div'); sh.className = 'sheet nx-sheet'; sh.setAttribute('role', 'dialog'); sh.setAttribute('aria-modal', 'true'); sh.setAttribute('aria-labelledby', 'nxT'); D.body.appendChild(sh); sh.onclick = e => { if (e.target === sh) sh.classList.remove('show'); }; }
    sh.innerHTML = `<div class="sheet-in"><div class="sheet-grab"></div><div class="nx-head"><h3 id="nxT">🔭 Coming next: ${E(n.title)}</h3><button type="button" class="nx-x" data-close>Close</button></div><p class="nx-load">Loading…</p></div>`;
    sh.classList.add('show'); $1('[data-close]', sh).onclick = () => sh.classList.remove('show');
    let body = '';
    try {
      if (n.ca) {
        for (const l of n.ca) {
          const st = await loadJSON(`content/ca/${l}/structure.json`);
          body += `<h4 class="nx-lv">🎓 ${E(NM[l])}</h4>` + (st.papers || []).map((p, i) => `<details class="nx-sub"${i === 0 && l === n.ca[0] ? ' open' : ''}><summary><b>${E(p.name)}</b><small>${(p.chapters || []).length} chapters</small></summary><ol>${(p.chapters || []).map(c => `<li>${E(c.title)}${(c.units || []).length > 1 ? `<small> · ${c.units.length} units</small>` : ''}</li>`).join('')}</ol></details>`).join('');
        }
      } else {
        const subs = typeof curSubjects === 'function' ? curSubjects(n.g) : ((CUR && CUR.grades && CUR.grades[n.g]) || {}).subjects || [];
        body = subs.map((s, i) => `<details class="nx-sub"${i === 0 ? ' open' : ''}><summary><b>${E(s.name)}</b><small>${(s.chapters || []).length} chapters${s.book ? ' · ' + E(s.book) : ''}</small></summary><ol>${(s.chapters || []).map(c => `<li>${E(c.title)}</li>`).join('')}</ol></details>`).join('')
          || '<p>Coming soon.</p>';
      }
    } catch (e) { body = '<p>Could not load. Check your internet and try again.</p>'; }
    const tip = n.ca ? 'Finish your current level strongly — every unit you master now makes the next level easier.' : `Finish Grade ${n.g - 1} strongly — every topic you master now makes Grade ${n.g} easier.`;
    $1('.nx-load', sh).outerHTML = `<p class="nx-note">👀 Just a peek — these open when you move up. ${E(tip)}</p>${body}`;
  }
  let css = false;
  function style() {
    if (css) return; css = true;
    D.head.insertAdjacentHTML('beforeend', `<style id="nxCss">
      .nx-card{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:0;cursor:pointer;font:inherit;background:linear-gradient(135deg,#1b2a6b,#5b3fd1);color:#fff}
      .nx-card .nx-e{font-size:34px;animation:nxB 3s ease-in-out infinite}.nx-card .nx-t{flex:1;display:flex;flex-direction:column}.nx-card small{opacity:.85}.nx-card .nx-c{font-size:22px}
      #s-me.me-lay>.nx-card{order:23}#s-ca.me-lay>.nx-card{order:23}
      .nx-head{display:flex;justify-content:space-between;align-items:center;gap:8px}.nx-head h3{margin:0}.nx-x{border:0;background:transparent;font-weight:800;cursor:pointer;color:inherit;font-family:inherit}
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
