/* Knowtopia — end-of-game answer review, shared by the solo games (js/arcade.js) and the game rooms (js/live.js).
   Every answer the student gave is listed: ✅ / ❌ / ⏰, subject › chapter › topic, the question, their answer,
   the right answer and a short explanation — so they learn from the game, not just score it.
   Entry: { ok: true | false | null (no answer), q, your, right, why, path: [subject, chapter, topic] | 'A · B · C', kind } */
(function () {
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const short = (s, n) => { s = String(s || '').replace(/\s+/g, ' ').trim(); if (s.length <= n) return s; const cut = s.slice(0, n), sp = cut.lastIndexOf(' '); return (sp > n * .6 ? cut.slice(0, sp) : cut) + '…'; };
  const pathOf = p => (Array.isArray(p) ? p : String(p || '').split(' · ')).map(x => String(x || '').trim()).filter(Boolean);
  const fromSrc = src => src ? [`${src.se || ''} ${src.sname || ''}`.trim(), src.ch, src.tt] : [];

  function row(e, i) {
    const st = e.ok === true ? 'ok' : e.ok === false ? 'bad' : 'skip';
    const icon = st === 'ok' ? '✅' : st === 'bad' ? '❌' : '⏰';
    const p = pathOf(e.path), why = short(e.why, 260), full = String(e.why || '').trim();
    const your = e.your == null || e.your === '' ? '<i>No answer</i>' : E(e.your);
    return `<li class="rv-row ${st}" data-st="${st}"><div class="rv-top"><span class="rv-n">${i + 1}</span><span class="rv-ic" aria-label="${st === 'ok' ? 'Correct' : st === 'bad' ? 'Wrong' : 'Not answered'}">${icon}</span>
      ${p.length ? `<span class="rv-path">${p.map(E).join(' <b>›</b> ')}</span>` : ''}</div>
      <div class="rv-q">${E(e.q)}</div>
      ${e.kind === 'pair' ? `<div class="rv-a ok">✔ ${E(e.right)}</div>` : `
      <div class="rv-a ${st === 'ok' ? 'ok' : 'mine'}">${st === 'ok' ? '✔ Your answer' : '✗ Your answer'}: <b>${your}</b></div>
      ${st === 'ok' ? '' : `<div class="rv-a ok">✔ Right answer: <b>${E(e.right)}</b></div>`}`}
      ${why ? `<div class="rv-why">💡 ${E(why)}${full.length > why.length ? ` <button type="button" class="rv-more" data-full="${E(full)}">More</button>` : ''}</div>` : ''}
    </li>`;
  }

  /* list → HTML card. opt.title, opt.open (default true) */
  function html(list, opt) {
    opt = opt || {}; list = (list || []).filter(e => e && e.q);
    if (!list.length) return '';
    const nOk = list.filter(e => e.ok === true).length, nBad = list.filter(e => e.ok === false).length, nSkip = list.length - nOk - nBad;
    const miss = nBad + nSkip;
    return `<details class="rv"${opt.open === false ? '' : ' open'}><summary><span>📝 ${E(opt.title || 'Your answers')}</span>
      <small>✅ ${nOk} right${nBad ? ` · ❌ ${nBad} wrong` : ''}${nSkip ? ` · ⏰ ${nSkip} not answered` : ''}</small></summary>
      <p class="rv-tip">${miss ? 'Read the ❌ ones once more — that is how they stick next time.' : 'All right — brilliant! Read the explanations to lock them in.'}</p>
      ${miss && nOk ? `<div class="rv-f" role="group" aria-label="Show"><button type="button" class="on" data-f="all">All (${list.length})</button><button type="button" data-f="miss">To revise (${miss})</button></div>` : ''}
      <ol class="rv-list">${list.map(row).join('')}</ol></details>`;
  }

  /* wire the filter + "More" buttons inside root */
  function wire(root) {
    if (!root) return;
    root.querySelectorAll('.rv').forEach(rv => {
      rv.querySelectorAll('.rv-f button').forEach(b => b.onclick = () => {
        rv.querySelectorAll('.rv-f button').forEach(x => x.classList.toggle('on', x === b));
        rv.querySelectorAll('.rv-row').forEach(r => { r.hidden = b.dataset.f === 'miss' && r.dataset.st === 'ok'; });
      });
      rv.querySelectorAll('.rv-more').forEach(b => b.onclick = () => { const w = b.parentNode; w.textContent = '💡 ' + b.dataset.full; });
    });
  }

  (function css() {
    if (document.getElementById('rvCss')) return;
    const c = document.createElement('style'); c.id = 'rvCss';
    c.textContent = `.rv{text-align:left;margin:14px 0 12px;background:transparent;border:1.5px solid rgba(118,70,234,.25);border-radius:16px;padding:10px 12px;color:var(--ink,#1d1f3a)}
.rv summary{cursor:pointer;display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;font-weight:800;font-size:16px;list-style:none}
.rv summary::-webkit-details-marker{display:none}.rv summary::after{content:'▾';margin-left:auto;opacity:.6}.rv:not([open]) summary::after{content:'▸'}
.rv summary small{font-weight:700;font-size:13px;color:var(--muted,#5f6485)}
.rv-tip{margin:6px 0 8px;font-size:13px;color:var(--muted,#5f6485)}
.rv-f{display:flex;gap:6px;margin:0 0 8px}.rv-f button{border:1.5px solid rgba(118,70,234,.35);background:transparent;color:inherit;border-radius:999px;padding:5px 11px;font:700 13px/1 inherit;cursor:pointer}
.rv-f button.on{background:#7646ea;border-color:#7646ea;color:#fff}
.rv-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.rv-row{border-radius:12px;padding:9px 10px;border-left:5px solid #2fbf71;background:rgba(47,191,113,.08)}
.rv-row.bad{border-left-color:#e5484d;background:rgba(229,72,77,.08)}.rv-row.skip{border-left-color:#f0a020;background:rgba(240,160,32,.1)}
.rv-top{display:flex;align-items:center;gap:6px;flex-wrap:wrap;font-size:12px;color:var(--muted,#5f6485);font-weight:700}
.rv-n{min-width:20px;height:20px;border-radius:999px;background:rgba(0,0,0,.08);display:inline-grid;place-items:center;font-size:11px}
.rv-path b{opacity:.55;font-weight:800}
.rv-q{font-weight:800;font-size:14.5px;margin:4px 0 3px;line-height:1.35;overflow-wrap:anywhere}
.rv-a{font-size:13.5px;margin:2px 0;overflow-wrap:anywhere}.rv-a.ok{color:#17834b}.rv-a.mine{color:#c4282d}
.rv-why{font-size:13px;margin-top:5px;line-height:1.4;color:var(--ink,#1d1f3a);opacity:.9;overflow-wrap:anywhere}
.rv-more{border:0;background:none;color:#7646ea;font:800 13px inherit;cursor:pointer;padding:0 2px}
html[data-age=pro] .rv{border-color:rgba(255,255,255,.18)}
html.sv-hc .rv-row{border:2px solid #000;background:#fff}`;
    document.head.appendChild(c);
  })();

  window.Review = { html, wire, fromSrc };
})();
