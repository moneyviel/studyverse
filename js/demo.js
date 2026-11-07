/* StudyVerse temporary demo login (device-only; no server).
   Open the app with ?demo to see the demo sign-in. Correct ID/password switches this device to a demo
   CA student for 7 days; the real progress is kept aside and restored by "Exit demo" (or on expiry).
   This is NOT real security — real accounts arrive with the backend. Must load before js/app.js. */
(function () {
  const ID = 'demo.ca', PW = 'CA@2027', DAYS = 7;
  const LS = localStorage, now = Date.now();
  const get = k => { try { return LS.getItem(k); } catch (e) { return null; } };
  const set = (k, v) => { try { v == null ? LS.removeItem(k) : LS.setItem(k, v); } catch (e) {} };
  // apply a pending switch before app.js reads sv_state (the app saves on page close, so we switch on the next load)
  const sw = get('sv_demo_swap'); if (sw != null) { set('sv_state', sw === '__none__' ? null : sw); set('sv_demo_swap', null); }
  const until = +(get('sv_demo') || 0);

  function exitDemo() {
    const real = get('sv_state_real');
    set('sv_demo_swap', real == null ? '__none__' : real); set('sv_state_real', null); set('sv_demo', null);
    location.replace(location.pathname);
  }
  /* Demo login switched OFF (owner asked to log every demo out): any device still in demo goes back to its own progress. */
  const OFF = true;
  if (until && (OFF || now > until)) { exitDemo(); return; }  // expired or switched off: restore on reload
  if (OFF) { if (/[?&]demo\b/.test(location.search)) try { history.replaceState(history.state, '', location.pathname); } catch (e) {} return; }

  function enterDemo() {
    if (!until) set('sv_state_real', get('sv_state') || '__none__');
    const exam = new Date(now + 190 * 864e5).toISOString().slice(0, 10);
    set('sv_demo_swap', JSON.stringify({ profile: { name: 'Demo Student', avatar: '🎓', course: 'ca', grade: 12, board: 'cbse' }, ca: { level: 'foundation', exam } }));
    set('sv_demo', String(now + DAYS * 864e5));
    location.replace(location.pathname);
  }

  const css = `.dm-gate{position:fixed;inset:0;z-index:9999;background:#15161C;display:flex;align-items:center;justify-content:center;padding:20px;font-family:Inter,system-ui,sans-serif}
.dm-card{background:#FFFDF8;border-radius:16px;max-width:360px;width:100%;padding:24px;box-shadow:0 10px 40px rgba(0,0,0,.5)}
.dm-card h1{margin:0 0 4px;font-size:22px;color:#15161C}.dm-card p{margin:0 0 14px;color:#4a4d57;font-size:14px;line-height:1.45}
.dm-card label{display:block;font-weight:600;font-size:13px;color:#15161C;margin:10px 0 4px}
.dm-card input{width:100%;box-sizing:border-box;padding:12px;border:1.5px solid #c9c2b2;border-radius:10px;font-size:16px}
.dm-card button{width:100%;margin-top:16px;padding:13px;border:0;border-radius:10px;background:#15161C;color:#C9A76A;font-weight:700;font-size:16px;cursor:pointer}
.dm-card .dm-x{background:none;color:#8A6A2E;margin-top:8px;font-weight:600}.dm-err{color:#B71C2C;font-size:13px;min-height:18px;margin-top:8px}
.dm-bar{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(84px + env(safe-area-inset-bottom));z-index:9998;background:#C9A76A;opacity:.95;color:#15161C;border-radius:999px;padding:4px 6px 4px 12px;font:600 12px Inter,system-ui,sans-serif;display:flex;gap:8px;align-items:center;box-shadow:0 2px 8px rgba(0,0,0,.3)}
.dm-bar button{border:0;background:#15161C;color:#fff;border-radius:999px;padding:4px 10px;font:600 12px Inter,system-ui,sans-serif;cursor:pointer}`;

  function gate() {
    const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    const g = document.createElement('div'); g.className = 'dm-gate'; g.setAttribute('role', 'dialog'); g.setAttribute('aria-modal', 'true'); g.setAttribute('aria-labelledby', 'dmT');
    g.innerHTML = `<form class="dm-card" id="dmF" autocomplete="off"><h1 id="dmT">StudyVerse demo sign-in</h1>
      <p>Temporary demo of the CA course. It lasts ${DAYS} days on this device, and "Exit demo" brings back your own progress.</p>
      <label for="dmId">Login ID</label><input id="dmId" autocapitalize="none" spellcheck="false">
      <label for="dmPw">Password</label><input id="dmPw" type="password">
      <div class="dm-err" id="dmE" role="alert"></div><button type="submit">Sign in</button><button type="button" class="dm-x" id="dmX">Cancel</button></form>`;
    document.body.appendChild(g);
    document.getElementById('dmX').onclick = () => location.replace(location.pathname);
    document.getElementById('dmF').onsubmit = e => {
      e.preventDefault();
      const id = document.getElementById('dmId').value.trim().toLowerCase(), pw = document.getElementById('dmPw').value;
      if (id === ID && pw === PW) enterDemo(); else document.getElementById('dmE').textContent = 'Wrong login ID or password.';
    };
  }
  function bar() {
    const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    const b = document.createElement('div'); b.className = 'dm-bar';
    const d = Math.max(1, Math.ceil((until - now) / 864e5));
    b.innerHTML = `<span>Demo account · ${d} day${d > 1 ? 's' : ''} left</span><button type="button">Exit demo</button>`;
    b.querySelector('button').onclick = exitDemo; document.body.appendChild(b);
  }
  const wantGate = /[?&]demo\b/.test(location.search);
  const run = () => { if (wantGate) gate(); else if (until) bar(); };
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', run) : run();
})();
