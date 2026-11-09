/* ================= Game templates: every topic's games are built from data ================= */
(function () {
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const S = k => (window.sfx ? sfx(k) : 0);
  const RA = (opts = 1) => ` <button class="spk"${opts ? ' data-opts="1"' : ''} aria-label="Read aloud">🔊</button>`;
  const head = (g, extra = '') => `<div class="ghead"><span class="gtype">${{ match: '🧩 Match', sort: '🗂️ Sort', order: '🔢 Order', truefalse: '✅ True or False', fill: '✏️ Fill the gap', speed: '⚡ Speed round' }[g.type]}</span>${extra}</div><h3>${esc(g.title)}</h3>`;
  /* score: stars-score when Gappu hints were used (a hinted right answer counts ½); hints: how many cards used one */
  const finish = (el, right, total, done, score, hints) => {
    const pct = total ? right / total : 1;
    el.insertAdjacentHTML('beforeend', `<div class="gdone">${pct >= .8 ? '🎉 Brilliant!' : pct >= .5 ? '👍 Good job!' : '💪 Nice try!'} ${right}/${total}</div>${hints ? `<p class="sub gp-used">💡 Gappu gave you ${hints} hint${hints > 1 ? 's' : ''}, so ${hints > 1 ? 'those cards earn' : 'that card earns'} ½ ⭐.</p>` : ''}<button class="btn mint gnext">Continue ▶</button>`);
    el.querySelector('.gnext').onclick = () => done(score == null ? right : score, total);
  };
  /* stars-score of a game: a right answer counts 1, or ½ if Gappu gave a hint on that card */
  const wscore = (oks, hs) => oks.reduce((a, ok, j) => a + (ok ? (hs[j] && hs[j].n ? .5 : 1) : 0), 0);
  const nHints = hs => hs.filter(h => h && h.n).length;
  const topicNow = () => { try { return (typeof RUN !== 'undefined' && RUN && RUN.t) || null; } catch (e) { return null; } };

  /* ================= 💡 Ask Gappu: one gentle hint, only when the student taps =================
     Nothing shows until the student taps "💡 Ask Gappu (½ ⭐)". A hint never shows the answer:
       1st tap: Gappu crosses out one wrong option (only when at least two wrong ones are still showing);
       next tap: a clue: the question's own explanation, or the topic's Big ideas, with the answer words hidden (____);
       then (if still stuck) one more wrong option crossed out. At least one wrong option always stays.
     Two-option questions (True/False, two baskets) only get the clue, because crossing one out would give it away.
     st = the question's hint state, kept by the caller (one per question, so ◀ Previous / Next ▶ keep it).
     Using a hint halves that question's stars (the caller does the scoring: Games.hint.used(st)). */
  const HSTOP = new Set(('the a an of to in on is are was were be been being and or for with by at as from that this these those it its into than then what which who whom whose when where why how do does did not no yes can could will would shall should may might must has have had our your their his her they them we you he she one all some any very more most also only just like so if but there here about after before over under out up down each other such same way ' +
    'के का की है हैं और में से को पर भी यह वह एक था थी थे').split(' '));
  const WCH = '\\p{L}\\p{N}\\p{M}';
  const hnorm = s => String(s == null ? '' : s).toLowerCase().normalize('NFC');
  const hwords = s => hnorm(s).split(/[^\p{L}\p{N}\p{M}]+/u).filter(w => w.length > 2 && !HSTOP.has(w));
  const reEsc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  // whole word (or, for words of 4+ letters, any word that starts with it: clap → clapping)
  const wordRe = w => new RegExp(`(^|[^${WCH}])(${reEsc(w)})${w.length >= 4 && !/^\d+$/.test(w) ? `[${WCH}]*` : ''}(?=[^${WCH}]|$)`, 'giu');
  function mask(text, answer, keep) {
    let t = String(text == null ? '' : text); const a = String(answer == null ? '' : answer).trim(); if (!a) return t;
    t = t.replace(wordRe(hnorm(a)), '$1____');
    hwords(a).forEach(w => { if (!keep || !keep.has(w)) t = t.replace(wordRe(w), '$1____'); });
    return t;
  }
  const sentences = s => String(s || '').split(/(?<=[.!?।])\s+/).map(x => x.trim()).filter(Boolean);
  /* o = { q: question text, answer: right answer text (none for True/False), explain, topic, tf: true for True/False } */
  function clue(o) {
    const qw = new Set(hwords(o.q)), cands = [], t = o.topic;
    if (!o.tf) sentences(o.explain).slice(0, 2).forEach(x => cands.push(x));
    const facts = [...((t && t.learn && t.learn.points) || []), ...((t && t.revise && t.revise.remember) || [])];
    facts.map(p => [p, hwords(p).filter(w => qw.has(w)).length]).filter(x => x[1] > 0).sort((a, b) => b[1] - a[1]).forEach(x => cands.push(x[0]));
    const flat = s => hnorm(s).replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
    for (const c of cands) {
      const m = o.tf ? c : mask(c, o.answer, qw);
      if (!o.tf) {
        const a = flat(o.answer);
        if (a && (` ${flat(m)} `).includes(` ${a} `)) continue;                                  // answer still there
        if (hwords(o.answer).some(w => !qw.has(w) && wordRe(w).test(m))) continue;
        if ((m.match(/____/g) || []).length > 3) continue;                                         // too many gaps to help
        const ad = String(o.answer).replace(/\D/g, '');                                            // a number written another way (605000 / 6,05,000)
        if (ad.length >= 2 && (m.match(/\d[\d,]*(\.\d+)?/g) || []).some(x => x.replace(/\D/g, '') === ad)) continue;
      }
      const left = hwords(m.replace(/_+/g, ' '));
      if (left.length < 3) continue;
      if (flat(m) === flat(o.q)) continue;
      if (o.tf) { const sw = hwords(o.q); if (sw.length && sw.filter(w => left.includes(w)).length / sw.length >= .8 && left.length <= sw.length + 2) continue; }   // repeats the statement
      return m;
    }
    return '';
  }
  let hintCss = false;
  function hintStyle() {
    if (hintCss) return; hintCss = true;
    const st = document.createElement('style'); st.id = 'gpHintCss';
    st.textContent = `.gp-hint{margin:10px 0 4px;display:flex;flex-direction:column;align-items:flex-start;gap:8px}
.gp-ask{border:2px dashed #f5b301;background:#fffbea;color:#7a5200;border-radius:999px;padding:8px 14px;min-height:44px;font:inherit;font-weight:800;font-size:14px;cursor:pointer}
.gp-ask:active{transform:scale(.97)}.gp-ask:focus-visible{outline:3px solid #6c5ce7;outline-offset:2px}
.gp-say:empty{display:none}.gp-say{display:flex;gap:8px;align-items:flex-start;background:#fff8dc;border-radius:14px;padding:10px 12px;font-size:14px;line-height:1.45;color:#3b4064;width:100%;box-sizing:border-box}
.gp-say>span{font-size:26px;line-height:1}.gp-say p{margin:0 0 4px}.gp-say p:last-child{margin:0}
.gp-out,.opt.gp-out,.arc-opt.gp-out,.arc-lb.gp-out,.sbk.gp-out{opacity:.3!important;text-decoration:line-through;filter:grayscale(1);pointer-events:none}
.gp-used{margin:6px 0 10px;text-align:center}`;
    document.head.appendChild(st);
  }
  /* box: an empty element under the options. cfg = { wrong: () => ids of wrong options still showing, hide: id => cross it out,
     clue: () => clue text or '', answered: bool, cost: show "(½ ⭐)" (default true), onUse: st => {} } */
  function hintBar(box, st, cfg) {
    if (!box || !st) return { done() {} };
    hintStyle();
    if (st.n == null) { st.n = 0; st.out = []; st.outs = 0; st.msgs = []; st.c = null; st.cSaid = false; }
    if (cfg.answered) { box.innerHTML = ''; return { done() {} }; }
    st.out.forEach(id => cfg.hide(id));
    const getClue = () => { if (st.c == null) { try { st.c = (cfg.clue && cfg.clue()) || ''; } catch (e) { st.c = ''; } } return st.c; };
    const avail = () => (cfg.wrong() || []).filter(id => !st.out.includes(id));
    const nextAct = () => {
      if (!st.outs && avail().length >= 2) return 'out';
      if (!st.cSaid && getClue()) return 'clue';
      if (st.outs < 2 && avail().length >= 2) return 'out';
      return '';
    };
    const label = () => st.n ? '💡 One more hint' : `💡 Ask Gappu${cfg.cost === false ? '' : ' (½ ⭐)'}`;
    const aria = () => st.n ? 'Ask Gappu for one more hint' : `Ask Gappu for a hint${cfg.cost === false ? '' : '. The stars for this question are halved.'}`;
    const say = () => st.msgs.length ? `<span aria-hidden="true">🐥</span><div>${st.msgs.map(m => `<p>${m}</p>`).join('')}</div>` : '';
    if (!nextAct() && !st.n) { box.innerHTML = ''; return { done() {} }; }   // no hint possible here
    box.innerHTML = `<div class="gp-hint">${nextAct() ? `<button type="button" class="gp-ask" aria-label="${aria()}">${label()}</button>` : ''}<div class="gp-say" role="status" aria-live="polite">${say()}</div></div>`;
    const sayEl = box.querySelector('.gp-say');
    const wire = () => {
      const b = box.querySelector('.gp-ask'); if (!b) return;
      b.onclick = () => {
        const act = nextAct(); if (!act) { b.remove(); return; }
        let msg;
        if (act === 'out') {
          const av = avail(), id = av[Math.floor(Math.random() * av.length)];
          st.out.push(id); st.outs++; cfg.hide(id);
          msg = st.outs === 1 ? 'I crossed out one answer that is <b>not</b> right. Think about the others!' : 'I crossed out one more wrong answer. You can do it!';
        } else { st.cSaid = true; msg = `Here is a clue: “${esc(getClue())}”`; }
        st.n++; S('tap');
        if (!nextAct()) msg += ' That was my last hint. 💪';
        st.msgs.push(msg);
        sayEl.innerHTML = say();
        if (nextAct()) { b.textContent = label(); b.setAttribute('aria-label', aria()); } else b.remove();
        try { if (window.A11Y && A11Y.cue) A11Y.cue('Gappu says: ' + sayEl.textContent.replace(/\s+/g, ' ').trim()); } catch (e) {}
        if (cfg.onUse) cfg.onUse(st);
      };
    };
    wire();
    return { done() { box.innerHTML = ''; } };
  }
  const crossOut = (scope, sel, match) => id => scope.querySelectorAll(sel).forEach(x => { if (match(x, id)) { x.disabled = true; x.classList.add('gp-out'); x.setAttribute('aria-label', `${x.textContent.trim()}: crossed out by Gappu`); } });

  function match(el, g, done) {
    const left = shuffle(g.pairs.map((p, i) => ({ t: p[0], i }))), right = shuffle(g.pairs.map((p, i) => ({ t: p[1], i })));
    el.innerHTML = head(g) + `<p class="sub">Tap one on the left, then its partner on the right.</p><div class="mgrid"><div>${left.map(x => `<button class="mbtn" data-s="L" data-i="${x.i}">${esc(x.t)}</button>`).join('')}</div><div>${right.map(x => `<button class="mbtn" data-s="R" data-i="${x.i}">${esc(x.t)}</button>`).join('')}</div></div>`;
    let sel = null, matched = 0, tries = 0;
    el.querySelectorAll('.mbtn').forEach(b => b.onclick = () => {
      if (b.classList.contains('ok')) return;
      if (!sel || sel.dataset.s === b.dataset.s) { el.querySelectorAll('.mbtn.sel').forEach(x => x.classList.remove('sel')); sel = b; b.classList.add('sel'); S('tap'); return; }
      tries++;
      if (sel.dataset.i === b.dataset.i) { [sel, b].forEach(x => { x.classList.remove('sel'); x.classList.add('ok'); }); matched++; S('coin'); if (matched === g.pairs.length) { el.insertAdjacentHTML('beforeend', `<div class="tfwhy grev">${verdict(tries === g.pairs.length)}<b>All pairs:</b><ul>${g.pairs.map(p => `<li>${esc(p[0])} ↔ <b>${esc(p[1])}</b></li>`).join('')}</ul>${tries > g.pairs.length ? `<small>${tries - g.pairs.length} wrong tr${tries - g.pairs.length > 1 ? 'ies' : 'y'} on the way.</small>` : ''}</div>`); } if (matched === g.pairs.length) finish(el, g.pairs.length, Math.max(tries, g.pairs.length), (r, t) => done(Math.round(g.pairs.length * g.pairs.length / t), g.pairs.length)); }
      else { [sel, b].forEach(x => { x.classList.add('shake'); setTimeout(() => x.classList.remove('shake', 'sel'), 450); }); S('wrong'); }
      sel = null;
    });
  }

  function sort(el, g, done) {
    const items = shuffle(g.items), N = items.length, ans = items.map(() => null);
    el.innerHTML = head(g, `<span class="gcount" id="sn0">1 of ${N}</span>`) + `<p class="sub">Where does it belong? Tap a box.</p><div class="scard" id="scard"></div><div class="sbuckets">${g.buckets.map((b, k) => `<button class="sbk" data-k="${k}">${esc(b)}</button>`).join('')}</div><div class="ghint"></div><div class="sfb tfwhy" id="sfb" aria-live="polite"></div><div class="gnav"></div>`;
    const card = el.querySelector('#scard'), fb = el.querySelector('#sfb'), bk = el.querySelector('.sbuckets'), cnt = el.querySelector('#sn0'), hb = el.querySelector('.ghint'), hs = items.map(() => ({}));
    const left = () => ans.filter(a => a == null).length;
    const sp = stepper(el, N, i => show(i), () => { card.remove(); bk.remove(); hb.remove(); fb.remove(); cnt.remove(); el.querySelector('.gnav').remove(); el.querySelector('.sub').remove();
      const oks = ans.map((a, j) => a === items[j][1]); finish(el, oks.filter(Boolean).length, N, done, wscore(oks, hs), nHints(hs)); });
    const show = i => {
      const it = items[i], a = ans[i], ok = a === it[1];
      card.textContent = it[0]; card.className = 'scard popin' + (a != null ? (ok ? ' good' : ' bad') : ''); cnt.textContent = `${i + 1} of ${N}`;
      el.querySelectorAll('.sbk').forEach(b => { const k = +b.dataset.k; b.disabled = a != null; b.classList.remove('gp-out'); b.removeAttribute('aria-label'); b.classList.toggle('right', a != null && k === it[1]); b.classList.toggle('wrong', a != null && k === a && !ok); });
      hintBar(hb, hs[i], { answered: a != null, wrong: () => g.buckets.map((x, k) => k).filter(k => k !== it[1]), hide: crossOut(bk, '.sbk', (x, k) => +x.dataset.k === k),
        clue: () => clue({ q: it[0], answer: g.buckets[it[1]], topic: topicNow() }) });
      fb.innerHTML = a != null ? verdict(ok) + `<b>${esc(it[0])}</b> belongs in <b>${esc(g.buckets[it[1]])}</b>.${ok ? '' : ` You chose <b>${esc(g.buckets[a])}</b>.`}` : '';
      sp.wire(a != null, left);
    };
    el.querySelectorAll('.sbk').forEach(b => b.onclick = () => {
      const i = sp.at(); if (ans[i] != null) return;               /* scored once */
      ans[i] = +b.dataset.k; S(ans[i] === items[i][1] ? 'correct' : 'wrong'); show(i);
      const nx = el.querySelector('.tfn'); if (nx) nx.focus({ preventScroll: true });
    });
    show(0);
  }

  function order(el, g, done) {
    const items = g.items.map((t, i) => ({ t, i })); let sh = shuffle(items); if (sh.every((x, k) => x.i === k)) sh = sh.reverse();
    let next = 0, mistakes = 0;
    el.innerHTML = head(g) + `<p class="sub">${esc(g.prompt)} — tap them in order.</p><div class="otrack" id="otrack"></div><div class="opool">${sh.map(x => `<button class="ochip" data-i="${x.i}">${esc(x.t)}</button>`).join('')}</div>`;
    const track = el.querySelector('#otrack');
    el.querySelectorAll('.ochip').forEach(b => b.onclick = () => {
      if (+b.dataset.i === next) { S('coin'); b.disabled = true; b.classList.add('used'); track.insertAdjacentHTML('beforeend', `${next ? '<span class="oarrow">→</span>' : ''}<span class="ostep popin">${esc(b.textContent)}</span>`); next++;
        if (next === items.length) { el.insertAdjacentHTML('beforeend', `<div class="tfwhy grev">${verdict(!mistakes)}<b>${esc(g.prompt)}:</b> ${items.map(x => esc(x.t)).join(' → ')}${mistakes ? `<br><small>${mistakes} wrong tap${mistakes > 1 ? 's' : ''} on the way.</small>` : ''}</div>`); finish(el, Math.max(0, items.length - mistakes), items.length, done); } }
      else { mistakes++; S('wrong'); b.classList.add('shake'); setTimeout(() => b.classList.remove('shake'), 450); }
    });
  }

  /* ◀ Previous / Next ▶ (like the quiz runners): skip a card and come back, revisit an answered card (your answer and
     the reason are shown again), each card is scored once. Finishing with blanks asks once; blanks score 0. */
  const navRow = (i, N, done) => `<div class="tst-nav qnav gnav"><button class="btn ghost gprev" ${i ? '' : 'disabled'} aria-label="Previous">◀ Previous</button>`
    + `<button class="btn ${done ? 'mint' : 'ghost'} tfn" aria-label="${i < N - 1 ? (done ? 'Next' : 'Skip to the next one') : 'Finish'}">${i < N - 1 ? 'Next ▶' : 'Finish ▶'}</button></div>`;
  const verdict = ok => `<div class="gverdict ${ok ? 'ok' : 'no'}">${ok ? '✅ Correct!' : '❌ Not quite'}</div>`;
  function stepper(el, N, show, end) {
    let i = 0, sure = false;
    const go = j => { if (j < 0 || j >= N) return; i = j; sure = false; show(i); };
    const wire = (answered, left) => {
      const nav = el.querySelector('.gnav'); if (!nav) return;
      nav.outerHTML = navRow(i, N, answered);
      const n2 = el.querySelector('.gnav');
      n2.querySelector('.gprev').onclick = () => go(i - 1);
      const nx = n2.querySelector('.tfn');
      nx.onclick = () => {
        if (i < N - 1) return go(i + 1);
        const l = left();
        if (l && !sure) { sure = true; nx.textContent = `${l} not answered — tap again to finish`; nx.setAttribute('aria-label', nx.textContent); return; }
        end();
      };
    };
    return { go, wire, at: () => i };
  }

  function truefalse(el, g, done) {
    const items = shuffle(g.items), N = items.length, ans = items.map(() => null);
    el.innerHTML = head(g, `<span class="gcount" id="tfn0">1 of ${N}</span>`) + `<div class="tfcard" id="tfc"></div><div class="tfwhy" id="tfw" aria-live="polite"></div><div class="tfbtns"><button class="btn tfb" data-v="1">👍 True</button><button class="btn tfb no" data-v="0">👎 False</button></div><div class="ghint"></div><div class="gnav"></div>`;
    const c = el.querySelector('#tfc'), w = el.querySelector('#tfw'), btns = el.querySelector('.tfbtns'), cnt = el.querySelector('#tfn0'), hb = el.querySelector('.ghint'), hs = items.map(() => ({}));
    const left = () => ans.filter(a => !a).length;
    const sp = stepper(el, N, i => show(i), () => { c.remove(); w.remove(); btns.remove(); hb.remove(); el.querySelector('.gnav').remove(); cnt.remove(); const oks = ans.map(a => !!(a && a.ok)); finish(el, oks.filter(Boolean).length, N, done, wscore(oks, hs), nHints(hs)); });
    const show = i => {
      const it = items[i], a = ans[i];
      c.innerHTML = esc(it[0]) + RA(0); c.className = 'tfcard popin' + (a ? (a.ok ? ' good' : ' bad') : ''); cnt.textContent = `${i + 1} of ${N}`;
      if (a) { w.innerHTML = verdict(a.ok) + `<b>${it[1] ? 'TRUE' : 'FALSE'}.</b> ${esc(it[2])}<div class="gpick">You said: <b>${a.v ? 'True' : 'False'}</b> ${a.ok ? '✅' : '❌'}</div>`; btns.style.display = 'none'; }
      else { w.textContent = ''; btns.style.display = ''; }
      hintBar(hb, hs[i], { answered: !!a, wrong: () => [], hide: () => {}, clue: () => clue({ q: it[0], tf: true, topic: topicNow() }) });
      sp.wire(!!a, left);
    };
    el.querySelectorAll('.tfb').forEach(b => b.onclick = () => {
      const i = sp.at(); if (ans[i]) return;                     /* scored once */
      const v = b.dataset.v === '1', ok = v === items[i][1]; ans[i] = { v, ok };
      S(ok ? 'correct' : 'wrong'); show(i);
      const nx = el.querySelector('.tfn'); if (nx) nx.focus({ preventScroll: true });
    });
    show(0);
  }

  function fill(el, g, done) {
    const items = g.items, N = items.length, ans = items.map(() => null), orders = items.map(it => shuffle(it.options));
    el.innerHTML = head(g, `<span class="gcount" id="fn0">1 of ${N}</span>`) + `<div class="fsent" id="fs"></div><div class="fopts" id="fo"></div><div class="ghint"></div><div class="tfwhy" id="fw" aria-live="polite"></div><div class="gnav"></div>`;
    const s = el.querySelector('#fs'), o = el.querySelector('#fo'), w = el.querySelector('#fw'), cnt = el.querySelector('#fn0'), hb = el.querySelector('.ghint'), hs = items.map(() => ({}));
    const left = () => ans.filter(a => a == null).length;
    const sp = stepper(el, N, i => show(i), () => { s.remove(); o.remove(); hb.remove(); w.remove(); el.querySelector('.gnav').remove(); cnt.remove(); const oks = ans.map((a, j) => a != null && a === items[j].answer); finish(el, oks.filter(Boolean).length, N, done, wscore(oks, hs), nHints(hs)); });
    const show = i => {
      const it = items[i], a = ans[i], ok = a === it.answer;
      s.innerHTML = esc(it.text).replace('___', `<span class="blank${a != null ? (ok ? ' ok' : ' no') : ''}">${a != null ? esc(it.answer) : '?'}</span>`) + RA(); s.className = 'fsent popin'; cnt.textContent = `${i + 1} of ${N}`;
      w.innerHTML = a != null ? verdict(ok) + (ok ? '' : `The answer is <b>${esc(it.answer)}</b>. `) + `<span class="gfull">“${esc(it.text).replace('___', `<b>${esc(it.answer)}</b>`)}”</span>` : '';
      o.innerHTML = orders[i].map(x => `<button class="opt${a != null && x === it.answer ? ' right' : ''}${a != null && x === a && !ok ? ' wrong' : ''}"${a != null ? ' disabled' : ''}>${esc(x)}</button>`).join('');
      o.querySelectorAll('.opt').forEach(b => b.onclick = () => {
        if (ans[i] != null) return;                              /* scored once */
        ans[i] = b.textContent; S(ans[i] === it.answer ? 'correct' : 'wrong'); show(i);
        const nx = el.querySelector('.tfn'); if (nx) nx.focus({ preventScroll: true });
      });
      hintBar(hb, hs[i], { answered: a != null, wrong: () => it.options.filter(x => x !== it.answer), hide: crossOut(o, '.opt', (x, t) => x.textContent === t),
        clue: () => clue({ q: it.text.replace('___', ' '), answer: it.answer, topic: topicNow() }) });
      sp.wire(a != null, left);
    };
    show(0);
  }

  /* Speed round: one question at a time, ✅/❌ with the working, Next ▶ only when you tap it.
     The clock runs only while a question is waiting for an answer (it pauses on the answer card). */
  const working = (c, a) => { if (!c) return ''; const t = String(c).replace(/\*/g, ' × ').replace(/\//g, ' ÷ ').replace(/\s+/g, ' ').trim(); return `Working: ${esc(t)} = <b>${esc(a)}</b>`; };
  function speed(el, g, done) {
    const items = shuffle(g.items), N = items.length, answers = items.map(x => String(x.a)), ans = items.map(() => null);
    const distract = a => {
      const n = Number(a); const set = new Set([a]);
      if (!isNaN(n) && String(n) === a) [n + 1, n - 1, n + 10, n - 10, n + 2, n * 2].forEach(x => { if (set.size < 3 && x >= 0 && x !== n) set.add(String(x)); });
      shuffle(answers).forEach(x => { if (set.size < 3) set.add(x); });
      return shuffle([...set]);
    };
    const opts = items.map(it => distract(String(it.a)));
    /* timers: normal, extra time (×2) or none (A11Y.timeScale); the clock also waits while the app is talking */
    const sc = window.A11Y ? A11Y.timeScale() : 1;
    let t = Math.round(Math.max(20, N * 6) * (sc || 1)), timer, over = false;
    el.innerHTML = head(g, (sc ? `<span class="timer" id="tm" role="timer" aria-label="Seconds left">${t}s</span>` : '<span class="timer" id="tm">No timer</span>') + `<span class="gcount" id="spn0">1 of ${N}</span>`)
      + `<div class="spq" id="spq"></div><div class="fopts" id="spo"></div><div class="ghint"></div><div class="tfwhy" id="spw" aria-live="polite"></div><div class="gnav"></div>`;
    const q = el.querySelector('#spq'), o = el.querySelector('#spo'), w = el.querySelector('#spw'), tm = el.querySelector('#tm'), cnt = el.querySelector('#spn0'), hb = el.querySelector('.ghint'), hs = items.map(() => ({}));
    const left = () => ans.filter(a => a == null).length;
    const end = () => { clearInterval(timer); q.remove(); o.remove(); hb.remove(); w.remove(); cnt.remove(); el.querySelector('.gnav').remove(); const oks = ans.map((a, j) => a === String(items[j].a)); finish(el, oks.filter(Boolean).length, N, done, wscore(oks, hs), nHints(hs)); };
    const sp = stepper(el, N, i => show(i), end);
    const show = i => {
      const it = items[i], a = ans[i], ok = a === String(it.a), locked = a != null || over;
      q.innerHTML = esc(it.q) + RA(); q.className = 'spq popin'; cnt.textContent = `${i + 1} of ${N}`;
      o.innerHTML = opts[i].map(x => `<button class="opt${locked && x === String(it.a) ? ' right' : ''}${a != null && x === a && !ok ? ' wrong' : ''}"${locked ? ' disabled' : ''}>${esc(x)}</button>`).join('');
      w.innerHTML = a != null ? verdict(ok) + (ok ? '' : `The answer is <b>${esc(it.a)}</b>. `) + working(it.check, it.a) : over ? `⏰ Time is up. The answer is <b>${esc(it.a)}</b>. ` + working(it.check, it.a) : '';
      o.querySelectorAll('.opt').forEach(b => b.onclick = () => {
        if (ans[i] != null || over) return;                       /* scored once */
        ans[i] = b.textContent; S(ans[i] === String(it.a) ? 'correct' : 'wrong'); show(i);
        const nx = el.querySelector('.tfn'); if (nx) nx.focus({ preventScroll: true });
      });
      hintBar(hb, hs[i], { answered: locked, wrong: () => opts[i].filter(x => x !== String(it.a)), hide: crossOut(o, '.opt', (x, t) => x.textContent === t), clue: () => '' });
      sp.wire(a != null || over, left);
    };
    show(0);
    if (sc) timer = setInterval(() => {
      if (!tm.isConnected) { clearInterval(timer); return; }
      if ((window.ReadAlong && ReadAlong.active) || (window.A11Y && A11Y.holdClock())) return;
      if (over || ans[sp.at()] != null) return;                   /* paused while you read the answer */
      t--; tm.textContent = t + 's'; if (window.A11Y) A11Y.timerTick(el, t); if (t <= 5) tm.classList.add('hot');
      if (t <= 0) { over = true; clearInterval(timer); tm.textContent = '⏰ 0s'; show(sp.at()); }
    }, 1000);
  }

  window.Games = { play: (el, g, done) => ({ match, sort, order, truefalse, fill, speed }[g.type] || ((e, gg, d) => d(0, 0)))(el, g, done), shuffle,
    hint: { bar: hintBar, clue, mask, used: st => !!(st && st.n), words: hwords, crossOut } };
})();
