/* StudyVerse Concept Lab: punnett — Punnett-square cross builder + pedigree reader
 *
 * Crosses: the child taps the allele buttons on each parent (♀ and ♂) to change their genotype.
 * Gametes are formed (law of segregation / independent assortment), the Punnett square fills in
 * and the genotype and phenotype ratios are computed live.
 * Pedigree: the child reads a pedigree chart, taps people to see their possible genotypes under a
 * chosen mode of inheritance, and decides dominant/recessive and autosomal/X-linked.
 *
 * PARAMS (all optional)
 *  mode      string  'mono' | 'di' | 'test' (test cross) | 'incomplete' | 'codominance' (ABO) |
 *                    'sexlinked' | 'pedigree'                                                default 'mono'
 *  gene      object  one gene {letter:'T', dom:'Tall', rec:'Dwarf', het?:'Pink' (incomplete)}
 *                    defaults: mono/test T Tall/Dwarf; incomplete R Red/Pink/White (snapdragon);
 *                    sexlinked H Normal/Haemophilic (alleles on X)
 *  genes     array   di-hybrid (and di test cross): two gene objects
 *                                       default [{R,Round,Wrinkled},{Y,Yellow,Green}]
 *  parents   array   [♀, ♂] genotypes as text: 'Tt','RrYy'; ABO 'IAi','IBIB' (or 'AO','BB');
 *                    sexlinked 'XHXh', 'XhY'                               default heterozygous × heterozygous
 *  lock      bool    parents cannot be changed                                              default false
 *  goal      object  {type:'ratio', target:'1:1', of:'phenotype'|'genotype'} — set the parents to get
 *                       this ratio (order of numbers does not matter)
 *                    {type:'predict', of:'phenotype'|'genotype'} — parents fixed, grid hidden; choose the ratio
 *                    {type:'possible', phenotype:'Haemophilic ♀'} — make a cross that can give this offspring
 *                       (phenotype labels as shown in the ratio box)
 *                    {type:'unknown'} — test mode: find the hidden genotype of the dominant parent
 *                    defaults: mono/di/incomplete/codominance → ratio (1:1 / 1:1:1:1 / 1:2:1 / 1:1:1:1);
 *                    test → unknown; sexlinked → possible 'Haemophilic ♀' (with that gene's rec label)
 *  pedigree  string|object  pedigree mode: 'ar' | 'ad' | 'xr' | 'xd' (built-in) or
 *                    {people:[{id:'I-1', sex:'m'|'f', aff:true|false, father?:'id', mother?:'id'}], answer?:'AR'}
 *                    people in each generation listed left→right, spouses next to each other.
 *                    answer is auto-worked out (most likely mode, allele frequency 0.01) if omitted. default 'ar'
 *  labels    object  {dominant, recessive, autosomal, xlinked, female, male} button words (may be Hindi)
 *  challenge string  challenge sentence (else generated)
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const gcd = (a, b) => b ? gcd(b, a % b) : a;
  const shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const PCOL = ['#8b5cf6', '#2ed3a5', '#ffc93c', '#ff6b6b', '#3b82f6', '#f472b6', '#14b8a6', '#a3a3c2', '#fb923c'];
  const PBG = ['#efe9ff', '#dcfaf1', '#fff4cf', '#ffe3e3', '#e0ebff', '#fde4f1', '#d5f5f1', '#eeeef5', '#ffe9d6'];

  const CSS = `
  .lb-punnett{color:#1b1f3a;font-weight:700;user-select:none;-webkit-user-select:none}
  .lb-punnett-ch{background:#f3efff;color:#4c2fb0;border-radius:14px;padding:7px 11px;font-size:13px;line-height:1.3;margin-bottom:6px}
  .lb-punnett-par{display:flex;gap:6px;align-items:stretch}
  .lb-punnett-pc{flex:1;background:#f7f8fd;border-radius:14px;padding:5px 6px;min-width:0}
  .lb-punnett-pc .h{font-size:11px;color:#6b7090;display:flex;justify-content:space-between;gap:4px;white-space:nowrap;overflow:hidden}
  .lb-punnett-pc .h b{color:#1b1f3a;overflow:hidden;text-overflow:ellipsis}
  .lb-punnett-al{display:flex;gap:4px;margin-top:3px}
  .lb-punnett-a{flex:1;min-width:0;height:40px;border-radius:11px;border:2px solid #d9dcf0;background:#fff;font:inherit;font-size:17px;font-weight:900;color:#1b1f3a;cursor:pointer;padding:0}
  .lb-punnett-a.d{background:#efe9ff;border-color:#c4b2ff;color:#4c2fb0}
  .lb-punnett-a.r{background:#dcfaf1;border-color:#9fe8d3;color:#0f7a5c}
  .lb-punnett-a.y{background:#eef0fb;border-color:#e3e6f6;color:#6b7090;cursor:default}
  .lb-punnett-a:disabled{cursor:default}
  .lb-punnett-x{align-self:center;font-size:18px;color:#9aa0c0;font-weight:900}
  .lb-punnett-gw{margin-top:6px;display:flex;justify-content:center}
  .lb-punnett-g{border-collapse:separate;border-spacing:3px;table-layout:fixed}
  .lb-punnett-g td,.lb-punnett-g th{text-align:center;border-radius:10px;font-weight:900;padding:0}
  .lb-punnett-g th{font-size:12px;color:#6b7090;background:#fff;border:2px dashed #d9dcf0}
  .lb-punnett-g th.c{border:none;font-size:10px;color:#9aa0c0}
  .lb-punnett-g td{transition:background .3s,transform .3s;line-height:1.05}
  .lb-punnett-g td small{display:block;font-size:8.5px;font-weight:800;opacity:.8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .lb-punnett-g td.pop{animation:lb-punnett-pop .35s ease}
  @keyframes lb-punnett-pop{0%{transform:scale(.6);opacity:0}100%{transform:scale(1);opacity:1}}
  .lb-punnett-rat{background:#f7f8fd;border-radius:14px;padding:5px 9px;margin-top:5px;font-size:11.5px;line-height:1.35;color:#6b7090}
  .lb-punnett-rat b{color:#1b1f3a}
  .lb-punnett-rat i{font-style:normal;display:inline-block;width:9px;height:9px;border-radius:3px;margin-right:3px;vertical-align:0}
  .lb-punnett-opts{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
  .lb-punnett-btn{flex:1 1 0;min-height:42px;padding:0 6px;border:none;border-radius:13px;font:inherit;font-weight:800;font-size:13px;cursor:pointer;color:#fff;background:#8b5cf6;box-shadow:0 3px 0 #5b33c9;white-space:nowrap}
  .lb-punnett-btn:active{transform:translateY(2px);box-shadow:none}
  .lb-punnett-btn.g{background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef}
  .lb-punnett-btn.on{background:#4c2fb0;box-shadow:0 3px 0 #2d1a73}
  .lb-punnett-btn.m{background:#2ed3a5;box-shadow:0 3px 0 #1a9c78}
  .lb-punnett-foot{display:flex;flex-wrap:wrap;align-items:center;column-gap:8px}
  .lb-punnett-foot .lb-punnett-opts{flex:1 1 100%}
  .lb-punnett-foot.inl .lb-punnett-opts{flex:0 0 auto;order:2}
  .lb-punnett-foot.inl .lb-punnett-msg{flex:1 1 0;order:1}
  .lb-punnett-msg{font-size:12px;color:#6b7090;min-height:16px;margin-top:5px;line-height:1.3}
  .lb-punnett-msg.good{color:#0f7a5c}.lb-punnett-msg.bad{color:#c94545}
  .lb-punnett-ped{display:block;width:100%;height:auto;background:#f7f8fd;border-radius:14px}
  .lb-punnett-ped text{font-family:inherit}
  .lb-punnett-ped .p{cursor:pointer}
  .lb-punnett-tg{display:flex;gap:5px;margin-top:6px}
  .lb-punnett-tg .lb-punnett-btn{font-size:12.5px;padding:0 6px}`;

  // ================================================================ PEDIGREE ENGINE
  const BUILTIN = {
    ar: [['I-1', 'm', 0], ['I-2', 'f', 0], ['II-1', 'm', 0, 'I-1', 'I-2'], ['II-2', 'f', 1, 'I-1', 'I-2'], ['II-3', 'm', 0, 'I-1', 'I-2'], ['II-4', 'f', 0],
      ['III-1', 'f', 0, 'II-3', 'II-4'], ['III-2', 'm', 1, 'II-3', 'II-4'], ['III-3', 'f', 0, 'II-3', 'II-4']],
    ad: [['I-1', 'm', 1], ['I-2', 'f', 0], ['II-1', 'm', 1, 'I-1', 'I-2'], ['II-2', 'f', 0, 'I-1', 'I-2'], ['II-3', 'f', 1, 'I-1', 'I-2'], ['II-4', 'm', 1],
      ['III-1', 'm', 0, 'II-4', 'II-3'], ['III-2', 'f', 1, 'II-4', 'II-3'], ['III-3', 'f', 1, 'II-4', 'II-3']],
    xr: [['I-1', 'm', 0], ['I-2', 'f', 0], ['II-1', 'm', 1, 'I-1', 'I-2'], ['II-2', 'm', 0, 'I-1', 'I-2'], ['II-3', 'f', 0, 'I-1', 'I-2'], ['II-4', 'm', 0],
      ['III-1', 'm', 1, 'II-4', 'II-3'], ['III-2', 'f', 0, 'II-4', 'II-3'], ['III-3', 'm', 0, 'II-4', 'II-3'], ['III-4', 'm', 1, 'II-4', 'II-3']],
    xd: [['I-1', 'm', 1], ['I-2', 'f', 0], ['II-1', 'f', 1, 'I-1', 'I-2'], ['II-2', 'm', 0, 'I-1', 'I-2'], ['II-3', 'f', 1, 'I-1', 'I-2'], ['II-4', 'm', 0],
      ['III-1', 'm', 1, 'II-4', 'II-3'], ['III-2', 'f', 0, 'II-4', 'II-3'], ['III-3', 'f', 1, 'II-4', 'II-3']]
  };
  const MODES = ['AD', 'AR', 'XD', 'XR'];
  const MODENAME = { AD: 'autosomal dominant', AR: 'autosomal recessive', XD: 'X-linked dominant', XR: 'X-linked recessive' };
  const Q = 0.01; // disease-allele frequency for founders
  function pedModel(people) {
    const byId = {}; people.forEach(x => byId[x.id] = x);
    people.forEach(x => { x.F = byId[x.father] || null; x.M = byId[x.mother] || null; if (!(x.F && x.M)) x.F = x.M = null; });
    // generation: founders start at 1, children one below their parents, marry-ins beside their spouse
    people.forEach(x => x._g = 1);
    for (let it = 0; it < 12; it++) people.forEach(x => {
      if (x.F) x._g = Math.max(x.F._g, x.M._g) + 1;
      else { const kid = people.find(k => k.F === x || k.M === x); const sp = kid ? (kid.F === x ? kid.M : kid.F) : null; if (sp && sp.F) x._g = sp._g; }
    });
    // order so parents come before children
    const order = people.slice().sort((a, b) => a._g - b._g);
    return { people, order, byId };
  }
  function genoOptions(x, mode) { return (mode[0] === 'X' && x.sex === 'm') ? [0, 1] : [0, 1, 2]; }
  function affected(x, k, mode) { const dom = mode[1] === 'D'; if (dom) return k >= 1; return (mode[0] === 'X' && x.sex === 'm') ? k === 1 : k === 2; }
  function prior(x, k, mode) {
    if (mode[0] === 'X' && x.sex === 'm') return k ? Q : 1 - Q;
    return k === 2 ? Q * Q : k === 1 ? 2 * Q * (1 - Q) : (1 - Q) * (1 - Q);
  }
  function trans(x, k, kf, km, mode) {
    const pm = km / 2; // mother passes disease allele
    if (mode[0] === 'X') {
      if (x.sex === 'm') return k ? pm : 1 - pm;
      const pf = kf; // father's single X
      return k === 2 ? pf * pm : k === 1 ? pf * (1 - pm) + (1 - pf) * pm : (1 - pf) * (1 - pm);
    }
    const pf = kf / 2;
    return k === 2 ? pf * pm : k === 1 ? pf * (1 - pm) + (1 - pf) * pm : (1 - pf) * (1 - pm);
  }
  function analyse(model, mode) { // returns {L, poss: Map id → Set(k)}
    const ord = model.order, G = {}, poss = {}; ord.forEach(x => poss[x.id] = new Set());
    let L = 0;
    (function rec(i, w) {
      if (i === ord.length) { L += w; ord.forEach(x => poss[x.id].add(G[x.id])); return; }
      const x = ord[i];
      for (const k of genoOptions(x, mode)) {
        if (affected(x, k, mode) !== !!x.aff) continue;
        const pr = x.F ? trans(x, k, G[x.F.id], G[x.M.id], mode) : prior(x, k, mode);
        if (pr <= 0) continue; G[x.id] = k; rec(i + 1, w * pr);
      }
    })(0, 1);
    return { L, poss };
  }
  function reasonAgainst(model, mode) {
    const P = model.people, kids = x => P.filter(k => k.F === x || k.M === x);
    const couples = []; P.forEach(k => { if (k.F && !couples.some(c => c[0] === k.F && c[1] === k.M)) couples.push([k.F, k.M]); });
    const id = x => x.id;
    if (mode[1] === 'R') for (const [f, m] of couples) if (f.aff && m.aff) { const u = kids(f).find(k => k.M === m && !k.aff); if (u) return `${id(f)} and ${id(m)} are both affected but ${id(u)} is not. Two affected parents (aa × aa) can only have affected children if the trait is recessive.`; }
    if (mode[1] === 'D') for (const [f, m] of couples) if (!f.aff && !m.aff) { const a = kids(f).find(k => k.M === m && k.aff); if (a) return `${id(a)} is affected but both parents are unaffected — a dominant trait would show in a parent.`; }
    if (mode === 'XR') { for (const x of P) if (x.sex === 'f' && x.aff && x.F && !x.F.aff) return `${id(x)} is an affected female, so for X-linked recessive her father (${id(x.F)}) must be affected — he is not.`;
      for (const x of P) if (x.sex === 'm' && !x.aff && x.M && x.M.aff) return `${id(x.M)} is an affected mother (XᵃXᵃ) — all her sons would be affected, but ${id(x)} is not.`; }
    if (mode === 'XD') { for (const x of P) if (x.sex === 'f' && !x.aff && x.F && x.F.aff) return `${id(x.F)} is an affected father; he gives his X to every daughter, so ${id(x)} would be affected.`;
      for (const x of P) if (x.sex === 'm' && x.aff && x.M && !x.M.aff) return `${id(x)} is an affected son; under X-linkage his X comes from his mother ${id(x.M)}, who is unaffected.`; }
    return 'No set of genotypes fits this pedigree under that mode.';
  }

  Labs.register('punnett', {
    title: 'Punnett & pedigree lab',
    subjects: ['biology', 'science'],
    render(host, p, api) {
      const MODESET = ['mono', 'di', 'test', 'incomplete', 'codominance', 'sexlinked', 'pedigree'];
      const mode = MODESET.includes(p.mode) ? p.mode : 'mono';
      const LB = Object.assign({ dominant: 'Dominant', recessive: 'Recessive', autosomal: 'Autosomal', xlinked: 'X-linked', female: '♀', male: '♂' }, (p.labels && typeof p.labels === 'object') ? p.labels : {});
      let won = false; const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(m); };
      const timers = []; const later = (f, ms) => timers.push(setTimeout(f, ms));
      const goal = (p.goal && typeof p.goal === 'object') ? p.goal : {};
      if (mode === 'pedigree') return renderPedigree();

      // ---------------------------------------------------------------- genes
      const G0 = { mono: { letter: 'T', dom: 'Tall', rec: 'Dwarf' }, test: { letter: 'T', dom: 'Tall', rec: 'Dwarf' }, incomplete: { letter: 'R', dom: 'Red', het: 'Pink', rec: 'White' }, sexlinked: { letter: 'H', dom: 'Normal', rec: 'Haemophilic' } };
      const fixGene = (g, d) => { g = Object.assign({}, d, g && typeof g === 'object' ? g : {}); g.letter = String(g.letter || d.letter).trim().charAt(0) || d.letter; return g; };
      let genes;
      const twoGenes = mode === 'di' || (mode === 'test' && Array.isArray(p.genes) && p.genes.length >= 2);
      if (twoGenes) { const gd = [{ letter: 'R', dom: 'Round', rec: 'Wrinkled' }, { letter: 'Y', dom: 'Yellow', rec: 'Green' }]; const gi = Array.isArray(p.genes) ? p.genes : []; genes = [fixGene(gi[0], gd[0]), fixGene(gi[1], gd[1])]; if (genes[0].letter.toLowerCase() === genes[1].letter.toLowerCase()) genes[1].letter = genes[0].letter.toUpperCase() === 'Y' ? 'R' : 'Y'; }
      else if (mode !== 'codominance') genes = [fixGene(p.gene, G0[mode] || G0.mono)];
      const U = g => g.letter.toUpperCase(), Lw = g => g.letter.toLowerCase();
      const isX = mode === 'sexlinked', isABO = mode === 'codominance';
      // allele codes: 1 dominant / 0 recessive; ABO 'A','B','O'; sexlinked father locus [k,'Y']
      const nL = isABO ? 1 : genes.length;
      function parse(str, who) {
        str = String(str || '');
        if (isABO) { const s = str.replace(/I\s*A|Iᴬ/g, 'A').replace(/I\s*B|Iᴮ/g, 'B').replace(/i|O|o/g, 'O').replace(/[^ABO]/g, ''); return s.length >= 2 ? [[s[0], s[1]]] : null; }
        if (isX) { const xs = [...str.matchAll(/X\s*\^?\s*([A-Za-z])/g)].map(m => m[1] === U(genes[0]) ? 1 : 0); if (who === 1) return xs.length >= 1 ? [[xs[0], 'Y']] : null; return xs.length >= 2 ? [[xs[0], xs[1]]] : null; }
        const out = genes.map(g => [...str].filter(c => c.toLowerCase() === Lw(g)).map(c => c === U(g) ? 1 : 0));
        return out.every(a => a.length >= 2) ? out.map(a => a.slice(0, 2)) : null;
      }
      const dflt = who => isABO ? (who ? [['B', 'B']] : [['A', 'A']]) : isX ? (who ? [[1, 'Y']] : [[1, 0]]) : genes.map(() => [1, 0]);
      const P0 = Array.isArray(p.parents) ? p.parents : [];
      let par = [parse(P0[0], 0) || dflt(0), parse(P0[1], 1) || dflt(1)];
      if (mode === 'test') par[1] = genes.map(() => [0, 0]);
      const lock = !!p.lock;
      // ---------------------------------------------------------------- naming
      const alHTML = (a, li) => {
        if (isABO) return a === 'O' ? 'i' : 'I<sup>' + a + '</sup>';
        if (isX) return a === 'Y' ? 'Y' : 'X<sup>' + (a ? U(genes[0]) : Lw(genes[0])) + '</sup>';
        return a ? U(genes[li]) : Lw(genes[li]);
      };
      const sortLocus = l => isABO ? l.slice().sort((x, y) => 'ABO'.indexOf(x) - 'ABO'.indexOf(y)) : isX ? (l[1] === 'Y' ? l : l.slice().sort((x, y) => y - x)) : l.slice().sort((x, y) => y - x);
      const genoHTML = g => g.map((l, li) => sortLocus(l).map(a => alHTML(a, li)).join('')).join('');
      function pheno(g, sex) { // returns label
        if (isABO) { const s = new Set(g[0]); return s.has('A') && s.has('B') ? 'AB' : s.has('A') ? 'A' : s.has('B') ? 'B' : 'O'; }
        if (isX) { const gn = genes[0]; if (sex === 'm') return (g[0][0] ? gn.dom : gn.rec) + ' ' + LB.male; const k = g[0][0] + g[0][1]; return (k === 2 ? gn.dom : k === 1 ? 'Carrier' : gn.rec) + ' ' + LB.female; }
        if (mode === 'incomplete') { const k = g[0][0] + g[0][1]; const gn = genes[0]; return k === 2 ? gn.dom : k === 1 ? (gn.het || 'Intermediate') : gn.rec; }
        return g.map((l, li) => (l[0] || l[1]) ? genes[li].dom : genes[li].rec).join(' ');
      }
      const phenoOrder = () => { // canonical order of phenotype labels
        if (isABO) return ['A', 'B', 'AB', 'O'].map(x => x);
        if (isX) { const gn = genes[0]; return [gn.dom + ' ' + LB.female, 'Carrier ' + LB.female, gn.rec + ' ' + LB.female, gn.dom + ' ' + LB.male, gn.rec + ' ' + LB.male]; }
        if (mode === 'incomplete') return [genes[0].dom, genes[0].het || 'Intermediate', genes[0].rec];
        if (genes.length === 2) return [[1, 1], [1, 0], [0, 1], [0, 0]].map(([a, b]) => (a ? genes[0].dom : genes[0].rec) + ' ' + (b ? genes[1].dom : genes[1].rec));
        return [genes[0].dom, genes[0].rec];
      };
      const phLabel = l => isABO ? 'Blood group ' + l : l;
      // ---------------------------------------------------------------- crossing
      function gametes(pg) {
        let out = [[]]; pg.forEach(l => { const n = []; out.forEach(o => l.forEach(a => n.push(o.concat([a])))); out = n; }); return out;
      }
      function cross() {
        const gm = gametes(par[0]), gf = gametes(par[1]), cells = [];
        gm.forEach(a => gf.forEach(b => { const g = a.map((x, i) => [x, b[i]]); const sex = isX ? (b[0] === 'Y' ? 'm' : 'f') : null; if (isX && sex === 'm') g[0] = [a[0], 'Y']; cells.push({ g, sex, html: genoHTML(g), ph: pheno(g, sex) }); }));
        const order = phenoOrder();
        const cnt = (key) => { const m = new Map(); cells.forEach(c => m.set(c[key], (m.get(c[key]) || 0) + 1)); return m; };
        const phm = cnt('ph'), gtm = cnt('html');
        const phList = order.filter(o => phm.has(o)).map(o => [o, phm.get(o)]);
        const gOf = {}; cells.forEach(c => gOf[c.html] = c);
        const gtList = [...gtm.entries()].sort((x, y) => genoRank(gOf[y[0]]) - genoRank(gOf[x[0]]));
        return { gm, gf, cells, phList, gtList };
      }
      const genoRank = c => { // order: dominant-first per locus; ABO A,B,AB,O; X-linked females first
        if (isABO) { const k = sortLocus(c.g[0]).join(''); return -['AA', 'AO', 'BB', 'BO', 'AB', 'OO'].indexOf(k); }
        if (isX) { const k = c.sex === 'm' ? c.g[0][0] : c.g[0][0] + c.g[0][1]; return (c.sex === 'm' ? 0 : 10) + k; }
        return c.g.reduce((a, l, li) => a + (l[0] + l[1]) * Math.pow(3, c.g.length - 1 - li), 0); };
      const reduce = list => { const g = list.reduce((a, [, n]) => gcd(a, n), 0) || 1; return list.map(([k, n]) => [k, n / g]); };
      const ratioNums = s => String(s).split(/[:∶]/).map(x => parseInt(x, 10)).filter(x => x > 0);
      const sameRatio = (nums, list) => { const a = nums.slice().sort((x, y) => x - y), r = reduce(list).map(x => x[1]).sort((x, y) => x - y); const g = a.reduce(gcd, 0) || 1; return a.length === r.length && a.every((v, i) => v / g === r[i]); };
      const phWords = list => list.length === 1 ? 'all ' + phLabel(list[0][0]) : reduce(list).map(([k, n]) => n + ' ' + phLabel(k)).join(' : ');
      const numStr = list => list.length === 1 ? '1 (all alike)' : reduce(list).map(x => x[1]).join(' : ');

      // ---------------------------------------------------------------- goals
      let gtype = ['ratio', 'predict', 'possible', 'unknown'].includes(goal.type) ? goal.type : null;
      if (!gtype) gtype = mode === 'test' ? 'unknown' : isX ? 'possible' : 'ratio';
      if (gtype === 'unknown' && mode !== 'test') gtype = 'ratio';
      const of = goal.of === 'genotype' ? 'genotype' : 'phenotype';
      const target = gtype === 'ratio' ? (ratioNums(goal.target).length ? ratioNums(goal.target) : (isABO ? [1, 1, 1, 1] : mode === 'incomplete' ? [1, 1] : nL === 2 ? [1, 1, 1, 1] : [1, 1])) : null;
      const wantPh = gtype === 'possible' ? String(goal.phenotype || (isX ? genes[0].rec + ' ' + LB.female : isABO ? 'O' : genes[0].rec)) : null;
      let hidden = null, predictLocked = gtype === 'predict' || gtype === 'unknown', revealed = !predictLocked;
      if (gtype === 'unknown') { // hidden dominant-phenotype genotype
        const opts = nL === 2 ? [[[1, 1], [1, 1]], [[1, 0], [1, 1]], [[1, 1], [1, 0]], [[1, 0], [1, 0]]] : [[[1, 1]], [[1, 0]]];
        hidden = opts[Math.floor(Math.random() * opts.length)]; par[0] = hidden;
      }
      const editable = who => !lock && gtype !== 'predict' && gtype !== 'unknown' && !(mode === 'test' && who === 1);
      let challenge = p.challenge ? String(p.challenge) : '';
      if (!challenge) {
        if (gtype === 'ratio') challenge = `Change the parents' alleles to get a ${target.join(' : ')} ${of} ratio in the offspring.`;
        else if (gtype === 'predict') challenge = `Predict the ${of} ratio of this cross, then see the Punnett square.`;
        else if (gtype === 'possible') challenge = `Set the parents so that a ${wantPh} child is possible.`;
        else challenge = `Test cross: the ${nL === 2 ? genes[0].dom + ' ' + genes[1].dom : genes[0].dom} parent's genotype is hidden. Read the offspring and work it out.`;
      }

      // ---------------------------------------------------------------- DOM
      host.innerHTML = `<style>${CSS}</style><div class="lb-punnett">
        <div class="lb-punnett-ch">🎯 Challenge: ${esc(challenge)}</div>
        <div class="lb-punnett-par"><div class="lb-punnett-pc" data-w="0"></div><div class="lb-punnett-x">×</div><div class="lb-punnett-pc" data-w="1"></div></div>
        <div class="lb-punnett-gw"><table class="lb-punnett-g"></table></div>
        <div class="lb-punnett-rat"></div>
        <div class="lb-punnett-foot"><div class="lb-punnett-opts"></div><div class="lb-punnett-msg"></div></div></div>`;
      const root = host.querySelector('.lb-punnett'), $ = s => root.querySelector(s);
      const grid = $('.lb-punnett-g'), rat = $('.lb-punnett-rat'), opts = $('.lb-punnett-opts'), msg = $('.lb-punnett-msg');
      const setMsg = (t, c) => { msg.innerHTML = t; msg.className = 'lb-punnett-msg' + (c ? ' ' + c : ''); };
      const phCol = {}; phenoOrder().forEach((o, i) => phCol[o] = i);
      if (mode === 'incomplete') { phCol[genes[0].dom] = 3; phCol[genes[0].het || 'Intermediate'] = 5; phCol[genes[0].rec] = 7; }

      function drawParents() {
        [0, 1].forEach(w => {
          const el = root.querySelector(`[data-w="${w}"]`), g = par[w];
          const sexS = w === 0 ? LB.female : LB.male;
          let btns = '';
          g.forEach((l, li) => l.forEach((a, ai) => {
            const yy = a === 'Y';
            const cls = yy ? 'y' : isABO ? (a === 'O' ? 'r' : 'd') : (a ? 'd' : 'r');
            const hide = gtype === 'unknown' && w === 0 && !(ai === 0);
            btns += `<button class="lb-punnett-a ${hide ? 'y' : cls}" data-w="${w}" data-l="${li}" data-a="${ai}" ${yy || !editable(w) ? 'disabled' : ''}>${hide ? '?' : alHTML(a, li)}</button>`;
          }));
          const phT = (gtype === 'unknown' && w === 0) ? pheno(g, 'f') : pheno(g, isX ? (w ? 'm' : 'f') : null);
          el.innerHTML = `<div class="h"><span>${sexS} <b>${(gtype === 'unknown' && w === 0) ? '?' : genoHTML(g)}</b></span><b style="color:#4c2fb0">${esc(isABO ? 'Group ' + phT : phT)}</b></div><div class="lb-punnett-al">${btns}</div>`;
        });
      }
      let lastKey = '';
      function drawGrid(res, anim) {
        const n = res.gf.length, m = res.gm.length, big = n <= 2;
        const cw = big ? 92 : 66, ch = big ? 42 : 29;
        const gHead = (gm, li) => gm.map((a, i) => alHTML(a, i)).join('');
        let h = `<tr><th class="c" style="width:${big ? 46 : 40}px;height:24px">${LB.female}\\${LB.male}</th>${res.gf.map(gf => `<th style="width:${cw}px">${gHead(gf)}</th>`).join('')}</tr>`;
        res.gm.forEach((gm, i) => {
          h += `<tr><th style="height:${ch}px">${gHead(gm)}</th>`;
          for (let j = 0; j < n; j++) {
            const c = res.cells[i * n + j], k = phCol[c.ph] || 0;
            if (!revealed) { h += `<td style="background:#eef0fb;color:#c3c7da;height:${ch}px">?</td>`; continue; }
            const showG = !(gtype === 'unknown');
            h += `<td class="${anim ? 'pop' : ''}" style="background:${PBG[k]};color:#1b1f3a;height:${ch}px;font-size:${big ? 16 : 11.5}px;line-height:1;animation-delay:${(i * n + j) * (big ? 70 : 25)}ms;animation-fill-mode:both">${showG ? c.html : ''}<small style="color:${PCOL[k]};filter:brightness(.75)">${esc(isABO ? c.ph : c.ph)}</small></td>`;
          }
          h += '</tr>';
        });
        grid.innerHTML = h;
      }
      function drawRatio(res) {
        if (!revealed) { rat.innerHTML = gtype === 'unknown' ? 'Press <b>Test cross</b> to breed it with the recessive parent.' : `Gametes: ${LB.female} ${[...new Set(res.gm.map(g => g.map((a, i) => alHTML(a, i)).join('')))].join(', ')} · ${LB.male} ${[...new Set(res.gf.map(g => g.map((a, i) => alHTML(a, i)).join('')))].join(', ')}`; return; }
        const ph = reduce(res.phList), gt = reduce(res.gtList);
        const phS = ph.map(([k, n]) => `<i style="background:${PCOL[phCol[k] || 0]}"></i><b>${n}</b> ${esc(phLabel(k))}`).join(' : ');
        const gtS = gtype === 'unknown' ? '<span>hidden (you only see what the offspring look like)</span>' : gt.map(([k, n]) => `<b>${n}</b> ${k}`).join(' : ');
        rat.innerHTML = `<div>Phenotype: ${phS}</div><div>Genotype: ${gtS}</div>`;
      }
      let touched = false;
      function check(res) {
        if (gtype === 'ratio') {
          const list = of === 'genotype' ? res.gtList : res.phList;
          if (sameRatio(target, list) && !touched) setMsg(`This starting cross already gives ${numStr(list)}. Change the alleles and build it yourself!`);
          else if (sameRatio(target, list)) { setMsg(`✓ ${of === 'genotype' ? 'Genotype' : 'Phenotype'} ratio ${numStr(list)}!`, 'good'); if (touched) later(() => winOnce(`Parents ${genoHTML(par[0]).replace(/<[^>]+>/g, '')} × ${genoHTML(par[1]).replace(/<[^>]+>/g, '')} give ${numStr(list)} (${of}).`), 450); }
          else setMsg(`Now ${numStr(list)} (${of}). Target ${target.join(' : ')}. Tap the alleles to change a parent.`);
        } else if (gtype === 'possible') {
          const c = res.cells.filter(x => x.ph.toLowerCase() === wantPh.toLowerCase()).length;
          if (c && !touched) setMsg(`This starting cross can already give a ${wantPh} child. Change the alleles and find another way!`);
          else if (c) { setMsg(`✓ ${c} of ${res.cells.length} boxes are ${wantPh}.`, 'good'); if (touched) later(() => winOnce(`${genoHTML(par[0]).replace(/<sup>/g, '').replace(/<\/sup>/g, '')} × ${genoHTML(par[1]).replace(/<sup>/g, '').replace(/<\/sup>/g, '')}: probability ${c}/${res.cells.length} of a ${wantPh} child.`), 450); }
          else setMsg(`No ${wantPh} child possible yet. Tap the alleles to change a parent.`);
        }
      }
      function refresh(anim) {
        const res = cross(); drawParents(); const key = JSON.stringify(par) + revealed;
        drawGrid(res, anim && key !== lastKey); lastKey = key; drawRatio(res);
        if (revealed) check(res);
        return res;
      }
      // predict / unknown option buttons
      function setupOpts() {
        if (gtype === 'predict') {
          const res = cross(), list = of === 'genotype' ? res.gtList : res.phList, right = numStr(list);
          const pool = ['3 : 1', '1 : 1', '1 : 2 : 1', '9 : 3 : 3 : 1', '1 : 1 : 1 : 1', '1', '3 : 3 : 1 : 1', '15 : 1', '9 : 7'].concat(right.split(':').length > 5 ? ['1 : 2 : 1 : 2 : 4 : 2 : 1 : 2 : 1'] : []).filter(x => x !== right && (x.split(':').length === right.split(':').length || Math.random() < 0.5));
          const choices = shuffle([right, ...shuffle(pool).slice(0, 3)]);
          opts.innerHTML = choices.map(c => `<button class="lb-punnett-btn g" data-o="${c}">${c === '1' ? 'all alike' : c}</button>`).join('');
          opts.querySelectorAll('[data-o]').forEach(b => b.onclick = () => {
            if (b.dataset.o === right) { api.sfx('coin'); revealed = true; opts.innerHTML = ''; refresh(true); setMsg(`✓ Correct — ${of} ratio ${right}.`, 'good'); later(() => winOnce(`Predicted ${right}! Each box of the Punnett square is equally likely.`), 700); }
            else { api.sfx('wrong'); b.disabled = true; b.style.opacity = .4; setMsg('Not that one. List the gametes of each parent first, then combine them.', 'bad'); }
          });
        } else if (gtype === 'unknown') {
          const optsG = nL === 2 ? [[[1, 1], [1, 1]], [[1, 0], [1, 1]], [[1, 1], [1, 0]], [[1, 0], [1, 0]]] : [[[1, 1]], [[1, 0]]];
          opts.innerHTML = `<button class="lb-punnett-btn m" data-t style="flex-basis:100%">🧪 Test cross with ${genoHTML(par[1])}</button>`;
          opts.querySelector('[data-t]').onclick = () => {
            api.sfx('tap'); revealed = true; refresh(true);
            opts.innerHTML = `<div style="flex-basis:100%;font-size:12px;color:#6b7090">The hidden parent is…</div>` + optsG.map((g, i) => `<button class="lb-punnett-btn g" data-u="${i}">${genoHTML(g)}</button>`).join('');
            opts.querySelectorAll('[data-u]').forEach(b => b.onclick = () => {
              const g = optsG[+b.dataset.u];
              if (JSON.stringify(g) === JSON.stringify(hidden)) { api.sfx('coin'); setMsg(`✓ It is ${genoHTML(hidden)}.`, 'good'); gtype = 'done'; drawParents(); later(() => winOnce(`The test cross gave ${phWords(cross().phList)} — so the parent is ${genoHTML(hidden).replace(/<[^>]+>/g, '')}.`), 500); }
              else { api.sfx('wrong'); b.disabled = true; b.style.opacity = .4; setMsg(`If it were ${genoHTML(g)}, the test cross would give ${(() => { const keep = par[0]; par[0] = g; const r = phWords(cross().phList); par[0] = keep; return r; })()} — compare with what you see.`, 'bad'); }
            });
          };
        }
        if (gtype === 'ratio' || gtype === 'possible') { root.querySelector('.lb-punnett-foot').classList.add('inl'); opts.innerHTML = `<button class="lb-punnett-btn g" data-reset style="flex:0 0 auto;min-height:40px">↺ Reset</button>`; }
        const rb = opts.querySelector('[data-reset]'); if (rb) rb.onclick = () => { api.sfx('tap'); par = [parse(P0[0], 0) || dflt(0), parse(P0[1], 1) || dflt(1)]; if (mode === 'test') par[1] = genes.map(() => [0, 0]); if (won) { won = false; api.resetWin && api.resetWin(); } refresh(true); };
      }
      root.addEventListener('click', onClick);
      function onClick(e) {
        const b = e.target.closest('.lb-punnett-a'); if (!b || b.disabled) return;
        const w = +b.dataset.w, li = +b.dataset.l, ai = +b.dataset.a; if (!editable(w)) return;
        const cur = par[w][li][ai];
        par[w][li][ai] = isABO ? ({ A: 'B', B: 'O', O: 'A' })[cur] : (cur ? 0 : 1);
        api.sfx('tap'); touched = true; refresh(true);
      }
      setupOpts(); refresh(true);
      if (gtype === 'predict') setMsg('Parents are fixed. Work out the gametes, then pick the ratio.');
      return () => { timers.forEach(clearTimeout); root.removeEventListener('click', onClick); };

      // ================================================================ PEDIGREE
      function renderPedigree() {
        let src = p.pedigree, people, answer = null;
        if (src && typeof src === 'object' && Array.isArray(src.people)) {
          people = src.people.filter(x => x && x.id).map(x => ({ id: String(x.id), sex: x.sex === 'f' ? 'f' : 'm', aff: !!x.aff, father: x.father, mother: x.mother }));
          if (MODES.includes(String(src.answer || '').toUpperCase())) answer = String(src.answer).toUpperCase();
        }
        if (!people || people.length < 2) { const key = BUILTIN[String(src || '').toLowerCase()] ? String(src).toLowerCase() : 'ar'; people = BUILTIN[key].map(([id, sex, aff, father, mother]) => ({ id, sex, aff: !!aff, father, mother })); }
        const model = pedModel(people);
        const R = {}; MODES.forEach(m => R[m] = analyse(model, m));
        const best = Math.max(...MODES.map(m => R[m].L));
        const accepted = answer ? [answer] : MODES.filter(m => R[m].L > 0 && R[m].L >= best * 0.5);
        if (!accepted.length) accepted.push('AR');
        let challenge = p.challenge ? String(p.challenge) : 'Read the pedigree. Is the trait dominant or recessive? Autosomal or X-linked?';
        // layout
        const gens = [...new Set(people.map(x => x._g))].sort((a, b) => a - b);
        const W = 360, RH = 54, H = gens.length * RH + 6, S = 20;
        const pos = {};
        gens.forEach((g, gi) => { const row = people.filter(x => x._g === g); row.forEach((x, i) => pos[x.id] = { x: 34 + (i + 0.5) * (W - 44) / row.length, y: 18 + gi * RH }); });
        host.innerHTML = `<style>${CSS}</style><div class="lb-punnett">
          <div class="lb-punnett-ch">🎯 Challenge: ${esc(challenge)}</div>
          <svg class="lb-punnett-ped" viewBox="0 0 ${W} ${H}"></svg>
          <div class="lb-punnett-rat lb-punnett-pinfo">Tap a person for details. Pick a mode, then tap people to see their possible genotypes.</div>
          <div class="lb-punnett-tg"><button class="lb-punnett-btn g" data-d="D">${esc(LB.dominant)}</button><button class="lb-punnett-btn g" data-d="R">${esc(LB.recessive)}</button></div>
          <div class="lb-punnett-tg"><button class="lb-punnett-btn g" data-x="A">${esc(LB.autosomal)}</button><button class="lb-punnett-btn g" data-x="X">${esc(LB.xlinked)}</button><button class="lb-punnett-btn m" data-c style="flex:0 0 auto">Check</button></div>
          <div class="lb-punnett-msg"></div></div>`;
        const root = host.querySelector('.lb-punnett'), svg = root.querySelector('svg'), info = root.querySelector('.lb-punnett-pinfo'), msg = root.querySelector('.lb-punnett-msg');
        const setMsg = (t, c) => { msg.innerHTML = t; msg.className = 'lb-punnett-msg' + (c ? ' ' + c : ''); };
        let dSel = null, xSel = null, sel = null;
        const modeSel = () => dSel && xSel ? xSel + dSel : null;
        const gtxt = (x, k, m) => {
          const dz = m[1] === 'D', A = dz ? 'A' : 'a', N = dz ? 'a' : 'A'; // A/a with disease allele first in mind
          if (m[0] === 'X') { const xa = 'X<tspan baseline-shift="super" font-size="70%">' + A + '</tspan>', xn = 'X<tspan baseline-shift="super" font-size="70%">' + N + '</tspan>'; if (x.sex === 'm') return (k ? xa : xn) + 'Y'; return k === 2 ? xa + xa : k === 1 ? (dz ? xa + xn : xn + xa) : xn + xn; }
          return k === 2 ? A + A : k === 1 ? 'Aa' : N + N;
        };
        function draw() {
          let s = '';
          gens.forEach((g, gi) => s += `<text x="8" y="${18 + gi * RH + 4}" font-size="11" font-weight="900" fill="#9aa0c0">${['I', 'II', 'III', 'IV', 'V'][gi] || gi + 1}</text>`);
          const couples = []; people.forEach(k => { if (k.F && !couples.some(c => c[0] === k.F && c[1] === k.M)) couples.push([k.F, k.M]); });
          couples.forEach(([f, m]) => {
            const a = pos[f.id], b = pos[m.id], mx = (a.x + b.x) / 2, y = a.y;
            s += `<line x1="${a.x}" y1="${y}" x2="${b.x}" y2="${b.y}" stroke="#6b7090" stroke-width="1.6"/>`;
            const kids = people.filter(k => k.F === f && k.M === m); if (!kids.length) return;
            const ky = pos[kids[0].id].y - S / 2 - 12, xs = kids.map(k => pos[k.id].x);
            s += `<line x1="${mx}" y1="${y}" x2="${mx}" y2="${ky}" stroke="#6b7090" stroke-width="1.6"/><line x1="${Math.min(mx, ...xs)}" y1="${ky}" x2="${Math.max(mx, ...xs)}" y2="${ky}" stroke="#6b7090" stroke-width="1.6"/>`;
            kids.forEach(k => s += `<line x1="${pos[k.id].x}" y1="${ky}" x2="${pos[k.id].x}" y2="${pos[k.id].y - S / 2}" stroke="#6b7090" stroke-width="1.6"/>`);
          });
          const m = modeSel();
          people.forEach(x => {
            const { x: cx, y: cy } = pos[x.id], fillc = x.aff ? '#4c2fb0' : '#fff', on = sel === x;
            const shape = x.sex === 'm' ? `<rect x="${cx - S / 2}" y="${cy - S / 2}" width="${S}" height="${S}" rx="3" fill="${fillc}" stroke="#1b1f3a" stroke-width="2"/>` : `<circle cx="${cx}" cy="${cy}" r="${S / 2 + 1}" fill="${fillc}" stroke="#1b1f3a" stroke-width="2"/>`;
            let lab = `<text x="${cx}" y="${cy + S / 2 + 11}" font-size="9" text-anchor="middle" fill="#6b7090" font-weight="800">${x.id}</text>`;
            if (on && m) { const ps = [...R[m].poss[x.id]]; lab = `<text x="${cx}" y="${cy + S / 2 + 12}" font-size="10" text-anchor="middle" fill="${ps.length ? '#0f7a5c' : '#c94545'}" font-weight="900">${ps.length ? ps.sort((a, b) => b - a).map(k => gtxt(x, k, m)).join(' / ') : '✗'}</text>`; }
            s += `<g class="p" data-id="${x.id}">${on ? `<circle cx="${cx}" cy="${cy}" r="${S / 2 + 7}" fill="#ffc93c" opacity=".55"/>` : ''}${shape}${lab}<rect x="${cx - 22}" y="${cy - 22}" width="44" height="44" fill="transparent"/></g>`;
          });
          svg.innerHTML = s;
        }
        function showInfo() {
          if (!sel) return;
          const m = modeSel(), who = `<b>${sel.id}</b>: ${sel.aff ? 'affected' : 'unaffected'} ${sel.sex === 'm' ? 'male' : 'female'}${sel.F ? ` (parents ${sel.F.id} × ${sel.M.id})` : ''}`;
          if (!m) { info.innerHTML = who + '. Choose a mode below to see possible genotypes.'; return; }
          const ps = [...R[m].poss[sel.id]];
          info.innerHTML = who + `. If ${MODENAME[m]}: ${ps.length ? '<b>' + ps.sort((a, b) => b - a).map(k => gtxt(sel, k, m).replace(/<tspan[^>]*>/g, '<sup>').replace(/<\/tspan>/g, '</sup>')).join(' or ') + '</b>' : '<b style="color:#c94545">impossible</b> — no genotype fits'}.`;
        }
        svg.addEventListener('click', onTap);
        function onTap(e) { const g = e.target.closest('.p'); if (!g) return; sel = model.byId[g.dataset.id]; api.sfx('tap'); draw(); showInfo(); }
        const tgl = () => { root.querySelectorAll('[data-d]').forEach(b => b.classList.toggle('on', b.dataset.d === dSel)); root.querySelectorAll('[data-x]').forEach(b => b.classList.toggle('on', b.dataset.x === xSel)); root.querySelectorAll('[data-d],[data-x]').forEach(b => b.classList.toggle('g', !b.classList.contains('on'))); draw(); showInfo(); };
        root.querySelectorAll('[data-d]').forEach(b => b.onclick = () => { dSel = b.dataset.d; api.sfx('tap'); tgl(); });
        root.querySelectorAll('[data-x]').forEach(b => b.onclick = () => { xSel = b.dataset.x; api.sfx('tap'); tgl(); });
        root.querySelector('[data-c]').onclick = () => {
          const m = modeSel(); if (!m) { setMsg('Choose both: dominant/recessive AND autosomal/X-linked.', 'bad'); api.sfx('hmm'); return; }
          if (accepted.includes(m)) { api.sfx('coin'); setMsg(`✓ ${MODENAME[m]}!`, 'good'); winOnce(`This pedigree shows ${MODENAME[m]} inheritance.` + (m === 'AR' ? ' Unaffected parents had an affected child, so both are carriers (Aa).' : m === 'AD' ? ' Affected parents had an unaffected child, and affected fathers have unaffected daughters.' : m === 'XR' ? ' Mostly males are affected, through carrier mothers; fathers never pass it to sons.' : ' Affected fathers pass it to all daughters and no sons.')); return; }
          api.sfx('wrong');
          if (R[m].L === 0) setMsg('✗ Impossible: ' + reasonAgainst(model, m), 'bad');
          else { const bm = accepted[0], f = R[bm].L / R[m].L; setMsg(`✗ ${MODENAME[m]} is possible, but ${f > 50 ? 'far' : 'about ' + Math.round(f) + '×'} less likely — it needs ${m[1] === 'R' ? 'unrelated carriers marrying into the family' : 'many chance events'}. Look for a better fit.`, 'bad'); }
        };
        draw();
        return () => { svg.removeEventListener('click', onTap); };
      }
    },
    example: {
      mode: 'mono', gene: { letter: 'T', dom: 'Tall', rec: 'Dwarf' }, parents: ['Tt', 'Tt'],
      goal: { type: 'ratio', target: '1:1', of: 'phenotype' },
      challenge: 'Mendel\'s peas: the F₂ is 3 Tall : 1 Dwarf. Change the parents to get 1 Tall : 1 Dwarf.'
    },
    examples: [
      { mode: 'di', genes: [{ letter: 'R', dom: 'Round', rec: 'Wrinkled' }, { letter: 'Y', dom: 'Yellow', rec: 'Green' }], parents: ['RrYy', 'RrYy'], lock: true,
        goal: { type: 'predict', of: 'phenotype' }, challenge: 'Class 12 · Dihybrid F₁ self-cross RrYy × RrYy: predict the phenotypic ratio.' },
      { mode: 'codominance', parents: ['IAIA', 'IBIB'], goal: { type: 'ratio', target: '1:1:1:1', of: 'phenotype' },
        challenge: 'ABO blood groups (Iᴬ, Iᴮ codominant, i recessive): which parents can have children of all four groups?' },
      { mode: 'pedigree', pedigree: 'xr', labels: { dominant: 'प्रभावी', recessive: 'अप्रभावी' },
        challenge: 'Pedigree analysis: decide the mode of inheritance.' }
    ]
  });
})();
