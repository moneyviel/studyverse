/* StudyVerse Concept Lab: periodictable — interactive long-form periodic table (Z = 1–118)
 *
 * The child drags a finger across the table (the element under the finger is previewed live)
 * and lifts to select. Explore shows configuration / block / valence; Trend paints a heat-map of
 * a periodic property; Find asks for elements by position or configuration.
 *
 * PARAMS (all optional)
 *  mode       string  'explore' | 'trend' | 'find'                                         default 'explore'
 *  range      [a,b]   atomic numbers that are active (others are dimmed / hidden)            default [1,118]
 *  layout     string  'full' (18 groups + f-block rows) | 'main' (only groups 1,2,13–18,
 *                     big tiles — good for "first 20 elements")                              default 'full'
 *                     (rows/periods with no active element are not drawn)
 *  property   string  trend mode start property: 'radius' (atomic radius, pm, NCERT Table 3.6) |
 *                     'ie' (first ionisation enthalpy, kJ mol⁻¹) | 'en' (electronegativity,
 *                     Pauling) | 'metal' (metallic character, qualitative)                   default 'ie'
 *  properties array   property chips shown in trend mode                     default ['radius','ie','en','metal']
 *  goal       object  explore: {type:'blocks'} tap an element of every block present         (default)
 *                              {type:'visit', elements:['Na','K',…]} open all listed elements
 *                     trend:   {type:'max'|'min', property, among:['Na','Mg',…]} tap the extreme
 *                              {type:'order', property, among:[…]} tap in INCREASING order
 *                              default {type:'order', property:'ie', among:['Li','Be','B','C','N','O','F']}
 *  questions  array   find mode: items {q:'text', a:'Cl' | ['Li','Na']}  (q may be Hindi) or
 *                     criteria objects (text auto-made): {period:3, group:17} | {z:26} |
 *                     {config:'3s2 3p4'} (valence shell) | {block:'d', period:4} | {family:'halogen'}
 *                     default: 5 random questions generated from the active range
 *  rounds     number  how many generated questions when `questions` is absent               default 5
 *  hideValues bool    trend mode: hide the numbers (predict from the colours/trend only)     default false
 *  challenge  string  challenge sentence (else generated)
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const SUP = { 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
  const sup = s => String(s).replace(/([spdf])(\d+)/g, (m, l, n) => l + n.replace(/\d/g, d => SUP[d])); // electron counts only
  // symbol name mass  (mass in ( ) = mass number of the longest-lived isotope)
  const RAW = ('H Hydrogen 1.008|He Helium 4.003|Li Lithium 6.94|Be Beryllium 9.01|B Boron 10.81|C Carbon 12.01|N Nitrogen 14.01|O Oxygen 16.00|F Fluorine 19.00|Ne Neon 20.18|' +
    'Na Sodium 22.99|Mg Magnesium 24.31|Al Aluminium 26.98|Si Silicon 28.09|P Phosphorus 30.97|S Sulphur 32.06|Cl Chlorine 35.45|Ar Argon 39.95|' +
    'K Potassium 39.10|Ca Calcium 40.08|Sc Scandium 44.96|Ti Titanium 47.87|V Vanadium 50.94|Cr Chromium 52.00|Mn Manganese 54.94|Fe Iron 55.85|Co Cobalt 58.93|Ni Nickel 58.69|Cu Copper 63.55|Zn Zinc 65.38|Ga Gallium 69.72|Ge Germanium 72.63|As Arsenic 74.92|Se Selenium 78.97|Br Bromine 79.90|Kr Krypton 83.80|' +
    'Rb Rubidium 85.47|Sr Strontium 87.62|Y Yttrium 88.91|Zr Zirconium 91.22|Nb Niobium 92.91|Mo Molybdenum 95.95|Tc Technetium (98)|Ru Ruthenium 101.07|Rh Rhodium 102.91|Pd Palladium 106.42|Ag Silver 107.87|Cd Cadmium 112.41|In Indium 114.82|Sn Tin 118.71|Sb Antimony 121.76|Te Tellurium 127.60|I Iodine 126.90|Xe Xenon 131.29|' +
    'Cs Caesium 132.91|Ba Barium 137.33|La Lanthanum 138.91|Ce Cerium 140.12|Pr Praseodymium 140.91|Nd Neodymium 144.24|Pm Promethium (145)|Sm Samarium 150.36|Eu Europium 151.96|Gd Gadolinium 157.25|Tb Terbium 158.93|Dy Dysprosium 162.50|Ho Holmium 164.93|Er Erbium 167.26|Tm Thulium 168.93|Yb Ytterbium 173.05|Lu Lutetium 174.97|' +
    'Hf Hafnium 178.49|Ta Tantalum 180.95|W Tungsten 183.84|Re Rhenium 186.21|Os Osmium 190.23|Ir Iridium 192.22|Pt Platinum 195.08|Au Gold 196.97|Hg Mercury 200.59|Tl Thallium 204.38|Pb Lead 207.2|Bi Bismuth 208.98|Po Polonium (209)|At Astatine (210)|Rn Radon (222)|' +
    'Fr Francium (223)|Ra Radium (226)|Ac Actinium (227)|Th Thorium 232.04|Pa Protactinium 231.04|U Uranium 238.03|Np Neptunium (237)|Pu Plutonium (244)|Am Americium (243)|Cm Curium (247)|Bk Berkelium (247)|Cf Californium (251)|Es Einsteinium (252)|Fm Fermium (257)|Md Mendelevium (258)|No Nobelium (259)|Lr Lawrencium (262)|' +
    'Rf Rutherfordium (267)|Db Dubnium (268)|Sg Seaborgium (269)|Bh Bohrium (270)|Hs Hassium (269)|Mt Meitnerium (278)|Ds Darmstadtium (281)|Rg Roentgenium (282)|Cn Copernicium (285)|Nh Nihonium (286)|Fl Flerovium (289)|Mc Moscovium (290)|Lv Livermorium (293)|Ts Tennessine (294)|Og Oganesson (294)').split('|');

  // ---------- electronic configuration (Aufbau + the experimentally known exceptions, NCERT) ----------
  const ORD = ['1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p', '5s', '4d', '5p', '6s', '4f', '5d', '6p', '7s', '5f', '6d', '7p'];
  const CAP = { s: 2, p: 6, d: 10, f: 14 }, LORD = { s: 0, p: 1, d: 2, f: 3 };
  const NOBLE = [2, 10, 18, 36, 54, 86, 118], NSYM = { 2: 'He', 10: 'Ne', 18: 'Ar', 36: 'Kr', 54: 'Xe', 86: 'Rn' };
  const EXC = { 24: '3d5 4s1', 29: '3d10 4s1', 41: '4d4 5s1', 42: '4d5 5s1', 44: '4d7 5s1', 45: '4d8 5s1', 46: '4d10', 47: '4d10 5s1',
    57: '5d1 6s2', 58: '4f1 5d1 6s2', 64: '4f7 5d1 6s2', 78: '4f14 5d9 6s1', 79: '4f14 5d10 6s1',
    89: '6d1 7s2', 90: '6d2 7s2', 91: '5f2 6d1 7s2', 92: '5f3 6d1 7s2', 93: '5f4 6d1 7s2', 96: '5f7 6d1 7s2' };
  function madelung(z) { const c = {}; let e = z; for (const o of ORD) { if (e <= 0) break; const k = Math.min(e, CAP[o[1]]); c[o] = k; e -= k; } return c; }
  const sortOrb = a => a.sort((x, y) => (+x[0] - +y[0]) || (LORD[x[1]] - LORD[y[1]]));
  function config(z) {
    let core = 0; for (const n of NOBLE) if (n < z) core = n;
    let rem = {};
    if (EXC[z]) EXC[z].split(' ').forEach(t => { rem[t.slice(0, 2)] = +t.slice(2); });
    else { const full = madelung(z), cc = madelung(core); for (const o in full) { const k = full[o] - (cc[o] || 0); if (k > 0) rem[o] = k; } }
    const orbs = sortOrb(Object.keys(rem));
    const remStr = orbs.map(o => o + rem[o]).join(' ');
    const all = Object.assign({}, madelung(core)); for (const o in rem) all[o] = (all[o] || 0) + rem[o];
    const shells = []; for (const o in all) { const n = +o[0]; shells[n - 1] = (shells[n - 1] || 0) + all[o]; }
    return { core, rem, remStr, text: (core ? '[' + NSYM[core] + '] ' : '') + sup(remStr), shells: Array.from(shells, v => v || 0) };
  }
  // ---------- position ----------
  const START = [0, 1, 3, 11, 19, 37, 55, 87];
  function place(z) {
    const per = z <= 2 ? 1 : z <= 10 ? 2 : z <= 18 ? 3 : z <= 36 ? 4 : z <= 54 ? 5 : z <= 86 ? 6 : 7;
    const i = z - START[per]; let g = null, col, row = per;
    if (per === 1) g = z === 1 ? 1 : 18;
    else if (per <= 3) g = i < 2 ? i + 1 : i + 11;
    else if (per <= 5) g = i + 1;
    else if (i < 3) g = i + 1;
    else if (i < 17) { col = 4 + (i - 3); row = per + 2; }
    else g = i - 17 + 4;
    if (g) col = g;
    const block = !g ? 'f' : (g <= 2 || z === 2) ? 's' : g <= 12 ? 'd' : 'p';
    return { per, g, col, row, block };
  }
  const METALLOID = new Set(['Si', 'Ge', 'As', 'Sb', 'Te']);
  const NONMETAL = new Set(['H', 'B', 'C', 'N', 'O', 'P', 'S', 'Se']);
  const E = [null];
  RAW.forEach((r, k) => {
    const [sym, name, m] = r.split(' '), z = k + 1, ps = place(z);
    const e = Object.assign({ z, sym, name, mass: m }, ps);
    e.cfg = config(z);
    if (z >= 104) e.cat = 'Synthetic superheavy (properties barely known)';
    else if (ps.g === 18) e.cat = 'Noble gas';
    else if (ps.g === 17) e.cat = z === 85 ? 'Halogen (radioactive)' : 'Halogen — non-metal';
    else if (NONMETAL.has(sym)) e.cat = 'Non-metal';
    else if (METALLOID.has(sym)) e.cat = 'Metalloid';
    else if (ps.g === 1) e.cat = 'Alkali metal';
    else if (ps.g === 2) e.cat = 'Alkaline earth metal';
    else if (ps.block === 'd') e.cat = [30, 48, 80].includes(z) ? 'd-block metal (not a typical transition element: full d¹⁰)' : 'Transition metal';
    else if (ps.block === 'f') e.cat = ps.per === 6 ? 'Lanthanoid (inner transition)' : 'Actinoid (inner transition, radioactive)';
    else e.cat = 'p-block metal';
    E.push(e);
  });
  const BYSYM = {}; E.forEach(e => { if (e) BYSYM[e.sym.toLowerCase()] = e; });
  const bySym = s => BYSYM[String(s || '').trim().toLowerCase()];
  function valence(e) {
    if (e.block === 's') return e.z === 2 ? 2 : e.g;
    if (e.block === 'p') return e.g - 10;
    return null;
  }
  function valency(e) {
    const v = valence(e); if (v == null) return null;
    if (e.g === 18) return 0;
    return v <= 4 ? v : 8 - v;
  }
  function valShell(e) { // valence-shell configuration string, e.g. '3s2 3p5', '3d5 4s1'
    const o = Object.keys(e.cfg.rem); const n = e.per;
    if (e.block === 's' || e.block === 'p') return sortOrb(o.filter(k => +k[0] === n)).map(k => k + e.cfg.rem[k]).join(' ');
    if (e.block === 'd') return sortOrb(o.filter(k => k[1] !== 'f')).map(k => k + e.cfg.rem[k]).join(' ');
    return e.cfg.remStr;
  }
  const normCfg = s => String(s || '').replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹]/g, c => Object.keys(SUP).find(k => SUP[k] === c)).replace(/\s+/g, '').toLowerCase();

  // ---------- trend data (exact standard values; elements absent = "data not shown") ----------
  const RADIUS = { Li: 152, Be: 111, B: 88, C: 77, N: 74, O: 66, F: 64, Na: 186, Mg: 160, Al: 143, Si: 117, P: 110, S: 104, Cl: 99, K: 231, Rb: 244, Cs: 262, Br: 114, I: 133, At: 140 };
  const IE = { H: 1312, He: 2372, Li: 520, Be: 899, B: 801, C: 1086, N: 1402, O: 1314, F: 1681, Ne: 2081, Na: 496, Mg: 738, Al: 578, Si: 787, P: 1012, S: 1000, Cl: 1251, Ar: 1521,
    K: 419, Ca: 590, Sc: 633, Ti: 659, V: 651, Cr: 653, Mn: 717, Fe: 762, Co: 760, Ni: 737, Cu: 745, Zn: 906, Ga: 579, Ge: 762, As: 944, Se: 941, Br: 1140, Kr: 1351,
    Rb: 403, Sr: 549, In: 558, Sn: 709, Sb: 831, Te: 869, I: 1008, Xe: 1170, Cs: 376, Ba: 503, Tl: 589, Pb: 716, Bi: 703, Po: 812, At: 899, Rn: 1037, Fr: 393, Ra: 509 };
  const EN = { H: 2.20, Li: 0.98, Be: 1.57, B: 2.04, C: 2.55, N: 3.04, O: 3.44, F: 3.98, Na: 0.93, Mg: 1.31, Al: 1.61, Si: 1.90, P: 2.19, S: 2.58, Cl: 3.16,
    K: 0.82, Ca: 1.00, Sc: 1.36, Ti: 1.54, V: 1.63, Cr: 1.66, Mn: 1.55, Fe: 1.83, Co: 1.88, Ni: 1.91, Cu: 1.90, Zn: 1.65, Ga: 1.81, Ge: 2.01, As: 2.18, Se: 2.55, Br: 2.96,
    Rb: 0.82, Sr: 0.95, In: 1.78, Sn: 1.96, Sb: 2.05, Te: 2.10, I: 2.66, Cs: 0.79, Ba: 0.89, Tl: 1.62, Bi: 2.02 };
  const METAL_LV = ['', 'Low (non-metal)', 'Intermediate (metalloid)', 'Metallic', 'High', 'Very high'];
  function metalLevel(e) {
    if (e.z >= 104 || e.g === 18 || e.z === 85) return null;
    if (e.g === 1 && e.z > 1) return 5; if (e.g === 2) return 4;
    if (METALLOID.has(e.sym)) return 2; if (NONMETAL.has(e.sym) || e.g === 17) return 1;
    return 3;
  }
  const PROPS = {
    radius: { name: 'Atomic radius', unit: 'pm', get: e => RADIUS[e.sym], fmt: v => v + ' pm', trend: 'Decreases across a period (nuclear charge ↑, same shell); increases down a group (new shell added).', src: 'NCERT Table 3.6' },
    ie: { name: 'Ionisation enthalpy', unit: 'kJ mol⁻¹', get: e => IE[e.sym], fmt: v => v + ' kJ mol⁻¹', trend: 'Generally increases across a period and decreases down a group. Dips: Be→B (2p is easier to remove) and N→O (paired 2p electron).', src: 'first ionisation enthalpy, Δ<sub>i</sub>H₁' },
    en: { name: 'Electronegativity', unit: 'Pauling', get: e => EN[e.sym], fmt: v => v.toFixed(2) + ' (Pauling)', trend: 'Increases across a period, decreases down a group. F is the most electronegative (3.98).', src: 'Pauling scale' },
    metal: { name: 'Metallic character', unit: '', get: metalLevel, fmt: v => METAL_LV[v], trend: 'Increases down a group and decreases across a period (qualitative — there is no single number).', src: 'qualitative' }
  };
  const FAM = { 1: 'alkali metal', 2: 'alkaline earth metal', 15: 'group 15 element (pnictogen)', 16: 'chalcogen', 17: 'halogen', 18: 'noble gas' };
  const BLOCKCOL = { s: ['#ffe1e1', '#c94545'], p: ['#fff3c9', '#a67c00'], d: ['#dde9ff', '#2257b8'], f: ['#d8f7ec', '#0f7a5c'] };
  const HEAT = ['#f3efff', '#d9ccff', '#b49cff', '#8b5cf6', '#6a3be0', '#4a22b5'];
  const hex = h => [1, 3, 5].map(i => parseInt(h.substr(i, 2), 16));
  const heat = t => { t = Math.max(0, Math.min(1, t)) * (HEAT.length - 1); const i = Math.min(HEAT.length - 2, Math.floor(t)), f = t - i, a = hex(HEAT[i]), b = hex(HEAT[i + 1]); return 'rgb(' + a.map((v, k) => Math.round(v + (b[k] - v) * f)).join(',') + ')'; };

  const CSS = `
  .lb-periodictable{color:#1b1f3a;font-weight:700;user-select:none;-webkit-user-select:none}
  .lb-periodictable-ch{background:#f3efff;color:#4c2fb0;border-radius:14px;padding:7px 11px;font-size:13px;line-height:1.3;margin-bottom:6px}
  .lb-periodictable-q{font-size:13.5px;font-weight:900;color:#1b1f3a;margin:-1px 0 5px;min-height:18px;line-height:1.25}
  .lb-periodictable-q small{color:#6b7090;font-weight:800}
  .lb-periodictable-chips{display:flex;gap:5px;margin-bottom:6px;overflow-x:auto;scrollbar-width:none}
  .lb-periodictable-chips::-webkit-scrollbar{display:none}
  .lb-periodictable-chip{flex:none;min-height:36px;padding:0 10px;border-radius:12px;border:2px solid #e3e6f6;background:#fff;font:inherit;font-size:12px;font-weight:800;color:#1b1f3a;cursor:pointer}
  .lb-periodictable-chip.on{border-color:#8b5cf6;background:#f1edff;color:#4c2fb0}
  .lb-periodictable-svg{display:block;width:100%;height:auto;touch-action:none;cursor:pointer}
  .lb-periodictable-svg text{pointer-events:none;font-family:inherit}
  .lb-periodictable-info{display:flex;gap:9px;align-items:stretch;background:#f7f8fd;border-radius:16px;padding:8px;margin-top:6px;min-height:92px}
  .lb-periodictable-tile{flex:none;width:76px;border-radius:13px;display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1.05;border:2px solid rgba(0,0,0,.06);transition:background .2s}
  .lb-periodictable-tile b{font-size:27px;font-weight:900}
  .lb-periodictable-tile span{font-size:10.5px;font-weight:800;opacity:.85}
  .lb-periodictable-txt{flex:1;font-size:12px;line-height:1.38;color:#6b7090;min-width:0}
  .lb-periodictable-txt b{color:#1b1f3a}
  .lb-periodictable-txt .nm{font-size:14.5px;color:#1b1f3a;font-weight:900}
  .lb-periodictable-bar{display:flex;align-items:center;gap:6px;font-size:10.5px;color:#6b7090;margin-top:4px}
  .lb-periodictable-bar i{flex:1;height:9px;border-radius:5px}
  .lb-periodictable-row{display:flex;gap:6px;align-items:center;margin-top:6px}
  .lb-periodictable-msg{flex:1;font-size:12px;color:#6b7090;min-height:16px;line-height:1.3}
  .lb-periodictable-msg.good{color:#0f7a5c}.lb-periodictable-msg.bad{color:#c94545}
  .lb-periodictable-btn{flex:none;min-height:40px;padding:0 13px;border:none;border-radius:12px;background:#eef0fb;color:#1b1f3a;font:inherit;font-weight:800;font-size:12.5px;box-shadow:0 3px 0 #d3d7ef;cursor:pointer}
  .lb-periodictable-btn:active{transform:translateY(2px);box-shadow:none}
  @keyframes lb-periodictable-pop{0%{opacity:1}100%{opacity:0}}
  .lb-periodictable-flash{animation:lb-periodictable-pop .9s ease-out forwards}`;

  Labs.register('periodictable', {
    title: 'Periodic table',
    subjects: ['science', 'chemistry'],
    render(host, p, api) {
      const mode = ['explore', 'trend', 'find'].includes(p.mode) ? p.mode : 'explore';
      let lo = 1, hi = 118;
      if (Array.isArray(p.range) && p.range.length === 2) { lo = Math.max(1, Math.min(118, Math.round(+p.range[0] || 1))); hi = Math.max(lo, Math.min(118, Math.round(+p.range[1] || 118))); }
      const active = z => z >= lo && z <= hi;
      const layout = p.layout === 'main' ? 'main' : 'full';
      const timers = []; const later = (f, ms) => timers.push(setTimeout(f, ms));
      let won = false; const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(m); };
      const rand = a => a[Math.floor(Math.random() * a.length)];
      const els = E.filter(e => e && active(e.z) && (layout === 'full' || e.block === 's' || e.block === 'p'));
      if (!els.length) els.push(E[1]);

      // ---------- geometry ----------
      let cols, rows, CW, CH, GAP = 1.2, HEAD = 11, cells = [];
      if (layout === 'main') {
        const G = [1, 2, 13, 14, 15, 16, 17, 18];
        const pers = [...new Set(els.map(e => e.per))].sort((a, b) => a - b);
        CW = 46; CH = pers.length > 4 ? 38 : 42; cols = 8;
        els.forEach(e => cells.push({ e, x: G.indexOf(e.g) * CW, y: HEAD + pers.indexOf(e.per) * CH, w: CW - 3, h: CH - 3 }));
        rows = pers.length;
        var W = cols * CW - 3, H = HEAD + rows * CH - 3, colHead = G.map((g, i) => [i * CW + (CW - 3) / 2, g]);
      } else {
        CW = 21; CH = 23;
        const maxPer = Math.max(...els.map(e => e.per)), hasF = els.some(e => e.block === 'f');
        const fGap = 6;
        E.forEach(e => {
          if (!e || e.per > maxPer) return; if (e.block === 'f' && !hasF) return;
          const r = e.row <= 7 ? e.row - 1 : maxPer + (e.row - 8); const y = HEAD + r * CH + (e.row > 7 ? fGap : 0);
          cells.push({ e, x: (e.col - 1) * CW, y, w: CW - GAP, h: CH - GAP });
        });
        const lastRow = Math.max(...cells.map(c => c.y + c.h));
        var W = 18 * CW - GAP, H = lastRow, colHead = Array.from({ length: 18 }, (_, i) => [i * CW + (CW - GAP) / 2, i + 1]);
      }
      const big = layout === 'main';

      // ---------- goals / challenge ----------
      const goal = (p.goal && typeof p.goal === 'object') ? p.goal : {};
      const propList = (Array.isArray(p.properties) ? p.properties : ['radius', 'ie', 'en', 'metal']).filter(k => PROPS[k]);
      let prop = PROPS[p.property] ? p.property : (PROPS[goal.property] ? goal.property : 'ie');
      if (mode === 'trend' && !propList.includes(prop)) propList.unshift(prop);
      let challenge = p.challenge ? String(p.challenge) : '';
      let tGoal = null, among = [], seq = [], visited = new Set(), qList = [], qi = 0;
      const blocksPresent = [...new Set(els.map(e => e.block))];

      if (mode === 'explore') {
        if (goal.type === 'visit' && Array.isArray(goal.elements)) {
          among = goal.elements.map(bySym).filter(e => e && active(e.z));
          if (!challenge) challenge = 'Open each of these elements and compare them: ' + among.map(e => e.sym).join(', ') + '.';
        }
        if (!among.length && !challenge) challenge = 'Drag across the table and lift to open an element. Open one from each block: ' + blocksPresent.join(', ') + '.';
      } else if (mode === 'trend') {
        const tg = PROPS[goal.property] ? goal.property : prop;
        const tType = ['max', 'min', 'order'].includes(goal.type) ? goal.type : 'order';
        let am = (Array.isArray(goal.among) ? goal.among : (goal.type ? [] : ['Li', 'Be', 'B', 'C', 'N', 'O', 'F'])).map(bySym).filter(e => e && active(e.z) && PROPS[tg].get(e) != null);
        if (am.length < 2) { // fall back to a period that has data
          am = ['Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl'].map(bySym).filter(e => active(e.z) && PROPS[tg].get(e) != null).slice(0, 7);
        }
        if (am.length >= 2) {
          tGoal = { type: tType, prop: tg }; among = am;
          const nm = PROPS[tg].name.toLowerCase();
          if (!challenge) challenge = tType === 'order' ? `Tap ${am.map(e => e.sym).join(', ')} in increasing order of ${nm}.` : `Among ${am.map(e => e.sym).join(', ')}, tap the one with the ${tType === 'max' ? 'highest' : 'lowest'} ${nm}.`;
          if (tType === 'order') { const vals = am.map(e => PROPS[tg].get(e)); if (new Set(vals).size !== vals.length) tGoal.type = 'max'; }
        }
        if (!challenge) challenge = 'Switch properties and see how they change across a period and down a group.';
      } else {
        // build questions
        const crit = q => {
          if (!q || typeof q !== 'object') return null;
          if (q.a != null) { const a = (Array.isArray(q.a) ? q.a : [q.a]).map(bySym).filter(Boolean).map(e => e.z); return a.length ? { text: String(q.q || 'Find ' + q.a), ans: a } : null; }
          let pool = els.slice(), parts = [];
          if (q.z) { pool = pool.filter(e => e.z === +q.z); parts.push('atomic number ' + (+q.z)); }
          if (q.family) { const g = +Object.keys(FAM).find(k => FAM[k].startsWith(String(q.family).toLowerCase())); if (g) { pool = pool.filter(e => e.g === g && e.z !== 1); } }
          if (q.group) pool = pool.filter(e => e.g === +q.group);
          if (q.period) pool = pool.filter(e => e.per === +q.period);
          if (q.block) pool = pool.filter(e => e.block === String(q.block).toLowerCase());
          if (q.config) pool = pool.filter(e => normCfg(valShell(e)) === normCfg(q.config) || normCfg(e.cfg.remStr) === normCfg(q.config));
          if (!pool.length) return null;
          let text = q.q ? String(q.q) : '';
          if (!text) {
            const fam = q.family ? String(q.family).toLowerCase() : (q.group && FAM[q.group] && !q.period ? null : null);
            if (q.config) text = 'Valence shell: ' + sup(q.config);
            else if (q.z) text = 'The element with Z = ' + (+q.z);
            else if (q.family && q.period) text = 'The ' + fam + ' of period ' + q.period;
            else if (q.family) text = 'Any ' + fam;
            else if (q.period && q.group) text = 'Period ' + q.period + ', group ' + q.group;
            else if (q.block && q.period) text = 'Any ' + q.block + '-block element of period ' + q.period;
            else if (q.group) text = 'Any element of group ' + q.group;
            else text = 'Find the element';
          }
          return { text, ans: pool.map(e => e.z) };
        };
        if (Array.isArray(p.questions) && p.questions.length) qList = p.questions.map(crit).filter(Boolean);
        if (!qList.length) {
          const n = Math.max(1, Math.min(12, Math.round(+p.rounds || 5)));
          const gens = [
            () => { const e = rand(els.filter(e => e.g && FAM[e.g] && e.z !== 1 && e.z < 104)); return e && { family: FAM[e.g], period: e.per }; },
            () => { const e = rand(els.filter(e => e.g)); return e && { period: e.per, group: e.g }; },
            () => { const e = rand(els.filter(e => (e.block === 's' || e.block === 'p') && e.z < 104 && e.z > 2)); return e && { config: valShell(e) }; },
            () => { const e = rand(els.filter(e => e.block === 'd' && e.z < 104)); return e && { config: valShell(e) }; },
            () => { const e = rand(els); return e && { z: e.z }; }
          ];
          let guard = 0; const seen = new Set();
          while (qList.length < n && guard++ < 200) {
            const c = rand(gens)(); if (!c) continue; const q = crit(c); if (!q) continue;
            const key = q.ans.join(','); if (seen.has(key)) continue; seen.add(key); qList.push(q);
          }
        }
        if (!qList.length) qList = [{ text: 'Hydrogen', ans: [1] }];
        if (!challenge) challenge = `Find ${qList.length} element${qList.length > 1 ? 's' : ''}: read the clue, drag to the right square and lift your finger.`;
      }

      // ---------- DOM ----------
      const chipsHTML = mode === 'trend' ? `<div class="lb-periodictable-chips">${propList.map(k => `<button class="lb-periodictable-chip" data-p="${k}">${PROPS[k].name}</button>`).join('')}</div>` : '';
      host.innerHTML = `<style>${CSS}</style><div class="lb-periodictable">
        <div class="lb-periodictable-ch">🎯 Challenge: ${esc(challenge)}</div>
        ${mode === 'find' ? '<div class="lb-periodictable-q"></div>' : ''}${chipsHTML}
        <svg class="lb-periodictable-svg" viewBox="-1 0 ${W + 2} ${H + 1}"></svg>
        <div class="lb-periodictable-info"></div>
        <div class="lb-periodictable-row"><div class="lb-periodictable-msg"></div>${mode === 'find' || tGoal ? '<button class="lb-periodictable-btn" data-r>↺ New</button>' : ''}</div></div>`;
      const root = host.querySelector('.lb-periodictable'), $ = s => root.querySelector(s);
      const svg = $('svg'), info = $('.lb-periodictable-info'), msg = $('.lb-periodictable-msg'), qEl = $('.lb-periodictable-q');
      const setMsg = (t, c) => { msg.innerHTML = t; msg.className = 'lb-periodictable-msg' + (c ? ' ' + c : ''); };

      function cellFill(e) {
        if (!active(e.z) || (layout === 'main' && !(e.block === 's' || e.block === 'p'))) return ['#f1f2f7', '#c3c7da'];
        if (mode === 'trend') {
          const P = PROPS[prop], v = P.get(e); if (v == null) return ['#f6f7fb', '#b4b8cc'];
          const vs = els.map(P.get).filter(x => x != null); const mn = Math.min(...vs), mx = Math.max(...vs);
          const t = mx > mn ? (v - mn) / (mx - mn) : 0.5; return [heat(t), t > 0.55 ? '#fff' : '#1b1f3a'];
        }
        if (mode === 'find') return ['#eef1fb', '#1b1f3a'];
        return BLOCKCOL[e.block];
      }
      function draw() {
        let s = colHead.map(([x, g]) => `<text x="${x}" y="${big ? 8 : 7.5}" font-size="${big ? 8 : 6}" text-anchor="middle" fill="#9aa0c0" font-weight="800">${g}</text>`).join('');
        cells.forEach(c => {
          const e = c.e, [bg, fg] = cellFill(e), on = active(e.z);
          const mark = among.includes(e) ? `<rect x="${c.x - 0.6}" y="${c.y - 0.6}" width="${c.w + 1.2}" height="${c.h + 1.2}" rx="${big ? 7 : 3.5}" fill="none" stroke="#ff6b6b" stroke-width="${big ? 2 : 1.3}"/>` : '';
          const ord = seq.includes(e) ? `<circle cx="${c.x + c.w - (big ? 6 : 3)}" cy="${c.y + (big ? 6 : 3)}" r="${big ? 6 : 3.4}" fill="#2ed3a5"/><text x="${c.x + c.w - (big ? 6 : 3)}" y="${c.y + (big ? 8.5 : 4.5)}" font-size="${big ? 7 : 4}" text-anchor="middle" fill="#fff" font-weight="900">${seq.indexOf(e) + 1}</text>` : '';
          let val = '';
          if (mode === 'trend' && on && !p.hideValues && prop !== 'metal') { const v = PROPS[prop].get(e); if (v != null && big) val = `<text x="${c.x + c.w / 2}" y="${c.y + c.h - 4}" font-size="7" text-anchor="middle" fill="${fg}" opacity=".85">${prop === 'en' ? v.toFixed(2) : v}</text>`; }
          else if (mode === 'trend' && on && PROPS[prop].get(e) == null && big) val = `<text x="${c.x + c.w / 2}" y="${c.y + c.h - 4}" font-size="6.5" text-anchor="middle" fill="${fg}">no data</text>`;
          const nodata = mode === 'trend' && on && PROPS[prop].get(e) == null && !(layout === 'main' && !(e.block === 's' || e.block === 'p'));
          s += `<g><rect x="${c.x}" y="${c.y}" width="${c.w}" height="${c.h}" rx="${big ? 7 : 3}" fill="${nodata ? '#fff' : bg}"${nodata ? ` stroke="#c9cde3" stroke-width="${big ? 1 : 0.5}" stroke-dasharray="${big ? '3 2' : '1.5 1'}"` : ''}/>
            <text x="${c.x + (big ? 4 : 1.6)}" y="${c.y + (big ? 9 : 5.6)}" font-size="${big ? 7.5 : 4.6}" fill="${fg}" opacity=".75">${e.z}</text>
            <text x="${c.x + c.w / 2}" y="${c.y + (big ? (val || mode !== 'trend' ? 25 : 27) : 15.4)}" font-size="${big ? 15 : 8.6}" font-weight="900" text-anchor="middle" fill="${fg}">${e.sym}</text>
            ${big && mode !== 'trend' ? `<text x="${c.x + c.w / 2}" y="${c.y + c.h - 5}" font-size="6.3" text-anchor="middle" fill="${fg}" opacity=".8">${esc(e.mass)}</text>` : ''}${val}${mark}${ord}</g>`;
        });
        if (layout === 'full' && cells.some(c => c.e.block === 'f')) {
          const r6 = cells.find(c => c.e.z === 57), r7 = cells.find(c => c.e.z === 89);
          if (r6) s += `<text x="${3 * CW - 3}" y="${cells.find(c => c.e.z === 58).y + 14}" font-size="5.5" text-anchor="end" fill="#9aa0c0" font-weight="800">Ce–Lu ▸</text>`;
          if (r7 && cells.find(c => c.e.z === 90)) s += `<text x="${3 * CW - 3}" y="${cells.find(c => c.e.z === 90).y + 14}" font-size="5.5" text-anchor="end" fill="#9aa0c0" font-weight="800">Th–Lr ▸</text>`;
        }
        s += `<rect class="lb-periodictable-ring" x="0" y="0" width="0" height="0" rx="${big ? 8 : 4}" fill="none" stroke="#1b1f3a" stroke-width="${big ? 2.6 : 1.6}" style="display:none"/><g class="lb-periodictable-fx"></g>`;
        svg.innerHTML = s;
      }
      function ring(c) {
        const r = svg.querySelector('.lb-periodictable-ring'); if (!c) { r.style.display = 'none'; return; }
        const pad = big ? 1.5 : 1; r.style.display = ''; r.setAttribute('x', c.x - pad); r.setAttribute('y', c.y - pad); r.setAttribute('width', c.w + 2 * pad); r.setAttribute('height', c.h + 2 * pad);
      }
      function flash(c, col) {
        const g = svg.querySelector('.lb-periodictable-fx'); const r = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        r.setAttribute('x', c.x - 1); r.setAttribute('y', c.y - 1); r.setAttribute('width', c.w + 2); r.setAttribute('height', c.h + 2); r.setAttribute('rx', big ? 8 : 4);
        r.setAttribute('fill', col); r.setAttribute('opacity', '.75'); r.setAttribute('class', 'lb-periodictable-flash'); g.appendChild(r); later(() => r.remove(), 950);
      }
      function legend() {
        if (mode !== 'trend') return '';
        const P = PROPS[prop], vs = els.map(P.get).filter(x => x != null);
        if (!vs.length) return '<div class="lb-periodictable-bar">No data for these elements</div>';
        const g = `linear-gradient(90deg,${HEAT.join(',')})`;
        const f = v => prop === 'metal' ? '' : (prop === 'en' ? v.toFixed(2) : v);
        return `<div class="lb-periodictable-bar"><span>${prop === 'metal' ? 'low' : f(Math.min(...vs))}</span><i style="background:${g}"></i><span>${prop === 'metal' ? 'high' : f(Math.max(...vs)) + ' ' + P.unit}</span><span style="display:inline-block;width:10px;height:9px;border-radius:3px;background:#fff;border:1px dashed #b4b8cc"></span><span>no data</span></div>`;
      }
      function showInfo(e, preview) {
        if (!e) {
          const hint = mode === 'trend' ? `<div class="nm">${PROPS[prop].name}${PROPS[prop].unit ? ' <small style="font-weight:800;color:#6b7090">(' + PROPS[prop].unit + ')</small>' : ''}</div><div>${PROPS[prop].trend}</div>${legend()}`
            : `<div class="nm">Drag across the table</div><div>The element under your finger shows here. Lift your finger to choose it.</div>${mode === 'explore' ? '<div style="margin-top:3px"><span style="color:#c94545">■ s</span> · <span style="color:#a67c00">■ p</span> · <span style="color:#2257b8">■ d</span> · <span style="color:#0f7a5c">■ f</span>-block</div>' : ''}`;
          info.innerHTML = `<div class="lb-periodictable-tile" style="background:#eef0fb;color:#9aa0c0"><b>?</b></div><div class="lb-periodictable-txt">${hint}</div>`; return;
        }
        const [bg, fg] = mode === 'trend' ? cellFill(e) : BLOCKCOL[e.block];
        const tile = `<div class="lb-periodictable-tile" style="background:${bg};color:${fg}"><span>${e.z}</span><b>${e.sym}</b><span>${esc(e.mass)}</span></div>`;
        if (mode === 'find' && preview) { info.innerHTML = `<div class="lb-periodictable-tile" style="background:#eef1fb;color:#1b1f3a"><span>${e.z}</span><b>${e.sym}</b><span>${esc(e.mass)}</span></div><div class="lb-periodictable-txt"><div class="nm">${e.name}</div><div>Lift your finger to choose ${e.sym}.</div></div>`; return; }
        const pos = e.g ? `Period <b>${e.per}</b> · Group <b>${e.g}</b> · <b>${e.block}</b>-block` : `Period <b>${e.per}</b> · <b>f</b>-block (no group no.)`;
        let body;
        if (mode === 'trend') {
          const P = PROPS[prop], v = P.get(e);
          body = `<div class="nm">${e.name}</div><div>${pos}</div><div>${P.name}: <b>${v == null ? 'data not shown' : (p.hideValues && prop !== 'metal' ? 'hidden — use the colour' : P.fmt(v))}</b></div>${legend()}`;
        } else {
          const ve = valence(e), vy = valency(e);
          const vline = ve != null ? `Valence e⁻ <b>${ve}</b> · Valency <b>${vy}</b>` : `Valency <b>variable</b>`;
          body = `<div class="nm">${e.name} <small style="font-size:10.5px;color:#6b7090;font-weight:800">${esc(e.cat.replace(/ \(.*\)$/, '').replace(' — non-metal', ''))}</small></div><div>${pos}</div><div><b>${e.cfg.text}</b>${e.z >= 104 ? ' (predicted)' : ''}</div><div>Shells <b>${e.cfg.shells.join(', ')}</b> · ${vline}</div>`;
        }
        info.innerHTML = tile + `<div class="lb-periodictable-txt">${body}</div>`;
      }
      function showQ() {
        if (!qEl) return;
        if (qi >= qList.length) { qEl.innerHTML = '✅ All found!'; return; }
        qEl.innerHTML = `<small>Clue ${qi + 1}/${qList.length}:</small> ${esc(qList[qi].text)}`;
      }
      // ---------- selection logic ----------
      function commit(c) {
        const e = c.e; showInfo(e); ring(c); api.sfx('tap');
        if (mode === 'explore') {
          visited.add(e);
          if (among.length) {
            const left = among.filter(x => !visited.has(x));
            setMsg(left.length ? `Opened ${among.length - left.length}/${among.length}. Still to open: ${left.map(x => x.sym).join(', ')}` : 'All opened!', left.length ? '' : 'good');
            if (!left.length) later(() => winOnce('You compared ' + among.map(x => x.sym).join(', ') + ' — same group means the same valence-shell configuration.'), 400);
          } else {
            const got = blocksPresent.filter(b => [...visited].some(x => x.block === b));
            setMsg('Blocks opened: ' + blocksPresent.map(b => got.includes(b) ? '✅' + b : '⬜' + b).join(' '), got.length === blocksPresent.length ? 'good' : '');
            if (got.length === blocksPresent.length) later(() => winOnce('The block is the subshell that receives the last electron: ' + blocksPresent.map(b => b + ' → ' + b + '-orbital').join(', ') + '.'), 400);
          }
        } else if (mode === 'find') {
          if (qi >= qList.length) return;
          const q = qList[qi];
          if (q.ans.includes(e.z)) {
            api.sfx('coin'); flash(c, '#2ed3a5'); setMsg(`✓ ${e.name} (${e.sym}) — period ${e.per}${e.g ? ', group ' + e.g : ''}, ${sup(valShell(e))}.`, 'good'); qi++; showQ();
            if (qi >= qList.length) later(() => winOnce(`You found all ${qList.length}! Position in the table follows from the electronic configuration.`), 500);
          } else {
            api.sfx('wrong'); flash(c, '#ff6b6b');
            setMsg(`✗ ${e.sym} is period ${e.per}${e.g ? ', group ' + e.g : ' (f-block)'} (${sup(valShell(e))}). Try again.`, 'bad');
          }
        } else if (tGoal) {
          if (!among.includes(e)) { setMsg('That one is not in the challenge — tap a red-outlined element.', ''); return; }
          const P = PROPS[tGoal.prop], V = x => P.get(x);
          if (tGoal.type === 'order') {
            if (seq.includes(e)) return;
            const rest = among.filter(x => !seq.includes(x)), mn = Math.min(...rest.map(V));
            if (V(e) === mn) { seq.push(e); api.sfx('coin'); draw(); ring(c); setMsg(`✓ ${seq.map(x => x.sym).join(' < ')}`, 'good');
              if (seq.length === among.length) later(() => winOnce(`${P.name}: ${seq.map(x => x.sym + ' ' + (tGoal.prop === 'en' ? V(x).toFixed(2) : V(x))).join(' < ')} ${P.unit}`), 400); }
            else { api.sfx('wrong'); flash(c, '#ff6b6b'); setMsg(`✗ Not the next lowest. ${e.sym}: ${P.fmt(V(e))}. Look at the others first.`, 'bad'); }
          } else {
            const vals = among.map(V), best = tGoal.type === 'max' ? Math.max(...vals) : Math.min(...vals);
            if (V(e) === best) { api.sfx('coin'); flash(c, '#2ed3a5'); setMsg(`✓ ${e.sym}: ${P.fmt(V(e))}`, 'good'); later(() => winOnce(`${e.name} has the ${tGoal.type === 'max' ? 'highest' : 'lowest'} ${P.name.toLowerCase()} here (${P.fmt(V(e))}).`), 400); }
            else { api.sfx('wrong'); flash(c, '#ff6b6b'); setMsg(`✗ ${e.sym}: ${P.fmt(V(e))} — not the ${tGoal.type === 'max' ? 'highest' : 'lowest'}.`, 'bad'); }
          }
        }
      }
      // ---------- pointer ----------
      let dragging = false, last = null;
      function hit(ev) {
        const m = svg.getScreenCTM(); if (!m) return null;
        const pt = svg.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY; const q = pt.matrixTransform(m.inverse());
        let best = null, bd = 1e9;
        cells.forEach(c => { if (!active(c.e.z) || (layout === 'main' && !(c.e.block === 's' || c.e.block === 'p'))) return; const dx = Math.max(c.x - q.x, 0, q.x - c.x - c.w), dy = Math.max(c.y - q.y, 0, q.y - c.y - c.h), d = dx * dx + dy * dy; if (d < bd) { bd = d; best = c; } });
        return bd <= (big ? 36 : 16) ? best : null;
      }
      const down = ev => { dragging = true; try { svg.setPointerCapture(ev.pointerId); } catch (e) {} const c = hit(ev); last = c; if (c) { ring(c); showInfo(c.e, true); } };
      const move = ev => { if (!dragging) return; const c = hit(ev); if (c && c !== last) { last = c; ring(c); showInfo(c.e, true); } };
      const up = ev => { if (!dragging) return; dragging = false; const c = hit(ev) || last; last = null; if (c) commit(c); };
      const cancel = () => { dragging = false; last = null; };
      svg.addEventListener('pointerdown', down); svg.addEventListener('pointermove', move); svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', cancel);

      root.querySelectorAll('[data-p]').forEach(b => b.onclick = () => { prop = b.dataset.p; api.sfx('tap'); root.querySelectorAll('[data-p]').forEach(x => x.classList.toggle('on', x === b)); draw(); showInfo(null); });
      const rb = $('[data-r]');
      if (rb) rb.onclick = () => {
        api.sfx('tap'); seq = []; setMsg('');
        if (mode === 'find') { if (!(Array.isArray(p.questions) && p.questions.length)) { /* reshuffle generated */ qList.sort(() => Math.random() - 0.5); } qi = 0; showQ(); }
        if (won) { won = false; api.resetWin && api.resetWin(); }
        draw(); showInfo(null);
      };
      root.querySelectorAll('[data-p]').forEach(x => x.classList.toggle('on', x.dataset.p === prop));
      draw(); showInfo(null); showQ();
      if (mode === 'trend' && tGoal) setMsg('Red outline = elements in the challenge.');
      return () => { timers.forEach(clearTimeout); svg.removeEventListener('pointerdown', down); svg.removeEventListener('pointermove', move); svg.removeEventListener('pointerup', up); svg.removeEventListener('pointercancel', cancel); };
    },
    example: {
      mode: 'explore', range: [1, 118], layout: 'full',
      challenge: 'Drag across the table and lift to open an element. Open one element from each block — s, p, d and f — and compare their configurations.'
    },
    examples: [
      { mode: 'find', range: [1, 36], layout: 'full',
        questions: [{ family: 'halogen', period: 3 }, { period: 4, group: 2 }, { config: '3d5 4s1' }, { config: '2s2 2p4' }, { q: 'सबसे हल्की उत्कृष्ट गैस (lightest noble gas)', a: 'He' }],
        challenge: 'Class 11 · Classification: use period, group and configuration clues to find each element.' },
      { mode: 'trend', range: [1, 20], layout: 'main', property: 'ie', properties: ['ie', 'radius', 'en', 'metal'],
        goal: { type: 'order', property: 'ie', among: ['Li', 'Be', 'B', 'C', 'N', 'O', 'F'] },
        challenge: 'Tap Li to F in increasing order of first ionisation enthalpy — watch the Be/B and N/O dips!' },
      { mode: 'trend', range: [1, 56], layout: 'full', property: 'radius', properties: ['radius', 'en'],
        goal: { type: 'max', property: 'radius', among: ['Li', 'Na', 'K', 'Rb', 'Cs'] },
        challenge: 'Down group 1: tap the alkali metal with the largest atomic radius.' }
    ]
  });
})();
