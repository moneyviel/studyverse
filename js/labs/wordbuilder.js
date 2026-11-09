/* Knowtopia Concept Lab — wordbuilder
 * Spin word-part wheels (prefix + root + suffix, word 1 + word 2, onset + rime…) to build words.
 * When the parts make a real word from the data list, the word glows and its meaning appears.
 * Works for English and Hindi/Sanskrit (उपसर्ग / प्रत्यय) — every valid word comes from data.
 *
 * PARAMS
 *  slots       array of arrays  the wheels, left to right; each is a list of parts.
 *                               Use '' for "no part" (e.g. no prefix).          default: prefix/root/suffix (see example)
 *  slotLabels  array of strings label above each wheel, e.g. ['Prefix','Root','Suffix'] or ['उपसर्ग','मूल शब्द']
 *                                                                                default ['Part 1','Part 2',…]
 *  rootSlot    number           index of the main (root) wheel; a root alone is "not built yet",
 *                               not "wrong"                                      default 1 if 3 wheels, else 0
 *  words       array | object   the valid words.
 *                 array:  [{ parts:['un','happy','ness'], word:'unhappiness', meaning:'the state of not being happy' }]
 *                         'parts' (same order as slots, '' for empty) lets spelling change (happy+ness → happiness)
 *                         or sandhi (सु+आगत → स्वागत). Without 'parts', the word must equal the joined parts.
 *                 object: { 'unkind': 'not kind', … } — word = parts joined together.
 *  goal        number           how many different words to find to win          default min(5, number of words)
 *  targets     array of strings optional: specific words to make, in order; the child sees the meaning as a clue
 *                               (overrides goal: win after all targets are made)  default none
 *  challenge   string           challenge line                                   default generated
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const norm = s => { s = String(s == null ? '' : s).trim(); return (s === '—' || s === '-' || s === '–') ? '' : s; };
  const COLORS = [['#8b5cf6', '#f1ecff'], ['#3b82f6', '#e8f0ff'], ['#2ed3a5', '#e3fbf3'], ['#ff6b6b', '#ffeded']];
  const ROW = 30;

  Labs.register('wordbuilder', {
    title: 'Word builder',
    subjects: ['english', 'hindi', 'sanskrit'],
    render(host, p, api) {
      const slots = (Array.isArray(p.slots) && p.slots.length ? p.slots : [['', 'un'], ['kind'], ['', 'ness']])
        .slice(0, 4).map(s => (Array.isArray(s) && s.length ? s : ['']).map(norm));
      const n = slots.length;
      const labels = slots.map((_, i) => (p.slotLabels && p.slotLabels[i]) || `Part ${i + 1}`);
      const rootSlot = Number.isInteger(p.rootSlot) ? p.rootSlot : (n === 3 ? 1 : 0);
      // valid words
      let list = [];
      if (Array.isArray(p.words)) list = p.words.map(w => typeof w === 'string' ? { word: w } : w).filter(w => w && w.word);
      else if (p.words && typeof p.words === 'object') list = Object.keys(p.words).map(k => ({ word: k, meaning: p.words[k] }));
      list = list.map(w => ({ word: String(w.word), meaning: w.meaning || '', parts: Array.isArray(w.parts) ? w.parts.map(norm) : null }));
      const targets = Array.isArray(p.targets) ? p.targets.map(String).filter(t => list.some(w => w.word === t)) : [];
      const goal = targets.length || Math.max(1, Math.min(list.length || 1, +p.goal || Math.min(5, list.length || 1)));
      const challenge = p.challenge || (targets.length ? `Make the ${targets.length} words from their meanings` : `Find ${goal} real words by spinning the wheels`);

      const pos = slots.map(s => { const i = s.indexOf(''); return i >= 0 ? i : 0; });
      // start the root wheel on its first part
      if (slots[rootSlot]) pos[rootSlot] = Math.max(0, slots[rootSlot].findIndex(x => x !== ''));
      const found = []; let tIdx = 0, won = false, lastHit = '';

      host.innerHTML = `<style>
.lb-wordbuilder-w{color:#1b1f3a;max-width:400px;margin:0 auto}
.lb-wordbuilder-ch{font-weight:800;font-size:13.5px;background:#fff7dd;border-radius:12px;padding:7px 10px;margin-bottom:8px;line-height:1.3}
.lb-wordbuilder-clue{font-weight:800;font-size:14px;background:#eef4ff;color:#1e4fb8;border-radius:12px;padding:6px 10px;margin-bottom:8px;line-height:1.3}
.lb-wordbuilder-wheels{display:flex;gap:6px;align-items:stretch}
.lb-wordbuilder-col{flex:1;min-width:0;display:flex;flex-direction:column;align-items:stretch;gap:3px}
.lb-wordbuilder-lab{font-size:11.5px;font-weight:800;text-align:center;letter-spacing:.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lb-wordbuilder-plus{align-self:center;font-weight:900;color:#b5b8d2;font-size:18px;padding-top:14px}
.lb-wordbuilder-arr{border:none;font-family:inherit;height:40px;border-radius:12px;cursor:pointer;font-size:15px;font-weight:900}
.lb-wordbuilder-arr:active{transform:scale(.95)}
.lb-wordbuilder-win{position:relative;height:${ROW * 3}px;overflow:hidden;border-radius:14px;touch-action:none;cursor:grab;user-select:none;-webkit-user-select:none}
.lb-wordbuilder-win::before,.lb-wordbuilder-win::after{content:'';position:absolute;left:0;right:0;height:${ROW}px;z-index:2;pointer-events:none}
.lb-wordbuilder-win::before{top:0;background:linear-gradient(#fff,rgba(255,255,255,.35))}
.lb-wordbuilder-win::after{bottom:0;background:linear-gradient(rgba(255,255,255,.35),#fff)}
.lb-wordbuilder-sel{position:absolute;left:3px;right:3px;top:${ROW - 2}px;height:${ROW + 4}px;border-radius:10px;z-index:1;pointer-events:none}
.lb-wordbuilder-strip{position:absolute;left:0;right:0;top:0;transition:transform .22s cubic-bezier(.3,1.4,.5,1);z-index:1}
.lb-wordbuilder-it{height:${ROW}px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;white-space:nowrap;padding:0 3px;color:#6b7090}
.lb-wordbuilder-it.cur{font-size:18px;color:#1b1f3a}
.lb-wordbuilder-res{margin-top:9px;border-radius:16px;background:#f7f8fd;padding:9px 10px;min-height:94px;text-align:center;transition:background .3s,box-shadow .3s}
.lb-wordbuilder-res.ok{background:#e9fbf5;box-shadow:0 0 0 2px #2ed3a5 inset}
.lb-wordbuilder-eq{font-weight:800;font-size:13px;color:#6b7090;min-height:18px}
.lb-wordbuilder-eq b{padding:1px 6px;border-radius:7px}
.lb-wordbuilder-word{font-size:27px;font-weight:900;line-height:1.25;word-break:break-word;margin:2px 0}
.lb-wordbuilder-word span{transition:color .2s}
.lb-wordbuilder-res.ok .lb-wordbuilder-word{animation:lbwbpop .45s ease}
@keyframes lbwbpop{40%{transform:scale(1.15)}}
.lb-wordbuilder-mean{font-size:13.5px;font-weight:700;color:#0f7a5c;line-height:1.3}
.lb-wordbuilder-mean.no{color:#8a8fb0}
.lb-wordbuilder-bot{display:flex;align-items:center;gap:8px;margin-top:8px}
.lb-wordbuilder-cnt{font-weight:900;font-size:13px;color:#fff;background:#8b5cf6;border-radius:10px;padding:5px 9px;white-space:nowrap}
.lb-wordbuilder-found{flex:1;display:flex;gap:5px;overflow-x:auto;scrollbar-width:none;min-height:28px;align-items:center}
.lb-wordbuilder-found::-webkit-scrollbar{display:none}
.lb-wordbuilder-f{background:#e3fbf3;color:#0f7a5c;font-weight:800;font-size:13px;border-radius:9px;padding:4px 8px;white-space:nowrap;animation:lbwbpop .4s}
.lb-wordbuilder-empty{color:#a4a8c6;font-size:12.5px;font-weight:700}
.lb-wordbuilder-say{border:none;font-family:inherit;width:42px;height:40px;border-radius:12px;background:#fff7dd;font-size:18px;cursor:pointer}
</style>
<div class="lb-wordbuilder-w">
  <div class="lb-wordbuilder-ch">🎯 Challenge: ${esc(challenge)}</div>
  <div class="lb-wordbuilder-clue" style="display:none"></div>
  <div class="lb-wordbuilder-wheels">${slots.map((s, i) => {
        const [c, bg] = COLORS[i % 4];
        return (i ? '<div class="lb-wordbuilder-plus">+</div>' : '') + `<div class="lb-wordbuilder-col" data-s="${i}">
      <div class="lb-wordbuilder-lab" style="color:${c}">${esc(labels[i])}</div>
      <button class="lb-wordbuilder-arr" data-d="-1" data-s="${i}" style="background:${bg};color:${c}" aria-label="previous ${esc(labels[i])}">▲</button>
      <div class="lb-wordbuilder-win" data-s="${i}" style="background:${bg}"><div class="lb-wordbuilder-sel" style="box-shadow:0 0 0 2px ${c} inset;background:#fff"></div><div class="lb-wordbuilder-strip"></div></div>
      <button class="lb-wordbuilder-arr" data-d="1" data-s="${i}" style="background:${bg};color:${c}" aria-label="next ${esc(labels[i])}">▼</button>
    </div>`;
      }).join('')}</div>
  <div class="lb-wordbuilder-res"><div class="lb-wordbuilder-eq"></div><div class="lb-wordbuilder-word"></div><div class="lb-wordbuilder-mean"></div></div>
  <div class="lb-wordbuilder-bot"><div class="lb-wordbuilder-cnt"></div><div class="lb-wordbuilder-found"></div><button class="lb-wordbuilder-say" aria-label="read aloud">🔊</button></div>
</div>`;
      const $ = s => host.querySelector(s);
      const res = $('.lb-wordbuilder-res'), eqEl = $('.lb-wordbuilder-eq'), wordEl = $('.lb-wordbuilder-word'), meanEl = $('.lb-wordbuilder-mean');
      const cntEl = $('.lb-wordbuilder-cnt'), foundEl = $('.lb-wordbuilder-found'), clueEl = $('.lb-wordbuilder-clue');
      const strips = [...host.querySelectorAll('.lb-wordbuilder-strip')];

      function drawWheel(i) {
        const s = slots[i], L = s.length, k = pos[i];
        // show prev, current, next (wrap) — use a 5-row strip so it can animate
        const rows = [-2, -1, 0, 1, 2].map(o => {
          const v = L > 1 || o === 0 ? s[((k + o) % L + L) % L] : null;
          return `<div class="lb-wordbuilder-it ${o === 0 ? 'cur' : ''}">${v == null ? '' : v === '' ? '—' : esc(v)}</div>`;
        }).join('');
        strips[i].style.transition = 'none';
        strips[i].innerHTML = rows;
        strips[i].style.transform = `translateY(${-ROW}px)`;
      }
      function spin(i, d) {
        const L = slots[i].length; if (L < 2) { api.sfx('hmm'); return; }
        // animate from offset then settle
        pos[i] = ((pos[i] + d) % L + L) % L;
        drawWheel(i);
        strips[i].style.transform = `translateY(${-ROW + d * ROW}px)`;
        void strips[i].offsetWidth;
        strips[i].style.transition = '';
        strips[i].style.transform = `translateY(${-ROW}px)`;
        api.sfx('tap');
        update(true);
      }

      function match() {
        const parts = pos.map((k, i) => slots[i][k]);
        const joined = parts.join('');
        const hit = list.find(w => w.parts ? w.parts.length === n && w.parts.every((x, i) => x === parts[i]) : false)
          || list.find(w => !w.parts && w.word === joined);
        return { parts, joined, hit };
      }

      function update(fromUser) {
        const { parts, joined, hit } = match();
        const used = parts.map((x, i) => [x, i]).filter(([x]) => x !== '');
        eqEl.innerHTML = used.length > 1 ? used.map(([x, i]) => `<b style="background:${COLORS[i % 4][1]};color:${COLORS[i % 4][0]}">${esc(x)}</b>`).join(' + ') + ' =' : '&nbsp;';
        res.classList.toggle('ok', !!hit);
        if (hit) {
          const shown = hit.word;
          // colour the parts when the spelling is unchanged, otherwise show the real spelling
          wordEl.innerHTML = shown === joined ? used.map(([x, i]) => `<span style="color:${COLORS[i % 4][0]}">${esc(x)}</span>`).join('') : `<span style="color:#0f7a5c">${esc(shown)}</span>`;
          meanEl.className = 'lb-wordbuilder-mean';
          meanEl.innerHTML = (hit.meaning ? '📖 ' + esc(hit.meaning) : '✅ A real word!') + (shown !== joined ? `<div style="color:#c26a00;font-size:12px;margin-top:2px">✏️ Spelling changes when the parts join (not “${esc(joined)}”)</div>` : '');
          if (fromUser && lastHit !== shown) {
            lastHit = shown;
            api.speak(shown + (hit.meaning ? '. ' + hit.meaning : ''));
            const isNew = !found.includes(shown);
            if (isNew) { found.push(shown); }
            if (targets.length) {
              if (tIdx < targets.length && shown === targets[tIdx]) { tIdx++; api.sfx('correct'); }
              else api.sfx(isNew ? 'coin' : 'tap');
            } else api.sfx(isNew ? 'coin' : 'tap');
            progress();
          }
        } else {
          lastHit = '';
          wordEl.innerHTML = used.map(([x, i]) => `<span style="color:${COLORS[i % 4][0]};opacity:.55">${esc(x)}</span>`).join('') || '<span style="opacity:.4">—</span>';
          meanEl.className = 'lb-wordbuilder-mean no';
          const onlyRoot = used.length <= 1;
          meanEl.textContent = onlyRoot ? 'Spin the other wheels to add parts ↺' : 'Not a word in our list — keep spinning!';
        }
      }

      function progress() {
        const have = targets.length ? tIdx : Math.min(found.length, goal);
        cntEl.textContent = `${have}/${goal}`;
        foundEl.innerHTML = found.length ? found.slice().reverse().map(w => `<span class="lb-wordbuilder-f">${esc(w)}</span>`).join('') : '<span class="lb-wordbuilder-empty">Words you find appear here</span>';
        if (targets.length) {
          if (tIdx < targets.length) {
            const t = list.find(w => w.word === targets[tIdx]);
            clueEl.style.display = ''; clueEl.textContent = `🔎 Make a word that means: “${t.meaning || t.word}”`;
          } else { clueEl.style.display = ''; clueEl.textContent = '🌟 All clue words made!'; }
        }
        if (!won && have >= goal) {
          won = true;
          api.win(targets.length ? `You made all ${goal} clue words!` : `You found ${goal} real words: ${found.slice(0, goal).join(', ')}`);
        }
      }

      // drag to spin
      let drag = null;
      function down(e) {
        const w = e.target.closest('.lb-wordbuilder-win'); if (!w) return;
        drag = { s: +w.dataset.s, y: e.clientY, acc: 0, id: e.pointerId, el: w };
        try { w.setPointerCapture(e.pointerId); } catch (_) {}
        e.preventDefault();
      }
      function move(e) {
        if (!drag || e.pointerId !== drag.id) return;
        const dy = e.clientY - drag.y;
        if (Math.abs(dy) >= ROW * 0.8) { spin(drag.s, dy < 0 ? 1 : -1); drag.y = e.clientY; drag.moved = true; }
      }
      function up(e) {
        if (!drag || e.pointerId !== drag.id) return;
        if (!drag.moved) { // tap: upper third = previous, otherwise next
          const r = drag.el.getBoundingClientRect();
          spin(drag.s, e.clientY - r.top < r.height / 3 ? -1 : 1);
        }
        drag = null;
      }
      function onClick(e) {
        const b = e.target.closest('button'); if (!b || !host.contains(b)) return;
        if (b.dataset.d) spin(+b.dataset.s, +b.dataset.d);
        else if (b.classList.contains('lb-wordbuilder-say')) { const { hit, parts } = match(); api.speak(hit ? hit.word + (hit.meaning ? '. ' + hit.meaning : '') : parts.filter(Boolean).join(' ')); }
      }
      host.addEventListener('pointerdown', down);
      host.addEventListener('pointermove', move);
      host.addEventListener('pointerup', up);
      host.addEventListener('pointercancel', up);
      host.addEventListener('click', onClick);
      // start on a combination that is not already a word, so the first word is the child's own find
      const spinSlot = slots.findIndex((s, i) => i !== rootSlot && s.length > 1);
      if (spinSlot >= 0) for (let t = 0; t < slots[spinSlot].length && match().hit; t++) pos[spinSlot] = (pos[spinSlot] + 1) % slots[spinSlot].length;
      { const h = match().hit; if (h && (!targets.length)) { found.push(h.word); lastHit = h.word; } }
      slots.forEach((_, i) => drawWheel(i));
      update(false); progress();
      return () => {
        host.removeEventListener('pointerdown', down); host.removeEventListener('pointermove', move);
        host.removeEventListener('pointerup', up); host.removeEventListener('pointercancel', up);
        host.removeEventListener('click', onClick);
      };
    },
    example: {
      challenge: 'Spin prefix, root and suffix wheels to find 6 real words',
      slots: [['', 'un', 're', 'dis'], ['happy', 'kind', 'play', 'agree', 'help'], ['', 'ful', 'ness', 'less', 'able', 'er', 'ment']],
      slotLabels: ['Prefix', 'Root', 'Suffix'],
      goal: 6,
      words: [
        { parts: ['un', 'happy', ''], word: 'unhappy', meaning: 'not happy, sad' },
        { parts: ['', 'happy', 'ness'], word: 'happiness', meaning: 'the feeling of being happy' },
        { parts: ['un', 'happy', 'ness'], word: 'unhappiness', meaning: 'the feeling of being sad' },
        { parts: ['un', 'kind', ''], word: 'unkind', meaning: 'not kind, mean' },
        { parts: ['', 'kind', 'ness'], word: 'kindness', meaning: 'being kind and caring' },
        { parts: ['un', 'kind', 'ness'], word: 'unkindness', meaning: 'being mean to others' },
        { parts: ['re', 'play', ''], word: 'replay', meaning: 'play again' },
        { parts: ['', 'play', 'er'], word: 'player', meaning: 'a person who plays' },
        { parts: ['', 'play', 'ful'], word: 'playful', meaning: 'full of fun' },
        { parts: ['', 'play', 'able'], word: 'playable', meaning: 'can be played' },
        { parts: ['un', 'play', 'able'], word: 'unplayable', meaning: 'cannot be played' },
        { parts: ['dis', 'agree', ''], word: 'disagree', meaning: 'not agree, have a different opinion' },
        { parts: ['', 'agree', 'able'], word: 'agreeable', meaning: 'pleasant; willing to agree' },
        { parts: ['dis', 'agree', 'able'], word: 'disagreeable', meaning: 'not pleasant' },
        { parts: ['', 'agree', 'ment'], word: 'agreement', meaning: 'when people agree' },
        { parts: ['dis', 'agree', 'ment'], word: 'disagreement', meaning: 'when people do not agree' },
        { parts: ['', 'help', 'ful'], word: 'helpful', meaning: 'gives help' },
        { parts: ['un', 'help', 'ful'], word: 'unhelpful', meaning: 'not giving help' },
        { parts: ['', 'help', 'less'], word: 'helpless', meaning: 'unable to help oneself' },
        { parts: ['', 'help', 'er'], word: 'helper', meaning: 'a person who helps' }
      ]
    },
    examples: [
      {
        challenge: 'Join two small words to make 5 compound words',
        slots: [['sun', 'rain', 'foot', 'butter', 'tooth'], ['flower', 'bow', 'ball', 'fly', 'brush', 'coat', 'shine', 'print']],
        slotLabels: ['Word 1', 'Word 2'],
        rootSlot: 0,
        goal: 5,
        words: {
          sunflower: 'a tall plant with a big yellow flower', sunshine: 'the light of the sun',
          rainbow: 'an arc of seven colours in the sky', raincoat: 'a coat that keeps you dry',
          football: 'a game played by kicking a ball', footprint: 'the mark a foot leaves',
          butterfly: 'an insect with colourful wings', toothbrush: 'a brush to clean your teeth'
        }
      },
      {
        challenge: 'The -at family: make 6 words that rhyme with “cat”',
        slots: [['c', 'h', 'm', 'r', 'b', 's', 'f', 'p'], ['at']],
        slotLabels: ['Sound', 'Family'],
        rootSlot: 1,
        goal: 6,
        words: { cat: 'a pet that says meow', hat: 'you wear it on your head', mat: 'a small rug on the floor', rat: 'a small animal with a long tail', bat: 'used to hit the ball; also a flying animal', sat: 'did sit', fat: 'big and round', pat: 'a soft tap' }
      },
      {
        challenge: 'उपसर्ग जोड़कर अर्थ बदलो — संकेत देखकर शब्द बनाओ',
        slots: [['', 'सु', 'कु', 'अ'], ['पुत्र', 'ज्ञान', 'मार्ग', 'यश']],
        slotLabels: ['उपसर्ग', 'मूल शब्द'],
        rootSlot: 1,
        words: [
          { parts: ['सु', 'पुत्र'], word: 'सुपुत्र', meaning: 'अच्छा पुत्र (good son)' },
          { parts: ['कु', 'पुत्र'], word: 'कुपुत्र', meaning: 'बुरा पुत्र (bad son)' },
          { parts: ['अ', 'ज्ञान'], word: 'अज्ञान', meaning: 'ज्ञान का न होना (ignorance)' },
          { parts: ['सु', 'मार्ग'], word: 'सुमार्ग', meaning: 'अच्छा रास्ता (right path)' },
          { parts: ['कु', 'मार्ग'], word: 'कुमार्ग', meaning: 'बुरा रास्ता (wrong path)' },
          { parts: ['सु', 'यश'], word: 'सुयश', meaning: 'अच्छी कीर्ति (good fame)' }
        ],
        targets: ['कुपुत्र', 'अज्ञान', 'सुमार्ग']
      }
    ]
  });
})();
