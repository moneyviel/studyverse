/* ================= Game templates: every topic's games are built from data ================= */
(function () {
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const S = k => (window.sfx ? sfx(k) : 0);
  const RA = (opts = 1) => ` <button class="spk"${opts ? ' data-opts="1"' : ''} aria-label="Read aloud">🔊</button>`;
  const head = (g, extra = '') => `<div class="ghead"><span class="gtype">${{ match: '🧩 Match', sort: '🗂️ Sort', order: '🔢 Order', truefalse: '✅ True or False', fill: '✏️ Fill the gap', speed: '⚡ Speed round' }[g.type]}</span>${extra}</div><h3>${esc(g.title)}</h3>`;
  const finish = (el, right, total, done) => {
    const pct = total ? right / total : 1;
    el.insertAdjacentHTML('beforeend', `<div class="gdone">${pct >= .8 ? '🎉 Brilliant!' : pct >= .5 ? '👍 Good job!' : '💪 Nice try!'} ${right}/${total}</div><button class="btn mint gnext">Continue ▶</button>`);
    el.querySelector('.gnext').onclick = () => done(right, total);
  };

  function match(el, g, done) {
    const left = shuffle(g.pairs.map((p, i) => ({ t: p[0], i }))), right = shuffle(g.pairs.map((p, i) => ({ t: p[1], i })));
    el.innerHTML = head(g) + `<p class="sub">Tap one on the left, then its partner on the right.</p><div class="mgrid"><div>${left.map(x => `<button class="mbtn" data-s="L" data-i="${x.i}">${esc(x.t)}</button>`).join('')}</div><div>${right.map(x => `<button class="mbtn" data-s="R" data-i="${x.i}">${esc(x.t)}</button>`).join('')}</div></div>`;
    let sel = null, matched = 0, tries = 0;
    el.querySelectorAll('.mbtn').forEach(b => b.onclick = () => {
      if (b.classList.contains('ok')) return;
      if (!sel || sel.dataset.s === b.dataset.s) { el.querySelectorAll('.mbtn.sel').forEach(x => x.classList.remove('sel')); sel = b; b.classList.add('sel'); S('tap'); return; }
      tries++;
      if (sel.dataset.i === b.dataset.i) { [sel, b].forEach(x => { x.classList.remove('sel'); x.classList.add('ok'); }); matched++; S('coin'); if (matched === g.pairs.length) finish(el, g.pairs.length, Math.max(tries, g.pairs.length), (r, t) => done(Math.round(g.pairs.length * g.pairs.length / t), g.pairs.length)); }
      else { [sel, b].forEach(x => { x.classList.add('shake'); setTimeout(() => x.classList.remove('shake', 'sel'), 450); }); S('wrong'); }
      sel = null;
    });
  }

  function sort(el, g, done) {
    const items = shuffle(g.items); let i = 0, right = 0;
    el.innerHTML = head(g) + `<div class="scard" id="scard"></div><div class="sbuckets">${g.buckets.map((b, k) => `<button class="sbk" data-k="${k}">${esc(b)}</button>`).join('')}</div><div class="sfb" id="sfb"></div>`;
    const card = el.querySelector('#scard'), fb = el.querySelector('#sfb');
    const show = () => { card.textContent = items[i][0]; card.classList.remove('popin'); void card.offsetWidth; card.classList.add('popin'); fb.textContent = `${i + 1} of ${items.length}`; };
    show();
    el.querySelectorAll('.sbk').forEach(b => b.onclick = () => {
      if (i >= items.length) return;
      const ok = +b.dataset.k === items[i][1];
      if (ok) { right++; S('coin'); b.classList.add('flash-ok'); } else { S('wrong'); b.classList.add('flash-no'); fb.innerHTML = `<b>${esc(items[i][0])}</b> goes in <b>${esc(g.buckets[items[i][1]])}</b>`; }
      setTimeout(() => b.classList.remove('flash-ok', 'flash-no'), 400);
      i++;
      setTimeout(() => { if (i < items.length) show(); else { card.remove(); el.querySelector('.sbuckets').remove(); finish(el, right, items.length, done); } }, ok ? 350 : 1300);
    });
  }

  function order(el, g, done) {
    const items = g.items.map((t, i) => ({ t, i })); let sh = shuffle(items); if (sh.every((x, k) => x.i === k)) sh = sh.reverse();
    let next = 0, mistakes = 0;
    el.innerHTML = head(g) + `<p class="sub">${esc(g.prompt)} — tap them in order.</p><div class="otrack" id="otrack"></div><div class="opool">${sh.map(x => `<button class="ochip" data-i="${x.i}">${esc(x.t)}</button>`).join('')}</div>`;
    const track = el.querySelector('#otrack');
    el.querySelectorAll('.ochip').forEach(b => b.onclick = () => {
      if (+b.dataset.i === next) { S('coin'); b.disabled = true; b.classList.add('used'); track.insertAdjacentHTML('beforeend', `${next ? '<span class="oarrow">→</span>' : ''}<span class="ostep popin">${esc(b.textContent)}</span>`); next++;
        if (next === items.length) finish(el, Math.max(0, items.length - mistakes), items.length, done); }
      else { mistakes++; S('wrong'); b.classList.add('shake'); setTimeout(() => b.classList.remove('shake'), 450); }
    });
  }

  /* ◀ Previous / Next ▶ (like the quiz runners): skip a card and come back, revisit an answered card (your answer and
     the reason are shown again), each card is scored once. Finishing with blanks asks once; blanks score 0. */
  const navRow = (i, N, done) => `<div class="tst-nav qnav gnav"><button class="btn ghost gprev" ${i ? '' : 'disabled'} aria-label="Previous">◀ Previous</button>`
    + `<button class="btn ${done ? 'mint' : 'ghost'} tfn" aria-label="${i < N - 1 ? (done ? 'Next' : 'Skip to the next one') : 'Finish'}">${i < N - 1 ? 'Next ▶' : 'Finish ▶'}</button></div>`;
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
    el.innerHTML = head(g, `<span class="gcount" id="tfn0">1 of ${N}</span>`) + `<div class="tfcard" id="tfc"></div><div class="tfwhy" id="tfw" aria-live="polite"></div><div class="tfbtns"><button class="btn tfb" data-v="1">👍 True</button><button class="btn tfb no" data-v="0">👎 False</button></div><div class="gnav"></div>`;
    const c = el.querySelector('#tfc'), w = el.querySelector('#tfw'), btns = el.querySelector('.tfbtns'), cnt = el.querySelector('#tfn0');
    const left = () => ans.filter(a => !a).length;
    const sp = stepper(el, N, i => show(i), () => { c.remove(); w.remove(); btns.remove(); el.querySelector('.gnav').remove(); cnt.remove(); finish(el, ans.filter(a => a && a.ok).length, N, done); });
    const show = i => {
      const it = items[i], a = ans[i];
      c.innerHTML = esc(it[0]) + RA(0); c.className = 'tfcard popin' + (a ? (a.ok ? ' good' : ' bad') : ''); cnt.textContent = `${i + 1} of ${N}`;
      if (a) { w.innerHTML = `<b>${it[1] ? 'TRUE' : 'FALSE'}.</b> ${esc(it[2])}<div class="gpick">You said: <b>${a.v ? 'True' : 'False'}</b> ${a.ok ? '✅' : '❌'}</div>`; btns.style.display = 'none'; }
      else { w.textContent = ''; btns.style.display = ''; }
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
    el.innerHTML = head(g, `<span class="gcount" id="fn0">1 of ${N}</span>`) + `<div class="fsent" id="fs"></div><div class="fopts" id="fo"></div><div class="gnav"></div>`;
    const s = el.querySelector('#fs'), o = el.querySelector('#fo'), cnt = el.querySelector('#fn0');
    const left = () => ans.filter(a => a == null).length;
    const sp = stepper(el, N, i => show(i), () => { s.remove(); o.remove(); el.querySelector('.gnav').remove(); cnt.remove(); finish(el, ans.filter((a, j) => a != null && a === items[j].answer).length, N, done); });
    const show = i => {
      const it = items[i], a = ans[i], ok = a === it.answer;
      s.innerHTML = esc(it.text).replace('___', `<span class="blank${a != null ? (ok ? ' ok' : ' no') : ''}">${a != null ? esc(it.answer) : '?'}</span>`) + RA(); s.className = 'fsent popin'; cnt.textContent = `${i + 1} of ${N}`;
      o.innerHTML = orders[i].map(x => `<button class="opt${a != null && x === it.answer ? ' right' : ''}${a != null && x === a && !ok ? ' wrong' : ''}"${a != null ? ' disabled' : ''}>${esc(x)}</button>`).join('');
      o.querySelectorAll('.opt').forEach(b => b.onclick = () => {
        if (ans[i] != null) return;                              /* scored once */
        ans[i] = b.textContent; S(ans[i] === it.answer ? 'correct' : 'wrong'); show(i);
        const nx = el.querySelector('.tfn'); if (nx) nx.focus({ preventScroll: true });
      });
      sp.wire(a != null, left);
    };
    show(0);
  }

  function speed(el, g, done) {
    const items = shuffle(g.items), answers = items.map(x => String(x.a));
    /* timers: normal, extra time (×2) or none (A11Y.timeScale); the clock also waits while the app is talking */
    const sc = window.A11Y ? A11Y.timeScale() : 1;
    let i = 0, right = 0, t = Math.round(Math.max(20, items.length * 6) * (sc || 1)), timer;
    el.innerHTML = head(g, sc ? `<span class="timer" id="tm" role="timer" aria-label="Seconds left">${t}s</span>` : '<span class="timer" id="tm">No timer</span>') + `<div class="spq" id="spq"></div><div class="fopts" id="spo"></div>`;
    const q = el.querySelector('#spq'), o = el.querySelector('#spo'), tm = el.querySelector('#tm');
    const distract = a => {
      const n = Number(a); const set = new Set([a]);
      if (!isNaN(n) && String(n) === a) [n + 1, n - 1, n + 10, n - 10, n + 2, n * 2].forEach(x => { if (set.size < 3 && x >= 0 && x !== n) set.add(String(x)); });
      shuffle(answers).forEach(x => { if (set.size < 3) set.add(x); });
      return shuffle([...set]);
    };
    const end = () => { clearInterval(timer); q.remove(); o.remove(); finish(el, right, items.length, done); };
    const show = () => { const it = items[i]; q.innerHTML = esc(it.q) + RA(); q.className = 'spq popin';
      o.innerHTML = distract(String(it.a)).map(x => `<button class="opt">${esc(x)}</button>`).join('');
      o.querySelectorAll('.opt').forEach(b => b.onclick = () => { const ok = b.textContent === String(it.a); if (ok) { right++; S('coin'); } else S('wrong'); b.classList.add(ok ? 'right' : 'wrong');
        setTimeout(() => { i++; if (i < items.length) show(); else end(); }, ok ? 250 : 700); }); };
    show();
    if (sc) timer = setInterval(() => { if (!tm.isConnected) { clearInterval(timer); return; } if ((window.ReadAlong && ReadAlong.active) || (window.A11Y && A11Y.holdClock())) return; t--; tm.textContent = t + 's'; if (window.A11Y) A11Y.timerTick(el, t); if (t <= 5) tm.classList.add('hot'); if (t <= 0) end(); }, 1000);
  }

  window.Games = { play: (el, g, done) => ({ match, sort, order, truefalse, fill, speed }[g.type] || ((e, gg, d) => d(0, 0)))(el, g, done), shuffle };
})();
