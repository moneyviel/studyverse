/* Knowtopia Concept Lab — punctuation
 * A sentence or short passage appears with NO punctuation and no capital letters. The child taps the
 * gaps between words to insert marks ( . , ? ! ' " । …) and taps words to make Capital letters or add an
 * apostrophe (can't, Riya's). "Check" compares with the correct version from data; it is read aloud
 * when correct.
 *
 * PARAMS
 *  items     array of strings  the correctly punctuated sentences / passages, one per round. Curly quotes
 *                              are treated as straight quotes. Hindi/Sanskrit text works (no capitals).
 *                                                                     default: see example
 *  text      string            a single passage (used if items is missing)
 *  caps      boolean           the child must fix capital letters (words start in lower case)  default true
 *  keep      string            marks that stay already in place (e.g. ',' so the child only adds end marks)
 *                                                                     default '' (child adds everything)
 *  palette   array of strings  the mark buttons offered               default . , ? ! ' " (। instead of . for Hindi)
 *                              plus any other mark used in the text (; : – …)
 *  goal      number            rounds to solve to win                 default all items
 *  challenge string            challenge line                         default generated
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const MARKS = '.,?!\'";:।॥…–—';
  const isMark = ch => MARKS.includes(ch);
  const DEVA = /[ऀ-ॿ]/;
  const normQ = s => String(s || '').replace(/[“”„]/g, '"').replace(/[‘’‚]/g, "'");
  const hasCase = ch => !!ch && ch.toUpperCase() !== ch.toLowerCase();

  function parse(text, keep, caps) {
    text = normQ(text).trim();
    const toks = text.split(/\s+/).filter(Boolean);
    const words = []; const gaps = [''];
    for (const tk of toks) {
      let a = 0, b = tk.length;
      while (a < b && isMark(tk[a])) a++;
      while (b > a && isMark(tk[b - 1])) b--;
      const lead = tk.slice(0, a), trail = tk.slice(b);
      let core = tk.slice(a, b);
      if (!core) { gaps[gaps.length - 1] += tk; continue; }
      gaps[gaps.length - 1] += lead;
      let apos = -1; const ai = core.indexOf("'");
      if (ai > 0) { apos = ai; core = core.slice(0, ai) + core.slice(ai + 1); }
      const first = core[0];
      const allCaps = core.length > 1 && core === core.toUpperCase() && hasCase(first);
      const toggle = caps && hasCase(first) && !allCaps;
      const needCap = toggle && first === first.toUpperCase();
      const base = toggle ? first.toLowerCase() + core.slice(1) : core;
      words.push({ base, apos, needCap, toggle });
      gaps.push(trail);
    }
    // what is already filled in for the child
    const start = gaps.map(g => keep ? [...g].filter(c => keep.includes(c)).join('') : '');
    return { text, words, gaps, start };
  }

  Labs.register('punctuation', {
    title: 'Punctuation fixer',
    subjects: ['english', 'hindi'],
    render(host, p, api) {
      let items = Array.isArray(p.items) && p.items.length ? p.items.map(String) : (p.text ? [String(p.text)] : ['"Where are you going, Riya?" asked Mother.']);
      items = items.filter(t => t.trim());
      const caps = p.caps !== false, keep = typeof p.keep === 'string' ? normQ(p.keep) : '';
      const goal = Math.max(1, Math.min(items.length, +p.goal || items.length));
      const challenge = p.challenge || `Add the missing punctuation${caps ? ' and capital letters' : ''} — ${goal} sentence${goal > 1 ? 's' : ''}`;

      host.innerHTML = `<style>
.lb-punctuation-w{color:#1b1f3a;max-width:400px;margin:0 auto}
.lb-punctuation-ch{font-weight:800;font-size:13.5px;background:#fff7dd;border-radius:12px;padding:7px 10px;margin-bottom:7px;line-height:1.3}
.lb-punctuation-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px}
.lb-punctuation-dots{display:flex;gap:5px}.lb-punctuation-dots i{width:11px;height:11px;border-radius:50%;background:#e6e8f5}.lb-punctuation-dots i.on{background:#2ed3a5}
.lb-punctuation-leg{font-size:11.5px;font-weight:800;color:#6b7090}
.lb-punctuation-pas{background:#f8f9ff;border:2px solid #e6e8f5;border-radius:16px;padding:6px 4px;display:flex;flex-wrap:wrap;align-items:center;row-gap:2px;transition:border-color .3s,background .3s}
.lb-punctuation-pas.ok{border-color:#2ed3a5;background:#e9fbf5}
.lb-punctuation-u{display:inline-flex;align-items:center;white-space:nowrap}
.lb-punctuation-g,.lb-punctuation-wd{border:none;font-family:inherit;cursor:pointer;height:40px;background:none;color:#1b1f3a;display:inline-flex;align-items:center;justify-content:center;border-radius:10px;padding:0}
.lb-punctuation-g{min-width:20px;font-weight:900;font-size:23px;color:#ff4f4f;padding:0 1px}
.lb-punctuation-g:empty::after{content:'';width:7px;height:7px;border-radius:50%;border:2px solid #c9cde6;background:#fff}
.lb-punctuation-wd{font-weight:800;font-size:18px;padding:0 3px}
.lb-punctuation-wd .cap{color:#8b5cf6}
.lb-punctuation-wd .ap{color:#ff6b6b;font-weight:900}
.lb-punctuation-g.sel,.lb-punctuation-wd.sel{background:#ffc93c;color:#1b1f3a;box-shadow:0 0 0 2px #d9a300 inset}
.lb-punctuation-g.sel:empty::after{border-color:#1b1f3a;background:#ffc93c}
.lb-punctuation-bad{animation:lbpcbad .9s ease 2;box-shadow:0 0 0 2px #ff6b6b inset;background:#ffeded}
@keyframes lbpcbad{50%{background:#ffc9c9}}
.lb-punctuation-fixd{background:#d9f7ee}
.lb-punctuation-prev{font-size:13px;font-weight:700;color:#6b7090;margin:6px 2px 0;line-height:1.35;min-height:18px}
.lb-punctuation-prev b{color:#1b1f3a}
.lb-punctuation-tool{margin-top:8px;background:#f1ecff;border-radius:14px;padding:7px;min-height:58px;display:flex;flex-wrap:wrap;gap:6px;align-items:center;justify-content:center}
.lb-punctuation-tip{font-size:13px;font-weight:800;color:#7a6bb5;text-align:center}
.lb-punctuation-m{border:none;font-family:inherit;min-width:42px;height:42px;border-radius:12px;background:#fff;color:#1b1f3a;font-size:22px;font-weight:900;cursor:pointer;box-shadow:0 3px 0 #d6cff5;padding:0 8px}
.lb-punctuation-m.txt{font-size:14px;font-weight:800}
.lb-punctuation-m.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-punctuation-m.del{background:#ffeded;color:#d64545;box-shadow:0 3px 0 #f3c4c4;font-size:17px}
.lb-punctuation-m:active{transform:translateY(2px)}
.lb-punctuation-btns{display:flex;gap:6px;margin-top:8px}
.lb-punctuation-b{flex:1;border:none;font-family:inherit;font-weight:800;font-size:14.5px;min-height:42px;border-radius:13px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef}
.lb-punctuation-b.go{background:#2ed3a5;color:#fff;box-shadow:0 3px 0 #1a9c78;flex:1.4}
.lb-punctuation-b:active{transform:translateY(2px)}
.lb-punctuation-fb{min-height:18px;text-align:center;font-weight:800;font-size:13.5px;margin-top:6px;line-height:1.3}
.lb-punctuation-fb.ok{color:#0f7a5c}.lb-punctuation-fb.no{color:#d64545}
</style>
<div class="lb-punctuation-w">
  <div class="lb-punctuation-ch">🎯 Challenge: ${esc(challenge)}</div>
  <div class="lb-punctuation-top"><div class="lb-punctuation-dots"></div><div class="lb-punctuation-leg">Tap a ○ gap or a word</div></div>
  <div class="lb-punctuation-pas"></div>
  <div class="lb-punctuation-prev"></div>
  <div class="lb-punctuation-tool"></div>
  <div class="lb-punctuation-btns">
    <button class="lb-punctuation-b" data-a="reset">↺ Clear</button>
    <button class="lb-punctuation-b" data-a="hint">💡 Hint</button>
    <button class="lb-punctuation-b go" data-a="check">✔ Check</button>
  </div>
  <div class="lb-punctuation-fb"></div>
</div>`;
      const $ = s => host.querySelector(s);
      const pas = $('.lb-punctuation-pas'), prev = $('.lb-punctuation-prev'), tool = $('.lb-punctuation-tool'), fb = $('.lb-punctuation-fb'), dots = $('.lb-punctuation-dots');
      let idx = 0, solved = 0, won = false, done = false;
      let D, G, W, sel = null, aposOpen = false, palette = [];
      const timers = [];

      function setup() {
        D = parse(items[idx % items.length], keep, caps);
        G = D.start.slice();
        W = D.words.map(w => ({ cap: false, apos: -1 }));
        sel = null; aposOpen = false; done = false;
        const deva = DEVA.test(D.text);
        const base = Array.isArray(p.palette) && p.palette.length ? p.palette.map(normQ) : (deva ? ['।', ',', '?', '!', '"', "'"] : ['.', ',', '?', '!', "'", '"']);
        const extra = [...new Set(D.gaps.join(''))].filter(c => !base.includes(c));
        palette = base.concat(extra);
        pas.classList.remove('ok');
        const b = host.querySelector('[data-a="next"]'); if (b) { b.dataset.a = 'check'; b.textContent = '✔ Check'; }
        say('');
        drawDots(); draw();
      }
      function drawDots() { dots.innerHTML = Array.from({ length: goal }, (_, i) => `<i class="${i < solved ? 'on' : ''}"></i>`).join(''); }
      function say(t, c) { fb.textContent = t; fb.className = 'lb-punctuation-fb ' + (c || ''); }

      function wordText(i, html) {
        const w = D.words[i], s = W[i];
        let core = w.base;
        let first = core[0], rest = core.slice(1);
        if (w.toggle && s.cap) first = first.toUpperCase();
        if (!html) { let t = first + rest; if (s.apos > 0) t = t.slice(0, s.apos) + "'" + t.slice(s.apos); return t; }
        let t = (w.toggle && s.cap ? `<span class="cap">${esc(first)}</span>` : esc(first));
        const chars = [...rest];
        // insert apostrophe (position counts from start of the word)
        let out = '';
        const restStr = rest;
        for (let k = 0; k <= restStr.length; k++) {
          if (s.apos === k + 1) out += '<span class="ap">\'</span>';
          if (k < restStr.length) out += esc(restStr[k]);
        }
        void chars;
        return t + out;
      }
      function sentence() {
        // a " is an opening quote when an even number of " came before it: it then sits before the next word
        let dq = 0;
        const split = g => { let tr = '', ld = ''; for (const c of g) { if (c === '"') { if (dq % 2 === 0) ld += c; else (ld ? ld += c : tr += c); dq++; } else (ld ? ld += c : tr += c); } return [tr, ld]; };
        let s = split(G[0]).join('');
        D.words.forEach((_, i) => { const [tr, ld] = split(G[i + 1]); s += wordText(i, false) + tr + (i < D.words.length - 1 ? ' ' : '') + ld; });
        return s.replace(/\s+/g, ' ').trim();
      }

      function draw() {
        let h = '';
        const n = D.words.length;
        // unit = [gap0] word0 gap1 | word1 gap2 | ...
        for (let i = 0; i < n; i++) {
          h += '<span class="lb-punctuation-u">';
          if (i === 0) h += gapBtn(0);
          h += `<button class="lb-punctuation-wd${sel && sel.w === i ? ' sel' : ''}" data-w="${i}">${wordText(i, true)}</button>`;
          h += gapBtn(i + 1);
          h += '</span>';
        }
        pas.innerHTML = h;
        const s = sentence();
        prev.innerHTML = s ? `Reads as: <b>${esc(s)}</b>` : '';
        drawTool();
      }
      function gapBtn(g) { return `<button class="lb-punctuation-g${sel && sel.g === g ? ' sel' : ''}" data-g="${g}" aria-label="gap ${g}">${esc(G[g])}</button>`; }

      function drawTool() {
        if (done) { tool.innerHTML = `<button class="lb-punctuation-m txt" data-a="say">🔊 Hear it again</button>`; return; }
        if (!sel) { tool.innerHTML = `<div class="lb-punctuation-tip">👆 Tap a circle ○ between words to add a mark${D.words.some(w => w.toggle) ? ',<br>or tap a word for a Capital letter' : ''}</div>`; return; }
        if (sel.g != null) {
          tool.innerHTML = palette.map(m => `<button class="lb-punctuation-m" data-m="${esc(m)}" aria-label="add ${esc(m)}">${esc(m)}</button>`).join('') +
            `<button class="lb-punctuation-m del" data-a="del" aria-label="remove mark">⌫</button>`;
          return;
        }
        const i = sel.w, w = D.words[i], s = W[i];
        if (aposOpen) {
          const L = [...w.base].length;
          let opts = '';
          for (let k = 1; k < L; k++) {
            const tmp = wordText(i, false).replace("'", '');
            opts += `<button class="lb-punctuation-m txt${s.apos === k ? ' on' : ''}" data-ap="${k}">${esc(tmp.slice(0, k) + "'" + tmp.slice(k))}</button>`;
          }
          tool.innerHTML = opts + `<button class="lb-punctuation-m txt${s.apos < 0 ? ' on' : ''}" data-ap="-1">no '</button><button class="lb-punctuation-m del txt" data-a="apback">↩</button>`;
          return;
        }
        let t = '';
        if (w.toggle) t += `<button class="lb-punctuation-m txt${s.cap ? ' on' : ''}" data-a="cap">${s.cap ? 'A → a' : 'a → A'} Capital</button>`;
        if ([...w.base].length > 1) t += `<button class="lb-punctuation-m txt" data-a="apopen">' Apostrophe…</button>`;
        tool.innerHTML = t || `<div class="lb-punctuation-tip">Nothing to change in this word — try a gap.</div>`;
      }

      function mistakes() {
        const bad = [];
        D.gaps.forEach((g, i) => { if (G[i] !== g) bad.push({ g: i }); });
        D.words.forEach((w, i) => {
          if (w.toggle && W[i].cap !== w.needCap) bad.push({ w: i, k: 'cap' });
          if (W[i].apos !== w.apos) bad.push({ w: i, k: 'apos' });
        });
        return bad;
      }
      function flash(list) {
        list.forEach(b => {
          const el = b.g != null ? pas.querySelector(`[data-g="${b.g}"]`) : pas.querySelector(`[data-w="${b.w}"]`);
          if (el) el.classList.add('lb-punctuation-bad');
        });
      }
      function check() {
        if (done) return;
        const bad = mistakes();
        if (!bad.length) {
          done = true; solved++; sel = null; draw(); pas.classList.add('ok');
          api.sfx('correct'); api.speak(D.text);
          say('✅ Perfect punctuation!', 'ok'); drawDots();
          if (solved >= goal && !won) { won = true; api.win(`Punctuation pro! You fixed ${goal} sentence${goal > 1 ? 's' : ''}.`); }
          const b = host.querySelector('[data-a="check"]'); b.dataset.a = 'next'; b.textContent = '➜ Next';
          return;
        }
        api.sfx('wrong'); sel = null; draw(); flash(bad);
        say(`${bad.length} thing${bad.length > 1 ? 's' : ''} to fix — look for the red spots.`, 'no');
      }
      function hint() {
        if (done) return;
        const bad = mistakes(); if (!bad.length) { say('Looks right — press Check!', 'ok'); return; }
        // prefer a missing capital or end mark: first mistake in reading order
        const b = bad.sort((x, y) => ((x.g != null ? x.g * 2 : x.w * 2 + 1) - (y.g != null ? y.g * 2 : y.w * 2 + 1)))[0];
        let msg;
        if (b.g != null) { G[b.g] = D.gaps[b.g]; msg = D.gaps[b.g] ? `Added “${D.gaps[b.g]}” here.` : 'No mark is needed in that gap.'; }
        else if (b.k === 'cap') { W[b.w].cap = D.words[b.w].needCap; msg = D.words[b.w].needCap ? 'That word needs a Capital letter.' : 'That word should be small.'; }
        else { W[b.w].apos = D.words[b.w].apos; msg = 'Fixed the apostrophe.'; }
        sel = null; draw(); api.sfx('hmm'); say('💡 ' + msg, '');
        const el = b.g != null ? pas.querySelector(`[data-g="${b.g}"]`) : pas.querySelector(`[data-w="${b.w}"]`);
        if (el) el.classList.add('lb-punctuation-fixd');
      }

      function onClick(e) {
        const t = e.target.closest('button'); if (!t || !host.contains(t)) return;
        const a = t.dataset.a;
        if (a === 'check') return check();
        if (a === 'next') { idx++; return setup(); }
        if (a === 'hint') return hint();
        if (a === 'say') { api.speak(D.text); return; }
        if (a === 'reset') { if (!done) { G = D.start.slice(); W = D.words.map(() => ({ cap: false, apos: -1 })); sel = null; say(''); draw(); } return; }
        if (done) return;
        if (t.dataset.g != null) { const g = +t.dataset.g; sel = sel && sel.g === g ? null : { g }; aposOpen = false; api.sfx('tap'); draw(); return; }
        if (t.dataset.w != null) {
          const i = +t.dataset.w; aposOpen = false;
          // quick action: tapping a word that only can change case toggles it straight away when already selected
          if (sel && sel.w === i && D.words[i].toggle) { W[i].cap = !W[i].cap; }
          sel = { w: i }; api.sfx('tap'); say(''); draw(); return;
        }
        if (t.dataset.m != null && sel && sel.g != null) { G[sel.g] += t.dataset.m; api.sfx('tap'); say(''); draw(); return; }
        if (a === 'del' && sel && sel.g != null) { G[sel.g] = [...G[sel.g]].slice(0, -1).join(''); api.sfx('tap'); draw(); return; }
        if (a === 'cap' && sel && sel.w != null) { W[sel.w].cap = !W[sel.w].cap; api.sfx('tap'); say(''); draw(); return; }
        if (a === 'apopen') { aposOpen = true; drawTool(); return; }
        if (a === 'apback') { aposOpen = false; drawTool(); return; }
        if (t.dataset.ap != null && sel && sel.w != null) { W[sel.w].apos = +t.dataset.ap; aposOpen = false; api.sfx('tap'); say(''); draw(); return; }
      }
      host.addEventListener('click', onClick);
      setup();
      return () => { host.removeEventListener('click', onClick); timers.forEach(clearTimeout); };
    },
    example: {
      challenge: 'Add capital letters, commas, question marks, apostrophes and speech marks',
      items: [
        '"Where are you going, Riya?" asked Mother.',
        "I can't find Ravi's red bag.",
        'Wow, what a lovely kite!'
      ]
    },
    examples: [
      {
        challenge: 'Start with a capital letter and end with a full stop',
        items: ['My name is Anu. I live in Delhi.', 'The dog is big.'],
        goal: 2
      },
      {
        challenge: 'सही विराम चिह्न लगाओ ( । , ? ! )',
        items: ['क्या तुम मेरे साथ चलोगे? हाँ, मैं चलूँगा।', 'वाह! कितना सुंदर फूल है।'],
        goal: 2
      },
      {
        challenge: 'Punctuate the passage: commas in a list, a question and speech marks',
        items: ['We bought apples, bananas and grapes. "Are they sweet?" asked Kabir.'],
        goal: 1
      }
    ]
  });
})();
