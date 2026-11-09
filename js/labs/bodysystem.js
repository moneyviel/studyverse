/* Knowtopia Concept Lab: bodysystem — "Body systems explorer"
 *
 * PARAMS (all optional)
 *  system     string  starting system: 'digestive' | 'respiratory' | 'circulatory' | 'excretory' | 'nervous'
 *                                                                                           default 'digestive'
 *  systems    array   systems offered as tabs                                default all five
 *  order      object  per-system list of organ ids the child must put in order, e.g.
 *                     {digestive:['mouth','oesophagus','stomach','smallint','largeint','rectum','anus']}
 *                     (organ ids listed below). Default = the main path of each system.
 *  names      object  organ id → display name (e.g. Hindi)                  default English names
 *  jobs       object  organ id → job text                                   default built-in
 *  goal       string  'order' (put the path organs in order — win) | 'all' (order challenge in EVERY offered
 *                     system before winning) | 'explore' (tap every organ of the system to win)  default 'order'
 *  challenge  string  challenge sentence (any language); a default is generated
 *
 *  Organ ids — digestive: mouth, oesophagus, stomach, smallint, largeint, rectum, anus, liver, pancreas
 *              respiratory: nose, trachea, bronchi, lungs, alveoli, diaphragm
 *              circulatory: heart, arteries, capillaries, veins, lungs
 *              excretory: kidneys, ureters, bladder, urethra, renalartery
 *              nervous: receptor, sensory, spinal, motor, muscle, brain
 */
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[<>&"]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]));
  const hit = d => `<path d="${d}" fill="none" stroke="transparent" stroke-width="16" stroke-linecap="round"/>`;
  // ---------------------------------------------------------------- systems (viewBox 0 0 200 360)
  const SYS = {
    digestive: {
      name: 'Digestive', icon: '🍎', dot: '#ff9f43', what: 'food',
      organs: {
        liver: ['Liver', 'Makes bile, which breaks fats into tiny drops.', `<path d="M60 140 Q62 124 86 126 Q104 128 104 136 Q100 152 72 152 Q60 150 60 140 Z" fill="#b5523b"/>`],
        pancreas: ['Pancreas', 'Makes pancreatic juice with enzymes for digestion.', `<ellipse cx="108" cy="166" rx="15" ry="4.5" fill="#f6c26b"/>`],
        mouth: ['Mouth', 'Teeth chew food; saliva starts digesting starch.', `<ellipse cx="100" cy="50" rx="8" ry="3.6" fill="#e35d6a"/>`],
        oesophagus: ['Oesophagus (food pipe)', 'Muscles squeeze food down to the stomach (peristalsis).', `<path d="M100 56 L100 120 Q101 131 108 137" fill="none" stroke="#f08f8f" stroke-width="5" stroke-linecap="round"/>`],
        stomach: ['Stomach', 'Churns food with acid and juices; starts digesting proteins.', `<path d="M106 133 Q128 120 132 140 Q133 160 112 161 Q102 160 104 150 Q110 146 106 133 Z" fill="#f4a3a8" stroke="#e07c86" stroke-width="1.5"/>`],
        smallint: ['Small intestine', 'Finishes digestion; nutrients are absorbed into the blood (villi).', `<path d="M90 172 Q112 172 112 180 Q112 186 92 186 Q86 192 108 194 Q114 200 90 202 Q84 208 104 210" fill="none" stroke="#f7b39a" stroke-width="7" stroke-linecap="round"/>`],
        largeint: ['Large intestine', 'Absorbs water from the undigested food.', `<path d="M82 214 L79 178 Q80 170 90 170 L112 170 Q122 170 122 178 L121 210 Q120 220 108 222" fill="none" stroke="#d98b6c" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`],
        rectum: ['Rectum', 'Stores the waste (faeces) for a while.', `<path d="M104 222 L100 236" fill="none" stroke="#c46f55" stroke-width="7" stroke-linecap="round"/>`],
        anus: ['Anus', 'Waste leaves the body — egestion.', `<circle cx="100" cy="242" r="3.5" fill="#8a4a3b"/>`]
      },
      path: [['mouth', [[100, 50]]], ['oesophagus', [[100, 58], [100, 120], [106, 134]]], ['stomach', [[116, 138], [126, 146], [118, 156], [108, 157]]],
        ['smallint', [[96, 172], [110, 178], [92, 186], [108, 194], [90, 202], [104, 210]]], ['largeint', [[82, 212], [80, 178], [90, 171], [112, 171], [121, 178], [121, 210], [108, 221]]],
        ['rectum', [[102, 228], [100, 236]]], ['anus', [[100, 242]]]],
      order: ['mouth', 'oesophagus', 'stomach', 'smallint', 'largeint', 'rectum', 'anus']
    },
    respiratory: {
      name: 'Respiratory', icon: '🫁', dot: '#3b82f6', what: 'air',
      organs: {
        lungs: ['Lungs', 'Two spongy organs filled with millions of air sacs.', `<path d="M96 108 Q76 104 64 124 Q56 150 64 162 Q80 166 96 158 Z" fill="#f6a5b5" stroke="#e48aa0" stroke-width="1.5"/><path d="M104 108 Q124 104 136 124 Q144 150 136 162 Q120 166 104 158 Z" fill="#f6a5b5" stroke="#e48aa0" stroke-width="1.5"/>`],
        diaphragm: ['Diaphragm', 'Muscle under the lungs. It moves down to pull air in.', `<path d="M56 170 Q100 150 144 170" fill="none" stroke="#d07a7a" stroke-width="5" stroke-linecap="round"/>`],
        nose: ['Nose', 'Air goes in. Hairs and mucus trap dust; air gets warm and moist.', `<path d="M100 36 L95 47 L105 47 Z" fill="#f0a77f"/>`],
        trachea: ['Trachea (windpipe)', 'Carries air to the chest. Rings of cartilage keep it open.', `<path d="M100 50 L100 106" stroke="#8fc2ff" stroke-width="7" stroke-linecap="round"/><path d="M96 60h8M96 70h8M96 80h8M96 90h8M96 100h8" stroke="#5a9be6" stroke-width="1.5"/>`],
        bronchi: ['Bronchi', 'Two tubes that take air into each lung, branching again and again.', `<path d="M100 106 L84 120 L80 136 M100 106 L116 120 L120 136" fill="none" stroke="#8fc2ff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>`],
        alveoli: ['Alveoli (air sacs)', 'Oxygen passes into the blood here; carbon dioxide comes out.', `<g fill="#ffd0dc" stroke="#e48aa0" stroke-width="1"><circle cx="76" cy="146" r="4"/><circle cx="83" cy="150" r="4"/><circle cx="76" cy="154" r="4"/><circle cx="70" cy="149" r="3.6"/></g>`]
      },
      path: [['nose', [[100, 42]]], ['trachea', [[100, 52], [100, 104]]], ['bronchi', [[90, 114], [83, 124], [80, 134]]], ['lungs', [[78, 140]]], ['alveoli', [[77, 150]]]],
      back: true,
      order: ['nose', 'trachea', 'bronchi', 'lungs', 'alveoli']
    },
    circulatory: {
      name: 'Circulatory', icon: '❤️', dot: '#e53950', what: 'blood',
      organs: {
        lungs: ['Lungs', 'Blood picks up oxygen and gives out carbon dioxide here.', `<ellipse cx="80" cy="128" rx="15" ry="26" fill="#f9cbd5" opacity=".8"/><ellipse cx="120" cy="128" rx="15" ry="26" fill="#f9cbd5" opacity=".8"/>`],
        arteries: ['Arteries', 'Carry blood AWAY from the heart, under high pressure.', `<path d="M104 120 L104 54 M104 140 L104 218 L118 232 L122 336 M104 124 Q150 104 168 212 M104 124 Q52 100 34 212" fill="none" stroke="#e53950" stroke-width="3.5" stroke-linecap="round"/>`],
        veins: ['Veins', 'Bring blood BACK to the heart. They have valves.', `<path d="M96 120 L96 54 M96 140 L96 222 L82 232 L78 336 M98 130 Q146 112 162 214 M98 130 Q56 112 40 214" fill="none" stroke="#3b6fe0" stroke-width="3.5" stroke-linecap="round"/>`],
        capillaries: ['Capillaries', 'Tiny thin vessels: oxygen and food pass to the cells; wastes are picked up.', `<path d="M122 336 Q110 346 100 342 Q90 346 78 336 M122 336 Q100 334 78 336 M116 340 Q104 330 90 340" fill="none" stroke="#9b4dca" stroke-width="2"/>`],
        heart: ['Heart', 'A muscular pump. It beats about 72 times a minute.', `<path d="M100 140 C 86 130, 88 116, 96 116 Q100 116 100 122 Q100 116 104 116 C 112 116, 114 130, 100 140 Z" transform="translate(-50 -64) scale(1.5)" fill="#e53950" stroke="#b8243a" stroke-width="1"/>`]
      },
      path: [['heart', [[100, 128]]], ['arteries', [[104, 142], [104, 218], [118, 232], [122, 334]]], ['capillaries', [[112, 340], [100, 341], [88, 340]]], ['veins', [[78, 334], [82, 232], [96, 222], [96, 142]]],
        ['heart', [[100, 128]]], ['lungs', [[84, 120], [78, 132], [90, 128]]], ['heart', [[100, 128]]]],
      order: ['heart', 'arteries', 'capillaries', 'veins']
    },
    excretory: {
      name: 'Excretory', icon: '💧', dot: '#f2b705', what: 'urine',
      organs: {
        renalartery: ['Blood vessels', 'Blood with wastes (urea) reaches the kidneys through the renal artery.', `<path d="M98 120 L98 230 M98 170 L88 174 M98 182 L112 178" fill="none" stroke="#e53950" stroke-width="3" stroke-linecap="round"/><path d="M103 120 L103 230" fill="none" stroke="#3b6fe0" stroke-width="3"/>`],
        kidneys: ['Kidneys', 'Filter the blood and make urine from wastes and extra water.', `<path d="M78 162 Q70 164 70 178 Q70 192 80 192 Q88 190 86 182 Q84 176 88 172 Q88 162 78 162 Z" fill="#a0434f"/><path d="M122 162 Q130 164 130 178 Q130 192 120 192 Q112 190 114 182 Q116 176 112 172 Q112 162 122 162 Z" fill="#a0434f"/>`],
        ureters: ['Ureters', 'Two tubes carrying urine from the kidneys to the bladder.', `<path d="M84 186 Q90 204 95 214 M116 186 Q110 204 105 214" fill="none" stroke="#e8b84a" stroke-width="3" stroke-linecap="round"/>`],
        bladder: ['Urinary bladder', 'A muscular bag that stores urine.', `<ellipse cx="100" cy="221" rx="13" ry="9.5" fill="#f3d36b" stroke="#d9b13d" stroke-width="1.5"/>`],
        urethra: ['Urethra', 'Urine leaves the body through this tube.', `<path d="M100 230 L100 246" stroke="#e8b84a" stroke-width="3.5" stroke-linecap="round"/>`]
      },
      path: [['renalartery', [[98, 140], [98, 170], [88, 174]]], ['kidneys', [[80, 176]]], ['ureters', [[86, 192], [92, 205], [96, 214]]], ['bladder', [[100, 221]]], ['urethra', [[100, 232], [100, 246]]]],
      order: ['kidneys', 'ureters', 'bladder', 'urethra']
    },
    nervous: {
      name: 'Nervous', icon: '⚡', dot: '#8b5cf6', what: 'message',
      organs: {
        brain: ['Brain', 'The control centre: thinking, memory, senses. Reflexes do not wait for it!', `<ellipse cx="100" cy="32" rx="20" ry="15" fill="#f7a8c4" stroke="#e07fa3" stroke-width="1.5"/><path d="M90 26 q4 -4 8 0 q4 4 8 0 M88 34 q5 -3 10 0 q5 3 10 0" fill="none" stroke="#e07fa3" stroke-width="1.2"/>`],
        spinal: ['Spinal cord', 'Carries messages up and down; quick reflexes are decided here.', `<path d="M100 52 L100 226" stroke="#f2b705" stroke-width="5" stroke-linecap="round"/>`],
        receptor: ['Receptor (skin)', 'Senses heat, pain or touch — e.g. a hot pan!', `<circle cx="169" cy="224" r="7" fill="#ff9f43" stroke="#e07020" stroke-width="1.5"/><text x="169" y="245" text-anchor="middle" font-size="12">🔥</text>`],
        sensory: ['Sensory nerve', 'Carries the message from the receptor to the spinal cord.', `<path d="M166 218 Q160 160 140 132 Q124 118 103 118" fill="none" stroke="#8b5cf6" stroke-width="2.6" stroke-dasharray="5 3"/>`],
        motor: ['Motor nerve', 'Carries the order from the spinal cord to the muscle.', `<path d="M103 128 Q128 132 146 146" fill="none" stroke="#2ed3a5" stroke-width="2.6"/>`],
        muscle: ['Muscle (effector)', 'Contracts and pulls the hand away — the reflex action!', `<ellipse cx="153" cy="152" rx="7" ry="13" transform="rotate(-18 153 152)" fill="#e86a6a"/>`]
      },
      path: [['receptor', [[169, 224]]], ['sensory', [[166, 210], [160, 160], [140, 132], [104, 118]]], ['spinal', [[100, 118], [100, 128]]], ['motor', [[104, 128], [128, 133], [146, 146]]], ['muscle', [[153, 152]]]],
      order: ['receptor', 'sensory', 'spinal', 'motor', 'muscle']
    }
  };
  const BODY = `<g fill="#ffe3cc" stroke="#efb994" stroke-width="2">
    <path d="M80 228 L77 350 M120 228 L123 350" stroke="#efb994" stroke-width="27" stroke-linecap="round" fill="none"/>
    <path d="M54 92 Q38 150 32 214 M146 92 Q162 150 168 214" stroke="#efb994" stroke-width="20" stroke-linecap="round" fill="none"/>
    <path d="M80 228 L77 350 M120 228 L123 350" stroke="#ffe3cc" stroke-width="23" stroke-linecap="round" fill="none"/>
    <path d="M54 92 Q38 150 32 214 M146 92 Q162 150 168 214" stroke="#ffe3cc" stroke-width="16" stroke-linecap="round" fill="none"/>
    <circle cx="31" cy="222" r="9"/><circle cx="169" cy="222" r="9"/>
    <path d="M70 78 Q100 72 130 78 L146 88 Q154 140 140 236 Q100 246 60 236 Q46 140 54 88 Z"/>
    <rect x="90" y="58" width="20" height="22" rx="6" stroke="none"/>
    <circle cx="100" cy="36" r="26"/></g>
    <g fill="#1b1f3a" opacity=".55"><circle cx="91" cy="34" r="2.2"/><circle cx="109" cy="34" r="2.2"/></g>`;

  const CSS = `
  .lb-bodysystem{font-weight:700;color:#1b1f3a;user-select:none;-webkit-user-select:none}
  .lb-bodysystem-ch{background:#f3efff;color:#4c2fb0;border-radius:14px;padding:8px 11px;font-size:13.5px;line-height:1.3;margin-bottom:7px}
  .lb-bodysystem-tabs{display:flex;gap:5px;overflow-x:auto;scrollbar-width:none;margin-bottom:6px}
  .lb-bodysystem-tabs::-webkit-scrollbar{display:none}
  .lb-bodysystem-tab{flex:none;min-height:38px;border:2px solid #e3e6f6;background:#fff;border-radius:12px;padding:0 9px;font-family:inherit;font-weight:800;font-size:12.5px;cursor:pointer;color:#1b1f3a}
  .lb-bodysystem-tab.on{background:#8b5cf6;border-color:#8b5cf6;color:#fff}
  .lb-bodysystem-tab.ok::after{content:' ✓'}
  .lb-bodysystem-wrap{display:flex;gap:8px}
  .lb-bodysystem-wrap>svg{flex:none;width:46%;max-width:170px;height:auto;background:linear-gradient(#f6f8ff,#eef1fb);border-radius:16px}
  .lb-bodysystem-side{flex:1;display:flex;flex-direction:column;gap:6px;min-width:0}
  .lb-bodysystem-info{background:#f7f8fd;border-radius:14px;padding:8px 9px;font-size:12px;color:#6b7090;line-height:1.3;min-height:78px}
  .lb-bodysystem-info b{display:block;color:#1b1f3a;font-size:14px;margin-bottom:2px;line-height:1.15}
  .lb-bodysystem-info.bad{background:#fff0f0}.lb-bodysystem-info.good{background:#e3fbf3}
  .lb-bodysystem-btn{min-height:40px;border:none;border-radius:12px;font-family:inherit;font-weight:800;font-size:13px;cursor:pointer;color:#fff;background:#8b5cf6;box-shadow:0 3px 0 #5b33c9}
  .lb-bodysystem-btn:active{transform:translateY(2px);box-shadow:none}
  .lb-bodysystem-lbl{font-size:11.5px;color:#6b7090;line-height:1.2}.lb-bodysystem-lbl:empty{display:none}
  .lb-bodysystem-chips{display:grid;grid-template-columns:1fr 1fr;gap:4px}
  .lb-bodysystem-chip{min-height:40px;border:2px solid #e3e6f6;background:#fff;border-radius:11px;font-family:inherit;font-weight:800;font-size:11px;line-height:1.1;color:#1b1f3a;cursor:pointer;padding:2px 3px}
  .lb-bodysystem-chip.ok{background:#e3fbf3;border-color:#2ed3a5;color:#0f7a5c}
  .lb-bodysystem-chip.shake{animation:lb-bodysystem-sh .35s}
  @keyframes lb-bodysystem-sh{25%{transform:translateX(-4px)}75%{transform:translateX(4px)}}
  .lb-bodysystem-o{cursor:pointer;transition:opacity .3s}
  .lb-bodysystem-o.hl{filter:drop-shadow(0 0 4px #ffc93c) drop-shadow(0 0 2px #ffc93c)}
  .lb-bodysystem-o.dim{opacity:.55}`;

  Labs.register('bodysystem', {
    title: 'Body systems explorer',
    subjects: ['science', 'biology', 'evs'],
    render(host, p, api) {
      const sysList = (Array.isArray(p.systems) && p.systems.length ? p.systems : Object.keys(SYS)).filter(k => SYS[k]);
      if (!sysList.length) sysList.push('digestive');
      let cur = SYS[p.system] && sysList.includes(p.system) ? p.system : sysList[0];
      const names = (p.names && typeof p.names === 'object') ? p.names : {}, jobs = (p.jobs && typeof p.jobs === 'object') ? p.jobs : {};
      const goalT = ['order', 'all', 'explore'].includes(p.goal) ? p.goal : 'order';
      const nm = (s, id) => String(names[id] || SYS[s].organs[id][0]);
      const job = (s, id) => String(jobs[id] || SYS[s].organs[id][1]);
      const orderOf = s => { const o = p.order && Array.isArray(p.order[s]) ? p.order[s].filter(id => SYS[s].organs[id]) : null; return o && o.length >= 2 ? o : SYS[s].order; };
      let challenge = p.challenge;
      if (!challenge) {
        if (goalT === 'explore') challenge = `Tap every organ of the ${SYS[cur].name.toLowerCase()} system to learn its job.`;
        else if (goalT === 'all') challenge = 'Put the organs in the right order for every body system!';
        else challenge = `Watch the path, then put the ${SYS[cur].name.toLowerCase()} system organs in order (tap the names).`;
      }
      host.innerHTML = `<style>${CSS}</style><div class="lb-bodysystem">
        <div class="lb-bodysystem-ch">🎯 Challenge: ${esc(challenge)}</div>
        ${sysList.length > 1 ? `<div class="lb-bodysystem-tabs">${sysList.map(k => `<button class="lb-bodysystem-tab" data-s="${k}">${SYS[k].icon} ${SYS[k].name}</button>`).join('')}</div>` : ''}
        <div class="lb-bodysystem-wrap"><svg viewBox="0 0 200 360"></svg>
          <div class="lb-bodysystem-side"><div class="lb-bodysystem-info"></div><button class="lb-bodysystem-btn lb-bodysystem-play">▶ Play path</button>
            <div class="lb-bodysystem-lbl"></div><div class="lb-bodysystem-chips"></div></div></div></div>`;
      const root = host.querySelector('.lb-bodysystem'), svg = root.querySelector('svg'), info = root.querySelector('.lb-bodysystem-info');
      const chipsEl = root.querySelector('.lb-bodysystem-chips'), lbl = root.querySelector('.lb-bodysystem-lbl'), playB = root.querySelector('.lb-bodysystem-play');
      let raf = 0, alive = true, timers = [], won = false;
      const later = (f, ms) => timers.push(setTimeout(f, ms));
      const winOnce = m => { if (won) return; won = true; api.sfx('correct'); api.win(m); };
      const solved = new Set(); let seen = new Set(), placed = [], playing = null;
      const setInfo = (h, c) => { info.innerHTML = h; info.className = 'lb-bodysystem-info' + (c ? ' ' + c : ''); };

      function shuffle(a, seed) { const r = a.slice(); let s = seed; for (let i = r.length - 1; i > 0; i--) { s = (s * 9301 + 49297) % 233280; const j = Math.floor(s / 233280 * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; } if (r.join() === a.join() && r.length > 1) r.push(r.shift()); return r; }

      function build() {
        stop();
        root.querySelectorAll('[data-s]').forEach(b => { b.classList.toggle('on', b.dataset.s === cur); b.classList.toggle('ok', solved.has(b.dataset.s)); });
        const S = SYS[cur];
        let s = BODY;
        for (const id in S.organs) s += `<g class="lb-bodysystem-o" data-o="${id}">${S.organs[id][2]}</g>`;
        s += `<g class="lb-bodysystem-badges"></g><circle class="lb-bodysystem-dot" r="5.5" fill="${S.dot}" stroke="#fff" stroke-width="2" style="display:none"/>`;
        svg.innerHTML = s;
        // generous invisible hit areas on top
        svg.querySelectorAll('.lb-bodysystem-o').forEach(g => {
          let bb; try { bb = g.getBBox(); } catch (e) { return; }
          const r = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
          const pad = 4; r.setAttribute('x', bb.x - pad); r.setAttribute('y', bb.y - pad); r.setAttribute('width', bb.width + 2 * pad); r.setAttribute('height', bb.height + 2 * pad); r.setAttribute('fill', 'transparent');
          g.appendChild(r);
          g.addEventListener('click', () => tapOrgan(g.dataset.o));
        });
        placed = []; seen = new Set();
        const ord = orderOf(cur);
        lbl.textContent = goalT === 'explore' ? `Tap each organ on the body (${0}/${Object.keys(S.organs).length})` : '';
        chipsEl.innerHTML = goalT === 'explore' ? '' : shuffle(ord, ord.length * 17 + cur.length).map(id => `<button class="lb-bodysystem-chip" data-c="${id}">${esc(nm(cur, id))}</button>`).join('');
        chipsEl.querySelectorAll('[data-c]').forEach(b => b.onclick = () => choose(b));
        setInfo(goalT === 'explore' ? `<b>${S.icon} ${S.name} system</b>Press ▶ to watch the ${S.what} travel. Tap any organ to learn its job.`
          : `<b>${S.icon} ${S.name} system</b>Press ▶ to watch the ${S.what} travel, then tap the names below in order. Tap organs to learn their jobs.`);
        badges();
      }
      function badges() {
        const g = svg.querySelector('.lb-bodysystem-badges'); let s = '';
        const S = SYS[cur], pos = {};
        S.path.forEach(([id, pts]) => { if (!pos[id]) pos[id] = [pts.reduce((a, q) => a + q[0], 0) / pts.length, pts.reduce((a, q) => a + q[1], 0) / pts.length]; });
        placed.forEach((id, i) => { const pt = pos[id] || [100, 100]; s += `<circle cx="${pt[0] + 10}" cy="${pt[1] - 8}" r="7.5" fill="#2ed3a5" stroke="#fff" stroke-width="1.5"/><text x="${pt[0] + 10}" y="${pt[1] - 4.6}" text-anchor="middle" font-size="9.5" font-weight="900" fill="#fff">${i + 1}</text>`; });
        g.innerHTML = s;
      }
      function hl(id) { svg.querySelectorAll('.lb-bodysystem-o').forEach(g => { g.classList.toggle('hl', g.dataset.o === id); }); }
      function tapOrgan(id) {
        if (playing) return; api.sfx('tap'); hl(id); setInfo(`<b>${esc(nm(cur, id))}</b>${esc(job(cur, id))}`);
        seen.add(id);
        if (goalT === 'explore') {
          const n = Object.keys(SYS[cur].organs).length; lbl.textContent = `Tap each organ on the body (${seen.size}/${n})`;
          if (seen.size === n) later(() => winOnce(`You explored the whole ${SYS[cur].name.toLowerCase()} system!`), 400);
        }
      }
      function choose(b) {
        if (playing) stop();
        const ord = orderOf(cur), id = b.dataset.c;
        if (placed.includes(id)) return;
        if (ord[placed.length] === id) {
          placed.push(id); b.classList.add('ok'); b.textContent = placed.length + '. ' + nm(cur, id); api.sfx('coin'); hl(id);
          setInfo(`<b>${placed.length}. ${esc(nm(cur, id))}</b>${esc(job(cur, id))}`, 'good'); badges();
          if (placed.length === ord.length) {
            solved.add(cur); root.querySelectorAll('[data-s]').forEach(t => t.classList.toggle('ok', solved.has(t.dataset.s)));
            if (goalT === 'all' && sysList.some(k => !solved.has(k))) { setInfo(`<b>✓ ${SYS[cur].name} done!</b>Now try another system tab.`, 'good'); api.sfx('unlock'); }
            else later(() => winOnce(`Correct order: ${ord.map(o => nm(cur, o)).join(' → ')}`), 300);
            later(() => play(), 700);
          }
        } else {
          api.sfx('wrong'); b.classList.remove('shake'); void b.offsetWidth; b.classList.add('shake');
          const prev = placed.length ? nm(cur, placed[placed.length - 1]) : null;
          setInfo(`<b>Not yet!</b>${prev ? `After the ${esc(prev.toLowerCase())}, where does the ${SYS[cur].what} go next?` : `Where does the ${SYS[cur].what} enter first?`} Tip: press ▶ to watch.`, 'bad');
        }
      }
      // ---- animation along the path ----
      function play() {
        stop(); const S = SYS[cur], dot = svg.querySelector('.lb-bodysystem-dot');
        let segs = S.path.map(([id, pts]) => ({ id, pts }));
        if (S.back) segs = segs.concat(segs.slice(0, -1).reverse().map(sg => ({ id: sg.id, pts: sg.pts.slice().reverse(), back: true })));
        const pts = []; segs.forEach(sg => sg.pts.forEach(pt => pts.push({ x: pt[0], y: pt[1], id: sg.id, back: !!sg.back })));
        let i = 0, x = pts[0].x, y = pts[0].y, lastId = null, hold = 0.5, last = performance.now();
        dot.style.display = ''; playing = true; playB.textContent = '■ Stop';
        const step = now => {
          if (!alive || !playing) return;
          const dt = Math.min(0.05, Math.max(0, (now - last) / 1000)); last = now;
          const tg = pts[i];
          if (hold > 0) hold -= dt;
          else {
            const d = Math.hypot(tg.x - x, tg.y - y), v = 70 * dt;
            if (d <= v) {
              x = tg.x; y = tg.y;
              if (tg.id !== lastId) {
                lastId = tg.id; hl(tg.id); hold = 0.55;
                let extra = '';
                if (cur === 'respiratory') extra = tg.back ? ' <i>(breathing out: CO₂)</i>' : ' <i>(breathing in: O₂)</i>';
                setInfo(`<b>${esc(nm(cur, tg.id))}</b>${esc(job(cur, tg.id))}${extra}`);
                if (cur === 'circulatory') {
                  if (tg.id === 'capillaries') { dot.setAttribute('fill', '#3b6fe0'); extra = ' <i>(gives O₂ to cells → blood turns deoxygenated)</i>'; }
                  if (tg.id === 'lungs') { dot.setAttribute('fill', '#e53950'); extra = ' <i>(picks up O₂ → oxygenated again)</i>'; }
                  setInfo(`<b>${esc(nm(cur, tg.id))}</b>${esc(job(cur, tg.id))}${extra}`);
                }
                if (cur === 'respiratory') dot.setAttribute('fill', tg.back && tg.id !== 'alveoli' ? '#9aa0c0' : '#3b82f6');
              }
              i++;
              if (i >= pts.length) { later(stop, 900); playing = 'end'; return; }
            } else { x += (tg.x - x) / d * v; y += (tg.y - y) / d * v; }
          }
          dot.setAttribute('cx', x.toFixed(1)); dot.setAttribute('cy', y.toFixed(1));
          raf = requestAnimationFrame(step);
        };
        raf = requestAnimationFrame(step);
      }
      function stop() {
        cancelAnimationFrame(raf); playing = null; playB.textContent = '▶ Play path';
        const dot = svg.querySelector('.lb-bodysystem-dot'); if (dot) { dot.style.display = 'none'; dot.setAttribute('fill', SYS[cur].dot); }
      }
      playB.onclick = () => { api.sfx('tap'); if (playing) stop(); else play(); };
      root.querySelectorAll('[data-s]').forEach(b => b.onclick = () => { cur = b.dataset.s; api.sfx('tap'); build(); });
      build();
      return () => { alive = false; cancelAnimationFrame(raf); timers.forEach(clearTimeout); };
    },
    example: { system: 'digestive', systems: ['digestive', 'respiratory', 'circulatory', 'excretory', 'nervous'], goal: 'order' },
    examples: [
      { system: 'respiratory', systems: ['respiratory'], goal: 'order',
        challenge: 'Grade 7: Put the parts of the breathing path in order, from nose to air sacs.' },
      { system: 'nervous', systems: ['nervous'], goal: 'order',
        challenge: 'Grade 10: Touch a hot pan! Put the reflex arc in order: receptor → … → muscle.' },
      { system: 'circulatory', systems: ['circulatory', 'excretory'], goal: 'all',
        challenge: 'Grade 7: Put the organs in order for both the circulatory and excretory systems.' }
    ]
  });
})();
