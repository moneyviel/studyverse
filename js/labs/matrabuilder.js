/* Knowtopia lab: matrabuilder — Hindi syllable (अक्षर) composer: व्यंजन + मात्रा = अक्षर
 *
 * PARAMS (all optional; missing ones fall back to `example`)
 *  consonants  array   consonant buttons, e.g. ['क','म','ल']   (letters needed by targets are added automatically)
 *                                                                   default 20 common व्यंजन
 *  matras      array   vowel-sign buttons from ['ा','ि','ी','ु','ू','ृ','े','ै','ो','ौ'];
 *                      '' (no sign = अ) is always offered       default all ten
 *  nasal       boolean show the ं (अनुस्वार) and ँ (चन्द्रबिन्दु) add-on buttons   default true
 *  targets     array   words (or single syllables) to build, in order. Each item is a string
 *                      'कमल' or an object { w:'कमल', e:'🌸', m:'lotus' } (e = emoji, m = meaning).
 *                      Words must be made of consonant (+ matra) (+ ं/ँ) syllables — no conjuncts
 *                      or stand-alone vowels; others are skipped.          default कमल, पानी, किताब…
 *  rounds      number  how many targets to finish to win               default all targets (max 8)
 *  challenge   string  the "🎯 Challenge" line                          default auto
 *
 * The child: picks a consonant and a matra (optionally ं/ँ), sees "क + ि = कि" and hears it,
 * then taps "Add" to put that syllable into the target word's next slot. Wrong syllables are
 * rejected with a hint; after 2 misses the needed buttons glow. Win = all `rounds` words built.
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const ALLM = ['ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'े', 'ै', 'ो', 'ौ'];
  const MNAME = { '': 'अ (no matra)', 'ा': 'आ की मात्रा', 'ि': 'इ की मात्रा', 'ी': 'ई की मात्रा', 'ु': 'उ की मात्रा', 'ू': 'ऊ की मात्रा', 'ृ': 'ऋ की मात्रा', 'े': 'ए की मात्रा', 'ै': 'ऐ की मात्रा', 'ो': 'ओ की मात्रा', 'ौ': 'औ की मात्रा' };
  const UPPER = ['ि', 'ी', 'े', 'ै', 'ो', 'ौ'];            // signs that reach above the शिरोरेखा
  const DEFC = ['क', 'ख', 'ग', 'घ', 'च', 'ज', 'ट', 'ड', 'त', 'द', 'न', 'प', 'ब', 'म', 'य', 'र', 'ल', 'व', 'स', 'ह'];
  const isCons = ch => /[क-हक़-य़]/.test(ch);

  // split a word into syllables {c, m, n} — returns null if it has conjuncts / independent vowels
  function split(w) {
    const out = []; const a = Array.from(String(w || '').normalize('NFC').trim());
    let i = 0;
    while (i < a.length) {
      let c = a[i];
      if (!isCons(c)) return null;
      i++;
      if (a[i] === '़') { c += a[i]; i++; }                // nukta (ज़, ड़ …)
      let m = '', n = '';
      if (a[i] && ALLM.includes(a[i])) { m = a[i]; i++; }
      if (a[i] === 'ं' || a[i] === 'ँ') { n = a[i]; i++; }
      if (a[i] === '्') return null;                         // conjunct — not supported
      out.push({ c, m, n });
    }
    return out.length ? out : null;
  }
  const syl = s => s.c + s.m + s.n;

  Labs.register('matrabuilder', {
    title: 'Matra builder',
    subjects: ['hindi'],
    render(host, p, api) {
      let T = (Array.isArray(p.targets) && p.targets.length ? p.targets : Labs.registry.matrabuilder.example.targets)
        .map(t => typeof t === 'string' ? { w: t } : (t && typeof t === 'object' ? { w: String(t.w || t.word || ''), e: t.e || t.emoji || '', m: t.m || t.meaning || '' } : null))
        .filter(Boolean).map(t => Object.assign(t, { parts: split(t.w) })).filter(t => t.parts);
      if (!T.length) T = [{ w: 'कमल', e: '🌸', m: 'lotus', parts: split('कमल') }];
      const useNasal = p.nasal !== false || T.some(t => t.parts.some(s => s.n));
      const cons = (Array.isArray(p.consonants) && p.consonants.length ? p.consonants.map(String) : DEFC).filter(c => split(c));
      T.forEach(t => t.parts.forEach(s => { if (!cons.includes(s.c)) cons.push(s.c); }));
      const want = new Set(Array.isArray(p.matras) ? p.matras.map(String) : ALLM);
      T.forEach(t => t.parts.forEach(s => s.m && want.add(s.m)));
      const mats = [''].concat(ALLM.filter(m => want.has(m)));
      const rounds = Math.max(1, Math.min(T.length, 8, parseInt(p.rounds, 10) || T.length));
      const defCh = rounds === 1 ? `Build the word ${T[0].w}` : `Build ${rounds} words with matras`;
      const timers = []; const later = (f, ms) => timers.push(setTimeout(f, ms));

      host.innerHTML = `<style>
.lb-matrabuilder-w{color:#1b1f3a;font-size:15px;user-select:none;-webkit-user-select:none}
.lb-matrabuilder-ch{font-weight:800;margin:0 0 8px;line-height:1.3}
.lb-matrabuilder-tg{display:flex;align-items:center;gap:10px;background:#fffaf0;border-radius:16px;padding:8px 10px}
.lb-matrabuilder-emo{font-size:36px;line-height:1}
.lb-matrabuilder-slots{display:flex;gap:6px;flex-wrap:wrap;flex:1}
.lb-matrabuilder-slot{min-width:46px;height:46px;border-radius:12px;border:2px dashed #e0c98a;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:700;color:#c4a24e;padding:0 4px;transition:all .25s}
.lb-matrabuilder-slot.cur{border-color:#8b5cf6;border-style:solid;box-shadow:0 0 0 3px #ece4ff}
.lb-matrabuilder-slot.ok{background:#2ed3a5;border:2px solid #2ed3a5;color:#fff;animation:lb-matrabuilder-pop .4s cubic-bezier(.2,1.5,.4,1)}
.lb-matrabuilder-meta{font-size:12px;font-weight:700;color:#6b7090;text-align:right;line-height:1.3}
.lb-matrabuilder-meta b{display:block;font-size:18px;color:#1b1f3a}
.lb-matrabuilder-eq{display:flex;align-items:center;gap:6px;margin:10px 0;background:linear-gradient(135deg,#f5f0ff,#eafff8);border-radius:18px;padding:8px 10px}
.lb-matrabuilder-pc{width:44px;height:52px;border-radius:12px;background:#fff;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:700;color:#8b5cf6}
.lb-matrabuilder-pm{color:#ff6b6b}
.lb-matrabuilder-op{font-weight:800;color:#6b7090;font-size:18px}
.lb-matrabuilder-res{min-width:64px;height:62px;border-radius:16px;background:#fff;border:0;font:inherit;font-size:38px;font-weight:700;color:#1b1f3a;box-shadow:0 3px 0 #dcd3f7;cursor:pointer;padding:0 8px}
.lb-matrabuilder-res.bump{animation:lb-matrabuilder-pop .35s cubic-bezier(.2,1.5,.4,1)}
.lb-matrabuilder-add{margin-left:auto;min-width:72px;height:52px;border:0;border-radius:16px;background:#8b5cf6;color:#fff;font:inherit;font-weight:800;font-size:16px;cursor:pointer;box-shadow:0 3px 0 #6d3fd6}
.lb-matrabuilder-add:active{transform:translateY(2px);box-shadow:0 1px 0 #6d3fd6}
.lb-matrabuilder-name{font-size:12px;font-weight:700;color:#6b7090;margin:-4px 0 6px;min-height:16px}
.lb-matrabuilder-lbl{font-size:12px;font-weight:800;color:#6b7090;margin:4px 0}
.lb-matrabuilder-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(42px,1fr));gap:5px}
.lb-matrabuilder-cg{max-height:94px;overflow-y:auto;padding:2px}
.lb-matrabuilder-k{height:42px;border:0;border-radius:11px;background:#f3f4fb;font:inherit;font-size:21px;font-weight:700;color:#1b1f3a;cursor:pointer;transition:transform .12s,background .15s}
.lb-matrabuilder-k.m{background:#fff3f3;color:#e14d4d}
.lb-matrabuilder-k.n{background:#fff8e1;color:#b8860b}
.lb-matrabuilder-k.on{background:#8b5cf6;color:#fff;transform:scale(1.06)}
.lb-matrabuilder-k.m.on{background:#ff6b6b}
.lb-matrabuilder-k.n.on{background:#ffc93c;color:#1b1f3a}
.lb-matrabuilder-k.glow{animation:lb-matrabuilder-glow 1s infinite}
@keyframes lb-matrabuilder-glow{50%{box-shadow:0 0 0 4px #2ed3a5}}
@keyframes lb-matrabuilder-pop{from{transform:scale(.5);opacity:.2}to{transform:scale(1);opacity:1}}
@keyframes lb-matrabuilder-shk{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
.lb-matrabuilder-shk{animation:lb-matrabuilder-shk .4s}
.lb-matrabuilder-msg{min-height:20px;font-size:13px;font-weight:800;text-align:center;margin-top:8px;color:#6b7090}
.lb-matrabuilder-foot{display:flex;justify-content:space-between;align-items:center;margin-top:6px}
.lb-matrabuilder-btn{border:0;border-radius:12px;min-height:40px;padding:0 12px;font:inherit;font-weight:800;background:#f1effb;color:#8b5cf6;cursor:pointer}
.lb-matrabuilder-cnt{font-weight:800;color:#6b7090;font-size:13px}
</style>
<div class="lb-matrabuilder-w">
  <div class="lb-matrabuilder-ch">🎯 Challenge: ${esc(p.challenge || defCh)}</div>
  <div class="lb-matrabuilder-tg"></div>
  <div class="lb-matrabuilder-eq">
    <div class="lb-matrabuilder-pc lb-matrabuilder-c1"></div><span class="lb-matrabuilder-op">+</span>
    <div class="lb-matrabuilder-pc lb-matrabuilder-pm"></div><span class="lb-matrabuilder-op">=</span>
    <button class="lb-matrabuilder-res" title="Hear it"></button>
    <button class="lb-matrabuilder-add">➕ Add</button>
  </div>
  <div class="lb-matrabuilder-name"></div>
  <div class="lb-matrabuilder-lbl">व्यंजन · consonant</div>
  <div class="lb-matrabuilder-grid lb-matrabuilder-cg">${cons.map(c => `<button class="lb-matrabuilder-k" data-c="${esc(c)}">${esc(c)}</button>`).join('')}</div>
  <div class="lb-matrabuilder-lbl">मात्रा · matra</div>
  <div class="lb-matrabuilder-grid">${mats.map(m => `<button class="lb-matrabuilder-k m" data-m="${esc(m)}">${m ? '◌' + esc(m) : 'अ'}</button>`).join('')}${useNasal ? `<button class="lb-matrabuilder-k n" data-n="ं">◌ं</button><button class="lb-matrabuilder-k n" data-n="ँ">◌ँ</button>` : ''}</div>
  <div class="lb-matrabuilder-msg"></div>
  <div class="lb-matrabuilder-foot"><span class="lb-matrabuilder-cnt"></span><button class="lb-matrabuilder-btn lb-matrabuilder-skip">⏭ Next word</button></div>
</div>`;
      const $ = s => host.querySelector(s);
      const tg = $('.lb-matrabuilder-tg'), res = $('.lb-matrabuilder-res'), msg = $('.lb-matrabuilder-msg');
      let c = T[0].parts[0].c === cons[0] && cons.length > 1 ? cons[1] : cons[0], m = '', n = '';
      let ti = 0, si = 0, done = 0, misses = 0, won = false;
      const shown = new Set();

      function current() {
        let nn = n;
        if (nn === 'ँ' && UPPER.includes(m)) nn = 'ं';                 // ँ becomes ं when matra is above the line
        return { c, m, n: nn };
      }
      function paint(bump) {
        const s = current();
        $('.lb-matrabuilder-c1').textContent = c;
        $('.lb-matrabuilder-pm').textContent = (m ? '◌' + m : '–') + (s.n ? s.n : '');
        res.textContent = syl(s);
        if (bump) { res.classList.remove('bump'); void res.offsetWidth; res.classList.add('bump'); }
        let nm = MNAME[m] || '';
        if (s.n) nm += (m ? ' + ' : ' · ') + (s.n === 'ं' ? 'अनुस्वार ं' : 'चन्द्रबिन्दु ँ');
        if (n === 'ँ' && s.n === 'ं') nm += ' (ँ is written ं when the matra goes above the line)';
        $('.lb-matrabuilder-name').textContent = nm;
        host.querySelectorAll('[data-c]').forEach(b => b.classList.toggle('on', b.dataset.c === c));
        host.querySelectorAll('[data-m]').forEach(b => b.classList.toggle('on', b.dataset.m === m));
        host.querySelectorAll('[data-n]').forEach(b => b.classList.toggle('on', b.dataset.n === n));
      }
      function drawTarget() {
        const t = T[ti];
        tg.innerHTML = `<div class="lb-matrabuilder-emo">${esc(t.e || '📝')}</div>
          <div class="lb-matrabuilder-slots">${t.parts.map((s, i) => `<div class="lb-matrabuilder-slot${i < si ? ' ok' : ''}${i === si ? ' cur' : ''}">${i < si ? esc(syl(s)) : '?'}</div>`).join('')}</div>
          <div class="lb-matrabuilder-meta"><b>${esc(t.w)}</b>${esc(t.m || '')}</div>`;
        $('.lb-matrabuilder-cnt').textContent = `Words: ${done} / ${rounds}`;
        clearGlow();
      }
      function clearGlow() { host.querySelectorAll('.glow').forEach(b => b.classList.remove('glow')); }
      function hint() {
        const need = T[ti].parts[si];
        clearGlow();
        host.querySelectorAll('[data-c]').forEach(b => { if (b.dataset.c === need.c) { b.classList.add('glow'); b.scrollIntoView && b.parentNode.scrollTo({ top: b.offsetTop - b.parentNode.offsetTop - 4, behavior: 'smooth' }); } });
        host.querySelectorAll('[data-m]').forEach(b => { if (b.dataset.m === need.m) b.classList.add('glow'); });
        host.querySelectorAll('[data-n]').forEach(b => { if (need.n && b.dataset.n === need.n) b.classList.add('glow'); });
        msg.textContent = `Hint: next is ${syl(need)} = ${need.c} + ${need.m ? '◌' + need.m : 'अ'}${need.n ? ' + ' + need.n : ''}`;
      }
      function add() {
        const t = T[ti], need = t.parts[si], s = current();
        const slotEls = tg.querySelectorAll('.lb-matrabuilder-slot');
        if (syl(s) === syl(need)) {
          api.sfx('correct'); misses = 0; si++; msg.style.color = '#0f9a73';
          msg.textContent = `${need.c} + ${need.m ? '◌' + need.m : 'अ'}${need.n ? ' + ' + need.n : ''} = ${syl(need)} ✓`;
          drawTarget();
          if (si >= t.parts.length) {
            done++; $('.lb-matrabuilder-cnt').textContent = `Words: ${done} / ${rounds}`;
            api.speak(t.w); msg.textContent = `🎉 ${t.w}${t.m ? ' — ' + t.m : ''}!`;
            if (done >= rounds && !won) { won = true; later(() => api.win(`शाबाश! You built ${rounds === 1 ? t.w : rounds + ' words'} using matras.`), 500); }
            later(nextWord, 1500);
          } else api.speak(syl(need));
        } else {
          api.sfx('wrong'); misses++; msg.style.color = '#e14d4d';
          const el = slotEls[si]; if (el) { el.classList.remove('lb-matrabuilder-shk'); void el.offsetWidth; el.classList.add('lb-matrabuilder-shk'); }
          if (s.c !== need.c) msg.textContent = `${syl(s)} is not right — listen: the sound starts with a different letter`;
          else msg.textContent = `Right letter ${need.c}! Now change the matra`;
          api.speak(syl(need));
          if (misses >= 2) hint();
        }
      }
      function nextWord() {
        ti = (ti + 1) % T.length; si = 0; misses = 0;
        msg.textContent = ''; msg.style.color = '';
        drawTarget(); api.speak(T[ti].w);
      }
      host.querySelectorAll('[data-c]').forEach(b => b.onclick = () => { c = b.dataset.c; api.sfx('tap'); paint(true); api.speak(syl(current())); });
      host.querySelectorAll('[data-m]').forEach(b => b.onclick = () => { m = b.dataset.m; api.sfx('tap'); paint(true); api.speak(syl(current())); });
      host.querySelectorAll('[data-n]').forEach(b => b.onclick = () => { n = n === b.dataset.n ? '' : b.dataset.n; api.sfx('tap'); paint(true); api.speak(syl(current())); });
      res.onclick = () => api.speak(syl(current()));
      $('.lb-matrabuilder-add').onclick = add;
      $('.lb-matrabuilder-skip').onclick = () => { api.sfx('tap'); nextWord(); };
      drawTarget(); paint(false);
      return () => { timers.forEach(clearTimeout); host.innerHTML = ''; };
    },
    example: {
      consonants: ['क', 'ख', 'ग', 'च', 'ज', 'त', 'द', 'न', 'प', 'ब', 'म', 'र', 'ल', 'स', 'ह'],
      matras: ['ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'े', 'ै', 'ो', 'ौ'],
      nasal: true,
      targets: [{ w: 'कमल', e: '🌸', m: 'lotus' }, { w: 'पानी', e: '💧', m: 'water' }, { w: 'किताब', e: '📕', m: 'book' }, { w: 'मोर', e: '🦚', m: 'peacock' }, { w: 'पतंग', e: '🪁', m: 'kite' }],
      rounds: 4,
      challenge: 'Build 4 words: कमल, पानी, किताब, मोर'
    },
    examples: [
      { consonants: ['क', 'ग', 'ज', 'त', 'न', 'प', 'म', 'र', 'ल', 'स'], matras: ['ि'], nasal: false,
        targets: [{ w: 'कि', e: '✏️', m: 'ki' }, { w: 'दिन', e: '☀️', m: 'day' }, { w: 'गिलास', e: '🥛', m: 'glass' }, { w: 'तितली', e: '🦋', m: 'butterfly' }],
        rounds: 3, challenge: 'इ की मात्रा (ि) — build 3 words' },
      { consonants: ['क', 'च', 'ब', 'म', 'स', 'ल', 'द', 'थ', 'न', 'ग', 'ह'], matras: ['ा', 'ु', 'ू', 'ृ', 'ै', 'ौ', 'ो'], nasal: true,
        targets: [{ w: 'चाँद', e: '🌙', m: 'moon' }, { w: 'बंदर', e: '🐒', m: 'monkey' }, { w: 'मृग', e: '🦌', m: 'deer' }, { w: 'थैला', e: '👜', m: 'bag' }, { w: 'नौका', e: '⛵', m: 'boat' }],
        rounds: 5, challenge: 'चन्द्रबिन्दु, अनुस्वार और ऋ/ऐ/औ की मात्रा — build all 5 words' }
    ]
  });
})();
