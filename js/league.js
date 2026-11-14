/* 🌱→🌌 Seed to Stars — the weekly study league.
   Points come only from LEARNING (never from games) and are decided by the server (rpc league_award):
   finish a topic or unit +20 · revise a finished topic +10 · fix an old mistake +4 · right answer +2 ·
   back after 3+ days +15 · at most 200 a day.
   Every student at the same level (class / JEE / CA level) is on one weekly board: rank, percentile, top 10,
   the 2 just above you, Hall of Fame (everyone who hit their weekly target), Most Improved, and a race against
   last week's you. Hit your level's weekly target → grow one level on Monday (IST); a week with no study at all
   → back one level. Levels: Seed, Sprout, Bloom, Tree, Summit, Sky, Star, Galaxy (rpc league_board).
   Owner-only until the server switch studyverse.league_settings.live is turned on (LIVE below too). */
(function () {
  'use strict';
  const LIVE = false;
  const D = document;
  const NAME = 'Seed to Stars';
  const TIERS = [
    { n: 'Seed', e: '🌱', h: 'you have just started', sky: '#8a5a2b', mid: '#5e3a1a', gr: '#3a2210', dk: false },
    { n: 'Sprout', e: '🌿', h: 'your first steady week', sky: '#3f9a4a', mid: '#2a7036', gr: '#174a22', dk: false },
    { n: 'Bloom', e: '🌸', h: 'studying regularly', sky: '#c2408a', mid: '#8e2a66', gr: '#5a1742', dk: false },
    { n: 'Tree', e: '🌳', h: 'strong roots', sky: '#1f8a5c', mid: '#146642', gr: '#0b432b', dk: false },
    { n: 'Summit', e: '⛰️', h: 'above the clouds', sky: '#5a6f9a', mid: '#3f5178', gr: '#273352', dk: false },
    { n: 'Sky', e: '☁️', h: 'flying high', sky: '#2f8fe8', mid: '#1f6cc4', gr: '#134a8e', dk: true },
    { n: 'Star', e: '⭐', h: 'shining for others', sky: '#2b3a8a', mid: '#1d2766', gr: '#111842', dk: true },
    { n: 'Galaxy', e: '🌌', h: 'the very top', sky: '#6a35b8', mid: '#4a2290', gr: '#2a1160', dk: true }
  ];
  const T = i => TIERS[Math.max(0, Math.min(7, i | 0))];
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
    t.textContent = `${T((ls('sv_lg') || {}).tier).e} +${r.pts}${r.comeback ? ' · welcome back!' : ''}`;
    t.classList.remove('show'); void t.offsetWidth; t.classList.add('show'); clearTimeout(pop.t); pop.t = setTimeout(() => t.classList.remove('show'), 1800);
  }

  /* ---------- words ---------- */
  function lvlName(k) {
    k = String(k || lvl());
    if (k === 'jee') return 'JEE';
    if (k.startsWith('ca-')) return 'CA ' + ({ foundation: 'Foundation', inter: 'Intermediate', final: 'Final' }[k.slice(3)] || '');
    const m = k.match(/^g(\d+)(?:-(\w+))?$/); if (m) return 'Class ' + m[1] + (m[2] ? ' ' + m[2][0].toUpperCase() + m[2].slice(1) : '');
    return 'your level';
  }
  const place = (rank, n) => !n ? '' : rank === 1 ? `#1 in ${lvlName()}` : `Top ${Math.max(1, Math.ceil(rank / n * 100))}% of ${lvlName()}`;

  /* ---------- look: every level is its own scene, soil to stars ---------- */
  const scene = i => { const t = T(i); return `--sky:${t.sky};--mid:${t.mid};--gr:${t.gr}`; };
  function css() {
    if (D.getElementById('lgCss')) return;
    const s = D.createElement('style'); s.id = 'lgCss';
    s.textContent = `
.lg-ban{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:0;cursor:pointer;margin:0 0 12px;padding:14px 16px;border-radius:18px;font:inherit;color:#fff;
 background:linear-gradient(180deg,var(--sky) 0%,var(--mid) 62%,var(--gr) 100%);box-shadow:0 6px 18px rgba(0,0,0,.25);text-shadow:0 1px 3px rgba(0,0,0,.45)}
.lg-ban .lg-e{font-size:2rem;line-height:1;filter:drop-shadow(0 2px 4px rgba(0,0,0,.3))}
.lg-ban b{display:block;font-size:1.02rem}.lg-ban small{opacity:.95}.lg-ban .lg-go{margin-left:auto;font-size:1.3rem}
.lg-ov{position:fixed;inset:0;z-index:9000;overflow:auto;color:#fff;background:linear-gradient(180deg,#141233 0%,#0b0920 100%);-webkit-overflow-scrolling:touch}
.lg-in{max-width:560px;margin:0 auto;padding:12px 14px 40px}
.lg-top{display:flex;align-items:center;gap:10px;margin-bottom:10px}.lg-top h1{font-size:1.1rem;margin:0;flex:1;color:#fff}
.lg-x{background:rgba(255,255,255,.14);border:0;color:#fff;border-radius:12px;padding:8px 12px;font:inherit;cursor:pointer}
.lg-scene{position:relative;overflow:hidden;border-radius:22px;padding:22px 16px 18px;text-align:center;min-height:230px;
 background:linear-gradient(180deg,var(--sky) 0%,var(--mid) 70%,var(--gr) 100%);text-shadow:0 1px 3px rgba(0,0,0,.35);box-shadow:inset 0 1px 0 rgba(255,255,255,.15)}
.lg-scene:after{content:"";position:absolute;left:-10%;right:-10%;bottom:-40px;height:72px;border-radius:50%;background:var(--gr);opacity:.55}
.lg-deco{position:absolute;font-size:1.1rem;opacity:.75;animation:lgDrift 7s ease-in-out infinite}
@keyframes lgDrift{50%{transform:translate(8px,-5px)}}
.lg-big{position:relative;z-index:1;font-size:4.6rem;line-height:1;display:inline-block;animation:lgGrow 3.6s ease-in-out infinite;filter:drop-shadow(0 6px 10px rgba(0,0,0,.3))}
@keyframes lgGrow{50%{transform:translateY(-6px) scale(1.04)}}
.lg-tn{position:relative;z-index:1;font-size:1.7rem;font-weight:800;margin:8px 0 0}.lg-th{position:relative;z-index:1;font-size:.92rem}
.lg-pills{position:relative;z-index:1;display:flex;justify-content:center;gap:6px;flex-wrap:wrap;margin-top:12px}
.lg-pill{background:rgba(0,0,0,.32);border-radius:999px;padding:6px 11px;font-size:.84rem;text-shadow:none}
.lg-path{display:flex;justify-content:space-between;align-items:center;margin:14px 0 4px;padding:10px 8px;border-radius:16px;background:rgba(255,255,255,.06);position:relative}
.lg-path:before{content:"";position:absolute;left:24px;right:24px;top:24px;border-top:2px dashed rgba(255,255,255,.25)}
.lg-st{position:relative;text-align:center;font-size:.58rem;width:12.5%;opacity:.45}.lg-st i{display:block;font-style:normal;font-size:1.35rem;line-height:28px;width:30px;height:30px;margin:0 auto 3px;border-radius:50%;background:#1e1b45}
.lg-st.past{opacity:.85}.lg-st.on{opacity:1;font-weight:800}.lg-st.on i{background:#ffe27a;box-shadow:0 0 0 3px rgba(255,226,122,.35);transform:scale(1.15)}
.lg-card{background:rgba(255,255,255,.07);border-radius:16px;padding:13px;margin-top:12px}
.lg-card h3{margin:0 0 8px;font-size:1rem;color:#fff}.lg-card p{margin:0;color:#fff}
.lg-sub{font-size:.86rem;opacity:.85;margin-top:6px!important;line-height:1.4}
.lg-bar{height:12px;border-radius:9px;background:rgba(255,255,255,.12);overflow:hidden;margin-top:8px;position:relative}
.lg-bar i{display:block;height:100%;border-radius:9px;background:linear-gradient(90deg,#7cf0c4,#ffe27a)}
.lg-bar.ghost i{background:rgba(255,255,255,.35)}
.lg-vs{display:grid;grid-template-columns:auto 1fr auto;gap:6px 10px;align-items:center;font-size:.86rem}.lg-vs .lg-bar{margin:0}
.lg-row{display:flex;align-items:center;gap:10px;padding:8px;border-radius:12px}
.lg-row.me{background:rgba(255,226,122,.18);outline:1px solid rgba(255,226,122,.5)}
.lg-rk{width:26px;text-align:center;font-weight:800}.lg-av{font-size:1.25rem;width:28px;text-align:center}.lg-nm{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.lg-pt{font-weight:700}.lg-tt{font-size:.95rem}
.lg-dots{text-align:center;opacity:.5;line-height:.8}
.lg-chips{display:flex;flex-wrap:wrap;gap:6px}.lg-chip{background:rgba(255,255,255,.1);border-radius:999px;padding:5px 10px;font-size:.84rem}.lg-chip.me{background:rgba(255,226,122,.3)}
.lg-up{color:#7cf0c4}
.lg-earn{display:flex;align-items:center;gap:10px;padding:5px 2px;font-size:.9rem}.lg-earn span:nth-child(2){flex:1}.lg-earn b{color:#ffe27a}
.lg-ov .lg-note{font-size:.8rem;opacity:.75;margin:10px 0 0;line-height:1.45;background:none;border:0;padding:0;color:#fff;box-shadow:none}
.lg-msg{text-align:center;padding:40px 10px;opacity:.9}
.lg-res{position:fixed;inset:0;z-index:9100;display:flex;align-items:center;justify-content:center;background:rgba(5,3,20,.8);padding:20px}
.lg-res>div{text-align:center;max-width:330px;width:100%;border-radius:22px;padding:28px 20px 22px;color:#fff;background:linear-gradient(180deg,var(--sky) 0%,var(--mid) 65%,var(--gr) 100%);text-shadow:0 1px 4px rgba(0,0,0,.5);box-shadow:0 10px 40px rgba(0,0,0,.5)}
.lg-res .lg-big{animation:lgPopIn 1s cubic-bezier(.2,1.5,.4,1) both}@keyframes lgPopIn{from{transform:scale(.1) rotate(-30deg);opacity:0}}
.lg-res h2{margin:12px 0 6px;color:#fff}.lg-res p{margin:0 0 16px;color:#fff}
.lg-btn{background:linear-gradient(180deg,#ffe27a,#f5b70f);color:#3a2500;border:0;border-radius:14px;padding:12px 22px;font:inherit;font-weight:800;cursor:pointer;text-shadow:none}
.lg-pop{position:fixed;left:50%;bottom:86px;transform:translate(-50%,20px);opacity:0;z-index:9050;pointer-events:none;background:#1a1440;color:#ffe27a;font-weight:800;padding:8px 14px;border-radius:999px;box-shadow:0 6px 18px rgba(0,0,0,.35);transition:.25s}
.lg-pop.show{opacity:1;transform:translate(-50%,0)}
.lg-own{display:inline-block;font-size:.68rem;background:rgba(0,0,0,.35);border-radius:8px;padding:2px 6px;margin-left:6px;vertical-align:middle;text-shadow:none}
@media (prefers-reduced-motion:reduce){.lg-deco,.lg-big,.lg-res .lg-big{animation:none}}`;
    D.head.appendChild(s);
  }
  /* little scenery per level — clouds by day, sparkles at night */
  function deco(i) {
    const day = ['🦋', '🐝', '🌼', '🐦', '☁️', '☁️'], night = ['✨', '✦', '✨', '·', '✦', '✨'];
    const set = i >= 6 ? night : i === 4 || i === 5 ? ['☁️', '☁️', '🕊️', '☁️', '☁️', '☁️'] : day;
    const pos = [[8, 14], [80, 10], [18, 46], [88, 52], [64, 28], [36, 20]];
    return pos.map(([x, y], k) => `<span class="lg-deco" aria-hidden="true" style="left:${x}%;top:${y}%;animation-delay:${k * .9}s">${set[k]}</span>`).join('');
  }

  /* ---------- banner on the Squad / Group tab ---------- */
  function bannerInner() {
    const c = ls('sv_lg'), t = T(c && c.tier);
    const sub = c ? `${c.rank && c.n ? place(c.rank, c.n) + ' · ' : ''}${c.points || 0} points this week` : 'Study every day and grow from seed to stars';
    return `<span class="lg-e" aria-hidden="true">${t.e}</span><span><b>${NAME} · ${esc(t.n)}${!LIVE ? '<span class="lg-own">🔑 only you</span>' : ''}</b><small>${esc(sub)}</small></span><span class="lg-go" aria-hidden="true">›</span>`;
  }
  /* the banner refreshes itself quietly (at most every 5 minutes); a week's result waits for the next open */
  let bgBusy = false;
  async function refresh() {
    const c = ls('sv_lg'); if (bgBusy || !visible() || (c && Date.now() - (c.at || 0) < 3e5)) return; bgBusy = true;
    try { const r = await rpc('league_board', who()); if (r && r.ok) remember(r, r.result || (c && c.pend) || null); } catch (e) {} finally { bgBusy = false; }
  }
  function remember(r, pend) { ls('sv_lg', { tier: r.tier | 0, points: r.points, today: r.today, rank: r.rank, n: r.n, at: Date.now(), pend: pend || null }); paintBanners(); }
  function banner() { if (!visible()) return ''; css(); setTimeout(refresh, 0); const c = ls('sv_lg'); return `<button class="lg-ban" data-league style="${scene(c && c.tier)}">${bannerInner()}</button>`; }
  function paintBanners() { const c = ls('sv_lg'); D.querySelectorAll('.lg-ban').forEach(b => { b.innerHTML = bannerInner(); b.setAttribute('style', scene(c && c.tier)); }); }
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
    OV = D.createElement('div'); OV.className = 'lg-ov'; OV.setAttribute('role', 'dialog'); OV.setAttribute('aria-label', NAME);
    OV.innerHTML = `<div class="lg-in"><div class="lg-top"><button class="lg-x" id="lgBack">‹ Back</button><h1>${NAME}</h1></div><div id="lgBody"><p class="lg-msg" role="status">Opening…</p></div></div>`;
    D.body.appendChild(OV); D.addEventListener('keydown', onKey);
    OV.querySelector('#lgBack').onclick = () => { try { if (window.sfx) sfx('tap'); } catch (e) {} close(); };
    let r;
    try { r = await rpc('league_board', who()); }
    catch (e) { const b = OV && OV.querySelector('#lgBody'); if (b) b.innerHTML = `<p class="lg-msg">${esc((window.Cloud && Cloud.errText && Cloud.errText(e)) || 'No connection.')}<br><br><button class="lg-btn" id="lgRetry">Try again</button></p>`; const t = OV && OV.querySelector('#lgRetry'); if (t) t.onclick = open; return; }
    if (!OV) return;
    if (!r || !r.ok) { OV.querySelector('#lgBody').innerHTML = `<p class="lg-msg">${r && r.why === 'off' ? 'This is not open yet.' : 'Could not open it. Please try again.'}</p>`; return; }
    const pend = r.result || ((ls('sv_lg') || {}).pend);
    paint(r);
    if (pend) result(pend);
  }
  const person = (x, i) => `<div class="lg-row${x.me ? ' me' : ''}"><span class="lg-rk">${i}</span><span class="lg-av" aria-hidden="true">${esc(x.a)}</span><span class="lg-nm">${esc(x.n)}${x.me ? ' (you)' : ''}</span>${x.t != null ? `<span class="lg-tt" title="${esc(T(x.t).n)}">${T(x.t).e}</span>` : ''}<span class="lg-pt">${x.p}</span></div>`;
  function paint(r) {
    remember(r, null);
    const tier = r.tier | 0, t = T(tier), nx = tier < 7 ? T(tier + 1) : null, pts = r.points || 0, tgt = r.target || 100;
    const top = r.top || [], near = r.near || [], hall = r.hall || [], imp = r.improved || [];
    const meIn = top.some(x => x.me);
    /* 1. climb */
    const done = pts >= tgt;
    const climb = nx
      ? (done ? `<p>✅ <b>Target reached!</b> You will grow into <b>${nx.e} ${esc(nx.n)}</b> on Monday — and you are in this week's Hall of Fame.</p>`
              : `<p>Reach <b>${tgt}</b> points this week to grow into <b>${nx.e} ${esc(nx.n)}</b>.</p><p class="lg-sub">${tgt - pts} to go — about ${Math.ceil((tgt - pts) / 20)} topic${Math.ceil((tgt - pts) / 20) === 1 ? '' : 's'}.</p>`)
      : (done ? `<p>✅ <b>You shine at the very top.</b> You are in this week's Hall of Fame.</p>` : `<p>You are at the top. Reach <b>${tgt}</b> this week to shine in the Hall of Fame.</p>`);
    /* 2. race yourself */
    let self;
    if (r.last == null) self = `<p>This is your first week here. Next week you will race against <b>this week's you</b>.</p>`;
    else {
      const g = r.ghost || 0, diff = pts - g, mx = Math.max(pts, g, r.last || 0, 1);
      self = `<div class="lg-vs"><span>You now</span><div class="lg-bar"><i style="width:${pts / mx * 100}%"></i></div><b>${pts}</b>
          <span>Last week, by today</span><div class="lg-bar ghost"><i style="width:${g / mx * 100}%"></i></div><b>${g}</b></div>
        <p class="lg-sub">${diff > 0 ? `💪 <b>${diff} ahead</b> of last week's you.` : diff === 0 ? 'Level with last week’s you — one more topic puts you ahead.' : `<b>${-diff} behind</b> last week's you — one topic and you are ahead again.`}
        Last week: ${r.last}.${r.best ? ` Best week ever: ${r.best}.` : ''}${pts > (r.best || 0) && r.best ? ' 🏆 <b>New personal best!</b>' : ''}</p>`;
    }
    /* 3. the board */
    let board = top.map((x, i) => person(x, i + 1)).join('');
    if (!meIn && r.rank) board += `<div class="lg-dots" aria-hidden="true">⋮</div>` + person({ n: (prof().name || 'You'), a: prof().avatar || '🙂', p: pts, t: tier, me: true }, r.rank);
    const nearH = near.length ? near.slice().reverse().map(x => `<div class="lg-row"><span class="lg-av" aria-hidden="true">${esc(x.a)}</span><span class="lg-nm">${esc(x.n)}</span><span class="lg-pt">${x.gap} ahead</span></div>`).join('')
      + `<p class="lg-sub">${near[0].gap <= 20 ? `Just one topic and you pass ${esc(near[0].n)}.` : `Keep going — every topic is +20.`}</p>`
      : `<p>🥇 Nobody is ahead of you this week. Stay there!</p>`;
    const pct = Math.min(100, (r.today || 0) / (r.cap || 200) * 100);
    const body = OV.querySelector('#lgBody');
    body.innerHTML = `
      <div class="lg-scene" style="${scene(tier)}">${deco(tier)}<span class="lg-big" aria-hidden="true">${t.e}</span>
        <div class="lg-tn">${esc(t.n)}</div><div class="lg-th">${esc(t.h)}</div>
        <div class="lg-pills"><span class="lg-pill">🏅 ${esc(place(r.rank, r.n))}</span><span class="lg-pill">⭐ ${pts} this week</span><span class="lg-pill" id="lgLeft">⏳ ${left(r.ends)}</span></div></div>
      <div class="lg-path" aria-label="Your journey">${TIERS.map((x, i) => `<div class="lg-st${i === tier ? ' on' : i < tier ? ' past' : ''}"><i aria-hidden="true">${x.e}</i>${esc(x.n)}</div>`).join('')}</div>
      <div class="lg-card"><h3>🌱 Grow this week</h3>${climb}<div class="lg-bar"><i style="width:${Math.min(100, pts / tgt * 100)}%"></i></div></div>
      <div class="lg-card"><h3>🪞 You vs last week's you</h3>${self}</div>
      <div class="lg-card"><h3>🎯 Next to pass</h3>${nearH}</div>
      <div class="lg-card"><h3>🏅 ${esc(lvlName())} this week <small style="opacity:.7;font-weight:400">· ${r.n} student${r.n === 1 ? '' : 's'}</small></h3>${board}</div>
      <div class="lg-card"><h3>🏛️ Hall of Fame</h3><p class="lg-sub" style="margin:0 0 8px!important">Everyone who reaches their weekly target gets in — no limit.</p>
        ${hall.length ? `<div class="lg-chips">${hall.map(x => `<span class="lg-chip${x.me ? ' me' : ''}">${esc(x.a)} ${esc(x.n)} ${T(x.t).e}</span>`).join('')}${r.hall_n > hall.length ? `<span class="lg-chip">+${r.hall_n - hall.length} more</span>` : ''}</div>` : '<p>Nobody yet this week — be the first!</p>'}</div>
      <div class="lg-card"><h3>🚀 Most improved</h3><p class="lg-sub" style="margin:0 0 6px!important">Biggest jump over last week. Anyone can top this.</p>
        ${imp.length ? imp.map((x, i) => `<div class="lg-row${x.me ? ' me' : ''}"><span class="lg-rk">${i + 1}</span><span class="lg-av" aria-hidden="true">${esc(x.a)}</span><span class="lg-nm">${esc(x.n)}${x.me ? ' (you)' : ''}</span><span class="lg-pt lg-up">+${x.g}</span></div>`).join('') : '<p>Study more than last week and your name appears here.</p>'}</div>
      <div class="lg-card"><h3>⭐ How to earn points</h3><p>Today: <b>${r.today || 0}</b> of ${r.cap || 200}</p><div class="lg-bar"><i style="width:${pct}%"></i></div><div style="height:8px"></div>
        ${EARN.map(([e, d, p]) => `<div class="lg-earn"><span aria-hidden="true">${e}</span><span>${esc(d)}</span><b>+${p}</b></div>`).join('')}
        <p class="lg-note">Points come only from studying, not from games, up to 200 a day. A new week starts every Monday (India time). Reach your weekly target and you grow one level. You only go back a level after a whole week with no study.</p></div>`;
    clearInterval(tick); tick = setInterval(() => { const el = OV && OV.querySelector('#lgLeft'); if (!el) return clearInterval(tick); el.textContent = '⏳ ' + left(r.ends); }, 30000);
  }
  function result(res) {
    const [k, v, p] = String(res).split(':'), i = Math.max(0, Math.min(7, +v || 0)), t = T(i);
    const h = k === 'up' ? `You grew into ${t.n}!` : k === 'down' ? `Back to ${t.n}` : `Still ${/^[AEIOU]/.test(t.n) ? 'an' : 'a'} ${t.n}`;
    const msg = k === 'up' ? `${p ? p + ' points last week. ' : ''}A new week has begun — keep growing!`
      : k === 'down' ? 'Every tree starts small. A little study each day and you grow back up.'
      : `${p ? p + ' points last week. ' : ''}Reach this week's target to grow.`;
    const m = D.createElement('div'); m.className = 'lg-res'; m.setAttribute('role', 'alertdialog');
    m.innerHTML = `<div style="${scene(i)}"><span class="lg-big" aria-hidden="true">${t.e}</span><h2>${esc(h)}</h2><p>${esc(msg)}</p><button class="lg-btn">Let's go</button></div>`;
    D.body.appendChild(m); m.querySelector('button').onclick = () => m.remove();
    try { if (window.sfx) sfx(k === 'up' ? 'unlock' : 'open'); } catch (e) {}
  }

  window.League = { visible, live: LIVE, banner, open, ans, fix, topic, unit, TIERS, _lvl: lvl, _name: lvlName };
})();
