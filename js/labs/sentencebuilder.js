/* Knowtopia Concept Lab — sentencebuilder
 * The child taps shuffled word chips to build a sentence in the right order, then checks it.
 * Works for any language (English, Hindi, Sanskrit...). Correct sentences are read aloud.
 *
 * PARAMS
 *  mode       string  'order' | 'kinds' | 'transform'                                 default 'order'
 *               order     – put the words of each sentence in order.
 *               kinds     – put words in order AND choose the kind of sentence + its end mark.
 *               transform – a source sentence is shown (e.g. active voice); build its pair
 *                           (e.g. passive voice) from the word chips.
 *  items      array   the rounds. Each item may be a plain string (the correct sentence) or an object:
 *               { text: 'The cat sat on the mat.',   // correct sentence (end mark included)
 *                 alt:  ['On the mat sat the cat.'], // other accepted orders (optional)
 *                 kind: 'statement',                 // kinds mode: statement|question|exclamation|command
 *                 from: 'The cat chased the rat.',   // transform mode: source sentence (text = target)
 *                 hint: 'Who did what?',             // optional clue line
 *                 meaning: '…' }                     // optional translation shown when solved
 *             The end mark (. ? ! । ॥) is split off as its own fixed piece.     default: see example
 *  fromLabel  string  transform mode: tag for the source, e.g. 'Active' / 'Direct'        default 'Given'
 *  toLabel    string  transform mode: tag for the target, e.g. 'Passive' / 'Reported'    default 'Make'
 *  kindLabels object  names shown on the kind buttons, e.g. {statement:'विधानवाचक'}       default English
 *  extra      array   distractor words added to every round's chips (optional)           default []
 *  goal       number  how many rounds must be solved to win                               default all items
 *  shuffle    boolean shuffle round order                                                 default false
 *  challenge  string  challenge line                                     default generated from mode/goal
 */
(function () {
  const END = /([.?!।॥]+)\s*$/;
  const DEVA = /[ऀ-ॿ]/;
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const KINDS = ['statement', 'question', 'exclamation', 'command'];
  const KDEF = { statement: 'Statement', question: 'Question', exclamation: 'Exclamation', command: 'Command' };
  const KICON = { statement: '💬', question: '❓', exclamation: '😲', command: '👉' };

  function splitSentence(t) {
    t = String(t || '').trim();
    const m = t.match(END); const mark = m ? m[1] : '';
    const body = m ? t.slice(0, m.index).trim() : t;
    return { words: body.split(/\s+/).filter(Boolean), mark };
  }
  function shuffled(arr, avoid) {
    for (let k = 0; k < 8; k++) {
      const a = arr.slice();
      for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
      if (!avoid || a.length < 2 || a.join('\u0001') !== avoid.join('\u0001')) return a;
    }
    return arr.slice().reverse();
  }

  Labs.register('sentencebuilder', {
    title: 'Sentence builder',
    subjects: ['english', 'hindi', 'sanskrit'],
    render(host, p, api) {
      const mode = ['order', 'kinds', 'transform'].includes(p.mode) ? p.mode : 'order';
      let items = (Array.isArray(p.items) && p.items.length ? p.items : ['The cat sat on the mat.'])
        .map(it => typeof it === 'string' ? { text: it } : Object.assign({}, it))
        .filter(it => it.text);
      if (!items.length) items = [{ text: 'The cat sat on the mat.' }];
      if (p.shuffle) items = shuffled(items);
      const goal = Math.max(1, Math.min(items.length, +p.goal || items.length));
      const kl = Object.assign({}, KDEF, p.kindLabels || {});
      const extra = Array.isArray(p.extra) ? p.extra.map(String) : [];
      const challenge = p.challenge || (mode === 'kinds' ? `Build ${goal} sentence${goal > 1 ? 's' : ''} and pick the right kind and end mark`
        : mode === 'transform' ? `Change ${goal} sentence${goal > 1 ? 's' : ''} from ${p.fromLabel || 'given'} to ${p.toLabel || 'the new form'}`
        : `Put the words in order for ${goal} sentence${goal > 1 ? 's' : ''}`);

      host.innerHTML = `<style>
.lb-sentencebuilder-w{font-family:inherit;color:#1b1f3a;max-width:400px;margin:0 auto}
.lb-sentencebuilder-ch{font-weight:800;font-size:13.5px;background:#fff7dd;border-radius:12px;padding:7px 10px;margin-bottom:8px;line-height:1.3}
.lb-sentencebuilder-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;gap:6px}
.lb-sentencebuilder-dots{display:flex;gap:5px}
.lb-sentencebuilder-dots i{width:11px;height:11px;border-radius:50%;background:#e6e8f5;transition:background .3s,transform .3s}
.lb-sentencebuilder-dots i.on{background:#2ed3a5;transform:scale(1.15)}
.lb-sentencebuilder-dots i.cur{box-shadow:0 0 0 2px #8b5cf6}
.lb-sentencebuilder-rd{font-size:12px;font-weight:800;color:#6b7090}
.lb-sentencebuilder-src{background:#eef4ff;border-radius:14px;padding:8px 10px;margin-bottom:8px;font-weight:700;font-size:15px;line-height:1.35}
.lb-sentencebuilder-tag{display:inline-block;font-size:11px;font-weight:800;color:#fff;background:#3b82f6;border-radius:8px;padding:2px 7px;margin-right:6px;vertical-align:1px}
.lb-sentencebuilder-tag.to{background:#8b5cf6}
.lb-sentencebuilder-hint{font-size:12.5px;color:#6b7090;font-weight:700;margin:-2px 0 6px}
.lb-sentencebuilder-line{min-height:84px;border-radius:16px;background:#f6f4ff;border:2px dashed #cfc3fb;padding:8px;display:flex;flex-wrap:wrap;align-content:flex-start;gap:6px;transition:border-color .25s,background .25s}
.lb-sentencebuilder-w.kinds .lb-sentencebuilder-line{min-height:58px}
.lb-sentencebuilder-w.kinds .lb-sentencebuilder-tray{margin:8px 0 6px}
.lb-sentencebuilder-line.ok{border-color:#2ed3a5;border-style:solid;background:#e9fbf5}
.lb-sentencebuilder-line.bad{animation:lbsbshake .35s}
@keyframes lbsbshake{25%{transform:translateX(-6px)}50%{transform:translateX(6px)}75%{transform:translateX(-3px)}}
.lb-sentencebuilder-ph{color:#a4a8c6;font-weight:700;font-size:13.5px;align-self:center;margin:auto}
.lb-sentencebuilder-chip{border:none;font-family:inherit;font-weight:800;font-size:16.5px;min-height:40px;padding:6px 12px;border-radius:12px;cursor:pointer;background:#fff;color:#1b1f3a;box-shadow:0 3px 0 #d6d9ee,0 0 0 2px #e3e6f6 inset;animation:lbsbin .22s ease;line-height:1.2}
.lb-sentencebuilder-line .lb-sentencebuilder-chip{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-sentencebuilder-line .lb-sentencebuilder-chip.wrong{background:#ff6b6b;box-shadow:0 3px 0 #c94444}
.lb-sentencebuilder-line .lb-sentencebuilder-chip.right{background:#2ed3a5;box-shadow:0 3px 0 #1a9c78}
.lb-sentencebuilder-chip:active{transform:translateY(2px)}
.lb-sentencebuilder-mark{min-width:40px;min-height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;color:#1b1f3a;background:#ffe9a8}
.lb-sentencebuilder-mark.q{background:#fff;border:2px dashed #ffc93c;color:#c99500;font-size:16px}
@keyframes lbsbin{from{transform:scale(.6);opacity:0}to{transform:none;opacity:1}}
.lb-sentencebuilder-tray{display:flex;flex-wrap:wrap;gap:7px;justify-content:center;min-height:48px;margin:10px 0 8px}
.lb-sentencebuilder-kinds{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;margin-bottom:7px}
.lb-sentencebuilder-k{border:none;font-family:inherit;font-weight:800;font-size:11.5px;min-height:46px;border-radius:12px;cursor:pointer;background:#eef0fb;color:#1b1f3a;padding:3px 2px;line-height:1.1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;overflow:hidden;word-break:break-word}
.lb-sentencebuilder-k i{font-style:normal;font-size:16px}
.lb-sentencebuilder-k.on{background:#3b82f6;color:#fff}
.lb-sentencebuilder-marks{display:flex;gap:6px;justify-content:center;margin-bottom:8px}
.lb-sentencebuilder-m{border:none;font-family:inherit;font-weight:900;font-size:22px;width:48px;height:42px;border-radius:12px;cursor:pointer;background:#fff7dd;color:#1b1f3a;box-shadow:0 0 0 2px #ffe08a inset}
.lb-sentencebuilder-m.on{background:#ffc93c;box-shadow:0 3px 0 #d9a300}
.lb-sentencebuilder-btns{display:flex;gap:6px}
.lb-sentencebuilder-b{flex:1;border:none;font-family:inherit;font-weight:800;font-size:14.5px;min-height:42px;border-radius:13px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 3px 0 #d3d7ef}
.lb-sentencebuilder-b.go{background:#2ed3a5;color:#fff;box-shadow:0 3px 0 #1a9c78;flex:1.4}
.lb-sentencebuilder-b:active{transform:translateY(2px)}
.lb-sentencebuilder-b:disabled{opacity:.45}
.lb-sentencebuilder-fb{min-height:20px;font-weight:800;font-size:13.5px;text-align:center;margin:7px 0 0;line-height:1.3}
.lb-sentencebuilder-fb.ok{color:#0f7a5c}.lb-sentencebuilder-fb.no{color:#d64545}
</style>
<div class="lb-sentencebuilder-w${mode === 'kinds' ? ' kinds' : ''}">
  <div class="lb-sentencebuilder-ch">🎯 Challenge: ${esc(challenge)}</div>
  <div class="lb-sentencebuilder-top"><div class="lb-sentencebuilder-dots"></div><div class="lb-sentencebuilder-rd"></div></div>
  <div class="lb-sentencebuilder-srcbox"></div>
  <div class="lb-sentencebuilder-line" aria-live="polite"></div>
  <div class="lb-sentencebuilder-tray"></div>
  <div class="lb-sentencebuilder-kindbox"></div>
  <div class="lb-sentencebuilder-btns">
    <button class="lb-sentencebuilder-b" data-a="undo">↩ Undo</button>
    <button class="lb-sentencebuilder-b" data-a="hint">💡 Hint</button>
    <button class="lb-sentencebuilder-b go" data-a="check">✔ Check</button>
  </div>
  <div class="lb-sentencebuilder-fb"></div>
</div>`;
      const $ = s => host.querySelector(s);
      const line = $('.lb-sentencebuilder-line'), tray = $('.lb-sentencebuilder-tray'), fb = $('.lb-sentencebuilder-fb');
      const srcbox = $('.lb-sentencebuilder-srcbox'), kindbox = $('.lb-sentencebuilder-kindbox');
      const dotsEl = $('.lb-sentencebuilder-dots'), rdEl = $('.lb-sentencebuilder-rd');
      const checkBtn = $('[data-a="check"]');

      let idx = 0, solvedCount = 0, solved = false, won = false;
      let R = null; // current round state
      const timers = [];

      function setupRound() {
        const it = items[idx % items.length];
        const sp = splitSentence(it.text);
        const deva = DEVA.test(it.text);
        const alts = [sp.words].concat((it.alt || []).map(a => splitSentence(a).words));
        let pool = sp.words.concat(extra).map((w, i) => ({ w, id: i }));
        pool = shuffled(pool, null);
        if (pool.map(x => x.w).join(' ') === sp.words.join(' ') && pool.length > 1) pool.reverse();
        const kind = KINDS.includes(it.kind) ? it.kind : (sp.mark.includes('?') ? 'question' : sp.mark.includes('!') ? 'exclamation' : 'statement');
        R = { it, sp, deva, alts, pool, built: [], kind, pickKind: null, pickMark: null };
        solved = false; line.classList.remove('ok');
        fb.textContent = ''; fb.className = 'lb-sentencebuilder-fb';
        checkBtn.disabled = false;
        // source sentence / hint
        let src = '';
        if (mode === 'transform' && it.from) src = `<div class="lb-sentencebuilder-src"><span class="lb-sentencebuilder-tag">${esc(p.fromLabel || 'Given')}</span>${esc(it.from)}<br><span class="lb-sentencebuilder-tag to" style="margin-top:5px">${esc(p.toLabel || 'Make')}</span><span style="color:#6b7090;font-size:13px">build it below ↓</span></div>`;
        if (it.hint) src += `<div class="lb-sentencebuilder-hint">💡 ${esc(it.hint)}</div>`;
        srcbox.innerHTML = src;
        // kinds UI
        if (mode === 'kinds') {
          const marks = [deva ? '।' : '.', '?', '!'];
          kindbox.innerHTML = `<div class="lb-sentencebuilder-kinds">${KINDS.map(k => `<button class="lb-sentencebuilder-k" data-k="${k}"><i>${KICON[k]}</i>${esc(kl[k])}</button>`).join('')}</div>
            <div class="lb-sentencebuilder-marks">${marks.map(m => `<button class="lb-sentencebuilder-m" data-m="${esc(m)}" aria-label="end mark ${esc(m)}">${esc(m)}</button>`).join('')}</div>`;
        } else kindbox.innerHTML = '';
        drawDots(); draw();
      }

      function drawDots() {
        dotsEl.innerHTML = Array.from({ length: goal }, (_, i) => `<i class="${i < solvedCount ? 'on' : ''} ${i === solvedCount && !won ? 'cur' : ''}"></i>`).join('');
        rdEl.textContent = `Sentence ${Math.min(idx + 1, items.length)} of ${items.length}`;
      }

      function currentMark() { return mode === 'kinds' ? (R.pickMark || '') : R.sp.mark; }

      function draw() {
        line.innerHTML = R.built.length ? R.built.map((x, i) => `<button class="lb-sentencebuilder-chip" data-b="${i}">${esc(x.w)}</button>`).join('')
          : `<span class="lb-sentencebuilder-ph">Tap the words below in the right order</span>`;
        const mk = currentMark();
        if (R.built.length || mode === 'kinds') {
          if (mk) line.insertAdjacentHTML('beforeend', `<span class="lb-sentencebuilder-mark">${esc(mk)}</span>`);
          else if (mode === 'kinds') line.insertAdjacentHTML('beforeend', `<span class="lb-sentencebuilder-mark q">?.!</span>`);
        }
        const used = new Set(R.built.map(x => x.id));
        tray.innerHTML = R.pool.filter(x => !used.has(x.id)).map(x => `<button class="lb-sentencebuilder-chip" data-t="${x.id}">${esc(x.w)}</button>`).join('')
          || `<span class="lb-sentencebuilder-ph" style="font-size:12.5px">All words placed — press Check ✔</span>`;
        kindbox.querySelectorAll('[data-k]').forEach(b => b.classList.toggle('on', b.dataset.k === R.pickKind));
        kindbox.querySelectorAll('[data-m]').forEach(b => b.classList.toggle('on', b.dataset.m === R.pickMark));
      }

      function say(t, cls) { fb.textContent = t; fb.className = 'lb-sentencebuilder-fb ' + (cls || ''); }

      function matchAlt() {
        const b = R.built.map(x => x.w).join('\u0001');
        return R.alts.some(a => a.join('\u0001') === b);
      }
      function okMark() {
        if (mode !== 'kinds') return true;
        const mk = R.pickMark || '';
        const want = R.sp.mark || (R.deva ? '।' : '.');
        if (R.kind === 'command') return mk === want || mk === '!' || mk === '.' || mk === '।';
        return mk === want;
      }

      function check() {
        if (solved) return;
        const nWords = R.sp.words.length;
        if (R.built.length < nWords) { say(`Use all the words first (${R.built.length}/${nWords}).`, 'no'); api.sfx('hmm'); return; }
        const orderOK = R.built.length === nWords && matchAlt();
        const kindOK = mode !== 'kinds' || R.pickKind === R.kind;
        const markOK = okMark();
        if (orderOK && kindOK && markOK) return success();
        api.sfx('wrong');
        line.classList.remove('bad'); void line.offsetWidth; line.classList.add('bad');
        if (!orderOK) {
          // mark the chips that are in the wrong place (against the main answer)
          const main = R.sp.words;
          line.querySelectorAll('[data-b]').forEach((el, i) => el.classList.add(R.built[i] && R.built[i].w === main[i] ? 'right' : 'wrong'));
          say('Red words are in the wrong place — tap to send back.', 'no');
        } else if (!kindOK) say(mode === 'kinds' && !R.pickKind ? 'Words are right! Now pick the kind of sentence.' : 'Word order is right — but think again about the kind of sentence.', 'no');
        else say(R.pickMark ? 'Nearly! Check the end mark.' : 'Words are right! Now pick the end mark.', 'no');
      }

      function success() {
        solved = true; solvedCount++;
        draw();
        line.classList.add('ok');
        line.querySelectorAll('[data-b]').forEach(el => el.classList.add('right'));
        checkBtn.disabled = true;
        api.sfx('correct');
        const full = R.built.map(x => x.w).join(' ') + currentMark();
        api.speak(full);
        const extraMsg = mode === 'kinds' ? ` It is ${/^[aeiou]/i.test(kl[R.kind]) ? 'an' : 'a'} ${kl[R.kind]}.` : '';
        say('✅ Correct!' + extraMsg + (R.it.meaning ? ' — ' + R.it.meaning : ''), 'ok');
        drawDots();
        if (solvedCount >= goal && !won) {
          won = true; drawDots();
          api.win(mode === 'transform' ? `You changed ${goal} sentence${goal > 1 ? 's' : ''} correctly!` : `You built ${goal} sentence${goal > 1 ? 's' : ''} correctly!`);
          timers.push(setTimeout(() => { say('🏆 All done! Tap “Next” to keep practising.', 'ok'); }, 1600));
        }
        swapNext();
      }
      function swapNext() {
        const b = $('[data-a="check"]');
        b.textContent = '➜ Next'; b.disabled = false; b.dataset.a = 'next';
      }
      function next() {
        const b = $('[data-a="next"]'); if (b) { b.textContent = '✔ Check'; b.dataset.a = 'check'; }
        idx = (idx + 1) % items.length;
        if (won && idx === 0) items = shuffled(items);
        setupRound();
      }

      function hint() {
        if (solved) return;
        const main = R.sp.words;
        // remove wrong tail first
        let k = 0; while (k < R.built.length && R.built[k].w === main[k]) k++;
        if (k < R.built.length) { R.built = R.built.slice(0, k); draw(); say('Took back the words after the last correct one.', ''); api.sfx('hmm'); return; }
        if (k < main.length) {
          const used = new Set(R.built.map(x => x.id));
          const c = R.pool.find(x => !used.has(x.id) && x.w === main[k]);
          if (c) { R.built.push(c); draw(); say(`Next word: “${c.w}”`, ''); api.sfx('tap'); return; }
        }
        if (mode === 'kinds') say(`Think: does it tell, ask, show strong feeling, or give an order?`, '');
      }

      function onClick(e) {
        const t = e.target.closest('button'); if (!t || !host.contains(t)) return;
        if (t.dataset.t != null && !solved) {
          const c = R.pool.find(x => String(x.id) === t.dataset.t); if (!c) return;
          R.built.push(c); api.sfx('tap'); say(''); draw();
        } else if (t.dataset.b != null && !solved) {
          R.built.splice(+t.dataset.b, 1); api.sfx('tap'); say(''); draw();
        } else if (t.dataset.k && !solved) {
          R.pickKind = t.dataset.k; api.sfx('tap'); draw();
        } else if (t.dataset.m && !solved) {
          R.pickMark = t.dataset.m; api.sfx('tap'); draw();
        } else if (t.dataset.a === 'undo' && !solved) {
          R.built.pop(); draw(); say('');
        } else if (t.dataset.a === 'hint') hint();
        else if (t.dataset.a === 'check') check();
        else if (t.dataset.a === 'next') next();
      }
      host.addEventListener('click', onClick);
      setupRound();
      return () => { host.removeEventListener('click', onClick); timers.forEach(clearTimeout); };
    },
    example: {
      mode: 'order',
      challenge: 'Put the jumbled words in order to make 3 sentences',
      items: [
        { text: 'The little bird sang a sweet song.', hint: 'Who? → did what? → what?' },
        { text: 'My mother cooks tasty food.', hint: 'Start with “My”.' },
        { text: 'We play cricket in the park.', alt: ['In the park we play cricket.'] }
      ],
      goal: 3
    },
    examples: [
      {
        mode: 'kinds',
        challenge: 'Build each sentence, then pick its kind and the right end mark',
        items: [
          { text: 'Where do you live?', kind: 'question' },
          { text: 'Please close the door.', kind: 'command' },
          { text: 'What a beautiful garden this is!', kind: 'exclamation' },
          { text: 'The sun rises in the east.', kind: 'statement' }
        ],
        goal: 4
      },
      {
        mode: 'transform',
        fromLabel: 'Active',
        toLabel: 'Passive',
        challenge: 'Change the active voice sentences into passive voice',
        items: [
          { from: 'The cat chased the mouse.', text: 'The mouse was chased by the cat.' },
          { from: 'Riya wrote a letter.', text: 'A letter was written by Riya.' },
          { from: 'The boys are playing football.', text: 'Football is being played by the boys.', hint: 'is/are + being + V3' }
        ],
        goal: 3
      },
      {
        mode: 'order',
        challenge: 'शब्दों को सही क्रम में लगाकर वाक्य बनाओ',
        items: [
          { text: 'राम विद्यालय जाता है।', meaning: 'Ram goes to school.' },
          { text: 'बालकः पुस्तकं पठति।', meaning: 'The boy reads a book. (Sanskrit)', alt: ['पुस्तकं बालकः पठति।'] }
        ],
        goal: 2
      }
    ]
  });
})();
