/* Knowtopia Concept Lab: foodchain — "Food chain builder" (food chains, food webs, energy pyramid, 10% law)
 *
 * PARAMS (all optional)
 *  mode       string  'chain' (tap organisms in order to build a chain; energy pyramid grows) |
 *                     'web' (whole food web with arrows; tap an organism to remove it and see effects) default 'chain'
 *  habitat    string  built-in habitat: 'grassland' | 'pond' | 'forest' | 'ocean' | 'desert'          default 'grassland'
 *  habitats   array   habitats offered as tabs, e.g. ['grassland','pond']                              default [habitat]
 *  organisms  array   custom organisms (replaces habitats): [{id, name, emoji, eats:[ids]}]; producers
 *                     have eats:[]                                                                    default — (built-in data)
 *  energy     number  energy captured by the producer level, used by the 10% law                      default 10000
 *  unit       string  energy unit label                                                               default 'J'
 *  pyramid    bool    chain mode: show the energy pyramid                                             default true
 *  goal       object  chain mode: {length:n} chain with at least n organisms | {end:id} chain ending at
 *                     that organism | {topEnergy:x} top organism receives exactly x (unit)
 *                     web mode: {target:id, dir:'up'|'down'|'starve'} remove one organism so that the
 *                     target goes up / down / starves | {most:true} remove the organism that affects the most
 *                                                                                                     default chain {length:4}, web {most:true}
 *  challenge  string  challenge sentence (any language); a default is generated
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[<>&"]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]));
  const num = (v, d) => (v === null || v === undefined || v === '' || !Number.isFinite(+v)) ? d : +v;
  const O = (id, name, emoji, eats) => ({ id, name, emoji, eats });
  const HAB = {
    grassland: { name: 'Grassland', icon: '🌾', org: [O('grass', 'Grass', '🌾', []), O('grasshopper', 'Grasshopper', '🦗', ['grass']), O('rabbit', 'Rabbit', '🐇', ['grass']), O('mouse', 'Mouse', '🐁', ['grass']), O('frog', 'Frog', '🐸', ['grasshopper']), O('snake', 'Snake', '🐍', ['frog', 'mouse']), O('hawk', 'Hawk', '🦅', ['snake', 'rabbit', 'mouse'])] },
    pond: { name: 'Pond', icon: '🪷', org: [O('algae', 'Algae', '🌿', []), O('waterflea', 'Water flea', '🦐', ['algae']), O('snail', 'Snail', '🐌', ['algae']), O('smallfish', 'Small fish', '🐟', ['waterflea']), O('bigfish', 'Big fish', '🐠', ['smallfish']), O('duck', 'Duck', '🦆', ['snail', 'algae']), O('kingfisher', 'Kingfisher', '🐦', ['smallfish', 'bigfish'])] },
    forest: { name: 'Forest', icon: '🌳', org: [O('tree', 'Trees', '🌳', []), O('caterpillar', 'Caterpillar', '🐛', ['tree']), O('deer', 'Deer', '🦌', ['tree']), O('monkey', 'Monkey', '🐒', ['tree']), O('bird', 'Small bird', '🐦', ['caterpillar']), O('snake', 'Snake', '🐍', ['bird']), O('tiger', 'Tiger', '🐅', ['deer', 'monkey']), O('eagle', 'Eagle', '🦅', ['snake', 'bird'])] },
    ocean: { name: 'Ocean', icon: '🌊', org: [O('phyto', 'Phytoplankton', '🌱', []), O('zoo', 'Zooplankton', '🦐', ['phyto']), O('smallfish', 'Small fish', '🐟', ['zoo']), O('squid', 'Squid', '🦑', ['smallfish']), O('seal', 'Seal', '🦭', ['smallfish', 'squid']), O('shark', 'Shark', '🦈', ['seal', 'squid']), O('whale', 'Blue whale', '🐋', ['zoo'])] },
    desert: { name: 'Desert', icon: '🌵', org: [O('plants', 'Desert plants', '🌵', []), O('locust', 'Locust', '🦗', ['plants']), O('rat', 'Desert rat', '🐀', ['plants']), O('lizard', 'Lizard', '🦎', ['locust']), O('snake', 'Snake', '🐍', ['rat', 'lizard']), O('fox', 'Fox', '🦊', ['rat', 'lizard']), O('hawk', 'Hawk', '🦅', ['snake', 'lizard'])] }
  };
  const LEVEL = ['Producer', 'Primary consumer', 'Secondary consumer', 'Tertiary consumer', 'Quaternary consumer', 'Level 6', 'Level 7'];
  const LCOL = ['#2ed3a5', '#ffc93c', '#ff9f68', '#ff6b6b', '#8b5cf6', '#3b82f6', '#6b7090'];
  const fmtE = (e, u) => (e >= 1 ? Math.round(e * 100) / 100 : +e.toPrecision(2)).toLocaleString('en-IN') + ' ' + u;

  const CSS = `
  .lb-foodchain{font-weight:700;color:#1b1f3a;user-select:none;-webkit-user-select:none}
  .lb-foodchain-ch{background:#f3efff;color:#4c2fb0;border-radius:14px;padding:8px 11px;font-size:13.5px;line-height:1.3;margin-bottom:7px}
  .lb-foodchain-tabs{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;margin-bottom:6px}
  .lb-foodchain-tabs::-webkit-scrollbar{display:none}
  .lb-foodchain-tab{flex:none;min-height:36px;border:2px solid #e3e6f6;background:#fff;border-radius:12px;padding:0 10px;font-family:inherit;font-weight:800;font-size:12.5px;cursor:pointer;color:#1b1f3a}
  .lb-foodchain-tab.on{background:#8b5cf6;border-color:#8b5cf6;color:#fff}
  .lb-foodchain-pal{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
  .lb-foodchain-org{min-height:48px;border:2px solid #e3e6f6;background:#fff;border-radius:14px;font-family:inherit;font-weight:800;font-size:11px;color:#1b1f3a;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:2px;line-height:1.05}
  .lb-foodchain-org span{font-size:21px;line-height:1.1}
  .lb-foodchain-org.used{opacity:.35}
  .lb-foodchain-org.shake{animation:lb-foodchain-sh .35s}
  @keyframes lb-foodchain-sh{25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
  .lb-foodchain svg{display:block;width:100%;height:auto}
  .lb-foodchain-row{display:flex;gap:6px;align-items:center;margin-top:5px}
  .lb-foodchain-msg{flex:1;font-size:12.5px;color:#6b7090;line-height:1.3;min-height:32px}
  .lb-foodchain-msg.bad{color:#c94545}.lb-foodchain-msg.good{color:#0f7a5c}
  .lb-foodchain-btn{min-height:40px;border:none;border-radius:12px;padding:0 12px;font-family:inherit;font-weight:800;font-size:13px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef}
  .lb-foodchain-btn:active{transform:translateY(2px);box-shadow:none}
  .lb-foodchain-node{cursor:pointer}
  .lb-foodchain-node circle{transition:fill .3s,stroke .3s}
  .lb-foodchain-in{animation:lb-foodchain-pop .35s ease}
  @keyframes lb-foodchain-pop{from{transform:scale(.3);opacity:0}to{transform:scale(1);opacity:1}}
  .lb-foodchain-flow{stroke-dasharray:5 6;animation:lb-foodchain-fl 1s linear infinite}
  @keyframes lb-foodchain-fl{to{stroke-dashoffset:-11}}`;

  Labs.register('foodchain', {
    title: 'Food chain builder',
    subjects: ['science', 'evs', 'biology'],
    render(host, p, api) {
      const mode = p.mode === 'web' ? 'web' : 'chain';
      const E0 = Math.max(1, num(p.energy, 10000)), unit = String(p.unit || 'J');
      let habs;
      if (Array.isArray(p.organisms) && p.organisms.length) {
        const org = p.organisms.filter(o => o && o.id).map(o => O(String(o.id), String(o.name || o.id), String(o.emoji || '🐾'), Array.isArray(o.eats) ? o.eats.map(String) : []));
        habs = [{ key: 'custom', name: p.habitatName || 'Habitat', icon: '🌍', org }];
      } else {
        const list = (Array.isArray(p.habitats) && p.habitats.length ? p.habitats : [p.habitat || 'grassland']).filter(h => HAB[h]);
        if (!list.length) list.push('grassland');
        habs = list.map(k => Object.assign({ key: k }, HAB[k]));
      }
      const start = Math.max(0, habs.findIndex(h => h.key === p.habitat));
      let hab = habs[start], byId = {}, timers = [];
      const later = (f, ms) => timers.push(setTimeout(f, ms));
      let won = false; const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(m); };
      const goal = (p.goal && typeof p.goal === 'object') ? p.goal : (mode === 'chain' ? { length: 4 } : { most: true });
      const nameOf = id => { for (const h of habs) for (const o of h.org) if (o.id === id) return o.name; return id; };

      let challenge = p.challenge;
      if (!challenge) {
        if (mode === 'chain') {
          if (goal.end) challenge = `Build a food chain from a producer that ends with the ${nameOf(goal.end).toLowerCase()}.`;
          else if (goal.topEnergy != null) challenge = `Build a chain where the top animal gets only ${fmtE(+goal.topEnergy, unit)} (10% law).`;
          else challenge = `Build a food chain with ${goal.length || 4} living things. Start with a producer!`;
        } else if (goal.target) challenge = `Remove one living thing so that the ${nameOf(goal.target).toLowerCase()} ${goal.dir === 'up' ? 'increase' : goal.dir === 'starve' ? 'starve' : 'decrease'}.`;
        else challenge = 'Remove the one living thing whose loss would harm the most others.';
      }
      const tabs = habs.length > 1 ? `<div class="lb-foodchain-tabs">${habs.map((h, i) => `<button class="lb-foodchain-tab" data-h="${i}">${h.icon} ${esc(h.name)}</button>`).join('')}</div>` : '';
      host.innerHTML = `<style>${CSS}</style><div class="lb-foodchain"><div class="lb-foodchain-ch">🎯 Challenge: ${esc(challenge)}</div>${tabs}<div class="lb-foodchain-main"></div></div>`;
      const root = host.querySelector('.lb-foodchain'), main = root.querySelector('.lb-foodchain-main');
      root.querySelectorAll('[data-h]').forEach(b => b.onclick = () => { hab = habs[+b.dataset.h]; api.sfx('tap'); build(); });

      function levels(org) { // trophic level = 1 + max(level of foods)
        const L = {}; const get = (o, seen) => {
          if (L[o.id]) return L[o.id]; if (seen.has(o.id)) return 2; seen.add(o.id);
          const foods = o.eats.map(id => byId[id]).filter(Boolean);
          return (L[o.id] = foods.length ? 1 + Math.max(...foods.map(f => get(f, seen))) : 1);
        };
        org.forEach(o => get(o, new Set())); return L;
      }

      function build() {
        root.querySelectorAll('[data-h]').forEach(b => b.classList.toggle('on', habs[+b.dataset.h] === hab));
        byId = {}; hab.org.forEach(o => byId[o.id] = o);
        if (mode === 'chain') buildChain(); else buildWeb();
      }

      // ------------------------------------------------------------------ CHAIN MODE
      function buildChain() {
        const order = hab.org.slice().sort((a, b) => (a.name.length * 7 + a.id.charCodeAt(0)) % 11 - (b.name.length * 7 + b.id.charCodeAt(0)) % 11);
        const showPyr = p.pyramid !== false;
        main.innerHTML = `<div class="lb-foodchain-pal">${order.map(o => `<button class="lb-foodchain-org" data-o="${esc(o.id)}"><span>${o.emoji}</span>${esc(o.name)}</button>`).join('')}</div>
          <svg class="lb-foodchain-track" viewBox="0 0 352 84"></svg>
          <div class="lb-foodchain-row"><div class="lb-foodchain-msg"></div><button class="lb-foodchain-btn lb-foodchain-undo">↶ Undo</button><button class="lb-foodchain-btn lb-foodchain-clear">✕</button></div>
          ${showPyr ? '<svg class="lb-foodchain-pyr" viewBox="0 0 352 118"></svg>' : ''}`;
        const track = main.querySelector('.lb-foodchain-track'), pyr = main.querySelector('.lb-foodchain-pyr'), msg = main.querySelector('.lb-foodchain-msg');
        let chain = [];
        const setMsg = (t, c) => { msg.innerHTML = t; msg.className = 'lb-foodchain-msg' + (c ? ' ' + c : ''); };
        function draw(justAdded) {
          main.querySelectorAll('[data-o]').forEach(b => b.classList.toggle('used', chain.includes(b.dataset.o)));
          const n = chain.length, slots = Math.max(5, n), gap = 352 / slots, r = Math.min(22, gap / 2 - 9);
          let s = `<defs><marker id="lbfc-ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#ff6b6b"/></marker></defs>`;
          if (!n) s += `<text x="176" y="40" text-anchor="middle" font-size="12.5" font-weight="800" fill="#9aa0c0">Tap a producer (plant) to start your chain</text>`;
          for (let i = 0; i < n; i++) {
            const x = gap * (i + .5), o = byId[chain[i]];
            if (i > 0) { const x0 = gap * (i - .5); s += `<line class="lb-foodchain-flow" x1="${x0 + r + 3}" y1="32" x2="${x - r - 4}" y2="32" stroke="#ff6b6b" stroke-width="3" marker-end="url(#lbfc-ah)"/>`; }
            s += `<g class="${i === n - 1 && justAdded ? 'lb-foodchain-in' : ''}" style="transform-origin:${x}px 32px"><circle cx="${x}" cy="32" r="${r}" fill="#fff" stroke="${LCOL[i] || '#6b7090'}" stroke-width="3.5"/>
              <text x="${x}" y="${32 + r * .38}" text-anchor="middle" font-size="${r * 1.05}">${o.emoji}</text>
              <text x="${x}" y="${32 + r + 13}" text-anchor="middle" font-size="10" font-weight="800" fill="#1b1f3a">${esc(o.name.length > 12 ? o.name.slice(0, 11) + '…' : o.name)}</text>
              <text x="${x}" y="${32 + r + 24}" text-anchor="middle" font-size="8.5" font-weight="800" fill="#9aa0c0">${i === 0 ? 'producer' : i === 1 ? 'herbivore' : 'carnivore'}</text></g>`;
          }
          track.innerHTML = s;
          if (pyr) {
            let q = ''; const LV = Math.max(4, n), bh = 22, base = 112;
            for (let i = 0; i < LV; i++) {
              const w = 340 - i * (230 / (LV - 1)), x = 176 - w / 2, y = base - (i + 1) * (bh + 1.5), on = i < n;
              const nx = 176 - (340 - (i + 1) * (230 / (LV - 1))) / 2;
              q += `<path d="M${x} ${y + bh} L${x + w} ${y + bh} L${352 - nx} ${y} L${nx} ${y} Z" fill="${on ? LCOL[i] || '#6b7090' : '#f1f2f8'}" opacity="${on ? 1 : .9}"/>`;
              const e = E0 * Math.pow(0.1, i);
              const long = `${on ? byId[chain[i]].emoji + ' ' : ''}${LEVEL[i]} · ${fmtE(e, unit)}`, short = `${on ? byId[chain[i]].emoji + ' ' : ''}${fmtE(e, unit)}`;
              const txt = long.length * 6 < (352 - 2 * nx) - 14 ? long : short;
              q += `<text x="176" y="${y + 15.5}" text-anchor="middle" font-size="11" font-weight="800" fill="${on ? '#1b1f3a' : '#b7bbd3'}">${esc(on ? txt : (i === 0 ? LEVEL[0] + ' · ' + fmtE(e, unit) : '?'))}</text>`;
            }
            q += `<text x="2" y="10" font-size="9.5" font-weight="800" fill="#6b7090">⚡ Energy pyramid — only about 10% passes to the next level</text>`;
            pyr.innerHTML = q;
          }
        }
        function check() {
          const n = chain.length; if (!n) return;
          const top = byId[chain[n - 1]], eaters = hab.org.filter(o => o.eats.includes(top.id) && !chain.includes(o.id));
          let ok = false;
          if (goal.end) ok = top.id === goal.end;
          else if (goal.topEnergy != null) ok = Math.abs(E0 * Math.pow(0.1, n - 1) - +goal.topEnergy) < 1e-9 * Math.max(1, +goal.topEnergy);
          else ok = n >= (goal.length || 4);
          if (ok) { setMsg(`✓ ${n} links! The ${esc(top.name.toLowerCase())} gets only ${fmtE(E0 * Math.pow(.1, n - 1), unit)}.`, 'good'); later(() => winOnce(`Great food chain: ${chain.map(id => byId[id].name).join(' → ')}. Energy shrinks 10× at each step!`), 400); }
          else if (!eaters.length) setMsg(`Nothing here eats the ${esc(top.name.toLowerCase())} — it is the <b>top consumer</b>. ${goal.end || goal.length > n ? 'Undo and try another path!' : ''}`);
          else setMsg(`Who eats the <b>${esc(top.name.toLowerCase())}</b>? Tap it next.`);
        }
        main.querySelectorAll('[data-o]').forEach(b => b.onclick = () => {
          const o = byId[b.dataset.o]; if (chain.includes(o.id)) return;
          const shake = t => { api.sfx('wrong'); setMsg(t, 'bad'); b.classList.remove('shake'); void b.offsetWidth; b.classList.add('shake'); };
          if (!chain.length) { if (o.eats.length) return shake(`A food chain starts with a <b>producer</b> — a plant that makes its own food. The ${esc(o.name.toLowerCase())} eats others.`); }
          else { const last = byId[chain[chain.length - 1]]; if (!o.eats.includes(last.id)) return shake(`The ${esc(o.name.toLowerCase())} does not eat the ${esc(last.name.toLowerCase())}. Try again!`); }
          chain.push(o.id); api.sfx('coin'); draw(true); check();
        });
        main.querySelector('.lb-foodchain-undo').onclick = () => { chain.pop(); api.sfx('tap'); draw(); chain.length ? check() : setMsg('Arrows show the direction energy flows: food → eater.'); };
        main.querySelector('.lb-foodchain-clear').onclick = () => { chain = []; api.sfx('tap'); draw(); setMsg('Arrows show the direction energy flows: food → eater.'); };
        draw(); setMsg('Arrows show the direction energy flows: food → eater.');
      }

      // ------------------------------------------------------------------ WEB MODE
      function buildWeb() {
        const org = hab.org, L = levels(org), Lmax = Math.max(...Object.values(L));
        const H = 76 + (Lmax - 1) * 62, pos = {};
        const bary = o => { const f = o.eats.filter(id => pos[id]); return f.length ? f.reduce((a, id) => a + pos[id].x, 0) / f.length : 176; };
        for (let l = 1; l <= Lmax; l++) {
          const row = org.filter(o => L[o.id] === l), y = H - 38 - (l - 1) * 62;
          if (l === 1 || row.length >= 4) {
            if (l > 1) row.sort((a, b) => bary(a) - bary(b));
            row.forEach((o, i) => pos[o.id] = { x: 352 * (i + .5) / row.length, y });
          } else { // place near the average x of its foods, keeping nodes apart
            const below = org.filter(o => L[o.id] === l - 1).map(o => pos[o.id].x);
            const xs = row.map(o => ({ o, x: bary(o) }));
            xs.forEach(e => { if (below.some(bx => Math.abs(bx - e.x) < 30)) e.x += (e.x >= 176 ? -1 : 1) * 46; });
            xs.sort((a, b) => a.x - b.x);
            const m0 = xs.reduce((a, e) => a + e.x, 0) / xs.length;
            for (let i = 1; i < xs.length; i++) xs[i].x = Math.max(xs[i].x, xs[i - 1].x + 92);
            const m1 = xs.reduce((a, e) => a + e.x, 0) / xs.length; xs.forEach(e => e.x -= (m1 - m0));
            if (xs[0].x < 30) { const u = 30 - xs[0].x; xs.forEach(e => e.x += u); }
            const over = xs[xs.length - 1].x - 322; if (over > 0) xs.forEach(e => e.x -= over);
            const clash = d => xs.some(e => below.some(bx => Math.abs(bx - (e.x + d)) < 30) || e.x + d < 28 || e.x + d > 324);
            if (clash(0)) { const d = [46, -46, 92, -92, 23, -23].find(v => !clash(v)); if (d) xs.forEach(e => e.x += d); }
            xs.forEach(e => pos[e.o.id] = { x: Math.min(322, Math.max(30, e.x)), y });
          }
        }
        main.innerHTML = `<svg class="lb-foodchain-web" viewBox="0 0 352 ${H}"></svg>
          <div class="lb-foodchain-row"><div class="lb-foodchain-msg"></div><button class="lb-foodchain-btn lb-foodchain-reset">↺ Reset</button></div>`;
        const svg = main.querySelector('svg'), msg = main.querySelector('.lb-foodchain-msg');
        const setMsg = (t, c) => { msg.innerHTML = t; msg.className = 'lb-foodchain-msg' + (c ? ' ' + c : ''); };
        let removed = null;
        function effects(xid) {
          const fx = {}; if (!xid) return fx;
          const gone = new Set([xid]); let changed = true;
          while (changed) { changed = false; for (const o of org) if (!gone.has(o.id) && o.eats.length && o.eats.every(id => gone.has(id))) { gone.add(o.id); fx[o.id] = 'starve'; changed = true; } }
          for (const o of org) {
            if (o.id === xid || fx[o.id]) continue;
            if (o.eats.some(id => gone.has(id))) fx[o.id] = 'down';
            else if (byId[xid].eats.includes(o.id)) fx[o.id] = 'up';
          }
          return fx;
        }
        function draw() {
          const fx = effects(removed), R = 21;
          let s = `<defs><marker id="lbfc-aw" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#8b93b8"/></marker>
            <marker id="lbfc-ax" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#e3e6f6"/></marker></defs>`;
          for (const o of org) for (const f of o.eats) {
            if (!pos[f]) continue; const a = pos[f], b = pos[o.id], dx = b.x - a.x, dy = b.y - a.y, d = Math.hypot(dx, dy) || 1;
            const dead = removed && (f === removed || o.id === removed);
            const span = Math.abs(L[o.id] - L[f]);
            let cx = (a.x + b.x) / 2, cy = (a.y + b.y) / 2;
            if (span >= 2) { // curve long links around the nodes in between
              const sg = cx >= 176 ? 1 : -1, nx = -dy / d, ny = dx / d, k = (nx * sg >= 0 ? 1 : -1) * 28 * span;
              cx += nx * k; cy += ny * k;
            }
            const sx = cx - a.x, sy = cy - a.y, sd = Math.hypot(sx, sy) || 1, ex = b.x - cx, ey = b.y - cy, ed = Math.hypot(ex, ey) || 1;
            s += `<path d="M${a.x + sx / sd * (R + 2)} ${a.y + sy / sd * (R + 2)} Q${cx} ${cy} ${b.x - ex / ed * (R + 5)} ${b.y - ey / ed * (R + 5)}" fill="none" stroke="${dead ? '#e3e6f6' : '#8b93b8'}" stroke-width="2" marker-end="url(#${dead ? 'lbfc-ax' : 'lbfc-aw'})"/>`;
          }
          for (const o of org) {
            const { x, y } = pos[o.id], gone = o.id === removed, e = fx[o.id];
            const ring = gone ? '#c9cde3' : e === 'up' ? '#2ed3a5' : e === 'down' ? '#ffb020' : e === 'starve' ? '#ff6b6b' : LCOL[L[o.id] - 1];
            s += `<g class="lb-foodchain-node" data-o="${esc(o.id)}" opacity="${gone ? .45 : 1}"><circle cx="${x}" cy="${y}" r="${R + 4}" fill="transparent"/><circle cx="${x}" cy="${y}" r="${R}" fill="${e === 'starve' ? '#ffe9e9' : '#fff'}" stroke="${ring}" stroke-width="${e ? 4.5 : 3}"/>
              <text x="${x}" y="${y + 7.5}" text-anchor="middle" font-size="21">${o.emoji}</text>
              <text x="${x}" y="${y + R + 11}" text-anchor="middle" font-size="9.5" font-weight="800" fill="#1b1f3a" stroke="#fff" stroke-width="3" paint-order="stroke">${esc(o.name)}</text>
              ${gone ? `<path d="M${x - 13} ${y - 13}L${x + 13} ${y + 13}M${x + 13} ${y - 13}L${x - 13} ${y + 13}" stroke="#ff6b6b" stroke-width="4" stroke-linecap="round"/>` : ''}
              ${e ? `<g><circle cx="${x + 17}" cy="${y - 16}" r="9.5" fill="${ring}"/><text x="${x + 17}" y="${y - 12}" text-anchor="middle" font-size="12" font-weight="900" fill="#fff">${e === 'up' ? '↑' : e === 'down' ? '↓' : '✕'}</text></g>` : ''}</g>`;
          }
          svg.innerHTML = s;
          svg.querySelectorAll('[data-o]').forEach(g => g.addEventListener('click', () => tap(g.dataset.o)));
          return fx;
        }
        function tap(id) {
          removed = removed === id ? null : id; api.sfx('tap');
          const fx = draw(); if (!removed) { setMsg('Tap a living thing to remove it from the web.'); return; }
          const list = k => org.filter(o => fx[o.id] === k).map(o => esc(o.name.toLowerCase()));
          const up = list('up'), dn = list('down'), st = list('starve'); const parts = [];
          if (up.length) parts.push(`<b style="color:#0f7a5c">↑ ${up.join(', ')}</b> (fewer enemies)`);
          if (dn.length) parts.push(`<b style="color:#b97800">↓ ${dn.join(', ')}</b> (less food)`);
          if (st.length) parts.push(`<b style="color:#c94545">✕ ${st.join(', ')}</b> (no food left!)`);
          setMsg(`Without the ${esc(byId[id].name.toLowerCase())}: ${parts.join('; ') || 'little change'}.`);
          let ok = false;
          if (goal.target) ok = fx[goal.target] === (goal.dir || 'down') || (goal.dir === 'down' && fx[goal.target] === 'starve');
          else { const score = k => { const f = effects(k); return Object.keys(f).length + Object.values(f).filter(v => v === 'starve').length; }; const best = Math.max(...org.map(o => score(o.id))); ok = score(id) === best; }
          const nm = byId[id].name.toLowerCase();
          if (ok) later(() => winOnce(goal.target ? `Removing the ${nm} changed the ${nameOf(goal.target).toLowerCase()} — everything in a food web is linked!` : `Yes! Without the ${nm} the whole web suffers — producers support every food chain.`), 500);
          else api.sfx('hmm');
        }
        main.querySelector('.lb-foodchain-reset').onclick = () => { removed = null; draw(); api.sfx('tap'); setMsg('Tap a living thing to remove it from the web.'); };
        draw(); setMsg('Arrows point from food to eater. Tap a living thing to remove it.');
      }

      build();
      return () => { timers.forEach(clearTimeout); };
    },
    example: { mode: 'chain', habitat: 'grassland', habitats: ['grassland', 'pond', 'forest', 'ocean', 'desert'], energy: 10000, unit: 'J', pyramid: true },
    examples: [
      { mode: 'chain', habitat: 'pond', habitats: ['pond'], goal: { end: 'kingfisher' },
        challenge: 'Grade 6–7: Make a pond food chain that ends with the kingfisher.' },
      { mode: 'chain', habitat: 'forest', habitats: ['forest', 'grassland'], energy: 10000, goal: { topEnergy: 10 },
        challenge: 'Grade 10: Using the 10% law, build a chain where the top consumer gets just 10 J.' },
      { mode: 'web', habitat: 'grassland', habitats: ['grassland', 'desert'], goal: { target: 'grasshopper', dir: 'up' },
        challenge: 'Grade 7–10: Remove one animal so that the grasshoppers increase.' }
    ]
  });
})();
