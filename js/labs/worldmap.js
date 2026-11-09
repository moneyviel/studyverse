/* Knowtopia Concept Lab: worldmap — simple equirectangular world map.

   PARAMS (all optional — missing ones fall back to `example`)
   ─────────────────────────────────────────────────────────────────────────────────────────
   title      string   Heading text.                                            'World map'
   mode       string   Starting mode: 'explore' | 'find' | 'time'.             'explore'
   modes      string[] Mode tabs to show (one entry = no tabs).                [mode]
   challenge  string   Challenge text for the starting mode (else generated).
   points     object[] Places: {name, lat, lon, emoji?, info?}.                 (example cities)
   grid       number   Grid spacing in degrees (0 = off). Special lines (Equator, Tropics,
                       Polar circles, Prime Meridian, 180°) are always drawn.     30
   goal       number   explore: different things (continents/oceans/points/lines) to tap.  5
   ask        string[] find: names to ask — continents ('Asia', 'Africa', 'Europe',
                       'North America', 'South America', 'Australia', 'Antarctica'), oceans
                       ('Pacific Ocean', 'Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean',
                       'Southern Ocean') or point names.                         all continents+oceans
   rounds     number   find: correct answers needed.                             5
   radius     number   find: km tolerance for points.                            800
   gmt        number   time: starting time at Greenwich in hours (0–24, e.g. 12.5).   12
   home       object   time: reference place {name, lon} for "difference from home".  {name:'India (IST)', lon:82.5}
   target     object   time: {offset: hours ahead(+)/behind(−) Greenwich} or {lon}, tol (deg, default 2).
                       Default {offset: 5.5}.

   What the child does: explore = tap continents, oceans, cities and special latitude lines;
   find = tap the asked continent/ocean/city; time = drag a meridian across the map and change the
   time at Greenwich — sees longitude → time difference (15° = 1 hour, 1° = 4 min), day/night side.
*/
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const CONT = {
    'Asia': { e: '🏯', c: '#ffc93c', info: 'Largest continent with the most people. India is in Asia.', polys: [
      [[30, 70], [60, 70], [100, 77], [140, 72], [180, 68], [170, 60], [160, 55], [140, 50], [130, 42], [122, 40], [121, 30], [110, 20], [108, 12], [105, 9], [100, 13], [98, 8], [92, 20], [88, 22], [80, 15], [77, 8], [73, 20], [67, 25], [57, 25], [52, 28], [48, 30], [44, 12], [36, 30], [28, 41], [40, 45], [50, 47], [40, 66]],
      [[36, 30], [44, 12], [52, 15], [58, 22], [56, 26], [50, 29], [48, 30]],
      [[130, 31], [135, 34], [141, 38], [142, 44], [139, 40], [133, 34]],
      [[95, 5], [106, -6], [115, -8], [120, -9], [125, -8], [110, -3], [100, -1]],
      [[109, 1], [119, 7], [119, 0], [116, -4], [110, -3]],
      [[131, -1], [141, -3], [150, -10], [141, -9], [134, -4]],
      [[80, 9.8], [81.8, 7.5], [80.6, 6], [79.8, 8]]] },
    'Europe': { e: '🏰', c: '#3b82f6', info: 'A small continent with many countries, joined to Asia.', polys: [
      [[-10, 36], [-9, 43], [-2, 48], [5, 52], [10, 58], [5, 62], [15, 69], [30, 70], [40, 66], [50, 47], [40, 45], [28, 41], [20, 40], [15, 38], [10, 44], [3, 43], [-5, 36]],
      [[-5, 50], [1, 51], [-2, 56], [-6, 58], [-5, 54]], [[-24, 64], [-14, 64], [-15, 66], [-22, 66]]] },
    'Africa': { e: '🦁', c: '#ff9f43', info: 'Second largest continent. The Equator passes through its middle.', polys: [
      [[-17, 21], [-10, 30], [10, 37], [32, 31], [43, 12], [51, 12], [40, -10], [35, -25], [20, -35], [12, -17], [9, 4], [-8, 5], [-17, 14]],
      [[44, -16], [50, -15], [50, -25], [45, -25]]] },
    'North America': { e: '🦅', c: '#ff6b6b', info: 'Has Canada, USA and Mexico. Greenland is part of it too.', polys: [
      [[-168, 66], [-160, 70], [-130, 70], [-95, 72], [-80, 73], [-62, 60], [-55, 50], [-66, 45], [-75, 35], [-81, 25], [-97, 26], [-97, 18], [-87, 15], [-80, 8], [-90, 14], [-105, 20], [-115, 30], [-124, 40], [-125, 49], [-140, 60], [-165, 60]],
      [[-50, 60], [-30, 68], [-20, 80], [-40, 83], [-60, 80], [-55, 70]]] },
    'South America': { e: '🦜', c: '#2ed3a5', info: 'Home of the Amazon rainforest and the Andes mountains.', polys: [
      [[-80, 8], [-62, 10], [-50, 0], [-35, -7], [-40, -22], [-53, -34], [-65, -42], [-68, -55], [-75, -50], [-72, -30], [-70, -18], [-81, -5]]] },
    'Australia': { e: '🦘', c: '#8b5cf6', info: 'Smallest continent — a country and a continent.', polys: [
      [[114, -22], [122, -18], [130, -12], [137, -12], [142, -11], [146, -19], [153, -28], [150, -37], [140, -38], [132, -32], [115, -34]],
      [[172, -35], [178, -38], [174, -42], [167, -46], [172, -41]]] },
    'Antarctica': { e: '🐧', c: '#cfe3f7', info: 'Icy continent around the South Pole. No country owns it.', polys: [
      [[-180, -70], [-120, -72], [-60, -65], [0, -70], [60, -67], [120, -66], [180, -70], [180, -90], [-180, -90]]] }
  };
  const OCEANS = {
    'Pacific Ocean': { e: '🌊', info: 'Largest and deepest ocean, between Asia/Australia and the Americas.', at: [[-150, 10], [165, 20]] },
    'Atlantic Ocean': { e: '🚢', info: 'Second largest ocean, between the Americas and Europe/Africa.', at: [[-35, 20]] },
    'Indian Ocean': { e: '🐬', info: 'Third largest ocean. The only ocean named after a country — India!', at: [[75, -15]] },
    'Arctic Ocean': { e: '🐻‍❄️', info: 'Smallest ocean, around the North Pole. Mostly frozen.', at: [[0, 80]] },
    'Southern Ocean': { e: '🐧', info: 'Cold ocean that circles Antarctica.', at: [[-100, -64]] }
  };
  const SPECIAL = [
    { name: 'Equator', lat: 0, c: '#ff6b6b', info: '0° latitude. Divides Earth into Northern and Southern Hemispheres.' },
    { name: 'Tropic of Cancer', lat: 23.44, c: '#ff9f43', info: '23.5° N. The Sun is overhead here around 21 June. It passes through India.' },
    { name: 'Tropic of Capricorn', lat: -23.44, c: '#ff9f43', info: '23.5° S. The Sun is overhead here around 22 December.' },
    { name: 'Arctic Circle', lat: 66.56, c: '#3b82f6', info: '66.5° N. North of it there is at least one day of 24-hour daylight in summer.' },
    { name: 'Antarctic Circle', lat: -66.56, c: '#3b82f6', info: '66.5° S. Circle around the far south.' },
    { name: 'Prime Meridian', lon: 0, c: '#8b5cf6', info: '0° longitude, through Greenwich (London). Time here is GMT.' },
    { name: '180° meridian', lon: 180, c: '#8b5cf6', info: '180° longitude. The International Date Line mostly follows it.' }
  ];
  const R = Math.PI / 180;
  const km = (a, b) => { const dLa = (b[1] - a[1]) * R, dLo = (b[0] - a[0]) * R; const h = Math.sin(dLa / 2) ** 2 + Math.cos(a[1] * R) * Math.cos(b[1] * R) * Math.sin(dLo / 2) ** 2; return 12742 * Math.asin(Math.sqrt(h)); };
  const inPoly = (pt, poly) => { let ins = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const [xi, yi] = poly[i], [xj, yj] = poly[j]; if ((yi > pt[1]) !== (yj > pt[1]) && pt[0] < (xj - xi) * (pt[1] - yi) / (yj - yi) + xi) ins = !ins; } return ins; };
  const contAt = ll => Object.keys(CONT).find(k => CONT[k].polys.some(pl => inPoly(ll, pl))) || null;
  const oceanAt = ([lo, la]) => {
    if (la <= -60) return 'Southern Ocean';
    if (la >= 68) return 'Arctic Ocean';
    if ((lo >= -70 && lo <= 20) || (la > 8 && lo >= -100 && lo < -70) || (la > 47 && lo >= -100 && lo <= 40) || (la > 30 && la <= 47 && lo >= -6 && lo <= 42)) return 'Atlantic Ocean';
    if ((lo > 20 && lo <= 100 && la < 31) || (la < 0 && lo > 100 && lo <= 147) || (la < -20 && lo > 20 && lo <= 147)) return 'Indian Ocean';
    return 'Pacific Ocean';
  };
  const nf = v => (Math.abs(v) % 1 ? Math.abs(v).toFixed(1) : Math.abs(v).toFixed(0));
  const fmtLat = v => nf(v) + '°' + (Math.abs(v) < 0.5 ? '' : v > 0 ? ' N' : ' S');
  const fmtLon = v => nf(v) + '°' + (Math.abs(v) < 0.5 || Math.abs(v) > 179.5 ? '' : v > 0 ? ' E' : ' W');
  const fmtDiff = mins => { const s = mins < 0 ? '−' : '+', a = Math.abs(Math.round(mins)); return `${s}${Math.floor(a / 60)} h ${String(a % 60).padStart(2, '0')} min`; };
  const clock = h => { h = ((h % 24) + 24) % 24; let H = Math.floor(h + 1e-9), M = Math.round((h - H) * 60); if (M === 60) { M = 0; H = (H + 1) % 24; } const ap = H < 12 ? 'AM' : 'PM'; return `${(H % 12) || 12}:${String(M).padStart(2, '0')} ${ap}`; };
  const MODES = { explore: '👆 Explore', find: '🔎 Find', time: '🕒 Time zones' };

  Labs.register('worldmap', {
    title: 'World map', subjects: ['social', 'geography', 'evs', 'science'],
    render(host, p, api) {
      const ex = this.example || {};
      const points = Array.isArray(p.points) ? p.points : ex.points;
      const modes = (Array.isArray(p.modes) && p.modes.length ? p.modes : [p.mode || 'explore']).filter(m => MODES[m]);
      if (!modes.length) modes.push('explore');
      let mode = modes.includes(p.mode) ? p.mode : modes[0];
      const step = p.grid === 0 || p.grid === false ? 0 : (+p.grid > 0 ? +p.grid : 30);
      const goal = Math.max(1, +p.goal || 5);
      const all = [...Object.keys(CONT), ...Object.keys(OCEANS), ...points.map(o => o.name)];
      const askNames = (Array.isArray(p.ask) && p.ask.length ? p.ask : [...Object.keys(CONT), ...Object.keys(OCEANS)]).filter(n => all.includes(n));
      const rounds = Math.max(1, Math.min(+p.rounds || 5, askNames.length || 1));
      const radius = +p.radius > 0 ? +p.radius : 800;
      const home = p.home && p.home.lon != null ? { name: p.home.name || 'Home', lon: +p.home.lon } : { name: 'India (IST)', lon: 82.5 };
      const tg = p.target && typeof p.target === 'object' ? p.target : { offset: 5.5 };
      const tLon = tg.lon != null ? +tg.lon : (tg.offset != null ? +tg.offset * 15 : 82.5), tTol = +tg.tol > 0 ? +tg.tol : 2;
      const LAT1 = 84, LAT0 = -78, W = 360, H = LAT1 - LAT0;
      const X = lon => lon + 180, Y = lat => LAT1 - lat;
      const path = pts => pts.map((q, i) => (i ? 'L' : 'M') + X(q[0]).toFixed(1) + ' ' + Y(Math.max(LAT0, q[1])).toFixed(1)).join('') + 'Z';

      host.innerHTML = `<div class="lb-worldmap-w"><style>
.lb-worldmap-w{font-size:14px;color:#1b1f3a;user-select:none;-webkit-user-select:none}
.lb-worldmap-ch{font-weight:800;font-size:14px;line-height:1.3;margin-bottom:6px}
.lb-worldmap-tabs{display:flex;gap:6px;margin-bottom:6px}
.lb-worldmap-tabs button{flex:1;min-height:40px;border:none;border-radius:12px;background:#eef0fb;color:#1b1f3a;font:inherit;font-weight:800;font-size:13px;cursor:pointer}
.lb-worldmap-tabs button.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-worldmap-stage{position:relative;border-radius:16px;overflow:hidden;background:#cfe6fb}
.lb-worldmap-stage svg{display:block;width:100%;height:auto}
.lb-worldmap-land{stroke:#fff;stroke-width:.5;stroke-linejoin:round;cursor:pointer;transition:filter .2s}
.lb-worldmap-land.sel{filter:brightness(1.12) drop-shadow(0 0 2px #1b1f3a)}
.lb-worldmap-plain .lb-worldmap-land{fill:#bfe9c4 !important}
.lb-worldmap-grid{stroke:#fff;stroke-width:.35;opacity:.8}
.lb-worldmap-gl{fill:#5b84b1;font-size:5px;font-weight:700}
.lb-worldmap-ol{fill:#4f7fb5;font-size:5.5px;font-weight:800;font-style:italic;pointer-events:none}
.lb-worldmap-pt .d{fill:#ff6b6b;stroke:#fff;stroke-width:.8}
.lb-worldmap-pt.seen .d{fill:#2ed3a5}
.lb-worldmap-pt text{font-size:5.5px;font-weight:800;fill:#1b1f3a;paint-order:stroke;stroke:#fff;stroke-width:1.6px;pointer-events:none}
.lb-worldmap-score{position:absolute;right:6px;top:6px;background:#fff;border-radius:999px;padding:3px 9px;font-weight:800;font-size:12px;box-shadow:0 3px 10px rgba(27,31,58,.15)}
.lb-worldmap-score:empty{display:none}
.lb-worldmap-info{margin-top:6px;background:#f6f7ff;border-radius:14px;padding:8px 10px;min-height:58px;font-size:13px;line-height:1.3}
.lb-worldmap-info b{font-size:14.5px}
.lb-worldmap-info .m{color:#6b7090;font-weight:700;font-size:12px}
.lb-worldmap-big{display:flex;gap:6px;margin-top:4px}
.lb-worldmap-big div{flex:1;background:#fff;border-radius:10px;padding:4px 6px;text-align:center;font-weight:800;font-size:15px;line-height:1.15}
.lb-worldmap-big small{display:block;color:#6b7090;font-size:10.5px;font-weight:700}
.lb-worldmap-ctl{display:flex;align-items:center;gap:8px;margin-top:6px;font-weight:800;font-size:13px}
.lb-worldmap-ctl input{flex:1;accent-color:#8b5cf6;height:32px}
.lb-worldmap-bar{display:flex;align-items:center;gap:8px;margin-top:6px;min-height:40px}
.lb-worldmap-msg{flex:1;font-weight:800;font-size:13.5px;line-height:1.25}
.lb-worldmap-bar button{min-height:40px;border:none;border-radius:12px;padding:0 12px;background:#2ed3a5;color:#fff;font:inherit;font-weight:800;cursor:pointer;box-shadow:0 3px 0 #1a9c78}
.lb-worldmap-ring{fill:none;stroke-width:1.5;animation:lb-worldmap-p .9s ease-out infinite}
@keyframes lb-worldmap-p{from{r:1;opacity:1}to{r:10;opacity:0}}
</style>
<div class="lb-worldmap-ch"></div>
${modes.length > 1 ? `<div class="lb-worldmap-tabs">${modes.map(m => `<button data-m="${m}">${MODES[m]}</button>`).join('')}</div>` : ''}
<div class="lb-worldmap-stage"><svg viewBox="0 0 ${W} ${H}"></svg><div class="lb-worldmap-score"></div></div>
<div class="lb-worldmap-info"></div>
<div class="lb-worldmap-ctl" style="display:none">🕒 Greenwich <input type="range" min="0" max="23.5" step="0.5"><span class="g"></span></div>
<div class="lb-worldmap-bar"><div class="lb-worldmap-msg"></div><button style="display:none"></button></div></div>`;
      const $ = s => host.querySelector(s);
      const svg = $('svg'), info = $('.lb-worldmap-info'), msg = $('.lb-worldmap-msg'), score = $('.lb-worldmap-score'), act = $('.lb-worldmap-bar button'), ctl = $('.lb-worldmap-ctl'), gIn = ctl.querySelector('input'), gOut = ctl.querySelector('.g');
      const NS = 'http://www.w3.org/2000/svg', timers = [];
      let seen = new Set(), won = false, askQ = [], askI = 0, correct = 0, tries = 0, mer = 0, gmt = +p.gmt >= 0 && +p.gmt <= 24 ? +p.gmt % 24 : 12, dragging = false, busy = false;
      gIn.value = gmt;

      const toLL = ev => { const pt = svg.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY; const q = pt.matrixTransform(svg.getScreenCTM().inverse()); return [Math.max(-180, Math.min(180, q.x - 180)), LAT1 - q.y]; };
      const pxPerUnit = () => svg.getBoundingClientRect().width / W;
      function challengeText() {
        if (p.challenge && mode === (modes.includes(p.mode) ? p.mode : modes[0])) return p.challenge;
        if (mode === 'explore') return `Tap ${goal} different continents, oceans, places or lines`;
        if (mode === 'find') return `Find ${rounds} on the map — tap the right spot`;
        return tg.lon != null ? `Drag the time line to longitude ${fmtLon(tLon)}` : `Drag the time line to where the time is ${fmtDiff(tLon * 4)} from Greenwich`;
      }
      function draw() {
        let s = `<rect width="${W}" height="${H}" fill="#cfe6fb"/>`;
        if (step) {
          for (let la = -90 + step; la < 90; la += step) if (la <= LAT1 && la >= LAT0) s += `<line class="lb-worldmap-grid" x1="0" x2="${W}" y1="${Y(la)}" y2="${Y(la)}"/>`;
          for (let lo = -180 + step; lo < 180; lo += step) s += `<line class="lb-worldmap-grid" y1="0" y2="${H}" x1="${X(lo)}" x2="${X(lo)}"/>`;
        }
        if (mode !== 'find') Object.entries(OCEANS).forEach(([n, o]) => o.at.forEach(a => { s += `<text class="lb-worldmap-ol" x="${X(a[0])}" y="${Y(a[1])}" text-anchor="middle">${n.replace(' Ocean', '')}</text>`; }));
        Object.entries(CONT).forEach(([n, c]) => { s += `<g data-c="${n}">${c.polys.map(pl => `<path class="lb-worldmap-land${seen.has(n) && mode === 'explore' ? ' sel' : ''}" fill="${c.c}" d="${path(pl)}"/>`).join('')}</g>`; });
        if (mode === 'time') s += `<g class="night" style="pointer-events:none"></g>`;
        SPECIAL.forEach(l => {
          if (l.lat != null) s += `<line x1="0" x2="${W}" y1="${Y(l.lat)}" y2="${Y(l.lat)}" stroke="${l.c}" stroke-width="${l.lat ? .7 : 1}" stroke-dasharray="${l.lat ? '3 2' : ''}"/><text class="lb-worldmap-gl" style="fill:${l.c}" x="2" y="${Y(l.lat) - 1.5}">${l.name}</text>`;
          else if (l.lon === 0) s += `<line y1="0" y2="${H}" x1="${X(0)}" x2="${X(0)}" stroke="${l.c}" stroke-width=".8"/><text class="lb-worldmap-gl" style="fill:${l.c}" x="${X(0) + 1.5}" y="${H - 3}">0°</text>`;
        });
        if (step) for (let lo = -180 + step; lo < 180; lo += step) if (lo && lo % 30 === 0) s += `<text class="lb-worldmap-gl" x="${X(lo) + 1}" y="${H - 3}">${Math.abs(lo)}°${lo > 0 ? 'E' : 'W'}</text>`;
        if (mode !== 'find') points.forEach((o, i) => { const x = X(+o.lon), y = Y(+o.lat), left = +o.lon > 120; s += `<g class="lb-worldmap-pt${seen.has(o.name) ? ' seen' : ''}" data-i="${i}"><circle class="d" cx="${x}" cy="${y}" r="2.4"/><text x="${left ? x - 3.5 : x + 3.5}" y="${y + 2}" text-anchor="${left ? 'end' : 'start'}">${esc((o.emoji ? o.emoji + ' ' : '') + o.name)}</text></g>`; });
        s += `<g class="fx"></g>`;
        if (mode === 'time') s += `<g class="mer"><rect class="mhit" y="0" width="24" height="${H}" fill="transparent"/><line class="ml" y1="0" y2="${H}" stroke="#1b1f3a" stroke-width="1.3"/><g class="mk"><circle r="7" fill="#ffc93c" stroke="#1b1f3a" stroke-width=".8"/><text y="2.2" text-anchor="middle" font-size="6.5">⇆</text></g></g><text class="sun" font-size="10" text-anchor="middle">☀️</text>`;
        svg.innerHTML = s;
        svg.style.touchAction = mode === 'time' ? 'none' : '';
        $('.lb-worldmap-stage').classList.toggle('lb-worldmap-plain', mode === 'find');
        if (mode === 'time') updTime();
      }
      function fx(ll, color) { const g = svg.querySelector('.fx'); if (!g) return; const c = document.createElementNS(NS, 'circle'); c.setAttribute('cx', X(ll[0])); c.setAttribute('cy', Y(ll[1])); c.setAttribute('class', 'lb-worldmap-ring'); c.setAttribute('stroke', color || '#ffc93c'); g.appendChild(c); timers.push(setTimeout(() => c.remove(), 1700)); }
      function whatAt(ev) {
        const ll = toLL(ev), tolDeg = 9 / pxPerUnit();
        const pi = points.findIndex(o => Math.hypot(+o.lon - ll[0], +o.lat - ll[1]) < tolDeg);
        if (pi >= 0 && mode !== 'find') return { kind: 'point', name: points[pi].name, o: points[pi], ll };
        const ln = SPECIAL.find(l => (l.lat != null && Math.abs(ll[1] - l.lat) < 2 / pxPerUnit()) || (l.lon != null && Math.abs(Math.abs(ll[0]) - l.lon) < 2 / pxPerUnit()));
        const c = contAt(ll);
        if (ln && mode === 'explore') return { kind: 'line', name: ln.name, o: ln, ll };
        if (c) return { kind: 'cont', name: c, o: CONT[c], ll };
        const oc = oceanAt(ll); return { kind: 'ocean', name: oc, o: OCEANS[oc], ll };
      }
      function explore(ev) {
        const t = whatAt(ev); api.sfx('tap'); fx(t.ll);
        const o = t.o, emoji = t.kind === 'line' ? '📏' : (o.emoji || o.e || '📍');
        info.innerHTML = `<b>${emoji} ${esc(t.name)}</b> <span class="m">${fmtLat(Math.round(t.ll[1]))}, ${fmtLon(Math.round(t.ll[0]))}</span><br>${esc(o.info || '')}${t.kind === 'cont' ? ' <span class="m">(continent)</span>' : ''}`;
        api.speak(t.name + '. ' + (o.info || ''));
        seen.add(t.name);
        svg.querySelectorAll('.lb-worldmap-land').forEach(e => e.classList.toggle('sel', seen.has(e.parentNode.dataset.c)));
        if (t.kind === 'point') { const g = svg.querySelector(`.lb-worldmap-pt[data-i="${points.indexOf(o)}"]`); g && g.classList.add('seen'); }
        score.textContent = `⭐ ${Math.min(seen.size, goal)} / ${goal}`;
        if (!won && seen.size >= goal) { won = true; msg.textContent = 'Super explorer! 🎉'; api.win(`You explored ${goal} parts of the world map!`); }
        else if (!won) msg.textContent = `Tap ${goal - seen.size} more`;
      }
      function nextAsk() {
        busy = false; tries = 0; if (!askQ.length) { msg.textContent = 'Nothing to find.'; return; }
        const n = askQ[askI % askQ.length], pt = points.find(o => o.name === n), e = pt ? pt.emoji : (CONT[n] || OCEANS[n] || {}).e;
        msg.innerHTML = `Tap <span style="color:#8b5cf6">${esc((e ? e + ' ' : '') + n)}</span>`;
        score.textContent = `✅ ${correct} / ${rounds}`;
      }
      function find(ev) {
        if (busy) return;
        const n = askQ[askI % askQ.length], ll = toLL(ev), pt = points.find(o => o.name === n);
        let ok, where;
        if (pt) { const d = km(ll, [+pt.lon, +pt.lat]); ok = d <= radius; where = `${Math.round(d / 100) * 100} km away`; }
        else { const t = whatAt(ev); ok = t.name === n; where = `that is ${t.name}`; }
        tries++; fx(ll, ok ? '#2ed3a5' : '#ff6b6b');
        if (ok) {
          correct++; api.sfx('correct'); score.textContent = `✅ ${correct} / ${rounds}`;
          const o = pt || CONT[n] || OCEANS[n]; info.innerHTML = `<b>✅ ${esc(n)}</b><br>${esc(o.info || '')}`;
          if (correct >= rounds) { if (!won) { won = true; api.win(`You found ${rounds} on the world map!`); } msg.textContent = 'All found! 🎉'; act.textContent = 'Play again'; act.style.display = ''; busy = true; return; }
          askI++; busy = true; msg.textContent = 'Correct!'; timers.push(setTimeout(nextAsk, 1000));
        } else {
          api.sfx('wrong');
          if (tries >= 3) { const at = pt ? [+pt.lon, +pt.lat] : (CONT[n] ? CONT[n].polys[0][0] : OCEANS[n].at[0]); if (CONT[n]) { const g = svg.querySelector(`[data-c="${n}"]`); g && g.querySelectorAll('path').forEach(e => e.style.fill = CONT[n].c); } fx(at, '#ffc93c'); msg.textContent = `Here it is! Next one…`; askI++; busy = true; timers.push(setTimeout(() => { draw(); nextAsk(); }, 2000)); }
          else msg.textContent = `Oops, ${where}. Try again!`;
        }
      }
      function updTime() {
        const x = X(mer), ml = svg.querySelector('.ml'); if (!ml) return;
        ml.setAttribute('x1', x); ml.setAttribute('x2', x); svg.querySelector('.mhit').setAttribute('x', x - 12); svg.querySelector('.mk').setAttribute('transform', `translate(${x},${H / 2})`);
        const sunLon = (((12 - gmt) * 15 + 540) % 360) - 180, sun = svg.querySelector('.sun'); sun.setAttribute('x', X(sunLon)); sun.setAttribute('y', 11);
        /* night = longitudes more than 90° from the Sun's meridian */
        const night = svg.querySelector('.night'); let n = '';
        [sunLon + 90].forEach(a => { for (const off of [0, 360, -360]) { const x0 = X(a + off), x1 = x0 + 180; if (x1 > 0 && x0 < W) n += `<rect x="${Math.max(0, x0)}" width="${Math.min(W, x1) - Math.max(0, x0)}" y="0" height="${H}" fill="#1b1f3a" opacity=".22"/>`; } });
        night.innerHTML = n;
        const dMin = mer * 4, local = gmt + mer / 15, hDiff = (mer - home.lon) * 4;
        const dayPart = Math.abs(((mer - sunLon + 540) % 360) - 180) <= 90 ? '☀️ Day' : '🌙 Night';
        info.innerHTML = `<b>Longitude ${fmtLon(mer)}</b> <span class="m">· ${nf(mer)}° × 4 min = ${Math.abs(Math.round(dMin))} min</span>
<div class="lb-worldmap-big"><div>${fmtDiff(dMin)}<small>vs Greenwich</small></div><div>${clock(local)}<small>local sun time · ${dayPart}</small></div><div>${fmtDiff(hDiff)}<small>vs ${esc(home.name)}</small></div></div>`;
        gOut.textContent = clock(gmt);
        if (!won && !dragging && Math.abs(mer - tLon) <= tTol) { won = true; api.sfx('correct'); fx([mer, 0], '#2ed3a5'); msg.textContent = 'Exactly right! 🎉'; api.win(`At ${fmtLon(mer)} the time is ${fmtDiff(dMin)} from Greenwich — 15° = 1 hour!`); }
        else if (!won && !dragging) msg.textContent = `Drag the line ⇆ ${mer < tLon ? 'east ➡️' : 'west ⬅️'}`;
      }
      function setMode(m) {
        mode = m; won = false; api.resetWin && api.resetWin(); seen = new Set(); correct = 0; askI = 0; busy = false; score.textContent = ''; act.style.display = 'none'; info.innerHTML = '';
        host.querySelectorAll('.lb-worldmap-tabs button').forEach(b => b.classList.toggle('on', b.dataset.m === m));
        $('.lb-worldmap-ch').textContent = '🎯 Challenge: ' + challengeText();
        ctl.style.display = m === 'time' ? '' : 'none';
        draw();
        if (m === 'explore') { msg.textContent = 'Tap land, sea, a dot or a line 👆'; score.textContent = `⭐ 0 / ${goal}`; info.innerHTML = '<span class="m">Tap anywhere on the map to learn what is there.</span>'; }
        else if (m === 'find') { askQ = askNames.slice().sort(() => Math.random() - .5); info.innerHTML = '<span class="m">Colours are hidden — use what you know!</span>'; nextAsk(); }
        else { mer = 0; updTime(); }
      }
      function onDown(ev) {
        if (mode === 'time') { dragging = true; svg.setPointerCapture && svg.setPointerCapture(ev.pointerId); onMove(ev); return; }
        if (mode === 'explore') explore(ev); else find(ev);
      }
      function onMove(ev) { if (!dragging) return; mer = Math.round(toLL(ev)[0] * 2) / 2; updTime(); }
      function onUp() { if (!dragging) return; dragging = false; updTime(); }
      svg.addEventListener('pointerdown', onDown); svg.addEventListener('pointermove', onMove); svg.addEventListener('pointerup', onUp); svg.addEventListener('pointercancel', onUp);
      gIn.addEventListener('input', () => { gmt = +gIn.value; updTime(); });
      host.querySelectorAll('.lb-worldmap-tabs button').forEach(b => b.addEventListener('click', () => { api.sfx('tap'); setMode(b.dataset.m); }));
      act.addEventListener('click', () => { api.sfx('tap'); setMode(mode); });
      setMode(mode);
      return () => { timers.forEach(clearTimeout); };
    },
    example: {
      title: 'Continents and oceans', mode: 'explore', modes: ['explore', 'find', 'time'],
      challenge: 'Tap 5 different continents, oceans or lines to learn about them', goal: 5, grid: 30, rounds: 5,
      points: [{ name: 'New Delhi', lat: 28.6, lon: 77.2, emoji: '🇮🇳', info: 'Capital of India.' },
        { name: 'London', lat: 51.5, lon: -0.1, emoji: '🇬🇧', info: 'Greenwich, home of the Prime Meridian, is in London.' },
        { name: 'Tokyo', lat: 35.7, lon: 139.7, emoji: '🇯🇵', info: 'Capital of Japan — 9 hours ahead of Greenwich.' },
        { name: 'New York', lat: 40.7, lon: -74.0, emoji: '🗽', info: 'Big city in the USA — 5 hours behind Greenwich (in winter).' },
        { name: 'Cairo', lat: 30.0, lon: 31.2, emoji: '🐫', info: 'Capital of Egypt, on the river Nile.' },
        { name: 'Sydney', lat: -33.9, lon: 151.2, emoji: '🦘', info: 'Biggest city of Australia.' },
        { name: 'Rio de Janeiro', lat: -22.9, lon: -43.2, emoji: '⚽', info: 'City in Brazil, near the Tropic of Capricorn.' }],
      gmt: 12, home: { name: 'India', lon: 82.5 }, target: { offset: 5.5, tol: 2 }
    },
    examples: [
      { title: 'Longitude and time (Class 6)', mode: 'time', modes: ['time', 'explore'], gmt: 12,
        challenge: 'India\'s clocks are 5 h 30 min ahead of Greenwich. Drag the time line to India\'s Standard Meridian (82.5° E)',
        target: { offset: 5.5, tol: 1.5 }, home: { name: 'India', lon: 82.5 }, grid: 15,
        points: [{ name: 'India', lat: 22, lon: 82.5, emoji: '🇮🇳', info: 'IST = GMT + 5:30 (82.5° ÷ 15°).' },
          { name: 'Japan', lat: 36, lon: 138, emoji: '🗾', info: 'Japan uses 135° E → GMT + 9 h.' },
          { name: 'Brazil', lat: -10, lon: -52, emoji: '🇧🇷', info: 'Brasília time is GMT − 3 h (45° W).' }] },
      { title: 'Find continents and oceans (Class 3-5)', mode: 'find', modes: ['find', 'explore'], rounds: 4, grid: 0,
        challenge: 'Find 4 continents and oceans — colours are hidden!',
        ask: ['Asia', 'Africa', 'Australia', 'Antarctica', 'South America', 'Pacific Ocean', 'Indian Ocean', 'Atlantic Ocean'], points: [] }
    ]
  });
})();
