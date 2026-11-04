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

  function truefalse(el, g, done) {
    const items = shuffle(g.items); let i = 0, right = 0;
    el.innerHTML = head(g) + `<div class="tfcard" id="tfc"></div><div class="tfwhy" id="tfw"></div><div class="tfbtns"><button class="btn tfb" data-v="1">👍 True</button><button class="btn tfb no" data-v="0">👎 False</button></div>`;
    const c = el.querySelector('#tfc'), w = el.querySelector('#tfw'), btns = el.querySelector('.tfbtns');
    const show = () => { c.innerHTML = esc(items[i][0]) + RA(0); c.className = 'tfcard popin'; w.textContent = ''; btns.style.display = ''; };
    show();
    el.querySelectorAll('.tfb').forEach(b => b.onclick = () => {
      const ok = (b.dataset.v === '1') === items[i][1];
      if (ok) { right++; S('correct'); } else S('wrong');
      c.classList.add(ok ? 'good' : 'bad');
      w.innerHTML = `<b>${items[i][1] ? 'TRUE' : 'FALSE'}.</b> ${esc(items[i][2])}`; btns.style.display = 'none';
      w.insertAdjacentHTML('beforeend', `<button class="btn ghost tfn">${i < items.length - 1 ? 'Next ▶' : 'Finish ▶'}</button>`);
      w.querySelector('.tfn').onclick = () => { i++; if (i < items.length) show(); else { c.remove(); w.remove(); btns.remove(); finish(el, right, items.length, done); } };
    });
  }

  function fill(el, g, done) {
    const items = g.items; let i = 0, right = 0;
    el.innerHTML = head(g) + `<div class="fsent" id="fs"></div><div class="fopts" id="fo"></div>`;
    const s = el.querySelector('#fs'), o = el.querySelector('#fo');
    const show = () => {
      const it = items[i];
      s.innerHTML = esc(it.text).replace('___', '<span class="blank">?</span>') + RA(); s.className = 'fsent popin';
      o.innerHTML = shuffle(it.options).map(x => `<button class="opt">${esc(x)}</button>`).join('');
      o.querySelectorAll('.opt').forEach(b => b.onclick = () => {
        const ok = b.textContent === it.answer; o.querySelectorAll('.opt').forEach(x => { x.disabled = true; if (x.textContent === it.answer) x.classList.add('right'); });
        if (ok) { right++; S('correct'); } else { b.classList.add('wrong'); S('wrong'); }
        s.querySelector('.blank').textContent = it.answer; s.querySelector('.blank').classList.add(ok ? 'ok' : 'no');
        setTimeout(() => { i++; if (i < items.length) show(); else { s.remove(); o.remove(); finish(el, right, items.length, done); } }, ok ? 900 : 1700);
      });
    };
    show();
  }

  function speed(el, g, done) {
    const items = shuffle(g.items), answers = items.map(x => String(x.a));
    let i = 0, right = 0, t = Math.max(20, items.length * 6), timer;
    el.innerHTML = head(g, `<span class="timer" id="tm">${t}s</span>`) + `<div class="spq" id="spq"></div><div class="fopts" id="spo"></div>`;
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
    timer = setInterval(() => { if (window.ReadAlong && ReadAlong.active) return; t--; tm.textContent = t + 's'; if (t <= 5) tm.classList.add('hot'); if (t <= 0) end(); }, 1000);
  }

  window.Games = { play: (el, g, done) => ({ match, sort, order, truefalse, fill, speed }[g.type] || ((e, gg, d) => d(0, 0)))(el, g, done), shuffle };
})();
