/* ================= 📖 Story mode (school) — js/story.js =================
   Every chapter becomes a short adventure of 5–8 scenes. Each scene = a quest line (no facts, just the frame)
   + 1–2 lines taken word for word from that topic's lesson (hook / big ideas) + one question from the same
   topic's reviewed quiz that unlocks the next scene. Nothing is invented: every fact on screen is lesson text.
   Frames per subject: Science "Lab explorer", Maths "Treasure map", History "Time traveller",
   English "Story book", Hindi/Sanskrit "कहानी की किताब" (Hindi words for Devanagari subjects), others "Explorer".
   Entry: a "📖 Story" button added to the chapter screen's button row (.ch-btns, made by js/tests.js).
   State: ST.story["g7-science-3"] = { d: 'YYYY-MM-DD' first finish, stars: best 1–3, n: times finished }.
   Answers count like quiz answers (ST.qstats, logAns, ST.mistakes). Stars: +6 per right answer (+3 after a 💡 hint),
   finish bonus; a hinted right answer counts ½ for the 1–3 star rating. Hints: Games.hint (js/games.js) — never the answer. */
(function () {
  'use strict';
  const D = document;
  const tap = k => { try { sfx(k); } catch (e) {} };
  const say = m => { try { if (window.A11Y && A11Y.announce) A11Y.announce(m); } catch (e) {} };
  const isCA = () => !!(ST.profile && ST.profile.course === 'ca');
  const keyOf = (g, sid, ci) => `g${g}-${sid}-${ci}`;
  const S = () => (ST.story = ST.story && typeof ST.story === 'object' ? ST.story : {});

  /* ---------- quest frames: wording only, never facts ---------- */
  const FR = {
    lab: { e: '🔬', name: 'Lab explorer', bg: 'linear-gradient(135deg,#d9fbef,#e7f0ff)',
      intro: c => `Put on your lab coat! Each station in this lab hides one big idea from “${c}”. Read it, then solve the challenge to unlock the next station.`,
      label: (n, N) => `Station ${n} of ${N}`, lead: t => `You walk up to the next station: ${t}.`, unlock: 'Solve this to unlock the next station',
      done: 'Lab mission complete!' },
    map: { e: '🗺️', name: 'Treasure map', bg: 'linear-gradient(135deg,#fff3cf,#ffe3d3)',
      intro: c => `Follow the treasure map through “${c}”. Every clue is a maths idea. Crack it to find the next mark on the map.`,
      label: (n, N) => `Clue ${n} of ${N}`, lead: t => `The map points to the next clue: ${t}.`, unlock: 'Crack this clue to move on',
      done: 'You found the treasure!' },
    time: { e: '⏳', name: 'Time traveller', bg: 'linear-gradient(135deg,#f1e8ff,#ffe9f1)',
      intro: c => `Step into the time machine! Each stop in “${c}” has something to discover. Answer correctly to power up the next jump.`,
      label: (n, N) => `Stop ${n} of ${N}`, lead: t => `The time machine lands. This stop: ${t}.`, unlock: 'Answer to power up the time machine',
      done: 'Time trip complete!' },
    explore: { e: '🧭', name: 'Explorer', bg: 'linear-gradient(135deg,#e3f6ff,#e9ffe9)',
      intro: c => `Pack your bag, explorer! The trail through “${c}” has a stop for each idea. Answer at each stop to open the next part of the trail.`,
      label: (n, N) => `Stop ${n} of ${N}`, lead: t => `The trail brings you to: ${t}.`, unlock: 'Answer to open the trail',
      done: 'Trail complete!' },
    book: { e: '📖', name: 'Story book', bg: 'linear-gradient(135deg,#fff0e0,#f3ecff)',
      intro: c => `Open the story book of “${c}”. Read each page, then answer the question to turn to the next page.`,
      label: (n, N) => `Page ${n} of ${N}`, lead: t => `You turn the page: ${t}.`, unlock: 'Answer to turn the page',
      done: 'You finished the book!' },
    bookHi: { e: '📖', name: 'कहानी की किताब', bg: 'linear-gradient(135deg,#fff0e0,#f3ecff)',
      intro: c => `“${c}” की कहानी की किताब खोलो! हर पन्ना पढ़ो, फिर सवाल का जवाब देकर अगला पन्ना पलटो।`,
      label: (n, N) => `पन्ना ${n} / ${N}`, lead: t => `तुमने पन्ना पलटा: ${t}`, unlock: 'जवाब दो और अगला पन्ना खोलो',
      done: 'शाबाश! किताब पूरी हुई!' } };
  const UI = {
    en: { story: 'Story', start: 'Start the story ▶', next: 'Next ▶', finish: 'Finish ▶', right: '✅ Correct!', wrong: a => `❌ Not quite. The answer is: <b>${a}</b>`, steps: 'See the steps',
      hint: '💡 Ask Gappu', back: '← Chapter', scenes: n => `${n} scenes · about ${Math.max(3, Math.round(n * 1.2))} minutes`, stamp: 'Chapter completed as a story', hinted: n => `💡 ${n} hint${n > 1 ? 's' : ''} used (½ ⭐ for ${n > 1 ? 'those scenes' : 'that scene'})`,
      score: (r, n) => `${r} of ${n} questions right`, again: '🔁 Read it again', toCh: 'Back to chapter', before: s => `You finished this story before · best ${'⭐'.repeat(s)}`, listen: 'Read aloud' },
    hi: { story: 'कहानी', start: 'कहानी शुरू करो ▶', next: 'आगे ▶', finish: 'पूरा करो ▶', right: '✅ सही जवाब!', wrong: a => `❌ नहीं, सही जवाब है: <b>${a}</b>`, steps: 'हल देखो',
      hint: '💡 गप्पू से पूछो', back: '← अध्याय', scenes: n => `${n} पन्ने · लगभग ${Math.max(3, Math.round(n * 1.2))} मिनट`, stamp: 'अध्याय कहानी के रूप में पूरा हुआ', hinted: n => `💡 ${n} संकेत लिए (उन पन्नों पर ½ ⭐)`,
      score: (r, n) => `${n} में से ${r} सवाल सही`, again: '🔁 फिर से पढ़ो', toCh: 'अध्याय पर वापस', before: s => `यह कहानी तुम पहले पूरी कर चुके हो · सबसे अच्छा ${'⭐'.repeat(s)}`, listen: 'सुनो' } };
  const SCI = ['science', 'physics', 'chemistry', 'biology', 'evs'], HIST = ['history'], LANG_EN = ['english'];
  const deva = s => /[ऀ-ॿ]/.test(String(s || ''));
  function langOf(g, sid, c) {
    let l = null; try { l = ((CUR && CUR.grades && CUR.grades[g] && CUR.grades[g].subjects) || []).find(s => s.id === sid)?.language || null; } catch (e) {}
    if (l === 'hi' || deva(c.title) || deva(c.topics[0]?.title)) return 'hi';
    return 'en';
  }
  function frameOf(sid, lang) {
    if (lang === 'hi') return FR.bookHi;
    if (SCI.includes(sid)) return FR.lab;
    if (sid === 'maths') return FR.map;
    if (HIST.includes(sid)) return FR.time;
    if (LANG_EN.includes(sid)) return FR.book;
    return FR.explore;
  }

  /* ---------- building the scenes (5–8) from the chapter's own lesson + quiz ---------- */
  const STOPW = new Set('that this with from have they their there which what when where were will your into than then them these those about other also only some more most very been does like make made each such just over many much काम करते करता करती होता होती होते जाता जाती सकते लिए उसके उनके इसके किया दिया अपने अपनी'.split(' '));
  const words = s => new Set(String(s || '').toLowerCase().split(/[^a-z0-9ऀ-ॿ]+/).filter(w => w.length > 3 && !STOPW.has(w)));
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  function plan(c) {
    const T = c.topics.filter(t => (t.quiz || []).length && ((t.learn || {}).points || []).length);
    if (!T.length) return [];
    const N = Math.max(5, Math.min(8, T.length));
    let picks;                                                 // [{t, j: scene number inside this topic, k: scenes for this topic}]
    if (T.length >= N) {                                       // more topics than scenes: spread evenly across the chapter (first and last kept)
      const idx = N === T.length ? T.map((_, i) => i) : Array.from({ length: N }, (_, i) => Math.round(i * (T.length - 1) / (N - 1)));
      picks = [...new Set(idx)].map(i => ({ t: T[i], j: 0, k: 1 }));
    } else {                                                   // fewer topics: 2+ scenes per topic, each with its own lines and question
      const per = T.map(t => Math.min(Math.ceil(N / T.length), t.quiz.length, Math.max(1, Math.ceil(t.learn.points.length / 2))));
      let tot = per.reduce((a, b) => a + b, 0);
      while (tot > N) { const m = per.indexOf(Math.max(...per)); per[m]--; tot--; }
      picks = []; T.forEach((t, i) => { for (let j = 0; j < per[i]; j++) picks.push({ t, j, k: per[i] }); });
    }
    const used = {};
    return picks.map(({ t, j, k }) => {
      const L = t.learn || {}, pts = L.points || [];
      /* lines: this scene's share of the topic's big ideas (the hook opens a topic's first scene when it is short) */
      const per = Math.ceil(pts.length / k), part = pts.slice(j * per, j * per + per);
      let lines = [];
      if (j === 0 && L.hook && L.hook.length <= 170) lines.push(L.hook);
      for (const p of part) { if (lines.length >= 2) break; if (lines.length && (lines[0].length + p.length > 330)) break; lines.push(p); }
      if (!lines.length) lines = [part[0] || pts[0]];
      /* question: the one closest to what this scene just said (shared words), then one this student has not got
         right yet; never the same question twice in a story */
      const u = used[t.id] = used[t.id] || new Set();
      const qs = shuffle(t.quiz.map((q, i) => i).filter(i => !u.has(i)));
      const rank = i => { const s = (ST.qstats || {})[`${t.id}#${i}`]; return !s ? 1 : s.w > 0 ? 0 : 2; };
      const lw = words(lines.join(' ')), rel = {};
      qs.forEach(i => { const q = t.quiz[i]; let n = 0; words(`${q.q} ${q.options[q.answer]} ${q.explain || ''}`).forEach(w => { if (lw.has(w)) n++; }); rel[i] = Math.min(n, 4); });
      qs.sort((a, b) => rel[b] - rel[a] || rank(a) - rank(b));
      const qi = qs.length ? qs[0] : 0; u.add(qi);
      return { t, lines, qi, q: t.quiz[qi], qid: `${t.id}#${qi}` };
    });
  }

  /* ---------- styles (once) ---------- */
  function css() {
    if (D.getElementById('styCss')) return;
    D.head.insertAdjacentHTML('beforeend', `<style id="styCss">
.sty-hero{display:flex;gap:12px;align-items:center}.sty-hero .sty-e{font-size:42px;line-height:1}.sty-hero h2{margin:2px 0 0;font-size:21px;line-height:1.15}
.sty-hero .tag{margin-bottom:2px}.sty-intro{font-size:15px;line-height:1.45;font-weight:700;margin:10px 0 12px}
.sty-path{display:flex;gap:5px;margin:2px 0 10px}.sty-path i{flex:1;height:7px;border-radius:9px;background:#e3e6f6}.sty-path i.on{background:var(--violet)}.sty-path i.ok{background:var(--mint)}.sty-path i.no{background:#ffb27a}
.sty-scene{border-radius:22px}.sty-lead{font-family:'Baloo 2';font-weight:800;font-size:17px;line-height:1.25;margin:2px 0 8px;color:var(--ink)}
.sty-narr{position:relative;background:rgba(255,255,255,.72);border-radius:16px;padding:10px 44px 10px 12px;font-size:15px;line-height:1.5;color:var(--ink)}
.sty-narr p{margin:0}.sty-narr p+p{margin-top:8px}.sty-narr .spk{position:absolute;top:6px;right:6px}
.sty-unlock{font-weight:800;font-size:12.5px;color:var(--violet);text-transform:uppercase;letter-spacing:.04em;margin:0 0 4px}
.sty-q{font-size:17px;line-height:1.35;margin:0 0 4px}
.sty-res{margin-top:10px;border-radius:14px;padding:10px 12px;font-size:14.5px;line-height:1.45;font-weight:700}.sty-res.good{background:#e3fbf1}.sty-res.bad{background:#fff1e6}
.sty-res .v{font-family:'Baloo 2';font-size:17px;display:block;margin-bottom:3px}.sty-res details{margin-top:6px}.sty-res summary{cursor:pointer;color:var(--violet)}.sty-res ol{margin:6px 0 0 18px;font-weight:600}
.sty-ask{border:2px dashed #f5b301;background:#fffbea;color:#7a5200;border-radius:999px;padding:8px 14px;min-height:44px;font:inherit;font-weight:800;font-size:14px;cursor:pointer;margin-top:10px}
.sty-say:empty{display:none}.sty-say{background:#fff8dc;border-radius:14px;padding:10px 12px;font-size:14px;margin-top:8px}
#styOpts .opt.gp-out{opacity:.3;text-decoration:line-through;pointer-events:none}
.sty-row{display:flex;gap:8px;margin-top:12px}.sty-row .btn{flex:1}.sty-row .btn.ghost{flex:0 0 auto;width:auto;font-size:15px}
.sty-stamp{display:inline-flex;align-items:center;gap:8px;border:3px dashed #e05d2a;color:#c2410c;border-radius:14px;padding:8px 12px;font-family:'Baloo 2';font-weight:800;font-size:16px;transform:rotate(-3deg);margin:6px 0 10px;background:#fff8f0}
.sty-fin{text-align:center}.sty-fin .bigstars{justify-content:center}
.ch-btns button.sty-done::after{content:' ✓';color:#0a7d55}
</style>`);
  }

  /* ---------- 💡 hints: the shared helper in js/games.js (Games.hint) when present, else a local 50/50 ---------- */
  const MAXHINT = 2;
  function hintBar(box, st, q, topic, el) {
    const wrong = () => q.options.map((_, k) => k).filter(k => k !== q.answer && !el.querySelector(`#styOpts .opt[data-k="${k}"].gp-out`));
    const hide = k => el.querySelectorAll('#styOpts .opt').forEach(x => { if (+x.dataset.k === k) { x.disabled = true; x.classList.add('gp-out'); x.setAttribute('aria-label', `${x.textContent.trim()}: crossed out by Gappu`); } });
    const cap = () => { if (st.n >= MAXHINT) { const b = box.querySelector('.gp-ask'); if (b) b.remove(); } };
    const H = window.Games && Games.hint;
    if (H && H.bar && H.clue) {
      const bar = H.bar(box, st, { answered: false, wrong, hide, clue: () => H.clue({ q: q.q, answer: q.options[q.answer], explain: q.explain, topic }), onUse: cap });
      cap(); return bar;
    }
    /* local fallback: cross out one wrong option per tap (2 at most, one wrong option always stays) */
    if (st.n == null) { st.n = 0; st.out = []; }
    st.out.forEach(hide);
    const draw = () => {
      const can = st.n < MAXHINT && wrong().length >= 2;
      box.innerHTML = `${can ? `<button type="button" class="gp-ask sty-ask" aria-label="Ask Gappu for a hint. The stars for this scene are halved.">💡 Ask Gappu (½ ⭐)</button>` : ''}<div class="sty-say" role="status" aria-live="polite">${st.n ? `🐥 I crossed out ${st.n > 1 ? 'two answers that are' : 'one answer that is'} <b>not</b> right.` : ''}</div>`;
      const b = box.querySelector('.sty-ask'); if (b) b.onclick = () => { const w = wrong(), k = w[Math.floor(Math.random() * w.length)]; st.out.push(k); st.n++; hide(k); tap('tap'); draw(); };
    };
    draw();
    return { done() { box.innerHTML = ''; } };
  }

  /* ---------- the story screen (inside #s-chapter, like the revision sheet) ---------- */
  async function open(sid, ci) {
    if (isCA()) return;
    css();
    const g = ST.profile.grade, d = await subjectData(g, sid); if (!d || !d.chapters[ci]) return;
    const c = d.chapters[ci], lang = langOf(g, sid, c), F = frameOf(sid, lang), U = UI[lang];
    const scenes = plan(c);
    show('chapter', 'world'); RUN = null;
    const el = D.getElementById('s-chapter'); if (!el) return;
    const back = () => { try { ReadAlong.stop(); } catch (e) {} chapterScreen(sid, ci); };
    if (!scenes.length) { el.innerHTML = `<button class="back" id="styBack">${U.back}</button><div class="card"><p class="sub">This chapter's story is coming soon.</p></div>`; D.getElementById('styBack').onclick = back; return; }
    const N = scenes.length, res = [], hints = [], hinted = x => !!(hints[x] && hints[x].n), prev = S()[keyOf(g, sid, ci)];
    let at = -1;
    const pathHTML = () => `<div class="sty-path" aria-hidden="true">${scenes.map((_, i) => `<i class="${res[i] === true ? 'ok' : res[i] === false ? 'no' : i === at ? 'on' : ''}"></i>`).join('')}</div>`;
    const head = () => `<button class="back" id="styBack">${U.back}</button>`;
    function intro() {
      el.innerHTML = head() + `<div class="card sty-scene" style="background:${F.bg}"><div class="sty-hero"><div class="sty-e" aria-hidden="true">${F.e}</div><div><span class="tag">${esc(F.name)} · ${lang === 'hi' ? 'अध्याय' : 'Chapter'} ${esc(c.n)}</span><h2>${esc(c.title)}</h2></div></div>
        <div class="sty-narr" id="styNarr"><p>${esc(F.intro(c.title))}</p><button class="spk" data-ra=".sty-narr" aria-label="${U.listen}">🔊</button></div>
        <p class="sub" style="margin:10px 0 0">${esc(U.scenes(N))}${prev ? ` · ${esc(U.before(prev.stars || 1))}` : ''}</p>
        <div style="height:12px"></div><button class="btn" id="styGo">${U.start}</button></div>`;
      D.getElementById('styBack').onclick = back;
      D.getElementById('styGo').onclick = () => { tap('open'); scene(0); };
    }
    function scene(i) {
      try { ReadAlong.stop(); } catch (e) {}
      at = i; const s = scenes[i], q = s.q, order = shuffle(q.options.map((_, k) => k));
      const shownAt = Date.now();
      el.innerHTML = head() + `<div class="card sty-scene" style="background:${F.bg}"><span class="tag">${F.e} ${esc(F.label(i + 1, N))}</span>${pathHTML()}
          <h2 class="sty-lead">${esc(F.lead(s.t.title))}</h2>
          <div class="sty-narr" id="styNarr">${s.lines.map(x => `<p>${esc(x)}</p>`).join('')}<button class="spk" data-ra=".sty-narr" aria-label="${U.listen}">🔊</button></div></div>
        <div class="card" id="styQ"><p class="sty-unlock">🔓 ${esc(F.unlock)}</p>
          <h3 class="sty-q qtext">${esc(q.q)} ${spk(q.q, 1)}</h3>
          <div id="styOpts" role="group" aria-label="${lang === 'hi' ? 'विकल्प' : 'Answer choices'}">${order.map(k => `<button class="opt" data-k="${k}">${esc(q.options[k])}</button>`).join('')}</div>
          <div id="styRes" aria-live="polite"></div>
          <div class="sty-hint" id="styHintBox"></div>
          <div class="sty-row"><button class="btn" id="styNext" hidden>${i < N - 1 ? U.next : U.finish}</button></div></div>`;
      D.getElementById('styBack').onclick = back;
      window.scrollTo(0, 0);
      /* 💡 Ask Gappu: a hint that never shows the answer (crosses out a wrong option / a lesson clue with the answer
         words hidden as ____). Only on tap, at most 2 per scene; a hinted right answer earns half. */
      const hbox = D.getElementById('styHintBox'), hst = hints[i] = hints[i] || {};
      const hint = hintBar(hbox, hst, q, s.t, el);
      el.querySelectorAll('#styOpts .opt').forEach(b => b.onclick = () => {
        if (res[i] != null) return;
        const k = +b.dataset.k, ok = k === q.answer; res[i] = ok; hint.done();
        el.querySelectorAll('#styOpts .opt').forEach(x => { x.disabled = true; const kk = +x.dataset.k; if (kk === q.answer) x.classList.add('right'); else if (kk === k) x.classList.add('wrong'); });
        /* counts like a quiz answer */
        try { const qs = ST.qstats[s.qid] || { s: 0, w: 0 }; qs.s++; if (!ok) { qs.w++; if (q.mistake) ST.mistakes[q.mistake] = (ST.mistakes[q.mistake] || 0) + 1; } ST.qstats[s.qid] = qs; logAns(s.qid, ok, (Date.now() - shownAt) / 1000); } catch (e) {}
        if (ok) { tap('correct'); addXP(hinted(i) ? 3 : 6); } else { tap('wrong'); save(); }
        const r = D.getElementById('styRes');
        r.innerHTML = `<div class="sty-res ${ok ? 'good' : 'bad'}"><span class="v">${ok ? U.right : U.wrong(esc(q.options[q.answer]))}</span>${q.visual && window.Visual ? `<div class="vis">${Visual.render(q.visual)}</div>` : ''}${esc(q.explain || '')}
          ${(q.steps || []).length ? `<details><summary>${U.steps}</summary><ol>${q.steps.map(x => `<li>${esc(x)}</li>`).join('')}</ol></details>` : ''}</div>`;
        const p = el.querySelector('.sty-path'); if (p) p.outerHTML = pathHTML();
        const nx = D.getElementById('styNext'); nx.hidden = false; nx.onclick = () => { tap('tap'); i < N - 1 ? scene(i + 1) : finish(); };
        setTimeout(() => { try { r.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); nx.focus({ preventScroll: true }); } catch (e) {} }, 120);
      });
    }
    function finish() {
      try { ReadAlong.stop(); } catch (e) {}
      const right = res.filter(Boolean).length, score = res.reduce((a, ok, x) => a + (ok ? (hinted(x) ? .5 : 1) : 0), 0), pct = score / N, stars = pct >= .85 ? 3 : pct >= .6 ? 2 : 1;
      const k = keyOf(g, sid, ci), st = S(), old = st[k];
      st[k] = { d: (old && old.d) || today(), stars: Math.max(stars, (old && old.stars) || 0), n: ((old && old.n) || 0) + 1, last: today() };
      bumpStreak();
      const bonus = !old ? 10 + stars * 5 : stars > (old.stars || 0) ? (stars - old.stars) * 5 : 0;
      if (bonus) addXP(bonus, lang === 'hi' ? 'कहानी पूरी!' : 'Story complete!'); else save();
      tap('unlock');
      el.innerHTML = head() + `<div class="card done-card sty-fin"><div class="confetti" aria-hidden="true">${Array.from('🎉⭐✨📖🌟'.repeat(4)).map((e, x) => `<span style="left:${(x * 37) % 100}%;animation-delay:${(x % 7) * .12}s">${e}</span>`).join('')}</div>
        <div class="gbig" aria-hidden="true">${F.e}</div><h2>${esc(F.done)}</h2>
        <div class="sty-stamp" role="img" aria-label="${esc(U.stamp)}">📖 ${esc(U.stamp)}</div>
        <div class="bigstars" aria-label="${stars} of 3 stars">${[0, 1, 2].map(x => `<span class="${x < stars ? 'on' : ''}" style="animation-delay:${x * .25}s">⭐</span>`).join('')}</div>
        <p class="sub" role="status">${esc(U.score(right, N))}${hints.filter(h => h && h.n).length ? ` · ${esc(U.hinted(hints.filter(h => h && h.n).length))}` : ''}</p>
        <button class="btn" id="styAgain">${U.again}</button><div style="height:8px"></div><button class="btn ghost" id="styDone">${U.toCh}</button></div>`;
      D.getElementById('styBack').onclick = back;
      D.getElementById('styDone').onclick = back;
      D.getElementById('styAgain').onclick = () => { tap('open'); open(sid, ci); };
      say(`${F.done} ${U.score(right, N)}`);
      window.scrollTo(0, 0);
    }
    intro();
  }

  /* ---------- the 📖 Story button in the chapter's button row ---------- */
  function place() {
    if (!ST.profile || isCA()) return;
    const w = D.getElementById('s-chapter'); if (!w || !w.classList.contains('active')) return;
    const row = w.querySelector('.ch-tools .ch-btns'); if (!row || row.querySelector('[data-story]')) return;
    let nv = {}; try { nv = NAV || {}; } catch (e) {}
    const sid = nv.subject, ci = nv.chapter; if (sid == null || ci == null) return;
    css();
    const done = S()[keyOf(ST.profile.grade, sid, ci)];
    row.insertAdjacentHTML('afterbegin', `<button id="chStory" data-story="1" class="${done ? 'sty-done' : ''}" aria-label="Story mode: learn this chapter as an adventure${done ? ' (completed)' : ''}">📖 Story</button>`);
    row.querySelector('[data-story]').onclick = () => { tap('open'); api.open(sid, ci); };
  }
  let t = 0;
  new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; try { place(); } catch (e) {} }); }).observe(D.body, { childList: true, subtree: true });

  const api = { open, plan, _frame: frameOf, _lang: langOf };
  if (window.Nav) api.open = Nav.route('story', open);
  window.Story = api;
})();
