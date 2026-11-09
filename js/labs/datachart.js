/* Knowtopia Concept Lab: datachart — tally, pictograph, bar / double-bar graph and pie chart.
 *
 * The child taps + / − to change the data (like adding tally marks) and switches between views;
 * the chart and the live mean / median / mode / range update instantly. Challenge: read the graph,
 * build a given data set, or change the data to reach a target statistic.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   title     string    chart title                                                    default 'Favourite fruit'
 *   labels    string[]  categories (2–7), English or Hindi                              default ['Apple','Mango','Banana','Grapes']
 *   values    number[]  counts / amounts, same length as labels. Any size (e.g. sex ratio 943);
 *                       whole numbers unless some value has decimals (then kept to 2 dp)  default [4,7,3,5]
 *   values2   number[]  second data set → double bar graph                             default none
 *   series    [string,string]  names of the two data sets                             default ['Class A','Class B']
 *   views     string[]  any of 'tally','picto','bar','pie' (order = tab order)          default ['tally','picto','bar','pie']
 *                       (['bar','pie'] when the data goes above 40). Tally / picto rows
 *                       too long to fit are cut with '…' (the number is still shown).
 *   view      string    starting view                                                   default first of views
 *   icon      string    pictograph symbol (emoji)                                       default '🍎'
 *   key       number    pictograph: one icon stands for this many                       default 1
 *   unit      string    what is counted, e.g. 'students'                                default 'students'
 *   editable  boolean   show + / − controls                                              default true
 *   max       number    largest value allowed per category (no upper cap; raised
 *                       automatically to the largest value in values / values2 / ask)   default 20
 *   step      number    how much one tap of + / − changes a value. Hold + / − to repeat
 *                       quickly (speeds up ×10 after a while)                        default 1 (0.1 / 0.01 for decimal data)
 *             Bar axis: values up to 100 keep the 1 / 2 / 5 / 10 ticks; bigger or decimal data
 *             auto-scales with nice ticks (e.g. 0–1000 by 200).
 *   statsOf   'values' | 'frequency' | 'none'   'frequency' = labels are numbers (marks, sizes) and
 *             values are how often each occurs (Σfx/Σf)                                  default 'values'
 *   ask       the challenge, one of:
 *               {type:'most'} | {type:'least'}               tap the biggest / smallest category
 *               {type:'read', question:'…', answer:'Mango' | 7}   answer a question about the chart
 *               {type:'build', values:[…]}                   make the chart show these values
 *               {type:'stat', stat:'mean'|'median'|'mode'|'range', value:n}   reach a statistic
 *             default {type:'most'}
 *   challenge string    challenge sentence (else generated)
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const PAL = ['#8b5cf6', '#2ed3a5', '#ffc93c', '#ff6b6b', '#3b82f6', '#ff9f43', '#f472b6'];
  const r2 = v => Math.round(v * 100) / 100;
  const deg = v => Math.abs(v - Math.round(v)) < 1e-9 ? Math.round(v) + '°' : '≈' + (Math.round(v * 10) / 10) + '°';

  Labs.register('datachart', {
    title: 'Data & graphs',
    subjects: ['maths'],
    render(host, p, api) {
      const ex = this.example;
      let labels = Array.isArray(p.labels) && p.labels.length >= 2 ? p.labels.slice(0, 7).map(String) : ex.labels.slice();
      const okVals = a => Array.isArray(a) && a.length === labels.length && a.every(v => Number.isFinite(+v) && +v >= 0);
      const given = [p.values, p.values2, p.ask && p.ask.values].filter(okVals).flat().map(Number);
      // decimals: only when the data itself has decimals (whole-number data behaves exactly as before)
      const dp = Math.min(2, Math.max(0, ...given.map(v => { const t = String(r2(v)).split('.')[1]; return t ? t.length : 0; })));
      const dec = dp > 0, fix = v => dec ? Math.round(v * 10 ** dp) / 10 ** dp : Math.round(v);
      const max = Math.max(5, +p.max > 0 ? +p.max : 20, ...given.map(fix));
      const step = +p.step > 0 ? +p.step : dec ? 10 ** -dp : 1;
      let vals = okVals(p.values) ? p.values.map(v => Math.min(max, fix(+v))) : labels.map((_, i) => (ex.values[i] ?? 3));
      let vals2 = okVals(p.values2) ? p.values2.map(v => Math.min(max, fix(+v))) : null;
      const series = Array.isArray(p.series) && p.series.length === 2 ? p.series.map(String) : ['Class A', 'Class B'];
      const allViews = ['tally', 'picto', 'bar', 'pie'];
      const bigData = Math.max(0, ...vals, ...(vals2 || [])) > 40;
      const defViews = bigData ? ['bar', 'pie'] : allViews.slice();
      let views = Array.isArray(p.views) ? p.views.filter(v => allViews.includes(v)) : defViews.slice();
      if (!views.length) views = defViews.slice();
      if (vals2) views = views.filter(v => v !== 'picto' && v !== 'tally').concat(views.includes('bar') ? [] : ['bar']);
      let view = views.includes(p.view) ? p.view : views[0];
      const icon = String(p.icon || '🍎'), key = Math.max(1, +p.key || 1);
      const unit = String(p.unit || 'students');
      const editable = p.editable !== false;
      const statsOf = ['values', 'frequency', 'none'].includes(p.statsOf) ? p.statsOf : 'values';
      const title = String(p.title || '');
      let edit = 0, won = false;

      // ---- ask ----
      let ask = p.ask && typeof p.ask === 'object' ? p.ask : { type: 'most' };
      if (ask.type === 'build' && !okVals(ask.values)) ask = { type: 'most' };
      if (ask.type === 'stat' && !(['mean', 'median', 'mode', 'range'].includes(ask.stat) && isFinite(+ask.value))) ask = { type: 'most' };
      if (ask.type === 'read' && (ask.answer == null || !ask.question)) ask = { type: 'most' };
      if (!['most', 'least', 'read', 'build', 'stat'].includes(ask.type)) ask = { type: 'most' };
      const chText = p.challenge || (ask.type === 'most' ? `Which has the most ${unit}? Tap it below.` : ask.type === 'least' ? `Which has the fewest ${unit}? Tap it below.`
        : ask.type === 'read' ? ask.question : ask.type === 'build' ? `Make the graph show: ${labels.map((l, i) => `${l} ${ask.values[i]}`).join(', ')}.` : `Change the data so the ${ask.stat} is ${ask.value}.`);

      function stats(v) {
        if (statsOf === 'frequency') {
          const xs = labels.map(Number);
          if (xs.some(x => !isFinite(x))) return null;
          const N = v.reduce((s, f) => s + f, 0); if (!N) return { n: 0 };
          const mean = xs.reduce((s, x, i) => s + x * v[i], 0) / N;
          const list = []; xs.forEach((x, i) => { for (let k = 0; k < v[i]; k++) list.push(x); }); list.sort((a, b) => a - b);
          const med = N % 2 ? list[(N - 1) / 2] : (list[N / 2 - 1] + list[N / 2]) / 2;
          const mf = Math.max(...v); const modes = xs.filter((x, i) => v[i] === mf);
          return { n: N, mean, median: med, mode: modes.length === xs.length && xs.length > 1 ? null : modes, range: list[N - 1] - list[0] };
        }
        const list = v.slice().sort((a, b) => a - b), n = list.length;
        const mean = list.reduce((s, x) => s + x, 0) / n;
        const median = n % 2 ? list[(n - 1) / 2] : (list[n / 2 - 1] + list[n / 2]) / 2;
        const freq = {}; list.forEach(x => { freq[x] = (freq[x] || 0) + 1; });
        const mf = Math.max(...Object.values(freq));
        const modes = mf > 1 ? Object.keys(freq).filter(k => freq[k] === mf).map(Number) : null;
        return { n, mean, median, mode: modes, range: list[n - 1] - list[0] };
      }

      host.innerHTML = `
<style>
.lb-datachart-w{font-size:14px;color:#1b1f3a}
.lb-datachart-ch{font-weight:800;font-size:14px;margin-bottom:5px;line-height:1.25}
.lb-datachart-tabs{display:flex;gap:4px;background:#eef0fb;border-radius:12px;padding:3px}
.lb-datachart-tab{flex:1;min-height:36px;border:none;border-radius:10px;background:transparent;font-family:inherit;font-weight:800;font-size:13px;color:#6b7090;cursor:pointer}
.lb-datachart-tab.on{background:#fff;color:#8b5cf6;box-shadow:0 2px 6px rgba(27,31,58,.1)}
.lb-datachart-svg{width:100%;height:auto;display:block;margin-top:5px;background:#fbfbff;border:2px solid #eef0fb;border-radius:14px}
.lb-datachart-st{display:flex;gap:4px;margin-top:5px}
.lb-datachart-st div{flex:1;background:#f6f4ff;border-radius:9px;text-align:center;padding:2px 0;font-size:10.5px;font-weight:800;color:#6b7090;line-height:1.2}
.lb-datachart-st b{display:block;font-size:14px;color:#1b1f3a}
.lb-datachart-ed{display:flex;gap:4px;margin-top:5px}
.lb-datachart-col{flex:1;min-width:0;display:flex;flex-direction:column;align-items:stretch;gap:2px;text-align:center}
.lb-datachart-col .v{font-weight:900;font-size:15px;line-height:1.1}
.lb-datachart-col .l{font-size:11px;font-weight:800;color:#6b7090;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lb-datachart-pm{min-height:40px;border:none;border-radius:9px;font-family:inherit;font-weight:900;font-size:17px;cursor:pointer;background:#eef0fb;color:#1b1f3a;line-height:1;padding:0}
.lb-datachart-pm.plus{background:#8b5cf6;color:#fff}
.lb-datachart-pm:active{transform:scale(.94)}
.lb-datachart-sw{display:flex;gap:4px;margin-top:5px;align-items:center;font-size:12px;font-weight:800;color:#6b7090}
.lb-datachart-sw button{flex:1;min-height:32px;border:2px solid #e3e6f6;border-radius:10px;background:#fff;font-family:inherit;font-weight:800;font-size:12.5px;cursor:pointer}
.lb-datachart-sw button.on{border-color:currentColor}
.lb-datachart-ans{display:flex;flex-wrap:wrap;gap:5px;margin-top:6px}
.lb-datachart-a{flex:1;min-width:56px;min-height:42px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:14px;cursor:pointer;background:#ffc93c;color:#1b1f3a;box-shadow:0 3px 0 #d99a00;padding:0 6px}
.lb-datachart-a.bad{background:#ffd6d6;box-shadow:0 3px 0 #ffb0b0;color:#c23b3b}
.lb-datachart-a.good{background:#2ed3a5;box-shadow:0 3px 0 #1a9c78;color:#fff}
.lb-datachart-msg{font-size:12.5px;font-weight:700;color:#6b7090;margin-top:4px;min-height:16px}
.lb-datachart-g{animation:lbdcin .35s ease both}
@keyframes lbdcin{from{opacity:.2}}
</style>
<div class="lb-datachart-w">
  <div class="lb-datachart-ch">🎯 Challenge: ${esc(chText)}</div>
  ${views.length > 1 ? `<div class="lb-datachart-tabs">${views.map(v => `<button class="lb-datachart-tab" data-view="${v}">${{ tally: 'Tally', picto: 'Picto', bar: vals2 ? 'Double bar' : 'Bar', pie: 'Pie' }[v]}</button>`).join('')}</div>` : ''}
  <svg class="lb-datachart-svg" viewBox="0 0 360 180"></svg>
  ${statsOf !== 'none' ? '<div class="lb-datachart-st"></div>' : ''}
  ${editable && vals2 ? `<div class="lb-datachart-sw">Edit: <button data-s="0" style="color:#8b5cf6">${esc(series[0])}</button><button data-s="1" style="color:#ff9f43">${esc(series[1])}</button></div>` : ''}
  ${editable ? '<div class="lb-datachart-ed"></div>' : ''}
  ${['most', 'least', 'read'].includes(ask.type) ? '<div class="lb-datachart-ans"></div>' : ''}
  <div class="lb-datachart-msg"></div>
</div>`;
      const $ = s => host.querySelector(s);
      const svg = $('.lb-datachart-svg'), stEl = $('.lb-datachart-st'), ed = $('.lb-datachart-ed'), ans = $('.lb-datachart-ans'), msg = $('.lb-datachart-msg');
      const W = 360, H = 180;

      const num = v => +(+v).toFixed(10);   // tidy float noise (0.30000000004 → 0.3)
      // y-axis scale for the bar graph. Whole numbers up to 100 keep the original ticks;
      // anything bigger (or decimal) gets 'nice' ticks of 1 / 2 / 2.5 / 5 × 10^k, about 5 steps.
      function scale(m) {
        if (!dec && m <= 100) {
          const top = Math.max(5, Math.ceil(Math.max(m, 1) / 5) * 5);
          return { top, stepT: top <= 10 ? 1 : top <= 20 ? 2 : top <= 50 ? 5 : 10 };
        }
        if (!(m > 0)) return { top: 5, stepT: 1 };
        const raw = m / 5, mag = 10 ** Math.floor(Math.log10(raw)), f = raw / mag;
        const stepT = num((f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * mag);
        return { top: num(Math.ceil(m / stepT - 1e-9) * stepT), stepT };
      }
      function tallyMarks(x, y, n, h) {
        let g = '', cx = x;
        for (let k = 0; k < n; k++) {
          const inGroup = k % 5;
          if (inGroup === 4) { g += `<line x1="${cx - 4 * 7 - 3}" y1="${y + h - 2}" x2="${cx + 1}" y2="${y + 2}" stroke="#ff6b6b" stroke-width="2.6" stroke-linecap="round"/>`; cx += 10; }
          else { g += `<line x1="${cx}" y1="${y}" x2="${cx}" y2="${y + h}" stroke="#1b1f3a" stroke-width="2.6" stroke-linecap="round"/>`; cx += 7; }
        }
        return g;
      }
      function draw() {
        let g = `<text x="${W / 2}" y="16" text-anchor="middle" font-size="13" font-weight="900" fill="#1b1f3a">${esc(title)}</text>`;
        const n = labels.length;
        if (view === 'tally' || view === 'picto') {
          const rowH = Math.min(30, (H - 44) / n), top = 24, lw = 74;
          labels.forEach((l, i) => {
            const y = top + i * rowH;
            g += `<rect x="6" y="${y + 1}" width="${W - 12}" height="${rowH - 2}" rx="7" fill="${i % 2 ? '#fff' : '#f4f2ff'}"/>`;
            g += `<text x="12" y="${y + rowH / 2 + 4}" font-size="12" font-weight="800" fill="#1b1f3a">${esc(l.length > 10 ? l.slice(0, 9) + '…' : l)}</text>`;
            if (view === 'tally') {
              const cap = 25, nT = Math.round(vals[i]);
              g += tallyMarks(lw + 10, y + 5, Math.min(cap, nT), rowH - 10);
              if (nT > cap) g += `<text x="${lw + 10 + 5 * 38 + 2}" y="${y + rowH / 2 + 4}" font-size="13" font-weight="900" fill="#6b7090">…</text>`;
              g += `<text x="${W - 14}" y="${y + rowH / 2 + 4}" text-anchor="end" font-size="13" font-weight="900" fill="#8b5cf6">${vals[i]}</text>`;
            } else {
              const full = Math.floor(vals[i] / key), part = (vals[i] % key) / key;
              const slots = Math.max(1, Math.ceil(max / key)), capI = 40, cut = slots > capI && full > capI - 1;
              const fs = Math.min(rowH - 8, 20), step = Math.min(fs + 3, (W - lw - 20) / Math.min(slots, capI));
              for (let k = 0; k < (cut ? capI - 1 : full); k++) g += `<text x="${lw + 8 + k * step}" y="${y + rowH / 2 + fs * 0.36}" font-size="${fs}">${esc(icon)}</text>`;
              if (cut) g += `<text x="${W - 12}" y="${y + rowH / 2 + 4}" text-anchor="end" font-size="11" font-weight="900" fill="#8b5cf6" paint-order="stroke" stroke="#fff" stroke-width="3">…${vals[i]}</text>`;
              else if (part > 0) {
                const cid = 'lbdc' + Math.random().toString(36).slice(2, 7);
                g += `<clipPath id="${cid}"><rect x="${lw + 8 + full * step}" y="${y}" width="${fs * 1.1 * part}" height="${rowH}"/></clipPath><text clip-path="url(#${cid})" x="${lw + 8 + full * step}" y="${y + rowH / 2 + fs * 0.36}" font-size="${fs}">${esc(icon)}</text>`;
              }
            }
          });
          if (view === 'picto') g += `<text x="${W - 10}" y="${H - 6}" text-anchor="end" font-size="11.5" font-weight="800" fill="#6b7090">Key: ${esc(icon)} = ${key} ${esc(unit)}${key > 1 ? ` · half = ${key / 2}` : ''}</text>`;
          else g += `<text x="${W - 10}" y="${H - 6}" text-anchor="end" font-size="11.5" font-weight="800" fill="#6b7090">4 lines + 1 across = 5</text>`;
        } else if (view === 'bar') {
          const B = H - 24, T = 30, all = vals2 ? vals.concat(vals2) : vals;
          const { top, stepT } = scale(Math.max(...all, 0));
          const ticks = []; for (let k = 0; k * stepT <= top + stepT * 1e-6; k++) ticks.push(num(k * stepT));
          const L = Math.max(30, 8 + Math.max(...ticks.map(t => String(t).length)) * 5.6);
          const y = v => B - v / top * (B - T);
          ticks.forEach(t => { g += `<line x1="${L}" x2="${W - 6}" y1="${y(t)}" y2="${y(t)}" stroke="#eef0fb"/><text x="${L - 4}" y="${y(t) + 3}" text-anchor="end" font-size="9.5" font-weight="700" fill="#6b7090">${t}</text>`; });
          const slot = (W - L - 8) / n, bw = Math.min(vals2 ? 20 : 34, slot * (vals2 ? 0.38 : 0.6));
          labels.forEach((l, i) => {
            const cx = L + slot * (i + 0.5);
            const bars = vals2 ? [[vals[i], '#8b5cf6', cx - bw / 2 - 1], [vals2[i], '#ff9f43', cx + bw / 2 + 1]] : [[vals[i], PAL[i % PAL.length], cx]];
            bars.forEach(([v, c, bx]) => {
              g += `<rect x="${bx - bw / 2}" y="${y(v)}" width="${bw}" height="${B - y(v)}" rx="4" fill="${c}"/>`;
              g += `<text x="${bx}" y="${y(v) - 3}" text-anchor="middle" font-size="10" font-weight="900" fill="#1b1f3a">${v}</text>`;
            });
            g += `<text x="${cx}" y="${B + 14}" text-anchor="middle" font-size="${n > 5 ? 10 : 11.5}" font-weight="800" fill="#1b1f3a">${esc(l.length > 8 ? l.slice(0, 7) + '…' : l)}</text>`;
          });
          g += `<line x1="${L}" x2="${W - 6}" y1="${B}" y2="${B}" stroke="#1b1f3a" stroke-width="1.5"/><line x1="${L}" x2="${L}" y1="${T - 6}" y2="${B}" stroke="#1b1f3a" stroke-width="1.5"/>`;
          if (vals2) g += `<g transform="translate(${W - 150} 24)"><rect width="10" height="10" rx="2" fill="#8b5cf6"/><text x="14" y="9" font-size="10.5" font-weight="800">${esc(series[0])}</text><rect x="74" width="10" height="10" rx="2" fill="#ff9f43"/><text x="88" y="9" font-size="10.5" font-weight="800">${esc(series[1])}</text></g>`;
          else {
            // keep the unit label clear of the centred title (long units are shortened with …)
            const room = title ? (W / 2 - title.length * 3.6) - (L + 10) : W - L - 20, fit = Math.max(4, Math.floor(room / 5.6));
            g += `<text x="${L + 4}" y="${T - 10}" font-size="10" font-weight="800" fill="#6b7090">${esc(unit.length > fit ? unit.slice(0, fit - 1) + '…' : unit)}</text>`;
          }
        } else {
          const tot = num(vals.reduce((s, v) => s + v, 0)), C = [98, 100], R = 70;
          if (vals2) g += `<text x="196" y="${H - 22}" font-size="10" font-weight="800" fill="#8b5cf6">showing ${esc(series[0])}</text>`;
          if (!tot) g += `<circle cx="${C[0]}" cy="${C[1]}" r="${R}" fill="#eef0fb"/><text x="${C[0]}" y="${C[1] + 4}" text-anchor="middle" font-size="12" font-weight="800" fill="#6b7090">no data</text>`;
          let a0 = -90;
          vals.forEach((v, i) => {
            if (!v) return;
            const ang = v / tot * 360, a1 = a0 + ang, rad = a => a * Math.PI / 180;
            const p0 = [C[0] + R * Math.cos(rad(a0)), C[1] + R * Math.sin(rad(a0))], p1 = [C[0] + R * Math.cos(rad(a1)), C[1] + R * Math.sin(rad(a1))];
            g += ang >= 359.99 ? `<circle cx="${C[0]}" cy="${C[1]}" r="${R}" fill="${PAL[i % PAL.length]}"/>` : `<path d="M${C[0]} ${C[1]}L${p0[0]} ${p0[1]}A${R} ${R} 0 ${ang > 180 ? 1 : 0} 1 ${p1[0]} ${p1[1]}Z" fill="${PAL[i % PAL.length]}" stroke="#fff" stroke-width="2"/>`;
            if (ang >= 22) { const m = rad(a0 + ang / 2); g += `<text x="${C[0] + R * 0.62 * Math.cos(m)}" y="${C[1] + R * 0.62 * Math.sin(m) + 4}" text-anchor="middle" font-size="11" font-weight="900" fill="#fff" paint-order="stroke" stroke="rgba(0,0,0,.25)" stroke-width="2">${Math.round(ang * 10) / 10}°</text>`; }
            a0 = a1;
          });
          const lh = Math.min(24, (H - 40) / n);
          labels.forEach((l, i) => {
            const y = 36 + i * lh, ang = tot ? vals[i] / tot * 360 : 0;
            g += `<rect x="196" y="${y - 9}" width="11" height="11" rx="3" fill="${PAL[i % PAL.length]}"/><text x="211" y="${y}" font-size="11" font-weight="800" fill="#1b1f3a">${esc(l.length > 9 ? l.slice(0, 8) + '…' : l)}</text><text x="352" y="${y}" text-anchor="end" font-size="10.5" font-weight="800" fill="#6b7090">${vals[i]}/${tot} → ${deg(ang)}</text>`;
          });
          g += `<text x="196" y="${H - 8}" font-size="10" font-weight="800" fill="#6b7090">angle = value ÷ total × 360°</text>`;
        }
        svg.innerHTML = `<g class="lb-datachart-g">${g}</g>`;
        host.querySelectorAll('.lb-datachart-tab').forEach(b => b.classList.toggle('on', b.dataset.view === view));
        if (stEl) {
          const s = stats(vals);
          if (!s) stEl.innerHTML = '<div>Labels must be numbers for frequency stats</div>';
          else if (!s.n) stEl.innerHTML = '<div>No data yet</div>';
          else stEl.innerHTML = `<div>Mean<b>${r2(s.mean)}</b></div><div>Median<b>${r2(s.median)}</b></div><div>Mode<b>${s.mode ? s.mode.join(', ') : 'none'}</b></div><div>Range<b>${r2(s.range)}</b></div>`;
        }
        if (ed) {
          const cur = edit ? vals2 : vals;
          ed.innerHTML = labels.map((l, i) => `<div class="lb-datachart-col"><button class="lb-datachart-pm plus" data-pm="${i}" data-d="1" aria-label="add one ${esc(l)}">+</button><span class="v" style="color:${vals2 ? (edit ? '#ff9f43' : '#8b5cf6') : PAL[i % PAL.length]}">${cur[i]}</span><button class="lb-datachart-pm" data-pm="${i}" data-d="-1" aria-label="remove one ${esc(l)}">−</button><span class="l">${esc(l)}</span></div>`).join('');
          host.querySelectorAll('.lb-datachart-sw button').forEach(b => b.classList.toggle('on', +b.dataset.s === edit));
        }
      }
      function drawAns() {
        if (!ans) return;
        let opts;
        if (ask.type === 'read' && typeof ask.answer === 'number') {
          const a = ask.answer, d = key > 1 ? key : 1, set = [a, a + d, Math.max(0, a - d)];
          if (set[2] === a) set[2] = a + 2 * d;
          opts = set.sort(() => Math.random() - 0.5).map(String);
        } else opts = labels;
        ans.innerHTML = opts.map(o => `<button class="lb-datachart-a" data-ans="${esc(o)}">${esc(o)}</button>`).join('');
      }
      function check() {
        if (won) return;
        if (ask.type === 'build' && vals.every((v, i) => Math.abs(v - +ask.values[i]) < 1e-9)) { won = true; api.sfx('correct'); api.win(`Your ${view === 'pie' ? 'pie chart' : 'graph'} shows ${labels.map((l, i) => `${l} ${vals[i]}`).join(', ')}. Total ${r2(vals.reduce((s, v) => s + v, 0))} ${unit}.`); }
        if (ask.type === 'stat') {
          const s = stats(vals); if (!s || !s.n) return;
          const got = ask.stat === 'mode' ? (s.mode && s.mode.length === 1 ? s.mode[0] : NaN) : s[ask.stat];
          if (Math.abs(got - +ask.value) < 1e-6) {
            won = true; api.sfx('correct');
            const how = ask.stat === 'mean' ? (statsOf === 'frequency' ? `Σfx ÷ Σf = ${r2(s.mean)}` : `total ${r2(vals.reduce((a, b) => a + b, 0))} ÷ ${vals.length} = ${r2(s.mean)}`) : ask.stat === 'range' ? `highest − lowest = ${r2(s.range)}` : ask.stat === 'median' ? `middle value = ${r2(s.median)}` : `most frequent value = ${got}`;
            api.win(`The ${ask.stat} is ${ask.value}: ${how}.`);
          }
        }
      }
      // change one value by d × step × mult; returns false at the limits
      function bump(i, d, mult) {
        const arr = edit ? vals2 : vals, nv = num(arr[i] + d * step * mult);
        if (nv < -1e-9 || nv > max + 1e-9) { api.sfx('hmm'); return false; }
        arr[i] = nv; api.sfx('tap'); draw(); check();
        if (['most', 'least'].includes(ask.type)) host.querySelectorAll('.lb-datachart-a').forEach(x => x.classList.remove('bad', 'good'));
        return true;
      }
      // press and hold + / − to repeat (handy for big numbers like 943)
      let holdT = null, repeated = false;
      const stopHold = () => { clearTimeout(holdT); holdT = null; };
      function onDown(e) {
        const b = e.target.closest('.lb-datachart-pm'); if (!b) return;
        const i = +b.dataset.pm, d = +b.dataset.d; let n = 0; repeated = false; stopHold();
        const tick = () => {
          n++; repeated = true;
          // after 12 single steps jump by 10 steps at a time, but never past a multiple of 10 steps
          const cur = (edit ? vals2 : vals)[i] / step, mult = n > 12 && Math.abs(num(cur) % 10) < 1e-6 ? 10 : 1;
          if (won || !bump(i, d, mult)) return stopHold();
          holdT = setTimeout(tick, n > 12 ? 110 : 90);
        };
        holdT = setTimeout(tick, 450);
      }
      host.addEventListener('pointerdown', onDown);
      window.addEventListener('pointerup', stopHold); window.addEventListener('pointercancel', stopHold);
      function onClick(e) {
        const b = e.target.closest('button'); if (!b) return;
        if (b.dataset.view) { view = b.dataset.view; api.sfx('tap'); draw(); return; }
        if (b.dataset.s != null) { edit = +b.dataset.s; api.sfx('tap'); draw(); return; }
        if (b.dataset.pm != null) {
          if (repeated) { repeated = false; return; }
          bump(+b.dataset.pm, +b.dataset.d, 1);
          return;
        }
        if (b.dataset.ans != null) {
          if (won) return;
          const a = b.dataset.ans;
          let ok = false, why = '';
          if (ask.type === 'most' || ask.type === 'least') {
            const tv = ask.type === 'most' ? Math.max(...vals) : Math.min(...vals);
            const winners = labels.filter((l, i) => vals[i] === tv);
            ok = winners.includes(a) && winners.length === 1;
            if (winners.length > 1 && winners.includes(a)) { msg.textContent = `It's a tie between ${winners.join(' and ')}! Change the data with + / − and try again.`; api.sfx('hmm'); return; }
            why = `${a} has the ${ask.type === 'most' ? 'most' : 'fewest'}: ${tv} ${unit}.`;
          } else { ok = String(ask.answer).trim().toLowerCase() === a.trim().toLowerCase(); why = `Answer: ${a}.`; }
          if (ok) { won = true; b.classList.add('good'); api.sfx('correct'); msg.textContent = why; api.win(why); }
          else { b.classList.add('bad'); api.sfx('wrong'); msg.textContent = view === 'pie' ? 'Look at the sizes of the slices again.' : 'Look at the lengths again — compare carefully.'; }
        }
      }
      host.addEventListener('click', onClick);
      draw(); drawAns();
      return () => { stopHold(); host.removeEventListener('click', onClick); host.removeEventListener('pointerdown', onDown); window.removeEventListener('pointerup', stopHold); window.removeEventListener('pointercancel', stopHold); };
    },
    example: { title: 'Favourite fruit of Class 3', labels: ['Apple', 'Mango', 'Banana', 'Grapes'], values: [4, 7, 3, 5], views: ['tally', 'picto', 'bar', 'pie'], icon: '🍎', key: 1, unit: 'students', editable: true, max: 20, statsOf: 'values' },
    examples: [
      { title: 'Books read (1 📘 = 2 books)', labels: ['Ravi', 'Asha', 'Meera', 'John', 'Zoya'], values: [6, 9, 4, 8, 3], views: ['picto', 'bar'], icon: '📘', key: 2, unit: 'books', ask: { type: 'stat', stat: 'mean', value: 7 }, challenge: 'Change the books so the mean is exactly 7.' },
      { title: 'Marks in a test (out of 5)', labels: ['1', '2', '3', '4', '5'], values: [2, 3, 6, 5, 4], views: ['bar', 'pie'], view: 'bar', unit: 'students', statsOf: 'frequency', editable: false, ask: { type: 'read', question: 'How many students scored 3 marks?', answer: 6 } },
      { title: 'Rainfall (cm)', labels: ['Jun', 'Jul', 'Aug', 'Sep'], values: [12, 18, 15, 9], values2: [10, 20, 13, 7], series: ['2024', '2025'], unit: 'cm', ask: { type: 'build', values: [12, 18, 15, 11] }, challenge: 'Sep 2024 had 11 cm, not 9. Fix the purple bar!' },
      { title: 'Sex ratio (females per 1000 males)', labels: ['India', 'Kerala', 'Haryana', 'Bihar'], values: [943, 1084, 879, 918], views: ['bar'], unit: 'females', editable: false, statsOf: 'none', ask: { type: 'least' }, challenge: 'India’s sex ratio is 943. Which state has the lowest sex ratio? Tap it.' }
    ]
  });
})();
