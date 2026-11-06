/* ================= Easier navigation =================
   Search any topic · Map/List view of chapters with filters · Bookmarked questions · Analysis */
(function () {
  const pct = (a, b) => b ? Math.round(a / b * 100) : 0;
  function topicAcc(t) { let s = 0, w = 0; t.quiz.forEach((q, i) => { const x = ST.qstats[`${t.id}#${i}`]; if (x) { s += x.s; w += x.w; } }); return { s, w }; }
  function chStats(c) {
    let done = 0, s = 0, w = 0; c.topics.forEach(t => { if (ST.topics[t.id]) done++; const a = topicAcc(t); s += a.s; w += a.w; });
    const acc = s ? pct(s - w, s) : null;
    const state = !done && !s ? 'new' : done === c.topics.length ? 'done' : 'going';
    return { done, n: c.topics.length, acc, attempts: s, weak: acc !== null && acc < 60, state };
  }

  /* ---------- search on the world map ---------- */
  const _world = worldScreen;
  worldScreen = async function () {
    await _world();
    const hello = $('#worldTitle'); if (!hello || document.getElementById('gSearch')) return;
    const anchor = document.getElementById('q3bar') || hello;
    anchor.insertAdjacentHTML('afterend', `<div class="gsearch" id="gSearch"><span>🔍</span><input id="gsIn" placeholder="Search any topic… e.g. fractions, photosynthesis" autocomplete="off" aria-label="Search topics"></div><div id="gsRes" class="gs-res"></div>`);
    let tm; $('#gsIn').oninput = e => { clearTimeout(tm); const v = e.target.value.trim(); tm = setTimeout(() => results(v), 250); };
  };
  async function results(v) {
    const box = $('#gsRes'); if (!box) return;
    if (v.length < 2 || !window.Ask) { box.innerHTML = ''; return; }
    const hits = (await Ask.search(v)).slice(0, 8);
    box.innerHTML = hits.length ? hits.map(h => `<button class="gs-hit" data-s="${h.t.s}" data-c="${h.t.ci}" data-t="${h.t.ti}"><b>${esc(h.t.t)}</b><small>${esc((Worlds.SUBJECT_STYLE[h.t.s] || {}).e || '📘')} ${esc(h.t.sn)} · ${esc(h.t.ch)}</small></button>`).join('') : '<p class="sub gs-none">No topic found. Try other words.</p>';
    box.querySelectorAll('.gs-hit').forEach(b => b.onclick = () => playTopic(b.dataset.s, +b.dataset.c, +b.dataset.t));
  }

  /* ---------- subject: map or list ---------- */
  ST.view = ST.view || 'map';
  const _subject = subjectScreen;
  subjectScreen = async function (sid) {
    await _subject(sid);
    const g = ST.profile.grade, d = await subjectData(g, sid); if (!d) return;
    document.getElementById('viewTgl')?.remove(); document.getElementById('chList')?.remove();
    $('#subTitle').insertAdjacentHTML('afterend', `<div class="viewtgl" id="viewTgl" role="tablist"><button data-v="map" role="tab">🗺️ Map</button><button data-v="list" role="tab">☰ Chapter list</button></div>`);
    const draw = () => {
      document.querySelectorAll('#viewTgl button').forEach(b => { b.classList.toggle('on', b.dataset.v === ST.view); b.setAttribute('aria-selected', b.dataset.v === ST.view); });
      $('#cmap').style.display = ST.view === 'map' ? '' : 'none';
      document.getElementById('chList')?.remove(); if (ST.view !== 'list') return;
      const rows = d.chapters.map((c, i) => ({ c, i, st: chStats(c) }));
      $('#cmap').insertAdjacentHTML('afterend', `<div id="chList"><div class="chfilter">${[['all', 'All'], ['new', 'Not started'], ['going', 'In progress'], ['weak', 'Weak'], ['done', 'Completed']].map(([k, n], j) => `<button data-f="${k}" class="${j ? '' : 'on'}">${n}</button>`).join('')}</div>
        ${rows.map(({ c, i, st }) => `<button class="chrow" data-i="${i}" data-st="${st.state}" data-weak="${st.weak ? 1 : 0}"><span class="chn">${c.n}</span><span class="chm"><b>${esc(c.title)}</b><small>${st.done}/${st.n} topics${st.acc !== null ? ` · ${st.acc}% accuracy` : ''}${st.weak ? ' · ⚠️ weak' : ''}</small><i class="chbar"><i style="width:${pct(st.done, st.n)}%"></i></i></span><span class="chgo">›</span></button>`).join('')}</div>`);
      document.querySelectorAll('#chList .chrow').forEach(r => r.onclick = () => chapterScreen(sid, +r.dataset.i));
      document.querySelectorAll('#chList .chfilter button').forEach(b => b.onclick = () => { document.querySelectorAll('#chList .chfilter button').forEach(x => x.classList.toggle('on', x === b)); const f = b.dataset.f;
        document.querySelectorAll('#chList .chrow').forEach(r => r.style.display = f === 'all' || (f === 'weak' ? r.dataset.weak === '1' : r.dataset.st === f) ? '' : 'none'); });
    };
    document.querySelectorAll('#viewTgl button').forEach(b => b.onclick = () => { ST.view = b.dataset.v; save(); draw(); });
    draw();
  };

  /* ---------- bookmarks practice ---------- */
  const _practice = practiceScreen;
  practiceScreen = async function () {
    await _practice();
    const g = ST.profile.grade, ks = Object.keys(ST.bm || {}).filter(k => k.startsWith(`g${g}-`));
    const first = document.querySelector('#s-practice .card'); if (!first) return;
    first.insertAdjacentHTML('afterend', `<div class="card"><h3>🔖 Bookmarked questions</h3><p class="sub">${ks.length ? `${ks.length} saved. Practise them any time.` : 'Tap 🔖 on any question to save it here.'}</p>${ks.length ? '<button class="btn ghost" id="pBm">Practise bookmarks ▶</button>' : ''}</div>`);
    if (ks.length) $('#pBm').onclick = async () => {
      const list = []; for (const k of ks) { const [tid, i] = k.split('#'); const m = /^g(\d+)-([a-z]+)-(\d+)-(\d+)$/.exec(tid); if (!m) continue; const d = await subjectData(+m[1], m[2]); const t = d && d.chapters[+m[3] - 1] && d.chapters[+m[3] - 1].topics.find(x => x.id === tid) || (d && d.chapters.flatMap(c => c.topics).find(x => x.id === tid)); if (t && t.quiz[+i]) list.push({ q: t.quiz[+i], qid: k }); }
      if (!list.length) return; RUN = null; const host = $('#s-practice'); host.innerHTML = '<div id="pBody"></div>';
      quizRunner($('#pBody'), list, r => { $('#pBody').innerHTML = `<div class="card done-card"><div class="gbig">🔖</div><h2>${r.right} / ${r.total}</h2><button class="btn" id="bmBack">Back</button></div>`; $('#bmBack').onclick = practiceScreen; });
    };
  };

  /* ---------- analysis on Me ---------- */
  const _me = meScreen;
  meScreen = function () {
    _me();
    const g = ST.profile.grade, host = document.querySelector('#s-me'); if (!host) return;
    host.insertAdjacentHTML('beforeend', `<div class="card" id="anCard"><h3>📊 My analysis</h3><div id="anBody"><p class="sub">Loading…</p></div></div>`);
    (async () => {
      const subs = curSubjects(g); const rows = [];
      for (const s of subs) { const d = await subjectData(g, s.id); if (!d) continue; let done = 0, n = 0, at = 0, w = 0; const weak = [];
        d.chapters.forEach((c, i) => { const st = chStats(c); done += st.done; n += st.n; at += st.attempts; w += st.attempts && st.acc !== null ? Math.round(st.attempts * (100 - st.acc) / 100) : 0; if (st.weak) weak.push(c.title); });
        rows.push({ s, done, n, at, acc: at ? pct(at - w, at) : null, weak }); }
      const tests = Object.entries(ST.tests || {}).filter(([k]) => k.startsWith(`g${g}-`)).sort((a, b) => (b[1].d || '').localeCompare(a[1].d || '')).slice(0, 8);
      const el = document.getElementById('anBody'); if (!el) return;
      el.innerHTML = rows.map(r => `<div class="anrow"><div><b>${(Worlds.SUBJECT_STYLE[r.s.id] || {}).e || '📘'} ${esc(r.s.name)}</b><small>${r.done}/${r.n} topics · ${r.at} answers${r.acc !== null ? ` · ${r.acc}% correct` : ''}</small>${r.weak.length ? `<small class="anweak">⚠️ Weak: ${esc(r.weak.slice(0, 3).join(', '))}</small>` : ''}</div><i class="chbar"><i style="width:${pct(r.done, r.n)}%"></i></i></div>`).join('')
        + `<h3 style="margin-top:12px">🧾 Test history</h3>${tests.length ? tests.map(([k, t]) => `<div class="anrow"><div><b>${esc(k.replace(/^g\d+-/, '').replace(/-(\d+)$/, (m, c) => ' · chapter ' + (+c + 1)))}</b><small>${t.d} · ${t.pct}% score · readiness ${t.ready}%</small></div></div>`).join('') : '<p class="sub">No tests yet. Try a chapter test!</p>'}`;
    })();
  };
})();
