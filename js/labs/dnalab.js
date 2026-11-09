/* Knowtopia Concept Lab: dnalab — DNA replication, transcription, translation and mutation
 *
 * replicate : drag the helicase along to unzip the double helix, then add complementary
 *             nucleotides. The leading strand grows continuously 5′→3′ towards the fork; the
 *             lagging strand is made 5′→3′ away from the fork in Okazaki fragments.
 * transcribe: build mRNA (5′→3′) on the template strand (3′→5′) — A pairs with U in RNA.
 * translate : find the start codon AUG, move the ribosome codon by codon (standard genetic code),
 *             stop at UAA / UAG / UGA. Goal 'build': write an mRNA for a given polypeptide.
 * mutate    : substitute, insert or delete bases in a gene and see the mRNA and protein change
 *             (silent, missense, nonsense, frameshift).
 *
 * PARAMS (all optional)
 *  mode      string  'replicate' | 'transcribe' | 'translate' | 'mutate'                    default 'transcribe'
 *  dna       string  coding (sense) strand 5′→3′, letters A T G C. replicate: the top parental
 *                    strand; transcribe/mutate: the gene        default replicate 'ATGCCGTAAGCT',
 *                                                               transcribe 'TACATGGCATTCTAAGC'… (see code), mutate 'ATGTTCGGAAAGTGGTAA'
 *  mrna      string  translate mode mRNA 5′→3′ (A U G C); if absent, made from dna     default 'GCAUGUUCGGAAAGUGGUAACC'
 *  fragment  number  replicate: Okazaki fragment length in bases (2–6)                  default 4
 *  goal      object  replicate/transcribe: {type:'complete'} build the whole new strand(s)
 *                    translate: {type:'translate'} start → stop (default) | {type:'start'} tap the
 *                       start codon | {type:'stop'} tap the stop codon in frame |
 *                       {type:'build', protein:'Met-Phe-Gly-Stop' or ['Met','Phe',…] or 'MFG*'}
 *                    mutate: {type:'silent'|'missense'|'nonsense'|'frameshift'} make ONE mutation
 *                       of that kind                                                  default 'nonsense'
 *  challenge string  challenge sentence (else generated)
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const CODE = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'; // standard code, order U C A G
  const AA3 = { F: 'Phe', L: 'Leu', S: 'Ser', Y: 'Tyr', C: 'Cys', W: 'Trp', P: 'Pro', H: 'His', Q: 'Gln', R: 'Arg', I: 'Ile', M: 'Met', T: 'Thr', N: 'Asn', K: 'Lys', V: 'Val', A: 'Ala', D: 'Asp', E: 'Glu', G: 'Gly', '*': 'Stop' };
  const A1 = {}; Object.keys(AA3).forEach(k => A1[AA3[k].toLowerCase()] = k); A1.stop = '*'; A1.ter = '*';
  const IDX = { U: 0, C: 1, A: 2, G: 3 };
  const aaOf = c => (c.length === 3 && [...c].every(b => b in IDX)) ? CODE[16 * IDX[c[0]] + 4 * IDX[c[1]] + IDX[c[2]]] : null;
  const codonsFor = a => { const out = []; 'UCAG'.split('').forEach(x => 'UCAG'.split('').forEach(y => 'UCAG'.split('').forEach(z => { if (aaOf(x + y + z) === a) out.push(x + y + z); }))); return out; };
  const DCOMP = { A: 'T', T: 'A', G: 'C', C: 'G' }, RCOMP = { A: 'U', T: 'A', G: 'C', C: 'G' };
  const COL = { A: ['#d9f8ee', '#0f7a5c'], T: ['#ffe3e3', '#c94545'], U: ['#ffead6', '#c2410c'], G: ['#e0ebff', '#2257b8'], C: ['#efe9ff', '#5b33c9'] };
  const cleanDNA = s => String(s || '').toUpperCase().replace(/U/g, 'T').replace(/[^ATGC]/g, '');
  const cleanRNA = s => String(s || '').toUpperCase().replace(/T/g, 'U').replace(/[^AUGC]/g, '');
  function translate(m, start) { // from index start, until stop or end
    const out = []; for (let i = start; i + 3 <= m.length; i += 3) { const c = m.substr(i, 3), a = aaOf(c); out.push({ i, c, a }); if (a === '*') break; } return out;
  }
  function parseProtein(pr) {
    let arr = Array.isArray(pr) ? pr : String(pr || '').includes('-') || String(pr || '').includes(' ') ? String(pr).split(/[-\s,]+/) : String(pr || '').split('');
    arr = arr.map(x => String(x).trim()).filter(Boolean).map(x => x.length === 1 ? (AA3[x.toUpperCase()] ? x.toUpperCase() : null) : A1[x.toLowerCase()] || null).filter(Boolean);
    return arr;
  }
  const tile = (b, extra = '') => `<span class="lb-dnalab-b ${extra}" style="background:${b ? COL[b][0] : '#fff'};color:${b ? COL[b][1] : '#c3c7da'}">${b || ''}</span>`;

  const CSS = `
  .lb-dnalab{color:#1b1f3a;font-weight:700;user-select:none;-webkit-user-select:none}
  .lb-dnalab-ch{background:#f3efff;color:#4c2fb0;border-radius:14px;padding:7px 11px;font-size:13px;line-height:1.3;margin-bottom:6px}
  .lb-dnalab-stage{background:#f7f8fd;border-radius:16px;padding:7px 6px;position:relative}
  .lb-dnalab-lg{font-size:10.5px;color:#6b7090;line-height:1.3;margin-bottom:4px}
  .lb-dnalab-lg b{color:#1b1f3a}
  .lb-dnalab-seq{display:flex;flex-wrap:wrap;gap:6px 4px;justify-content:center}
  .lb-dnalab-cod{display:flex;flex-direction:column;align-items:center;gap:2px;border-radius:11px;padding:2px;border:2px solid transparent;transition:border-color .2s,background .2s}
  .lb-dnalab-cod.rib{border-color:#8b5cf6;background:#f1edff}
  .lb-dnalab-cod.tap{cursor:pointer}
  .lb-dnalab-cols{display:flex;gap:2px}
  .lb-dnalab-col{display:flex;flex-direction:column;gap:2px;align-items:center}
  .lb-dnalab-seq.n .lb-dnalab-b{width:23px}
  .lb-dnalab-b{width:26px;height:27px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:14px;border:1.5px solid rgba(27,31,58,.08);box-sizing:border-box;transition:transform .2s}
  .lb-dnalab-b.faint{opacity:.45;height:20px;font-size:11px}
  .lb-dnalab-b.slot{border:2px dashed #c9cde3}
  .lb-dnalab-b.next{border:2px solid #8b5cf6;box-shadow:0 0 0 3px #d9ccff;animation:lb-dnalab-pulse 1s infinite alternate}
  .lb-dnalab-b.big{width:32px;height:34px;font-size:16px;cursor:pointer}
  .lb-dnalab-b.chg{box-shadow:0 0 0 2.5px #ff6b6b}
  .lb-dnalab-b.sm{height:15px;font-size:9.5px;width:32px;opacity:.85;border-radius:5px}
  .lb-dnalab-b.fl{cursor:pointer}
  .lb-dnalab-b.st{box-shadow:0 0 0 2.5px #2ed3a5}
  @keyframes lb-dnalab-pulse{from{box-shadow:0 0 0 2px #d9ccff}to{box-shadow:0 0 0 5px #e9e1ff}}
  .lb-dnalab-aa{font-size:10.5px;font-weight:900;border-radius:7px;padding:1px 5px;min-height:16px;line-height:16px;color:#fff;background:#8b5cf6;white-space:nowrap}
  .lb-dnalab-aa.e{background:transparent;color:#c3c7da}
  .lb-dnalab-aa.stop{background:#ff6b6b}.lb-dnalab-aa.bad{background:#ffb4b4;color:#8a1f1f}.lb-dnalab-aa.chg{background:#ffc93c;color:#1b1f3a}
  .lb-dnalab-chain{display:flex;flex-wrap:wrap;gap:3px;align-items:center;min-height:22px;margin-top:5px;font-size:11px;color:#6b7090}
  .lb-dnalab-pal{display:flex;gap:6px;margin-top:6px}
  .lb-dnalab-pb{flex:1;min-height:44px;border:none;border-radius:13px;font:inherit;font-weight:900;font-size:19px;cursor:pointer;box-shadow:0 3px 0 rgba(27,31,58,.15)}
  .lb-dnalab-pb:active{transform:translateY(2px);box-shadow:none}
  .lb-dnalab-pb.g{background:#eef0fb;color:#1b1f3a;font-size:13px}
  .lb-dnalab-pb.on{background:#8b5cf6;color:#fff}
  .lb-dnalab-pb.v{background:#8b5cf6;color:#fff;font-size:13px}
  .lb-dnalab-msg{font-size:12px;color:#6b7090;min-height:16px;margin-top:5px;line-height:1.3}
  .lb-dnalab-msg.good{color:#0f7a5c}.lb-dnalab-msg.bad{color:#c94545}
  .lb-dnalab-svg{display:block;width:100%;height:auto;touch-action:none}
  .lb-dnalab-svg text{font-family:inherit;pointer-events:none}
  @keyframes lb-dnalab-shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-4px)}75%{transform:translateX(4px)}}
  .lb-dnalab-shake{animation:lb-dnalab-shake .3s}`;

  Labs.register('dnalab', {
    title: 'DNA lab',
    subjects: ['biology', 'science'],
    render(host, p, api) {
      const mode = ['replicate', 'transcribe', 'translate', 'mutate'].includes(p.mode) ? p.mode : 'transcribe';
      const goal = (p.goal && typeof p.goal === 'object') ? p.goal : (typeof p.goal === 'string' ? { type: p.goal } : {});
      let won = false; const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(m); };
      const timers = []; const later = (f, ms) => timers.push(setTimeout(f, ms));
      let cleanup = () => {};
      const shell = (challenge, body) => {
        host.innerHTML = `<style>${CSS}</style><div class="lb-dnalab"><div class="lb-dnalab-ch">🎯 Challenge: ${esc(challenge)}</div>${body}<div class="lb-dnalab-msg"></div></div>`;
        return host.querySelector('.lb-dnalab');
      };
      let root, msgEl;
      const setMsg = (t, c) => { msgEl.innerHTML = t; msgEl.className = 'lb-dnalab-msg' + (c ? ' ' + c : ''); };
      const shake = el => { if (!el) return; el.classList.remove('lb-dnalab-shake'); void el.offsetWidth; el.classList.add('lb-dnalab-shake'); };

      // ============================================================ TRANSCRIBE
      if (mode === 'transcribe') {
        let dna = cleanDNA(p.dna); if (dna.length < 3) dna = 'ATGGCATTCTAA'; dna = dna.slice(0, 24);
        const tmpl = [...dna].map(b => DCOMP[b]); // template 3'→5' (left→right)
        const want = [...dna].map(b => b === 'T' ? 'U' : b);
        let built = [];
        const challenge = p.challenge ? String(p.challenge) : 'Build the mRNA on the template strand, base by base (5′→3′).';
        root = shell(challenge, `<div class="lb-dnalab-stage"><div class="lb-dnalab-lg">Coding strand 5′→3′ (faint) · <b>template strand 3′→5′</b> · mRNA grows 5′→3′ ⬇</div><div class="lb-dnalab-seq"></div></div>
          <div class="lb-dnalab-pal">${['A', 'U', 'G', 'C', 'T'].map(b => `<button class="lb-dnalab-pb" data-b="${b}" style="background:${COL[b][0]};color:${COL[b][1]}">${b}</button>`).join('')}<button class="lb-dnalab-pb g" data-x>⌫</button></div>`);
        msgEl = root.querySelector('.lb-dnalab-msg'); const seq = root.querySelector('.lb-dnalab-seq');
        function draw() {
          let h = '';
          for (let c = 0; c < dna.length; c += 3) {
            h += '<div class="lb-dnalab-cod"><div class="lb-dnalab-cols">';
            for (let i = c; i < Math.min(c + 3, dna.length); i++) h += `<div class="lb-dnalab-col">${tile(dna[i], 'faint')}${tile(tmpl[i])}${i < built.length ? tile(built[i]) : tile('', i === built.length ? 'slot next' : 'slot')}</div>`;
            h += '</div></div>';
          }
          seq.innerHTML = h;
        }
        root.querySelectorAll('[data-b]').forEach(b => b.onclick = () => {
          if (built.length >= dna.length) return;
          const x = b.dataset.b, i = built.length;
          if (x === want[i]) { built.push(x); api.sfx('tap'); draw(); setMsg(`${tmpl[i]} on the template → ${x} in mRNA.`, '');
            if (built.length === dna.length) { setMsg(`mRNA 5′-${built.join('')}-3′ — same as the coding strand with U for T.`, 'good'); later(() => winOnce('mRNA complete! It is complementary to the template strand and matches the coding strand (T → U).'), 400); } }
          else { api.sfx('wrong'); shake(seq.querySelector('.next')); setMsg(x === 'T' ? 'RNA has no thymine — it uses uracil (U) instead.' : `${tmpl[i]} pairs with ${want[i]}, not ${x}. In RNA: A–U, G–C.`, 'bad'); }
        });
        root.querySelector('[data-x]').onclick = () => { if (built.length) { built.pop(); api.sfx('tap'); draw(); } };
        draw(); setMsg('RNA polymerase reads the template 3′→5′. Tap the matching base.');
        return () => timers.forEach(clearTimeout);
      }

      // ============================================================ TRANSLATE
      if (mode === 'translate') {
        const gtype = ['translate', 'start', 'stop', 'build'].includes(goal.type) ? goal.type : 'translate';
        if (gtype === 'build') return buildMode();
        let m = cleanRNA(p.mrna); if (m.length < 3 && p.dna) m = cleanRNA(cleanDNA(p.dna)); if (m.length < 6 || m.indexOf('AUG') < 0) m = 'GCAUGUUCGGAAAGUGGUAACC'; m = m.slice(0, 30);
        let start = -1, rib = -1; const chain = [];
        const firstStart = m.indexOf('AUG');
        const orf = translate(m, firstStart), stopC = orf.find(x => x.a === '*');
        const challenge = p.challenge ? String(p.challenge) : gtype === 'start' ? 'Find the start codon: tap the first base of AUG.' : gtype === 'stop' ? 'Find the start codon, then tap the stop codon in the same reading frame.' : 'Tap the start codon, then move the ribosome codon by codon until it reaches a stop codon.';
        root = shell(challenge, `<div class="lb-dnalab-stage"><div class="lb-dnalab-lg">mRNA <b>5′→3′</b>. <span class="lb-dnalab-hint">Tap the first base of the start codon.</span></div><div class="lb-dnalab-seq"></div>
          <div class="lb-dnalab-chain"></div></div>
          <div class="lb-dnalab-pal"><button class="lb-dnalab-pb v" data-n disabled style="opacity:.4">🧬 Ribosome ▶ next codon</button><button class="lb-dnalab-pb g" data-r style="flex:0 0 auto;padding:0 14px">↺</button></div>`);
        msgEl = root.querySelector('.lb-dnalab-msg'); const seq = root.querySelector('.lb-dnalab-seq'), chEl = root.querySelector('.lb-dnalab-chain'), nb = root.querySelector('[data-n]'), hint = root.querySelector('.lb-dnalab-hint');
        function draw() {
          let h = '';
          if (start < 0) { h = [...m].map((b, i) => `<div class="lb-dnalab-col" data-i="${i}">${tile(b, 'fl')}</div>`).join(''); seq.style.gap = '3px 2px'; }
          else {
            seq.style.gap = '';
            if (start > 0) h += `<div class="lb-dnalab-cod"><div class="lb-dnalab-cols">${[...m.slice(0, start)].map(b => tile(b, 'faint')).join('')}</div><div class="lb-dnalab-aa e">5′ UTR</div></div>`;
            let i = start;
            for (; i + 3 <= m.length; i += 3) {
              const c = m.substr(i, 3), a = aaOf(c), k = (i - start) / 3, done = k < chain.length, on = i === rib;
              h += `<div class="lb-dnalab-cod tap ${on ? 'rib' : ''}" data-c="${i}"><div class="lb-dnalab-cols">${[...c].map(b => tile(b, i === start ? 'st' : '')).join('')}</div><div class="lb-dnalab-aa ${done ? (a === '*' ? 'stop' : '') : 'e'}">${done ? AA3[a] : on ? 'tRNA ' + [...c].map(b => ({ A: 'U', U: 'A', G: 'C', C: 'G' })[b]).join('') : '···'}</div></div>`;
            }
            if (i < m.length) h += `<div class="lb-dnalab-cod"><div class="lb-dnalab-cols">${[...m.slice(i)].map(b => tile(b, 'faint')).join('')}</div><div class="lb-dnalab-aa e">3′</div></div>`;
          }
          seq.innerHTML = h;
          chEl.innerHTML = chain.length ? 'Polypeptide: ' + chain.map(a => `<span class="lb-dnalab-aa ${a === '*' ? 'stop' : ''}">${AA3[a]}</span>`).join('<span>–</span>') : '';
          const atStop = chain.length && chain[chain.length - 1] === '*';
          nb.disabled = start < 0 || atStop || rib + 3 > m.length || gtype !== 'translate'; nb.style.opacity = nb.disabled ? .4 : 1;
        }
        function step() {
          if (rib < 0 || rib + 3 > m.length) return;
          const c = m.substr(rib, 3), a = aaOf(c); chain.push(a); api.sfx(a === '*' ? 'coin' : 'tap');
          if (a === '*') { setMsg(`${c} is a stop codon — no tRNA matches it. The ribosome releases the polypeptide.`, 'good'); draw(); later(() => winOnce(`Polypeptide: ${chain.filter(x => x !== '*').map(x => AA3[x]).join('–')} (${chain.length - 1} amino acids). Start AUG, stop ${c}.`), 400); return; }
          setMsg(`${c} → ${AA3[a]}${a === 'M' && chain.length === 1 ? ' (start codon, methionine)' : ''}. Peptide bond joins it to the chain.`);
          rib += 3; if (rib + 3 > m.length) setMsg('The mRNA ended without a stop codon in this frame.', 'bad');
          draw();
        }
        nb.onclick = step;
        seq.addEventListener('click', onClick);
        function onClick(e) {
          if (start < 0) {
            const col = e.target.closest('[data-i]'); if (!col) return; const i = +col.dataset.i;
            if (m.substr(i, 3) === 'AUG') {
              start = i; rib = i; api.sfx('coin'); hint.textContent = gtype === 'stop' ? 'Reading frame set. Tap the stop codon.' : 'Reading frame set by AUG.';
              setMsg(`✓ AUG at base ${i + 1} — start codon (codes for Met). It sets the reading frame.`, 'good');
              if (gtype === 'translate') step(); else draw();
              if (gtype === 'start') later(() => winOnce('AUG is the start codon: it codes for methionine and sets the reading frame.'), 400);
            } else { api.sfx('wrong'); shake(col); setMsg(`${m.substr(i, 3).padEnd(3, '·')} is not AUG. Look for A-U-G.`, 'bad'); }
            return;
          }
          const cod = e.target.closest('[data-c]'); if (!cod) return; const i = +cod.dataset.c;
          if (gtype === 'stop') {
            const a = aaOf(m.substr(i, 3)), first = translate(m, start).find(x => x.a === '*');
            if (a === '*' && first && first.i === i) { api.sfx('coin'); chain.length = 0; translate(m, start).forEach(x => chain.push(x.a)); rib = -1; draw(); setMsg(`✓ ${m.substr(i, 3)} is the first stop codon in frame.`, 'good'); later(() => winOnce(`Stop codon ${m.substr(i, 3)} found — the polypeptide has ${chain.length - 1} amino acids.`), 400); }
            else { api.sfx('wrong'); shake(cod); setMsg(a === '*' ? 'That is a stop codon, but not the first one — translation would already have ended.' : `${m.substr(i, 3)} codes for ${AA3[a]}. Stop codons are UAA, UAG, UGA.`, 'bad'); }
          } else if (gtype === 'translate' && i === rib) step();
          else if (gtype === 'translate') { const a = aaOf(m.substr(i, 3)); setMsg(`${m.substr(i, 3)} → ${a ? AA3[a] : '?'}. The ribosome moves one codon at a time.`); }
        }
        root.querySelector('[data-r]').onclick = () => { start = -1; rib = -1; chain.length = 0; hint.textContent = 'Tap the first base of the start codon.'; api.sfx('tap'); setMsg(''); if (won) { won = false; api.resetWin && api.resetWin(); } draw(); };
        draw(); if (!stopC) setMsg('Note: no stop codon in this frame.');
        return () => { timers.forEach(clearTimeout); seq.removeEventListener('click', onClick); };
      }

      // ============================================================ MUTATE
      if (mode === 'mutate') {
        let gene = cleanDNA(p.dna); if (gene.length < 9 || gene.indexOf('ATG') < 0) gene = 'ATGTTCGGAAAGTGGTAA'; gene = gene.slice(0, 27);
        const gtype = ['silent', 'missense', 'nonsense', 'frameshift'].includes(goal.type) ? goal.type : 'nonsense';
        let cur = [...gene], marks = [], tool = 'sub', edits = 0;
        const prot = s => { const r = s.replace(/T/g, 'U'), st = r.indexOf('AUG'); return st < 0 ? [] : translate(r, st).map(x => x.a); };
        const P0 = prot(gene);
        const DESC = { silent: 'a silent mutation (protein unchanged)', missense: 'a missense mutation (one amino acid changes)', nonsense: 'a nonsense mutation (early stop codon)', frameshift: 'a frameshift (insert or delete one base)' };
        const challenge = p.challenge ? String(p.challenge) : `Make ${DESC[gtype]} with a single change.`;
        root = shell(challenge, `<div class="lb-dnalab-pal" style="margin:0 0 6px">${[['sub', '🔁 Swap'], ['ins', '➕ Insert'], ['del', '✂️ Delete']].map(([k, t]) => `<button class="lb-dnalab-pb g" data-t="${k}">${t}</button>`).join('')}<button class="lb-dnalab-pb g" data-r style="flex:0 0 auto;padding:0 13px">↺</button></div>
          <div class="lb-dnalab-stage"><div class="lb-dnalab-lg">Gene 5′→3′ · <span style="opacity:.7">mRNA</span> · protein — <b class="lb-dnalab-tl"></b></div><div class="lb-dnalab-seq"></div></div>
          <div class="lb-dnalab-chain lb-dnalab-res" style="display:block;line-height:1.4"></div>`);
        msgEl = root.querySelector('.lb-dnalab-msg'); const seq = root.querySelector('.lb-dnalab-seq'), res = root.querySelector('.lb-dnalab-res'), tl = root.querySelector('.lb-dnalab-tl');
        function classify() {
          const s = cur.join(''); if (s === gene) return null;
          const P1 = prot(s), d = s.length - gene.length;
          if (d % 3 !== 0) return 'frameshift';
          if (!P1.length || P1[0] !== 'M') return 'start lost';
          const same = P1.length === P0.length && P1.every((a, i) => a === P0[i]);
          if (same) return 'silent';
          const stopAt = P1.indexOf('*'), stop0 = P0.indexOf('*');
          if (stopAt >= 0 && (stop0 < 0 || stopAt < stop0)) return 'nonsense';
          if (d !== 0) return d > 0 ? 'in-frame insertion' : 'in-frame deletion';
          return 'missense';
        }
        function draw() {
          const s = cur.join(''), r = s.replace(/T/g, 'U'), st = r.indexOf('AUG'), P1 = prot(s);
          let h = '';
          const pre = st < 0 ? cur.length : st;
          if (pre > 0) h += `<div class="lb-dnalab-cod"><div class="lb-dnalab-cols">${cur.slice(0, pre).map((b, i) => `<div class="lb-dnalab-col" data-i="${i}">${tile(b, 'big' + (marks.includes(i) ? ' chg' : ''))}${tile(b === 'T' ? 'U' : b, 'sm')}</div>`).join('')}</div><div class="lb-dnalab-aa e">${st < 0 ? 'no AUG' : '—'}</div></div>`;
          if (st >= 0) for (let i = st, k = 0; i < cur.length; i += 3, k++) {
            const a = i + 3 <= cur.length ? aaOf(r.substr(i, 3)) : null;
            const after = P1.indexOf('*') >= 0 && k > P1.indexOf('*');
            const cls = !a ? 'e' : after ? 'e' : a === '*' ? 'stop' : (P0[k] !== a ? 'chg' : '');
            h += `<div class="lb-dnalab-cod"><div class="lb-dnalab-cols">${cur.slice(i, i + 3).map((b, j) => `<div class="lb-dnalab-col" data-i="${i + j}">${tile(b, 'big' + (marks.includes(i + j) ? ' chg' : ''))}${tile(b === 'T' ? 'U' : b, 'sm')}</div>`).join('')}</div><div class="lb-dnalab-aa ${cls}">${a ? AA3[a] : '—'}</div></div>`;
          }
          seq.innerHTML = h;
          const c = classify();
          const pr = x => x.map(a => AA3[a]).join('–') || '—';
          res.innerHTML = `Was: <b style="color:#1b1f3a">${pr(P0)}</b><br>Now: <b style="color:#1b1f3a">${pr(P1)}</b> ·  <b style="color:${c ? '#c94545' : '#0f7a5c'}">${c ? c : 'no mutation yet'}</b>${edits > 1 ? ` · ${edits} changes` : ''}`;
          tl.textContent = tool === 'sub' ? 'tap a base to change it' : tool === 'ins' ? 'tap a base to insert A before it' : 'tap a base to delete it';
          root.querySelectorAll('[data-t]').forEach(b => b.classList.toggle('on', b.dataset.t === tool));
          return c;
        }
        seq.addEventListener('click', onClick);
        function onClick(e) {
          const col = e.target.closest('[data-i]'); if (!col) return; const i = +col.dataset.i;
          if (tool === 'sub') { cur[i] = { A: 'T', T: 'G', G: 'C', C: 'A' }[cur[i]]; if (!marks.includes(i)) { marks.push(i); edits++; } if (cur.join('') === gene) { marks = []; edits = 0; } }
          else if (tool === 'ins') { if (cur.length >= 30) return; cur.splice(i, 0, 'A'); marks = marks.map(x => x >= i ? x + 1 : x); marks.push(i); edits++; }
          else { if (cur.length <= 6) return; cur.splice(i, 1); marks = marks.filter(x => x !== i).map(x => x > i ? x - 1 : x); edits++; }
          api.sfx('tap');
          const c = draw();
          if (!c) { setMsg('Back to the original gene.'); return; }
          if (edits > 1) { setMsg('That is more than one change — press Reset and try a single change.', 'bad'); return; }
          if (c === gtype) { setMsg(`✓ ${c[0].toUpperCase() + c.slice(1)}!`, 'good'); later(() => winOnce(c === 'silent' ? 'Silent: the new codon codes for the same amino acid (the code is degenerate).' : c === 'missense' ? 'Missense: one codon now codes for a different amino acid.' : c === 'nonsense' ? 'Nonsense: a stop codon appears early, so the protein is cut short.' : 'Frameshift: every codon after the change is read differently.'), 450); }
          else setMsg(`That made a ${c} mutation. You need ${DESC[gtype]}. (Tap the base again to keep changing it, or Reset.)`);
        }
        root.querySelectorAll('[data-t]').forEach(b => b.onclick = () => { tool = b.dataset.t; api.sfx('tap'); draw(); });
        root.querySelector('[data-r]').onclick = () => { cur = [...gene]; marks = []; edits = 0; api.sfx('tap'); setMsg(''); if (won) { won = false; api.resetWin && api.resetWin(); } draw(); };
        draw();
        return () => { timers.forEach(clearTimeout); seq.removeEventListener('click', onClick); };
      }

      // ============================================================ REPLICATE
      return replicateMode();

      // ------------------------------------------------------------ build mRNA for a protein
      function buildMode() {
        let target = parseProtein(goal.protein || p.protein); if (!target.length) target = ['M', 'F', 'G', 'K', '*'];
        if (target[0] !== 'M') target.unshift('M'); if (target[target.length - 1] !== '*') target.push('*');
        target = target.slice(0, 8);
        const L = target.length * 3; let m = [];
        const challenge = p.challenge ? String(p.challenge) : 'Write an mRNA (5′→3′) that codes for: ' + target.map(a => AA3[a]).join('–') + '.';
        root = shell(challenge, `<div class="lb-dnalab-stage"><div class="lb-dnalab-lg">Target: ${target.map(a => `<span class="lb-dnalab-aa ${a === '*' ? 'stop' : ''}">${AA3[a]}</span>`).join(' ')}</div><div class="lb-dnalab-seq n"></div>
          <div class="lb-dnalab-lg lb-dnalab-need" style="margin:5px 0 0"></div></div>
          <div class="lb-dnalab-pal">${['A', 'U', 'G', 'C'].map(b => `<button class="lb-dnalab-pb" data-b="${b}" style="background:${COL[b][0]};color:${COL[b][1]}">${b}</button>`).join('')}<button class="lb-dnalab-pb g" data-x>⌫</button></div>`);
        msgEl = root.querySelector('.lb-dnalab-msg'); const seq = root.querySelector('.lb-dnalab-seq'), need = root.querySelector('.lb-dnalab-need');
        function draw() {
          let h = '';
          for (let k = 0; k < target.length; k++) {
            const c = m.slice(k * 3, k * 3 + 3), full = c.length === 3, a = full ? aaOf(c.join('')) : null;
            h += `<div class="lb-dnalab-cod"><div class="lb-dnalab-cols">${[0, 1, 2].map(j => k * 3 + j < m.length ? tile(m[k * 3 + j]) : tile('', k * 3 + j === m.length ? 'slot next' : 'slot')).join('')}</div><div class="lb-dnalab-aa ${!full ? 'e' : a === target[k] ? (a === '*' ? 'stop' : '') : 'bad'}">${full ? AA3[a] : AA3[target[k]] + '?'}</div></div>`;
          }
          seq.innerHTML = h;
          const k = Math.min(Math.floor(m.length / 3), target.length - 1);
          need.innerHTML = m.length >= L ? '' : `Codons for <b>${AA3[target[k]]}</b>: ${codonsFor(target[k]).join(', ')}`;
        }
        root.querySelectorAll('[data-b]').forEach(b => b.onclick = () => {
          if (m.length >= L) return; m.push(b.dataset.b); api.sfx('tap'); draw();
          if (m.length % 3 === 0) {
            const k = m.length / 3 - 1, c = m.slice(k * 3).join(''), a = aaOf(c);
            if (a === target[k]) { setMsg(`✓ ${c} → ${AA3[a]}`, 'good'); if (m.length === L) later(() => winOnce(`mRNA 5′-${m.join('')}-3′ codes for ${target.filter(x => x !== '*').map(x => AA3[x]).join('–')} and stops at ${c}.`), 400); }
            else { api.sfx('wrong'); setMsg(`✗ ${c} codes for ${AA3[a]}, not ${AA3[target[k]]}. Press ⌫ and fix it.`, 'bad'); }
          } else setMsg('');
        });
        root.querySelector('[data-x]').onclick = () => { if (m.length) { m.pop(); api.sfx('tap'); setMsg(''); draw(); } };
        draw(); setMsg('Many amino acids have more than one codon — any correct one works.');
        return () => timers.forEach(clearTimeout);
      }

      // ------------------------------------------------------------ replication
      function replicateMode() {
        let top = cleanDNA(p.dna); if (top.length < 4) top = 'ATGCCGTAAGCT'; top = top.slice(0, 14);
        const N = top.length, bot = [...top].map(b => DCOMP[b]);
        const F = Math.max(2, Math.min(6, Math.round(+p.fragment || 4)));
        const lead = Array(N).fill(null), lag = Array(N).fill(null); // lead pairs with bottom (new 5'→3' L→R); lag pairs with top
        let fork = 0, active = 'lead', drag = false;
        const challenge = p.challenge ? String(p.challenge) : 'Unzip the DNA with the helicase and build both new strands. Watch how the lagging strand is made in pieces.';
        root = shell(challenge, `<div class="lb-dnalab-stage" style="padding:4px"><svg class="lb-dnalab-svg" viewBox="0 0 372 160"></svg><div class="lb-dnalab-lg" style="margin:0 4px">New strands: <b style="color:#0f7a5c">leading</b> (lower) grows 5′→3′ towards the fork ▶ · <b style="color:#b07d00">lagging</b> (upper) in Okazaki fragments ◀ — <span style="color:#c94545">●</span> = joined by DNA ligase</div></div>
          <div class="lb-dnalab-pal"><button class="lb-dnalab-pb g" data-s="lead">Leading ▶</button><button class="lb-dnalab-pb g" data-s="lag">◀ Lagging</button><button class="lb-dnalab-pb g" data-u style="flex:0 0 auto;padding:0 10px">Unzip ▶</button></div>
          <div class="lb-dnalab-pal">${['A', 'T', 'G', 'C'].map(b => `<button class="lb-dnalab-pb" data-b="${b}" style="background:${COL[b][0]};color:${COL[b][1]}">${b}</button>`).join('')}</div>`);
        msgEl = root.querySelector('.lb-dnalab-msg'); const svg = root.querySelector('svg');
        const X0 = 40, CW = Math.min(24, 310 / N), TW = CW - 3;
        const cx = i => X0 + i * CW;
        const nextLead = () => { const i = lead.indexOf(null); return i >= 0 && i < fork ? i : -1; };
        function nextLag() {
          for (let k = 0; k * F < N; k++) {
            const s = k * F, e = Math.min(N, s + F) - 1;
            if (lag.slice(s, e + 1).every(Boolean)) continue;
            if (fork <= e) return -1;
            for (let i = e; i >= s; i--) if (!lag[i]) return i;
          }
          return -1;
        }
        function draw() {
          const yT = i => i < fork ? 12 : 58, yB = i => i < fork ? 136 : 82;
          const lab = (t, x, y, a) => `<text x="${x}" y="${y}" font-size="8.5" fill="#6b7090" font-weight="900" text-anchor="${a}">${t}</text>`;
          let s = lab('5′', X0 - 4, yT(0) + 14, 'end') + lab('3′', X0 - 4, yB(0) + 14, 'end') + lab('3′', cx(N - 1) + TW + 4, yT(N - 1) + 14, 'start') + lab('5′', cx(N - 1) + TW + 4, yB(N - 1) + 14, 'start');
          // backbones
          s += `<polyline points="${Array.from({ length: N }, (_, i) => `${cx(i) + TW / 2},${yT(i) + 4}`).join(' ')}" fill="none" stroke="#1b1f3a" stroke-width="2.5" stroke-linejoin="round"/>`;
          s += `<polyline points="${Array.from({ length: N }, (_, i) => `${cx(i) + TW / 2},${yB(i) + 16}`).join(' ')}" fill="none" stroke="#1b1f3a" stroke-width="2.5" stroke-linejoin="round"/>`;
          const nl = nextLead(), ng = nextLag();
          for (let i = 0; i < N; i++) {
            const t = (b, x, y, cls) => `<rect x="${x}" y="${y}" width="${TW}" height="20" rx="5" fill="${b ? COL[b][0] : '#fff'}" stroke="${cls === 'next' ? '#8b5cf6' : b ? 'rgba(27,31,58,.12)' : '#c9cde3'}" stroke-width="${cls === 'next' ? 2.2 : 1.2}" ${!b && cls !== 'next' ? 'stroke-dasharray="3 2"' : ''}/>${b ? `<text x="${x + TW / 2}" y="${y + 14.5}" font-size="${TW > 20 ? 12 : 10}" text-anchor="middle" font-weight="900" fill="${COL[b][1]}">${b}</text>` : ''}`;
            s += t(top[i], cx(i), yT(i), '') + t(bot[i], cx(i), yB(i), '');
            if (i < fork) {
              s += t(lag[i], cx(i), 38, i === ng && active === 'lag' ? 'next' : '');
              s += t(lead[i], cx(i), 110, i === nl && active === 'lead' ? 'next' : '');
            } else s += `<line x1="${cx(i) + TW / 2}" y1="80" x2="${cx(i) + TW / 2}" y2="84" stroke="#9aa0c0" stroke-width="1.5"/>`;
          }
          // Okazaki fragments brackets & direction arrows
          for (let k = 0; k * F < N; k++) {
            const a = k * F, e = Math.min(N, a + F) - 1; if (fork <= a) break;
            const filled = lag.slice(a, e + 1).filter(Boolean).length; if (!filled) continue;
            const done = filled === e - a + 1, prevDone = k === 0 || lag.slice((k - 1) * F, k * F).every(Boolean);
            s += `<path d="M${cx(a) + 2} 61 h${cx(e) + TW - cx(a) - 4}" stroke="${done ? '#2ed3a5' : '#ffc93c'}" stroke-width="3" stroke-linecap="round"/>`;
            if (done && k > 0 && prevDone) s += `<circle cx="${cx(a) - 1.5}" cy="61" r="3" fill="#ff6b6b"/>`;
          }
          // helicase (fork)
          const fx = heliX();
          s += `<g class="lb-dnalab-heli" style="cursor:grab"><circle cx="${fx}" cy="80" r="16" fill="#8b5cf6" opacity=".18"/><polygon points="${[0, 1, 2, 3, 4, 5].map(k => `${fx + 11 * Math.cos(k * Math.PI / 3)},${80 + 11 * Math.sin(k * Math.PI / 3)}`).join(' ')}" fill="#8b5cf6"/><text x="${fx}" y="83.5" font-size="9" text-anchor="middle" fill="#fff" font-weight="900">▶</text></g>`;
          if (fork === 0) s += `<text x="186" y="128" font-size="9" text-anchor="middle" fill="#6b7090" font-weight="800">drag the purple helicase ▶ to unzip</text>`;
          svg.innerHTML = s;
          root.querySelectorAll('[data-s]').forEach(b => b.classList.toggle('on', b.dataset.s === active));
        }
        const heliX = () => fork >= N ? cx(N - 1) + TW + 16 : cx(fork) - 14;
        const svgX = e => { const m = svg.getScreenCTM(); if (!m) return 0; const pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY; return pt.matrixTransform(m.inverse()).x; };
        function setFork(f) { f = Math.max(fork, Math.min(N, f)); if (f !== fork) { fork = f; api.sfx('tap'); draw(); hintNext(); } }
        const down = e => { const x = svgX(e), fx = heliX(); if (Math.abs(x - fx) < 34) { drag = true; try { svg.setPointerCapture(e.pointerId); } catch (z) {} } };
        const move = e => { if (drag) setFork(Math.round((svgX(e) + 14 - X0) / CW)); };
        const up = () => { drag = false; };
        svg.addEventListener('pointerdown', down); svg.addEventListener('pointermove', move); svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);
        function hintNext() {
          if (lead.every(Boolean) && lag.every(Boolean)) return;
          const i = active === 'lead' ? nextLead() : nextLag();
          if (i >= 0) setMsg(`${active === 'lead' ? 'Leading' : 'Lagging'}: which base pairs with ${active === 'lead' ? bot[i] : top[i]}?`);
          else if (active === 'lead') setMsg(lead.every(Boolean) ? 'Leading strand done ✓ — switch to the lagging strand.' : 'The leading strand caught up with the fork — unzip more.');
          else setMsg(lag.every(Boolean) ? 'Lagging strand done ✓ — finish the leading strand.' : `The next Okazaki fragment needs ${F} more bases of open template — unzip more.`);
        }
        root.querySelectorAll('[data-s]').forEach(b => b.onclick = () => { active = b.dataset.s; api.sfx('tap'); draw(); hintNext(); });
        root.querySelector('[data-u]').onclick = () => setFork(fork + 1);
        root.querySelectorAll('[data-b]').forEach(b => b.onclick = () => {
          const i = active === 'lead' ? nextLead() : nextLag(); if (i < 0) { api.sfx('hmm'); hintNext(); return; }
          const tmpl = active === 'lead' ? bot[i] : top[i], x = b.dataset.b;
          if (x !== DCOMP[tmpl]) { api.sfx('wrong'); setMsg(`${tmpl} pairs with ${DCOMP[tmpl]} (A = T, G ≡ C).`, 'bad'); return; }
          (active === 'lead' ? lead : lag)[i] = x; api.sfx('tap'); draw(); hintNext();
          if (lead.every(Boolean) && lag.every(Boolean)) { setMsg('Both daughter DNA molecules: one old strand + one new strand each.', 'good'); later(() => winOnce('Semi-conservative replication! Each new DNA has one parental and one new strand; the leading strand was continuous, the lagging strand was made in Okazaki fragments joined by DNA ligase.'), 400); }
        });
        draw(); setMsg('Drag the purple helicase (or tap Unzip) to open the double helix.');
        return () => { timers.forEach(clearTimeout); svg.removeEventListener('pointerdown', down); svg.removeEventListener('pointermove', move); svg.removeEventListener('pointerup', up); svg.removeEventListener('pointercancel', up); };
      }
    },
    example: {
      mode: 'translate', mrna: 'GCAUGUUCGGAAAGUGGUAACC', goal: { type: 'translate' },
      challenge: 'Class 12 · Translation: find the start codon, then move the ribosome codon by codon to the stop codon.'
    },
    examples: [
      { mode: 'replicate', dna: 'ATGCCGTAAGCT', fragment: 4, goal: { type: 'complete' },
        challenge: 'Replication fork: unzip the DNA and build the leading and lagging strands.' },
      { mode: 'translate', goal: { type: 'build', protein: 'Met-Trp-Lys-Stop' }, mrna: '',
        challenge: 'Genetic code: write an mRNA that codes for Met–Trp–Lys, then stop.' },
      { mode: 'mutate', dna: 'ATGTTCGGAAAGTGGTAA', goal: { type: 'nonsense' },
        challenge: 'उत्परिवर्तन (mutation): change ONE base so that the protein stops early (nonsense mutation).' }
    ]
  });
})();
