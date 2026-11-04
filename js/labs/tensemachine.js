/* StudyVerse Concept Lab — tensemachine
 * A time machine: slide between PAST · PRESENT · FUTURE and pick the aspect (simple / continuous /
 * perfect / perfect continuous). The sentence on the screen changes to the matching verb form
 * (all forms come from a data table, so it works for English, Hindi, Sanskrit lakāras…).
 * A timeline picture shows WHEN the action happens and whether it is a whole event, ongoing, or finished.
 * Challenge: set the machine so that it produces the target sentence.
 *
 * PARAMS
 *  sentences    array   each: { forms: { past:{simple,continuous,perfect,perfectContinuous},
 *                                       present:{…}, future:{…} }, meaning?: '…' }
 *                       Each form is a full sentence; wrap the verb part in [square brackets] to
 *                       highlight it, e.g. 'She [was playing] football.' Missing cells are skipped.
 *                                                                          default: see example
 *  aspects      array   which aspects to show, in order (subset of simple, continuous, perfect,
 *                       perfectContinuous). One aspect hides the aspect buttons.
 *                                                        default: the aspects found in the first sentence
 *  timeLabels   object  {past, present, future} names, e.g. {past:'भूतकाल'}   default Past/Present/Future
 *  aspectLabels object  {simple, continuous, perfect, perfectContinuous} names  default English names
 *  rules        object  formula shown under the sentence, keyed 'time.aspect', e.g. {'past.perfect':'had + V3'}
 *                       English rules are built in for English sentences.       default built-in (English only)
 *  showRules    boolean show the formula line                                   default true
 *  showTimeline boolean show the timeline picture                               default true
 *  goal         number  how many target sentences to make to win                default 3
 *  targets      array   optional fixed targets: [{ s: 0, time: 'future', aspect: 'perfect' }]  default random
 *  challenge    string  challenge line                                         default generated
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const DEVA = /[ऀ-ॿ]/;
  const TIMES = ['past', 'present', 'future'];
  const ASP = ['simple', 'continuous', 'perfect', 'perfectContinuous'];
  const TL = { past: 'Past', present: 'Present', future: 'Future' };
  const AL = { simple: 'Simple', continuous: 'Continuous', perfect: 'Perfect', perfectContinuous: 'Perfect Cont.' };
  const TICON = { past: '◀', present: '●', future: '▶' };
  const EN_RULES = {
    'past.simple': 'V2 (past form)', 'present.simple': 'V1 / V1 + s, es', 'future.simple': 'will + V1',
    'past.continuous': 'was / were + V-ing', 'present.continuous': 'am / is / are + V-ing', 'future.continuous': 'will be + V-ing',
    'past.perfect': 'had + V3', 'present.perfect': 'has / have + V3', 'future.perfect': 'will have + V3',
    'past.perfectContinuous': 'had been + V-ing', 'present.perfectContinuous': 'has / have been + V-ing', 'future.perfectContinuous': 'will have been + V-ing'
  };
  const plain = s => String(s || '').replace(/[\[\]]/g, '');
  const marked = s => esc(s).replace(/\[([^\]]*)\]/g, '<b class="lb-tensemachine-v">$1</b>');

  Labs.register('tensemachine', {
    title: 'Tense time machine',
    subjects: ['english', 'hindi', 'sanskrit'],
    render(host, p, api) {
      const uid = 'lbtm' + Math.random().toString(36).slice(2, 8);
      const sents = (Array.isArray(p.sentences) ? p.sentences : []).filter(s => s && s.forms);
      if (!sents.length) sents.push({ forms: { past: { simple: 'I [played].' }, present: { simple: 'I [play].' }, future: { simple: 'I [will play].' } } });
      const get = (si, t, a) => { const f = sents[si].forms[t]; return f && f[a] ? String(f[a]) : ''; };
      let aspects = Array.isArray(p.aspects) ? p.aspects.filter(a => ASP.includes(a)) : [];
      if (!aspects.length) aspects = ASP.filter(a => TIMES.some(t => get(0, t, a)));
      if (!aspects.length) aspects = ['simple'];
      const tl = Object.assign({}, TL, p.timeLabels || {}), al = Object.assign({}, AL, p.aspectLabels || {});
      const anyDeva = sents.some(s => TIMES.some(t => aspects.some(a => DEVA.test(get(sents.indexOf(s), t, a)))));
      const rules = Object.assign({}, anyDeva ? {} : EN_RULES, p.rules || {});
      const showRules = p.showRules !== false, showTL = p.showTimeline !== false;
      const goal = Math.max(1, +p.goal || 3);
      const fixed = Array.isArray(p.targets) ? p.targets.filter(t => t && sents[t.s || 0] && get(t.s || 0, t.time, t.aspect)) : [];
      const challenge = p.challenge || `Set the time machine to make ${goal} target sentences`;
      const cells = []; sents.forEach((_, si) => TIMES.forEach(t => aspects.forEach(a => { if (get(si, t, a)) cells.push({ s: si, time: t, aspect: a }); })));

      let si = 0, time = 'present', aspect = aspects[0];
      let target = null, done = 0, won = false, busy = false, prevKey = '';
      const timers = [];

      host.innerHTML = `<style>
.lb-tensemachine-w{color:#1b1f3a;max-width:400px;margin:0 auto}
.lb-tensemachine-ch{font-weight:800;font-size:13.5px;background:#fff7dd;border-radius:12px;padding:7px 10px;margin-bottom:7px;line-height:1.3}
.lb-tensemachine-tg{display:flex;align-items:center;gap:8px;background:#f1ecff;border-radius:14px;padding:6px 6px 6px 10px;margin-bottom:8px}
.lb-tensemachine-tgt{flex:1;font-weight:800;font-size:14.5px;line-height:1.3}
.lb-tensemachine-tgt small{display:block;font-size:11px;color:#8b5cf6;letter-spacing:.3px}
.lb-tensemachine-dots{display:flex;gap:4px}
.lb-tensemachine-dots i{width:10px;height:10px;border-radius:50%;background:#ddd6fb}
.lb-tensemachine-dots i.on{background:#2ed3a5}
.lb-tensemachine-skip{border:none;font-family:inherit;font-weight:800;font-size:12px;min-width:44px;height:40px;border-radius:11px;background:#fff;color:#6b7090;cursor:pointer}
.lb-tensemachine-scr{position:relative;background:linear-gradient(160deg,#1b1f3a,#2d2f6b);border-radius:18px;padding:10px 46px 10px 12px;color:#fff;min-height:96px;transition:box-shadow .3s}
.lb-tensemachine-scr.hit{box-shadow:0 0 0 3px #2ed3a5,0 0 22px rgba(46,211,165,.6)}
.lb-tensemachine-nm{display:inline-block;font-size:11.5px;font-weight:900;letter-spacing:.4px;background:rgba(255,255,255,.14);border-radius:8px;padding:2px 8px;margin-bottom:4px}
.lb-tensemachine-s{font-size:20px;font-weight:800;line-height:1.3;animation:lbtmin .3s ease}
@keyframes lbtmin{from{opacity:0;transform:translateY(6px);filter:blur(2px)}to{opacity:1;transform:none;filter:none}}
.lb-tensemachine-v{color:#ffc93c;background:rgba(255,201,60,.14);border-radius:6px;padding:0 2px}
.lb-tensemachine-rule{font-size:12.5px;font-weight:700;color:#b9bde6;margin-top:3px}
.lb-tensemachine-rule b{color:#7ff0cf}
.lb-tensemachine-spk{position:absolute;right:6px;top:6px;border:none;width:40px;height:40px;border-radius:12px;background:rgba(255,255,255,.14);font-size:18px;cursor:pointer}
.lb-tensemachine-tl{display:block;width:100%;height:58px;margin:4px 0 0}
.lb-tensemachine-sl{position:relative;height:58px;margin:2px 4px 0;touch-action:none;cursor:pointer;user-select:none;-webkit-user-select:none}
.lb-tensemachine-trk{position:absolute;left:16.66%;right:16.66%;top:16px;height:10px;border-radius:6px;background:linear-gradient(90deg,#8b5cf6,#3b82f6,#2ed3a5)}
.lb-tensemachine-stop{position:absolute;top:13px;width:16px;height:16px;margin-left:-8px;border-radius:50%;background:#fff;border:3px solid #c9cde6}
.lb-tensemachine-knob{position:absolute;top:3px;width:36px;height:36px;margin-left:-18px;border-radius:50%;background:#ffc93c;box-shadow:0 3px 0 #d9a300,0 4px 12px rgba(0,0,0,.18);display:flex;align-items:center;justify-content:center;font-size:17px;transition:left .25s cubic-bezier(.3,1.4,.5,1)}
.lb-tensemachine-sl.drag .lb-tensemachine-knob{transition:none}
.lb-tensemachine-tlab{position:absolute;top:40px;width:33.33%;text-align:center;font-size:12.5px;font-weight:800;color:#6b7090;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lb-tensemachine-tlab.on{color:#1b1f3a}
.lb-tensemachine-asp{display:grid;gap:5px;margin-top:6px}
.lb-tensemachine-a{border:none;font-family:inherit;font-weight:800;font-size:13px;min-height:42px;border-radius:12px;background:#eef0fb;color:#1b1f3a;cursor:pointer;padding:3px 4px;line-height:1.15;box-shadow:0 3px 0 #d3d7ef}
.lb-tensemachine-a.on{background:#3b82f6;color:#fff;box-shadow:0 3px 0 #2560c4}
.lb-tensemachine-a:active{transform:translateY(2px)}
.lb-tensemachine-fb{min-height:18px;text-align:center;font-weight:800;font-size:13px;margin-top:6px;color:#0f7a5c}
</style>
<div class="lb-tensemachine-w">
  <div class="lb-tensemachine-ch">🎯 Challenge: ${esc(challenge)}</div>
  <div class="lb-tensemachine-tg"><div class="lb-tensemachine-tgt"></div><div class="lb-tensemachine-dots"></div><button class="lb-tensemachine-skip" aria-label="new target">🔀</button></div>
  <div class="lb-tensemachine-scr"><span class="lb-tensemachine-nm"></span><div class="lb-tensemachine-s"></div><div class="lb-tensemachine-rule"></div><button class="lb-tensemachine-spk" aria-label="read aloud">🔊</button></div>
  ${showTL ? '<svg class="lb-tensemachine-tl" viewBox="0 0 360 58" aria-hidden="true"></svg>' : ''}
  <div class="lb-tensemachine-sl" role="slider" aria-label="time" aria-valuemin="0" aria-valuemax="2">
    <div class="lb-tensemachine-trk"></div>
    ${TIMES.map((t, i) => `<div class="lb-tensemachine-stop" style="left:${16.66 + i * 33.33}%"></div><div class="lb-tensemachine-tlab" data-t="${t}" style="left:${i * 33.33}%">${TICON[t]} ${esc(tl[t])}</div>`).join('')}
    <div class="lb-tensemachine-knob">⏱</div>
  </div>
  <div class="lb-tensemachine-asp" style="grid-template-columns:repeat(${aspects.length === 4 ? 2 : aspects.length},1fr);${aspects.length < 2 ? 'display:none' : ''}">
    ${aspects.map(a => `<button class="lb-tensemachine-a" data-a="${a}">${esc(al[a])}</button>`).join('')}
  </div>
  <div class="lb-tensemachine-fb"></div>
</div>`;
      const $ = s => host.querySelector(s);
      const scr = $('.lb-tensemachine-scr'), nm = $('.lb-tensemachine-nm'), sEl = $('.lb-tensemachine-s'), ruleEl = $('.lb-tensemachine-rule');
      const svg = $('.lb-tensemachine-tl'), sl = $('.lb-tensemachine-sl'), knob = $('.lb-tensemachine-knob');
      const tgt = $('.lb-tensemachine-tgt'), dots = $('.lb-tensemachine-dots'), fb = $('.lb-tensemachine-fb');

      function timeline() {
        if (!svg) return;
        const X = { past: 62, present: 180, future: 298 }[time];
        const cl = x => Math.max(8, Math.min(352, x));
        let shape = '';
        if (aspect === 'simple') shape = `<circle cx="${X}" cy="22" r="9" fill="#ffc93c" stroke="#d9a300" stroke-width="2"><animate attributeName="r" values="7;10;7" dur="1.6s" repeatCount="indefinite"/></circle>`;
        else if (aspect === 'continuous') shape = `<rect x="${cl(X - 44)}" y="15" width="${cl(X + 44) - cl(X - 44)}" height="14" rx="7" fill="url(#${uid})"/><text x="${X}" y="11" text-anchor="middle" font-size="9.5" font-weight="800" fill="#3b82f6">in progress…</text>`;
        else if (aspect === 'perfect') shape = `<rect x="${cl(X - 80)}" y="15" width="${X - 12 - cl(X - 80)}" height="14" rx="7" fill="#2ed3a5"/><text x="${Math.max(34, X - 46)}" y="11" text-anchor="middle" font-size="9.5" font-weight="800" fill="#0f7a5c">finished ✓</text>`;
        else shape = `<rect x="${cl(X - 80)}" y="15" width="${X - cl(X - 80)}" height="14" rx="7" fill="url(#${uid})"/><path d="M${X - 4} 12 L${X + 4} 22 L${X - 4} 32" fill="none" stroke="#3b82f6" stroke-width="3" stroke-linecap="round"/><text x="${Math.max(34, X - 40)}" y="11" text-anchor="middle" font-size="9.5" font-weight="800" fill="#3b82f6">ongoing ➜</text>`;
        svg.innerHTML = `<defs><pattern id="${uid}" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="14" height="14" fill="#3b82f6"/><rect width="6" height="14" fill="#8db8ff"/><animateTransform attributeName="patternTransform" type="translate" from="0 0" to="14 0" dur="0.8s" repeatCount="indefinite" additive="sum"/></pattern></defs>
          <line x1="6" y1="22" x2="350" y2="22" stroke="#e1e4f3" stroke-width="4" stroke-linecap="round"/>
          <path d="M346 16 L354 22 L346 28" fill="none" stroke="#c9cde6" stroke-width="3" stroke-linecap="round"/>
          <line x1="180" y1="6" x2="180" y2="40" stroke="#ff6b6b" stroke-width="2" stroke-dasharray="4 3"/>
          <text x="180" y="52" text-anchor="middle" font-size="10.5" font-weight="900" fill="#ff6b6b">NOW</text>
          <text x="8" y="52" font-size="10" font-weight="800" fill="#a4a8c6">earlier</text><text x="352" y="52" text-anchor="end" font-size="10" font-weight="800" fill="#a4a8c6">later</text>
          ${time !== 'present' ? `<line x1="${X}" y1="8" x2="${X}" y2="38" stroke="#8b5cf6" stroke-width="2"/><text x="${X}" y="52" text-anchor="middle" font-size="10" font-weight="900" fill="#8b5cf6">then</text>` : ''}
          ${shape}`;
      }

      function draw(animate) {
        const s = get(si, time, aspect);
        nm.textContent = `${tl[time]}${aspects.length > 1 ? ' · ' + al[aspect] : ''}`;
        const html = s ? marked(s) : '<span style="opacity:.6">— (no form given)</span>';
        if (animate) { sEl.style.animation = 'none'; void sEl.offsetWidth; sEl.style.animation = ''; }
        sEl.innerHTML = html;
        const r = rules[time + '.' + aspect];
        ruleEl.innerHTML = showRules && r ? `Verb = <b>${esc(r)}</b>` : (sents[si].meaning ? esc(sents[si].meaning) : '');
        knob.style.left = (16.66 + TIMES.indexOf(time) * 33.33) + '%';
        sl.setAttribute('aria-valuenow', TIMES.indexOf(time));
        host.querySelectorAll('.lb-tensemachine-tlab').forEach(e => e.classList.toggle('on', e.dataset.t === time));
        host.querySelectorAll('.lb-tensemachine-a').forEach(e => e.classList.toggle('on', e.dataset.a === aspect));
        timeline();
      }

      function newTarget() {
        let pool;
        if (fixed.length) { const t = fixed[done % fixed.length]; target = { s: t.s || 0, time: t.time, aspect: t.aspect }; }
        else {
          pool = cells.filter(c => !(c.time === time && c.aspect === aspect) && (c.s + c.time + c.aspect) !== prevKey);
          if (!pool.length) pool = cells;
          target = pool[Math.floor(Math.random() * pool.length)];
        }
        prevKey = target.s + target.time + target.aspect;
        if (si !== target.s) { si = target.s; }
        // make sure the machine is not already showing the target
        if (time === target.time && aspect === target.aspect) {
          time = TIMES.find(t => t !== target.time && get(si, t, aspect)) || time;
          if (time === target.time) aspect = aspects.find(a => a !== target.aspect) || aspect;
        }
        tgt.innerHTML = `<small>MAKE THIS SENTENCE</small>${esc(plain(get(target.s, target.time, target.aspect)))}`;
        scr.classList.remove('hit'); fb.textContent = '';
        drawDots(); draw(true);
      }
      function drawDots() { dots.innerHTML = Array.from({ length: goal }, (_, i) => `<i class="${i < done ? 'on' : ''}"></i>`).join(''); }

      function changed() {
        api.sfx('tap'); draw(true);
        if (busy || !target) return;
        if (si === target.s && time === target.time && aspect === target.aspect) {
          busy = true; done++; scr.classList.add('hit'); drawDots();
          api.sfx('correct'); api.speak(plain(get(si, time, aspect)));
          fb.textContent = `✅ Yes! That is the ${tl[time]}${aspects.length > 1 ? ' ' + al[aspect] : ''} form.`;
          if (done >= goal && !won) { won = true; api.win(`Time traveller! You made ${goal} target sentences.`); }
          timers.push(setTimeout(() => { busy = false; newTarget(); }, 1700));
        }
      }

      // slider
      let drag = null;
      function tFromX(x) { const r = sl.getBoundingClientRect(); const f = (x - r.left) / r.width; return TIMES[Math.max(0, Math.min(2, Math.floor(f * 3)))]; }
      function down(e) {
        if (!e.target.closest('.lb-tensemachine-sl')) return;
        drag = e.pointerId; sl.classList.add('drag');
        try { sl.setPointerCapture(e.pointerId); } catch (_) {}
        e.preventDefault(); moveTo(e.clientX);
      }
      function moveTo(x) {
        const r = sl.getBoundingClientRect();
        const lo = r.width * 0.1666, hi = r.width * 0.8333;
        knob.style.left = Math.max(lo, Math.min(hi, x - r.left)) + 'px';
        const t = tFromX(x); if (t !== time) { time = t; changed(); knob.style.left = Math.max(lo, Math.min(hi, x - r.left)) + 'px'; }
      }
      function move(e) { if (drag === e.pointerId) moveTo(e.clientX); }
      function up(e) { if (drag !== e.pointerId) return; drag = null; sl.classList.remove('drag'); draw(false); }
      function onClick(e) {
        const b = e.target.closest('button'); if (!b || !host.contains(b)) return;
        if (b.dataset.a && aspect !== b.dataset.a) { aspect = b.dataset.a; changed(); }
        else if (b.classList.contains('lb-tensemachine-spk')) api.speak(plain(get(si, time, aspect)));
        else if (b.classList.contains('lb-tensemachine-skip') && !busy) { api.sfx('tap'); newTarget(); }
      }
      sl.addEventListener('pointerdown', down);
      sl.addEventListener('pointermove', move);
      sl.addEventListener('pointerup', up);
      sl.addEventListener('pointercancel', up);
      host.addEventListener('click', onClick);
      newTarget();
      return () => {
        timers.forEach(clearTimeout);
        sl.removeEventListener('pointerdown', down); sl.removeEventListener('pointermove', move);
        sl.removeEventListener('pointerup', up); sl.removeEventListener('pointercancel', up);
        host.removeEventListener('click', onClick);
      };
    },
    example: {
      challenge: 'Slide through time and pick the aspect to make 3 target sentences',
      goal: 3,
      sentences: [
        { forms: {
          past: { simple: 'Riya [played] football.', continuous: 'Riya [was playing] football.', perfect: 'Riya [had played] football.' },
          present: { simple: 'Riya [plays] football.', continuous: 'Riya [is playing] football.', perfect: 'Riya [has played] football.' },
          future: { simple: 'Riya [will play] football.', continuous: 'Riya [will be playing] football.', perfect: 'Riya [will have played] football.' } } },
        { forms: {
          past: { simple: 'They [finished] the work.', continuous: 'They [were finishing] the work.', perfect: 'They [had finished] the work.' },
          present: { simple: 'They [finish] the work.', continuous: 'They [are finishing] the work.', perfect: 'They [have finished] the work.' },
          future: { simple: 'They [will finish] the work.', continuous: 'They [will be finishing] the work.', perfect: 'They [will have finished] the work.' } } }
      ]
    },
    examples: [
      {
        challenge: 'All 12 tenses! Make 4 target sentences',
        goal: 4,
        sentences: [
          { forms: {
            past: { simple: 'I [wrote] a story.', continuous: 'I [was writing] a story.', perfect: 'I [had written] a story.', perfectContinuous: 'I [had been writing] a story.' },
            present: { simple: 'I [write] a story.', continuous: 'I [am writing] a story.', perfect: 'I [have written] a story.', perfectContinuous: 'I [have been writing] a story.' },
            future: { simple: 'I [will write] a story.', continuous: 'I [will be writing] a story.', perfect: 'I [will have written] a story.', perfectContinuous: 'I [will have been writing] a story.' } } }
        ]
      },
      {
        challenge: 'काल-यंत्र से लक्ष्य वाक्य बनाओ',
        goal: 3,
        timeLabels: { past: 'भूतकाल', present: 'वर्तमान', future: 'भविष्यत्' },
        aspectLabels: { simple: 'सामान्य', continuous: 'अपूर्ण', perfect: 'पूर्ण' },
        sentences: [
          { forms: {
            past: { simple: 'राम विद्यालय [गया]।', continuous: 'राम विद्यालय [जा रहा था]।', perfect: 'राम विद्यालय [जा चुका था]।' },
            present: { simple: 'राम विद्यालय [जाता है]।', continuous: 'राम विद्यालय [जा रहा है]।', perfect: 'राम विद्यालय [जा चुका है]।' },
            future: { simple: 'राम विद्यालय [जाएगा]।', continuous: 'राम विद्यालय [जा रहा होगा]।', perfect: 'राम विद्यालय [जा चुका होगा]।' } } }
        ]
      },
      {
        challenge: 'लकार बदलो: लट् (वर्तमान), लङ् (भूत), लृट् (भविष्यत्)',
        goal: 3,
        aspects: ['simple'],
        timeLabels: { past: 'लङ्', present: 'लट्', future: 'लृट्' },
        sentences: [
          { meaning: 'The boy reads.', forms: { past: { simple: 'बालकः [अपठत्]।' }, present: { simple: 'बालकः [पठति]।' }, future: { simple: 'बालकः [पठिष्यति]।' } } },
          { meaning: 'The students go.', forms: { past: { simple: 'छात्राः [अगच्छन्]।' }, present: { simple: 'छात्राः [गच्छन्ति]।' }, future: { simple: 'छात्राः [गमिष्यन्ति]।' } } },
          { meaning: 'You write.', forms: { past: { simple: 'त्वम् [अलिखः]।' }, present: { simple: 'त्वं [लिखसि]।' }, future: { simple: 'त्वं [लेखिष्यसि]।' } } }
        ]
      }
    ]
  });
})();
