/* StudyVerse lab: sandhi — join (सन्धि) and split (सन्धि-विच्छेद) words, with animated merging
 * Works for Hindi/Sanskrit स्वर, व्यंजन, विसर्ग सन्धि and for English contractions / compound words.
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *  pairs      array   [[part1, part2, result, rule, wrongJoins?, wrongSplits?], …]
 *                       part1 + part2 = result; rule = short text shown after joining
 *                       (e.g. 'अ + उ = ओ · गुण सन्धि'); wrongJoins = optional array of wrong joined
 *                       forms; wrongSplits = optional array of wrong splits like 'हिम + अलय'.
 *                       Wrong options are generated automatically when not given.  default 8 Hindi स्वर सन्धि
 *  mode       string  challenge question type: 'join' | 'split' | 'both'           default 'both'
 *  rounds     number  correct answers needed to win                                default min(5, pairs)
 *  title      string  small heading over the word stage (e.g. 'स्वर सन्धि')        default 'Sandhi'
 *  challenge  string  the "🎯 Challenge" line                                       default auto
 *
 * The child: chooses a pair (◀ ▶), drags the second word onto the first (or taps Join) and watches
 * the boundary letters merge into the new letters, with the rule shown; taps Split to pull them
 * apart again. Challenge: pick the correct joined form / split; `rounds` right answers = win.
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const SEG = (typeof Intl !== 'undefined' && Intl.Segmenter) ? new Intl.Segmenter('hi', { granularity: 'grapheme' }) : null;
  const cl = s => SEG ? Array.from(SEG.segment(String(s)), x => x.segment) : Array.from(String(s));
  const isDeva = s => /[ऀ-ॿ]/.test(s);

  // where do part1 / part2 survive unchanged inside the result?
  function diff(p1, p2, r) {
    const A = cl(p1), B = cl(p2), R = cl(r);
    const capA = isDeva(r) ? A.length - 1 : A.length;
    let pre = 0; while (pre < capA && pre < R.length && A[pre] === R[pre]) pre++;
    let suf = 0; while (suf < B.length - 1 && suf < R.length - pre && B[B.length - 1 - suf] === R[R.length - 1 - suf]) suf++;
    return { k1: A.slice(0, pre).join(''), c1: A.slice(pre).join(''), c2: B.slice(0, B.length - suf).join(''), k2: B.slice(B.length - suf).join(''), mid: R.slice(pre, R.length - suf).join('') };
  }
  const MSW = [['ो', 'ौ'], ['े', 'ै'], ['ि', 'ी'], ['ु', 'ू'], ['ौ', 'ो'], ['ै', 'े'], ['ी', 'ि'], ['ू', 'ु']];
  const VSW = { 'अ': 'आ', 'आ': 'अ', 'इ': 'ई', 'ई': 'इ', 'उ': 'ऊ', 'ऊ': 'उ', 'ए': 'ऐ', 'ऐ': 'ए', 'ओ': 'औ', 'औ': 'ओ' };
  function wrongJoins(p1, p2, r) {
    const out = [];
    const cat = isDeva(p1) ? p1 + p2 : p1 + p2;
    out.push(cat);
    if (isDeva(r)) {
      const d = diff(p1, p2, r); const at = d.k1.length;               // mutate near the joint first
      const tries = [];
      MSW.forEach(([a, b]) => { let i = r.indexOf(a, Math.max(0, at - 1)); if (i < 0) i = r.indexOf(a); if (i >= 0) tries.push(r.slice(0, i) + b + r.slice(i + 1)); });
      const ia = r.indexOf('ा', Math.max(0, at - 1)); if (ia >= 0) tries.push(r.slice(0, ia) + r.slice(ia + 1));
      out.push(...shuffle(tries));
    } else {
      const ap = r.indexOf("'");
      if (ap > 0) { out.push(r.slice(0, ap - 1) + "'" + r[ap - 1] + r.slice(ap + 1)); out.push(r.replace("'", '')); }
      out.push(p1 + "'" + p2.slice(1));
    }
    return out;
  }
  function wrongSplits(p1, p2, r) {
    const out = [];
    if (VSW[p2[0]]) out.push(p1 + ' + ' + VSW[p2[0]] + p2.slice(1));
    const last = p1.slice(-1);
    if (last === 'ा') out.push(p1.slice(0, -1) + ' + ' + p2);
    else if (/[क-ह]/.test(last)) out.push(p1 + 'ा + ' + p2);
    MSW.forEach(([a, b]) => { if (last === a) out.push(p1.slice(0, -1) + b + ' + ' + p2); });
    const R = cl(r), d = diff(p1, p2, r), pre = cl(d.k1).length;
    const ks = shuffle(Array.from({ length: R.length - 1 }, (_, i) => i + 1)).sort((x, y) => Math.abs(x - pre - 1) - Math.abs(y - pre - 1));
    ks.forEach(k => out.push(R.slice(0, k).join('') + ' + ' + R.slice(k).join('')));
    return out;
  }
  function options(correct, extra, auto, n) {
    const seen = new Set([correct.replace(/\s+/g, ' ')]); const out = [correct];
    for (const o of (extra || []).concat(auto)) {
      const k = String(o).replace(/\s+/g, ' ').trim();
      if (!k || seen.has(k)) continue; seen.add(k); out.push(k); if (out.length >= n) break;
    }
    return shuffle(out);
  }

  Labs.register('sandhi', {
    title: 'Sandhi joiner',
    subjects: ['hindi', 'sanskrit', 'english'],
    render(host, p, api) {
      let P = (Array.isArray(p.pairs) ? p.pairs : []).filter(x => Array.isArray(x) && x[0] && x[1] && x[2])
        .map(x => ({ a: String(x[0]).trim(), b: String(x[1]).trim(), r: String(x[2]).trim(), rule: x[3] ? String(x[3]) : '', wj: Array.isArray(x[4]) ? x[4] : [], ws: Array.isArray(x[5]) ? x[5] : [] }));
      if (!P.length) P = Labs.registry.sandhi.example.pairs.map(x => ({ a: x[0], b: x[1], r: x[2], rule: x[3], wj: [], ws: [] }));
      const mode = ['join', 'split', 'both'].includes(p.mode) ? p.mode : 'both';
      const rounds = Math.max(1, Math.min(12, parseInt(p.rounds, 10) || Math.min(5, P.length)));
      const defCh = mode === 'join' ? `Pick the correct joined word ${rounds} times` : mode === 'split' ? `Pick the correct split ${rounds} times` : `Join and split correctly ${rounds} times`;
      const timers = []; const later = (f, ms) => timers.push(setTimeout(f, ms));

      host.innerHTML = `<style>
.lb-sandhi-w{color:#1b1f3a;font-size:15px;user-select:none;-webkit-user-select:none}
.lb-sandhi-ch{font-weight:800;margin:0 0 8px;line-height:1.3}
.lb-sandhi-box{background:linear-gradient(135deg,#f5f0ff,#eafff8);border-radius:20px;padding:8px 10px 10px}
.lb-sandhi-nav{display:flex;align-items:center;justify-content:space-between;gap:6px}
.lb-sandhi-nb{width:40px;height:40px;border:0;border-radius:12px;background:#fff;font-size:16px;font-weight:800;color:#8b5cf6;cursor:pointer}
.lb-sandhi-tt{font-weight:800;font-size:13px;color:#6b7090;text-align:center;flex:1}
.lb-sandhi-stage{height:84px;display:flex;align-items:center;justify-content:center;flex-wrap:nowrap;font-size:32px;font-weight:800;touch-action:none;overflow:hidden;white-space:nowrap}
.lb-sandhi-wd{display:inline-flex;align-items:center;background:#fff;border-radius:16px;padding:4px 10px;box-shadow:0 3px 0 #ddd6f6;transition:transform .35s cubic-bezier(.3,1.3,.5,1)}
.lb-sandhi-w2{cursor:grab}
.lb-sandhi-plus{display:inline-block;width:30px;text-align:center;color:#6b7090;transition:width .35s,opacity .3s;overflow:hidden}
.lb-sandhi-c1{color:#8b5cf6;background:#efe8ff;border-radius:8px;padding:0 2px;display:inline-block;transition:transform .35s,opacity .35s}
.lb-sandhi-c2{color:#e14d4d;background:#ffe9e9;border-radius:8px;padding:0 2px;display:inline-block;transition:transform .35s,opacity .35s}
.lb-sandhi-mid{color:#fff;background:#2ed3a5;border-radius:8px;padding:0 3px;display:inline-block;animation:lb-sandhi-pop .5s cubic-bezier(.2,1.6,.4,1)}
.lb-sandhi-stage.merge .lb-sandhi-plus{width:0;opacity:0}
.lb-sandhi-stage.merge .lb-sandhi-c1,.lb-sandhi-stage.merge .lb-sandhi-c2{transform:scale(.4) translateY(-14px);opacity:0}
.lb-sandhi-stage.enter .lb-sandhi-c1,.lb-sandhi-stage.enter .lb-sandhi-c2,.lb-sandhi-stage.enter .lb-sandhi-plus{animation:lb-sandhi-pop .45s cubic-bezier(.2,1.6,.4,1)}
@keyframes lb-sandhi-pop{from{transform:scale(.3);opacity:0}to{transform:scale(1);opacity:1}}
@keyframes lb-sandhi-shk{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
.lb-sandhi-rule{min-height:42px;text-align:center;font-size:14px;font-weight:700;color:#1b1f3a;line-height:1.35}
.lb-sandhi-rule .f{font-size:16px;font-weight:800}
.lb-sandhi-rule .f i{font-style:normal;border-radius:6px;padding:0 3px}
.lb-sandhi-rule .h{color:#6b7090;font-size:12px}
.lb-sandhi-act{display:flex;justify-content:center;gap:8px;margin-top:4px}
.lb-sandhi-btn{border:0;border-radius:14px;min-height:42px;padding:0 18px;font:inherit;font-weight:800;cursor:pointer}
.lb-sandhi-btn.j{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #6d3fd6}
.lb-sandhi-btn.s{background:#fff;color:#8b5cf6;box-shadow:0 3px 0 #ddd6f6}
.lb-sandhi-q{margin-top:10px;background:#fffaf0;border-radius:18px;padding:10px}
.lb-sandhi-qt{display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:13px;color:#6b7090}
.lb-sandhi-dots{display:flex;gap:4px}
.lb-sandhi-dot{width:12px;height:12px;border-radius:50%;background:#efe6cf;transition:background .3s}
.lb-sandhi-dot.on{background:#2ed3a5}
.lb-sandhi-qq{text-align:center;font-size:24px;font-weight:800;margin:6px 0 8px}
.lb-sandhi-qq b{color:#8b5cf6}
.lb-sandhi-opts{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.lb-sandhi-opt{min-height:48px;border:0;border-radius:14px;background:#fff;box-shadow:0 3px 0 #ecdcae;font:inherit;font-size:17px;font-weight:800;color:#1b1f3a;cursor:pointer;padding:4px;line-height:1.2;word-break:break-word}
.lb-sandhi-opt.ok{background:#2ed3a5;color:#fff;box-shadow:0 3px 0 #1fa983}
.lb-sandhi-opt.no{background:#ff6b6b;color:#fff;box-shadow:0 3px 0 #d94b4b;animation:lb-sandhi-shk .4s}
</style>
<div class="lb-sandhi-w">
  <div class="lb-sandhi-ch">🎯 Challenge: ${esc(p.challenge || defCh)}</div>
  <div class="lb-sandhi-box">
    <div class="lb-sandhi-nav"><button class="lb-sandhi-nb lb-sandhi-prev" aria-label="previous">◀</button><div class="lb-sandhi-tt"></div><button class="lb-sandhi-nb lb-sandhi-next" aria-label="next">▶</button></div>
    <div class="lb-sandhi-stage"></div>
    <div class="lb-sandhi-rule"></div>
    <div class="lb-sandhi-act"><button class="lb-sandhi-btn j">🔗 Join</button></div>
  </div>
  <div class="lb-sandhi-q"></div>
</div>`;
      const $ = s => host.querySelector(s);
      const stage = $('.lb-sandhi-stage'), rule = $('.lb-sandhi-rule'), btn = $('.lb-sandhi-btn'), tt = $('.lb-sandhi-tt'), qbox = $('.lb-sandhi-q');
      let idx = 0, joined = false, busy = false, score = 0, won = false;

      function drawParts(enter) {
        const x = P[idx], d = diff(x.a, x.b, x.r);
        stage.className = 'lb-sandhi-stage' + (enter ? ' enter' : '');
        stage.innerHTML = `<span class="lb-sandhi-wd lb-sandhi-w1">${esc(d.k1)}${d.c1 ? `<span class="lb-sandhi-c1">${esc(d.c1)}</span>` : ''}</span><span class="lb-sandhi-plus">+</span><span class="lb-sandhi-wd lb-sandhi-w2">${d.c2 ? `<span class="lb-sandhi-c2">${esc(d.c2)}</span>` : ''}${esc(d.k2)}</span>`;
        rule.innerHTML = '<div class="h">Drag the right word onto the left word, or tap Join</div>';
        btn.textContent = '🔗 Join'; btn.className = 'lb-sandhi-btn j';
        fit(); bindDrag();
      }
      function drawJoined() {
        const x = P[idx], d = diff(x.a, x.b, x.r);
        stage.className = 'lb-sandhi-stage';
        stage.innerHTML = `<span class="lb-sandhi-wd">${esc(d.k1)}<span class="lb-sandhi-mid">${esc(d.mid || '·')}</span>${esc(d.k2)}</span>`;
        rule.innerHTML = `<div class="f">${d.c1 ? `<i style="color:#8b5cf6;background:#efe8ff">${esc(d.c1)}</i> + ` : ''}<i style="color:#e14d4d;background:#ffe9e9">${esc(d.c2 || '∅')}</i> → <i style="color:#fff;background:#2ed3a5">${esc(d.mid || '∅')}</i> &nbsp; ${esc(x.a)} + ${esc(x.b)} = ${esc(x.r)}</div>${x.rule ? `<div>${esc(x.rule)}</div>` : ''}`;
        btn.textContent = '✂️ Split'; btn.className = 'lb-sandhi-btn s';
        fit();
      }
      function fit() {                                                  // shrink long words to fit the stage
        stage.style.fontSize = '32px';
        let f = 32; while (stage.scrollWidth > stage.clientWidth + 1 && f > 16) { f -= 2; stage.style.fontSize = f + 'px'; }
      }
      function setPair(i) {
        idx = (i + P.length) % P.length; joined = false; busy = false;
        tt.textContent = `${p.title || 'Sandhi'} · ${idx + 1} / ${P.length}`;
        drawParts(true);
      }
      function join() {
        if (busy) return; busy = true; api.sfx('tap');
        const w1 = stage.querySelector('.lb-sandhi-w1'), w2 = stage.querySelector('.lb-sandhi-w2');
        if (w1 && w2) { const g = w2.getBoundingClientRect().left - w1.getBoundingClientRect().right; w2.style.transform = `translateX(${-g + 4}px)`; }
        stage.classList.add('merge');
        later(() => { joined = true; busy = false; drawJoined(); api.sfx('correct'); api.speak(P[idx].r); }, 420);
      }
      function split() { if (busy) return; api.sfx('tap'); joined = false; drawParts(true); api.speak(P[idx].a + ', ' + P[idx].b); }
      btn.onclick = () => joined ? split() : join();
      $('.lb-sandhi-prev').onclick = () => { api.sfx('tap'); setPair(idx - 1); };
      $('.lb-sandhi-next').onclick = () => { api.sfx('tap'); setPair(idx + 1); };

      function bindDrag() {
        const w2 = stage.querySelector('.lb-sandhi-w2'); if (!w2) return;
        let st = null;
        w2.addEventListener('pointerdown', e => { if (busy) return; st = e.clientX; try { w2.setPointerCapture(e.pointerId); } catch (_) {} w2.style.transition = 'none'; });
        w2.addEventListener('pointermove', e => { if (st == null) return; const dx = Math.min(0, e.clientX - st); w2.style.transform = `translateX(${dx}px)`; });
        const end = e => {
          if (st == null) return; const dx = e.clientX - st; st = null; w2.style.transition = '';
          if (dx < -24) join(); else { w2.style.transform = ''; if (Math.abs(dx) < 6) api.speak(P[idx].b); }
        };
        w2.addEventListener('pointerup', end); w2.addEventListener('pointercancel', end);
      }

      // ---------- challenge ----------
      let deck = [];
      function nextQ() {
        if (!deck.length) deck = shuffle(P.map((x, i) => i));
        const i = deck.pop(), x = P[i];
        const kind = mode === 'both' ? (Math.random() < .5 ? 'join' : 'split') : mode;
        let q, correct, opts;
        if (kind === 'join') {
          correct = x.r; opts = options(correct, x.wj, wrongJoins(x.a, x.b, x.r), 3);
          q = `<b>${esc(x.a)}</b> + <b>${esc(x.b)}</b> = ?`;
        } else {
          correct = `${x.a} + ${x.b}`; opts = options(correct, x.ws, wrongSplits(x.a, x.b, x.r), 3);
          q = `<b>${esc(x.r)}</b> = ? + ?`;
        }
        qbox.innerHTML = `<div class="lb-sandhi-qt"><span>${kind === 'join' ? 'Join it' : 'Split it'}${isDeva(x.r) ? (kind === 'join' ? ' · सन्धि' : ' · सन्धि-विच्छेद') : ''}</span><span class="lb-sandhi-dots">${Array.from({ length: rounds }, (_, k) => `<i class="lb-sandhi-dot${k < score ? ' on' : ''}"></i>`).join('')}</span></div>
          <div class="lb-sandhi-qq">${q}</div>
          <div class="lb-sandhi-opts">${opts.map(o => `<button class="lb-sandhi-opt" data-o="${esc(o)}">${esc(o)}</button>`).join('')}</div>`;
        let locked = false;
        qbox.querySelectorAll('.lb-sandhi-opt').forEach(b => b.onclick = () => {
          if (locked) return; locked = true;
          const ok = b.dataset.o === correct;
          qbox.querySelectorAll('.lb-sandhi-opt').forEach(o => { if (o.dataset.o === correct) o.classList.add('ok'); });
          if (ok) {
            api.sfx('correct'); score++;
            const dd = qbox.querySelectorAll('.lb-sandhi-dot')[score - 1]; dd && dd.classList.add('on');
            api.speak(x.r);
            if (score >= rounds && !won) { won = true; later(() => api.win(isDeva(x.r) ? `बहुत बढ़िया! ${rounds} sandhi questions correct.` : `Well done! ${rounds} correct joins and splits.`), 500); }
          } else {
            b.classList.add('no'); api.sfx('wrong');
          }
          // show this pair on the stage and play the merge so the child sees why
          setPair(i); later(join, 450);
          later(nextQ, ok ? 1700 : 2600);
        });
      }
      setPair(0); nextQ();
      return () => { timers.forEach(clearTimeout); host.innerHTML = ''; };
    },
    example: {
      title: 'स्वर सन्धि',
      mode: 'both', rounds: 5,
      challenge: 'स्वर सन्धि — join and split 5 words correctly',
      pairs: [
        ['विद्या', 'आलय', 'विद्यालय', 'आ + आ = आ · दीर्घ सन्धि'],
        ['हिम', 'आलय', 'हिमालय', 'अ + आ = आ · दीर्घ सन्धि'],
        ['सूर्य', 'उदय', 'सूर्योदय', 'अ + उ = ओ · गुण सन्धि'],
        ['महा', 'ईश', 'महेश', 'आ + ई = ए · गुण सन्धि'],
        ['देव', 'इन्द्र', 'देवेन्द्र', 'अ + इ = ए · गुण सन्धि'],
        ['सदा', 'एव', 'सदैव', 'आ + ए = ऐ · वृद्धि सन्धि'],
        ['इति', 'आदि', 'इत्यादि', 'इ + आ = या · यण् सन्धि'],
        ['ने', 'अन', 'नयन', 'ए + अ = अय · अयादि सन्धि']
      ]
    },
    examples: [
      { title: 'Contractions', mode: 'both', rounds: 5, challenge: 'Join words into short forms (and split them back) — 5 right',
        pairs: [
          ['do', 'not', "don't", "The o of not is dropped — the apostrophe (') takes its place"],
          ['I', 'am', "I'm", "The a of am is dropped → '"],
          ['it', 'is', "it's", "The i of is is dropped → '"],
          ['we', 'will', "we'll", "wi is dropped → '"],
          ['they', 'are', "they're", "The a of are is dropped → '"],
          ['let', 'us', "let's", "The u of us is dropped → '"],
          ['can', 'not', "can't", "One n and the o are dropped → '"]
        ] },
      { title: 'व्यंजन · विसर्ग सन्धि', mode: 'split', rounds: 4, challenge: 'सन्धि-विच्छेद करो — pick the correct split 4 times',
        pairs: [
          ['जगत्', 'ईश', 'जगदीश', 'त् + स्वर → द् · व्यंजन सन्धि'],
          ['सत्', 'जन', 'सज्जन', 'त् + ज → ज्ज · व्यंजन सन्धि'],
          ['वाक्', 'ईश', 'वागीश', 'क् + स्वर → ग् · व्यंजन सन्धि'],
          ['उत्', 'नति', 'उन्नति', 'त् + न → न्न · व्यंजन सन्धि'],
          ['मनः', 'रथ', 'मनोरथ', 'अः + र → ओ · विसर्ग सन्धि'],
          ['निः', 'चल', 'निश्चल', 'ः + च → श्च · विसर्ग सन्धि'],
          ['नमः', 'ते', 'नमस्ते', 'ः + त → स्त · विसर्ग सन्धि'],
          ['दुः', 'आत्मा', 'दुरात्मा', 'ः + आ → र् · विसर्ग सन्धि']
        ] }
    ]
  });
})();
