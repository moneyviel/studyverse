/* StudyVerse Concept Lab: probability — coin / dice / spinner / bag-of-balls simulator.
 *
 * The child predicts a probability (or the most likely result), then runs 1, 10, 100 or 1000
 * trials. A live bar chart shows the experimental relative frequency of every outcome next to a
 * dashed marker at the theoretical probability, so they see the two get closer with more trials.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   device    'coin' | 'dice' | 'spinner' | 'bag'                                               default 'spinner'
 *   count     1 | 2   number of coins or dice (2 coins → number of heads; 2 dice → sum)          default 1
 *   sides     number  faces on a die (4–8; pips drawn up to 6, numbers above)                  default 6
 *   sectors   [{label, size, color?}]  spinner parts; size = relative angle                    default Red 2, Blue 1, Green 1
 *   balls     [{label, count, color?}] bag contents (drawn with replacement)                   default Red 5, Blue 3, Green 2
 *   ask       the prediction challenge, one of:
 *               {type:'prob', outcome:'Red'}          "What is P(Red)?"  (outcome = label, number, 'H'/'T')
 *               {type:'event', outcomes:[5,6], name:'more than 4'}   P(event) for a set of outcomes
 *               {type:'most'}                         "Which result is most likely?"
 *             default: a sensible question for the device
 *   minTrials number  trials needed after a correct prediction to finish the challenge           default 100
 *   challenge string  challenge sentence (else generated)
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const PAL = ['#ff6b6b', '#3b82f6', '#2ed3a5', '#ffc93c', '#8b5cf6', '#ff9f43', '#14b8c4', '#f472b6', '#84cc16', '#6b7090', '#a16207'];
  const NAMED = { red: '#ff6b6b', blue: '#3b82f6', green: '#2ed3a5', yellow: '#ffc93c', purple: '#8b5cf6', violet: '#8b5cf6', orange: '#ff9f43', pink: '#f472b6', black: '#1b1f3a', white: '#e9ebf7', लाल: '#ff6b6b', नीला: '#3b82f6', हरा: '#2ed3a5', पीला: '#ffc93c' };
  const gcd = (a, b) => { while (b) [a, b] = [b, a % b]; return Math.abs(a); };
  const fr = (n, d) => { const g = gcd(n, d) || 1; n /= g; d /= g; return d === 1 ? String(n) : `${n}/${d}`; };

  Labs.register('probability', {
    title: 'Chance machine',
    subjects: ['maths'],
    render(host, p, api) {
      const dev = ['coin', 'dice', 'spinner', 'bag'].includes(p.device) ? p.device : 'spinner';
      const cnt = (dev === 'coin' || dev === 'dice') && +p.count === 2 ? 2 : 1;
      const sides = dev === 'dice' ? Math.max(4, Math.min(8, Math.round(+p.sides || 6))) : 6;
      const minTrials = Math.max(10, Math.min(1000, +p.minTrials || 100));
      const colorOf = (it, i) => it.color || NAMED[String(it.label).toLowerCase()] || PAL[i % PAL.length];
      // outcomes: {key,label,color,n} with probability n/den
      let O = [], den = 1;
      if (dev === 'coin' && cnt === 1) { O = [{ key: 'H', label: 'Heads', n: 1, color: '#ffc93c' }, { key: 'T', label: 'Tails', n: 1, color: '#3b82f6' }]; den = 2; }
      else if (dev === 'coin') { O = [0, 1, 2].map(h => ({ key: h, label: `${h} head${h === 1 ? '' : 's'}`, n: h === 1 ? 2 : 1, color: PAL[h + 1] })); den = 4; }
      else if (dev === 'dice' && cnt === 1) { for (let i = 1; i <= sides; i++) O.push({ key: i, label: String(i), n: 1, color: PAL[(i - 1) % PAL.length] }); den = sides; }
      else if (dev === 'dice') { for (let s = 2; s <= 2 * sides; s++) { let n = 0; for (let a = 1; a <= sides; a++) { const b = s - a; if (b >= 1 && b <= sides) n++; } O.push({ key: s, label: String(s), n, color: '#8b5cf6' }); } den = sides * sides; }
      else {
        let list = dev === 'spinner' ? p.sectors : p.balls;
        const fld = dev === 'spinner' ? 'size' : 'count';
        if (!Array.isArray(list) || !list.length || !list.every(it => it && it.label != null && Number.isInteger(+it[fld]) && +it[fld] > 0)) list = dev === 'spinner' ? [{ label: 'Red', size: 2 }, { label: 'Blue', size: 1 }, { label: 'Green', size: 1 }] : [{ label: 'Red', count: 5 }, { label: 'Blue', count: 3 }, { label: 'Green', count: 2 }];
        list = list.slice(0, 8);
        O = list.map((it, i) => ({ key: String(it.label), label: String(it.label), n: +it[fld], color: colorOf(it, i) }));
        den = O.reduce((s, o) => s + o.n, 0);
      }
      const find = k => O.find(o => String(o.key).toLowerCase() === String(k).toLowerCase() || String(o.label).toLowerCase() === String(k).toLowerCase());

      // ---- the question ----
      let ask = p.ask && typeof p.ask === 'object' ? p.ask : null;
      if (ask && ask.type === 'prob' && !find(ask.outcome)) ask = null;
      if (ask && ask.type === 'event' && !(Array.isArray(ask.outcomes) && ask.outcomes.some(find))) ask = null;
      if (ask && !['prob', 'event', 'most'].includes(ask.type)) ask = null;
      if (!ask) {
        if (dev === 'coin' && cnt === 2) ask = { type: 'most' };
        else if (dev === 'dice' && cnt === 2) ask = { type: 'most' };
        else if (dev === 'dice') ask = { type: 'event', outcomes: [sides - 1, sides], name: `more than ${sides - 2}` };
        else if (dev === 'coin') ask = { type: 'prob', outcome: 'H' };
        else ask = { type: 'prob', outcome: O.slice().sort((a, b) => b.n - a.n)[0].key };
      }
      const evSet = ask.type === 'prob' ? [find(ask.outcome)] : ask.type === 'event' ? [...new Set(ask.outcomes.map(find).filter(Boolean))] : [];
      const evN = evSet.reduce((s, o) => s + o.n, 0);
      const evName = ask.type === 'prob' ? evSet[0].label : String(ask.name || evSet.map(o => o.label).join(' or '));
      const maxN = Math.max(...O.map(o => o.n));
      const best = O.filter(o => o.n === maxN);
      let choices = [];
      if (ask.type === 'most') choices = O.map(o => ({ t: o.label, ok: o.n === maxN, key: o.key }));
      else {
        const opts = [fr(evN, den)];
        const add = t => { if (t && !opts.includes(t)) opts.push(t); };
        if (den - evN > 0 && den - evN !== evN) add(fr(evN, den - evN).includes('/') ? fr(evN, den - evN) : `${evN}/${den - evN}`);
        add(fr(evSet.length, O.length)); add(fr(den - evN, den)); add(fr(1, den)); add(fr(evN + 1, den + 1)); add(fr(1, den + 1)); add('1');
        choices = opts.slice(0, 3).map((t, i) => ({ t, ok: i === 0 })).sort(() => Math.random() - 0.5);
      }
      const devWord = dev === 'coin' ? (cnt === 2 ? 'Toss 2 coins' : 'Toss a coin') : dev === 'dice' ? (cnt === 2 ? 'Roll 2 dice (add them)' : 'Roll a die') : dev === 'spinner' ? 'Spin' : 'Pick a ball (then put it back)';
      const chText = p.challenge || (ask.type === 'most' ? `${devWord}. Which result is most likely? Predict, then test it!` : `${devWord}. What is P(${evName})? Predict, then test it!`);

      const counts = O.map(() => 0);
      let total = 0, predicted = false, won = false, last = null, busy = 0, spinAngle = 0;
      const timers = [];

      // spinner geometry
      const sectorAngles = []; { let a0 = 0; O.forEach(o => { const a1 = a0 + 360 * o.n / den; sectorAngles.push([a0, a1]); a0 = a1; }); }

      host.innerHTML = `
<style>
.lb-probability-w{font-size:14px;color:#1b1f3a}
.lb-probability-ch{font-weight:800;font-size:14px;margin-bottom:5px;line-height:1.25}
.lb-probability-top{display:flex;gap:8px;align-items:stretch}
.lb-probability-dev{width:46%;flex-shrink:0;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:16px;display:block}
.lb-probability-side{flex:1;display:flex;flex-direction:column;gap:5px;min-width:0}
.lb-probability-runs{display:grid;grid-template-columns:1fr 1fr;gap:5px}
.lb-probability-b{min-height:40px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:14px;cursor:pointer;background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-probability-b:active{transform:translateY(2px);box-shadow:0 1px 0 #5b33c9}
.lb-probability-b.g{background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef}
.lb-probability-b:disabled{opacity:.4}
.lb-probability-tot{font-size:12.5px;font-weight:800;color:#6b7090;line-height:1.3}
.lb-probability-tot b{color:#1b1f3a;font-size:15px}
.lb-probability-chart{width:100%;height:auto;display:block;margin-top:6px;background:#fbfbff;border:2px solid #eef0fb;border-radius:14px}
.lb-probability-bar{transform-box:fill-box;transform-origin:50% 100%;transition:transform .45s cubic-bezier(.3,1.3,.5,1)}
.lb-probability-q{display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;align-items:center}
.lb-probability-q span{font-weight:800;font-size:13px;margin-right:2px}
.lb-probability-q.many span{width:100%}
.lb-probability-q.many .lb-probability-c{flex:1 1 13%!important;min-width:40px!important}
.lb-probability-c{flex:1;min-width:44px;min-height:42px;border:none;border-radius:12px;font-family:'Baloo 2',Nunito,sans-serif;font-weight:800;font-size:16px;cursor:pointer;background:#ffc93c;color:#1b1f3a;box-shadow:0 3px 0 #d99a00;padding:0 6px}
.lb-probability-c.bad{background:#ffd6d6;box-shadow:0 3px 0 #ffb0b0;color:#c23b3b}
.lb-probability-c.good{background:#2ed3a5;box-shadow:0 3px 0 #1a9c78;color:#fff}
.lb-probability-msg{font-size:12.5px;font-weight:700;color:#6b7090;margin-top:4px;min-height:17px}
.lb-probability-flip{animation:lbprobflip .5s ease;transform-box:fill-box;transform-origin:center}
@keyframes lbprobflip{0%{transform:scaleX(1)}25%{transform:scaleX(.05) translateY(-14px)}50%{transform:scaleX(1) translateY(-22px)}75%{transform:scaleX(.05) translateY(-10px)}100%{transform:scaleX(1)}}
.lb-probability-roll{animation:lbprobroll .5s ease;transform-box:fill-box;transform-origin:center}
@keyframes lbprobroll{0%{transform:rotate(0) scale(1)}50%{transform:rotate(200deg) scale(.8)}100%{transform:rotate(360deg) scale(1)}}
.lb-probability-pop{animation:lbprobpop .45s cubic-bezier(.2,1.5,.4,1);transform-box:fill-box;transform-origin:center}
@keyframes lbprobpop{from{transform:translateY(30px) scale(.3);opacity:0}}
.lb-probability-arrow{transition:transform .9s cubic-bezier(.15,.7,.25,1);transform-origin:80px 80px}
</style>
<div class="lb-probability-w">
  <div class="lb-probability-ch">🎯 Challenge: ${esc(chText)}</div>
  <div class="lb-probability-top">
    <svg class="lb-probability-dev" viewBox="0 0 160 160"></svg>
    <div class="lb-probability-side">
      <div class="lb-probability-runs">
        <button class="lb-probability-b" data-n="1">Run 1</button><button class="lb-probability-b" data-n="10">× 10</button>
        <button class="lb-probability-b" data-n="100">× 100</button><button class="lb-probability-b" data-n="1000">× 1000</button>
      </div>
      <div class="lb-probability-tot"></div>
      <button class="lb-probability-b g" data-a="reset">Reset counts ⟲</button>
    </div>
  </div>
  <svg class="lb-probability-chart" viewBox="0 0 360 140"></svg>
  <div class="lb-probability-q"></div>
  <div class="lb-probability-msg"></div>
</div>`;
      const $ = s => host.querySelector(s);
      const devSvg = $('.lb-probability-dev'), chart = $('.lb-probability-chart'), tot = $('.lb-probability-tot'), qEl = $('.lb-probability-q'), msg = $('.lb-probability-msg');

      // ---- device drawing ----
      function pips(cx, cy, s, v, col) {
        if (v > 6) return `<text x="${cx}" y="${cy + s * 0.18}" text-anchor="middle" font-size="${s * 0.5}" font-weight="800" fill="${col}">${v}</text>`;
        const o = s * 0.27, P = { 1: [[0, 0]], 2: [[-1, -1], [1, 1]], 3: [[-1, -1], [0, 0], [1, 1]], 4: [[-1, -1], [1, -1], [-1, 1], [1, 1]], 5: [[-1, -1], [1, -1], [0, 0], [-1, 1], [1, 1]], 6: [[-1, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [1, 1]] }[v];
        return P.map(([x, y]) => `<circle cx="${cx + x * o}" cy="${cy + y * o}" r="${s * 0.085}" fill="${col}"/>`).join('');
      }
      function drawDevice(anim, res) {
        let g = '';
        const arrow = dev === 'spinner' && devSvg.querySelector('.lb-probability-arrow');
        if (arrow) { arrow.style.transform = `rotate(${spinAngle}deg)`; return; }
        if (dev === 'coin') {
          const faces = res || (cnt === 2 ? ['H', 'T'] : ['H']);
          const xs = cnt === 2 ? [46, 114] : [80];
          faces.forEach((f, i) => {
            g += `<g class="${anim ? 'lb-probability-flip' : ''}"><circle cx="${xs[i]}" cy="80" r="${cnt === 2 ? 30 : 46}" fill="${f === 'H' ? '#ffc93c' : '#c7d2fe'}" stroke="${f === 'H' ? '#d99a00' : '#6b7fd7'}" stroke-width="4"/><circle cx="${xs[i]}" cy="80" r="${cnt === 2 ? 23 : 37}" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="2"/><text x="${xs[i]}" y="${80 + (cnt === 2 ? 10 : 15)}" text-anchor="middle" font-size="${cnt === 2 ? 28 : 42}" font-weight="900" fill="#1b1f3a">${f}</text></g>`;
          });
          g += `<text x="80" y="150" text-anchor="middle" font-size="11" font-weight="800" fill="#6b7090">H = heads · T = tails</text>`;
        } else if (dev === 'dice') {
          const faces = res || (cnt === 2 ? [3, 4] : [5]);
          const s = cnt === 2 ? 58 : 82, xs = cnt === 2 ? [44, 116] : [80];
          faces.forEach((f, i) => { g += `<g class="${anim ? 'lb-probability-roll' : ''}"><rect x="${xs[i] - s / 2}" y="${78 - s / 2}" width="${s}" height="${s}" rx="${s * 0.2}" fill="#fff" stroke="#8b5cf6" stroke-width="4"/>${pips(xs[i], 78, s, f, '#1b1f3a')}</g>`; });
          if (cnt === 2) g += `<text x="80" y="146" text-anchor="middle" font-size="14" font-weight="900" fill="#8b5cf6">${faces[0]} + ${faces[1]} = ${faces[0] + faces[1]}</text>`;
          else if (sides !== 6) g += `<text x="80" y="146" text-anchor="middle" font-size="11" font-weight="800" fill="#6b7090">${sides}-sided die</text>`;
        } else if (dev === 'spinner') {
          const R = 66, C = 80;
          const pt = a => [C + R * Math.sin(a * Math.PI / 180), C - R * Math.cos(a * Math.PI / 180)];
          O.forEach((o, i) => {
            const [a0, a1] = sectorAngles[i], [x0, y0] = pt(a0), [x1, y1] = pt(a1), mid = (a0 + a1) / 2, lr = R * 0.62;
            g += O.length === 1 ? `<circle cx="${C}" cy="${C}" r="${R}" fill="${o.color}"/>` : `<path d="M${C} ${C}L${x0} ${y0}A${R} ${R} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1} ${y1}Z" fill="${o.color}" stroke="#fff" stroke-width="2.5"/>`;
            if (a1 - a0 >= 28) g += `<text x="${C + lr * Math.sin(mid * Math.PI / 180)}" y="${C - lr * Math.cos(mid * Math.PI / 180) + 4}" text-anchor="middle" font-size="${a1 - a0 > 60 ? 12 : 10}" font-weight="800" fill="#fff" paint-order="stroke" stroke="rgba(0,0,0,.25)" stroke-width="2">${esc(o.label.slice(0, 8))}</text>`;
          });
          g += `<circle cx="${C}" cy="${C}" r="${R}" fill="none" stroke="#1b1f3a" stroke-width="3"/>`;
          g += `<g class="lb-probability-arrow" style="transform:rotate(${spinAngle}deg)"><path d="M80 80 L80 24" stroke="#1b1f3a" stroke-width="5" stroke-linecap="round"/><path d="M71 30 L80 16 L89 30Z" fill="#1b1f3a"/></g><circle cx="80" cy="80" r="8" fill="#fff" stroke="#1b1f3a" stroke-width="3"/>`;
        } else {
          g += `<path d="M28 58 Q24 150 80 152 Q136 150 132 58 Z" fill="#f0e3c8" stroke="#b08d57" stroke-width="3"/><path d="M28 58 Q80 44 132 58" fill="none" stroke="#b08d57" stroke-width="5" stroke-linecap="round"/>`;
          const balls = []; O.forEach(o => { for (let i = 0; i < o.n; i++) balls.push(o.color); });
          const show = balls.slice(0, 20), cols = 5, r = 9;
          // stable shuffle for nice mixing
          const mix = show.map((c, i) => [c, (i * 7919) % 97]).sort((a, b) => a[1] - b[1]).map(q => q[0]);
          mix.forEach((c, i) => { const row = Math.floor(i / cols), col = i % cols; g += `<circle cx="${40 + col * 19 + (row % 2) * 8}" cy="${136 - row * 18}" r="${r}" fill="${c}" stroke="rgba(0,0,0,.15)"/>`; });
          if (balls.length > 20) g += `<text x="80" y="76" text-anchor="middle" font-size="10" font-weight="800" fill="#7a5a2a">${den} balls</text>`;
          if (res) { const o = O[res]; g += `<g class="${anim ? 'lb-probability-pop' : ''}"><circle cx="80" cy="28" r="17" fill="${o.color}" stroke="#fff" stroke-width="3"/><text x="80" y="33" text-anchor="middle" font-size="12" font-weight="900" fill="#fff" paint-order="stroke" stroke="rgba(0,0,0,.3)" stroke-width="2">${esc(o.label.slice(0, 3))}</text></g>`; }
        }
        devSvg.innerHTML = g;
      }

      // ---- chart ----
      const CW = 360, CH = 140, L = 30, B = 118, TOP = 12, n = O.length, slot = (CW - L - 6) / n, bw = Math.min(40, slot * 0.62);
      const yOf = f => B - f * (B - TOP);
      const ymax = [0.2, 0.4, 0.6, 0.8, 1].find(y => y >= Math.max(...O.map(o => o.n / den)) * 1.5) || 1;
      const yv = f => B - Math.min(1, f / ymax) * (B - TOP);
      void yOf;
      function buildChart() {
        let g = '';
        for (let k = 0; k <= 4; k++) { const f = ymax * k / 4, y = yv(f); g += `<line x1="${L}" x2="${CW - 4}" y1="${y}" y2="${y}" stroke="#eef0fb"/><text x="${L - 4}" y="${y + 3}" text-anchor="end" font-size="9" font-weight="700" fill="#6b7090">${Math.round(f * 100) / 100}</text>`; }
        O.forEach((o, i) => {
          const cx = L + slot * (i + 0.5), th = o.n / den;
          g += `<rect class="lb-probability-bar" data-i="${i}" x="${cx - bw / 2}" y="${TOP}" width="${bw}" height="${B - TOP}" rx="4" fill="${o.color}" style="transform:scaleY(0)"/>`;
          g += `<line x1="${cx - bw / 2 - 4}" x2="${cx + bw / 2 + 4}" y1="${yv(th)}" y2="${yv(th)}" stroke="#1b1f3a" stroke-width="2.2" stroke-dasharray="4 3"/>`;
          g += `<text class="lb-probability-val" data-i="${i}" x="${cx}" y="${B - 3}" text-anchor="middle" font-size="${n > 8 ? 8 : 9.5}" font-weight="800" fill="#1b1f3a"></text>`;
          g += `<text x="${cx}" y="${B + 13}" text-anchor="middle" font-size="${n > 8 ? 9.5 : 11}" font-weight="800" fill="#1b1f3a">${esc(dev === 'coin' && cnt === 2 ? o.key + 'H' : o.label.slice(0, 7))}</text>`;
        });
        g += `<line x1="${L}" x2="${CW - 4}" y1="${B}" y2="${B}" stroke="#1b1f3a" stroke-width="1.5"/>`;
        g += `<g transform="translate(${L + 4} 2)"><rect x="0" y="0" width="10" height="8" rx="2" fill="#8b5cf6"/><text x="13" y="8" font-size="9" font-weight="800" fill="#6b7090">experiment</text><path d="M78 4 H94" stroke="#1b1f3a" stroke-width="2" stroke-dasharray="4 3"/><text x="97" y="8" font-size="9" font-weight="800" fill="#6b7090">theory</text></g>`;
        chart.innerHTML = g;
      }
      function updChart() {
        O.forEach((o, i) => {
          const f = total ? counts[i] / total : 0;
          const bar = chart.querySelector(`.lb-probability-bar[data-i="${i}"]`);
          bar.style.transform = `scaleY(${Math.min(1, f / ymax)})`;
          const t = chart.querySelector(`.lb-probability-val[data-i="${i}"]`);
          t.textContent = total ? (n > 8 ? Math.round(f * 100) + '%' : f.toFixed(2)) : '';
          t.setAttribute('y', Math.max(TOP + 9, yv(f) - 3));
        });
        let s = `Trials: <b>${total}</b>`;
        if (ask.type !== 'most' && total) {
          const hit = evSet.reduce((sum, o) => sum + counts[O.indexOf(o)], 0);
          s += `<br>${esc(evName)}: ${hit}/${total} = <b>${(hit / total).toFixed(2)}</b><br>theory ${fr(evN, den)} = ${(evN / den).toFixed(2)}`;
        } else if (last != null) s += `<br>Last: <b>${esc(O[last].label)}</b>`;
        tot.innerHTML = s;
      }

      function sample() {
        if (dev === 'coin') { const f = [0, 0].slice(0, cnt).map(() => Math.random() < 0.5 ? 'H' : 'T'); return { i: cnt === 1 ? (f[0] === 'H' ? 0 : 1) : f.filter(x => x === 'H').length, raw: f }; }
        if (dev === 'dice') { const f = [0, 0].slice(0, cnt).map(() => 1 + Math.floor(Math.random() * sides)); return { i: cnt === 1 ? f[0] - 1 : f[0] + f[1] - 2, raw: f }; }
        let r = Math.random() * den;
        for (let i = 0; i < O.length; i++) { if (r < O[i].n) return { i, raw: null, r: r / O[i].n }; r -= O[i].n; }
        return { i: O.length - 1, raw: null, r: 0.5 };
      }
      function run(k) {
        if (busy) return;
        let s;
        for (let j = 0; j < k; j++) { s = sample(); counts[s.i]++; total++; }
        last = s.i;
        if (dev === 'spinner') {
          const [a0, a1] = sectorAngles[s.i], target = a0 + (a1 - a0) * (0.15 + 0.7 * s.r);
          const base = Math.ceil(spinAngle / 360) * 360 + (k === 1 ? 720 : 360);
          spinAngle = base + target;
        }
        drawDevice(true, dev === 'bag' ? s.i : s.raw);
        api.sfx(k === 1 ? 'tap' : 'coin');
        busy = 1; timers.push(setTimeout(() => { busy = 0; }, k === 1 ? 350 : 200));
        updChart();
        if (predicted && !won && total >= minTrials) finish();
        else if (predicted && !won) msg.textContent = `Run ${minTrials - total} more trials to test your prediction.`;
      }
      function finish() {
        won = true;
        let text;
        if (ask.type === 'most') {
          const top = O[counts.indexOf(Math.max(...counts))];
          text = `Most likely: ${best.map(o => o.label).join(' / ')} (${fr(maxN, den)}). In ${total} trials the most common was ${top.label}.`;
        } else {
          const hit = evSet.reduce((sum, o) => sum + counts[O.indexOf(o)], 0);
          text = `P(${evName}) = ${fr(evN, den)} ≈ ${(evN / den).toFixed(2)}. Your ${total} trials gave ${(hit / total).toFixed(2)}${Math.abs(hit / total - evN / den) < 0.06 ? ' — very close!' : ' — more trials get closer.'}`;
        }
        msg.textContent = 'More trials → experiment gets closer to theory.';
        api.sfx('correct'); api.win(text);
      }
      function drawQ() {
        qEl.classList.toggle('many', choices.length > 5);
        qEl.innerHTML = `<span>${ask.type === 'most' ? 'Most likely?' : `P(${esc(evName)}) =`}</span>` + choices.map((c, i) => `<button class="lb-probability-c" data-c="${i}" style="${ask.type === 'most' ? 'font-size:14px;flex:0 1 auto;min-width:40px' : ''}">${esc(c.t)}</button>`).join('');
      }
      function onClick(e) {
        const b = e.target.closest('button'); if (!b || b.disabled) return;
        if (b.dataset.n) run(+b.dataset.n);
        else if (b.dataset.a === 'reset') { counts.fill(0); total = 0; last = null; updChart(); api.sfx('tap'); if (predicted && !won) msg.textContent = `Now run ${minTrials} trials to test it.`; }
        else if (b.dataset.c != null) {
          if (predicted) return;
          const c = choices[+b.dataset.c];
          if (c.ok) {
            predicted = true; b.classList.add('good'); api.sfx('correct');
            qEl.querySelectorAll('.lb-probability-c').forEach(x => { if (x !== b) x.disabled = true; });
            msg.textContent = ask.type === 'most' ? `Yes! ${best.map(o => o.label).join(' / ')} can happen in the most ways (${maxN} of ${den}).` : `Yes! ${evN} favourable out of ${den} equally likely → ${fr(evN, den)}.`;
            if (total >= minTrials) finish(); else timers.push(setTimeout(() => { if (!won) msg.textContent = `Now run ${minTrials - total} more trials to test it!`; }, 2200));
          } else {
            b.classList.add('bad'); api.sfx('wrong');
            msg.textContent = ask.type === 'most' ? 'Hmm — count the ways each result can happen.' : `Count: favourable outcomes ÷ ALL equally likely outcomes (${den}).`;
          }
        }
      }
      host.addEventListener('click', onClick);
      drawDevice(false); buildChart(); updChart(); drawQ();
      requestAnimationFrame(() => updChart());
      return () => { timers.forEach(clearTimeout); host.removeEventListener('click', onClick); };
    },
    example: { device: 'spinner', count: 1, sides: 6, sectors: [{ label: 'Red', size: 2 }, { label: 'Blue', size: 1 }, { label: 'Green', size: 1 }], balls: [{ label: 'Red', count: 5 }, { label: 'Blue', count: 3 }, { label: 'Green', count: 2 }], minTrials: 100 },
    examples: [
      { device: 'coin', count: 1, ask: { type: 'prob', outcome: 'H' }, minTrials: 50, challenge: 'Toss a coin. What is the chance of Heads? Guess, then toss 50 times.' },
      { device: 'dice', count: 2, ask: { type: 'most' }, challenge: 'Roll two dice and add. Which total comes up most often?' },
      { device: 'bag', balls: [{ label: 'Red', count: 5 }, { label: 'Blue', count: 3 }, { label: 'Green', count: 2 }], ask: { type: 'prob', outcome: 'Blue' }, challenge: 'A bag has 5 red, 3 blue and 2 green balls. What is P(blue)?' }
    ]
  });
})();
