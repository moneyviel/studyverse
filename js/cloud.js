/* Knowtopia accounts + progress saving (Supabase project "moneyviel-apps", schema "studyverse").
   No library: talks to Supabase Auth (/auth/v1) and the Data API (/rest/v1) with fetch.
   - Loads BEFORE app.js so it can catch login links (#access_token=… from confirm / reset emails)
     before the app touches the URL. It only uses ST / save / toast at run time.
   - The app still works fully without an account (progress stays on the phone).
   - Signed in: the saved progress (sv_state + question history) is copied to the account every
     30 s when something changed, when the app goes to the background, and when the phone comes online.
   - First sign-in on a phone: if only one side has progress it is used; if both have progress
     the student chooses which to keep. Sign-out removes the progress from this phone (it stays in the account).
   - Course access (studyverse.course_access) is read and kept in sv_access; only the owner can grant it.
   - Disabled while the temporary demo login (js/demo.js) is active. */
(function () {
  const API = 'https://fyvplhtpsxpxvvsilzqq.supabase.co', KEY = 'sb_publishable_w2TfDNignGxAwFAfAlrdnA_RZSQV8gT', SCHEMA = 'studyverse';
  const SITE = location.origin + location.pathname;
  const D = document, LS = localStorage;
  const get = k => { try { return LS.getItem(k); } catch (e) { return null; } };
  const set = (k, v) => { try { v == null ? LS.removeItem(k) : LS.setItem(k, v); } catch (e) {} };
  const jget = (k, d) => { try { const v = JSON.parse(get(k)); return v == null ? d : v; } catch (e) { return d; } };
  const demo = () => !!get('sv_demo');
  /* Knowtopia can only be used with an account: a full-screen sign-in gate covers the app until signed in. */
  const on = () => true;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const say = m => { try { toast(m); } catch (e) {} };
  const COURSES = { 'school-all': 'All school grades', 'ca-foundation': 'CA Foundation', 'ca-inter': 'CA Intermediate', 'ca-final': 'CA Final', school: 'School (Class 1–12)' };
  const EXTRA = ['sv_cagen'];                       // other progress kept with sv_state

  let S = jget('sv_auth', null);                    // session { at, rt, exp, user:{id,email} }
  // owner mode only comes from an owner (admin) account now — the old passcode owner mode is switched off
  if (get('sv_owner') === '1' && !(jget('sv_cloud', {}).adm && S)) set('sv_owner', null);
  let status = 'off', lastErr = '', recovery = false, busy = false, linked = false, linkMsg = '';
  const one = r => Array.isArray(r) ? r[0] : r;

  /* ---------- account role: 'student' or 'parent' (studyverse rpc set_my_role / my_role) ----------
     Chosen on the sign-up form and set once on the server after the first sign-in. Cached per user in
     sv_role = { uid, role: 'parent'|'student'|'none', sure } ('none' = no role on the server: treated as a student).
     Parent accounts see only Parent Home (js/parent.js): no onboarding, courses, trial, plans or paywall. */
  const ROLE_K = 'sv_role', PEND_K = 'sv_role_pending';
  let userMeta = null;                              // user_metadata from Auth (holds sv_role chosen at sign-up, any device)
  function role() { const c = jget(ROLE_K, null); return S && S.user && c && c.uid === S.user.id ? c.role : null; }
  const setRole = (uid, r, sure) => set(ROLE_K, JSON.stringify({ uid, role: r, sure: !!sure }));
  const isParent = () => !!S && !demo() && role() === 'parent';
  const parentCss = () => { if (D.getElementById('svParentCss')) return; const c = D.createElement('style'); c.id = 'svParentCss';
    c.textContent = 'html.sv-parent .app>:not(.toast){display:none!important}html.sv-parent .toast{z-index:995}html.sv-parent .askfab,html.sv-parent .sv-talk,html.sv-parent .ca-hlbtn{display:none!important}'; (D.head || D.documentElement).appendChild(c); };
  if (isParent()) { parentCss(); D.documentElement.classList.add('sv-parent'); }   // before the first paint: no flash of the student app

  /* ---------- 1. login links from emails: #access_token=…&type=signup|recovery ---------- */
  (function catchLink() {
    const h = location.hash || '';
    if (!/access_token=|error_description=/.test(h)) return;
    const p = new URLSearchParams(h.slice(1));
    if (p.get('error_description')) linkMsg = p.get('error_description').replace(/\+/g, ' ');
    else if (p.get('access_token')) {
      S = { at: p.get('access_token'), rt: p.get('refresh_token'), exp: Date.now() / 1000 + (+p.get('expires_in') || 3600), user: null };
      set('sv_auth', JSON.stringify(S));
      recovery = p.get('type') === 'recovery';
      if (recovery) try { sessionStorage.setItem('sv_recovery', '1'); } catch (e) {}   // survives the reload that adopting cloud progress may do
      linkMsg = recovery ? '' : 'Email confirmed — you are signed in ✓';
    }
    try { history.replaceState(history.state, '', location.pathname + location.search); } catch (e) {}
  })();

  /* ---------- 1b. parent's email invite: ?invite=1&email=<child email> → sign-up form prefilled, role Student ---------- */
  let invite = null;
  (function catchInvite() {
    try {
      const u = new URL(location.href); if (!u.searchParams.get('invite')) return;
      invite = { email: (u.searchParams.get('email') || '').trim().toLowerCase() };
      u.searchParams.delete('invite'); u.searchParams.delete('email');
      history.replaceState(history.state, '', u.pathname + u.search + u.hash);
    } catch (e) {}
  })();

  /* ---------- 2. talking to Supabase ---------- */
  async function call(path, opt = {}, auth = true) {
    const h = Object.assign({ apikey: KEY, 'Content-Type': 'application/json' }, opt.headers || {});
    if (auth) { await fresh(); if (!S) throw Object.assign(new Error('Please sign in again.'), { status: 401 }); h.Authorization = 'Bearer ' + S.at; }
    let r; try { r = await fetch(API + path, { method: opt.method || 'GET', headers: h, body: opt.body ? JSON.stringify(opt.body) : undefined, keepalive: !!opt.keepalive, cache: 'no-store' }); } catch (e) { throw Object.assign(new Error('No internet connection.'), { status: 0 }); }
    const t = await r.text(); let j = null;
    if (t) { try { j = JSON.parse(t); } catch (e) { throw Object.assign(new Error('No connection to the server.'), { status: 0 }); } }
    if (!r.ok) { const m = (j && (j.msg || j.error_description || j.message || j.error)) || ('Error ' + r.status); throw Object.assign(new Error(m), { status: r.status, code: j && (j.error_code || j.code) }); }
    return j;
  }
  const rest = (path, opt = {}) => call('/rest/v1/' + path, Object.assign({}, opt, { headers: Object.assign({ 'Accept-Profile': SCHEMA, 'Content-Profile': SCHEMA }, opt.headers || {}) }));
  function keep(j) {
    S = { at: j.access_token, rt: j.refresh_token, exp: j.expires_at || (Date.now() / 1000 + (j.expires_in || 3600)), user: j.user ? { id: j.user.id, email: j.user.email } : (S && S.user) };
    if (j.user && j.user.user_metadata) userMeta = j.user.user_metadata;
    set('sv_auth', JSON.stringify(S));
    gate();
  }
  let refreshing = null;
  async function fresh() {
    if (!S || S.exp - 60 > Date.now() / 1000) return;
    if (!refreshing) refreshing = call('/auth/v1/token?grant_type=refresh_token', { method: 'POST', body: { refresh_token: S.rt } }, false)
      .then(keep).catch(e => { if (e.status >= 400 && e.status < 500) drop(); throw e; }).finally(() => { refreshing = null; });
    return refreshing;
  }
  function drop() { S = null; set('sv_auth', null); linked = false; status = 'off'; paint(); gate(); }   // session ended: progress stays on the phone

  /* ---------- 3. progress ---------- */
  function payload() {
    const x = {}; EXTRA.forEach(k => { const v = get(k); if (v != null) x[k] = v; });
    let st; try { st = ST; } catch (e) { st = jget('sv_state', {}); }
    return { v: 1, st, x };
  }
  const hash = s => { let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; return h + ':' + s.length; };
  const meta = () => jget('sv_cloud', {});
  const setMeta = m => set('sv_cloud', JSON.stringify(m));
  const hasProgress = p => !!(p && p.st && p.st.profile);

  async function push(force, hidden) {
    if (!S || !S.user || !linked || demo() || busy) return;
    const m = meta(); if (m.uid !== S.user.id) return;
    const p = payload(), s = JSON.stringify(p), h = hash(s);
    if (!force && h === m.h) { if (status !== 'ok') { status = 'ok'; paint(); } return; }
    busy = true; status = 'saving'; paint();
    try {
      await rest('progress?on_conflict=user_id', { method: 'POST', keepalive: hidden && s.length < 60000, headers: { Prefer: 'resolution=merge-duplicates,return=minimal' }, body: { user_id: S.user.id, state: p } });
      setMeta(Object.assign(meta(), { uid: S.user.id, h, at: Date.now() })); status = 'ok';
    } catch (e) { status = navigator.onLine === false || e.status === 0 ? 'offline' : 'error'; lastErr = e.message; }
    finally { busy = false; }
    paint();
  }

  function reloadWith(stJSON) {                       // demo.js applies sv_demo_swap before app.js reads sv_state
    set('sv_demo_swap', stJSON == null ? '__none__' : stJSON);
    try { Object.keys(ST).forEach(k => delete ST[k]); Object.assign(ST, stJSON ? JSON.parse(stJSON) : { profile: null, xp: 0, streak: { n: 0, last: '' }, topics: {}, mistakes: {}, qstats: {} }); } catch (e) {}
    location.replace(SITE);
  }
  function adopt(cloud, uid) {
    EXTRA.forEach(k => set(k, (cloud.x || {})[k] == null ? null : cloud.x[k]));
    setMeta({ uid, h: '' });
    reloadWith(JSON.stringify(cloud.st));
  }
  function wipeLocal() { EXTRA.concat(['sv_photos']).forEach(k => set(k, null)); reloadWith(null); }

  async function link() {                            // first sign-in of this account on this phone
    const uid = S.user.id, m = meta();
    if (m.uid === uid) { linked = true; return; }
    const rows = await rest('progress?select=state,updated_at&user_id=eq.' + encodeURIComponent(uid));
    if (!Array.isArray(rows)) throw new Error('No connection to the server.');
    const cloud = rows[0] && rows[0].state, local = payload();
    const foreign = !!(m.uid && m.uid !== uid);      // phone progress belongs to another account
    const L = hasProgress(local) && !foreign, C = hasProgress(cloud);
    if (C && !L) return adopt(cloud, uid);
    if (!C && foreign) { setMeta({ uid }); return wipeLocal(); }
    if (!C) { setMeta({ uid }); linked = true; return push(true); }
    if (JSON.stringify(cloud) === JSON.stringify(local)) { setMeta({ uid, h: hash(JSON.stringify(local)) }); linked = true; return; }
    return choose(local, cloud, rows[0].updated_at, uid);
  }

  async function arrive() {
    if (!S) return;
    if (demo()) { status = 'demo'; paint(); return; }
    status = 'idle'; paint();
    try {
      if (!S.user) { const u = await call('/auth/v1/user'); S.user = { id: u.id, email: u.email }; userMeta = u.user_metadata || null; set('sv_auth', JSON.stringify(S)); }
      const wasParent = isParent(), r = await resolveRole();
      if (r === 'parent') { enterParent(); owner(); status = 'ok'; paint(); return; }   // parents: no progress sync, trial or courses
      if (wasParent && (r === 'student' || r === 'none')) { location.replace(SITE); return; }
      repaintMe();
      await claim();
      await link();
      access(); owner(); prof();
      if (linked) { status = status === 'saving' ? status : 'ok'; paint(); }
    } catch (e) { status = navigator.onLine === false || e.status === 0 ? 'offline' : 'error'; lastErr = e.message; paint(); }
  }

  /* role: cached once known for sure; otherwise ask the server, and set the role chosen at sign-up (once) */
  async function resolveRole() {
    const uid = S.user.id, email = (S.user.email || '').toLowerCase(), c = jget(ROLE_K, null), mine = c && c.uid === uid ? c : null;
    if (mine && mine.sure && (mine.role === 'parent' || mine.role === 'student')) { set(PEND_K, null); return mine.role; }
    const pj = jget(PEND_K, null);
    let pend = pj && pj.email === email ? pj.role : (userMeta && userMeta.sv_role) || null;
    if (pend !== 'parent' && pend !== 'student') pend = null;
    let r;
    try {
      r = one(await rest('rpc/my_role', { method: 'POST', body: {} }));
      if (r && typeof r === 'object') r = r.my_role || r.role || null;
    } catch (e) { if (pend) { setRole(uid, pend, false); return pend; } return mine ? mine.role : null; }
    if (r !== 'parent' && r !== 'student') r = null;
    if (!r && pend) {
      try { const y = one(await rest('rpc/set_my_role', { method: 'POST', body: { p_role: pend } })); r = y && (y.role === 'parent' || y.role === 'student') ? y.role : (y && y.ok ? pend : null); }
      catch (e) { setRole(uid, pend, false); return pend; }
    }
    set(PEND_K, null); setRole(uid, r || 'none', true);
    return r || 'none';
  }
  function enterParent() {
    parentCss(); D.documentElement.classList.add('sv-parent');
    try { if (SND.playing) { SND.playing = false; clearInterval(SND.timer); } } catch (e) {}   // music may have started on the sign-up tap
    let n = 0; const go = () => { if (window.Parent && Parent.home) Parent.home(); else if (n++ < 50) setTimeout(go, 100); }; go();
  }
  /* a parent's email invite for this student's email: link them (once per sign-in; cheap) */
  let claimedFor = null;
  async function claim() {
    const uid = S.user.id; if (claimedFor === uid) return; claimedFor = uid;
    try {
      const r = one(await rest('rpc/claim_invites', { method: 'POST', body: {} }));
      if (r && r.linked > 0) { setTimeout(() => say('You\u2019re now linked to your parent ✓'), 2100); try { if (window.Parent && Parent._pull) setTimeout(Parent._pull, 300); } catch (e) {} }
    } catch (e) {}
  }

  /* free-forever lock + discount code saved on the student's profile */
  async function prof() {
    try {
      const r = await rest('profiles?select=locked_course,discount_code&user_id=eq.' + encodeURIComponent((S && S.user && S.user.id) || '')); if (!Array.isArray(r)) return;
      const p = r[0] || {}; set('sv_lock', p.locked_course || null); set('sv_disc', p.discount_code || null); enforceLock(); codeCard(true);
    } catch (e) {}
  }
  const myCourse = () => { try { const p = ST.profile; if (!p) return null; return p.course === 'ca' ? 'ca-foundation' : 'school-g' + p.grade; } catch (e) { return null; } };
  const courseName = c => c && c.startsWith('school-g') ? 'Grade ' + c.slice(8) : (COURSES[c] || c);
  /* What this student may open. During the 24-hour trial (and for the owner) everything; after it, ONLY what they have:
     paid / code courses ('school-g<N>', 'ca-foundation') and a free-forever lock; with nothing paid, the free plan stays on
     the class or course they chose at the start. Returns null when there is no restriction. */
  function allowed() {
    if (!S || isParent() || meta().adm) return null;
    try { if (localStorage.getItem('sv_owner') === '1') return null; } catch (e) {}
    if (get('sv_access') == null) return null;                     // not loaded yet: decide after the first check
    const live = courses(), set_ = new Set();
    if (live.some(a => /trial/.test(a.note || ''))) return null;   // trial: everything open
    if (live.some(a => a.course === 'school-all')) return null;     // older all-classes grant
    live.forEach(a => { if (/^school-g\d+$/.test(a.course) || /^ca-/.test(a.course)) set_.add(a.course); });
    const L = get('sv_lock'); if (L) set_.add(L);
    if (!set_.size) { const m = myCourse(); if (m) set_.add(m); }   // free plan: stay where they are
    return set_;
  }
  function enforceLock() {                           // move the student onto something they are allowed to open
    const A = allowed(); if (!A) return;
    let p; try { p = ST.profile; } catch (e) { return; } if (!p) return;
    const cur = myCourse(); if (cur && A.has(cur)) return;
    const list = [...A].sort((a, b) => (a === get('sv_lock') ? -1 : 0) - (b === get('sv_lock') ? -1 : 0));
    const L = list.find(c => c === 'ca-foundation') && p.course === 'ca' ? 'ca-foundation' : list[0];
    if (!L) return;
    if (/^ca-/.test(L)) { p.course = 'ca'; ST.ca = Object.assign({}, ST.ca || {}, { level: ST.ca && ST.ca.level || 'foundation' }); save(); location.replace(SITE); }
    else { const g = +L.slice(8); p.course = null; p.grade = g; if (g < 11) { p.stream = null; p.subjects = null; } save(); location.replace(SITE); }
  }
  async function access() {
    if (isParent()) return;                          // parents have no courses and no trial
    try {
      // a new account gets its 24-hour trial of all school grades once (the server decides; repeated calls change nothing)
      if (!get('sv_trial')) { try { await rest('rpc/start_trial', { method: 'POST', body: {} }); set('sv_trial', '1'); } catch (e) {} }
      const r = await rest('course_access?select=course,valid_until,note&user_id=eq.' + encodeURIComponent((S && S.user && S.user.id) || '')); if (Array.isArray(r)) { set('sv_access', JSON.stringify(r)); paint(); enforceLock(); try { window.dispatchEvent(new Event('sv-access')); } catch (e) {} }
    } catch (e) {}
  }
  async function owner() {                         // studyverse.admins: an owner account turns owner mode on (once; "turn off" is respected)
    try {
      const r = await rest('admins?select=user_id&user_id=eq.' + encodeURIComponent((S && S.user && S.user.id) || '')); if (!Array.isArray(r)) return;
      const adm = r.length > 0, m = meta();
      if (adm && !m.adm) { set('sv_owner', '1'); say('Owner account — owner mode is on'); }
      if (!adm) set('sv_owner', null);
      if (!!m.adm !== adm) { setMeta(Object.assign(meta(), { adm })); repaintMe(); try { const a = D.querySelector('.screen.active'), typing = D.activeElement && /INPUT|TEXTAREA/.test(D.activeElement.tagName); if (a && a.id === 's-me' && !typing) meScreen(); } catch (e) {} }
    } catch (e) {}
  }
  const locked = () => !!(S && get('sv_lock'));
  const courses = () => jget('sv_access', []).filter(a => !a.valid_until || new Date(a.valid_until) > new Date());

  /* ---------- 4. account actions ---------- */
  const signUp = async (email, pw, r) => {
    let cm = {}; try { if (window.PlayReady && PlayReady.signupMeta) cm = PlayReady.signupMeta(r) || {}; } catch (e) {}   // { sv_consent: { v, g } }
    const j = await call('/auth/v1/signup?redirect_to=' + encodeURIComponent(SITE), { method: 'POST', body: r ? { email, password: pw, data: Object.assign({ sv_role: r }, cm) } : { email, password: pw } }, false);
    if (j && j.access_token) { keep(j); await arrive(); return 'in'; }
    return 'confirm';
  };
  const signIn = async (email, pw) => { keep(await call('/auth/v1/token?grant_type=password', { method: 'POST', body: { email, password: pw } }, false)); await arrive(); };
  const forgot = email => call('/auth/v1/recover?redirect_to=' + encodeURIComponent(SITE), { method: 'POST', body: { email } }, false);
  const newPassword = pw => call('/auth/v1/user', { method: 'PUT', body: { password: pw } });
  async function signOut() {
    try { await push(true); } catch (e) {}
    try { await call('/auth/v1/logout', { method: 'POST' }); } catch (e) {}
    S = null; ['sv_auth', 'sv_cloud', 'sv_access', 'sv_owner', 'sv_lock', 'sv_disc', 'sv_trial', ROLE_K, PEND_K, 'sv_pctl'].forEach(k => set(k, null));
    wipeLocal();
  }

  /* ---------- 5. screens ---------- */
  const css = `#svCloud .cl-st{font-size:13px;margin:6px 0 10px;color:#4a4d57}#svCloud .cl-st.ok{color:#1d7a46}#svCloud .cl-st.bad{color:#B71C2C}
.cl-row{display:flex;gap:8px;flex-wrap:wrap}.cl-row .btn{flex:1;min-width:130px}
.cl-sheet{z-index:990}.cl-sheet .sheet-in{color:#15161C;background:#FFFDF8;max-height:92vh;overflow:auto}
.cl-sheet h3{margin:0 0 6px}.cl-sheet p{margin:0 0 10px;font-size:14px;line-height:1.45;color:#4a4d57}
.cl-sheet label{display:block;font-weight:600;font-size:13px;margin:10px 0 4px}
.cl-in{width:100%;box-sizing:border-box;padding:12px;border:1.5px solid #c9c2b2;border-radius:10px;font-size:16px;background:#fff;color:#15161C}
.cl-err{color:#B71C2C;font-size:13px;min-height:18px;margin:8px 0 4px}.cl-ok{color:#1d7a46;font-size:14px;margin:8px 0}
.cl-link{background:none;border:0;color:#8A6A2E;font-weight:600;font-size:14px;padding:8px 0;cursor:pointer;text-decoration:underline}
.cl-small{font-size:12px!important;color:#6b6e78!important}.cl-show{display:flex;align-items:center;gap:6px;font-weight:500!important}
.cl-pick{display:block;width:100%;text-align:left;margin:8px 0;padding:12px 14px;border:1.5px solid #c9c2b2;border-radius:12px;background:#fff;color:#15161C;font-size:15px;cursor:pointer}
.cl-pick b{display:block}.cl-pick small{color:#4a4d57}
.cl-role{border:0;margin:10px 0 2px;padding:0;min-width:0}.cl-role legend{font-weight:700;font-size:14px;margin:0 0 6px;padding:0;color:#15161C}
.cl-roles{display:flex;gap:10px}.cl-rc{position:relative;flex:1;display:flex!important;flex-direction:column;align-items:center;gap:2px;margin:0!important;min-height:92px;padding:10px 8px;border:2px solid #c9c2b2;border-radius:14px;background:#fff;cursor:pointer;text-align:center;font-weight:500!important}
.cl-rc input{position:absolute;opacity:0;inset:0;margin:0;cursor:pointer}.cl-rc span{font-size:30px;line-height:1.1}.cl-rc b{font-size:16px;color:#15161C}.cl-rc small{font-size:12px;color:#4a4d57;line-height:1.25}
.cl-rc.on{border-color:#8A6A2E;background:#F4EAD8;box-shadow:0 0 0 2px #C9A76A}.cl-rc:focus-within{outline:3px solid #8A6A2E;outline-offset:2px}
.cl-inv{background:#F4EAD8;border-radius:12px;padding:10px 12px;font-size:14px!important;color:#15161C!important}`;
  function style() { if (D.getElementById('svCloudCss')) return; const s = D.createElement('style'); s.id = 'svCloudCss'; s.textContent = css; D.head.appendChild(s); }

  function stLine() {
    const m = meta(), t = m.at ? new Date(m.at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
    return ({ ok: ['ok', '✓ Progress saved to your account' + (t ? ' · ' + t : '')], saving: ['', 'Saving…'], idle: ['', 'Connecting…'],
      offline: ['bad', 'You are offline — your progress will be saved when you are back online.'],
      error: ['bad', 'Could not save just now (' + esc(lastErr) + '). It will try again.'] })[status] || ['', ''];
  }
  function cardHTML() {
    if (demo()) return '';
    if (!S) return `<h3>☁️ Save your progress</h3><p class="sub">Create a free account so your progress is safe and you can continue on any phone.</p>
      <div class="cl-row"><button class="btn" type="button" data-cl="up">Create account</button><button class="btn ghost" type="button" data-cl="in">Sign in</button></div>`;
    const [cls, txt] = stLine(), cs = courses();
    return `<h3>☁️ ${meta().adm ? 'Owner account 🔑' : 'Your account'}</h3><p class="sub">${esc((S.user && S.user.email) || '')}</p><p class="cl-st ${cls}" role="status">${txt}</p>
      <p class="sub">Your courses: ${cs.length ? cs.map(c => esc(courseName(c.course)) + (c.valid_until ? ' (till ' + new Date(c.valid_until).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) + ')' : '')).join(', ') : 'free courses'}</p>
      <div class="cl-row">${meta().adm ? '' : '<button class="btn" type="button" data-cl="plans">Plans &amp; subscribe</button>'}${status === 'error' || status === 'offline' ? '<button class="btn ghost" type="button" data-cl="retry">Try again</button>' : ''}<button class="btn ghost" type="button" data-cl="out">Sign out</button></div>${meta().adm ? '' : '<button class="pr-del" type="button" data-cl="del">Delete my account</button>'}`;
  }
  function wire(root) {
    root.querySelectorAll('[data-cl]').forEach(b => b.onclick = () => {
      const a = b.dataset.cl;
      if (a === 'up' || a === 'in') form(a);
      else if (a === 'plans') { if (window.Plans) Plans.open(); }
      else if (a === 'retry') { arrive().then(() => push(true)); }
      else if (a === 'del') { if (window.PlayReady) PlayReady.deleteAccount(); }   // js/playready.js: two-step delete
      else if (a === 'out') {
        if (b.dataset.sure) { b.disabled = true; b.textContent = 'Signing out…'; signOut(); }
        else { b.dataset.sure = 1; b.textContent = 'Tap again to sign out (progress stays in your account)'; }
      }
    });
  }
  function paint() {
    const c = D.getElementById('svCloud'); if (!c) return;
    const h = cardHTML(); if (!h) { c.remove(); return; }
    if (c.dataset.h === h) return; c.dataset.h = h; c.innerHTML = h; wire(c);
  }
  // the student's profile screen: school "Me", or the CA Profile (rendered inside #s-ca; it has the name box #caNm)
  const meHost = () => { const ca = D.getElementById('s-ca'); return (ca && ca.querySelector('#caNm')) ? ca : D.getElementById('s-me'); };
  function inject() {                                // account card on the Me / profile screen, sign-in link on onboarding
    const me = meHost();
    if (!on() || isParent()) return;
    if (me) ['svCloud', 'svCode', 'svCodes'].forEach(id => { const x = D.getElementById(id); if (x && !me.contains(x)) x.remove(); });   // cards follow the visible profile (school Me / CA Profile)
    if (me && me.firstElementChild && !D.getElementById('svCloud') && !demo()) {
      style(); const c = D.createElement('div'); c.className = 'card'; c.id = 'svCloud';
      const first = me.querySelector(':scope > .card'); first ? first.after(c) : me.prepend(c); paint();
    }
    if (me && S && !demo()) { if (!meta().adm) codeCard(); ownerCodes(); }
    const A = me ? allowed() : null;
    if (me && A) {                                    // after the trial a student only sees the class / course they have
      const grades = [...A].filter(c => /^school-g/.test(c)).map(c => +c.slice(8));
      const g = me.querySelector('.grid5');
      if (g && grades.length > 1) g.querySelectorAll('[data-g]').forEach(b => { if (!grades.includes(+b.dataset.g)) b.remove(); });
      else if (g && g.closest('.card')) g.closest('.card').remove();
      if (locked()) { const st = D.getElementById('meStream'); if (st && st.closest('.card')) st.closest('.card').remove(); }
    }
    const ob = D.getElementById('s-onboard');
    if (ob && !S && !demo() && ob.querySelector('.choice[data-b]') && !D.getElementById('svCloudOb')) {
      style(); const c = D.createElement('div'); c.className = 'card'; c.id = 'svCloudOb';
      c.innerHTML = `<h3>Already have an account?</h3><p class="sub">Sign in to bring back your saved progress.</p><button class="btn ghost" type="button" data-cl="in">Sign in</button>`;
      (ob.querySelector('.ob') || ob).appendChild(c); wire(c);
    }
  }

  /* ---------- codes: students redeem, owner creates ---------- */
  function codeCard(refresh) {
    const me = meHost(); if (!me || !S) return;
    let c = D.getElementById('svCode');
    if (c && !refresh) return;
    if (!c) { c = D.createElement('div'); c.className = 'card'; c.id = 'svCode'; const a = D.getElementById('svCloud'); a ? a.after(c) : me.appendChild(c); }
    const L = get('sv_lock'), disc = get('sv_disc');
    if (L) { c.innerHTML = `<h3>🎟️ Free access</h3><p class="sub">Your account has free access to <b>${esc(courseName(L))}</b> forever.</p>`; return; }
    c.innerHTML = `<h3>🎟️ Have a code?</h3><p class="sub">${window.SV_PLAY ? 'Enter a free-access code from your school or teacher.' : `Enter a free-access or discount code.${disc ? ` Discount code <b>${esc(disc)}</b> is saved for your payment.` : ''}`}</p>
      <form id="clCodeF" class="cl-row" novalidate><input class="cl-in" id="clCode" placeholder="e.g. FREE-AB12CD" autocapitalize="characters" spellcheck="false" maxlength="24" style="flex:2;min-width:150px;margin:0"><button class="btn" type="submit" id="clCodeGo" style="flex:1">Apply</button></form>
      <div class="cl-err" id="clCodeE" role="alert"></div><p class="cl-small" id="clCodeN">A free code gives free access only to ${esc(courseName(myCourse()) || 'your course')} — you will not be able to change it later.</p>`;
    c.querySelector('#clCodeF').onsubmit = async e => {
      e.preventDefault();
      const er = c.querySelector('#clCodeE'), go = c.querySelector('#clCodeGo'), code = c.querySelector('#clCode').value.trim().toUpperCase();
      er.textContent = ''; if (!/^[A-Z0-9-]{4,24}$/.test(code)) { er.textContent = 'Please check the code.'; return; }
      go.disabled = true;
      try {
        const r = await rest('rpc/redeem_code', { method: 'POST', body: { p_code: code, p_course: myCourse() } });
        if (!r || !r.ok) { er.textContent = (r && r.msg) || 'This code is not valid.'; return; }
        if (r.kind === 'free') { set('sv_lock', r.course); access(); say('Free access unlocked ✓'); codeCard(true); enforceLock(); try { (ST.profile && ST.profile.course === 'ca' && window.Ca) ? Ca.profile() : meScreen(); } catch (x) {} }
        else { set('sv_disc', code); say(window.SV_PLAY ? 'Code saved ✓' : r.percent + '% discount saved ✓ It will be used when you pay'); codeCard(true); }   // Play build: no payment talk
      } catch (err) { er.textContent = errText(err); }
      finally { go.disabled = false; }
    };
  }

  const ALPH = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  const genCode = () => { const a = new Uint32Array(6); crypto.getRandomValues(a); return 'FREE-' + [...a].map(n => ALPH[n % ALPH.length]).join(''); };
  function ownerCodes() {
    const me = meHost(); if (!me || !meta().adm || D.getElementById('svCodes')) return;
    const c = D.createElement('div'); c.className = 'card'; c.id = 'svCodes';
    const o = D.getElementById('caOwner'); o ? o.after(c) : me.appendChild(c);
    c.innerHTML = `<h3>🎟️ Codes (owner)</h3>
      <h4 style="margin:10px 0 4px">Free forever — one student</h4><p class="sub">The student enters it in Me. They get free access only to the grade or course they chose at the start, and cannot switch.</p>
      <label class="cl-small" for="ocNote">Student name (for your record)</label><input class="cl-in" id="ocNote" maxlength="120">
      <button class="btn" type="button" id="ocFree">Create free code</button><div id="ocFreeOut"></div>
      <h4 style="margin:16px 0 4px">Discount — anyone can use</h4>
      <label class="cl-small" for="ocDC">Code</label><input class="cl-in" id="ocDC" placeholder="e.g. DIWALI20" autocapitalize="characters" maxlength="24">
      <div class="cl-row"><div style="flex:1"><label class="cl-small" for="ocDP">% off</label><input class="cl-in" id="ocDP" type="number" min="1" max="100" inputmode="numeric"></div>
      <div style="flex:1"><label class="cl-small" for="ocDU">Max uses (optional)</label><input class="cl-in" id="ocDU" type="number" min="1" inputmode="numeric"></div></div>
      <label class="cl-small" for="ocDV">Valid till</label><input class="cl-in" id="ocDV" type="date">
      <button class="btn" type="button" id="ocDisc">Create discount code</button>
      <div class="cl-err" id="ocE" role="alert"></div>
      <h4 style="margin:16px 0 4px">Your codes</h4><div id="ocList" class="cl-small">Loading…</div>
      <button class="cl-link" type="button" id="ocWho">Who used codes?</button><div id="ocWhoOut" class="cl-small"></div>`;
    const er = c.querySelector('#ocE'), fail = e => { er.textContent = errText(e); };
    const ins = row => rest('codes', { method: 'POST', headers: { Prefer: 'return=minimal' }, body: row });
    c.querySelector('#ocFree').onclick = async () => {
      er.textContent = ''; let code = genCode();
      try {
        try { await ins({ code, kind: 'free', max_uses: 1, note: c.querySelector('#ocNote').value.trim() || null }); }
        catch (e) { if (e.code === '23505') { code = genCode(); await ins({ code, kind: 'free', max_uses: 1, note: c.querySelector('#ocNote').value.trim() || null }); } else throw e; }
        const out = c.querySelector('#ocFreeOut');
        out.innerHTML = `<p class="cl-ok">Code: <b style="font-size:20px;letter-spacing:1px">${code}</b></p><div class="cl-row"><button class="btn ghost" type="button" id="ocCopy">Copy</button>${navigator.share ? '<button class="btn ghost" type="button" id="ocShare">Share</button>' : ''}</div>`;
        const msg = `Your free Knowtopia code: ${code}\nOpen ${SITE}?account → Me → create your account → enter the code in "Have a code?".`;
        out.querySelector('#ocCopy').onclick = () => { try { navigator.clipboard.writeText(code); say('Copied'); } catch (x) {} };
        const shb = out.querySelector('#ocShare'); if (shb) shb.onclick = () => navigator.share({ text: msg }).catch(() => {});
        c.querySelector('#ocNote').value = ''; list();
      } catch (e) { fail(e); }
    };
    c.querySelector('#ocDisc').onclick = async () => {
      er.textContent = '';
      const code = c.querySelector('#ocDC').value.trim().toUpperCase(), pc = +c.querySelector('#ocDP').value, mu = +c.querySelector('#ocDU').value || null, vd = c.querySelector('#ocDV').value;
      if (!/^[A-Z0-9-]{4,24}$/.test(code)) { er.textContent = 'Code: 4–24 letters, numbers or -'; return; }
      if (!(pc >= 1 && pc <= 100)) { er.textContent = 'Enter % off between 1 and 100.'; return; }
      if (!vd) { er.textContent = 'Choose the last valid date.'; return; }
      try {
        await ins({ code, kind: 'discount', percent: pc, max_uses: mu, valid_until: new Date(vd + 'T23:59:59+05:30').toISOString() });
        say('Discount code ' + code + ' created ✓'); ['#ocDC', '#ocDP', '#ocDU', '#ocDV'].forEach(q => c.querySelector(q).value = ''); list();
      } catch (e) { er.textContent = e.code === '23505' ? 'This code already exists.' : errText(e); }
    };
    c.querySelector('#ocWho').onclick = async () => {
      const box = c.querySelector('#ocWhoOut'); box.textContent = 'Loading…';
      try { const r = await rest('rpc/code_report', { method: 'POST', body: {} });
        box.innerHTML = (r || []).length ? r.map(u => `<div>${esc(u.code)} · ${esc(u.email)}${u.course ? ' · ' + esc(courseName(u.course)) : ''} · ${new Date(u.used_at).toLocaleDateString('en-IN')}</div>`).join('') : 'No codes used yet.';
      } catch (e) { box.textContent = errText(e); }
    };
    async function list() {
      const box = c.querySelector('#ocList');
      try {
        const r = await rest('codes?select=*&order=created_at.desc&limit=100');
        box.innerHTML = (r || []).length ? r.map(x => `<div style="display:flex;gap:8px;align-items:center;justify-content:space-between;border-top:1px solid #eee;padding:6px 0">
          <div><b>${esc(x.code)}</b> ${x.kind === 'free' ? 'Free' : x.percent + '% off'}${x.note ? ' · ' + esc(x.note) : ''}<br>Used ${x.used}${x.max_uses ? '/' + x.max_uses : ''}${x.valid_until ? ' · till ' + new Date(x.valid_until).toLocaleDateString('en-IN') : ''}${x.active ? '' : ' · <b style="color:#B71C2C">stopped</b>'}</div>
          <span style="display:flex;gap:10px;align-items:center;flex:none"><button class="cl-link" type="button" data-oc="${esc(x.code)}" data-act="${x.active ? 0 : 1}">${x.active ? 'Stop' : 'Start'}</button>${+x.used ? '' : `<button class="cl-link" type="button" data-ocdel="${esc(x.code)}" style="color:#B71C2C" aria-label="Delete code ${esc(x.code)}">🗑 Delete</button>`}</span></div>`).join('') + ((r || []).some(x => +x.used) ? '<p class="cl-small" style="margin:6px 0 0">Used codes can\'t be deleted — use Stop instead.</p>' : '') : 'No codes yet.';
        box.querySelectorAll('[data-oc]').forEach(b => b.onclick = async () => {
          try { await rest('codes?code=eq.' + encodeURIComponent(b.dataset.oc), { method: 'PATCH', headers: { Prefer: 'return=minimal' }, body: { active: b.dataset.act === '1' } }); list(); } catch (e) { fail(e); }
        });
        /* never-used codes can be deleted (rpc delete_unused_code refuses a code that has been used) */
        box.querySelectorAll('[data-ocdel]').forEach(b => b.onclick = async () => {
          const code = b.dataset.ocdel; er.textContent = '';
          if (!confirm(`Delete code ${code}? This can't be undone.`)) return;
          b.disabled = true;
          try { const res = one(await rest('rpc/delete_unused_code', { method: 'POST', body: { p_code: code } }));
            if (res && res.ok === false) er.textContent = res.msg || 'This code could not be deleted.'; else say(res && res.msg ? res.msg : 'Code ' + code + ' deleted');
            list();
          } catch (e) { b.disabled = false; fail(e); }
        });
      } catch (e) { box.textContent = errText(e); }
    }
    list();
  }

  let sheet = null;
  function closeSheet() { if (sheet) sheet.classList.remove('show'); }
  function openSheet(html, closable = true) {
    style();
    if (!sheet) { sheet = D.createElement('div'); sheet.className = 'sheet cl-sheet'; sheet.id = 'svAuth'; sheet.setAttribute('role', 'dialog'); sheet.setAttribute('aria-modal', 'true'); sheet.setAttribute('aria-labelledby', 'clT'); D.body.appendChild(sheet); }
    sheet.onclick = e => { if (closable && e.target === sheet) closeSheet(); };
    sheet.toggleAttribute('data-noclose', !closable);   // js/sheets.js and Escape (js/a11y.js) leave it open
    sheet.innerHTML = `<div class="sheet-in"><div class="sheet-grab"></div>${html}</div>`;
    sheet.classList.add('show');
    return sheet;
  }
  const errText = e => {
    const m = (e && e.message) || '';
    if (/invalid login/i.test(m)) return 'Wrong email or password.';
    if (/not confirmed/i.test(m)) return 'Please open the confirmation email we sent you first.';
    if (/already registered|already been registered|exists/i.test(m)) return 'This email already has an account. Please sign in.';
    if (/rate limit|too many/i.test(m) || (e && e.status === 429)) return 'Too many tries. Please wait a few minutes and try again.';
    if (/password/i.test(m) && /(6|8|characters|weak|short)/i.test(m)) return 'Please choose a stronger password (at least 8 characters).';
    if (!e || e.status === 0 || /fetch|network|connection/i.test(m)) return 'No internet connection. Please try again.';
    return m;
  };

  /* sign-up tick box (recorded with version + time: js/playready.js, rpc accept_terms / legal_status) */
  const consentText = r => r === 'student'
    ? 'I agree to the <a href="legal/terms.html">Terms</a> and <a href="legal/privacy.html">Privacy Policy</a>. <b>Under 18?</b> I am the parent or guardian making this account, or my parent or guardian agrees.'
    : 'I am 18 or older and I agree to the <a href="legal/privacy.html">Privacy Policy</a> and <a href="legal/terms.html">Terms</a>. If this account is for a child, I am their parent or guardian.';
  function form(mode, msg, opt = {}) {
    const T = { up: 'Create your free account', in: 'Sign in', forgot: 'Reset your password', newpw: 'Set a new password' }[mode];
    const pwField = mode !== 'forgot', emField = mode !== 'newpw';
    const el = openSheet(`<h3 id="clT">${T}</h3>
      ${mode === 'up' && opt.invite ? '<p class="cl-inv">🎉 Your parent invited you. Create your account with this email — you will be linked to them automatically.</p>' : ''}
      ${mode === 'up' ? '<p>Your progress will be saved to your account. Under 18? Please do this with your parent or guardian.</p>' : ''}
      ${mode === 'forgot' ? '<p>Enter your email and we will send you a link to set a new password.</p>' : ''}
      <form id="clF" novalidate>
        ${mode === 'up' ? `<fieldset class="cl-role" role="radiogroup" aria-required="true" aria-labelledby="clRoleL"><legend id="clRoleL">I am a:</legend><div class="cl-roles">
          <label class="cl-rc${opt.role === 'student' ? ' on' : ''}"><input type="radio" name="clRole" value="student"${opt.role === 'student' ? ' checked' : ''}><span aria-hidden="true">🎓</span><b>Student</b><small>I want to learn</small></label>
          <label class="cl-rc${opt.role === 'parent' ? ' on' : ''}"><input type="radio" name="clRole" value="parent"${opt.role === 'parent' ? ' checked' : ''}><span aria-hidden="true">👨‍👩‍👧</span><b>Parent</b><small>I want to follow my child</small></label></div></fieldset>` : ''}
        ${emField ? `<label for="clE">Email</label><input class="cl-in" id="clE" type="email" data-field="email" autocomplete="email" autocapitalize="none" spellcheck="false" required value="${esc(opt.email || '')}">` : ''}
        ${pwField ? `<label for="clP">${mode === 'newpw' ? 'New password' : 'Password'}</label><input class="cl-in" id="clP" type="password" autocomplete="${mode === 'in' ? 'current-password' : 'new-password'}" minlength="8" required>
          <label class="cl-show cl-small"><input type="checkbox" id="clSh"> Show password</label>` : ''}
        ${mode === 'up' || mode === 'newpw' ? '<p class="cl-small">At least 8 characters.</p>' : ''}
        ${mode === 'up' ? `<label class="cl-show cl-small" style="align-items:flex-start"><input type="checkbox" id="clC" style="margin-top:3px"> <span id="clCt">${consentText(opt.role)}</span></label>` : ''}
        <div class="cl-err" id="clErr" role="alert"></div>${msg ? `<div class="cl-ok" role="status">${esc(msg)}</div>` : ''}
        <button class="btn" type="submit" id="clGo">${{ up: 'Create account', in: 'Sign in', forgot: 'Send reset link', newpw: 'Save new password' }[mode]}</button>
      </form>
      ${mode === 'up' ? `<button class="cl-link" type="button" data-go="in">Already have an account? Sign in</button>` : ''}
      ${mode === 'in' ? '<button class="cl-link" type="button" data-go="forgot">Forgot password?</button><br><button class="cl-link" type="button" data-go="up">New here? Create a free account</button>' : ''}
      ${mode === 'forgot' ? '<button class="cl-link" type="button" data-go="in">Back to sign in</button>' : ''}
      ${mode !== 'newpw' ? '<div style="height:6px"></div><button class="btn ghost" type="button" id="clX">Cancel</button>' : ''}`, mode !== 'newpw');
    el.querySelectorAll('[data-go]').forEach(b => b.onclick = () => form(b.dataset.go));
    const x = el.querySelector('#clX'); if (x) x.onclick = closeSheet;
    el.querySelectorAll('input[name=clRole]').forEach(i => i.onchange = () => { el.querySelectorAll('.cl-rc').forEach(l => l.classList.toggle('on', l.contains(i) ? i.checked : false));
      const ct = el.querySelector('#clCt'); if (ct) ct.innerHTML = consentText(i.value); });
    const sh = el.querySelector('#clSh'); if (sh) sh.onchange = () => { el.querySelector('#clP').type = sh.checked ? 'text' : 'password'; };
    el.querySelector('#clF').onsubmit = async e => {
      e.preventDefault();
      const er = el.querySelector('#clErr'), go = el.querySelector('#clGo'); er.textContent = '';
      const email = emField ? el.querySelector('#clE').value.trim().toLowerCase() : '', pw = pwField ? el.querySelector('#clP').value : '';
      if (emField && window.Fields && !Fields.valid(el.querySelector('#clF')).ok) return;   // js/fields.js shows the message under the box
      if (emField && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { er.textContent = 'Please enter a valid email address.'; return; }
      if (pwField && mode !== 'in' && pw.length < 8) { er.textContent = 'Please use at least 8 characters.'; return; }
      if (pwField && !pw) { er.textContent = 'Please enter your password.'; return; }
      const rc = el.querySelector('input[name=clRole]:checked'), rl = rc ? rc.value : null;
      if (mode === 'up' && !rl) { er.textContent = 'Please choose: Student or Parent.'; return; }
      if (mode === 'up' && !el.querySelector('#clC').checked) { er.textContent = rl === 'student' ? 'Please tick the box to agree (with your parent or guardian if you are under 18).' : 'Please tick the box: a parent or guardian must create a child\u2019s account.'; return; }
      go.disabled = true; const label = go.textContent; go.textContent = 'Please wait…';
      try {
        if (mode === 'up') {
          set(PEND_K, JSON.stringify({ email, role: rl }));   // set on the server after the first sign-in
          const r = await signUp(email, pw, rl);
          if (r === 'confirm') { openSheet(`<h3 id="clT">Check your email 📧</h3><p>We sent a confirmation link to <b>${esc(email)}</b>. Open it on this phone to finish creating your account.</p><p class="cl-small">Not there? Check Spam or Promotions.</p><button class="btn" type="button" id="clX">OK</button>`).querySelector('#clX').onclick = closeSheet; return; }
          if (sheet.querySelector('#clF')) closeSheet(); say(isParent() ? 'Account created ✓ Welcome!' : 'Account created ✓ Your progress is being saved');
        } else if (mode === 'in') { await signIn(email, pw); if (sheet.querySelector('#clF')) closeSheet(); say('Signed in ✓'); }
        else if (mode === 'forgot') { await forgot(email); form('in', 'If this email has an account, a reset link is on its way. Open it on this phone.'); return; }
        else if (mode === 'newpw') { await newPassword(pw); recovery = false; try { sessionStorage.removeItem('sv_recovery'); } catch (e) {} closeSheet(); say('New password saved ✓'); arrive(); }
        repaintMe();
      } catch (err) { er.textContent = errText(err); go.disabled = false; go.textContent = label; }
    };
    const f = el.querySelector(opt.email ? '#clP' : '.cl-in'); if (f && matchMedia('(pointer:fine)').matches) f.focus();
  }

  function choose(local, cloud, when, uid) {
    const info = p => { const st = p.st || {}, q = Object.keys(st.topics || {}).length, ca = st.ca && st.ca.level ? ' · CA ' + st.ca.level : '';
      return `${esc((st.profile && st.profile.name) || 'Student')}${ca} · ${window.kfmt ? kfmt(st.xp || 0) : (st.xp || 0)} ⭐ · ${q} quests`; };
    const d = when ? new Date(when).toLocaleString('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : '';
    const el = openSheet(`<h3 id="clT">Which progress should we keep?</h3><p>This phone and your account both have progress. Pick one — the other will be replaced.</p>
      <button class="cl-pick" type="button" data-k="cloud"><b>☁️ Progress in my account</b><small>${info(cloud)}${d ? ' · saved ' + d : ''}</small></button>
      <button class="cl-pick" type="button" data-k="local"><b>📱 Progress on this phone</b><small>${info(local)}</small></button>`, false);
    el.querySelectorAll('[data-k]').forEach(b => b.onclick = async () => {
      el.querySelectorAll('[data-k]').forEach(x => x.disabled = true);
      if (b.dataset.k === 'cloud') adopt(cloud, uid);
      else { setMeta({ uid }); linked = true; await push(true); closeSheet(); say('Saved this phone’s progress to your account ✓'); paint(); }
    });
  }

  /* ---------- sign-in gate ---------- */
  const gateCss = `#svGate{position:fixed;inset:0;z-index:980;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;padding:28px 22px;text-align:center;
background:radial-gradient(120% 80% at 50% 0%,#5B0F1B 0%,#15161C 70%);color:#F4EAD8;overflow:auto}
#svGate h1{margin:0;font-size:34px;letter-spacing:.5px}#svGate h1 span{color:#C9A76A}
#svGate p{margin:0;max-width:420px;line-height:1.5;color:#e9dcc4}
#svGate .g-btns{display:flex;flex-direction:column;gap:10px;width:100%;max-width:340px;margin-top:10px}
#svGate button{font-size:17px;font-weight:700;padding:14px;border-radius:14px;border:0;cursor:pointer}
#svGate .g-up{background:#C9A76A;color:#15161C}#svGate .g-in{background:transparent;color:#F4EAD8;border:1.5px solid #C9A76A}
#svGate .g-legal{font-size:12px;color:#c9bba0}#svGate .g-legal a{color:#C9A76A}
html.sv-gated,html.sv-gated body{overflow:hidden}`;
  function gate() {
    let g = D.getElementById('svGate');
    if (S || demo() || !D.body) {
      if (g) { g.remove(); D.documentElement.classList.remove('sv-gated'); D.querySelectorAll('[data-sv-inert]').forEach(x => { x.inert = false; x.removeAttribute('data-sv-inert'); }); }
      return;
    }
    if (g) return;
    style();
    if (!D.getElementById('svGateCss')) { const c = D.createElement('style'); c.id = 'svGateCss'; c.textContent = gateCss; D.head.appendChild(c); }
    g = D.createElement('div'); g.id = 'svGate'; g.setAttribute('role', 'dialog'); g.setAttribute('aria-modal', 'true'); g.setAttribute('aria-labelledby', 'svGateT');
    g.innerHTML = `<img class="gate-logo" src="icons/logo-full.webp" alt=""><h1 id="svGateT" class="sv-sr">Knowtopia</h1><p class="gate-tag">An ideal world of learning</p>
      <p>Learn, practise and play — CBSE Class 1–12 and CA Foundation. Create a free account to start; your progress is saved safely to it.</p>
      <div class="g-btns"><button class="g-up" type="button" data-cl="up">Create free account</button><button class="g-in" type="button" data-cl="in">Sign in</button></div>
      <p class="g-legal">A parent or guardian creates a child's account. <a href="legal/privacy.html">Privacy</a> · <a href="legal/terms.html">Terms</a></p>`;
    D.body.appendChild(g); D.documentElement.classList.add('sv-gated'); wire(g); gateInert();
  }
  function gateInert() {                             // things the app adds later stay unreachable behind the gate
    if (!D.getElementById('svGate')) return;
    [...D.body.children].forEach(x => { if (x.tagName !== 'SCRIPT' && x.id !== 'svGate' && x.id !== 'mDock' && !x.classList.contains('sheet') && !x.inert) { x.inert = true; x.setAttribute('data-sv-inert', '1'); } });
  }

  function repaintMe() { const c = D.getElementById('svCloud'); if (c) { c.dataset.h = ''; paint(); } const o = D.getElementById('svCloudOb'); if (o && S) o.remove(); }

  /* ---------- 5b. two copies open (installed app + browser tab): keep them in step ----------
     A copy left open in the background still holds old progress in memory and saves it when it is hidden or closed,
     which used to wipe a name or exam date saved in the other copy. When another copy saves, take its progress. */
  addEventListener('storage', e => {
    if (e.key !== 'sv_state' || !e.newValue) return;
    try { const n = JSON.parse(e.newValue); if (!n || typeof n !== 'object') return; Object.keys(ST).forEach(k => delete ST[k]); Object.assign(ST, n); } catch (x) {}
  });

  /* ---------- 6. start ---------- */
  function start() {
    gate();
    new MutationObserver(() => { if (!start.t) start.t = requestAnimationFrame(() => { start.t = 0; inject(); gateInert(); }); }).observe(D.body, { childList: true, subtree: true });
    inject();
    if (linkMsg) setTimeout(() => say(linkMsg), 800);
    try { if (sessionStorage.getItem('sv_recovery')) recovery = true; } catch (e) {}
    if (invite && !S) form('up', null, { email: invite.email, role: 'student', invite: true });
    if (isParent()) enterParent();
    if (S && recovery) form('newpw');                // ask for the new password straight away, before anything else can reload the page
    if (S) arrive().then(() => { if (recovery && !(sheet && sheet.classList.contains('show'))) form('newpw'); });
    setInterval(() => push(), 30000);
    D.addEventListener('visibilitychange', () => { if (D.visibilityState === 'hidden') push(false, true); else if (S && !linked) arrive(); });
    addEventListener('online', () => { if (S) (linked ? push() : arrive()); });
  }
  D.readyState === 'loading' ? D.addEventListener('DOMContentLoaded', () => setTimeout(start, 0)) : setTimeout(start, 0);

  window.Cloud = { rest, call, refreshAccess: access, user: () => (S && S.user) || null, api: API, key: KEY, errText: e => errText(e), sheet: openSheet, closeSheet, admin: () => !!(S && meta().adm), signedIn: () => !!S, email: () => (S && S.user && S.user.email) || '', courses, locked, has: c => courses().some(a => a.course === c), save: () => push(true), open: form, _status: () => status,
    isParent, role: () => role(), signOut: () => signOut() };
})();
