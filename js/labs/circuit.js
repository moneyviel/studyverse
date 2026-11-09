/* Knowtopia Concept Lab: circuit — build an electric circuit by tapping parts into slots.
 *
 * The child picks a part from the tray (cell, bulb, switch, wire, resistor) and taps a dashed
 * slot to put it there. When the loop is closed the bulb glows and "current" dots flow. Bulb
 * brightness is worked out from real circuit maths (series / parallel, I = V/R, P = I²R), so two
 * bulbs in series really are dimmer and two in parallel stay bright.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *   mode       string  'build' | 'series' | 'parallel' | 'materials' | 'ohm'          default 'build'
 *                'build'/'series' = one loop with 6 slots; 'parallel' = a cell line + two branches;
 *                'materials' = ready circuit with a test gap; 'ohm' = cells + resistor + ammeter.
 *   goal       string  'light' | 'switch' | 'series' | 'parallel' | 'materials' | 'current'
 *                                                    default: 'switch' (build), 'series', 'parallel',
 *                                                    'materials', 'current' (ohm) by mode
 *   challenge  string  challenge text (any language); a default is made from goal
 *   winText    string  optional message shown on win
 *   parts      array   tray parts for build modes, from ['cell','bulb','switch','wire','resistor']
 *                                                    default ['cell','bulb','switch','wire']
 *   preset     object  starting slots, e.g. {"L":"cell","T1":"wire"}; values 'cell','bulb','switch',
 *                      'switch-on','wire','resistor','empty'. Slot ids: series L,T1,T2,R,B1,B2;
 *                      parallel L1,L2,A1,A2,B1,B2 (A = middle branch, B = right branch)
 *   locked     array   slot ids the child cannot change                               default []
 *   cellV      number  volts per cell                                                default 1.5
 *   bulbR      number  resistance of one bulb in ohms                                default 3
 *   resistorR  number  resistance of the tray resistor (Ω)                           default 6
 *   showOhm    boolean show V, R, I readout in build modes                           default false
 *   materials  array   [{name, conductor:true/false, color}] for 'materials' mode    default 8 everyday items
 *   cells      number  starting number of cells in 'ohm' mode (1–4)                  default 2
 *   resistors  array   resistor choices in ohms for 'ohm' mode                       default [1,2,3,4,5,6]
 *   target     number  target current in amperes for goal 'current'                  default 1.5
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmt = (v, d = 2) => (Math.round(v * Math.pow(10, d)) / Math.pow(10, d)).toString();
  const H = 28; // half length of a slot

  // slot geometry; rot = direction in which current flows through the slot
  const LAYOUTS = {
    series: {
      slots: [
        { id: 'L', x: 40, y: 120, rot: -90, lx: 74, ly: 124, la: 'start', br: 'm' },
        { id: 'T1', x: 135, y: 40, rot: 0, lx: 135, ly: 74, la: 'middle', br: 'm' },
        { id: 'T2', x: 225, y: 40, rot: 0, lx: 225, ly: 74, la: 'middle', br: 'm' },
        { id: 'R', x: 320, y: 120, rot: 90, lx: 286, ly: 124, la: 'end', br: 'm' },
        { id: 'B1', x: 225, y: 200, rot: 180, lx: 225, ly: 172, la: 'middle', br: 'm' },
        { id: 'B2', x: 135, y: 200, rot: 180, lx: 135, ly: 172, la: 'middle', br: 'm' }
      ],
      rails: [
        ['m', [[40, 92], [40, 40], [107, 40]]], ['m', [[163, 40], [197, 40]]], ['m', [[253, 40], [320, 40], [320, 92]]],
        ['m', [[320, 148], [320, 200], [253, 200]]], ['m', [[197, 200], [163, 200]]], ['m', [[107, 200], [40, 200], [40, 148]]]
      ],
      dots: []
    },
    parallel: {
      slots: [
        { id: 'L1', x: 40, y: 85, rot: -90, lx: 70, ly: 89, la: 'start', br: 'm' },
        { id: 'L2', x: 40, y: 155, rot: -90, lx: 70, ly: 159, la: 'start', br: 'm' },
        { id: 'A1', x: 180, y: 85, rot: 90, lx: 210, ly: 89, la: 'start', br: 'a' },
        { id: 'A2', x: 180, y: 155, rot: 90, lx: 210, ly: 159, la: 'start', br: 'a' },
        { id: 'B1', x: 320, y: 85, rot: 90, lx: 290, ly: 89, la: 'end', br: 'b' },
        { id: 'B2', x: 320, y: 155, rot: 90, lx: 290, ly: 159, la: 'end', br: 'b' }
      ],
      rails: [
        ['m', [[40, 57], [40, 26], [180, 26]]], ['m', [[40, 127], [40, 113]]], ['m', [[180, 214], [40, 214], [40, 183]]],
        ['a', [[180, 26], [180, 57]]], ['a', [[180, 113], [180, 127]]], ['a', [[180, 183], [180, 214]]],
        ['b', [[180, 26], [320, 26], [320, 57]]], ['b', [[320, 113], [320, 127]]], ['b', [[320, 183], [320, 214], [180, 214]]]
      ],
      dots: [[180, 26], [180, 214]]
    }
  };

  const MATS = [
    { name: 'Iron nail', conductor: true, color: '#8a94a6' },
    { name: 'Steel coin', conductor: true, color: '#c9ced8' },
    { name: 'Aluminium foil', conductor: true, color: '#dfe5ee' },
    { name: 'Pencil lead', conductor: true, color: '#4b4f5c' },
    { name: 'Plastic scale', conductor: false, color: '#7cc7ff' },
    { name: 'Rubber eraser', conductor: false, color: '#ff9fb2' },
    { name: 'Wooden stick', conductor: false, color: '#c98a4b' },
    { name: 'Glass bangle', conductor: false, color: '#a8f0e0' }
  ];
  const PART_INFO = {
    cell: { label: 'Cell', icon: '🔋' }, bulb: { label: 'Bulb', icon: '💡' }, switch: { label: 'Switch', icon: '🔘' },
    wire: { label: 'Wire', icon: '〰️' }, resistor: { label: 'Resistor', icon: '▥' }, remove: { label: 'Remove', icon: '✖' }
  };

  const CSS = `
.lb-circuit-w{font-size:14px;color:#1b1f3a;-webkit-user-select:none;user-select:none}
.lb-circuit-ch{font-weight:800;font-size:14px;margin-bottom:6px;line-height:1.25}
.lb-circuit-svg{width:100%;height:auto;display:block;background:linear-gradient(#f7f8ff,#eef1ff);border-radius:18px;touch-action:manipulation}
.lb-circuit-slot{cursor:pointer}
.lb-circuit-slot:hover .lb-circuit-hit{fill:rgba(139,92,246,.07)}
.lb-circuit-flow{fill:none;stroke:#ffc93c;stroke-width:3;stroke-linecap:round;stroke-dasharray:3 9;animation:lb-circuit-flow 1s linear infinite}
@keyframes lb-circuit-flow{to{stroke-dashoffset:-24}}
.lb-circuit-glow{transition:opacity .35s}
.lb-circuit-pulse{animation:lb-circuit-pulse 1.4s ease-in-out infinite}
@keyframes lb-circuit-pulse{50%{opacity:.45}}
.lb-circuit-msg{margin-top:6px;min-height:36px;background:#f6f4ff;border-radius:12px;padding:6px 10px;font-weight:800;font-size:13px;line-height:1.3;display:flex;align-items:center;gap:6px}
.lb-circuit-msg.ok{background:#e3fbf3;color:#0f7a5c}.lb-circuit-msg.bad{background:#ffecec;color:#c23b3b}
.lb-circuit-ohm{font-size:12.5px;font-weight:800;color:#3b82f6;margin-top:3px;text-align:center;min-height:16px}
.lb-circuit-row{display:flex;gap:5px;margin-top:6px;flex-wrap:wrap}
.lb-circuit-b{flex:1 1 0;min-width:0;min-height:44px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:12px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef;padding:2px 3px;line-height:1.1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px}
.lb-circuit-b span{font-size:17px;line-height:1}
.lb-circuit-b.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-circuit-b:active{transform:translateY(2px);box-shadow:0 1px 0 #d3d7ef}
.lb-circuit-b.mat{flex:1 1 22%;font-size:11.5px;min-height:42px;flex-direction:row;gap:4px}
.lb-circuit-b.mat i{width:12px;height:12px;border-radius:4px;flex:0 0 12px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.15)}
.lb-circuit-b.yes{background:#dff8ef;box-shadow:0 3px 0 #9fe4cb}.lb-circuit-b.no{background:#ffe6e6;box-shadow:0 3px 0 #f5b5b5}
.lb-circuit-b.cur{outline:3px solid #8b5cf6}
.lb-circuit-b.reset{flex:0 0 auto;padding:0 12px;flex-direction:row;font-size:13px;gap:5px}
.lb-circuit-step{display:flex;align-items:center;gap:6px;font-weight:800;font-size:13px}
.lb-circuit-step .lb-circuit-b{flex:0 0 44px;font-size:20px}
.lb-circuit-step b{min-width:22px;text-align:center;font-size:16px}
.lb-circuit-lab{font-size:11px;font-weight:800;color:#6b7090;text-transform:uppercase;letter-spacing:.3px}
`;

  Labs.register('circuit', {
    title: 'Circuit builder',
    subjects: ['science', 'physics'],
    render(host, p, api) {
      const ex = this.example || {};
      // keys copied from `example` by the loader are ignored when the topic asks for a different mode/goal
      const diffMode = p.mode !== undefined && p.mode !== ex.mode;
      p = Object.assign({}, p);
      if (diffMode) ['goal', 'parts', 'preset'].forEach(k => { if (p[k] === ex[k]) delete p[k]; });
      if (diffMode || p.goal !== ex.goal || p.target !== ex.target) ['challenge', 'winText'].forEach(k => { if (p[k] === ex[k]) delete p[k]; });
      const MODES = ['build', 'series', 'parallel', 'materials', 'ohm'];
      const mode = MODES.includes(p.mode) ? p.mode : 'build';
      const GOALDEF = { build: 'switch', series: 'series', parallel: 'parallel', materials: 'materials', ohm: 'current' };
      const GOALS = ['light', 'switch', 'series', 'parallel', 'materials', 'current'];
      const goal = GOALS.includes(p.goal) ? p.goal : GOALDEF[mode];
      const layoutName = mode === 'parallel' ? 'parallel' : 'series';
      const LAY = LAYOUTS[layoutName];
      const cellV = +p.cellV > 0 ? +p.cellV : 1.5;
      const bulbR = +p.bulbR > 0 ? +p.bulbR : 3;
      const resR = +p.resistorR > 0 ? +p.resistorR : 6;
      const mats = (Array.isArray(p.materials) && p.materials.length ? p.materials : MATS)
        .filter(m => m && m.name).map((m, i) => ({ name: String(m.name), conductor: !!m.conductor, color: m.color || MATS[i % MATS.length].color }));
      const resistors = (Array.isArray(p.resistors) && p.resistors.length ? p.resistors : [1, 2, 3, 4, 5, 6]).map(Number).filter(r => r > 0);
      const target = +p.target > 0 ? +p.target : 1.5;
      const showOhm = mode === 'ohm' || !!p.showOhm;
      let tray = (Array.isArray(p.parts) && p.parts.length ? p.parts : ['cell', 'bulb', 'switch', 'wire']).filter(k => PART_INFO[k] && k !== 'remove');
      if (mode === 'parallel') tray = tray.filter(k => k !== 'cell');
      tray.push('remove');

      // ---- presets ----
      const mk = v => {
        if (v && typeof v === 'object') return Object.assign({}, v);
        switch (v) {
          case 'cell': return { k: 'cell' }; case 'bulb': return { k: 'bulb' }; case 'switch': return { k: 'switch', on: false };
          case 'switch-on': return { k: 'switch', on: true }; case 'wire': return { k: 'wire' };
          case 'resistor': return { k: 'res', r: resR }; default: return { k: 'empty' };
        }
      };
      let cells = Math.min(4, Math.max(1, Math.round(+p.cells || 2)));
      let resIdx = 0;
      const startRes = () => { resIdx = 0; while (resIdx < resistors.length - 1 && Math.abs(cells * (+p.cellV > 0 ? +p.cellV : 1.5) / resistors[resIdx] - target) < 0.005) resIdx++; };
      startRes();
      function defaultPreset() {
        if (mode === 'materials') return { L: { k: 'cell' }, T1: { k: 'wire' }, T2: { k: 'bulb' }, R: { k: 'wire' }, B1: { k: 'mat', m: null }, B2: { k: 'wire' } };
        if (mode === 'ohm') return { L: { k: 'batt', n: cells }, T1: { k: 'wire' }, T2: { k: 'meter' }, R: { k: 'res', r: resistors[resIdx] }, B1: { k: 'wire' }, B2: { k: 'wire' } };
        if (mode === 'parallel') return { L1: { k: 'cell' }, L2: { k: 'wire' }, A1: { k: 'empty' }, A2: { k: 'wire' }, B1: { k: 'empty' }, B2: { k: 'wire' } };
        if (mode === 'series') return { L: { k: 'cell' }, T1: { k: 'empty' }, T2: { k: 'wire' }, R: { k: 'wire' }, B1: { k: 'empty' }, B2: { k: 'wire' } };
        return { L: { k: 'empty' }, T1: { k: 'wire' }, T2: { k: 'empty' }, R: { k: 'wire' }, B1: { k: 'empty' }, B2: { k: 'wire' } };
      }
      const fixedLocks = mode === 'materials' || mode === 'ohm' ? LAY.slots.map(s => s.id) : mode === 'parallel' ? ['L1'] : [];
      const locked = new Set(fixedLocks.concat(Array.isArray(p.locked) ? p.locked.map(String) : []));
      let S = {};
      function resetSlots() {
        const d = defaultPreset();
        S = {};
        LAY.slots.forEach(s => {
          const pv = (mode === 'materials' || mode === 'ohm') ? undefined : (p.preset && p.preset[s.id]);
          S[s.id] = pv !== undefined ? mk(pv) : d[s.id];
          if (mode === 'parallel' && s.br !== 'm' && S[s.id].k === 'cell') S[s.id] = { k: 'wire' };
        });
      }
      resetSlots();
      let tool = tray.includes('bulb') ? 'bulb' : tray[0];
      let curMat = null;
      const tested = {};
      let won = false, note = '', noteTimer = 0;

      // ---- electrical analysis ----
      const rOf = q => {
        switch (q.k) {
          case 'wire': case 'cell': case 'batt': case 'meter': return 0;
          case 'bulb': return bulbR; case 'res': return q.r;
          case 'switch': return q.on ? 0 : Infinity;
          case 'mat': return q.m == null ? Infinity : (mats[q.m].conductor ? 0 : Infinity);
          default: return Infinity;
        }
      };
      const emfOf = q => q.k === 'cell' ? cellV : q.k === 'batt' ? q.n * cellV : 0;
      function solve() {
        const ids = br => LAY.slots.filter(s => s.br === br).map(s => s.id);
        const sum = (arr, f) => arr.reduce((a, id) => a + f(S[id]), 0);
        const main = ids('m');
        const V = sum(main, emfOf);
        const Rm = sum(main, rOf);
        const res = { V, Rm, I: 0, Ib: { m: 0, a: 0, b: 0 }, state: 'ok', Rt: Infinity };
        let branches = [];
        if (layoutName === 'parallel') branches = ['a', 'b'].map(b => ({ b, R: sum(ids(b), rOf) }));
        const open = !isFinite(Rm) || (branches.length && branches.every(x => !isFinite(x.R)));
        if (V === 0) { res.state = open ? 'open-nocell' : 'nocell'; return res; }
        if (open) { res.state = 'open'; return res; }
        let Req = 0;
        if (branches.length) {
          const live = branches.filter(x => isFinite(x.R));
          Req = live.some(x => x.R === 0) ? 0 : 1 / live.reduce((a, x) => a + 1 / x.R, 0);
          res.Req = Req;
        }
        const Rt = Rm + Req; res.Rt = Rt;
        if (Rt === 0) { res.state = 'short'; return res; }
        const I = V / Rt; res.I = I; res.Ib.m = I;
        if (branches.length) {
          const Vp = I * Req, live = branches.filter(x => isFinite(x.R)), zero = live.filter(x => x.R === 0);
          live.forEach(x => { res.Ib[x.b] = zero.length ? (x.R === 0 ? I / zero.length : 0) : Vp / x.R; });
        }
        return res;
      }
      const slotI = (r, s) => r.Ib[s.br] || 0;
      const bright = I => { if (I <= 1e-9) return 0; const rel = Math.pow(I * bulbR / cellV, 2); return Math.min(1, 0.22 + 0.78 * Math.sqrt(rel)); };

      // ---- drawing ----
      const lead = (a, b) => `<line x1="${a}" y1="0" x2="${b}" y2="0" stroke="#1b1f3a" stroke-width="4" stroke-linecap="round"/>`;
      function partSVG(q, s, I) {
        let g = '', t = '';
        const flow = I > 1e-9 ? `<line class="lb-circuit-flow" x1="${-H}" y1="0" x2="${H}" y2="0" style="animation-duration:${Math.max(0.35, Math.min(2.4, 0.6 / I)).toFixed(2)}s"/>` : '';
        switch (q.k) {
          case 'wire': g = lead(-H, H) + flow; break;
          case 'cell': case 'batt':
            g = lead(-H, -18) + lead(20, H) +
              `<rect x="-19" y="-12" width="37" height="24" rx="6" fill="#1b1f3a"/><rect x="5" y="-12" width="13" height="24" fill="#ffc93c"/>` +
              `<rect x="18" y="-6" width="5" height="12" rx="2" fill="#9aa0c0"/><rect x="-19" y="-12" width="37" height="24" rx="6" fill="none" stroke="#1b1f3a" stroke-width="2"/>`;
            t = `<text x="-6" y="4.5" text-anchor="middle" font-size="13" font-weight="800" fill="#fff">${q.k === 'batt' ? q.n + '×' : '+'}</text>`;
            break;
          case 'bulb': {
            const b = bright(I);
            g = lead(-H, -12) + lead(12, H);
            t = `<circle class="lb-circuit-glow lb-circuit-pulse" r="27" fill="url(#lbcGlow)" opacity="${b}"/>` +
              `<circle r="13" fill="${b ? '#fff3b0' : '#ffffff'}" stroke="#1b1f3a" stroke-width="2.5"/>` +
              `<path d="M-6 3 L-3 -4 L0 3 L3 -4 L6 3" fill="none" stroke="${b ? '#ff9f1c' : '#9aa0c0'}" stroke-width="2" stroke-linejoin="round"/>`;
            break;
          }
          case 'switch': {
            const ang = q.on ? 0 : -32;
            g = lead(-H, -14) + lead(14, H) +
              `<line x1="-14" y1="0" x2="15" y2="0" stroke="${q.on ? '#2ed3a5' : '#ff6b6b'}" stroke-width="5" stroke-linecap="round" transform="rotate(${ang} -14 0)" style="transition:transform .2s"/>` +
              `<circle cx="-14" cy="0" r="5" fill="#1b1f3a"/><circle cx="14" cy="0" r="5" fill="#1b1f3a"/>` + (q.on ? flow : '');
            break;
          }
          case 'res':
            g = lead(-H, -18) + lead(18, H) + `<rect x="-19" y="-10" width="38" height="20" rx="5" fill="#f3efff"/>` +
              `<path d="M-18 0 L-15 -7 L-9 7 L-3 -7 L3 7 L9 -7 L15 7 L18 0" fill="none" stroke="#8b5cf6" stroke-width="3" stroke-linejoin="round"/>`;
            break;
          case 'meter':
            g = lead(-H, -15) + lead(15, H);
            t = `<circle r="15" fill="#fff" stroke="#3b82f6" stroke-width="3"/><text y="5" text-anchor="middle" font-size="14" font-weight="800" fill="#3b82f6">A</text>`;
            break;
          case 'mat':
            if (q.m == null) {
              g = lead(-H, -16) + lead(16, H) + `<circle cx="-16" r="4" fill="#1b1f3a"/><circle cx="16" r="4" fill="#1b1f3a"/>`;
              t = `<text y="-11" text-anchor="middle" font-size="16">❓</text>`;
            } else {
              const m = mats[q.m];
              g = lead(-H, -16) + lead(16, H) + `<rect x="-17" y="-9" width="34" height="18" rx="6" fill="${esc(m.color)}" stroke="#1b1f3a" stroke-width="2"/>` + (m.conductor ? flow : '');
            }
            break;
          default:
            t = `<rect x="-24" y="-17" width="48" height="34" rx="10" fill="rgba(139,92,246,.08)" stroke="#8b5cf6" stroke-width="2" stroke-dasharray="5 4"/>` +
              `<text y="6" text-anchor="middle" font-size="18" font-weight="800" fill="#8b5cf6">+</text>`;
        }
        return { g, t };
      }
      function labelOf(q, I) {
        switch (q.k) {
          case 'cell': return `${fmt(cellV)} V`;
          case 'batt': return `${fmt(q.n * cellV)} V`;
          case 'bulb': return showOhm ? `${fmt(bulbR)} Ω` : (I > 1e-9 ? 'ON' : 'off');
          case 'switch': return q.on ? 'ON' : 'OFF';
          case 'res': return `${fmt(q.r)} Ω`;
          case 'meter': return `${fmt(I)} A`;
          case 'mat': return q.m == null ? 'test gap' : mats[q.m].name;
          default: return '';
        }
      }
      function draw(r) {
        let out = `<defs><radialGradient id="lbcGlow"><stop offset="0" stop-color="#ffe066" stop-opacity="1"/><stop offset=".55" stop-color="#ffd23f" stop-opacity=".55"/><stop offset="1" stop-color="#ffc93c" stop-opacity="0"/></radialGradient></defs>`;
        LAY.rails.forEach(([br, pts]) => {
          const P = pts.map(q => q.join(',')).join(' ');
          const I = r.Ib[br] || 0;
          out += `<polyline points="${P}" fill="none" stroke="#1b1f3a" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>`;
          if (I > 1e-9) out += `<polyline class="lb-circuit-flow" points="${P}" style="animation-duration:${Math.max(0.35, Math.min(2.4, 0.6 / I)).toFixed(2)}s"/>`;
        });
        LAY.dots.forEach(d => { out += `<circle cx="${d[0]}" cy="${d[1]}" r="5" fill="#1b1f3a"/>`; });
        LAY.slots.forEach(s => {
          const q = S[s.id], I = slotI(r, s), ps = partSVG(q, s, I), lab = labelOf(q, I);
          const lk = locked.has(s.id) && q.k !== 'switch';
          out += `<g class="lb-circuit-slot" data-slot="${s.id}" transform="translate(${s.x} ${s.y})">` +
            `<rect class="lb-circuit-hit" x="-30" y="-30" width="60" height="60" rx="14" fill="transparent"/>` +
            `<g transform="rotate(${s.rot})">${ps.g}</g>${ps.t}</g>`;
          if (lab) out += `<text x="${s.lx}" y="${s.ly}" text-anchor="${s.la}" font-size="11.5" font-weight="800" fill="${q.k === 'switch' ? (q.on ? '#14a37f' : '#e04848') : '#6b7090'}">${esc(lab)}${lk && mode !== 'materials' && mode !== 'ohm' ? ' 🔒' : ''}</text>`;
        });
        if (r.state === 'short') out += `<text x="180" y="126" text-anchor="middle" font-size="22">🔥</text>`;
        svg.innerHTML = out;
      }

      // ---- UI ----
      const DEFCH = {
        light: 'Make the bulb glow!',
        switch: 'Build a circuit with a cell, a bulb and a switch — then switch it ON.',
        series: 'Light TWO bulbs in one loop (series). Are they as bright as one bulb?',
        parallel: 'Put a bulb in each branch (parallel) and light both.',
        materials: 'Put each material in the test gap. Which ones make the bulb glow?',
        current: `Make the ammeter read ${fmt(target)} A. Use I = V ÷ R.`
      };
      const chText = p.challenge ? String(p.challenge) : DEFCH[goal];
      host.innerHTML = `<style>${CSS}</style>
<div class="lb-circuit-w">
  <div class="lb-circuit-ch">🎯 Challenge: ${esc(chText)}</div>
  <svg class="lb-circuit-svg" viewBox="0 0 360 240" role="img" aria-label="circuit"></svg>
  <div class="lb-circuit-msg"></div>
  <div class="lb-circuit-ohm"></div>
  <div class="lb-circuit-ctl"></div>
</div>`;
      const svg = host.querySelector('svg'), msgEl = host.querySelector('.lb-circuit-msg'),
        ohmEl = host.querySelector('.lb-circuit-ohm'), ctl = host.querySelector('.lb-circuit-ctl');
      if (!showOhm) ohmEl.style.display = 'none';

      function buildControls() {
        if (mode === 'materials') {
          ctl.innerHTML = `<div class="lb-circuit-row">${mats.map((m, i) =>
            `<button class="lb-circuit-b mat ${tested[i] === undefined ? '' : (tested[i] ? 'yes' : 'no')} ${curMat === i ? 'cur' : ''}" data-mat="${i}"><i style="background:${esc(m.color)}"></i>${esc(m.name)}${tested[i] === undefined ? '' : (tested[i] ? ' ✔' : ' ✖')}</button>`).join('')}</div>`;
        } else if (mode === 'ohm') {
          ctl.innerHTML = `<div class="lb-circuit-row" style="align-items:center;justify-content:space-between">
  <div class="lb-circuit-step"><span class="lb-circuit-lab">Cells</span><button class="lb-circuit-b" data-cells="-1">−</button><b>${cells}</b><button class="lb-circuit-b" data-cells="1">+</button></div>
  <button class="lb-circuit-b reset" data-reset="1">↺ Reset</button></div>
<div class="lb-circuit-row" style="align-items:center"><span class="lb-circuit-lab" style="width:100%;margin-bottom:-2px">Resistor</span>${resistors.map((rv, i) =>
            `<button class="lb-circuit-b ${i === resIdx ? 'on' : ''}" data-res="${i}" style="font-size:14px">${fmt(rv)} Ω</button>`).join('')}</div>`;
        } else {
          ctl.innerHTML = `<div class="lb-circuit-row">${tray.map(k =>
            `<button class="lb-circuit-b ${tool === k ? 'on' : ''}" data-tool="${k}"><span>${PART_INFO[k].icon}</span>${PART_INFO[k].label}</button>`).join('')}
  <button class="lb-circuit-b reset" data-reset="1" aria-label="reset">↺</button></div>`;
        }
      }

      function status(r) {
        const insul = LAY.slots.map(s => S[s.id]).find(q => q.k === 'mat' && q.m != null && !mats[q.m].conductor);
        const sw = LAY.slots.map(s => S[s.id]).find(q => q.k === 'switch' && !q.on);
        const bulbs = LAY.slots.filter(s => S[s.id].k === 'bulb');
        const lit = bulbs.filter(s => slotI(r, s) > 1e-9);
        if (r.state === 'short') return ['bad', '⚠️ Short circuit! Current has a path with no bulb or resistor — the cell gets hot. Add a bulb.'];
        if (r.state === 'nocell' || r.state === 'open-nocell') return ['', '🔋 Add a cell — it pushes the current round the circuit.'];
        if (r.state === 'open') {
          if (mode === 'materials' && insul) return ['bad', `✖ ${insul ? esc(mats[insul.m].name) : ''} is an insulator — no current flows.`];
          if (mode === 'materials') return ['', '👆 Tap a material below to put it in the test gap.'];
          if (sw && !LAY.slots.some(s => S[s.id].k === 'empty')) return ['', '🔘 The switch is OFF (open). Tap it to close it.'];
          return ['', '⭕ The circuit is open — fill every gap so the loop is complete.'];
        }
        if (mode === 'materials') { const m = mats[S.B1.m]; return ['ok', `✔ ${esc(m.name)} is a conductor — the bulb glows!`]; }
        if (mode === 'ohm') return ['ok', `⚡ Current flows: ${fmt(r.I)} A`];
        if (!bulbs.length) return ['', `Current flows (${fmt(r.I)} A) but there is no bulb to light.`];
        if (lit.length < bulbs.length) return ['ok', `💡 ${lit.length} of ${bulbs.length} bulbs glow — a bulb with a short path around it gets no current.`];
        if (lit.length >= 2 && layoutName === 'series') return ['ok', `💡 Both bulbs glow but dimmer — they share the cell's voltage.`];
        return ['ok', lit.length > 1 ? '💡 The bulbs glow — the circuit is closed!' : '💡 The bulb glows — the circuit is closed!'];
      }

      function check(r) {
        if (won) return;
        const bulbsLit = LAY.slots.filter(s => S[s.id].k === 'bulb' && slotI(r, s) > 1e-9);
        let ok = false, m = '';
        if (goal === 'light') { ok = bulbsLit.length > 0; m = 'The loop is closed, so current flows and the bulb glows!'; }
        else if (goal === 'switch') {
          ok = bulbsLit.length > 0 && LAY.slots.some(s => S[s.id].k === 'switch' && S[s.id].on);
          m = 'Switch ON = closed circuit, so the bulb glows. Switch OFF breaks the loop.';
        } else if (goal === 'series') {
          ok = layoutName === 'series' && bulbsLit.length >= 2;
          m = `In series the bulbs share the voltage: only ${fmt(r.I)} A flows, so each bulb is dimmer than one alone.`;
        } else if (goal === 'parallel') {
          ok = bulbsLit.some(s => s.br === 'a') && bulbsLit.some(s => s.br === 'b');
          m = 'In parallel each bulb gets the full cell voltage, so both glow brightly — and one can work without the other.';
        } else if (goal === 'materials') {
          ok = mats.every((_, i) => tested[i] !== undefined);
          const c = mats.filter(x => x.conductor).map(x => x.name), n = mats.filter(x => !x.conductor).map(x => x.name);
          m = `Conductors: ${c.join(', ') || '—'}. Insulators: ${n.join(', ') || '—'}.`;
        } else if (goal === 'current') {
          ok = r.state === 'ok' && Math.abs(r.I - target) < 0.005;
          m = `I = V ÷ R = ${fmt(r.V)} V ÷ ${fmt(r.Rt)} Ω = ${fmt(r.I)} A`;
        }
        if (ok) { won = true; api.sfx('correct'); api.win(p.winText ? String(p.winText) : m); }
      }

      function update() {
        if (mode === 'ohm') { S.L = { k: 'batt', n: cells }; S.R = { k: 'res', r: resistors[resIdx] }; }
        const r = solve();
        draw(r);
        const [cls, txt] = status(r);
        msgEl.className = 'lb-circuit-msg ' + (note ? '' : cls);
        msgEl.innerHTML = note || txt;
        if (showOhm) {
          ohmEl.textContent = r.state === 'ok'
            ? `V = ${fmt(r.V)} V · R = ${fmt(r.Rt)} Ω · I = V ÷ R = ${fmt(r.I)} A` + (layoutName === 'parallel' ? ` (I₁ = ${fmt(r.Ib.a)} A, I₂ = ${fmt(r.Ib.b)} A)` : '')
            : r.state === 'short' ? 'R ≈ 0 Ω — far too much current!' : `V = ${fmt(r.V)} V · circuit open, so I = 0 A`;
        }
        check(r);
      }
      function flash(t) { note = t; clearTimeout(noteTimer); noteTimer = setTimeout(() => { note = ''; update(); }, 2200); update(); }

      function tapSlot(id) {
        const s = LAY.slots.find(x => x.id === id), q = S[id];
        if (mode === 'materials' || mode === 'ohm') return;
        if (q.k === 'switch' && tool !== 'remove') { q.on = !q.on; note = ''; clearTimeout(noteTimer); api.sfx('tap'); update(); return; }
        if (locked.has(id)) { api.sfx('hmm'); flash('🔒 This part is fixed.'); return; }
        if (tool === 'remove') { if (q.k === 'empty') return; S[id] = { k: 'empty' }; api.sfx('tap'); update(); return; }
        if (tool === 'cell' && s.br !== 'm') { api.sfx('hmm'); flash('Put the cell on the left side.'); return; }
        const nq = mk(tool);
        if (q.k === nq.k) return;
        S[id] = nq; api.sfx('tap');
        if (tool === 'switch') { flash('🔘 Switch added (OFF). Tap it to switch ON.'); return; }
        update();
      }
      function onSvg(e) {
        const g = e.target.closest('[data-slot]');
        if (g) tapSlot(g.getAttribute('data-slot'));
      }
      function onCtl(e) {
        const b = e.target.closest('button'); if (!b) return;
        if (b.dataset.tool) { tool = b.dataset.tool; api.sfx('tap'); buildControls(); return; }
        if (b.dataset.reset) {
          resetSlots(); cells = Math.min(4, Math.max(1, Math.round(+p.cells || 2))); startRes();
          if (won) { won = false; api.resetWin && api.resetWin(); }
          note = ''; buildControls(); update(); return;
        }
        if (b.dataset.mat !== undefined) {
          const i = +b.dataset.mat; curMat = i; S.B1 = { k: 'mat', m: i }; tested[i] = mats[i].conductor;
          api.sfx(mats[i].conductor ? 'coin' : 'wrong'); buildControls(); update(); return;
        }
        if (b.dataset.cells) { cells = Math.min(4, Math.max(1, cells + +b.dataset.cells)); api.sfx('tap'); buildControls(); update(); return; }
        if (b.dataset.res !== undefined) { resIdx = +b.dataset.res; api.sfx('tap'); buildControls(); update(); }
      }
      svg.addEventListener('click', onSvg);
      ctl.addEventListener('click', onCtl);
      buildControls(); update();
      return () => { clearTimeout(noteTimer); svg.removeEventListener('click', onSvg); ctl.removeEventListener('click', onCtl); };
    },
    example: {
      mode: 'build',
      goal: 'switch',
      challenge: 'Build a circuit with a cell, a bulb and a switch — then switch it ON.',
      parts: ['cell', 'bulb', 'switch', 'wire'],
      cellV: 1.5,
      bulbR: 3
    },
    examples: [
      { mode: 'materials', goal: 'materials', challenge: 'Grade 6: Test each object. Sort them into conductors and insulators.' },
      { mode: 'parallel', goal: 'parallel', showOhm: true, parts: ['bulb', 'switch', 'wire'], challenge: 'Grade 10: Light one bulb in each branch. Compare the currents.' },
      { mode: 'ohm', goal: 'current', target: 1.5, cells: 1, resistors: [1, 2, 3, 4, 5, 6], challenge: 'Grade 10: Make a current of 1.5 A. Choose cells and a resistor (I = V ÷ R).' }
    ]
  });
})();
