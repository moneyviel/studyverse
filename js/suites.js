/* ================= 🪐🚀💡 Friendship Galaxy · Rise-Again Rocket · Idea Factory games (js/suites.js) =================
   Played through the Mind Gym game engine (js/mindplay.js); puzzles from js/suites-gen.js. Every answer is checked by
   the app. Looks change by age (j / m / s+CA). Each practice gets levels, a timed run and skill bars in its scorecard. */
(function () {
  'use strict';
  const D = document, $1 = (s, r) => (r || D).querySelector(s);
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const P = () => window.MindPlay;
  const tst = m => { try { toast(m); } catch (e) {} };

  const SUITES = {
    sq: { back: 'Friendship Galaxy', theme: {
        j: { name: 'Friendship Planet', e: '🪐', test: 'Star Friend Challenge', cls: 'pl-j sx-sqj', hero: 'Play fair, share, team up and make sure everyone can join in!' },
        m: { name: 'Galaxy Quest', e: '🌌', test: 'Galaxy Expedition', cls: 'pl-m sx-sqm', hero: 'Fly from planet to planet solving friendship missions.' },
        s: { name: 'Social Lab', e: '🛰️', test: 'People Skills Check', cls: 'pl-s sx-sqs', hero: 'Train fairness, teamwork, respectful talk and conflict-solving.' } },
      games: [
        { id: 'fair', e: '⚖️', skill: 'Fairness', n: { j: 'Fair Share', m: 'Fair Share', s: 'Fair Split' }, d: 'Share treats so every friend gets the same' },
        { id: 'peace', e: '☮️', skill: 'Solving conflicts', n: { j: 'Peace Steps', m: 'Peace Path', s: 'Conflict Resolver' }, d: 'Put the steps of solving a fight in order' },
        { id: 'imsg', e: '💬', skill: 'Respectful talk', n: { j: 'Kind Words', m: 'I-Message Builder', s: 'Assertive Message' }, d: 'Build a calm “I feel…” message, card by card' },
        { id: 'team', e: '🧑‍🤝‍🧑', skill: 'Teamwork', n: { j: 'Team Helpers', m: 'Team Builder', s: 'Team Roles' }, d: 'Give each job to the friend whose strength fits' },
        { id: 'include', e: '🤗', skill: 'Including others', n: { j: 'Everyone Plays', m: 'Everyone Joins', s: 'Inclusive Planner' }, d: 'Pick the plan every friend can join' }] },
    aq: { back: 'Rise-Again Rocket', theme: {
        j: { name: 'Rocket Park', e: '🚀', test: 'Blast-off Challenge', cls: 'pl-j sx-aqj', hero: 'Try, try again! Every mistake helps you fly higher.' },
        m: { name: 'Rise Quest', e: '🌋', test: 'Summit Expedition', cls: 'pl-m sx-aqm', hero: 'Climb the mountain of challenges — one step, one retry at a time.' },
        s: { name: 'Resilience Lab', e: '🧗', test: 'Resilience Check', cls: 'pl-s sx-aqs', hero: 'Train growth thinking, focus, planning, persistence and coping.' } },
      games: [
        { id: 'yet', e: '🌱', skill: 'Growth mindset', n: { j: 'Not Yet!', m: 'Thought Flipper', s: 'Mindset Sorter' }, d: 'Sort thoughts that help you grow from ones that keep you stuck' },
        { id: 'control', e: '🎯', skill: 'Focus on control', n: { j: 'My Control Circle', m: 'Control Circle', s: 'Circle of Control' }, d: 'What can YOU control, and what can’t you?' },
        { id: 'plan', e: '🪜', skill: 'Planning', n: { j: 'Step Ladder', m: 'Step Ladder', s: 'Goal Roadmap' }, d: 'Climb to a goal one step at a time' },
        { id: 'rocket', e: '🚀', skill: 'Persistence', n: { j: 'Rocket Retry', m: 'Rocket Retry', s: 'Launch Lab' }, d: 'Adjust and retry until you land on the planet' },
        { id: 'cope', e: '🧰', skill: 'Coping', n: { j: 'Feel-Better Box', m: 'Coping Toolbox', s: 'Coping Toolkit' }, d: 'Pick the tools that really help after a setback' }] },
    cq: { back: 'Idea Factory', theme: {
        j: { name: 'Idea Playground', e: '🎨', test: 'Spark Challenge', cls: 'pl-j sx-cqj', hero: 'Imagine, wonder and invent — your ideas are superpowers!' },
        m: { name: 'Invention Quest', e: '🏭', test: 'Inventor Expedition', cls: 'pl-m sx-cqm', hero: 'Think like an inventor: new uses, new links, new questions.' },
        s: { name: 'Innovation Lab', e: '🧠', test: 'Creativity Check', cls: 'pl-s sx-cqs', hero: 'Train flexible thinking, connections, invention moves and curiosity.' } },
      games: [
        { id: 'uses', e: '🔄', skill: 'Flexible thinking', n: { j: 'What Else?', m: 'Many Uses', s: 'Alternative Uses' }, d: 'Find clever new uses for everyday things' },
        { id: 'link', e: '🔗', skill: 'Connecting ideas', n: { j: 'Word Glue', m: 'Word Link', s: 'Remote Links' }, d: 'Find the one word that links all three' },
        { id: 'scamper', e: '🛠️', skill: 'Inventing', n: { j: 'Idea Tricks', m: 'Idea Moves', s: 'SCAMPER Lab' }, d: 'Spot the trick that turned something old into an invention' },
        { id: 'curious', e: '🔭', skill: 'Curiosity', n: { j: 'Big Questions', m: 'Question Quest', s: 'Inquiry Sorter' }, d: 'Find the questions that open up new ideas' },
        { id: 'riddle', e: '🧩', skill: 'Seeing differently', n: { j: 'Riddle Fun', m: 'Riddle Lab', s: 'Lateral Thinking' }, d: 'Crack riddles by thinking from a new angle' }] } };

  /* ---------- shared UI pieces ---------- */
  // order: tap tiles into numbered slots
  function order(host, p, list, intro, done, opt) {
    const slots = list.map(() => null);
    host.innerHTML = `${intro}<div class="sx-ord ${opt && opt.ladder ? 'ladder' : ''}"></div><div class="sx-tiles"></div><button type="button" class="btn sx-chk">✓ Check</button>`;
    const draw = rev => {
      $1('.sx-ord', host).innerHTML = slots.map((k, i) => { const t = k != null ? p.tiles[k] : null, cls = rev ? (t === list[i] ? ' ok' : ' no') : '';
        return `<button type="button" class="sx-slot${t ? ' full' : ''}${cls}" data-s="${i}"><b>${i + 1}</b><span>${t ? E(t) : '…'}</span>${rev && t !== list[i] ? `<small>✔ ${E(list[i])}</small>` : ''}</button>`; }).join('');
      $1('.sx-tiles', host).innerHTML = p.tiles.map((t, i) => `<button type="button" class="sx-tile${slots.includes(i) ? ' used' : ''}" data-t="${i}" ${slots.includes(i) || rev ? 'disabled' : ''}>${E(t)}</button>`).join('');
      if (rev) return;
      host.querySelectorAll('[data-t]').forEach(x => x.onclick = () => { const k = slots.indexOf(null); if (k < 0) return; S('tap'); slots[k] = +x.dataset.t; draw(); });
      host.querySelectorAll('[data-s]').forEach(x => x.onclick = () => { const k = +x.dataset.s; if (slots[k] == null) return; S('tap'); slots[k] = null; draw(); });
    };
    draw();
    $1('.sx-chk', host).onclick = () => {
      if (slots.includes(null)) { tst('Place every card first'); return; }
      $1('.sx-chk', host).remove(); draw(true);
      const right = slots.filter((k, i) => p.tiles[k] === list[i]).length;
      done(right === list.length, p.why, null, right / list.length);
    };
  }
  // bins: tap a card, then tap a bin
  function bins(host, p, done) {
    const put = p.items.map(() => null); let held = null;
    host.innerHTML = `<p class="pl-q sx-q">${E(p.q)}</p><div class="sx-cards"></div><div class="sx-bins">${p.bins.map((b, i) => `<button type="button" class="sx-bin b${i}" data-b="${i}"><b>${E(b)}</b><div class="sx-in"></div></button>`).join('')}</div><button type="button" class="btn sx-chk">✓ Check</button>`;
    const draw = rev => {
      $1('.sx-cards', host).innerHTML = p.items.map((it, i) => put[i] == null ? `<button type="button" class="sx-card${held === i ? ' held' : ''}" data-c="${i}" ${rev ? 'disabled' : ''}>${E(it.t)}</button>` : '').join('') || '<p class="sub sx-empty">All sorted — tap a card in a box to move it back.</p>';
      p.bins.forEach((_, b) => { $1(`.sx-bin.b${b} .sx-in`, host).innerHTML = p.items.map((it, i) => put[i] === b ? `<span class="sx-mini${rev ? (it.bin === b ? ' ok' : ' no') : ''}" data-u="${i}">${E(it.t)}</span>` : '').join(''); });
      if (rev) return;
      host.querySelectorAll('[data-c]').forEach(x => x.onclick = e => { e.stopPropagation(); S('tap'); held = held === +x.dataset.c ? null : +x.dataset.c; draw(); });
      host.querySelectorAll('[data-u]').forEach(x => x.onclick = e => { e.stopPropagation(); S('tap'); put[+x.dataset.u] = null; draw(); });
      host.querySelectorAll('[data-b]').forEach(x => x.onclick = () => { if (held == null) { const n = put.findIndex(v => v == null); if (n < 0) return; held = n; } S('open'); put[held] = +x.dataset.b; x.classList.remove('pop'); void x.offsetWidth; x.classList.add('pop'); held = put.findIndex(v => v == null); if (held < 0) held = null; draw(); });
    };
    held = 0; draw();
    $1('.sx-chk', host).onclick = () => {
      if (put.includes(null)) { tst('Sort every card first'); return; }
      $1('.sx-chk', host).remove(); draw(true);
      const right = p.items.filter((it, i) => put[i] === it.bin).length;
      done(right === p.items.length, p.why, null, right / p.items.length);
    };
  }
  // multi: pick exactly N into the box
  function multi(host, p, done) {
    const on = new Set(), box = p.kind === 'cope' ? '🧰' : '💡';
    host.innerHTML = `<p class="pl-q sx-q">${E(p.q)}</p><div class="sx-box"><span>${box}</span><b class="sx-cnt">0 / ${p.need}</b></div><div class="sx-picks"></div><button type="button" class="btn sx-chk">✓ Check</button>`;
    const draw = rev => {
      $1('.sx-cnt', host).textContent = `${on.size} / ${p.need}`;
      $1('.sx-picks', host).innerHTML = p.items.map((it, i) => `<button type="button" class="sx-pk${on.has(i) ? ' on' : ''}${rev ? (it.ok ? ' ok' : on.has(i) ? ' no' : '') : ''}" data-i="${i}" ${rev ? 'disabled' : ''}>${on.has(i) ? '✓ ' : ''}${E(it.t)}</button>`).join('');
      if (rev) return;
      host.querySelectorAll('[data-i]').forEach(x => x.onclick = () => { const i = +x.dataset.i; if (on.has(i)) on.delete(i); else { if (on.size >= p.need) { tst(`Pick only ${p.need}`); return; } on.add(i); } S('tap'); draw(); });
    };
    draw();
    $1('.sx-chk', host).onclick = () => {
      if (on.size !== p.need) { tst(`Pick ${p.need}`); return; }
      $1('.sx-chk', host).remove(); draw(true);
      const right = [...on].filter(i => p.items[i].ok).length;
      done(right === p.need, p.why, null, right / p.need);
    };
  }
  // pick: cards, with optional hint ladder
  function pickOne(host, p, done) {
    let used = 0;
    host.innerHTML = `<p class="pl-q sx-q">${E(p.q)}</p>${p.hints ? `<div class="sx-hints"><button type="button" class="sx-hint">💡 Hint</button><div class="sx-hl"></div></div>` : ''}<div class="hp-opts col">${p.opts.map((o, i) => `<button type="button" class="hp-opt sx-opt" data-i="${i}">${o.e ? `<span>${o.e}</span>` : ''}${E(o.t)}</button>`).join('')}</div>`;
    const hb = $1('.sx-hint', host);
    if (hb) hb.onclick = () => { if (used >= p.hints.length) return; S('open'); $1('.sx-hl', host).insertAdjacentHTML('beforeend', `<p class="sx-h">💡 ${E(p.hints[used])}</p>`); used++; hb.textContent = used < p.hints.length ? '💡 Another hint' : 'No more hints'; if (used >= p.hints.length) hb.disabled = true; };
    host.querySelectorAll('.sx-opt').forEach(x => x.onclick = () => {
      const i = +x.dataset.i, ok = i === p.a;
      host.querySelectorAll('.sx-opt').forEach(y => { y.disabled = true; if (+y.dataset.i === p.a) y.classList.add('ok'); });
      if (!ok) x.classList.add('no'); if (hb) hb.disabled = true;
      done(ok, p.why + (used && ok ? ` (You used ${used} hint${used > 1 ? 's' : ''} — next time try first without!)` : ''), null, ok ? Math.max(.5, 1 - .25 * used) : 0);
    });
  }

  /* ---------- the games ---------- */
  const X = {};
  X.fair = (host, p, done) => {
    const got = p.names.map(() => 0); let bowl = 0, pile = p.total;
    host.innerHTML = `<p class="pl-q sx-q">Share the ${p.total} ${p.t} fairly. Tap a friend’s plate to give one. If some can’t be shared equally, put them in the share bowl.</p>
      <div class="sx-pile"></div><div class="sx-plates"></div><div class="sx-row"><button type="button" class="sx-bowl"></button><button type="button" class="btn ghost sx-reset">↺ Start again</button></div><button type="button" class="btn sx-chk">✓ Check</button>`;
    const draw = rev => {
      $1('.sx-pile', host).innerHTML = pile ? `<span>${p.t.repeat(Math.min(pile, 30))}</span><b>${pile} left</b>` : '<b>All shared!</b>';
      $1('.sx-plates', host).innerHTML = p.names.map((n, i) => `<button type="button" class="sx-plate${rev ? (got[i] === p.each ? ' ok' : ' no') : ''}" data-p="${i}" ${rev ? 'disabled' : ''}><b>${E(n)}</b><span class="sx-pl">${p.t.repeat(got[i]) || '🍽️'}</span><small>${got[i]}</small></button>`).join('');
      const bw = $1('.sx-bowl', host); bw.innerHTML = `🥣 Share bowl: <b>${bowl}</b>`; bw.disabled = !!rev; if (rev) bw.classList.add(bowl === p.left ? 'ok' : 'no');
    };
    draw();
    host.querySelector('.sx-plates').onclick = e => { const b = e.target.closest('[data-p]'); if (!b || !pile) return; S('tap'); got[+b.dataset.p]++; pile--; draw(); };
    $1('.sx-bowl', host).onclick = () => { if (!pile) return; S('tap'); bowl++; pile--; draw(); };
    $1('.sx-reset', host).onclick = () => { S('tap'); got.fill(0); bowl = 0; pile = p.total; draw(); };
    $1('.sx-chk', host).onclick = () => {
      if (pile) { tst('Share every one first'); return; }
      $1('.sx-chk', host).remove(); $1('.sx-reset', host).remove(); draw(true);
      const ok = got.every(g => g === p.each) && bowl === p.left;
      done(ok, p.why);
    };
  };
  X.peace = (host, p, done) => order(host, p, p.steps, `<div class="hp-event">⚡ ${E(p.sit)}</div><p class="pl-q sx-q">Put the peace steps in order — tap the first step first.</p>`, done);
  X.plan = (host, p, done) => order(host, p, p.steps, `<div class="hp-event">🏁 Goal: ${E(p.goal)}</div><p class="pl-q sx-q">Build the ladder: tap the FIRST step first.</p>`, done, { ladder: 1 });
  X.imsg = (host, p, done) => {
    const ch = p.slots.map(() => null);
    host.innerHTML = `<div class="hp-event">😕 ${E(p.sit)}</div><p class="pl-q sx-q">Build a calm message. Pick one card for each part.</p><div class="sx-say"></div><div class="sx-slots"></div><button type="button" class="btn sx-chk">✓ Check</button>`;
    const draw = rev => {
      $1('.sx-say', host).innerHTML = '🗨️ ' + p.slots.map((s, i) => `<span class="${ch[i] == null ? 'gap' : rev ? (s.opts[ch[i]].ok ? 'ok' : 'no') : 'fill'}">${s.lab.replace('…', '')} ${ch[i] == null ? '____' : E(s.opts[ch[i]].t)}</span>`).join(' ');
      $1('.sx-slots', host).innerHTML = p.slots.map((s, i) => `<div class="sx-sl"><b>${E(s.lab)}</b>${s.opts.map((o, k) => `<button type="button" class="sx-chip${ch[i] === k ? ' on' : ''}${rev ? (o.ok ? ' ok' : ch[i] === k ? ' no' : '') : ''}" data-s="${i}" data-k="${k}" ${rev ? 'disabled' : ''}>${E(o.t)}</button>`).join('')}</div>`).join('');
      if (rev) return;
      host.querySelectorAll('.sx-chip').forEach(x => x.onclick = () => { S('tap'); ch[+x.dataset.s] = +x.dataset.k; draw(); });
    };
    draw();
    $1('.sx-chk', host).onclick = () => {
      if (ch.includes(null)) { tst('Pick a card for every part'); return; }
      $1('.sx-chk', host).remove(); draw(true);
      const right = ch.filter((k, i) => p.slots[i].opts[k].ok).length;
      done(right === p.slots.length, p.why, null, right / p.slots.length);
    };
  };
  X.team = (host, p, done) => {
    const give = p.tasks.map(() => null); let held = null;
    host.innerHTML = `<p class="pl-q sx-q">Tap a job, then tap the friend who is best at it.</p><div class="sx-jobs"></div><div class="sx-team"></div><button type="button" class="btn sx-chk">✓ Check</button>`;
    const draw = rev => {
      $1('.sx-jobs', host).innerHTML = p.tasks.map((t, i) => give[i] == null ? `<button type="button" class="sx-card${held === i ? ' held' : ''}" data-j="${i}">${E(t.t)}</button>` : '').join('') || '<p class="sub sx-empty">All jobs given!</p>';
      $1('.sx-team', host).innerHTML = p.people.map((pp, k) => { const j = give.findIndex(g => g === k), cls = rev ? (j >= 0 && p.tasks[j].skill === pp.skill ? ' ok' : ' no') : '';
        return `<button type="button" class="sx-mate${cls}" data-m="${k}" ${rev ? 'disabled' : ''}><span class="sx-me">${pp.e}</span><b>${E(pp.name)}</b><small>loves ${E(pp.skill)}</small><em>${j >= 0 ? E(p.tasks[j].t) : '＋ job'}</em></button>`; }).join('');
      if (rev) return;
      host.querySelectorAll('[data-j]').forEach(x => x.onclick = () => { S('tap'); held = +x.dataset.j; draw(); });
      host.querySelectorAll('[data-m]').forEach(x => x.onclick = () => { const k = +x.dataset.m; const was = give.findIndex(g => g === k);
        if (held == null) { if (was >= 0) { give[was] = null; S('tap'); draw(); } return; }
        if (was >= 0) give[was] = null; give[held] = k; held = null; S('open'); draw(); });
    };
    draw();
    $1('.sx-chk', host).onclick = () => {
      if (give.includes(null)) { tst('Give every job to someone'); return; }
      $1('.sx-chk', host).remove(); draw(true);
      const right = p.tasks.filter((t, i) => p.people[give[i]].skill === t.skill).length;
      done(right === p.tasks.length, p.why, null, right / p.tasks.length);
    };
  };
  X.include = (host, p, done) => pickOne(host, Object.assign({}, p, { q: `Plan something for your friends:\n${p.friends.map(f => '• ' + f).join('\n')}\nWhich plan lets EVERYONE join?` }), done);
  X.yet = X.control = X.curious = bins; X.cope = X.uses = multi; X.scamper = X.riddle = pickOne;
  X.link = (host, p, done) => {
    const typed = [];
    const j = P().band() === 'j';
    host.innerHTML = `<p class="pl-q sx-q">${j ? 'Which word joins each picture-word to make a new word?' : 'Find ONE word that goes with all three.'}</p>
      <div class="sx-three">${p.words.map(w => `<span class="sx-w">${E(w)}</span>`).join('<i>＋</i>')}</div><div class="pl-slots sx-ans"></div><div class="pl-tiles sx-lt"></div><div class="pl-row2"><button type="button" class="btn ghost sx-back">⌫</button><button type="button" class="btn sx-chk">✓ Check</button></div>`;
    const draw = rev => {
      $1('.sx-ans', host).innerHTML = Array.from({ length: p.answer.length }, (_, i) => `<span class="pl-slot${typed[i] != null ? ' full' : ''}">${typed[i] != null ? p.tiles[typed[i]] : ''}</span>`).join('');
      $1('.sx-lt', host).innerHTML = p.tiles.map((c, i) => `<button type="button" class="pl-tile${typed.includes(i) ? ' used' : ''}" data-l="${i}" ${typed.includes(i) || rev ? 'disabled' : ''}>${c}</button>`).join('');
      if (rev) return;
      host.querySelectorAll('[data-l]').forEach(x => x.onclick = () => { if (typed.length >= p.answer.length) return; S('tap'); typed.push(+x.dataset.l); draw(); });
    };
    draw();
    $1('.sx-back', host).onclick = () => { typed.pop(); S('tap'); draw(); };
    $1('.sx-chk', host).onclick = () => {
      if (typed.length !== p.answer.length) { tst(`The word has ${p.answer.length} letters`); return; }
      const w = typed.map(i => p.tiles[i]).join(''), ok = w === p.answer;
      host.querySelectorAll('button').forEach(b => b.disabled = true); $1('.sx-ans', host).classList.add(ok ? 'win' : 'shake');
      done(ok, p.why);
    };
  };
  X.rocket = (host, p, done) => {
    const G = window.SuitesGen; let ang = 45, pw = 25, left = p.tries, used = 0, over = false;
    const W = 100, H = 60, sx = x => x * 3, sy = y => 180 - y * 3;
    host.innerHTML = `<p class="pl-q sx-q">Land your rocket on the planet! Change the angle and power, then launch. ${p.wind ? `<b>Space wind blows ${p.wind > 0 ? 'forward ➡' : 'back ⬅'}.</b>` : ''}</p>
      <svg viewBox="0 0 300 190" class="sx-space" aria-label="Rocket launch area"><defs><radialGradient id="sxPl"><stop offset="0" stop-color="#ffd166"/><stop offset="1" stop-color="#e0408f"/></radialGradient></defs>
      ${Array.from({ length: 26 }, () => `<circle cx="${Math.random() * 300}" cy="${Math.random() * 150}" r="${Math.random() * 1.4 + .3}" fill="#fff" opacity=".8"/>`).join('')}
      <rect x="0" y="180" width="300" height="10" fill="#3b2f6b"/><ellipse cx="${sx(p.tx)}" cy="182" rx="${sx(p.tw / 2)}" ry="9" fill="url(#sxPl)"/><text x="${sx(p.tx)}" y="172" text-anchor="middle" font-size="16">🪐</text>
      <g class="sx-trails"></g><text x="6" y="178" font-size="18" class="sx-launcher">🚀</text></svg>
      <div class="sx-ctl"><label>Angle <b class="sx-av">45°</b><input type="range" min="15" max="75" step="5" value="45" class="sx-ang"></label><label>Power <b class="sx-pv">25</b><input type="range" min="10" max="40" step="1" value="25" class="sx-pow"></label></div>
      <div class="sx-row"><span class="sx-left">🚀 × ${left}</span><button type="button" class="btn sx-go">🚀 Launch!</button></div><p class="sx-msg" aria-live="polite"></p>`;
    const a = $1('.sx-ang', host), pv = $1('.sx-pow', host);
    a.oninput = () => { ang = +a.value; $1('.sx-av', host).textContent = ang + '°'; }; pv.oninput = () => { pw = +pv.value; $1('.sx-pv', host).textContent = pw; };
    $1('.sx-go', host).onclick = () => {
      if (over) return; S('open'); used++; left--; $1('.sx-left', host).textContent = `🚀 × ${left}`;
      const f = G.flight(ang, pw, p.wind), pts = f.pts.filter((_, i) => i % 3 === 0).map(([x, y]) => `${sx(Math.min(x, W)).toFixed(1)},${sy(Math.min(y, H)).toFixed(1)}`).join(' ');
      const tr = $1('.sx-trails', host); tr.querySelectorAll('polyline').forEach(l => l.setAttribute('opacity', '.35'));
      tr.insertAdjacentHTML('beforeend', `<polyline points="${pts}" fill="none" stroke="#ffd166" stroke-width="2" stroke-dasharray="4 3" class="sx-trail"/><text x="${sx(Math.min(f.land, W - 2))}" y="186" font-size="12" text-anchor="middle">💥</text>`);
      const diff = f.land - p.tx, hit = Math.abs(diff) <= p.tw / 2, msg = $1('.sx-msg', host);
      if (hit) { over = true; msg.innerHTML = `🎉 Landed in ${used} ${used === 1 ? 'try' : 'tries'}!`; S('right'); finish(true); return; }
      msg.innerHTML = `${diff > 0 ? '⬅ Too far' : '➡ Too short'} by ${Math.abs(diff).toFixed(0)}. ${left ? 'Adjust and try again — every miss tells you something!' : ''}`;
      if (!left) { over = true; finish(false); }
    };
    function finish(ok) {
      host.querySelectorAll('input,.sx-go').forEach(x => x.disabled = true);
      done(ok, ok ? `You used each miss as information — that’s persistence! A pro tip: change ONE thing at a time (just power, or just angle) to learn what it does.` : 'So close! Persistence means each miss teaches you: too short → more power or a better angle. Try the level again.', null, ok ? Math.max(.4, 1 - (used - 1) / p.tries) : 0);
    }
  };

  function style() {
    if (D.getElementById('sxCss')) return;
    D.head.insertAdjacentHTML('beforeend', `<style id="sxCss">
      .sx-sqj{--plh:linear-gradient(135deg,#6dd5ed,#a17fe0);--plc:#7b5cff}.sx-sqm{--plh:linear-gradient(135deg,#1e3c72,#6a3093);--plc:#5b6cff}.sx-sqs{--plh:linear-gradient(135deg,#0f2027,#2c5364);--plc:#3fa7d6}
      .sx-aqj{--plh:linear-gradient(135deg,#ff9a3c,#ff5e62);--plc:#ff5e62}.sx-aqm{--plh:linear-gradient(135deg,#f12711,#f5af19);--plc:#e8590c}.sx-aqs{--plh:linear-gradient(135deg,#232526,#5a3f37);--plc:#ff8a3c}
      .sx-cqj{--plh:linear-gradient(135deg,#f6d365,#fda085);--plc:#f08a24}.sx-cqm{--plh:linear-gradient(135deg,#11998e,#38ef7d);--plc:#11998e}.sx-cqs{--plh:linear-gradient(135deg,#141e30,#243b55);--plc:#ffc43d}
      .sx-q{white-space:pre-line}.sx-ord{display:flex;flex-direction:column;gap:6px;margin:8px 0}.sx-ord.ladder{flex-direction:column-reverse}
      .sx-slot{display:flex;gap:8px;align-items:center;text-align:left;border:2px dashed var(--plc);border-radius:12px;background:#fff;padding:8px 10px;cursor:pointer;font-family:inherit;color:#1f2d33;flex-wrap:wrap}
      .sx-slot b{width:26px;height:26px;border-radius:50%;background:var(--plc);color:#fff;display:grid;place-items:center;flex:none}.sx-slot span{flex:1;font-weight:700}.sx-slot.full{border-style:solid;background:#fff8e6}
      .sx-slot.ok{background:#e6f7ef;border-color:#1e9e6a}.sx-slot.no{background:#fdeaea;border-color:#e45}.sx-slot small{width:100%;color:#1e9e6a;font-weight:700;padding-left:34px}
      .sx-ord.ladder .sx-slot{border-left-width:8px}
      .sx-tiles,.sx-cards,.sx-jobs,.sx-picks{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:10px 0}
      .sx-tile,.sx-card{border:0;border-radius:14px;padding:10px 12px;background:var(--plc);color:#fff;font-weight:700;font-size:14px;cursor:pointer;font-family:inherit;box-shadow:0 4px 0 rgba(0,0,0,.2);animation:mpPop .3s both;text-align:left;max-width:100%}
      .sx-tile.used{visibility:hidden}.sx-card.held{outline:3px solid #ffc43d;transform:translateY(-3px) rotate(-1.5deg)}.sx-empty{margin:4px}
      .sx-bins{display:grid;grid-template-columns:1fr 1fr;gap:8px}.sx-bin{border:3px dashed var(--plc);border-radius:18px;background:rgba(255,255,255,.9);min-height:110px;padding:8px;cursor:pointer;font-family:inherit;color:#1f2d33;display:flex;flex-direction:column;gap:6px;align-items:stretch}
      .sx-bin.b1{border-color:#9aa3b5}.sx-bin.pop{animation:plHit .3s}.sx-bin b{font-size:14px}.sx-in{display:flex;flex-direction:column;gap:4px}.sx-mini{font-size:12px;background:#f1edff;border-radius:8px;padding:4px 6px;text-align:left}.sx-mini.ok{background:#d6f5e6}.sx-mini.no{background:#fde2e2}
      .sx-box{display:flex;align-items:center;gap:10px;justify-content:center;font-size:30px;margin:4px 0}.sx-box b{font-size:16px;color:var(--plc)}
      .sx-pk{border:2px solid rgba(0,0,0,.1);border-radius:999px;padding:9px 13px;background:#fff;color:#1f2d33;font-weight:700;font-size:14px;cursor:pointer;font-family:inherit}.sx-pk.on{background:var(--plc);color:#fff;border-color:var(--plc)}.sx-pk.ok{border-color:#1e9e6a;box-shadow:0 0 0 2px #1e9e6a inset}.sx-pk.no{background:#fde2e2;color:#7a1b1b}
      .sx-pile{text-align:center;padding:8px;border-radius:14px;background:#fff8e6;margin-bottom:8px}.sx-pile span{display:block;font-size:22px;letter-spacing:2px;word-break:break-all}
      .sx-plates{display:grid;grid-template-columns:repeat(auto-fit,minmax(90px,1fr));gap:8px}.sx-plate{border:0;border-radius:50% 50% 18px 18px;background:#fff;box-shadow:0 4px 12px rgba(0,0,0,.12);padding:10px 6px;cursor:pointer;font-family:inherit;color:#1f2d33;display:flex;flex-direction:column;align-items:center;gap:4px}
      .sx-pl{font-size:18px;min-height:26px;word-break:break-all}.sx-plate.ok{background:#e6f7ef}.sx-plate.no{background:#fde2e2}
      .sx-row{display:flex;gap:8px;align-items:center;justify-content:space-between;margin:10px 0}.sx-bowl{border:0;border-radius:14px;padding:10px 12px;background:#fff1d6;cursor:pointer;font-family:inherit;font-weight:700}.sx-bowl.ok{background:#d6f5e6}.sx-bowl.no{background:#fde2e2}
      .sx-say{padding:12px;border-radius:16px;background:#fff;line-height:1.6;font-weight:600;box-shadow:inset 0 0 0 2px #e7e2ff;margin:6px 0}.sx-say .gap{color:#99a}.sx-say .fill{color:var(--plc)}.sx-say .ok{color:#1e9e6a}.sx-say .no{color:#d33;text-decoration:line-through}
      .sx-sl{margin:8px 0}.sx-sl>b{display:block;font-size:13px;margin-bottom:4px}.sx-chip{border:2px solid rgba(0,0,0,.1);border-radius:12px;padding:8px 10px;margin:0 6px 6px 0;background:#fff;cursor:pointer;font-family:inherit;font-size:14px;text-align:left;color:#1f2d33}
      .sx-chip.on{background:var(--plc);color:#fff;border-color:var(--plc)}.sx-chip.ok{border-color:#1e9e6a;box-shadow:0 0 0 2px #1e9e6a inset}.sx-chip.no{background:#fde2e2;color:#7a1b1b}
      .sx-team{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px}.sx-mate{border:0;border-radius:18px;background:#fff;box-shadow:0 4px 12px rgba(0,0,0,.12);padding:10px;cursor:pointer;font-family:inherit;color:#1f2d33;display:flex;flex-direction:column;align-items:center;gap:2px}
      .sx-me{font-size:30px}.sx-mate small{color:#667}.sx-mate em{font-style:normal;font-size:12px;font-weight:700;color:var(--plc);text-align:center}.sx-mate.ok{background:#e6f7ef}.sx-mate.no{background:#fde2e2}
      .sx-three{display:flex;align-items:center;justify-content:center;gap:6px;flex-wrap:wrap;margin:8px 0}.sx-w{padding:10px 12px;border-radius:12px;background:#fff;font-weight:900;letter-spacing:1px;box-shadow:0 3px 10px rgba(0,0,0,.1);color:#1f2d33}.sx-three i{font-style:normal;color:var(--plc);font-weight:900}
      .sx-ans.win .pl-slot{background:#d6f5e6}.sx-ans.shake{animation:mgShake .4s}
      .sx-hints{margin:6px 0}.sx-hint{border:0;border-radius:999px;background:#fff1c2;padding:7px 12px;font-weight:800;cursor:pointer;font-family:inherit}.sx-h{margin:6px 0;padding:8px 10px;border-radius:10px;background:#fffbe6;font-size:14px;color:#5a4300}
      .sx-space{width:100%;border-radius:16px;background:linear-gradient(#0b1033,#2a1d5c)}.sx-trail{animation:sxDraw 1.1s ease-out both;stroke-dashoffset:0}
      .sx-ctl{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px}.sx-ctl label{display:flex;flex-direction:column;font-weight:700;font-size:13px}.sx-ctl input{width:100%;accent-color:var(--plc)}
      .sx-left{font-weight:900}.sx-msg{min-height:20px;font-weight:700;text-align:center}
      .pl-s .sx-slot,.pl-s .sx-bin,.pl-s .sx-pk,.pl-s .sx-chip,.pl-s .sx-mate,.pl-s .sx-plate,.pl-s .sx-say,.pl-s .sx-w{background:#232a48;color:#eef}.pl-s .sx-mini{background:#2f3760;color:#eef}.pl-s .sx-pile{background:#2a2350}
      @keyframes sxDraw{from{opacity:0}to{opacity:1}}
    </style>`);
  }

  function boot() {
    if (!window.MindPlay || !window.SuitesGen || !window.MindGym) return setTimeout(boot, 200);
    Object.assign(MindPlay.PLAY, X); style();
    Object.entries(SUITES).forEach(([id, c]) => MindPlay.addSuite({ id, test: id, theme: c.theme, games: c.games, gen: () => ({ make: (g, b, l) => window.SuitesGen.make(g, MindGym._band() === 'p' ? 'p' : b, l) }), back: () => MindGym.open(), backLabel: 'Mind Gym', store: id + 'tests', kind: g => g.skill }));
  }
  boot();
  window.SuitesUI = { SUITES };
})();
