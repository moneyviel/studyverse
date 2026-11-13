/* ================= 📳 Phone reminders (js/notify.js) =================
   One friendly reminder a day on the student's phone (web push; works in the Play Store app and in Chrome).
   • Offer: after a student FINISHES a topic/unit (js/mindgym.js calls Notify.afterTopic), a small card asks
     "Want one reminder a day?" — only then does the phone show its own Allow / Don't allow question.
     Asked at most twice, and never again within 3 days of "Not now".
   • Me → Settings: "📳 Phone reminders" switch (school Me and CA Profile), placed next to 🎵 Sound & music.
   • Parent control: Parent Hub → Controls → 📳 Phone reminders (js/playready.js). The SERVER checks it before sending.
   • Server: supabase/migrations/20261116_push_reminders.sql (rpc push_save / push_off; table studyverse.push_subs)
     and the Edge Function knowtopia-nudge (daily 17:31 India time, max one a day, skips students who studied today).
   • Only the push address and keys made by the browser are stored, plus the "topics to the next Mind Gym pack" number.
   • Parents (Parent Hub accounts), signed-out phones and the demo login never see any of this.
   window.Notify = { afterTopic, enable, disable, isOn } */
(function () {
  'use strict';
  const D = document, LS = localStorage;
  const KEY = 'BM2AWrIS2AHej6IbsoZK2SCFv7hGpBJ6xlPAC1NWZSoa9yidTPPjEmCgS5dVy7Z59yFVRT_qK-JeJkPlFlqQYIQ';   // public VAPID key (studyverse.job_config)
  const SK = 'sv_push';
  const C = () => window.Cloud || null;
  const say = m => { try { toast(m); } catch (e) {} };
  const tap = k => { try { sfx(k); } catch (e) {} };
  const one = r => Array.isArray(r) ? r[0] : r;
  const jget = (k, d) => { try { const v = JSON.parse(LS.getItem(k)); return v == null ? d : v; } catch (e) { return d; } };
  const jset = (k, v) => { try { v == null ? LS.removeItem(k) : LS.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const demo = () => { try { return !!LS.getItem('sv_demo'); } catch (e) { return false; } };
  const myId = () => { const u = C() && C().user(); return u ? u.id : null; };
  const signedIn = () => !!(C() && C().signedIn() && !demo() && myId());
  const isParent = () => { try { return !!(C() && C().isParent && C().isParent()); } catch (e) { return false; } };
  const isCA = () => { try { return !!(ST && ST.profile && ST.profile.course === 'ca'); } catch (e) { return false; } };
  const supported = () => 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window;
  const parentAllows = () => { try { return !(window.PlayReady && PlayReady.social && PlayReady.social().push === false); } catch (e) { return true; } };
  const rpc = async (n, b) => one(await C().rest('rpc/' + n, { method: 'POST', body: b || {} }));
  const need = () => { try { return window.MindGym && MindGym.need ? MindGym.need() : null; } catch (e) { return null; } };
  const today = () => new Date(Date.now() + 5.5 * 3600e3).toISOString().slice(0, 10);

  function st() { const s = jget(SK, null); return s && s.uid === myId() ? s : { uid: myId(), on: false, ask: 0, no: 0 }; }
  const put = o => jset(SK, Object.assign(st(), o, { uid: myId() }));
  const isOn = () => signedIn() && st().on && supported() && Notification.permission === 'granted';

  const b64 = s => { const p = '='.repeat((4 - s.length % 4) % 4); const r = atob((s + p).replace(/-/g, '+').replace(/_/g, '/')); return Uint8Array.from(r, c => c.charCodeAt(0)); };
  const reg = () => Promise.race([navigator.serviceWorker.ready, new Promise((_, no) => setTimeout(() => no(new Error('The app is still starting — please try again in a moment.')), 8000))]);

  async function save(sub) {
    const j = sub.toJSON(), k = j.keys || {};
    const r = await rpc('push_save', { p_endpoint: j.endpoint, p_p256dh: k.p256dh, p_auth: k.auth, p_need: need() });
    if (!r || !r.ok) throw new Error((r && r.msg) || 'Could not switch reminders on.');
    return r;
  }

  /* switch on: the phone asks Allow / Don't allow, then we save this phone */
  async function enable() {
    if (!signedIn() || isParent()) return false;
    if (!supported()) { say('This browser cannot show reminders. Use the Knowtopia app or Chrome.'); return false; }
    if (!parentAllows()) { say('Your parent has turned phone reminders off.'); return false; }
    let perm = Notification.permission;
    if (perm === 'default') perm = await Notification.requestPermission();
    if (perm !== 'granted') { put({ on: false }); say('Reminders are blocked. You can allow notifications for Knowtopia in your phone settings.'); render(); return false; }
    try {
      const r = await reg();
      const sub = (await r.pushManager.getSubscription()) || await r.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64(KEY) });
      const res = await save(sub);
      if (res.allowed === false) { await rpc('push_off', { p_endpoint: sub.endpoint }).catch(() => {}); put({ on: false }); say('Your parent has turned phone reminders off.'); render(); return false; }
      put({ on: true, sync: today() }); tap('right'); say('📳 Reminders on — at most one a day, around 5:30 pm.'); render(); return true;
    } catch (e) { put({ on: false }); say(e && /^(NotAllowedError|AbortError|InvalidStateError|NotSupportedError)$/.test(e.name) ? 'This phone could not turn on reminders right now. Please try again later.' : ((C() && C().errText ? C().errText(e) : e.message) || 'Could not switch reminders on.')); render(); return false; }
  }

  /* switch off: forget this phone on the server, then drop the push address */
  async function disable(quiet) {
    put({ on: false });
    try {
      const r = await reg(), sub = await r.pushManager.getSubscription();
      if (sub) { await rpc('push_off', { p_endpoint: sub.endpoint }).catch(() => {}); await sub.unsubscribe().catch(() => {}); }
    } catch (e) {}
    if (!quiet) say('Reminders off.'); render();
  }

  /* once a day while on: keep the server copy fresh (Mind Gym number, phone moved to this account, new push address) */
  async function refresh(force) {
    if (!signedIn() || isParent() || !supported()) return;
    const s = st(); if (!s.on) return;
    if (Notification.permission !== 'granted') { put({ on: false }); render(); return; }
    if (!force && s.sync === today()) return;
    try {
      const r = await reg();
      const sub = (await r.pushManager.getSubscription()) || await r.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64(KEY) });
      const res = await save(sub); put({ sync: today() });
      if (res.allowed === false) render();
    } catch (e) { /* offline: try again next time */ }
  }

  /* ---------- offer after a finished topic ---------- */
  function afterTopic() {
    if (!signedIn() || isParent() || !supported()) return;
    if (st().on) { refresh(true); return; }
    const s = st();
    if (Notification.permission === 'denied' || !parentAllows() || s.no >= 2 || Date.now() - (s.ask || 0) < 3 * 864e5) return;
    setTimeout(offer, 2500);   // after the "well done" moment, not on top of it
  }
  function offer() {
    if (D.getElementById('ntOffer') || st().on) return;
    style(); put({ ask: Date.now() });
    const w = isCA() ? 'unit' : 'topic';
    D.body.insertAdjacentHTML('beforeend', `<div id="ntOffer" class="nt-offer" role="dialog" aria-labelledby="ntOfT" aria-describedby="ntOfD">
      <div class="nt-big" aria-hidden="true">📳</div><b id="ntOfT">Want one reminder a day?</b>
      <p id="ntOfD">Nice work finishing that ${w}! We can send one short reminder around 5:30 pm to keep your 🔥 streak and tell you when new Mind Gym challenges are close. Never at night or in school hours. Turn it off any time in Me.</p>
      <div class="nt-btns"><button type="button" class="btn" id="ntYes">🔔 Yes, remind me</button><button type="button" class="btn ghost" id="ntNo">Not now</button></div></div>`);
    const box = D.getElementById('ntOffer'); tap('open');
    box.querySelector('#ntYes').onclick = async () => { box.remove(); await enable(); };
    box.querySelector('#ntNo').onclick = () => { box.remove(); put({ no: (st().no || 0) + 1 }); };
    setTimeout(() => { const y = D.getElementById('ntYes'); if (y) y.focus(); }, 50);
  }

  /* ---------- Me → Settings card ---------- */
  function cardHtml() {
    const s = st();
    if (!supported()) return `<h3>📳 Phone reminders</h3><p class="sub">This browser can't show reminders. Open Knowtopia from the Play Store app or in Chrome to use them.</p>`;
    if (!parentAllows()) return `<h3>📳 Phone reminders</h3><p class="sub">Your parent has turned phone reminders off. You can still learn as usual.</p>`;
    const denied = Notification.permission === 'denied';
    const on = s.on && Notification.permission === 'granted';
    return `<h3>📳 Phone reminders</h3>
      <label class="nt-sw" for="ntSw"><span class="nt-t"><b>One reminder a day</b><small>Around 5:30 pm, only if you haven't studied yet. Never at night or in school hours.</small></span>
      <input type="checkbox" role="switch" id="ntSw" ${on ? 'checked' : ''} ${denied ? 'disabled' : ''}><span aria-hidden="true"></span></label>
      ${denied ? `<p class="sub nt-warn">Notifications are blocked for Knowtopia. To use reminders, allow them in your phone's settings, then come back here.</p>` : ''}`;
  }
  function render() {
    const c = D.getElementById('svPush'); if (!c) return;
    c.innerHTML = cardHtml();
    const sw = c.querySelector('#ntSw');
    if (sw) sw.onchange = async () => { sw.disabled = true; if (sw.checked) await enable(); else await disable(false); };
  }
  function place() {
    if (!signedIn() || isParent()) { const o = D.getElementById('svPush'); if (o) o.remove(); return; }
    const snd = D.querySelector('.screen.active #meSound'); if (!snd) return;
    if (snd.nextElementSibling && snd.nextElementSibling.id === 'svPush') return;
    const o = D.getElementById('svPush'); if (o) o.remove();
    style(); snd.insertAdjacentHTML('afterend', '<div class="card" id="svPush"></div>'); render();
  }

  function style() {
    if (D.getElementById('ntCss')) return;
    D.head.insertAdjacentHTML('beforeend', `<style id="ntCss">
.nt-offer{position:fixed;left:12px;right:12px;bottom:calc(84px + env(safe-area-inset-bottom));z-index:990;max-width:460px;margin:0 auto;background:#fff;color:#1b1f3a;border-radius:20px;padding:16px 16px 14px;box-shadow:0 10px 30px rgba(0,0,0,.28);text-align:center;animation:ntUp .25s ease-out}
.nt-offer b{display:block;font-size:18px;margin:2px 0 6px}.nt-offer p{font-size:14px;line-height:1.45;margin:0 0 12px;color:#4a4d57}.nt-big{font-size:34px}
.nt-btns{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}.nt-btns .btn{flex:1 1 150px;min-height:48px}
@keyframes ntUp{from{transform:translateY(20px);opacity:0}to{transform:none;opacity:1}}
@media (prefers-reduced-motion:reduce){.nt-offer{animation:none}}
.nt-sw{display:flex;align-items:center;gap:12px;min-height:56px;cursor:pointer}.nt-sw .nt-t{flex:1;min-width:0;line-height:1.3}.nt-sw .nt-t b{display:block;font-size:15px}.nt-sw .nt-t small{color:var(--muted,#5d5a55);font-size:12.5px}
.nt-sw input{position:absolute;opacity:0;width:1px;height:1px}
.nt-sw input+span{flex:none;width:52px;height:30px;border-radius:30px;background:#c9c2b2;position:relative;transition:background .2s}
.nt-sw input+span::after{content:'';position:absolute;top:3px;left:3px;width:24px;height:24px;border-radius:50%;background:#fff;transition:transform .2s;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.nt-sw input:checked+span{background:#1d7a46}.nt-sw input:checked+span::after{transform:translateX(22px)}.nt-sw input:disabled+span{opacity:.5}
.nt-sw input:focus-visible+span{outline:3px solid #8A6A2E;outline-offset:2px}.nt-warn{color:#9a1b1b!important;margin-top:6px}
</style>`);
  }

  /* start: keep the card in Me, refresh the server copy once a day, react to the parent switch */
  let t = 0;
  const mo = new MutationObserver(() => { if (t) return; t = setTimeout(() => { t = 0; place(); }, 120); });
  function start() {
    try { mo.observe(D.querySelector('main') || D.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] }); } catch (e) {}
    place();
    setTimeout(() => refresh(false), 6000);
    setTimeout(async () => { try { if (window.PlayReady && PlayReady.pullSocial) { await PlayReady.pullSocial(); if (!parentAllows() && st().on) await disable(true); } } catch (e) {} render(); }, 9000);
  }
  D.readyState === 'loading' ? D.addEventListener('DOMContentLoaded', start) : start();

  window.Notify = { afterTopic, enable, disable, isOn };
})();
