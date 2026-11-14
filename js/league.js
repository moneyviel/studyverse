/* 💎 Ratna League — a weekly league of up to 30 students at the same level.
   Points come only from LEARNING (never from games) and are decided by the server (rpc league_award):
   finish a topic or unit +20 · revise a finished topic +10 · fix an old mistake +4 · right answer +2 ·
   back after 3+ days +15 · at most 200 a day. Monday (IST): top 5 move up a gem, bottom 5 move down.
   Owner-only until the server switch studyverse.league_settings.live is turned on (LIVE below too). */
(function () {
  'use strict';
  const LIVE = false;
  const D = document;
  const TIERS = [
    { n: 'Mitti', h: 'Clay', c1: '#b9855a', c2: '#6e4526' },
    { n: 'Tamba', h: 'Copper', c1: '#f0a067', c2: '#a24f1f' },
    { n: 'Chandi', h: 'Silver', c1: '#f4f6fa', c2: '#8d97a8' },
    { n: 'Sona', h: 'Gold', c1: '#ffe27a', c2: '#c48a10' },
    { n: 'Heera', h: 'Diamond', c1: '#e8fbff', c2: '#6fc6e8' },
    { n: 'Navratna', h: 'Nine gems', c1: '#ff9ad5', c2: '#6a4cff' },
    { n: 'Kohinoor', h: 'The crown jewel', c1: '#fffbe6', c2: '#ffb300' }
  ];
  const EARN = [['📗', 'Finish a topic or unit', 20], ['🔁', 'Revise a topic you finished', 10], ['🩹', 'Get right a question you once got wrong', 4], ['✅', 'Right answer', 2], ['👋', 'Come back after 3+ days', 15]];
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const ls = (k, v) => { try { if (v === undefined) return JSON.parse(localStorage.getItem(k) || 'null'); localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } };
  const isOwner = () => { try { return localStorage.getItem('sv_owner') === '1' || !!(window.Cloud && Cloud.admin && Cloud.admin()); } catch (e) { return false; } };
  const signedIn = () => !!(window.Cloud && Cloud.signedIn && Cloud.signedIn());
  const parentAcct = () => { try { return !!(window.Cloud && Cloud.isParent && Cloud.isParent()); } catch (e) { return false; } };
  const visible = () => (LIVE || isOwner()) && signedIn() && !parentAcct();
  const prof = () => { try { return (typeof ST !== 'undefined' && ST && ST.profile) || {}; } catch (e) { return {}; } };   // ST is app.js's global (let, so not on window)
  /* students race others at the same level: CA level, JEE, or school class (+ stream for 11–12) */
  function lvl() {
    const p = prof();
    if (p.course === 'ca') { let l = 'foundation'; try { l = (ST.ca && ST.ca.level) || l; } catch (e) {} return 'ca-' + l; }
    try { if (window.Jee && Jee.active && Jee.active()) return 'jee'; } catch (e) {}
    const g = +p.grade || 1; return 'g' + g + (g >= 11 && p.stream ? '-' + String(p.stream).toLowerCase().replace(/[^a-z0-9]/g, '') : '');
  }
  const todayIST = () => new Date(Date.now() + 5.5 * 36e5).toISOString().slice(0, 10);
  const one = r => Array.isArray(r) ? r[0] : r;
  const rpc = (fn, body) => Cloud.rest('rpc/' + fn, { method: 'POST', body }).then(one);
  const who = () => ({ p_lvl: lvl(), p_name: String(prof().name || 'Student').slice(0, 40), p_avatar: String(prof().avatar || '🙂').slice(0, 8) });
  const safeRef = s => String(s || '').replace(/[^A-Za-z0-9:_./-]/g, '_').slice(0, 90) || 'x';

  /* ---------- earning: a small queue, one call at a time ---------- */
  const Q = []; let busy = false;
  function push(kind, ref) { if (!visible()) return; Q.push([kind, safeRef(ref)]); if (Q.length > 40) Q.shift(); pump(); }
  async function pump() {
    if (busy) return; busy = true;
    try {
      while (Q.length) {
        const [kind, ref] = Q.shift();
        try {
          const r = await rpc('league_award', Object.assign({ p_kind: kind, p_ref: ref }, who()));
          if (r && r.ok && r.pts > 0) { pop(r); const c = ls('sv_lg'); if (c) { c.points = (c.points || 0) + r.pts; c.today = r.today; ls('sv_lg', c); paintBanners(); } }
          if (r && r.why === 'off') { Q.length = 0; break; }
        } catch (e) { if (e && e.status === 0) { Q.unshift([kind, ref]); break; } }
      }
    } finally { busy = false; }
  }
  /* same question right again the same day counts once; at most 10 right answers per topic a day from here */
  function ans(id, ok) {
    if (!ok || !visible()) return;
    const base = String(id || '').split('#')[0] || 'q', d = todayIST(); let m = ls('sv_lgc');
    if (!m || m.d !== d) m = { d, m: {} };
    const n = m.m[base] = (m.m[base] || 0) + 1; ls('sv_lgc', m);
    if (n <= 10) push('right', String(id || base).includes('#') ? String(id) : base + '.' + n);
  }
  const fix = id => push('fix', id);
  const topic = (id, again) => push(again ? 'revise' : 'topic', id);
  const unit = id => push('unit', id);

  function pop(r) {
    let t = D.getElementById('lgPop'); if (!t) { t = D.createElement('div'); t.id = 'lgPop'; t.className = 'lg-pop'; t.setAttribute('role', 'status'); D.body.appendChild(t); }
    t.innerHTML = `<i class="lg-gem lg-gem-s" style="${gemCss((ls('sv_lg') || {}).tier || 0)}"></i> +${r.pts}${r.comeback ? ' · welcome back!' : ''}`;
    t.classList.remove('show'); void t.offsetWidth; t.classList.add('show'); clearTimeout(pop.t); pop.t = setTimeout(() => t.classList.remove('show'), 1800);
  }

  /* ---------- look ---------- */
  const gemCss = i => { const t = TIERS[Math.max(0, Math.min(6, i | 0))]; return `--g1:${t.c1};--g2:${t.c2}`; };
  function css() {
    if (D.getElementById('lgCss')) return;
    const s = D.createElement('style'); s.id = 'lgCss';
    s.textContent = `
.lg-gem{display:inline-block;width:56px;height:56px;background:linear-gradient(150deg,var(--g1) 0%,var(--g1) 35%,var(--g2) 100%);clip-path:polygon(50% 0,100% 32%,82% 100%,18% 100%,0 32%);position:relative;filter:drop-shadow(0 4px 10px rgba(0,0,0,.35));vertical-align:middle}
.lg-gem:after{content:"";position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.75) 0 18%,transparent 19% 48%,rgba(255,255,255,.25) 49% 56%,transparent 57%);clip-path:polygon(50% 0,100% 32%,50% 46%,0 32%)}
.lg-gem-s{width:18px;height:18px;filter:none}.lg-gem-m{width:30px;height:30px}.lg-gem-xl{width:118px;height:118px}
.lg-ban{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:0;cursor:pointer;margin:0 0 12px;padding:14px 16px;border-radius:18px;color:#fff;font:inherit;background:radial-gradient(120% 140% at 0% 0%,#3b2a7a 0%,#1a1440 60%,#0e0b26 100%);box-shadow:0 6px 18px rgba(20,10,60,.35)}
.lg-ban b{display:block;font-size:1.02rem}.lg-ban small{opacity:.85}.lg-ban .lg-go{margin-left:auto;font-size:1.3rem;opacity:.9}
.lg-ov{position:fixed;inset:0;z-index:9000;overflow:auto;color:#fff;background:radial-gradient(130% 70% at 50% 0%,#3d2b86 0%,#17123a 55%,#0b0920 100%);-webkit-overflow-scrolling:touch}
.lg-in{max-width:560px;margin:0 auto;padding:14px 14px 40px}
.lg-top{display:flex;align-items:center;gap:10px}.lg-top h1{font-size:1.15rem;margin:0;flex:1}
.lg-x{background:rgba(255,255,255,.12);border:0;color:#fff;border-radius:12px;padding:8px 12px;font:inherit;cursor:pointer}
.lg-hero{text-align:center;padding:18px 0 6px;position:relative}
.lg-hero:before{content:"";position:absolute;left:50%;top:22px;width:190px;height:190px;transform:translateX(-50%);border-radius:50%;background:radial-gradient(circle,var(--g1) 0%,transparent 65%);opacity:.35;animation:lgGlow 3s ease-in-out infinite}
@keyframes lgGlow{50%{opacity:.6;transform:translateX(-50%) scale(1.08)}}
.lg-hero .lg-gem-xl{animation:lgFloat 3.4s ease-in-out infinite}@keyframes lgFloat{50%{transform:translateY(-6px) rotate(-2deg)}}
.lg-tn{font-size:1.6rem;font-weight:800;margin:12px 0 0;letter-spacing:.5px}.lg-th{opacity:.8;font-size:.9rem}
.lg-pills{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin:12px 0 4px}
.lg-pill{background:rgba(255,255,255,.12);border-radius:999px;padding:6px 12px;font-size:.88rem}
.lg-lad{display:flex;justify-content:space-between;align-items:flex-end;margin:16px 2px 6px;padding:12px 10px;border-radius:16px;background:rgba(255,255,255,.06)}
.lg-step{text-align:center;font-size:.62rem;opacity:.45;width:14%}.lg-step.on{opacity:1;font-weight:700}.lg-step.past{opacity:.8}
.lg-step .lg-gem{display:block;margin:0 auto 4px}.lg-step.on .lg-gem{transform:scale(1.25);margin-bottom:8px}
.lg-day{margin:14px 0 4px;font-size:.85rem}.lg-bar{height:10px;border-radius:9px;background:rgba(255,255,255,.12);overflow:hidden;margin-top:6px}
.lg-bar i{display:block;height:100%;border-radius:9px;background:linear-gradient(90deg,#7cf0c4,#ffe27a)}
.lg-card{background:rgba(255,255,255,.07);border-radius:16px;padding:12px;margin-top:14px}
.lg-card h3{margin:0 0 8px;font-size:1rem}
.lg-row{display:flex;align-items:center;gap:10px;padding:8px 8px;border-radius:12px}
.lg-row+.lg-row{margin-top:2px}.lg-row.me{background:rgba(255,226,122,.18);outline:1px solid rgba(255,226,122,.5)}
.lg-rk{width:24px;text-align:center;font-weight:800;opacity:.9}.lg-av{font-size:1.3rem;width:30px;text-align:center}.lg-nm{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.lg-pt{font-weight:700}
.lg-zone{font-size:.72rem;letter-spacing:.4px;text-transform:uppercase;padding:6px 8px 2px;opacity:.85}
.lg-up{color:#7cf0c4}.lg-dn{color:#ff9a9a}
.lg-earn{display:flex;align-items:center;gap:10px;padding:6px 2px;font-size:.92rem}.lg-earn span:nth-child(2){flex:1}.lg-earn b{color:#ffe27a}
.lg-ov .lg-note{font-size:.8rem;opacity:.75;margin:10px 0 0;line-height:1.4;background:none;border:0;padding:0;color:inherit;box-shadow:none}
.lg-msg{text-align:center;padding:40px 10px;opacity:.9}
.lg-res{position:fixed;inset:0;z-index:9100;display:flex;align-items:center;justify-content:center;background:rgba(5,3,20,.78);padding:20px}
.lg-res>div{text-align:center;max-width:320px;background:radial-gradient(120% 100% at 50% 0%,#4a35a0,#1a1440);border-radius:22px;padding:26px 20px;box-shadow:0 10px 40px rgba(0,0,0,.5)}
.lg-res .lg-gem-xl{animation:lgSpin 1.1s cubic-bezier(.2,1.4,.4,1) both}@keyframes lgSpin{from{transform:scale(.2) rotate(-200deg);opacity:0}}
.lg-res h2{margin:14px 0 6px;color:#fff}.lg-res p{opacity:.85;margin:0 0 16px;color:#fff}.lg-ov h1,.lg-ov h3{color:#fff}
.lg-btn{background:linear-gradient(180deg,#ffe27a,#f5b70f);color:#3a2500;border:0;border-radius:14px;padding:12px 22px;font:inherit;font-weight:800;cursor:pointer}
.lg-pop{position:fixed;left:50%;bottom:86px;transform:translate(-50%,20px);opacity:0;z-index:9050;pointer-events:none;background:#1a1440;color:#ffe27a;font-weight:800;padding:8px 14px;border-radius:999px;box-shadow:0 6px 18px rgba(0,0,0,.35);transition:.25s;display:flex;align-items:center;gap:8px}
.lg-pop.show{opacity:1;transform:translate(-50%,0)}
.lg-own{display:inline-block;font-size:.7rem;background:rgba(255,255,255,.14);border-radius:8px;padding:2px 6px;margin-left:6px;vertical-align:middle}
@media (prefers-reduced-motion:reduce){.lg-hero:before,.lg-hero .lg-gem-xl,.lg-res .lg-gem-xl{animation:none}}`;
    D.head.appendChild(s);
  }

  /* ---------- banner on the Squad / Group tab ---------- */
  function bannerInner() {
    const c = ls('sv_lg'), t = TIERS[(c && c.tier) || 0];
    const rk = c && c.rank ? `#${c.rank} of ${c.n}` : 'Join this week';
    return `<i class="lg-gem lg-gem-m" style="${gemCss((c && c.tier) || 0)}"></i><span><b>Ratna League · ${esc(t.n)}${!LIVE ? '<span class="lg-own">🔑 only you</span>' : ''}</b><small>${c ? `${rk} · ${c.points || 0} points this week` : 'Learn every day, climb the gems'}</small></span><span class="lg-go" aria-hidden="true">›</span>`;
  }
  /* the banner refreshes itself quietly (at most every 5 minutes); a week's result waits for the next open */
  let bgBusy = false;
  async function refresh() {
    const c = ls('sv_lg'); if (bgBusy || !visible() || (c && Date.now() - (c.at || 0) < 3e5)) return; bgBusy = true;
    try { const r = await rpc('league_board', who()); if (r && r.ok) remember(r, r.result || (c && c.pend) || null); } catch (e) {} finally { bgBusy = false; }
  }
  function remember(r, pend) {
    const rows = r.rows || [], me = rows.findIndex(x => x.me);
    ls('sv_lg', { tier: r.tier | 0, points: r.points, today: r.today, rank: me + 1, n: rows.length, at: Date.now(), pend: pend || null }); paintBanners();
  }
  function banner() { if (!visible()) return ''; css(); setTimeout(refresh, 0); return `<button class="lg-ban" data-league>${bannerInner()}</button>`; }
  function paintBanners() { D.querySelectorAll('.lg-ban').forEach(b => { b.innerHTML = bannerInner(); }); }
  D.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-league]'); if (b) { e.preventDefault(); open(); } });

  /* ---------- the league screen ---------- */
  let OV = null, tick = null;
  function close() { if (OV) { OV.remove(); OV = null; } clearInterval(tick); D.removeEventListener('keydown', onKey); }
  const onKey = e => { if (e.key === 'Escape') close(); };
  function left(ends) {
    const ms = new Date(ends) - Date.now(); if (!(ms > 0)) return 'ending now';
    const d = Math.floor(ms / 864e5), h = Math.floor(ms % 864e5 / 36e5), m = Math.floor(ms % 36e5 / 6e4);
    return d ? `${d}d ${h}h left` : h ? `${h}h ${m}m left` : `${m}m left`;
  }
  async function open() {
    if (!visible()) return;
    css(); close();
    try { if (window.sfx) sfx('open'); } catch (e) {}
    OV = D.createElement('div'); OV.className = 'lg-ov'; OV.setAttribute('role', 'dialog'); OV.setAttribute('aria-label', 'Ratna League');
    OV.innerHTML = `<div class="lg-in"><div class="lg-top"><button class="lg-x" id="lgBack">‹ Back</button><h1>Ratna League</h1></div><div id="lgBody"><p class="lg-msg" role="status">Opening the vault…</p></div></div>`;
    D.body.appendChild(OV); D.addEventListener('keydown', onKey);
    OV.querySelector('#lgBack').onclick = () => { try { if (window.sfx) sfx('tap'); } catch (e) {} close(); };
    let r;
    try { r = await rpc('league_board', who()); }
    catch (e) { const b = OV && OV.querySelector('#lgBody'); if (b) b.innerHTML = `<p class="lg-msg">${esc((window.Cloud && Cloud.errText && Cloud.errText(e)) || 'No connection.')}<br><br><button class="lg-btn" id="lgRetry">Try again</button></p>`; const t = OV && OV.querySelector('#lgRetry'); if (t) t.onclick = open; return; }
    if (!OV) return;
    if (!r || !r.ok) { OV.querySelector('#lgBody').innerHTML = `<p class="lg-msg">${r && r.why === 'off' ? 'The league is not open yet.' : 'Could not open the league. Please try again.'}</p>`; return; }
    const pend = r.result || ((ls('sv_lg') || {}).pend);
    paint(r);
    if (pend) result(pend);
  }
  function paint(r) {
    const rows = r.rows || [], n = rows.length, me = rows.findIndex(x => x.me), tier = r.tier | 0, t = TIERS[tier];
    remember(r, null);
    const upTo = tier < 6 ? Math.min(5, n) : 0, dnFrom = n >= 10 && tier > 0 ? n - 5 : n;
    const row = (x, i) => `<div class="lg-row${x.me ? ' me' : ''}"><span class="lg-rk">${i + 1}</span><span class="lg-av" aria-hidden="true">${esc(x.a)}</span><span class="lg-nm">${esc(x.n)}${x.me ? ' (you)' : ''}</span><span class="lg-pt">${x.p}</span></div>`;
    let list = '';
    rows.forEach((x, i) => {
      if (i === 0 && upTo) list += `<div class="lg-zone lg-up">⬆ Top ${upTo} rise to ${esc(TIERS[tier + 1].n)}</div>`;
      if (i === upTo && upTo && i < dnFrom) list += `<div class="lg-zone">Stay in ${esc(t.n)}</div>`;
      if (i === dnFrom && dnFrom < n) list += `<div class="lg-zone lg-dn">⬇ Bottom 5 slip to ${esc(TIERS[tier - 1].n)}</div>`;
      list += row(x, i);
    });
    const pct = Math.min(100, (r.today || 0) / (r.cap || 200) * 100);
    const body = OV.querySelector('#lgBody');
    body.innerHTML = `
      <div class="lg-hero" style="${gemCss(tier)}"><i class="lg-gem lg-gem-xl" style="${gemCss(tier)}"></i>
        <div class="lg-tn">${esc(t.n)}</div><div class="lg-th">${esc(t.h)} league · ${n} student${n === 1 ? '' : 's'} at your level</div>
        <div class="lg-pills"><span class="lg-pill">🏅 #${me + 1} of ${n}</span><span class="lg-pill">⭐ ${r.points} this week</span><span class="lg-pill" id="lgLeft">⏳ ${left(r.ends)}</span></div></div>
      <div class="lg-lad" aria-label="Gem ladder">${TIERS.map((x, i) => `<div class="lg-step${i === tier ? ' on' : i < tier ? ' past' : ''}"><i class="lg-gem lg-gem-m" style="${gemCss(i)}"></i>${esc(x.n)}</div>`).join('')}</div>
      <div class="lg-day">Today: <b>${r.today || 0}</b> of ${r.cap || 200} points<div class="lg-bar"><i style="width:${pct}%"></i></div></div>
      <div class="lg-card"><h3>This week</h3>${list || '<p class="lg-note">You are the first one here this week.</p>'}</div>
      <div class="lg-card"><h3>How to earn points</h3>${EARN.map(([e, d, p]) => `<div class="lg-earn"><span aria-hidden="true">${e}</span><span>${esc(d)}</span><b>+${p}</b></div>`).join('')}
        <p class="lg-note">Points come only from studying, not from games. Up to 200 a day. A new week starts every Monday (India time): the top 5 rise one gem, the bottom 5 slip one gem.</p></div>`;
    clearInterval(tick); tick = setInterval(() => { const el = OV && OV.querySelector('#lgLeft'); if (!el) return clearInterval(tick); el.textContent = '⏳ ' + left(r.ends); }, 30000);
  }
  function result(res) {
    const [k, v] = String(res).split(':'), i = Math.max(0, Math.min(6, +v || 0)), t = TIERS[i];
    const h = k === 'up' ? `You rose to ${t.n}!` : k === 'down' ? `Back to ${t.n}` : `You stayed in ${t.n}`;
    const p = k === 'up' ? 'Great week of study. A new league has begun — keep going!' : k === 'down' ? 'A fresh week, a fresh start. A little study every day brings you back up.' : 'Steady work. Finish a few more topics this week to rise.';
    const m = D.createElement('div'); m.className = 'lg-res'; m.setAttribute('role', 'alertdialog');
    m.innerHTML = `<div><i class="lg-gem lg-gem-xl" style="${gemCss(i)}"></i><h2>${esc(h)}</h2><p>${esc(p)}</p><button class="lg-btn">Let's go</button></div>`;
    D.body.appendChild(m); m.querySelector('button').onclick = () => m.remove();
    try { if (window.sfx) sfx(k === 'up' ? 'unlock' : 'open'); } catch (e) {}
  }

  window.League = { visible, live: LIVE, banner, open, ans, fix, topic, unit, TIERS, _lvl: lvl };
})();
