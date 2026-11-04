/* StudyVerse Concept Lab: placevalue — "Abacus & place-value builder"
 * The child adds / removes beads (abacus) or base-ten blocks and watches the number, its expanded form
 * and its number name change live. 10 beads on a rod regroup into 1 bead on the next rod.
 *
 * PARAMS (all optional)
 *  name          type            meaning                                                          default
 *  places        number|string   how many columns: 1-9, or 'tens' | 'hundreds' | 'thousands' |
 *                                'tenthousands' | 'lakhs' | 'tenlakhs' | 'crores' | 'tencrores'    6 ('lakhs')
 *                                (international names also work: 'hundredthousands', 'millions' …)
 *  view          string          'abacus' (rods & beads) or 'blocks' (hundreds flats, tens rods,
 *                                ones cubes — only up to 3 places)                                'abacus'
 *  system        string          comma style to start with: 'indian' (3,45,072) or 'international'
 *                                (345,072)                                                         'indian'
 *  toggle        boolean         show the Indian ⇄ International button (only for 4+ places)      true
 *  target        number          number the child must build                                      auto
 *  ask           string          how the target is shown: 'number' | 'words' | 'expanded'         'number'
 *  start         number          number already on the abacus at the start                        0
 *  carry         boolean         a 10th bead regroups into the next place (and borrowing back)    true
 *  showWords     boolean         show the number name live                                        true
 *  showExpanded  boolean         show the expanded form live                                      true
 *  newChallenge  boolean         show the "New" button                                             true
 *  challenge     string          challenge text (any language); default generated                 auto
 */
(function () {
  const T = 'placevalue';
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const NAMES = { ones: 1, tens: 2, hundreds: 3, thousands: 4, tenthousands: 5, lakhs: 6, hundredthousands: 6, tenlakhs: 7, millions: 7, crores: 8, tenmillions: 8, tencrores: 9, hundredmillions: 9 };
  const ABBR = { indian: ['O', 'T', 'H', 'Th', 'TTh', 'L', 'TL', 'C', 'TC'], international: ['O', 'T', 'H', 'Th', 'TTh', 'HTh', 'M', 'TM', 'HM'] };
  const FULL = { indian: ['ones', 'tens', 'hundreds', 'thousands', 'ten thousands', 'lakhs', 'ten lakhs', 'crores', 'ten crores'], international: ['ones', 'tens', 'hundreds', 'thousands', 'ten thousands', 'hundred thousands', 'millions', 'ten millions', 'hundred millions'] };
  const SING = { indian: ['one', 'ten', 'hundred', 'thousand', 'ten thousand', 'lakh', 'ten lakh', 'crore', 'ten crore'], international: ['one', 'ten', 'hundred', 'thousand', 'ten thousand', 'hundred thousand', 'million', 'ten million', 'hundred million'] };
  // period of each place (0 = ones period …) and colours
  const PERIOD = { indian: [0, 0, 0, 1, 1, 2, 2, 3, 3], international: [0, 0, 0, 1, 1, 1, 2, 2, 2] };
  const PNAME = { indian: ['Ones', 'Thousands', 'Lakhs', 'Crores'], international: ['Ones', 'Thousands', 'Millions'] };
  const PCOL = ['#2ed3a5', '#3b82f6', '#8b5cf6', '#ff6b6b'];
  const PDARK = ['#1a9c78', '#2563c9', '#6a3fd0', '#d04545'];
  const PLIGHT = ['#e3fbf3', '#e6f0ff', '#f1ebff', '#ffeaea'];

  function fmtNum(n, sys) {
    const s = String(Math.abs(Math.round(n)));
    let out;
    if (sys === 'international') out = s.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    else { if (s.length <= 3) out = s; else { const last = s.slice(-3); const rest = s.slice(0, -3); out = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ',') + ',' + last; } }
    return (n < 0 ? '-' : '') + out;
  }
  const W1 = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'];
  const W10 = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];
  const two = n => n < 20 ? W1[n] : W10[Math.floor(n / 10)] + (n % 10 ? '-' + W1[n % 10] : '');
  const three = n => { const h = Math.floor(n / 100), r = n % 100; return [h ? W1[h] + ' hundred' : '', r ? two(r) : ''].filter(Boolean).join(' '); };
  function words(n, sys) {
    if (n === 0) return 'zero';
    const parts = [];
    if (sys === 'international') {
      const m = Math.floor(n / 1e6), th = Math.floor(n / 1000) % 1000, r = n % 1000;
      if (m) parts.push(three(m) + ' million'); if (th) parts.push(three(th) + ' thousand'); if (r) parts.push(three(r));
    } else {
      const c = Math.floor(n / 1e7), l = Math.floor(n / 1e5) % 100, th = Math.floor(n / 1000) % 100, r = n % 1000;
      if (c) parts.push(three(c) + ' crore'); if (l) parts.push(two(l) + ' lakh'); if (th) parts.push(two(th) + ' thousand'); if (r) parts.push(three(r));
    }
    return parts.join(' ');
  }

  const CSS = `
  .lb-placevalue-w{user-select:none;-webkit-user-select:none}
  .lb-placevalue-ch{font-weight:800;font-size:14.5px;line-height:1.3;color:#1b1f3a;background:#f4f0ff;border-radius:14px;padding:9px 12px;margin-bottom:8px}
  .lb-placevalue-num{text-align:center;font-weight:800;font-size:30px;letter-spacing:1px;line-height:1.15;margin:2px 0}
  .lb-placevalue-num span{transition:transform .2s;display:inline-block}
  .lb-placevalue-num span.pop{animation:lbpvPop .3s}
  @keyframes lbpvPop{50%{transform:scale(1.35)}}
  .lb-placevalue-stage{background:#fffaf0;border-radius:18px;box-shadow:inset 0 0 0 2px #f3e6c8;padding:4px 4px 6px}
  .lb-placevalue-svg{display:block;width:100%;height:auto;touch-action:manipulation;cursor:pointer}
  .lb-placevalue-grid{display:grid;gap:3px;margin-top:4px}
  .lb-placevalue-b{height:40px;border:none;border-radius:11px;font-family:inherit;font-weight:800;font-size:20px;cursor:pointer;color:#fff;padding:0;min-width:0;transition:transform .08s}
  .lb-placevalue-b:active{transform:scale(.92)}
  .lb-placevalue-b.m{background:#fff!important;border:2px solid currentColor}
  .lb-placevalue-info{margin-top:8px;background:#f7f8fe;border-radius:14px;padding:8px 10px;font-size:13.5px;font-weight:700;color:#1b1f3a;line-height:1.4;min-height:44px}
  .lb-placevalue-info .k{color:#6b7090;font-weight:800;font-size:11.5px;text-transform:uppercase;letter-spacing:.4px;margin-right:4px}
  .lb-placevalue-info div{overflow-wrap:anywhere}
  .lb-placevalue-hint{text-align:center;font-weight:800;font-size:13.5px;color:#7c4ddb;min-height:20px;margin:6px 0 4px}
  .lb-placevalue-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
  .lb-placevalue-s{height:42px;border:none;border-radius:14px;font-family:inherit;font-weight:800;font-size:14px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 4px 0 #d3d7ef;padding:0 14px}
  .lb-placevalue-s:active{transform:translateY(3px);box-shadow:0 1px 0 #d3d7ef}
  `;

  Labs.register(T, {
    title: 'Abacus & place value',
    subjects: ['maths'],
    render(host, p, api) {
      let n = typeof p.places === 'string' ? (NAMES[p.places.toLowerCase().replace(/[^a-z]/g, '')] || parseInt(p.places, 10)) : +p.places;
      if (!n || n < 1) n = 6; n = Math.max(1, Math.min(9, Math.round(n)));
      const view = p.view === 'blocks' && n <= 3 ? 'blocks' : 'abacus';
      let sys = p.system === 'international' ? 'international' : 'indian';
      const carry = p.carry !== false;
      const maxVal = Math.pow(10, n) - 1;
      const toInt = v => { const x = Math.round(+String(v == null ? '' : v).replace(/[,\s]/g, '')); return isFinite(x) ? x : NaN; };
      let digits = new Array(n).fill(0); // digits[0] = ones
      const setVal = v => { v = Math.max(0, Math.min(maxVal, v | 0)); for (let i = 0; i < n; i++) { digits[i] = v % 10; v = Math.floor(v / 10); } };
      const val = () => digits.reduce((s, d, i) => s + d * Math.pow(10, i), 0);
      const startV = isFinite(toInt(p.start)) ? toInt(p.start) : 0;
      setVal(startV);
      let target = toInt(p.target);
      if (!isFinite(target) || target < 0 || target > maxVal || target === startV) target = randTarget();
      let customText = p.challenge ? String(p.challenge) : '';
      const ask = ['words', 'expanded'].includes(p.ask) ? p.ask : 'number';

      function randTarget() {
        let t, tries = 0;
        do {
          t = 0;
          for (let i = 0; i < n; i++) { let d = Math.floor(Math.random() * 10); if (i === n - 1 && n > 1) d = 1 + Math.floor(Math.random() * 9); if (n > 3 && i < n - 1 && Math.random() < 0.2) d = 0; t += d * Math.pow(10, i); }
          tries++;
        } while ((t === val() || t === 0) && tries < 30);
        return t;
      }
      function expanded(v, s2) {
        const terms = []; const ds = String(v).split('').reverse();
        for (let i = ds.length - 1; i >= 0; i--) if (+ds[i]) terms.push(fmtNum(+ds[i] * Math.pow(10, i), s2 || sys));
        return terms.length ? terms.join(' + ') : '0';
      }
      function targetShown() { return ask === 'words' ? words(target, sys) : ask === 'expanded' ? expanded(target) : fmtNum(target, sys); }
      function defaultText() { return ask === 'words' ? `Build the number: “${targetShown()}”` : ask === 'expanded' ? `Build ${targetShown()}` : `Build ${targetShown()} on the ${view === 'blocks' ? 'mat' : 'abacus'}`; }

      host.innerHTML = `<style>${CSS}</style><div class="lb-placevalue-w">
        <div class="lb-placevalue-ch"></div>
        <div class="lb-placevalue-num" aria-live="polite"></div>
        <div class="lb-placevalue-stage"><svg class="lb-placevalue-svg"></svg><div class="lb-placevalue-grid"></div></div>
        <div class="lb-placevalue-info"></div>
        <div class="lb-placevalue-hint"></div>
        <div class="lb-placevalue-row"></div></div>`;
      const $ = s => host.querySelector(s);
      const svg = $('svg'), grid = $('.lb-placevalue-grid'), numEl = $('.lb-placevalue-num'), infoEl = $('.lb-placevalue-info'), hintEl = $('.lb-placevalue-hint'), chEl = $('.lb-placevalue-ch'), rowEl = $('.lb-placevalue-row');
      const W = 360;
      const colW = W / n;
      const colX = i => (n - 1 - i) * colW + colW / 2; // i = place index (0 ones) → x centre; highest place on the left
      const pc = i => PERIOD[sys][i];

      // ---------- drawing ----------
      function drawAbacus() {
        const H = 196, top = 46, rodBot = 176;
        svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
        let s = `<rect x="2" y="${top - 8}" width="${W - 4}" height="${rodBot - top + 20}" rx="12" fill="#fff" stroke="#e8d7ad" stroke-width="2"/>`;
        // period bands
        const groups = [];
        for (let i = n - 1; i >= 0; i--) { const g = pc(i); if (!groups.length || groups[groups.length - 1].g !== g) groups.push({ g, from: i, to: i }); else groups[groups.length - 1].to = i; }
        groups.forEach(gr => {
          const x1 = colX(gr.from) - colW / 2 + 2, x2 = colX(gr.to) + colW / 2 - 2;
          s += `<rect x="${x1}" y="2" width="${x2 - x1}" height="17" rx="8" fill="${PLIGHT[gr.g]}"/><text x="${(x1 + x2) / 2}" y="14.5" text-anchor="middle" font-size="11.5" font-weight="800" fill="${PDARK[gr.g]}">${PNAME[sys][gr.g] || ''}</text>`;
        });
        const bw = Math.min(46, colW - 7), bh = 12.4;
        for (let i = 0; i < n; i++) {
          const x = colX(i), g = pc(i);
          s += `<text x="${x}" y="35" text-anchor="middle" font-size="${colW < 42 ? 12 : 13.5}" font-weight="800" fill="${PDARK[g]}">${ABBR[sys][i]}</text>`;
          s += `<rect x="${x - 2.5}" y="${top - 2}" width="5" height="${rodBot - top + 4}" rx="2.5" fill="#b78a4a"/>`;
          for (let b = 0; b < digits[i]; b++) {
            const y = rodBot - (b + 1) * bh - 0.5;
            s += `<rect x="${x - bw / 2}" y="${y}" width="${bw}" height="${bh - 1.4}" rx="${(bh - 1.4) / 2}" fill="${PCOL[g]}" stroke="${PDARK[g]}" stroke-width="1.3"/><rect x="${x - bw / 2 + 4}" y="${y + 2}" width="${bw * 0.35}" height="2.6" rx="1.3" fill="#fff" opacity=".55"/>`;
          }
          s += `<text x="${x}" y="${top + 8}" text-anchor="middle" font-size="12" font-weight="800" fill="#c7b48a">${digits[i] ? '' : '0'}</text>`;
        }
        s += `<rect x="2" y="${rodBot + 2}" width="${W - 4}" height="14" rx="6" fill="#c89b5b"/>`;
        svg.innerHTML = s;
      }
      function drawBlocks() {
        const H = 176;
        svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
        let s = '';
        const zone = i => ({ x: colX(i) - colW / 2, w: colW });
        const nm = ['Ones', 'Tens', 'Hundreds'];
        for (let i = 0; i < n; i++) {
          const z = zone(i), g = [0, 1, 2][i];
          s += `<rect x="${z.x + 3}" y="2" width="${z.w - 6}" height="${H - 4}" rx="12" fill="${PLIGHT[g]}"/>`;
          s += `<text x="${z.x + z.w / 2}" y="18" text-anchor="middle" font-size="13" font-weight="800" fill="${PDARK[g]}">${nm[i]}</text>`;
          const d = digits[i];
          if (i === 0) { // ones cubes in a 3x3
            for (let k = 0; k < d; k++) { const cx = z.x + z.w / 2 - 27 + (k % 3) * 20, cy = 40 + Math.floor(k / 3) * 22 + 18; s += cube(cx, cy, 16, PCOL[0], PDARK[0]); }
          } else if (i === 1) { // tens rods (1 x 10)
            const totalW = d * 10; const x0 = z.x + z.w / 2 - (d * 12 - 3) / 2;
            for (let k = 0; k < d; k++) { const rx = x0 + k * 12; s += `<g>`; for (let c = 0; c < 10; c++) s += `<rect x="${rx}" y="${30 + c * 13.6}" width="9" height="13" rx="1.5" fill="${PCOL[1]}" stroke="${PDARK[1]}" stroke-width="1"/>`; s += `</g>`; }
          } else { // hundreds flats 10x10
            const fs = Math.min(36, (z.w - 18) / 3);
            for (let k = 0; k < d; k++) {
              const fx = z.x + z.w / 2 - (fs * 3 + 8) / 2 + (k % 3) * (fs + 4), fy = 30 + Math.floor(k / 3) * (fs + 6);
              s += `<rect x="${fx}" y="${fy}" width="${fs}" height="${fs}" rx="2" fill="${PCOL[2]}" stroke="${PDARK[2]}" stroke-width="1.2"/>`;
              let gl = ''; for (let c = 1; c < 10; c++) { const o = c * fs / 10; gl += `M${fx + o} ${fy}v${fs}M${fx} ${fy + o}h${fs}`; }
              s += `<path d="${gl}" stroke="#fff" stroke-width=".6" opacity=".7"/>`;
            }
          }
          if (!d) s += `<text x="${z.x + z.w / 2}" y="${H / 2 + 12}" text-anchor="middle" font-size="13" font-weight="800" fill="${PDARK[g]}" opacity=".45">tap to add</text>`;
        }
        svg.innerHTML = s;
        function cube(x, y, sz, c, d) { return `<rect x="${x}" y="${y}" width="${sz}" height="${sz}" rx="3" fill="${c}" stroke="${d}" stroke-width="1.3"/><rect x="${x + 3}" y="${y + 3}" width="${sz * .4}" height="3" rx="1.5" fill="#fff" opacity=".6"/>`; }
      }
      function draw() { view === 'blocks' ? drawBlocks() : drawAbacus(); }

      function buildGrid() {
        grid.style.gridTemplateColumns = `repeat(${n}, 1fr)`;
        let s = '';
        for (let i = n - 1; i >= 0; i--) { const g = view === 'blocks' ? i : pc(i); s += `<button class="lb-placevalue-b" data-i="${i}" data-d="1" style="background:${PCOL[g]}" aria-label="add ${SING[sys][i]}">+</button>`; }
        for (let i = n - 1; i >= 0; i--) { const g = view === 'blocks' ? i : pc(i); s += `<button class="lb-placevalue-b m" data-i="${i}" data-d="-1" style="color:${PDARK[g]}" aria-label="remove ${SING[sys][i]}">−</button>`; }
        grid.innerHTML = s;
      }
      function readout(popIdx) {
        const v = val();
        // number with each digit coloured by its period
        const s = fmtNum(v, sys);
        let di = String(v).length - 1, out = '';
        for (const ch of s) {
          if (ch === ',') { out += '<span style="color:#9aa0c0">,</span>'; continue; }
          const g = view === 'blocks' ? Math.min(di, 2) : PERIOD[sys][di];
          out += `<span class="${di === popIdx ? 'pop' : ''}" style="color:${PDARK[g]}">${ch}</span>`; di--;
        }
        numEl.innerHTML = out;
        let info = '';
        if (p.showExpanded !== false) info += `<div><span class="k">Expanded</span>${esc(expanded(v))}</div>`;
        if (p.showWords !== false) info += `<div><span class="k">In words</span>${esc(words(v, sys))}</div>`;
        infoEl.innerHTML = info;
        infoEl.style.display = info ? '' : 'none';
      }
      function buildRow() {
        let s = '';
        if (p.toggle !== false && n >= 4 && view === 'abacus') s += `<button class="lb-placevalue-s" data-act="sys">${sys === 'indian' ? 'Indian 1,00,000' : 'International 100,000'} ⇄</button>`;
        s += `<button class="lb-placevalue-s" data-act="clear">↺ Clear</button>`;
        if (p.newChallenge !== false) s += `<button class="lb-placevalue-s" data-act="new">✨ New</button>`;
        rowEl.innerHTML = s;
      }
      function setChallengeText() { chEl.textContent = '🎯 Challenge: ' + (customText || defaultText()); }
      function hint(t) { hintEl.textContent = t || ''; }

      // ---------- actions ----------
      let won = false;
      function change(i, d) {
        if (d > 0) {
          if (digits[i] < 9) { digits[i]++; api.sfx('tap'); hint(''); }
          else if (!carry) { api.sfx('wrong'); hint('A rod holds only 9 beads!'); return; }
          else {
            // regroup: 10 of this place make 1 of the next
            let j = i; while (j < n && digits[j] === 9) j++;
            if (j >= n) { api.sfx('wrong'); hint('That is the biggest number this abacus can show!'); return; }
            for (let k = i; k < j; k++) digits[k] = 0; digits[j]++;
            api.sfx('coin');
            hint(`10 ${FULL[sys][i]} = 1 ${SING[sys][i + 1]}! Regrouped ➜`);
          }
        } else {
          if (digits[i] > 0) { digits[i]--; api.sfx('tap'); hint(''); }
          else if (!carry) { api.sfx('wrong'); hint('No beads here to take away.'); return; }
          else {
            let j = i; while (j < n && digits[j] === 0) j++;
            if (j >= n) { api.sfx('wrong'); hint('Nothing left to take away!'); return; }
            digits[j]--; for (let k = i; k < j; k++) digits[k] = 9;
            api.sfx('coin');
            hint(`Borrowed: 1 ${SING[sys][i + 1]} = 10 ${FULL[sys][i]}`);
          }
        }
        draw(); readout(i); check();
      }
      function check() {
        if (won || val() !== target) return;
        won = true; api.sfx('correct'); hint('⭐ Perfect!');
        api.win(`You built ${fmtNum(target, sys)} — ${words(target, sys)}.`);
      }
      grid.addEventListener('click', e => { const b = e.target.closest('button'); if (b) change(+b.dataset.i, +b.dataset.d); });
      svg.addEventListener('click', e => {
        const r = svg.getBoundingClientRect(); const x = (e.clientX - r.left) / r.width * W;
        const col = Math.floor(x / colW); const i = n - 1 - col; if (i >= 0 && i < n) change(i, 1);
      });
      rowEl.addEventListener('click', e => {
        const b = e.target.closest('button'); if (!b) return;
        const a = b.dataset.act;
        if (a === 'sys') { sys = sys === 'indian' ? 'international' : 'indian'; buildRow(); buildGrid(); draw(); readout(); setChallengeText(); hint(sys === 'indian' ? 'Indian: commas after 3 digits, then every 2' : 'International: a comma after every 3 digits'); api.sfx('tap'); }
        else if (a === 'clear') { setVal(0); draw(); readout(); hint(''); api.sfx('tap'); }
        else if (a === 'new') { target = randTarget(); customText = ''; if (won) { won = false; api.resetWin && api.resetWin(); } setChallengeText(); hint(''); api.sfx('tap'); }
      });

      buildGrid(); buildRow(); draw(); readout(); setChallengeText();
      return () => { };
    },
    example: {
      places: 'lakhs', view: 'abacus', system: 'indian', target: 305072, ask: 'number'
    },
    examples: [
      { places: 3, view: 'blocks', start: 38, target: 46, challenge: 'You have 38. Add blocks to make 46 — what happens when the ones reach 10?' },
      { places: 'crores', view: 'abacus', system: 'international', start: 0, target: 12045600, ask: 'words', challenge: 'Build: twelve million forty-five thousand six hundred' },
      { places: 'thousands', view: 'abacus', start: 2000, target: 1993, ask: 'expanded', challenge: 'Start at 2,000 and take away beads to build 1,000 + 900 + 90 + 3' }
    ]
  });
})();
