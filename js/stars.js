/* ================= Stars ⭐ and streak 🔥 explained =================
   The ⭐ and 🔥 pills in the top bar are buttons. They open a sheet that tells the student, in simple words:
   - Stars: what they are (XP for learning), stars today and this week (from ST.xpLog, written by addXP in js/app.js),
     the full earning table (it follows the real addXP calls in the app — keep it in step when those change),
     and what stars do (daily goal, squad, badges).
   - Streak: how it counts, what counts as a study day, today's status, best streak, the last 7 days.
   Works in the school and CA looks. window.Stars = { open, streak, close } */
(function () {
  const D = document;
  const isCA = () => { try { return !!(ST.profile && ST.profile.course === 'ca'); } catch (e) { return false; } };
  const dkey = d => d.toISOString().slice(0, 10);
  const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const log = () => (ST.xpLog && typeof ST.xpLog === 'object' ? ST.xpLog : {});
  function week() {              // Monday … Sunday of this week, as the app's day keys (today())
    const t = new Date(today() + 'T00:00:00Z'), dow = (t.getUTCDay() + 6) % 7, out = [];
    for (let i = 0; i < 7; i++) { const d = new Date(t.getTime() + (i - dow) * 864e5); out.push(dkey(d)); }
    return out;
  }
  function last7() { const t = new Date(today() + 'T00:00:00Z'), out = []; for (let i = 6; i >= 0; i--) out.push(dkey(new Date(t.getTime() - i * 864e5))); return out; }
  const dayName = k => new Date(k + 'T00:00:00Z').toLocaleDateString('en-IN', { weekday: 'short', timeZone: 'UTC' });
  const dateName = k => new Date(k + 'T00:00:00Z').toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'UTC' });
  /* when the app's day changes in the student's own clock (today() is the UTC date: 5:30 am in India) */
  function dayTurn() { const t = new Date(); t.setUTCHours(24, 0, 0, 0); if (t.getHours() === 0 && t.getMinutes() === 0) return ''; return t.toLocaleTimeString('en-IN', { hour: 'numeric', minute: '2-digit' }); }

  /* ---------- the earning table — mirrors every addXP() call in js/*.js ---------- */
  const SCHOOL = [
    ['🗺️ Quests', [
      ['Read the Learn page, then tap Let’s play / Start quiz', '+5'],
      ['Mini-game inside a quest', '2 per point you score (at least 5)'],
      ['Quiz question right — in quests, Daily Practice, Memory Garden, duels and bookmarks', '+10 each'],
      ['Teach Gappu (explain it in your own words)', '+25, once per quest'],
      ['Lab challenge in “Try it yourself” 🧪', '+15'],
      ['Endless practice ♾️ question right', '+2 each']]],
    ['🎯 Practice & tests', [
      ['Memory Garden watering 💧 (on top of +10 per right answer)', '+5 per right answer'],
      ['Chapter or subject test 📝', '3 per right answer, +20 bonus if you score 90% or more'],
      ['Arcade games 🎮', '5, plus 5 for each star you win (up to 20)'],
      ['👾 Boss of the week question right', '+10 each'],
      ['📖 Story mode question right', '+5 each (bonus the first time you finish a story)']]],
  ];
  const CA = [
    ['📘 CA units', [
      ['Finish a unit step for the first time (Learn, Examples, On the job, MCQ, Write, Revise)', '+5 each step'],
      ['Written answer checked', 'your marks ÷ total × 20 (at least 5)'],
      ['MCQ set or MCQ test', '2 per right answer (at least 5)'],
      ['Mock paper', 'your marks ÷ 5 (at least 10)'],
      ['Viva — speak your answer 🎙️', 'your score % ÷ 10 (at least 3)'],
      ['👾 Boss of the week question right', '2 each']]],
  ];
  const COMMON = [
    ['🎁 Rewards', [
      ['Mystery box (after today’s goal)', 'a free surprise — sometimes +10 bonus stars'],
      ['💡 Used a Gappu hint on a question', 'that question gives half the stars']]],
    ['🧭 GK Explorer & Brain Snacks', [
      ['Reveal the GK Bite on Brain Snacks', '+2, once a day'],
      ['A fact card you have not seen before', '+1 each, +5 when you finish the set'],
      ['GK quiz question right', '+5 each'],
      ['Speed round', '3 per right answer'],
      ['True or false right', '+3 each'],
      ['Fact streak', '2 per right answer, +5 bonus at 5 in a row']]],
    ['🧮 Calculator Academy', [
      ['Each mission step done (first time)', '+2'],
      ['Mission finished', '+10 the first time, +3 when you replay'],
      ['Spot the mistake — right first time', '+3'],
      ['Beat the clock', '3 per right answer'],
      ['New academy badge', '+10']]],
  ];
  const GOAL = () => (window.Garden && Garden.GOAL) || 50;
  const todayGoal = () => { try { return window.Garden && Garden.dailyXP ? Garden.dailyXP() : (ST.daily && ST.daily.d === today() ? ST.daily.xp : 0); } catch (e) { return 0; } };

  let el = null, opener = null;
  function sheet() {
    if (el) return el;
    const st = D.createElement('style'); st.textContent = CSS; D.head.appendChild(st);
    el = D.createElement('div'); el.className = 'sheet sv-stars'; el.id = 'svStars'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-labelledby', 'svStT');
    el.innerHTML = '<div class="sheet-in"><div class="sheet-grab"></div><div id="svStBody"></div></div>';
    el.addEventListener('click', e => { if (e.target === el) close(); });
    el.addEventListener('keydown', e => { if (e.key === 'Escape') { e.stopPropagation(); close(); } });
    D.body.appendChild(el);
    return el;
  }
  function show(html, focusSel) {
    const s = sheet(); opener = D.activeElement;
    s.querySelector('#svStBody').innerHTML = html;
    s.classList.add('show'); s.querySelector('.sheet-in').scrollTop = 0;
    s.querySelectorAll('[data-st]').forEach(b => b.onclick = () => (b.dataset.st === 'stars' ? open() : streak()));
    s.querySelectorAll('[data-stx]').forEach(b => b.onclick = close);
    s.querySelectorAll('[data-stgo]').forEach(b => b.onclick = () => { close(); const g = b.dataset.stgo; if (g === 'practice') practiceScreen(); else if (g === 'cxa' && window.CalcAcademy) CalcAcademy.open(); });
    setTimeout(() => { const f = s.querySelector(focusSel || '#svStT'); if (f) f.focus(); }, 30);
  }
  function close() { if (!el) return; el.classList.remove('show'); if (opener && opener.focus && D.contains(opener)) try { opener.focus(); } catch (e) {} }

  const table = groups => groups.map(([h, rows]) => `<h4 class="st-h4">${h}</h4><table class="st-tbl"><thead class="sr-only"><tr><th scope="col">What you do</th><th scope="col">Stars</th></tr></thead><tbody>${rows.map(([a, b]) => `<tr><td>${esc(a)}</td><td>${esc(b)}</td></tr>`).join('')}</tbody></table>`).join('');

  function open() {
    const L = log(), t = today(), wk = week(), ca = isCA();
    const nToday = L[t] || 0, nWeek = wk.reduce((a, k) => a + (k <= t ? L[k] || 0 : 0), 0);
    const max = Math.max(1, ...wk.map(k => L[k] || 0));
    const first = Object.keys(L).sort()[0];
    const note = first && first > wk[0] ? `<p class="st-small">Stars are counted day by day from ${dateName(first)}.</p>` : (!first ? '<p class="st-small">Stars are counted day by day from today.</p>' : '');
    const goal = GOAL(), gNow = todayGoal(), gp = Math.min(100, Math.round(gNow / goal * 100));
    const B = (window.Garden && Garden.BADGES) || [], mine = B.filter(b => ST.badges && ST.badges[b[0]]);
    const acad = window.CalcAcademy && CalcAcademy.badgeCount ? CalcAcademy.badgeCount() : null;
    const groups = (ca ? CA : SCHOOL).concat(COMMON);
    show(`<h2 id="svStT" tabindex="-1"><span aria-hidden="true">⭐</span> Your stars</h2>
      <div class="st-big"><div><b title="${ST.xp}">${kfmt(ST.xp)}</b><span>stars in total</span></div><div><b>${nToday}</b><span>today</span></div><div><b>${nWeek}</b><span>this week</span></div></div>
      <div class="st-week" role="img" aria-label="Stars this week: ${wk.map((k, i) => `${DAYS[i]} ${k > t ? 'not yet' : L[k] || 0}`).join(', ')}">${wk.map((k, i) => `<div class="st-col ${k === t ? 'now' : ''} ${k > t ? 'later' : ''}"><i style="height:${Math.round((L[k] || 0) / max * 100)}%"></i><span>${(L[k] || 0) || ''}</span><small>${DAYS[i]}</small></div>`).join('')}</div>
      ${note}
      <div class="st-goal"><div class="st-gtop"><b>🎯 Today’s goal</b><span>${Math.min(gNow, goal)} / ${goal} ⭐</span></div><div class="st-bar" role="progressbar" aria-label="Today's goal" aria-valuemin="0" aria-valuemax="${goal}" aria-valuenow="${Math.min(gNow, goal)}"><i style="width:${gp}%"></i></div>
        <p class="st-small">${gNow >= goal ? 'Goal reached — your 🔥 streak is safe today!' : `Earn ${goal - gNow} more today to reach your goal and keep your 🔥 streak safe.`}</p></div>
      <h3 class="st-h3">What are stars?</h3>
      <p>Stars are your learning points (also called XP). You earn them every time you learn, answer, play or practise. They never go down, and they are not money — you cannot spend or lose them.</p>
      <h3 class="st-h3">How to earn stars</h3>${table(groups)}
      <p class="st-small">🎯 Daily goal: reaching ${goal} ⭐ in a day gives no extra stars, but it keeps your streak safe and wins the 🎯 badge.</p>
      <p class="st-small">⚖️ Fair play: after 300 ⭐ in one day, each new award counts half — so steady daily study beats one marathon. Big totals show short, like 1.2k = 1,200.</p>
      <h3 class="st-h3">What stars do</h3>
      <ul class="st-list"><li><b>🎯 Daily goal</b> — ${goal} stars a day keeps your 🔥 streak alive.</li>
        ${ca ? '' : '<li><b>🦁 Squad</b> — your stars put you on the Team Lions leaderboard.</li>'}
        <li><b>🏅 Badges</b> — ${B.length ? `you have ${mine.length} of ${B.length}${mine.length ? ': ' + mine.map(b => `<span aria-hidden="true">${b[1]}</span>`).join('') + `<span class="sr-only">${mine.map(b => b[2]).join(', ')}</span>` : ''}.` : ''} Badges come from quests, streaks, your daily goal and duels.${acad ? ` Calculator Academy badges: ${acad.have} of ${acad.all}.` : ''}</li></ul>
      <div class="st-btns">${ca ? '' : '<button class="btn ghost" type="button" data-stgo="practice">See all badges</button>'}<button class="btn ghost" type="button" data-st="streak"><span aria-hidden="true">🔥</span> How my streak works</button></div>
      <div style="height:8px"></div><button class="btn" type="button" data-stx>Close</button>`);
  }

  function streak() {
    const t = today(), y = dkey(new Date(new Date(t + 'T00:00:00Z').getTime() - 864e5)), last = ST.streak && ST.streak.last;
    const n = typeof liveStreak === 'function' ? liveStreak() : (ST.streak.n || 0), best = Math.max(ST.streak.best || 0, ST.streak.n || 0), ca = isCA();
    const state = last === t ? ['✅', 'Today counts! Come back tomorrow to make it ' + (n + 1) + '.'] : last === y ? ['⏳', `Study today to keep your ${n}-day streak.`] : ['🌱', (ST.streak.n || 0) > 0 ? 'Your last streak ended. Study today to start a new one.' : 'Study today to start your first streak.'];
    const L = log(), d7 = last7(), turn = dayTurn();
    const counts = ca ? ['Finish a unit step (Learn, Examples, On the job, MCQ, Write, Revise)', 'Finish an MCQ set, a mock paper, a viva or Daily practice', 'Finish a GK quiz or a fact streak', 'Finish a Calculator Academy mission', `Reach your daily goal of ${GOAL()} ⭐`]
      : ['Finish a quest', 'Finish Daily Practice or water your Memory Garden', 'Finish a chapter or subject test', 'Finish a GK quiz or a fact streak', 'Finish a Calculator Academy mission', `Reach your daily goal of ${GOAL()} ⭐`];
    show(`<h2 id="svStT" tabindex="-1"><span aria-hidden="true">🔥</span> Your streak</h2>
      <div class="st-big"><div><b>${n}</b><span>day${n === 1 ? '' : 's'} in a row</span></div><div><b>${best}</b><span>best ever</span></div></div>
      <p class="st-state"><span aria-hidden="true">${state[0]}</span> ${esc(state[1])}</p>
      ${window.Rewards && Rewards.shieldHTML ? Rewards.shieldHTML() : ''}
      <div class="st-dots" role="img" aria-label="Last 7 days with stars: ${d7.map(k => `${dayName(k)} ${(L[k] || 0) > 0 || k === last ? 'yes' : 'no'}`).join(', ')}">${d7.map(k => `<div class="${(L[k] || 0) > 0 || k === last ? 'on' : ''} ${k === t ? 'now' : ''}"><i aria-hidden="true">${(L[k] || 0) > 0 || k === last ? '🔥' : '·'}</i><small>${dayName(k)}</small></div>`).join('')}</div>
      <h3 class="st-h3">How it counts</h3>
      <p>Every day you study adds 1 to your streak. Study again the next day and it keeps growing. Miss a whole day and it starts again from 1.</p>
      <h3 class="st-h3">What counts as a study day</h3>
      <ul class="st-list">${counts.map(c => `<li>${esc(c)}</li>`).join('')}</ul>
      ${turn ? `<p class="st-small">A new day starts at ${turn} on your phone’s clock.</p>` : ''}
      <div class="st-btns"><button class="btn ghost" type="button" data-st="stars"><span aria-hidden="true">⭐</span> How stars work</button></div>
      <div style="height:8px"></div><button class="btn" type="button" data-stx>Close</button>`);
  }

  const CSS = `
#svStars .sheet-in{max-height:90vh;overflow-y:auto;overscroll-behavior:contain;color:var(--ink,#1b1f3a)}
#svStars h2{margin:0 0 8px;font-size:22px}#svStars h2:focus{outline:none}
#svStars p{margin:6px 0;line-height:1.45}
.st-big{display:flex;gap:8px;margin:6px 0 10px}.st-big>div{flex:1;background:var(--sv-tint,#f3f0ff);border-radius:14px;padding:10px 8px;text-align:center}
.st-big b{display:block;font-size:26px;line-height:1.1}.st-big span{font-size:12.5px;color:var(--muted,#5a6077)}
.st-week{display:flex;gap:6px;align-items:flex-end;height:92px;margin:4px 0 2px;padding:0 2px}
.st-col{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;gap:2px;font-size:11px;color:var(--muted,#5a6077)}
.st-col i{display:block;width:70%;min-height:3px;border-radius:6px 6px 2px 2px;background:#ffc93c}.st-col.now i{background:#ff9f1c}.st-col.now small{font-weight:800;color:var(--ink,#1b1f3a)}
.st-col.later i{background:#e6e8f2}.st-col span{font-weight:800;color:var(--ink,#1b1f3a);min-height:14px}
.st-small{font-size:13px;color:var(--muted,#5a6077)}
.st-goal{background:#fff8e1;border-radius:14px;padding:10px 12px;margin:10px 0}.st-gtop{display:flex;justify-content:space-between;gap:8px}
.st-bar{height:10px;border-radius:9px;background:#f1e2b0;overflow:hidden;margin:6px 0 2px}.st-bar i{display:block;height:100%;background:#2ed3a5;border-radius:9px}
.st-h3{margin:14px 0 4px;font-size:17px}.st-h4{margin:10px 0 4px;font-size:15px}
.st-tbl{width:100%;border-collapse:collapse;font-size:14px}.st-tbl td{padding:7px 4px;border-bottom:1px solid #eceef6;vertical-align:top}
.st-tbl td:last-child{text-align:right;font-weight:800;width:42%;color:#8a5a00}
.st-list{margin:4px 0;padding-left:20px;line-height:1.5}.st-list li{margin:3px 0}
.st-btns{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}.st-btns .btn{flex:1;min-width:150px}
.st-state{background:var(--sv-tint,#f3f0ff);border-radius:12px;padding:10px 12px;font-weight:700}
.st-dots{display:flex;gap:6px;margin:8px 0}.st-dots>div{flex:1;text-align:center;border-radius:10px;padding:6px 0;background:#f2f3f8;font-size:11px;color:var(--muted,#5a6077)}
.st-dots>div.on{background:#ffe9d6}.st-dots>div.now{outline:2px solid #ff9f1c}.st-dots i{display:block;font-style:normal;font-size:18px;line-height:1.2}
html.sv-hc .st-big>div,html.sv-hc .st-goal,html.sv-hc .st-state,html.sv-hc .st-dots>div{background:#fff;border:2px solid #000;color:#000}`;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  window.Stars = { open, streak, close };
})();
