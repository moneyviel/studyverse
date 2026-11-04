/* 3D lab wrapper around js/scenes.js kind 'solid'. Params are passed to the scene (see scenes.js).
 *
 * PARAMS (all optional)
 *   shape     string  'cube' | 'cuboid' | 'cylinder' | 'cone' | 'sphere' | 'hemisphere' | 'pyramid' | 'prism'
 *                                                                                  default 'cube'
 *   challenge string  challenge line            default 'Turn the shape and press Unfold net'
 *                                               (with `ask`: 'Count the … of the …')
 *   ask       string  optional counting challenge: 'faces' | 'edges' | 'vertices' (also 'corners').
 *                     Shows a − / + stepper under the shape; when it is set to the correct number
 *                     api.win is called. While unsolved, the shape's count label and the spoken
 *                     counts are hidden so they don't give the answer away.         default none
 *   (any other scene params are passed through to scenes.js)
 * Layout: the "Spin the shape" hint is shown under the 3D view (not on top of it), so it never
 * covers the faces / edges / corners label.
 */
(function () {
  // faces, edges, vertices — same numbers as scenes.js S.solid
  const FEV = { cube: [6, 12, 8], cuboid: [6, 12, 8], cylinder: [3, 2, 0], cone: [2, 1, 1], sphere: [1, 0, 0], hemisphere: [2, 1, 0], pyramid: [5, 8, 5], prism: [5, 9, 6] };
  const esc = s => String(s == null ? '' : s).replace(/[<>&"]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;' }[c]));

  Labs.register('solid3d', {
    title: '3D solid', subjects: ['maths', 'science', 'evs', 'geography', 'social'],
    async render(host, p, api) {
      const m = await import('../scenes.js?v=' + (window.LAB_V || 1));
      const shape = String(p.shape || 'cube');
      const askKey = { faces: 0, face: 0, edges: 1, edge: 1, vertices: 2, vertex: 2, corners: 2, corner: 2 }[String(p.ask || '').toLowerCase()];
      const counts = FEV[shape];
      const ask = askKey != null && counts ? askKey : null;
      const askName = ['faces', 'edges', 'vertices'][ask], askShow = ['Faces', 'Edges', 'Vertices (corners)'][ask];
      const answer = ask != null ? counts[ask] : 0;
      const chText = p.challenge || (ask != null ? `Count the ${askName} of the ${shape}. Set the number below.` : 'Turn the shape and press Unfold net');

      host.innerHTML = `<style>
.lb-solid3d .s3d-cap{display:none}
${ask != null ? '.lb-solid3d .s3d{height:290px}' : ''}
.lb-solid3d-cap{font-size:12px;font-weight:800;color:#6b7090;margin:6px 2px 0}
.lb-solid3d-ask{display:flex;align-items:center;gap:8px;margin-top:8px;background:#f6f4ff;border-radius:14px;padding:6px 8px}
.lb-solid3d-ask span{flex:1;font-weight:800;font-size:14px;color:#1b1f3a}
.lb-solid3d-ask button{width:44px;height:44px;border:none;border-radius:12px;font-family:inherit;font-weight:900;font-size:22px;line-height:1;cursor:pointer;background:#eef0fb;color:#1b1f3a}
.lb-solid3d-ask button.plus{background:#8b5cf6;color:#fff}
.lb-solid3d-ask button:active{transform:scale(.94)}
.lb-solid3d-ask output{min-width:44px;text-align:center;font-weight:900;font-size:22px;color:#8b5cf6}
.lb-solid3d-ask.ok{background:#dcfaf0}.lb-solid3d-ask.ok output{color:#0f9b74}
.lb-solid3d-msg{font-size:12.5px;font-weight:700;color:#0f9b74;margin:4px 2px 0;min-height:0}
</style><div class="lb-solid3d"><div class="lb3d-ch">🎯 ${esc(chText)}</div><div class="lb3d"></div><div class="lb-solid3d-cap"></div>${ask != null ? `<div class="lb-solid3d-ask"><span>${askShow}:</span><button data-d="-1" aria-label="one less">−</button><output>0</output><button class="plus" data-d="1" aria-label="one more">+</button></div><div class="lb-solid3d-msg"></div>` : ''}</div>`;
      const box = host.querySelector('.lb3d');
      const ctx = m.mount(box, Object.assign({ kind: 'solid' }, p));
      const capSrc = box.querySelector('.s3d-cap');
      host.querySelector('.lb-solid3d-cap').textContent = capSrc ? capSrc.textContent : '';
      if (ask == null) return () => m.unmount();

      // ---- counting challenge ----
      let n = 0, won = false;
      const out = host.querySelector('output'), row = host.querySelector('.lb-solid3d-ask'), msg = host.querySelector('.lb-solid3d-msg');
      // hide the answer while unsolved: the count label sprite and tap-to-read info on the shape
      const sprites = ctx && ctx.scene ? ctx.scene.children.filter(o => o.isSprite) : [];
      const infos = [];
      if (ctx && ctx.scene) ctx.scene.traverse(o => { if (o.userData && o.userData.info) { infos.push([o, o.userData.info]); delete o.userData.info; } });
      sprites.forEach(s => { s.visible = false; });
      // the Faces / Edges / Corners buttons speak the count — keep them silent until solved
      const wrap = box.querySelector('.s3d-btns');
      let saved = null;
      const mute = () => { if (won || saved) return; saved = { f: window.speak }; window.speak = () => {}; setTimeout(unmute, 0); };
      const unmute = () => { if (saved) { window.speak = saved.f; saved = null; } };
      if (wrap) wrap.addEventListener('click', mute, true);

      function onClick(e) {
        const b = e.target.closest('.lb-solid3d-ask button'); if (!b || won) return;
        const nv = n + +b.dataset.d;
        if (nv < 0 || nv > 30) { api.sfx('hmm'); return; }
        n = nv; out.textContent = n; api.sfx('tap');
        if (n === answer) {
          won = true; row.classList.add('ok');
          sprites.forEach(s => { s.visible = true; });
          infos.forEach(([o, t]) => { o.userData.info = t; });
          const [F, E, V] = counts;
          const m2 = `Yes! A ${shape} has ${answer} ${answer === 1 ? askName.replace(/ices$/, 'ex').replace(/s$/, '') : askName}. (${F} face${F === 1 ? '' : 's'}, ${E} edge${E === 1 ? '' : 's'}, ${V} ${V === 1 ? 'vertex' : 'vertices'}.)`;
          msg.textContent = m2; api.sfx('correct'); api.win(m2);
        }
      }
      host.addEventListener('click', onClick);
      return () => { host.removeEventListener('click', onClick); if (wrap) wrap.removeEventListener('click', mute, true); unmute(); m.unmount(); };
    },
    example: { shape: 'cube' },
    examples: [{ shape: 'cylinder' }, { shape: 'pyramid' }, { shape: 'prism', ask: 'edges' }]
  });
})();
