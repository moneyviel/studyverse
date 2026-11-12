/* ================= Ask Gappu: "Doubts? Ask me" =================
   Answers ONLY from reviewed course content (content/index/gN-<subject>.json, built by tools/build_index.py),
   so every word shown has passed the strict checker and an independent review.
   Arithmetic questions are calculated exactly by the app. Voice input uses the browser's speech recognition. */
(function () {
  const IDX = {};                 // "g6-maths" -> {topics, qa}
  let docs = null, docsKey = '', df = {}, avgLen = 1, lastHits = [];
  const STOP = new Set(('a an the is are was were be been of to in on at for and or but with by from as it its this that these those what which who whom whose why how when where do does did can could should would will shall may might i me my we our you your he she they them their there here than then so if not no yes please tell explain define meaning mean means about give example examples simple simply words word kya hai hain ka ki ke ko se me mein aur ya ye yah woh vah kaise kyon kyu batao samjhao matlab arth').split(' ').concat(['क्या', 'है', 'हैं', 'का', 'की', 'के', 'को', 'से', 'में', 'और', 'या', 'यह', 'वह', 'कैसे', 'क्यों', 'बताओ', 'समझाओ', 'मतलब', 'अर्थ', 'होता', 'होती', 'होते', 'एक']));
  function stem(w) {
    if (/[ऀ-ॿ]/.test(w) || w.length <= 3 || /^\d/.test(w)) return w;
    if (w.endsWith('ies') && w.length > 4) return w.slice(0, -3) + 'y';
    if (w.endsWith('sses')) return w.slice(0, -2);
    if (w.endsWith('ing') && w.length > 5) return w.slice(0, -3);
    if (w.endsWith('ed') && w.length > 4) return w.slice(0, -2);
    if (w.endsWith('es') && w.length > 4 && /(ch|sh|x|ss)es$/.test(w)) return w.slice(0, -2);
    if (w.endsWith('s') && !w.endsWith('ss') && w.length > 3) return w.slice(0, -1);
    return w;
  }
  const toks = s => String(s || '').toLowerCase().replace(/[’']/g, '').split(/[^a-z0-9ऀ-ॿ]+/).filter(w => w && !STOP.has(w)).map(stem);
  const asText = v => Array.isArray(v) ? v.map(asText).join(' ') : (v && typeof v === 'object') ? Object.values(v).map(asText).join(' ') : String(v || '');

  /* course providers: CA, JEE and every future course plug their own checked content in here (Ask.provider) */
  const PROV = [];
  const cur = () => { for (const p of PROV) { try { if (p.active()) return p; } catch (e) {} } return null; };
  let lastProv = null;
  async function loadIndex() {
    const P = cur();
    if (P) {
      const key = 'p:' + P.name + ':' + (P.key ? P.key() : '');
      if (docs && docsKey === key) return;
      let items = []; try { items = await P.load(); } catch (e) { items = []; }
      docs = []; df = {};
      items.forEach(it => { const tf = {}; let len = 0; (it.fields || []).forEach(([txt, w]) => toks(asText(txt)).forEach(t => { tf[t] = (tf[t] || 0) + w; len += w; }));
        const doc = { kind: 't', t: { id: it.id, t: it.title, sn: it.sub, ch: it.ch, P, it }, tf, len: len || 1 }; Object.keys(tf).forEach(t => df[t] = (df[t] || 0) + 1); docs.push(doc); });
      avgLen = docs.reduce((a, d) => a + d.len, 0) / (docs.length || 1); docsKey = key; return;
    }
    const g = ST.profile.grade, subs = curSubjects(g).map(s => s.id), key = g + ':' + subs.join(',');
    if (docs && docsKey === key) return;
    await Promise.all(subs.map(async sid => { const k = `g${g}-${sid}`; if (!IDX[k]) { try { IDX[k] = await (await fetch(`content/index/${k}.json`)).json(); } catch (e) { IDX[k] = { topics: [], qa: [] }; } } }));
    docs = []; df = {};
    const add = (doc, fields) => { const tf = {}; let len = 0; fields.forEach(([txt, w]) => toks(txt).forEach(t => { tf[t] = (tf[t] || 0) + w; len += w; })); doc.tf = tf; doc.len = len || 1; Object.keys(tf).forEach(t => df[t] = (df[t] || 0) + 1); docs.push(doc); };
    const topicById = {};
    subs.forEach(sid => { const ix = IDX[`g${g}-${sid}`]; ix.topics.forEach(t => { topicById[t.id] = t;
      add({ kind: 't', t }, [[t.t, 4], [t.ch, 1], [t.rv && t.rv.summary, 2.5], [t.rv && t.rv.remember, 2], [t.rv && t.rv.focus, 1], [t.p, 1.5], [t.h, .7], [t.ex && t.ex.q, .6], [t.rl, .5]]); });
      ix.qa.forEach(q => { const t = topicById[q.id]; if (t) add({ kind: 'q', q, t }, [[q.q, 2.2], [q.a, 1.5], [q.e, 1]]); }); });
    avgLen = docs.reduce((a, d) => a + d.len, 0) / (docs.length || 1); docsKey = key;
  }
  function search(query) {
    const qt = [...new Set(toks(query))]; if (!qt.length) return [];
    const N = docs.length, k1 = 1.4, b = .75;
    const scored = [];
    for (const d of docs) { let s = 0, hit = 0;
      for (const t of qt) { const f = d.tf[t]; if (!f) continue; hit++; const idf = Math.log(1 + (N - df[t] + .5) / (df[t] + .5)); s += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * d.len / avgLen)); }
      if (s > 0) { s *= (.5 + .5 * hit / qt.length); if (d.kind === 'q') s *= .85; scored.push({ d, s, hit }); } }
    scored.sort((a, b) => b.s - a.s);
    const byTopic = new Map();
    for (const x of scored.slice(0, 80)) { const id = x.d.t.id; const cur = byTopic.get(id) || { t: x.d.t, s: 0, qa: null, qs: 0, hit: 0 };
      if (x.d.kind === 't') cur.s = Math.max(cur.s, x.s); else if (x.s > cur.qs) { cur.qs = x.s; cur.qa = x.d.q; }
      cur.hit = Math.max(cur.hit, x.hit); byTopic.set(id, cur); }
    return [...byTopic.values()].map(v => ({ ...v, score: Math.max(v.s, v.qs) + .3 * Math.min(v.s, v.qs) })).sort((a, b) => b.score - a.score).map(v => ({ ...v, cover: v.hit / qt.length }));
  }

  /* exact arithmetic: digits, + - × ÷ * / ^ ( ) %, "of" */
  function calc(q) {
    let s = String(q).toLowerCase().replace(/what\s+is|calculate|find|=|\?|answer/g, ' ').replace(/×|x(?=\s*\d)/g, '*').replace(/÷/g, '/').replace(/−/g, '-').replace(/,(?=\d{2,3}\b)/g, '').trim();
    s = s.replace(/(\d+(?:\.\d+)?)\s*%\s*of\s*/g, '($1/100)*').replace(/\bof\b/g, '*');
    if (!/^[\d\s+\-*/().^]+$/.test(s) || !/\d\s*[-+*/^]\s*[\d(]/.test(s)) return null;
    let i = 0; const peek = () => s[i], eat = c => { while (s[i] === ' ') i++; if (s[i] === c) { i++; return true; } return false; };
    const num = () => { while (s[i] === ' ') i++; let j = i; while (/[\d.]/.test(s[i] || '')) i++; if (j === i) throw 0; return parseFloat(s.slice(j, i)); };
    const atom = () => { if (eat('(')) { const v = expr(); if (!eat(')')) throw 0; return v; } if (eat('-')) return -atom(); return num(); };
    const pow = () => { let v = atom(); if (eat('^')) v = Math.pow(v, pow()); return v; };
    const term = () => { let v = pow(); for (;;) { if (eat('*')) v *= pow(); else if (eat('/')) { const d = pow(); if (d === 0) throw 0; v /= d; } else return v; } };
    const expr = () => { let v = term(); for (;;) { if (eat('+')) v += term(); else if (eat('-')) v -= term(); else return v; } };
    try { const v = expr(); while (s[i] === ' ') i++; if (i < s.length || !isFinite(v)) return null; return { expr: q.trim(), v: +v.toPrecision(12) }; } catch (e) { return null; }
  }

  /* ---------- UI ---------- */
  let sheet, log, input, rec = null, lang = 'en';
  function build() {
    if (sheet) return;
    document.body.insertAdjacentHTML('beforeend', `<button class="askfab" id="askFab" aria-label="Doubts? Ask Gappu"><span>🐥</span><b>Doubt?</b></button>
      <div class="asksheet" id="askSheet"><div class="ask-in"><div class="ask-head"><div><b>🐥 Doubts? Ask Gappu</b><small>Answers come only from your checked lessons</small></div><button class="ask-x" id="askX" aria-label="Close">✕</button></div>
      <div class="ask-log" id="askLog"></div>
      <div class="ask-bar"><button class="ask-lang" id="askLang" title="Voice language">EN</button><input id="askIn" placeholder="Type or speak your doubt…" autocomplete="off" enterkeyhint="send"><button class="ask-mic" id="askMic" aria-label="Speak">🎤</button><button class="ask-go" id="askGo" aria-label="Ask">➤</button></div></div></div>`);
    sheet = $('#askSheet'); log = $('#askLog'); input = $('#askIn');
    $('#askFab').onclick = open; $('#askX').onclick = close;
    sheet.addEventListener('click', e => { if (e.target === sheet) close(); });
    $('#askGo').onclick = () => ask(input.value);
    input.addEventListener('keydown', e => { if (e.key === 'Enter') ask(input.value); });
    $('#askLang').onclick = () => { lang = lang === 'en' ? 'hi' : 'en'; $('#askLang').textContent = lang === 'en' ? 'EN' : 'हिं'; };
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) $('#askMic').style.display = 'none';
    $('#askMic').onclick = () => {
      if (rec) { rec.stop(); return; }
      try { rec = new SR(); } catch (e) { toast('Voice is not available on this browser'); return; }
      rec.lang = lang === 'en' ? 'en-IN' : 'hi-IN'; rec.interimResults = true; rec.maxAlternatives = 1;
      $('#askMic').classList.add('on'); input.placeholder = lang === 'en' ? 'Listening… speak now' : 'सुन रहा हूँ… बोलो';
      rec.onresult = e => { input.value = Array.from(e.results).map(r => r[0].transcript).join(' '); if (e.results[e.results.length - 1].isFinal) { const v = input.value; setTimeout(() => ask(v), 250); } };
      rec.onerror = ev => { if (ev.error === 'not-allowed') toast('Please allow the microphone to ask by voice'); };
      rec.onend = () => { rec = null; $('#askMic').classList.remove('on'); input.placeholder = 'Type or speak your doubt…'; };
      rec.start();
    };
    hello();
  }
  function hello() {
    const P = cur();
    if (P !== lastProv) { log.innerHTML = ''; lastProv = P; }
    if (log.children.length) return;
    if (P) { log.innerHTML = `<div class="ask-msg bot"><div class="ask-bubble">Hi ${esc((ST.profile?.name || '').split(' ')[0])}! 👋 I'm Gappu. Ask me any doubt from your ${esc(P.label)}. For example: ${P.examples.map(x => `<i>"${esc(x)}"</i>`).join(', ')}. Tap 🎤 to speak.</div></div>`; return; }
    log.innerHTML = `<div class="ask-msg bot"><div class="ask-bubble">Hi ${esc(ST.profile?.name || '')}! 👋 Ask me any doubt from your Grade ${ST.profile?.grade} lessons. For example: <i>"What is photosynthesis?"</i>, <i>"How do I find the area of a triangle?"</i> or <i>"25% of 80"</i>. Tap 🎤 to speak.</div></div>`;
  }
  function open() { build(); hello(); const P = cur(); try { $('#askSheet .ask-head small').textContent = P ? `Answers come only from your checked ${P.label}` : 'Answers come only from your checked lessons'; } catch (e) {} sheet.classList.add('show'); setTimeout(() => input.focus(), 250); loadIndex(); }
  function close() { sheet.classList.remove('show'); try { ReadAlong.stop(); } catch (e) {} }
  const li = (arr) => (arr || []).filter(Boolean).map(x => `<li>${esc(x)}</li>`).join('');
  function card(h, alts) {
    if (h.t.P) { const t = h.t;
      return `<div class="ask-card" data-tid="${esc(t.id)}"><div class="ask-src ra-skip">${esc(t.sn)} · ${esc(t.ch)}</div><h3>${esc(t.t)} <button class="spk" data-ra=".ask-card" aria-label="Read aloud">🔊</button></h3>
        <div class="ask-sec">${t.it.html || ''}</div>${t.it.open ? '<div class="ask-acts ra-skip"><button class="btn ghost ask-open">📖 Open this lesson</button></div>' : ''}
        ${alts.length ? `<div class="ask-alts ra-skip"><small>Not what you meant? Try:</small>${alts.map(a => `<button class="ask-alt" data-tid="${esc(a.t.id)}">${esc(a.t.t)} <i>${esc(a.t.ch || a.t.sn)}</i></button>`).join('')}</div>` : ''}
        <div class="ask-trust ra-skip">✔ From your checked ${esc(t.P.label)}</div></div>`; }
    const t = h.t, rv = t.rv || {}, sty = (Worlds.SUBJECT_STYLE[t.s] || {}).e || '📘';
    const qa = h.qa && h.qs >= h.s * .8 ? h.qa : null;
    return `<div class="ask-card" data-tid="${esc(t.id)}">
      <div class="ask-src ra-skip">${sty} ${esc(t.sn)} · Ch: ${esc(t.ch)}</div><h3>${esc(t.t)} <button class="spk" data-ra=".ask-card" aria-label="Read aloud">🔊</button></h3>
      ${qa ? `<div class="ask-sec"><b>❓ ${esc(qa.q)}</b><p>✅ <b>${esc(qa.a)}</b>${qa.e ? ' — ' + esc(qa.e) : ''}</p></div>` : ''}
      <div class="ask-sec"><b>💡 In simple words</b><p>${esc(rv.summary || (t.p || []).slice(0, 2).join(' '))}</p></div>
      ${(t.p || []).length ? `<div class="ask-sec"><b>🧠 Key points</b><ul>${li(t.p.slice(0, 5))}</ul></div>` : ''}
      ${t.ex && t.ex.q ? `<div class="ask-sec"><b>🔍 Worked example</b><p>${esc(t.ex.q)}</p>${(t.ex.st || []).length ? `<ol>${li(t.ex.st)}</ol>` : ''}<p>👉 <b>${esc(t.ex.a)}</b></p></div>` : ''}
      ${t.rl ? `<div class="ask-sec"><b>🌍 In real life</b><p>${esc(t.rl)}</p></div>` : ''}
      ${(rv.remember || []).length ? `<div class="ask-sec rem"><b>📌 Remember</b><ul>${li(rv.remember)}</ul></div>` : ''}
      ${(rv.traps || []).length ? `<div class="ask-sec trap"><b>⚠️ Watch out</b><ul>${li(rv.traps)}</ul></div>` : ''}
      <div class="ask-acts ra-skip"><button class="btn ghost ask-open">📖 Open this lesson</button></div>
      ${alts.length ? `<div class="ask-alts ra-skip"><small>Not what you meant? Try:</small>${alts.map(a => `<button class="ask-alt" data-tid="${esc(a.t.id)}">${esc(a.t.t)} <i>${esc(a.t.sn)}</i></button>`).join('')}</div>` : ''}
      <div class="ask-trust ra-skip">✔ From your reviewed ${esc(t.sn)} lesson</div></div>`;
  }
  function wire(el, hits) {
    el.querySelectorAll('.ask-open').forEach(b => b.onclick = () => { const t = hits.find(h => h.t.id === b.closest('.ask-card').dataset.tid).t; close(); if (t.P) { try { t.it.open(); } catch (e) {} return; } playTopic(t.s, t.ci, t.ti); });
    el.querySelectorAll('.ask-alt').forEach(b => b.onclick = () => { const h = lastHits.find(x => x.t.id === b.dataset.tid); if (!h) return; const box = document.createElement('div'); box.className = 'ask-msg bot'; box.innerHTML = card(h, []); log.appendChild(box); wire(box, [h]); box.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
  }
  async function ask(raw) {
    const q = String(raw || '').trim(); if (!q) return; input.value = ''; try { ReadAlong.stop(); } catch (e) {}
    log.insertAdjacentHTML('beforeend', `<div class="ask-msg me"><div class="ask-bubble">${esc(q)}</div></div>`);
    const wait = document.createElement('div'); wait.className = 'ask-msg bot'; wait.innerHTML = '<div class="ask-bubble ask-think">🐥 Looking in your lessons<span>.</span><span>.</span><span>.</span></div>'; log.appendChild(wait); wait.scrollIntoView({ behavior: 'smooth' });
    const c = calc(q);
    if (c) { wait.innerHTML = `<div class="ask-card"><div class="ask-src ra-skip">🧮 Calculator</div><h3>${esc(c.expr)} = ${esc(String(c.v))} <button class="spk" data-ra=".ask-card" aria-label="Read aloud">🔊</button></h3><div class="ask-trust ra-skip">✔ Calculated exactly by the app</div></div>`; sfx('correct'); return; }
    await loadIndex();
    const hits = search(q); lastHits = hits;
    const top = hits[0];
    if (!top || top.cover < .5 || top.score < 2.2) {
      wait.innerHTML = `<div class="ask-card"><h3>🤔 I couldn't find that in your ${cur() ? esc(cur().label) : `Grade ${ST.profile.grade} lessons`} yet.</h3><p class="sub">I only answer from checked lessons, so I won't guess. Try other words, or ask about a topic from your books.</p>
        ${hits.length ? `<div class="ask-alts ra-skip"><small>Closest lessons:</small>${hits.slice(0, 3).map(a => `<button class="ask-alt" data-tid="${esc(a.t.id)}">${esc(a.t.t)} <i>${esc(a.t.sn)}</i></button>`).join('')}</div>` : ''}</div>`;
      wire(wait, hits); sfx('hmm'); return;
    }
    wait.innerHTML = card(top, hits.slice(1, 4)); wire(wait, hits); sfx('open');
    wait.scrollIntoView({ behavior: 'smooth', block: 'start' });
    try { const t = ST.asked = ST.asked || {}; t[top.t.id] = (t[top.t.id] || 0) + 1; save(); } catch (e) {}
  }
  window.Ask = { open, ask, search: async q => { await loadIndex(); return search(q); }, calc, provider: p => { PROV.push(p); docsKey = ''; } };
  const boot = () => { if (!ST.profile) return setTimeout(boot, 1500); build(); };
  setTimeout(boot, 800);
})();
