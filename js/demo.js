/* The temporary demo login has been REMOVED (owner's request).
   This file only cleans up phones that were still in demo: it puts back the student's own progress
   before app.js reads it, deletes every demo key, and strips ?demo from the address. Must load before js/app.js. */
(function () {
  const LS = localStorage;
  const get = k => { try { return LS.getItem(k); } catch (e) { return null; } };
  const set = (k, v) => { try { v == null ? LS.removeItem(k) : LS.setItem(k, v); } catch (e) {} };
  const sw = get('sv_demo_swap');                       // pending switch (also used by js/cloud.js)
  if (sw != null) { set('sv_state', sw === '__none__' ? null : sw); set('sv_demo_swap', null); }
  if (get('sv_demo') != null || get('sv_state_real') != null) {
    const real = get('sv_state_real');
    if (get('sv_demo') != null) set('sv_state', real == null || real === '__none__' ? null : real);
    set('sv_state_real', null); set('sv_demo', null);
  }
  // leftover demo profile on a phone (from the removed demo login): never let it become a real account's progress
  try { const st = JSON.parse(get('sv_state') || 'null'); if (st && st.profile && st.profile.name === 'Demo Student') set('sv_state', null); } catch (e) {}
  if (/[?&]demo\b/.test(location.search)) {
    try { const u = new URL(location.href); u.searchParams.delete('demo'); history.replaceState(history.state, '', u.pathname + u.search + u.hash); } catch (e) {}
  }
})();
