/* ================= StudyVerse app ================= */
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const BOARDS = [
  { id: 'cbse', name: 'CBSE', live: true }, { id: 'icse', name: 'ICSE', live: false },
  { id: 'state', name: 'State Board', live: false }, { id: 'cambridge', name: 'Cambridge', live: false }, { id: 'ib', name: 'IB', live: false }
];
const AVATARS = ['🦁', '🐯', '🦊', '🐼', '🐨', '🐸', '🦄', '🐙', '🦉', '🐬', '🚀', '⭐'];
const MAX_GRADE = 12;

/* ---------- read aloud: pick the clearest, most natural voice on this device ---------- */
const VOICE = { en: null, hi: null, rate: 0.9 };
try { Object.assign(VOICE, JSON.parse(localStorage.getItem('sv_voice') || '{}')); } catch (e) {}
function voiceScore(v, hi) {
  const n = (v.name + ' ' + v.voiceURI).toLowerCase(), l = (v.lang || '').toLowerCase().replace('_', '-');
  let s = 0;
  if (hi) { if (l.startsWith('hi')) s += 50; else return -1; }
  else { if (l === 'en-in') s += 40; else if (l.startsWith('en-gb') || l.startsWith('en-au')) s += 25; else if (l.startsWith('en')) s += 20; else return -1; }
  if (/natural|neural|online|premium|enhanced/.test(n)) s += 30;
  if (/google/.test(n)) s += 20;
  if (/neerja|swara|heera|kalpana|lekha|veena|aditi|raveena|sonia|libby|ava|samantha|serena/.test(n)) s += 8;
  if (!v.localService) s += 4;
  if (/compact|espeak|robot/.test(n)) s -= 40;
  return s;
}
function bestVoice(hi) {
  const vs = ('speechSynthesis' in window) ? speechSynthesis.getVoices() : [];
  const saved = hi ? VOICE.hi : VOICE.en; const pick = saved && vs.find(v => v.voiceURI === saved);
  if (pick) return pick;
  return vs.map(v => [voiceScore(v, hi), v]).filter(x => x[0] >= 0).sort((a, b) => b[0] - a[0])[0]?.[1] || null;
}
function speechText(t, hi) {
  let x = String(t).replace(/_{2,}/g, hi ? 'रिक्त स्थान' : 'blank');
  x = x.replace(/₹\s?([\d,.]+)/g, (m, n) => hi ? `${n} रुपये` : `${n} rupees`)
       .replace(/(\d)\s*[×x]\s*(\d)/g, hi ? '$1 गुणा $2' : '$1 times $2').replace(/÷/g, hi ? ' भाग ' : ' divided by ')
       .replace(/(\d)\s*−\s*(\d)/g, hi ? '$1 घटा $2' : '$1 minus $2').replace(/=/g, hi ? ' बराबर ' : ' equals ')
       .replace(/(\d+)\s*\/\s*(\d+)/g, hi ? '$2 में से $1' : '$1 over $2').replace(/°/g, hi ? ' डिग्री' : ' degrees')
       .replace(/²/g, hi ? ' का वर्ग' : ' squared').replace(/³/g, hi ? ' का घन' : ' cubed').replace(/√/g, hi ? 'वर्गमूल ' : 'square root of ')
       .replace(/π/g, 'pi').replace(/[🔊🎉👍💪🧬🔍✅❌⭐🎯]/gu, '');
  return x;
}
window.speak = function (t) {
  try {
    if (!('speechSynthesis' in window) || !t) return;
    speechSynthesis.cancel();
    const hi = /[\u0900-\u097F]/.test(t), v = bestVoice(hi);
    const parts = speechText(t, hi).split(/(?<=[.!?।])\s+|\n+/).map(s => s.trim()).filter(Boolean);
    parts.forEach(part => {
      const u = new SpeechSynthesisUtterance(part);
      u.lang = v ? v.lang : (hi ? 'hi-IN' : 'en-IN'); if (v) u.voice = v;
      u.rate = VOICE.rate || 0.9; u.pitch = 1.04; u.volume = 1;
      speechSynthesis.speak(u);
    });
  } catch (e) {}
};
if ('speechSynthesis' in window) { speechSynthesis.getVoices(); speechSynthesis.onvoiceschanged = () => { try { renderVoicePicker(); } catch (e) {} }; }
function renderVoicePicker() {
  const el = document.getElementById('voicePick'); if (!el || !('speechSynthesis' in window)) return;
  const vs = speechSynthesis.getVoices();
  const opts = hi => vs.map(v => [voiceScore(v, hi), v]).filter(x => x[0] >= 0).sort((a, b) => b[0] - a[0]).slice(0, 8)
    .map(([s, v]) => `<option value="${esc(v.voiceURI)}" ${bestVoice(hi) === v ? 'selected' : ''}>${esc(v.name)}${s >= 70 ? ' ★' : ''}</option>`).join('');
  el.innerHTML = `<div class="srow"><span>🗣️ English voice</span><select id="vEn">${opts(false) || '<option>Phone default</option>'}</select></div>
    <div class="srow"><span>🗣️ हिंदी आवाज़</span><select id="vHi">${opts(true) || '<option>Phone default</option>'}</select></div>
    <div class="srow"><span>🐢 Speed</span><input type="range" id="vRate" min="70" max="110" value="${Math.round((VOICE.rate || .9) * 100)}"></div>
    <div class="srow"><button class="btn ghost" id="vTest" style="width:100%">▶ Hear a sample</button></div>`;
  const saveV = () => { try { localStorage.setItem('sv_voice', JSON.stringify(VOICE)); } catch (e) {} };
  el.querySelector('#vEn').onchange = e => { VOICE.en = e.target.value; saveV(); speak('Hello! I will read your lessons to you.'); };
  el.querySelector('#vHi').onchange = e => { VOICE.hi = e.target.value; saveV(); speak('नमस्ते! मैं तुम्हारे पाठ पढ़कर सुनाऊँगी।'); };
  el.querySelector('#vRate').oninput = e => { VOICE.rate = e.target.value / 100; saveV(); };
  el.querySelector('#vTest').onclick = () => speak('Three rows of four laddoos make twelve laddoos. ₹45 + ₹5 = ₹50.');
}
/* ---------- Read-along: speaks text and lights up each word as it is spoken ---------- */
const ReadAlong = (() => {
  let session = 0, timer = null;
  const SYM = { '×': 'times', 'x': null, '÷': 'divided by', '=': 'equals', '−': 'minus', '-': 'minus', '+': 'plus', '<': 'is less than', '>': 'is greater than', '%': 'percent' };
  const SYM_HI = { '×': 'गुणा', '÷': 'भाग', '=': 'बराबर', '−': 'घटा', '-': 'घटा', '+': 'जोड़', '<': 'से छोटा', '>': 'से बड़ा', '%': 'प्रतिशत' };
  const SKIP = '.spk,.ra-skip,script,style';
  function spokenOf(w, hi) {
    if (/^_{2,}[.,!?]*$/.test(w)) return hi ? 'रिक्त स्थान' : 'blank';
    const m = (hi ? SYM_HI : SYM)[w]; if (m) return m;
    const s = speechText(w, hi).trim();
    return /[\p{L}\p{N}]/u.test(s) ? s : '';
  }
  function wrap(el) {
    if (!el.querySelector('.ra-w')) {
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, { acceptNode: n => (n.parentElement.closest(SKIP) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT) });
      const nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
      nodes.forEach(n => {
        const blank = n.parentElement.closest('.blank');
        if (blank) { blank.classList.add('ra-w'); blank.dataset.say = 'blank'; return; }
        if (!n.nodeValue.trim()) return;
        const frag = document.createDocumentFragment();
        n.nodeValue.split(/(\s+)/).forEach(tok => {
          if (!tok) return;
          if (/^\s+$/.test(tok)) { frag.appendChild(document.createTextNode(tok)); return; }
          const sp = document.createElement('span'); sp.className = 'ra-w'; sp.textContent = tok; frag.appendChild(sp);
        });
        n.parentNode.replaceChild(frag, n);
      });
    }
    return [...el.querySelectorAll('.ra-w')];
  }
  function clear() { clearTimeout(timer); document.querySelectorAll('.ra-w.on').forEach(x => x.classList.remove('on')); document.querySelectorAll('.ra-reading').forEach(x => x.classList.remove('ra-reading')); document.querySelectorAll('.spk.ra-play').forEach(x => x.classList.remove('ra-play')); }
  function stop() { session++; api.active = false; clear(); try { speechSynthesis.cancel(); } catch (e) {} }
  function play(els, btn) {
    if (!('speechSynthesis' in window)) return;
    const was = btn && btn.classList.contains('ra-play');
    stop(); if (was) return;                       // second tap = stop
    const my = ++session; api.active = true; if (btn) btn.classList.add('ra-play');
    els = els.filter(Boolean); let left = 0;
    els.forEach((el, k) => {
      const words = wrap(el); if (!words.length) return;
      const hi = /[ऀ-ॿ]/.test(el.textContent), v = bestVoice(hi);
      let text = '', offs = [], idx = [];
      words.forEach((w, i) => { const s = w.dataset.say || spokenOf(w.textContent, hi); if (!s) return; offs.push(text.length); idx.push(i); text += s + ' '; });
      if (!text.trim()) return;
      left++;
      const u = new SpeechSynthesisUtterance(text.trim());
      u.lang = v ? v.lang : (hi ? 'hi-IN' : 'en-IN'); if (v) u.voice = v;
      u.rate = VOICE.rate || 0.9; u.pitch = 1.04;
      let gotB = false, cur = -1;
      const light = j => { if (my !== session || j === cur || j < 0) return; cur = j; words.forEach(w => w.classList.remove('on')); const w = words[idx[j]]; if (w) w.classList.add('on'); };
      const tick = j => { if (gotB || my !== session || j >= idx.length) return; light(j);
        const s = text.slice(offs[j], offs[j + 1] ?? text.length); timer = setTimeout(() => tick(j + 1), (s.length * 62 + 140) / u.rate); };
      u.onstart = () => { if (my !== session) return; document.querySelectorAll('.ra-reading').forEach(x => x.classList.remove('ra-reading')); el.classList.add('ra-reading'); tick(0); };
      u.onboundary = e => { if (my !== session || (e.name && e.name !== 'word')) return; if (!gotB) { gotB = true; clearTimeout(timer); }
        let j = 0; while (j + 1 < offs.length && offs[j + 1] <= e.charIndex) j++; light(j); };
      u.onend = u.onerror = () => { if (my !== session) return; clearTimeout(timer); words.forEach(w => w.classList.remove('on')); el.classList.remove('ra-reading'); if (--left <= 0) { api.active = false; clear(); } };
      speechSynthesis.speak(u);
    });
    if (!left) { api.active = false; clear(); }
  }
  const api = { play, stop, active: false };
  return api;
})();
window.ReadAlong = ReadAlong;
const spk = (t, opts) => `<button class="spk"${opts ? ' data-opts="1"' : ''} data-say="${esc(t)}" aria-label="Read aloud">🔊</button>`;
document.addEventListener('click', e => {
  const b = e.target.closest('.spk');
  if (b) { e.stopPropagation(); const host = b.dataset.ra ? b.closest(b.dataset.ra) : b.parentElement; const els = [host];
    if (b.dataset.opts) { const scope = b.closest('.card') || document; els.push(...scope.querySelectorAll('.opt:not([disabled])')); }
    if (host && 'speechSynthesis' in window) ReadAlong.play(els, b); else speak(b.dataset.say); return; }
  if (e.target.closest('.opt,.tfb,.btn,.navb')) ReadAlong.stop();
}, true);

/* ---------- 3D concept studio (loaded only when needed) ---------- */
let S3D = null;
async function scenes() { if (!S3D) S3D = await import('./scenes.js?v=24'); return S3D; }
const LABMAP = {};
async function labFor(topic, chapter) {
  const k = `g${ST.profile.grade}-${NAV.subject}`;
  if (!(k in LABMAP)) { try { LABMAP[k] = await loadJSON(`content/labs/${k}.json`); } catch (e) { LABMAP[k] = {}; } }
  if (LABMAP[k][topic.id]) return LABMAP[k][topic.id];
  if (topic.lab === 'angle') return { type: 'anglemaker', p: {} };
  /* No keyword guessing: a lab appears only when it was chosen and checked for this exact topic. */
  return null;
}
async function mount3D(host, topic, chapter) {
  const card = host.closest('.card');
  const spec = await labFor(topic, chapter);
  if (!spec) { if (card) card.style.display = 'none'; return false; }
  const ok = await Labs.mount(host, spec, { onWin: () => addXP(15, 'Lab challenge done!') });
  if (!ok && card) card.style.display = 'none';
  return ok;
}
function unmount3D() { try { Labs.unmount(); } catch (e) {} if (S3D) S3D.unmount(); }
function open3D() {
  const sh = $('#sheet3d'); sh.classList.add('show');
  mount3D($('#s3dHost'), RUN.t, RUN.c);
}
function close3D() { $('#sheet3d').classList.remove('show'); unmount3D(); }

/* ---------- saved progress (on this phone until logins arrive) ---------- */
let ST = { profile: null, xp: 0, streak: { n: 0, last: '' }, topics: {}, mistakes: {}, qstats: {} };
try { const s = JSON.parse(localStorage.getItem('sv_state') || 'null'); if (s) ST = Object.assign(ST, s); } catch (e) {}
const save = () => { try { localStorage.setItem('sv_state', JSON.stringify(ST)); } catch (e) {} };
const today = () => new Date().toISOString().slice(0, 10);

let CUR = null;               // curriculum.json
const DATA = {};              // "g6/maths" -> subject content or null
let NAV = {};                 // where we are: {subject, chapter, topic}

function toast(m) { const t = $('#toast'); t.textContent = m; t.classList.add('show'); clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.remove('show'), 1900); }
function hud() { $('#xp').textContent = ST.xp; $('#streak').textContent = ST.streak.n || 0; }
function addXP(n, msg) { ST.xp += n; save(); hud(); if (msg) toast(`${msg}  +${n} ⭐`); }
function bumpStreak() { const d = today(); if (ST.streak.last === d) return; const y = new Date(Date.now() - 864e5).toISOString().slice(0, 10); ST.streak.n = ST.streak.last === y ? ST.streak.n + 1 : 1; ST.streak.last = d; save(); hud(); }

/* ================= Back button & history (Android back gesture / browser back) =================
   Every screen change and every open sheet gets a browser history entry, so the system Back button
   goes to the previous screen or closes the sheet instead of closing the app. On the first screen,
   Back shows "Press back again to exit" and only a second Back within 2 s leaves.
   - Screens: the main screen functions are wrapped as "routes" (Nav.route) — replayed on Back.
     show() calls made outside a route (other modules) get an "anonymous" entry that re-shows that section.
   - Sub-states (quiz/test runners inside a screen): Nav.sub(restore) — Back calls restore().
   - Sheets (.sheet.show / .asksheet.show) are detected automatically; Back closes them.
   history.state = { sv: <session id>, pos: n }; pos 0 is the guard entry, stack[i] lives at pos i+1. */
const Nav = (() => {
  const SID = Math.random().toString(36).slice(2, 8), now = () => Date.now();
  let stack = [], pos = 0, depth = 0, restoring = false, expect = null, lastRouteAt = 0, routeShown = true, started = false, armTimer = null, anonN = 0, pendingReplay = null;
  const S = p => ({ sv: SID, pos: p });
  const isOpen = el => !!(el && el.isConnected && el.classList.contains('show'));
  const keyOf = (name, args) => { const a = Array.from(args || []); while (a.length && (a[a.length - 1] == null || a[a.length - 1] === '')) a.pop();
    try { return name + JSON.stringify(a, (k, v) => typeof v === 'function' ? undefined : v); } catch (e) { return name + '#' + (++anonN); } };
  function start() { if (started) return; started = true; try { history.replaceState(S(0), ''); } catch (e) {} pos = 0; }
  function disarm() { clearTimeout(armTimer); armTimer = null; }
  function rearm() { if (pos === 0 && stack.length) { try { history.pushState(S(1), ''); } catch (e) {} pos = 1; } }
  function push(entry) {
    start(); disarm(); rearm(); stack.length = pos;
    const top = stack[stack.length - 1];
    if (top && top.sheet && !isOpen(top.sheet)) { stack[stack.length - 1] = entry; try { history.replaceState(S(pos), ''); } catch (e) {} return; }  // reuse a just-closed sheet's entry
    stack.push(entry); pos = stack.length; try { history.pushState(S(pos), ''); } catch (e) {}
  }
  function rewindTo(j) {            // the route at stack[j] is being opened again (in-app back button, bottom nav): behave like Back
    start(); disarm(); rearm();
    const n = pos - (j + 1); stack.length = j + 1;
    if (n > 0) { pos = j + 1; expect = pos; try { history.go(-n); } catch (e) {} }
  }
  function route(name, fn) {
    if (fn && fn._nav) return fn;
    const w = function (...args) {
      if (restoring || depth > 0) { depth++; try { return fn.apply(this, args); } finally { depth--; } }
      const key = keyOf(name, args); let j = -1;
      for (let i = Math.min(pos, stack.length) - 1; i >= 0; i--) { const e = stack[i]; if (e.key === key && !e.sheet && !e.dead && !e.sub) { j = i; break; } }
      if (j >= 0) rewindTo(j); else push({ key, name, fn: w, args });
      lastRouteAt = now(); routeShown = false;
      depth++; try { return fn.apply(this, args); } finally { depth--; }
    };
    w._nav = true; w._raw = fn; return w;
  }
  function shown(id, navKey, prev) {   // called by show(): attribute it to a route, or give it its own entry
    if (restoring || depth > 0) { routeShown = true; return; }
    if (!routeShown && now() - lastRouteAt < 4000) { routeShown = true; return; }
    routeShown = true;
    if (prev === id || !ST.profile) return;
    push({ key: 'show:' + id + '#' + (++anonN), anon: id, navKey });
  }
  function sub(restore) { if (restoring || depth > 0) return; push({ key: 'sub#' + (++anonN), sub: true, restore }); }
  function replay(en) {
    restoring = true; lastRouteAt = now(); routeShown = false;
    try { if (en.fn) en.fn.apply(null, en.args); else if (en.anon) show(en.anon, en.navKey); } catch (e) { console.warn('Back navigation could not restore a screen', e); }
    finally { restoring = false; }
  }
  function closeSheet(el) {
    const btn = [...el.querySelectorAll('button')].find(b => b.matches('.ask-x,#rvX,#uxDone,[data-close]') || /^(close|done|got it|cancel|no thanks|not now)$/i.test(b.textContent.trim()));
    if (btn) btn.click(); else el.classList.remove('show');
  }
  function atGuard() {
    pos = 0; disarm();
    const base = stack[0];
    if (base && base.name !== 'world' && base.name !== 'onboard' && ST.profile) { stack = []; try { worldScreen(); } catch (e) {} return; }   // deep link: Back goes home first
    toast('Press back again to exit');
    armTimer = setTimeout(() => { armTimer = null; if (pos === 0 && stack.length) { try { history.pushState(S(1), ''); } catch (e) {} pos = 1; } }, 2000);
  }
  window.addEventListener('popstate', e => {
    const s = e.state;
    if (s && s.sv && s.sv !== SID) { if (s.pos > 0) { expect = null; try { history.go(-s.pos); } catch (x) {} } return; }   // entries left from before a reload
    const p = s && s.sv === SID ? s.pos : 0;
    if (expect !== null) { const ex = expect; expect = null; if (p === ex) return; }
    try { speechSynthesis.cancel(); } catch (x) {}
    try { document.dispatchEvent(new CustomEvent('sv:back')); } catch (x) {}
    if (p === 0) {
      if (!stack.length) { pos = 0; return; }
      if (stack[0].sheet) { stack.forEach(en => { if (en.sheet && isOpen(en.sheet)) closeSheet(en.sheet); }); stack = []; pos = 0; return; }
      const leaving = stack.slice(1); stack.length = 1;
      leaving.forEach(en => { if (en.sheet && isOpen(en.sheet)) { en.dead = true; closeSheet(en.sheet); } });
      if (leaving.some(en => !en.sheet && !en.dead) || pendingReplay) { pendingReplay = null; replay(stack[0]); }
      atGuard(); return;
    }
    if (p > stack.length) { pos = Math.min(p, stack.length); return; }
    const leaving = stack.slice(p); stack.length = p; pos = p;
    leaving.forEach(en => { if (en.sheet && isOpen(en.sheet)) { en.dead = true; closeSheet(en.sheet); } });
    const top = stack[p - 1];
    const needs = pendingReplay || leaving.some(en => !en.sheet && !en.dead);
    if (top.dead || top.sheet) { pendingReplay = needs ? (pendingReplay || leaving.find(en => en.sub && en.restore) || true) : null; stack.length = p - 1; pos = p - 1; expect = null; try { history.back(); } catch (x) {} return; }
    const low = leaving[0]; pendingReplay = null;
    if (!needs) return;
    if (low && low.sub && low.restore) { restoring = true; try { low.restore(); } catch (x) { replay(top); } finally { restoring = false; } }
    else replay(top);
  });
  /* sheets: an opened sheet gets an entry; closing it from its own button removes the entry again */
  const tracked = new Set();
  function scanSheets() {
    document.querySelectorAll('.sheet.show, .asksheet.show').forEach(el => { if (tracked.has(el) || el.hasAttribute('data-nonav')) return; /* data-nonav: the sheet handles Back itself */ tracked.add(el); if (ST.profile || started) push({ key: 'sheet:' + (el.id || '') + '#' + (++anonN), sheet: el }); });
    [...tracked].forEach(el => {
      if (isOpen(el)) return; tracked.delete(el);
      const i = stack.findIndex(en => en.sheet === el); if (i < 0) return;
      if (i === stack.length - 1 && pos === stack.length) { stack.pop(); pos = stack.length; expect = pos; try { history.back(); } catch (x) {} }
      else stack[i].dead = true;
    });
  }
  let scanT = 0;
  new MutationObserver(() => { if (!scanT) scanT = requestAnimationFrame(() => { scanT = 0; scanSheets(); }); }).observe(document.documentElement, { subtree: true, childList: true, attributes: true, attributeFilter: ['class'] });
  /* wrap the main screen functions once every script has loaded (outermost wrapper = includes every module's additions) */
  function wrapGlobals() {
    [['worldScreen', 'world'], ['subjectScreen'], ['chapterScreen'], ['playTopic'], ['practiceScreen'], ['squadScreen'], ['meScreen'], ['onboard'], ['pickStream']].forEach(([n, k]) => {
      if (typeof window[n] === 'function' && !window[n]._nav) window[n] = route(k || n, window[n]);
    });
    if (!stack.length && ST.profile) { start(); stack.push({ key: keyOf('world', []), name: 'world', fn: window.worldScreen, args: [] }); pos = 1; try { history.pushState(S(1), ''); } catch (e) {} }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wrapGlobals); else setTimeout(wrapGlobals, 0);
  return { route, sub, shown, get depth() { return stack.length; }, get pos() { return pos; }, _stack: () => stack.map(e => e.key) };
})();
window.Nav = Nav;

function show(id, navKey) {
  const prevScr = document.querySelector('.screen.active'); try { Nav.shown(id, navKey, prevScr && prevScr.id.slice(2)); } catch (e) {}
  document.querySelectorAll('.screen').forEach(e => e.classList.remove('active'));
  $('#s-' + id).classList.add('active');
  document.querySelectorAll('nav button').forEach(b => b.classList.toggle('on', b.dataset.s === navKey));
  $('nav').style.display = id === 'topic' || id === 'onboard' ? 'none' : '';
  $('header').style.display = id === 'onboard' ? 'none' : '';
  window.scrollTo(0, 0);
}

async function loadJSON(p) { const r = await fetch(p, { cache: 'no-cache' }); if (!r.ok) throw new Error(r.status); return r.json(); }
async function subjectData(g, sid) {
  const k = `g${g}/${sid}`; if (k in DATA) return DATA[k];
  try { DATA[k] = await loadJSON(`content/${k}.json`); } catch (e) { DATA[k] = null; }
  return DATA[k];
}
const curSubjects = g => { const all = CUR?.grades?.[g]?.subjects || []; const mine = g >= 11 && ST.profile?.subjects;
  return mine && mine.length ? all.filter(s => mine.includes(s.id)) : all; };
/* ---------- Grades 11–12: pick a stream, then subjects ---------- */
const STREAMS = [{ id: 'science', e: '🔬', n: 'Science', d: 'Physics, Chemistry, Maths / Biology' }, { id: 'commerce', e: '📈', n: 'Commerce', d: 'Accountancy, Business Studies, Economics' }, { id: 'arts', e: '🎨', n: 'Arts / Humanities', d: 'History, Political Science, Geography, Psychology, Sociology' }];
function pickStream(g, done, back) {
  show('onboard'); const el = $('#s-onboard');
  el.innerHTML = `<div class="ob"><div class="ob-hero">🧭</div><h1>Grade ${g}: pick your stream</h1>
    <div class="card">${STREAMS.map(s => `<button class="choice stream" data-s="${s.id}"><b>${s.e} ${s.n}</b><small>${s.d}</small></button>`).join('')}</div>
    ${back ? '<button class="btn ghost" id="stBack">← Back</button>' : ''}</div>`;
  el.querySelectorAll('.stream').forEach(b => b.onclick = () => { sfx('tap'); pickSubjects(g, b.dataset.s, done, back); });
  if (back) $('#stBack').onclick = back;
}
function pickSubjects(g, stream, done, back) {
  const all = CUR?.grades?.[g]?.subjects || [], st = CUR?.streams?.[stream] || { core: [], optional: [] };
  const list = all.filter(s => st.core.includes(s.id) || st.optional.includes(s.id));
  let sel = new Set(st.core.filter(id => all.some(s => s.id === id)));
  if (stream === 'science') sel.delete('biology');          // PCM by default; tap to add Biology (PCB / PCMB)
  const el = $('#s-onboard');
  const draw = () => {
    el.innerHTML = `<div class="ob"><div class="ob-hero">🎒</div><h1>Your subjects</h1><p class="sub" style="color:#fff">Tap to add or remove. You can change this later in Me.</p>
      <div class="card">${list.map(s => { const sty = Worlds.SUBJECT_STYLE[s.id] || { e: '📘' }; return `<button class="choice subj ${sel.has(s.id) ? 'sel' : ''}" data-id="${s.id}"><b>${sty.e} ${esc(s.name)}</b>${st.optional.includes(s.id) ? '<small>optional</small>' : ''}</button>`; }).join('')}</div>
      <button class="btn" id="sjGo" ${sel.size ? '' : 'disabled'}>Continue ▶</button><div style="height:8px"></div><button class="btn ghost" id="sjBack">← Back</button></div>`;
    el.querySelectorAll('.subj').forEach(b => b.onclick = () => { const id = b.dataset.id; sel.has(id) ? sel.delete(id) : sel.add(id); sfx('tap'); draw(); });
    $('#sjGo').onclick = () => done(stream, list.map(s => s.id).filter(id => sel.has(id)));
    $('#sjBack').onclick = () => pickStream(g, done, back);
  };
  draw();
}
const topicStars = id => ST.topics[id]?.stars || 0;
function subjectPct(d) { if (!d) return 0; let t = 0, n = 0; d.chapters.forEach(c => c.topics.forEach(tp => { n++; if (topicStars(tp.id)) t++; })); return n ? t / n * 100 : 0; }
const chapterDone = c => c.topics.every(t => topicStars(t.id) > 0);

/* ================= Onboarding ================= */
function onboard(step = 1, draft = {}) {
  show('onboard');
  const el = $('#s-onboard');
  if (step === 1) {
    el.innerHTML = `<div class="ob"><div class="ob-hero bob">🌏</div><h1>Welcome to <span>StudyVerse</span></h1><p>Every subject is a game. Every grade is a new world.</p>
      <div class="card"><h3>Which board is your school?</h3><div class="grid2">${BOARDS.map(b => `<button class="choice ${b.live ? '' : 'off'}" data-b="${b.id}">${b.name}${b.live ? '' : '<small>coming soon</small>'}</button>`).join('')}</div></div></div>`;
    el.querySelectorAll('.choice').forEach(b => b.onclick = () => { if (b.classList.contains('off')) { toast('Coming soon! Start with CBSE for now.'); return; } sfx('tap'); onboard(2, { ...draft, board: b.dataset.b }); });
  } else if (step === 2) {
    el.innerHTML = `<div class="ob"><div class="ob-hero">🎒</div><h1>Which grade are you in?</h1>
      <div class="card"><div class="grid5">${Array.from({ length: MAX_GRADE }, (_, i) => `<button class="choice big" data-g="${i + 1}"><b>${i + 1}</b><small>${Worlds.THEMES[i + 1].name}</small></button>`).join('')}</div></div>
      <button class="btn ghost" id="obBack">← Back</button></div>`;
    el.querySelectorAll('.choice').forEach(b => b.onclick = () => { sfx('tap'); const g = +b.dataset.g;
      if (g >= 11) pickStream(g, (stream, subjects) => onboard(3, { ...draft, grade: g, stream, subjects }), () => onboard(2, draft));
      else onboard(3, { ...draft, grade: g, stream: null, subjects: null }); });
    $('#obBack').onclick = () => onboard(1, draft);
  } else {
    el.innerHTML = `<div class="ob"><div class="ob-hero">😊</div><h1>Pick your hero</h1>
      <div class="card"><div class="grid6">${AVATARS.map((a, i) => `<button class="choice av ${i === 0 ? 'sel' : ''}" data-a="${a}">${a}</button>`).join('')}</div>
      <input id="obName" maxlength="20" placeholder="Your first name" autocomplete="off"></div>
      <button class="btn" id="obGo">Enter my world ▶</button><div style="height:8px"></div><button class="btn ghost" id="obBack">← Back</button></div>`;
    let av = AVATARS[0];
    el.querySelectorAll('.av').forEach(b => b.onclick = () => { el.querySelectorAll('.av').forEach(x => x.classList.remove('sel')); b.classList.add('sel'); av = b.dataset.a; sfx('tap'); });
    $('#obBack').onclick = () => onboard(2, draft);
    $('#obGo').onclick = () => {
      const name = $('#obName').value.trim() || 'Explorer';
      ST.profile = { ...draft, name, avatar: av }; save(); sfx('unlock');
      setGrade(draft.grade); worldScreen();
    };
  }
}
function setGrade(g) { ST.profile.grade = g; save(); if (typeof SND !== 'undefined') { SND.myGrade = g; if (SND.playing && SND.choice === 'auto') startMusic(); } }

/* ================= Grade world ================= */
async function worldScreen() {
  show('world', 'world'); NAV = {};
  const g = ST.profile.grade, subs = curSubjects(g), th = Worlds.THEMES[g];
  $('#worldTitle').innerHTML = `${esc(ST.profile.avatar)} Hi ${esc(ST.profile.name)}! <small>Grade ${g} · ${esc(th.name)}</small>`;
  const map = $('#map'); map.classList.toggle('dark', !!th.dark);
  if (!subs.length) { map.innerHTML = `<div class="empty">Syllabus for Grade ${g} is loading soon.</div>`; return; }
  const datas = await Promise.all(subs.map(s => subjectData(g, s.id)));
  let curSet = false; let total = 0, done = 0;
  const nodes = subs.map((s, i) => {
    const d = datas[i], st = Worlds.SUBJECT_STYLE[s.id] || { e: '📘', c: '#ffc93c' }, pct = subjectPct(d);
    if (d) d.chapters.forEach(c => c.topics.forEach(t => { total++; if (topicStars(t.id)) done++; }));
    let state = !d ? 'soon' : pct >= 100 ? 'done' : 'open';
    if (state === 'open' && !curSet) { state = 'current'; curSet = true; }
    return { title: s.name, sub: d ? `${d.chapters.length} chapters` : (s.book || ''), emoji: st.e, color: st.c, state, pct };
  });
  $('#hudPct').textContent = total ? Math.round(done / total * 100) + '%' : '0%';
  $('#hudBar').style.width = (total ? done / total * 100 : 0) + '%';
  $('#hudName').textContent = `Grade ${g} journey`;
  Worlds.render(map, g, nodes, 'grade', i => {
    const s = subs[i];
    if (!datas[i]) { sfx('hmm'); toast(`${s.name} is being built — coming soon!`); return; }
    sfx('open'); subjectScreen(s.id);
  });
}

/* ================= Subject: chapter path ================= */
async function subjectScreen(sid) {
  const g = ST.profile.grade, d = await subjectData(g, sid), meta = curSubjects(g).find(s => s.id === sid);
  if (!d) return worldScreen();
  NAV = { subject: sid };
  show('subject', 'world');
  $('#subTitle').innerHTML = `${esc((Worlds.SUBJECT_STYLE[sid] || {}).e || '📘')} ${esc(meta?.name || sid)} <small>${esc(meta?.book || '')}</small>`;
  let curSet = false;
  const nodes = d.chapters.map(c => {
    const dn = chapterDone(c); let state = dn ? 'done' : 'open';
    if (!dn && !curSet) { state = 'current'; curSet = true; }
    const st = c.topics.length ? Math.round(c.topics.reduce((a, t) => a + topicStars(t.id), 0) / c.topics.length) : 0;
    return { title: c.title, sub: `${c.topics.length} quests`, emoji: c.emoji || '📘', color: (Worlds.SUBJECT_STYLE[sid] || {}).c || '#ffc93c', state, stars: st, num: c.n };
  });
  const map = $('#cmap'); map.classList.toggle('dark', !!Worlds.THEMES[g].dark);
  Worlds.render(map, g, nodes, 'chapter', i => { sfx('open'); chapterScreen(sid, i); });
}

/* ================= Chapter: list of topic quests ================= */
async function chapterScreen(sid, ci) {
  const g = ST.profile.grade, d = await subjectData(g, sid), c = d.chapters[ci];
  NAV = { subject: sid, chapter: ci };
  show('chapter', 'world');
  const el = $('#s-chapter');
  el.innerHTML = `<button class="back" id="chBack">← Chapters</button>
    <div class="card chead"><div class="cemoji">${esc(c.emoji || '📘')}</div><div><span class="tag">Chapter ${c.n}</span><h2>${esc(c.title)}</h2></div></div>
    ${c.topics.map((t, ti) => { const s = topicStars(t.id); return `<button class="tcard ${s ? 'done' : ''}" data-t="${ti}">
      <div class="tnum">${s ? '✓' : ti + 1}</div><div class="tbody"><b>${esc(t.title)}</b><span>${esc(t.learn?.hook || '')}</span></div>
      <div class="tstars">${window.Garden ? Garden.badge(t.id) : ''}${'⭐'.repeat(s)}${'☆'.repeat(3 - s)}</div></button>`; }).join('')}`;
  $('#chBack').onclick = () => subjectScreen(sid);
  el.querySelectorAll('.tcard').forEach(b => b.onclick = () => { sfx('open'); playTopic(sid, ci, +b.dataset.t); });
}

/* ================= Topic player: Learn → Play → Quiz → Teach → Done ================= */
let RUN = null;
async function playTopic(sid, ci, ti) {
  const g = ST.profile.grade, d = await subjectData(g, sid), c = d.chapters[ci], t = c.topics[ti];
  NAV = { subject: sid, chapter: ci, topic: ti };
  const steps = [{ k: 'learn', label: 'Learn' }, ...(t.games || []).map((gm, i) => ({ k: 'game', i, label: 'Play' })), { k: 'quiz', label: 'Quiz' }, { k: 'teach', label: 'Teach' }];
  RUN = { sid, ci, ti, t, c, steps, at: 0, quiz: { right: 0, total: 0, mistakes: [] }, gameScore: [0, 0], taught: false };
  show('topic');
  renderStep();
}
function stepBar() {
  const seen = new Set(); const pills = RUN.steps.map((s, i) => { const lab = s.label; const show = !seen.has(lab) || s.k !== 'game'; seen.add(lab); return { lab, i, show }; });
  return `<div class="tbar"><button class="x" id="tClose">✕</button><div class="pills">${RUN.steps.map((s, i) => `<i class="${i < RUN.at ? 'done' : i === RUN.at ? 'on' : ''}"></i>`).join('')}</div><span class="stepname">${RUN.steps[RUN.at]?.label || 'Done'}</span></div>`;
}
function nextStep() { RUN.at++; renderStep(); }
function renderStep() {
  unmount3D(); if ('speechSynthesis' in window) speechSynthesis.cancel();
  const el = $('#s-topic'); const s = RUN.steps[RUN.at];
  el.innerHTML = stepBar() + `<div id="stepBody"></div>`;
  $('#tClose').onclick = () => { unmount3D(); chapterScreen(RUN.sid, RUN.ci); };
  const b = $('#stepBody');
  if (!s) return doneStep(b);
  if (s.k === 'learn') learnStep(b);
  else if (s.k === 'game') { b.innerHTML = `<div class="card game" id="gbox"></div>`; Games.play($('#gbox'), RUN.t.games[s.i], (r, tot) => { RUN.gameScore[0] += r; RUN.gameScore[1] += tot; addXP(Math.max(5, r * 2)); nextStep(); }); }
  else if (s.k === 'quiz') quizRunner(b, RUN.t.quiz.map((q, i) => ({ q, qid: `${RUN.t.id}#${i}` })), res => { RUN.quiz = res; nextStep(); });
  else if (s.k === 'teach') teachStep(b);
  window.scrollTo(0, 0);
}

function learnStep(b) {
  const L = RUN.t.learn || {}, t = RUN.t;
  b.innerHTML = `<div class="card"><span class="tag">${esc(RUN.c.title)}</span><h2>${esc(t.title)}</h2>
      <div class="pet"><div class="face">🐣</div><div class="bubble">${esc(L.hook || '')} ${spk(L.hook || '')}</div></div></div>
    <div class="card labcard"><h3>🧪 Try it yourself</h3><div id="s3d" class="s3dhost"></div></div>
    <div class="card"><h3>💡 Big ideas</h3>${(L.points || []).map((p, i) => `<div class="point popin" style="animation-delay:${(i * .25).toFixed(2)}s"><span class="ra-skip">${i + 1}</span><div>${esc(p)} ${spk(p)}</div></div>`).join('')}</div>
    
    ${L.example ? `<div class="card"><h3>🧠 Watch me solve</h3><div class="exq">${esc(L.example.q)} ${spk(L.example.q)}</div><div id="exSteps"></div>
      <button class="btn ghost" id="exBtn">Show step 1</button></div>` : ''}
    ${L.reallife ? `<div class="reallife card">🌍 <b>In real life:</b> ${esc(L.reallife)}</div>` : ''}
    ${window.Gen && Gen.has(t.id, t.title, ST.profile.grade, NAV.subject) ? '<button class="btn ghost" id="genGo">♾️ Endless practice</button><div style="height:8px"></div>' : ''}
    <button class="btn mint" id="learnGo">${RUN.t.games?.length ? "Let's play ▶" : 'Start quiz ▶'}</button>`;
  mount3D($('#s3d'), t, RUN.c);
  if (L.example) {
    const st = L.example.steps || []; let k = 0; const box = $('#exSteps'), btn = $('#exBtn');
    const reveal = () => {
      if (k < st.length) { box.insertAdjacentHTML('beforeend', `<div class="exstep popin">${k + 1}. ${esc(st[k])}</div>`); k++; sfx('tap'); btn.textContent = k < st.length ? `Show step ${k + 1}` : 'Show answer'; }
      else { box.insertAdjacentHTML('beforeend', `<div class="exans popin">✅ ${esc(L.example.answer)}</div>`); btn.remove(); sfx('coin'); }
    };
    if (!st.length) btn.textContent = 'Show answer';
    btn.onclick = reveal;
  }
  $('#learnGo').onclick = () => { addXP(5); nextStep(); };
  if ($('#genGo')) $('#genGo').onclick = () => Gen.open($('#stepBody'), t, { onExit: renderStep });
}

/* ---------- Quiz with animated explanation after every answer ---------- */
function quizRunner(b, list, done) {
  if (!$('#s-topic').classList.contains('active')) Nav.sub();      // Back leaves the quiz and returns to the screen it started from
  let i = 0, right = 0; const mistakes = [], hist = [];
  ST.bm = ST.bm || {};
  const bmBtn = qid => `<button class="tst-ic qbm ${ST.bm[qid] ? 'on' : ''}" data-q="${esc(qid)}" aria-label="Bookmark this question">🔖</button>`;
  const wireBm = () => b.querySelectorAll('.qbm').forEach(x => x.onclick = () => { const id = x.dataset.q; if (ST.bm[id]) delete ST.bm[id]; else ST.bm[id] = today(); save(); x.classList.toggle('on', !!ST.bm[id]); toast(ST.bm[id] ? '🔖 Bookmarked' : 'Bookmark removed'); });
  const review = j => {   /* read-only look back at an answered question */
    const { q, qid } = list[j], h = hist[j];
    b.innerHTML = `<div class="card"><div class="tst-top"><span class="tag">Question ${j + 1} of ${list.length} · review</span>${bmBtn(qid)}</div>
      <h2 class="qtext">${esc(q.q)} ${spk(q.q, 1)}</h2><div>${h.order.map(k => `<button class="opt ${k === q.answer ? 'right' : k === h.k ? 'wrong' : ''}" disabled>${esc(q.options[k])}</button>`).join('')}</div>
      <div class="explain ${h.ok ? 'good' : 'bad'}"><div class="why">${esc(q.explain)} ${spk(q.explain)}</div>${(q.steps || []).map((s, n) => `<div class="exstep">${n + 1}. ${esc(s)}</div>`).join('')}</div>
      <div class="tst-nav"><button class="btn ghost" id="rvPrev" ${j ? '' : 'disabled'}>◀ Previous</button><button class="btn" id="rvBack">Back to question ${i + 1} ▶</button></div></div>`;
    wireBm(); $('#rvPrev').onclick = () => j && review(j - 1); $('#rvBack').onclick = () => (hist[i] ? review(i) : render());
    if (hist[i] && j === i) $('#rvBack').textContent = 'Continue ▶', $('#rvBack').onclick = () => { const nx = i < list.length - 1; i++; nx ? render() : done({ right, total: list.length, mistakes }); };
  };
  const render = () => {
    const { q, qid } = list[i];
    const order = Games.shuffle(q.options.map((o, k) => k));
    b.innerHTML = `<div class="card"><div class="tst-top"><span class="tag">Question ${i + 1} of ${list.length}</span>${i ? '<button class="tst-ic" id="qPrev" aria-label="See previous question">◀</button>' : ''}${bmBtn(qid)}</div><div class="progress"><i style="width:${i / list.length * 100}%"></i></div>
      <h2 class="qtext">${esc(q.q)} ${spk(q.q, 1)}</h2><div id="qo">${order.map(k => `<button class="opt" data-k="${k}">${esc(q.options[k])}</button>`).join('')}</div><div id="qx"></div></div>`;
    wireBm(); const qp = $('#qPrev'); if (qp) qp.onclick = () => review(i - 1);
    b.querySelectorAll('.opt').forEach(btn => btn.onclick = () => {
      const k = +btn.dataset.k, ok = k === q.answer; hist[i] = { order, k, ok };
      b.querySelectorAll('.opt').forEach(x => { x.disabled = true; if (+x.dataset.k === q.answer) x.classList.add('right'); });
      const qs = ST.qstats[qid] || { s: 0, w: 0 }; qs.s++;
      if (ok) { right++; sfx('correct'); addXP(10); }
      else { btn.classList.add('wrong'); sfx('wrong'); qs.w++; mistakes.push(q.mistake); ST.mistakes[q.mistake] = (ST.mistakes[q.mistake] || 0) + 1; }
      ST.qstats[qid] = qs; save();
      const box = $('#qx');
      const draw = () => {
        box.innerHTML = `<div class="explain ${ok ? 'good' : 'bad'}"><div class="verdict">${ok ? '🎉 Correct!' : `🤔 Not quite — it's <b>${esc(q.options[q.answer])}</b>`}</div>
          ${q.visual ? `<div class="vis">${Visual.render(q.visual)}</div>` : `<div class="bigans popin">${esc(q.options[q.answer])}</div>`}
          <div class="why">${esc(q.explain)} ${spk(q.explain)}</div>
          ${(q.steps || []).map((s, j) => `<div class="exstep popin" style="animation-delay:${(.4 + j * .45).toFixed(2)}s">${j + 1}. ${esc(s)}</div>`).join('')}</div>
          <div class="xrow">${q.visual ? '<button class="btn ghost" id="rep">🔁 Replay</button>' : ''}${RUN ? '<button class="btn ghost" id="try3d" onclick="open3D()">🧪 Try it</button>' : ''}${i ? '<button class="btn ghost" id="nxPrev" aria-label="Previous question">◀</button>' : ''}<button class="btn mint" id="nx">${i < list.length - 1 ? 'Next ▶' : 'Finish ▶'}</button></div>`;
        const np = $('#nxPrev'); if (np) np.onclick = () => review(i - 1);
        const rep = $('#rep'); if (rep) rep.onclick = draw;
        if (RUN) labFor(RUN.t, RUN.c).then(sp => { const t = $('#try3d'); if (t && !sp) t.remove(); });
        $('#nx').onclick = () => { i++; if (i < list.length) render(); else done({ right, total: list.length, mistakes }); };
        setTimeout(() => box.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 120);
      };
      draw();
    });
  };
  render();
}

/* ---------- Teach Gappu ---------- */
function teachStep(b) {
  const T = RUN.t.teach || {};
  b.innerHTML = `<div class="card"><span class="tag">Teach to learn</span><div class="pet"><div class="face" id="gf">🐣</div><div class="bubble" id="gs">${esc(T.ask)} ${spk(T.ask)}</div></div>
    <textarea id="ans" placeholder="Explain in your own words…"></textarea><button class="btn" id="tBtn">Explain to Gappu 💬</button>
    <div style="height:8px"></div><button class="btn ghost" id="tSkip">Skip for now</button></div>`;
  let tries = 0;
  $('#tSkip').onclick = nextStep;
  $('#tBtn').onclick = () => {
    const norm = t => String(t).toLowerCase().replace(/×/g, 'x').replace(/÷/g, '/').replace(/−/g, '-').replace(/\s+/g, ' ');
    const txt = norm($('#ans').value); tries++;
    const hasWord = w => { w = norm(w).trim(); if (!w) return false;
      if (/[^\x00-\x7f]/.test(w)) return txt.includes(w); // Hindi/Sanskrit: match inside text
      const e = w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); return new RegExp(`(^|[^a-z0-9])${e}(s|es)?([^a-z0-9]|$)`).test(txt); };
    const miss = (T.must || []).filter(grp => !grp.some(hasWord));
    const f = $('#gf'), s = $('#gs');
    if (txt.trim().length < 6) { f.textContent = '🐣'; s.textContent = 'Hmm, tell me a little more please! 🥺'; return; }
    if (!miss.length) {
      f.textContent = '🐥'; s.textContent = T.praise; sfx('correct');
      if (!RUN.taught) { RUN.taught = true; addXP(25, 'Gappu learned from you!'); }
      $('#tBtn').textContent = 'Finish ▶'; $('#tBtn').onclick = nextStep; $('#tSkip').remove();
    } else {
      f.textContent = '🤔'; sfx('hmm');
      s.textContent = T.nudge + (tries >= 2 ? `  (Hint: try talking about “${miss[0][0]}”)` : '');
    }
  };
}

function doneStep(b) {
  const q = RUN.quiz, pct = q.total ? q.right / q.total : 0;
  const stars = pct >= .9 ? 3 : pct >= .7 ? 2 : pct >= .4 ? 1 : 1;
  const prev = ST.topics[RUN.t.id]?.stars || 0;
  ST.topics[RUN.t.id] = { stars: Math.max(prev, stars), last: today() }; bumpStreak(); save();
  if (window.Garden) Garden.learned(RUN.t.id, pct);
  sfx('unlock');
  const uniq = [...new Set(q.mistakes)];
  const c = RUN.c, nextTi = RUN.ti + 1 < c.topics.length ? RUN.ti + 1 : null;
  b.innerHTML = `<div class="card done-card"><div class="confetti">${Array.from('🎉⭐✨🎊🌟'.repeat(4)).map((e, i) => `<span style="left:${(i * 37) % 100}%;animation-delay:${(i % 7) * .12}s">${e}</span>`).join('')}</div>
    <h2>Quest complete!</h2><div class="bigstars">${[0, 1, 2].map(i => `<span class="${i < stars ? 'on' : ''}" style="animation-delay:${i * .25}s">⭐</span>`).join('')}</div>
    <p class="sub">Quiz: ${q.right} of ${q.total} correct${RUN.taught ? ' · You taught Gappu 🐥' : ''}</p>
    ${uniq.length ? `<h3>🧬 Your Mistake DNA</h3><p class="sub">We'll bring these back in Practice until they're fixed.</p>${uniq.map(m => `<div class="dna">🔍 ${esc(m)}</div>`).join('')}` : '<p class="sub">No mistakes. Superstar! 🌟</p>'}
    <div id="dRev"></div><div style="height:12px"></div><div id="dExtra"></div>
    ${nextTi !== null ? `<button class="btn" id="dNext">Next quest: ${esc(c.topics[nextTi].title)} ▶</button><div style="height:8px"></div>` : ''}
    <button class="btn ghost" id="dBack">Back to chapter</button></div>`;
  if (nextTi !== null) $('#dNext').onclick = () => playTopic(RUN.sid, RUN.ci, nextTi);
  $('#dBack').onclick = () => chapterScreen(RUN.sid, RUN.ci);
  if (window.Garden) Garden.doneExtra($('#dExtra'));
  if (window.Tests) $('#dRev').innerHTML = `<h3 style="margin-top:14px">📝 Your revision card</h3>` + Tests.revCard(RUN.t);
}

/* ================= Practice: daily mix that targets mistakes ================= */
async function practiceScreen() {
  show('practice', 'practice');
  const el = $('#s-practice'), g = ST.profile.grade;
  const subs = curSubjects(g); const pool = [];
  for (const s of subs) { const d = await subjectData(g, s.id); if (!d) continue;
    d.chapters.forEach(c => c.topics.forEach(t => { if (!topicStars(t.id)) return; t.quiz.forEach((q, i) => { const qid = `${t.id}#${i}`, st = ST.qstats[qid] || { s: 0, w: 0 }; pool.push({ q, qid, wgt: 1 + st.w * 4 - Math.min(st.s, 3) * .2 }); }); })); }
  if (!pool.length) { el.innerHTML = `<div class="card"><h2>🎯 Daily Practice</h2><p class="sub">Finish your first quest and your daily practice mix appears here. It brings back the questions you found tricky until you master them.</p><button class="btn" id="pGo">Go to my world ▶</button></div>`; $('#pGo').onclick = worldScreen; return; }
  pool.sort((a, b) => b.wgt + Math.random() * 2 - (a.wgt + Math.random() * 2));
  const list = pool.slice(0, 10);
  const top = Object.entries(ST.mistakes).sort((a, b) => b[1] - a[1]).slice(0, 3);
  el.innerHTML = `<div class="card"><h2>🎯 Daily Practice</h2><p class="sub">${list.length} questions picked for you — tricky ones come first.</p>
    ${top.length ? `<h3>🧬 Fixing now</h3>${top.map(([m, n]) => `<div class="dna">🔍 ${esc(m)} <small>×${n}</small></div>`).join('')}` : ''}
    <div style="height:10px"></div><button class="btn" id="pStart">Start practice ▶</button></div><div id="pBody"></div>`;
  $('#pStart').onclick = () => { el.querySelector('.card').remove(); quizRunner($('#pBody'), list, r => {
    bumpStreak(); sfx('unlock');
    $('#pBody').innerHTML = `<div class="card done-card"><h2>Practice done! 💪</h2><p class="sub">${r.right} of ${r.total} correct. Come back tomorrow to keep your 🔥 streak.</p><button class="btn" id="pAgain">Another round</button></div>`;
    $('#pAgain').onclick = practiceScreen; }); };
}

/* ================= Squad (sample league until logins arrive) ================= */
function squadScreen() {
  show('squad', 'squad');
  const mates = [{ n: 'Aarav', e: '🐯', x: 420 }, { n: 'Diya', e: '🦊', x: 360 }, { n: 'Kabir', e: '🐼', x: 210 }, { n: 'Meera', e: '🐨', x: 140 }];
  const list = [...mates, { n: ST.profile.name + ' (you)', e: ST.profile.avatar, x: ST.xp, me: true }].sort((a, b) => b.x - a.x);
  const us = mates.reduce((s, m) => s + m.x, 0) + ST.xp, them = 1450;
  $('#s-squad').innerHTML = `<div class="card"><span class="tag">This week · School league</span>
    <div class="vs"><div><div class="big">🦁</div>Team Lions<br>${us} XP</div><div class="big">VS</div><div><div class="big">🦅</div>Team Eagles<br>${them} XP</div></div>
    <div class="bar2"><i style="width:${us / (us + them) * 100}%"></i></div><p class="sub" style="text-align:center">${us >= them ? '🎉 Lions are winning!' : `Lions need ${them - us} more XP!`}</p></div>
    <div class="card"><h3>🦁 Team Lions</h3>${list.map((m, i) => `<div class="row ${m.me ? 'me' : ''}"><div class="rank">${i + 1}</div><div class="av">${m.e}</div><div class="nm">${esc(m.n)}</div><div class="xp">${m.x} ⭐</div></div>`).join('')}</div>
    <p class="note">Sample squad. Real friends and school leagues arrive with logins.</p>`;
}

/* ================= Me / settings ================= */
function meScreen() {
  show('me', 'me');
  const p = ST.profile, done = Object.keys(ST.topics).length;
  $('#s-me').innerHTML = `<div class="card mecard"><div class="meav">${esc(p.avatar)}</div><div><h2>${esc(p.name)}</h2><p class="sub">Grade ${p.grade} · ${BOARDS.find(b => b.id === p.board)?.name || 'CBSE'}</p></div></div>
    <div class="card statrow"><div><b>${ST.xp}</b><span>XP</span></div><div><b>${ST.streak.n || 0}🔥</b><span>Streak</span></div><div><b>${done}</b><span>Quests</span></div></div>
    <div class="card"><h3>Change grade</h3><div class="grid5">${Array.from({ length: MAX_GRADE }, (_, i) => `<button class="choice ${p.grade === i + 1 ? 'sel' : ''}" data-g="${i + 1}"><b>${i + 1}</b></button>`).join('')}</div></div>
    <div class="card"><button class="btn ghost" onclick="openSound()">🎵 Sound & music</button><div style="height:8px"></div><button class="btn ghost" id="meReset">Start over</button></div>`;
  const go = g => { setGrade(g); sfx('unlock'); toast(`Welcome to ${Worlds.THEMES[g].name}!`); worldScreen(); };
  $('#s-me').querySelectorAll('.choice').forEach(b => b.onclick = () => { const g = +b.dataset.g;
    if (g >= 11) pickStream(g, (stream, subjects) => { ST.profile.stream = stream; ST.profile.subjects = subjects; save(); go(g); }, meScreen); else go(g); });
  if (p.grade >= 11) { const c = $('#s-me .grid5').closest('.card'); c.insertAdjacentHTML('afterend', `<div class="card"><h3>Stream & subjects</h3><p class="sub">${esc((STREAMS.find(x => x.id === p.stream) || {}).n || '')} · ${(p.subjects || []).length} subjects</p><button class="btn ghost" id="meStream">Change stream or subjects</button></div>`);
    $('#meStream').onclick = () => pickStream(p.grade, (stream, subjects) => { ST.profile.stream = stream; ST.profile.subjects = subjects; save(); worldScreen(); }, meScreen); }
  $('#meReset').onclick = () => { if ($('#meReset').dataset.sure) { localStorage.removeItem('sv_state'); location.reload(); } else { $('#meReset').dataset.sure = 1; $('#meReset').textContent = 'Tap again to erase all progress'; } };
}

/* ================= Angle lab (interactive) ================= */
function angleLab(host) {
  host.innerHTML = `<svg class="labsvg" viewBox="0 0 320 240"><path class="arc" fill="rgba(139,92,246,.18)" stroke="#8b5cf6" stroke-width="3"/>
    <line x1="160" y1="140" x2="290" y2="140" stroke="#1b1f3a" stroke-width="5" stroke-linecap="round"/><line class="ray" x1="160" y1="140" stroke="#1b1f3a" stroke-width="5" stroke-linecap="round"/>
    <circle cx="160" cy="140" r="7" fill="#1b1f3a"/><circle class="knob" r="17" fill="#ffc93c" stroke="#1b1f3a" stroke-width="3"/></svg>
    <div class="readout"><div class="deg"></div><div class="type"></div></div>`;
  const svg = host.querySelector('svg'), O = { x: 160, y: 140 }, R = 95; let drag = false, last = 45;
  const kinds = [[89.5, 'Acute', '#2ed3a5'], [90.5, 'Right', '#3b82f6'], [179.5, 'Obtuse', '#ff9f43'], [180.5, 'Straight', '#8b5cf6'], [359.5, 'Reflex', '#ff6b6b'], [361, 'Full turn', '#1b1f3a']];
  const draw = a => { const r = a * Math.PI / 180;
    host.querySelector('.knob').setAttribute('cx', O.x + R * Math.cos(r)); host.querySelector('.knob').setAttribute('cy', O.y - R * Math.sin(r));
    host.querySelector('.ray').setAttribute('x2', O.x + 130 * Math.cos(r)); host.querySelector('.ray').setAttribute('y2', O.y - 130 * Math.sin(r));
    const ex = O.x + 34 * Math.cos(r), ey = O.y - 34 * Math.sin(r);
    host.querySelector('.arc').setAttribute('d', `M${O.x},${O.y} L${O.x + 34},${O.y} A34,34 0 ${a > 180 ? 1 : 0} 0 ${ex},${ey} Z`);
    const k = kinds.find(k => a <= k[0]); host.querySelector('.deg').textContent = Math.round(a) + '°'; const ty = host.querySelector('.type'); ty.textContent = k[1]; ty.style.background = k[2]; };
  const move = e => { if (!drag) return; e.preventDefault(); const b = svg.getBoundingClientRect(); const p = { x: (e.clientX - b.left) * 320 / b.width, y: (e.clientY - b.top) * 240 / b.height };
    let a = Math.atan2(O.y - p.y, p.x - O.x) * 180 / Math.PI; if (a < 0) a += 360; if (last > 300 && a < 60) a = 360; if (last < 60 && a > 300) a = 0; [90, 180].forEach(s => { if (Math.abs(a - s) < 3) a = s; }); if (a < 1) a = 1; last = a; draw(a); };
  svg.addEventListener('pointerdown', e => { drag = true; svg.setPointerCapture(e.pointerId); move(e); });
  svg.addEventListener('pointermove', move); svg.addEventListener('pointerup', () => drag = false);
  draw(45);
}

/* ================= Install as an app ================= */
let deferredPrompt = null;
const isStandalone = () => window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
const inFrame = (() => { try { return window.self !== window.top; } catch (e) { return true; } })();
function showInstall() { if (isStandalone() || inFrame) return; try { if (sessionStorage.getItem('sv_noinst')) return; } catch (e) {} $('#installBar').style.display = 'flex'; }
function hideInstall() { $('#installBar').style.display = 'none'; try { sessionStorage.setItem('sv_noinst', '1'); } catch (e) {} }
window.addEventListener('beforeinstallprompt', e => { e.preventDefault(); deferredPrompt = e; showInstall(); });
window.addEventListener('appinstalled', () => { $('#installBar').style.display = 'none'; deferredPrompt = null; toast('🎉 StudyVerse installed!'); sfx('unlock'); });
async function installApp() {
  if (deferredPrompt) { deferredPrompt.prompt(); const r = await deferredPrompt.userChoice; deferredPrompt = null; if (r.outcome === 'accepted') $('#installBar').style.display = 'none'; return; }
  $('#instIntro').textContent = isIOS ? 'On iPhone/iPad, install from Safari in 3 taps:' : 'Your browser hides the install button. Do this:';
  $('#instSteps').innerHTML = isIOS ? '<li>Open this page in <b>Safari</b></li><li>Tap the <b>Share</b> button (square with ↑ arrow)</li><li>Tap <b>Add to Home Screen</b> → <b>Add</b></li>'
    : '<li>Open this page in <b>Google Chrome</b></li><li>Tap the <b>⋮</b> menu (top right)</li><li>Tap <b>Install app</b> → <b>Install</b></li>';
  $('#installSheet').classList.add('show');
}
if (!isStandalone() && !inFrame) setTimeout(() => { if (!deferredPrompt) showInstall(); }, 2500);
/* Service worker + updates reaching installed phones: check for a new version on load and whenever the app comes
   back to the screen; when a new worker takes control, reload once (never in a loop; deferred while the student is
   writing or in a test — then it applies the next time the app is reopened). */
if ('serviceWorker' in navigator && !inFrame && (location.protocol === 'https:' || location.hostname === 'localhost')) window.addEventListener('load', () => {
  const hadCtl = !!navigator.serviceWorker.controller; let lastCheck = 0, pending = false, done = false;
  navigator.serviceWorker.register('sw.js').then(reg => {
    const check = () => { if (Date.now() - lastCheck < 60000) return; lastCheck = Date.now(); try { const p = reg.update(); if (p && p.catch) p.catch(() => {}); } catch (e) {} };
    check();
    document.addEventListener('visibilitychange', () => { if (document.visibilityState !== 'visible') return; if (pending) reloadNow(); else check(); });
  }).catch(() => {});
  const busy = () => !!document.querySelector('.ca-pad, .ca-viva, .ca-set, .ca-mbar, .ca-mcq, textarea:focus');
  function reloadNow() {
    if (done) return; let last = 0; try { last = +sessionStorage.getItem('sv_swreload') || 0; } catch (e) {}
    if (Date.now() - last < 20000) return;          // loop guard
    done = true; try { sessionStorage.setItem('sv_swreload', String(Date.now())); } catch (e) {}
    location.reload();
  }
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (!hadCtl || done) return;                    // first install: nothing to refresh
    if (busy()) { pending = true; toast('Update ready — it applies next time you open the app'); } else reloadNow();
  });
});

/* ================= Start ================= */
(async function init() {
  hud();
  try { CUR = await loadJSON('content/curriculum.json'); } catch (e) { CUR = { grades: {} }; }
  if (!ST.profile) onboard(1); else { setGrade(ST.profile.grade); worldScreen(); }
})();
