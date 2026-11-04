/* ================= StudyVerse 3D Concept Studio =================
   Every topic gets a 3D scene the child can spin with a finger or mouse and pinch to zoom.
   Scenes are picked automatically from the topic (or set explicitly with topic.scene).      */
import * as THREE from './vendor/three.module.min.js';
import { OrbitControls } from './vendor/OrbitControls.js';

const COLORS = [0x8b5cf6, 0x2ed3a5, 0xff9f43, 0x3b82f6, 0xff6b6b, 0xffc93c, 0x4dd0e1, 0xba68c8, 0x81c784, 0xf06292];
const say = t => { try { window.speak && window.speak(t); } catch (e) {} };

/* ---------- helpers ---------- */
function label(text, { size = 34, color = '#1b1f3a', bg = 'rgba(255,255,255,.92)', scale = 0.5, maxW = 520, bold = true } = {}) {
  const c = document.createElement('canvas'), x = c.getContext('2d');
  const font = `${bold ? '800' : '600'} ${size}px Nunito, "Noto Sans Devanagari", sans-serif`;
  x.font = font;
  const words = String(text).split(' '); const lines = []; let line = '';
  for (const w of words) { const t = line ? line + ' ' + w : w; if (x.measureText(t).width > maxW && line) { lines.push(line); line = w; } else line = t; }
  lines.push(line);
  const w = Math.min(maxW, Math.max(...lines.map(l => x.measureText(l).width))) + 36, h = lines.length * size * 1.25 + 24;
  c.width = w; c.height = h; x.font = font;
  if (bg) { x.fillStyle = bg; const r = 18; x.beginPath(); x.roundRect(0, 0, w, h, r); x.fill(); }
  x.fillStyle = color; x.textBaseline = 'top';
  lines.forEach((l, i) => x.fillText(l, 18, 12 + i * size * 1.25));
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthTest: false, transparent: true }));
  s.scale.set(w / 66 * scale, h / 66 * scale, 1); s.renderOrder = 10;
  return s;
}
function emojiSprite(e, s = 1.6) {
  const c = document.createElement('canvas'); c.width = c.height = 256; const x = c.getContext('2d');
  x.font = '190px serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(e, 128, 140);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true })); sp.scale.set(s, s, 1); return sp;
}
const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: .55, metalness: .05, ...o });
function info(obj, text) { obj.userData.info = text; obj.traverse(ch => { ch.userData.info = text; }); return obj; }
function line(points, color = 0x1b1f3a, opacity = 1) {
  const g = new THREE.BufferGeometry().setFromPoints(points);
  return new THREE.Line(g, new THREE.LineBasicMaterial({ color, transparent: opacity < 1, opacity }));
}

/* ================= SCENES ================= */
const S = {};

/* ---- Idea Orbit: works for every topic ---- */
S.orbit = (ctx, p) => {
  const { scene } = ctx; const pts = (p.points || []).slice(0, 6);
  const core = new THREE.Mesh(new THREE.SphereGeometry(1.1, 48, 32), mat(0xffc93c, { emissive: 0xff9f00, emissiveIntensity: .35 }));
  scene.add(core); const em = emojiSprite(p.emoji || '💡', 1.7); em.position.set(0, 0, 0); em.renderOrder = 11; em.material.depthTest = false; scene.add(em);
  const ttl = label(p.title || '', { size: 38, scale: .45, bg: 'rgba(139,92,246,.95)', color: '#fff' }); ttl.position.set(0, 1.9, 0); scene.add(ttl);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(3.6, .025, 8, 120), mat(0x8b5cf6, { transparent: true, opacity: .5 })); ring.rotation.x = Math.PI / 2; scene.add(ring);
  const group = new THREE.Group(); scene.add(group);
  pts.forEach((t, i) => {
    const short = t.split(/[.,:;–—(]/)[0].split(' ').slice(0, 6).join(' ') + (t.length > 40 ? '…' : '');
    const a = i / pts.length * Math.PI * 2, card = label(`${i + 1}. ${short}`, { size: 30, scale: .3, maxW: 380, bg: 'rgba(255,255,255,.95)' });
    card.position.set(Math.cos(a) * 3.6, Math.sin(i * 1.7) * .6, Math.sin(a) * 3.6); info(card, t); group.add(card);
    const dot = new THREE.Mesh(new THREE.SphereGeometry(.12, 16, 12), mat(COLORS[i % COLORS.length])); dot.position.copy(card.position).multiplyScalar(.82); group.add(dot);
  });
  ctx.tick = (t) => { group.rotation.y = t * .12; core.rotation.y = t * .5; };
  ctx.camera.position.set(0, 3.6, 10);
  ctx.caption = 'Spin the ideas · tap a card to read and hear it';
};

/* ---- 3D solids with faces / edges / corners and cube net ---- */
S.solid = (ctx, p) => {
  const { scene } = ctx, shape = p.shape || 'cube';
  const G = {
    cube: [new THREE.BoxGeometry(2, 2, 2), 6, 12, 8], cuboid: [new THREE.BoxGeometry(3, 1.6, 2), 6, 12, 8],
    cylinder: [new THREE.CylinderGeometry(1.1, 1.1, 2.4, 48), 3, 2, 0], cone: [new THREE.ConeGeometry(1.3, 2.4, 48), 2, 1, 1],
    sphere: [new THREE.SphereGeometry(1.4, 48, 32), 1, 0, 0], hemisphere: [new THREE.SphereGeometry(1.4, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), 2, 1, 0],
    pyramid: [new THREE.ConeGeometry(1.6, 2.2, 4), 5, 8, 5], prism: [new THREE.CylinderGeometry(1.3, 1.3, 2.4, 3), 5, 9, 6]
  }[shape] || null;
  if (!G) return S.orbit(ctx, p);
  const [geo, F, E, V] = G;
  const solid = new THREE.Group(); scene.add(solid);
  const body = new THREE.Mesh(geo, mat(0x8b5cf6, { transparent: true, opacity: .82, flatShading: shape === 'pyramid' || shape === 'prism' })); solid.add(body);
  if (shape === 'hemisphere') { const cap = new THREE.Mesh(new THREE.CircleGeometry(1.4, 48), mat(0xffc93c, { side: THREE.DoubleSide })); cap.rotation.x = Math.PI / 2; solid.add(cap); }
  const edges = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 25), new THREE.LineBasicMaterial({ color: 0x1b1f3a })); solid.add(edges);
  const corners = new THREE.Group(); solid.add(corners);
  const posAttr = new THREE.EdgesGeometry(geo, 25).attributes.position; const seen = new Set();
  for (let i = 0; i < posAttr.count; i++) { const v = new THREE.Vector3().fromBufferAttribute(posAttr, i); const k = v.toArray().map(n => n.toFixed(2)).join(); if (seen.has(k) || V === 0) continue; seen.add(k); const s = new THREE.Mesh(new THREE.SphereGeometry(.11, 16, 12), mat(0xff6b6b)); s.position.copy(v); corners.add(s); }
  corners.visible = false;
  const nm = shape[0].toUpperCase() + shape.slice(1);
  const lab = label(`${nm}: ${F} face${F > 1 ? 's' : ''} · ${E} edge${E === 1 ? '' : 's'} · ${V} corner${V === 1 ? '' : 's'}`, { size: 30, scale: .5 }); lab.position.set(0, 2.4, 0); scene.add(lab);
  info(body, `A ${shape} has ${F} faces, ${E} edges and ${V} corners.`);
  ctx.buttons = [
    ['Faces', () => { body.material.color.set(body.material.color.getHex() === 0x8b5cf6 ? 0xffc93c : 0x8b5cf6); say(`${F} faces`); }],
    ['Edges', () => { edges.material.color.set(edges.material.color.getHex() === 0x1b1f3a ? 0xff6b6b : 0x1b1f3a); edges.material.linewidth = 3; say(`${E} edges`); }],
    ['Corners', () => { corners.visible = !corners.visible; say(`${V} corners`); }]
  ];
  if (shape === 'cube' || shape === 'cuboid') {
    // net: six faces that fold flat
    const [w, h, d] = shape === 'cube' ? [2, 2, 2] : [3, 1.6, 2];
    const faces = [
      { s: [w, h], f: [0, 0, d / 2, 0, 0, 0], u: [0, 0, 0, 0, 0, 0] },
      { s: [w, h], f: [0, 0, -d / 2, 0, Math.PI, 0], u: [0, h + d, 0, 0, 0, 0] },
      { s: [w, d], f: [0, h / 2, 0, -Math.PI / 2, 0, 0], u: [0, h / 2 + d / 2, 0, 0, 0, 0] },
      { s: [w, d], f: [0, -h / 2, 0, Math.PI / 2, 0, 0], u: [0, -h / 2 - d / 2, 0, 0, 0, 0] },
      { s: [d, h], f: [w / 2, 0, 0, 0, Math.PI / 2, 0], u: [w / 2 + d / 2, 0, 0, 0, 0, 0] },
      { s: [d, h], f: [-w / 2, 0, 0, 0, -Math.PI / 2, 0], u: [-w / 2 - d / 2, 0, 0, 0, 0, 0] }
    ];
    const net = new THREE.Group(); net.visible = false; scene.add(net);
    const panels = faces.map((f, i) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(...f.s), mat(COLORS[i], { side: THREE.DoubleSide })); const e = new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry), new THREE.LineBasicMaterial({ color: 0x1b1f3a })); m.add(e); net.add(m); return { m, f }; });
    let k = 0, target = 0;
    const place = () => panels.forEach(({ m, f }) => { const a = f.f, b = f.u; m.position.set(a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k); m.rotation.set(a[3] * (1 - k), a[4] * (1 - k), a[5] * (1 - k)); });
    place();
    ctx.buttons.push(['Unfold net', () => { net.visible = true; solid.visible = false; target = target ? 0 : 1; say(target ? 'This flat shape is the net. Six faces fold into the box.' : 'Folding back into a ' + shape); }]);
    ctx.tick = () => { if (Math.abs(k - target) > .001) { k += (target - k) * .06; place(); } else if (target === 0 && net.visible && k < .01) { net.visible = false; solid.visible = true; } };
  }
  ctx.camera.position.set(4, 3, 6);
  ctx.caption = 'Spin the shape · try the buttons';
};

/* ---- Earth globe with India, latitudes, tilt ---- */
const LANDS = {
  africa: [[-17, 21], [-10, 30], [10, 37], [32, 31], [43, 12], [51, 12], [40, -10], [35, -25], [20, -35], [12, -17], [9, 4], [-8, 5], [-17, 14]],
  europe: [[-10, 36], [-9, 43], [-2, 48], [5, 52], [10, 58], [5, 62], [15, 69], [30, 70], [40, 66], [50, 47], [40, 45], [28, 41], [20, 40], [15, 38], [10, 44], [3, 43], [-5, 36]],
  asia: [[30, 70], [60, 70], [100, 77], [140, 72], [180, 68], [170, 60], [160, 55], [140, 50], [130, 42], [122, 40], [121, 30], [110, 20], [105, 10], [100, 13], [98, 8], [92, 20], [88, 22], [80, 15], [77, 8], [73, 20], [67, 25], [57, 25], [52, 28], [48, 30], [44, 12], [36, 30], [28, 41], [40, 45], [50, 47], [40, 66]],
  arabia: [[36, 30], [44, 12], [52, 15], [58, 22], [56, 26], [50, 29], [48, 30]],
  namerica: [[-168, 66], [-160, 70], [-130, 70], [-95, 72], [-80, 73], [-62, 60], [-55, 50], [-66, 45], [-75, 35], [-81, 25], [-97, 26], [-97, 18], [-87, 15], [-80, 8], [-90, 14], [-105, 20], [-115, 30], [-124, 40], [-125, 49], [-140, 60], [-165, 60]],
  greenland: [[-50, 60], [-30, 68], [-20, 80], [-40, 83], [-60, 80], [-55, 70]],
  samerica: [[-80, 8], [-62, 10], [-50, 0], [-35, -7], [-40, -22], [-53, -34], [-65, -42], [-68, -55], [-75, -50], [-72, -30], [-70, -18], [-81, -5]],
  australia: [[114, -22], [122, -18], [130, -12], [137, -12], [142, -11], [146, -19], [153, -28], [150, -37], [140, -38], [132, -32], [115, -34]],
  antarctica: [[-180, -70], [-120, -72], [-60, -65], [0, -70], [60, -67], [120, -66], [180, -70], [180, -90], [-180, -90]],
  madagascar: [[44, -16], [50, -15], [50, -25], [45, -25]], uk: [[-5, 50], [1, 51], [-2, 56], [-6, 58], [-5, 54]], japan: [[130, 31], [135, 34], [141, 38], [141, 44], [139, 40], [133, 34]],
  indonesia: [[95, 5], [106, -6], [115, -8], [120, -9], [125, -8], [110, -3], [100, -1]]
};
const INDIA = [[68, 23], [70, 21], [73, 17], [74, 13], [76, 9], [77.5, 8], [80, 10], [80, 15], [83, 18], [87, 21], [89, 22], [92, 22], [92.5, 24], [94, 25], [97, 28], [95, 29], [92, 28], [88, 27.5], [84, 28], [81, 30], [79, 32], [80, 35], [77.8, 35.5], [75, 37], [73.5, 36.5], [74, 34], [72, 31], [71, 28], [69.5, 27], [68.5, 24.5]];
function earthTexture(highlight) {
  const W = 2048, H = 1024, c = document.createElement('canvas'); c.width = W; c.height = H; const x = c.getContext('2d');
  const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#1f6fb2'); g.addColorStop(.5, '#2b8fd6'); g.addColorStop(1, '#1f6fb2'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  const P = ([lo, la]) => [(lo + 180) / 360 * W, (90 - la) / 180 * H];
  const poly = (pts, fill, stroke) => { x.beginPath(); pts.forEach((p, i) => { const [a, b] = P(p); i ? x.lineTo(a, b) : x.moveTo(a, b); }); x.closePath(); x.fillStyle = fill; x.fill(); if (stroke) { x.strokeStyle = stroke; x.lineWidth = 4; x.stroke(); } };
  Object.entries(LANDS).forEach(([k, v]) => poly(v, k === 'antarctica' || k === 'greenland' ? '#eef6ff' : '#7cc576', '#3f8f45'));
  poly(INDIA, highlight ? '#ff9f43' : '#7cc576', highlight ? '#c2410c' : '#3f8f45');
  x.strokeStyle = 'rgba(255,255,255,.25)'; x.lineWidth = 2;
  for (let la = -60; la <= 60; la += 30) { const y = (90 - la) / 180 * H; x.beginPath(); x.moveTo(0, y); x.lineTo(W, y); x.stroke(); }
  for (let lo = -180; lo < 180; lo += 30) { const xx = (lo + 180) / 360 * W; x.beginPath(); x.moveTo(xx, 0); x.lineTo(xx, H); x.stroke(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
const ll = (lon, lat, r) => { const phi = (lon + 180) / 360 * Math.PI * 2, th = (90 - lat) / 180 * Math.PI; return new THREE.Vector3(-r * Math.cos(phi) * Math.sin(th), r * Math.cos(th), r * Math.sin(phi) * Math.sin(th)); };
function makeEarth(r = 2, hl = true) {
  const earth = new THREE.Mesh(new THREE.SphereGeometry(r, 96, 64), new THREE.MeshStandardMaterial({ map: earthTexture(hl), roughness: .8 }));
  return earth;
}
S.globe = (ctx, p) => {
  const { scene } = ctx; const tilt = new THREE.Group(); scene.add(tilt); tilt.rotation.z = p.tilt === false ? 0 : -23.5 * Math.PI / 180;
  const earth = makeEarth(2, true); tilt.add(earth); info(earth, 'The Earth. Land is green, water is blue. India is orange.');
  const ringAt = (lat, color, name) => { const r = 2 * Math.cos(lat * Math.PI / 180), y = 2 * Math.sin(lat * Math.PI / 180); const m = new THREE.Mesh(new THREE.TorusGeometry(r + .01, .015, 6, 160), new THREE.MeshBasicMaterial({ color })); m.rotation.x = Math.PI / 2; m.position.y = y; info(m, name); earth.add(m); };
  ringAt(0, 0xff3b3b, 'The Equator (0°) divides Earth into North and South halves.');
  ringAt(23.5, 0xffd54f, 'Tropic of Cancer (23½° N). It passes through the middle of India.');
  ringAt(-23.5, 0xffd54f, 'Tropic of Capricorn (23½° S).');
  ringAt(66.5, 0x80deea, 'Arctic Circle (66½° N).'); ringAt(-66.5, 0x80deea, 'Antarctic Circle (66½° S).');
  const pm = line(Array.from({ length: 61 }, (_, i) => ll(0, 90 - i * 3, 2.02)), 0xffffff); info(pm, 'Prime Meridian (0°), through Greenwich, London.'); earth.add(pm);
  const pin = new THREE.Mesh(new THREE.ConeGeometry(.09, .35, 12), mat(0xff3b3b)); const pp = ll(78, 22, 2.15); pin.position.copy(pp); pin.lookAt(0, 0, 0); pin.rotateX(-Math.PI / 2); earth.add(pin); info(pin, 'India! About 8° to 37° North and 68° to 97° East.');
  const il = label('India', { size: 30, scale: .4 }); il.position.copy(ll(78, 22, 2.55)); earth.add(il);
  const axis = line([new THREE.Vector3(0, -2.8, 0), new THREE.Vector3(0, 2.8, 0)], 0xffffff, .8); tilt.add(axis); info(axis, 'Earth spins on its tilted axis once a day.');
  ['N', 'S'].forEach((t, i) => { const l = label(t, { size: 36, scale: .35 }); l.position.y = i ? -3 : 3; tilt.add(l); });
  earth.rotation.y = -1.6;
  ctx.tick = (t, dt) => { if (!ctx.paused) earth.rotation.y += dt * .15; };
  ctx.light.position.set(5, 1, 4);
  ctx.buttons = [['Pause spin', b => { ctx.paused = !ctx.paused; b.textContent = ctx.paused ? 'Spin' : 'Pause spin'; }], ['Find India', () => { earth.rotation.y = -1.6; ctx.paused = true; say('India is in the northern half of the Earth, north of the equator.'); }]];
  ctx.camera.position.set(0, 1.5, 6.5); ctx.caption = 'Spin the Earth · tap the lines to learn them';
};

/* ---- Earth's inside layers ---- */
S.earthlayers = (ctx) => {
  const scene = new THREE.Group(); ctx.scene.add(scene); scene.rotation.y = Math.PI * 1.25; const L = [[2.4, 0x8d6e63, 'Crust: the thin rocky outer skin we live on.'], [2.25, 0xff7043, 'Mantle: very hot, slowly moving rock.'], [1.25, 0xffa726, 'Outer core: liquid iron and nickel.'], [.65, 0xffee58, 'Inner core: solid iron and nickel, the hottest part.']];
  L.forEach(([r, c, t], i) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 64, 48, 0, Math.PI * 1.5), mat(c, { side: THREE.DoubleSide })); info(m, t); scene.add(m);
    const cap = new THREE.Mesh(new THREE.CircleGeometry(r, 64, Math.PI / 2, Math.PI / 2), mat(c, { side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: -i * 2, polygonOffsetUnits: -i * 2 })); cap.rotation.y = 0; info(cap, t); scene.add(cap);
    const cap2 = cap.clone(); cap2.rotation.y = -Math.PI / 2; scene.add(cap2);
    const lb = label(t.split(':')[0], { size: 30, scale: .4 }); lb.position.set(r - .25, .3 + i * .05, .9 - i * .2); scene.add(lb); });
  const land = new THREE.Mesh(new THREE.SphereGeometry(2.42, 64, 48, 0, Math.PI * 1.5), new THREE.MeshStandardMaterial({ map: earthTexture(false), side: THREE.FrontSide })); scene.add(land);
  ctx.camera.position.set(4.5, 3, 4.5); ctx.caption = 'Look inside the Earth · tap each layer';
};

/* ---- Solar system ---- */
S.solar = (ctx) => {
  const { scene } = ctx; ctx.light.intensity = .3;
  const sun = new THREE.Mesh(new THREE.SphereGeometry(1, 48, 32), new THREE.MeshBasicMaterial({ color: 0xffc93c })); scene.add(sun); info(sun, 'The Sun is a star. It gives light and heat to all planets.');
  const pl = new THREE.PointLight(0xffffff, 60, 0, 1.4); scene.add(pl);
  const P = [['Mercury', .18, 1.8, 0xb0a99f, 'Closest to the Sun and the smallest planet.'], ['Venus', .28, 2.5, 0xe8c27a, 'The hottest planet; brightest in our night sky.'], ['Earth', .3, 3.3, 0x3b82f6, 'Our home, the only planet known to have life.'], ['Mars', .22, 4.1, 0xd9603b, 'The red planet.'],
    ['Jupiter', .62, 5.4, 0xd8b48a, 'The biggest planet.'], ['Saturn', .52, 6.8, 0xe9d38f, 'Famous for its bright rings.'], ['Uranus', .4, 8.0, 0x8fd6e0, 'Spins tipped over on its side.'], ['Neptune', .38, 9.1, 0x4f6fe0, 'Farthest planet from the Sun.']];
  const ps = P.map(([n, r, d, c, t], i) => { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 32, 24), mat(c)); info(m, `${n}: ${t}`); const g = new THREE.Group(); g.add(m); m.position.x = d; scene.add(g);
    if (n === 'Saturn') { const ring = new THREE.Mesh(new THREE.RingGeometry(r * 1.3, r * 2, 48), mat(0xe9d38f, { side: THREE.DoubleSide, transparent: true, opacity: .8 })); ring.rotation.x = 1.2; m.add(ring); }
    const orb = new THREE.Mesh(new THREE.RingGeometry(d - .01, d + .01, 128), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .25, side: THREE.DoubleSide })); orb.rotation.x = Math.PI / 2; scene.add(orb);
    const lb = label(n, { size: 26, scale: .32 }); lb.position.set(0, r + .3, 0); m.add(lb);
    g.rotation.y = i * 1.3; return [g, 1 / Math.pow(d, 1.5)]; });
  ctx.tick = (t, dt) => ps.forEach(([g, s]) => g.rotation.y += dt * s * 2.2);
  ctx.camera.position.set(0, 9, 12); ctx.caption = 'Tap a planet to learn about it (sizes not to scale)';
};

/* ---- Sun, Earth and Moon: day/night and phases ---- */
S.moon = (ctx) => {
  const { scene } = ctx; ctx.light.position.set(-10, 0, 0); ctx.light.intensity = 3; ctx.ambient.intensity = .12;
  const sun = new THREE.Mesh(new THREE.SphereGeometry(.9, 32, 24), new THREE.MeshBasicMaterial({ color: 0xffc93c })); sun.position.set(-7, 0, 0); scene.add(sun); info(sun, 'Sunlight always lights up half of the Earth and half of the Moon.');
  const earth = makeEarth(1, true); scene.add(earth); info(earth, 'The lit half of Earth has day; the dark half has night.');
  const moonG = new THREE.Group(); scene.add(moonG); const moon = new THREE.Mesh(new THREE.SphereGeometry(.3, 32, 24), mat(0xdddddd)); moon.position.x = 3; moonG.add(moon); info(moon, 'The Moon goes around the Earth in about 29½ days.');
  const orb = new THREE.Mesh(new THREE.RingGeometry(2.99, 3.01, 128), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .3, side: THREE.DoubleSide })); orb.rotation.x = Math.PI / 2; scene.add(orb);
  const phaseLbl = label('', { size: 30, scale: .45 }); phaseLbl.position.set(0, 2.2, 0); scene.add(phaseLbl);
  const names = ['Full moon', 'Waning gibbous', 'Last quarter', 'Waning crescent', 'New moon', 'Waxing crescent', 'First quarter', 'Waxing gibbous'];
  let last = '';
  ctx.tick = (t, dt) => { earth.rotation.y += dt * .6; moonG.rotation.y += dt * .12;
    const a = ((moonG.rotation.y % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2); const nm = names[Math.round(a / (Math.PI / 4)) % 8];
    if (nm !== last) { last = nm; scene.remove(phaseLbl.__l || phaseLbl); const l = label('From Earth we see: ' + nm, { size: 30, scale: .45 }); l.position.set(0, 2.2, 0); scene.add(l); phaseLbl.__l = l; } };
  ctx.camera.position.set(0, 6, 8); ctx.caption = 'Watch the Moon go round · its lit side makes the phases';
};

/* ---- Atom (Bohr model, school rule 2, 8, 8, 2) ---- */
const ELEMENTS = ['', 'Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', 'Carbon', 'Nitrogen', 'Oxygen', 'Fluorine', 'Neon', 'Sodium', 'Magnesium', 'Aluminium', 'Silicon', 'Phosphorus', 'Sulphur', 'Chlorine', 'Argon', 'Potassium', 'Calcium'];
const SYM = ['', 'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca'];
S.atom = (ctx, p) => {
  const { scene } = ctx; let Z = Math.max(1, Math.min(20, p.z || 6));
  const root = new THREE.Group(); scene.add(root); let anim = [];
  const build = () => {
    root.clear(); anim = [];
    const shells = []; let left = Z; for (const cap of [2, 8, 8, 2]) { if (left <= 0) break; shells.push(Math.min(cap, left)); left -= cap; }
    const nuc = new THREE.Group(); root.add(nuc); const N = Math.round(Z * 1.05);
    for (let i = 0; i < Z + N; i++) { const s = new THREE.Mesh(new THREE.SphereGeometry(.16, 16, 12), mat(i < Z ? 0xff6b6b : 0x9e9e9e)); const r = .12 * Math.cbrt(Z + N) * 1.6; s.position.set((Math.random() - .5) * r, (Math.random() - .5) * r, (Math.random() - .5) * r); nuc.add(s); }
    info(nuc, `Nucleus: ${Z} protons (red) and neutrons (grey).`);
    shells.forEach((n, si) => { const R = 1.3 + si * .9; const g = new THREE.Group(); g.rotation.x = .4 * si; g.rotation.z = .3 * si; root.add(g);
      const ring = new THREE.Mesh(new THREE.TorusGeometry(R, .02, 8, 120), new THREE.MeshBasicMaterial({ color: 0x8b5cf6 })); ring.rotation.x = Math.PI / 2; g.add(ring); info(ring, `Shell ${'KLMN'[si]} holds ${n} electron${n > 1 ? 's' : ''}.`);
      for (let e = 0; e < n; e++) { const el = new THREE.Mesh(new THREE.SphereGeometry(.12, 16, 12), mat(0x3b82f6, { emissive: 0x1e40af, emissiveIntensity: .6 })); const a = e / n * Math.PI * 2; el.position.set(Math.cos(a) * R, 0, Math.sin(a) * R); g.add(el); info(el, 'Electron: tiny, negatively charged, moving around the nucleus.'); }
      anim.push([g, .6 / (si + 1)]); });
    const lb = label(`${ELEMENTS[Z]} (${SYM[Z]}) · ${Z} electrons: ${shells.join(', ')}`, { size: 30, scale: .5 }); lb.position.set(0, 3.4, 0); root.add(lb);
  };
  build();
  ctx.tick = (t, dt) => anim.forEach(([g, s]) => g.rotation.y += dt * s);
  ctx.buttons = [['◀ Element', () => { Z = Z > 1 ? Z - 1 : 20; build(); say(ELEMENTS[Z]); }], ['Element ▶', () => { Z = Z < 20 ? Z + 1 : 1; build(); say(ELEMENTS[Z]); }]];
  ctx.camera.position.set(0, 2.5, 10.5); ctx.caption = 'Change the element · tap the shells';
};

/* ---- Molecules (ball and stick) ---- */
const CPK = { H: 0xffffff, O: 0xff3b3b, C: 0x333333, N: 0x3b5bff, Cl: 0x2ecc40, Na: 0xab5cf2 };
const MOLS = {
  water: { name: 'Water (H₂O)', atoms: [['O', 0, 0, 0], ['H', .95, .6, 0], ['H', -.95, .6, 0]], bonds: [[0, 1], [0, 2]] },
  co2: { name: 'Carbon dioxide (CO₂)', atoms: [['C', 0, 0, 0], ['O', 1.3, 0, 0], ['O', -1.3, 0, 0]], bonds: [[0, 1, 2], [0, 2, 2]] },
  oxygen: { name: 'Oxygen (O₂)', atoms: [['O', .6, 0, 0], ['O', -.6, 0, 0]], bonds: [[0, 1, 2]] },
  methane: { name: 'Methane (CH₄)', atoms: [['C', 0, 0, 0], ['H', .9, .9, .9], ['H', -.9, -.9, .9], ['H', -.9, .9, -.9], ['H', .9, -.9, -.9]], bonds: [[0, 1], [0, 2], [0, 3], [0, 4]] },
  ammonia: { name: 'Ammonia (NH₃)', atoms: [['N', 0, .3, 0], ['H', 1, -.2, 0], ['H', -.5, -.2, .87], ['H', -.5, -.2, -.87]], bonds: [[0, 1], [0, 2], [0, 3]] },
  hydrogen: { name: 'Hydrogen (H₂)', atoms: [['H', .4, 0, 0], ['H', -.4, 0, 0]], bonds: [[0, 1]] }
};
S.molecule = (ctx, p) => {
  const { scene } = ctx; const keys = Object.keys(MOLS); let k = keys.indexOf(p.name) >= 0 ? keys.indexOf(p.name) : 0; const root = new THREE.Group(); scene.add(root);
  const build = () => { root.clear(); const M = MOLS[keys[k]]; const pos = M.atoms.map(a => new THREE.Vector3(a[1], a[2], a[3]).multiplyScalar(1.4));
    M.atoms.forEach((a, i) => { const s = new THREE.Mesh(new THREE.SphereGeometry(a[0] === 'H' ? .32 : .5, 32, 24), mat(CPK[a[0]])); s.position.copy(pos[i]); info(s, `${a[0]} atom`); root.add(s); const l = label(a[0], { size: 30, scale: .3, bg: null }); l.position.copy(pos[i]); root.add(l); });
    M.bonds.forEach(([i, j, n = 1]) => { for (let b = 0; b < n; b++) { const A = pos[i], B = pos[j], mid = A.clone().add(B).multiplyScalar(.5), len = A.distanceTo(B); const c = new THREE.Mesh(new THREE.CylinderGeometry(.07, .07, len, 12), mat(0xbdbdbd)); c.position.copy(mid); c.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), B.clone().sub(A).normalize()); if (n > 1) c.position.add(new THREE.Vector3(0, (b - .5) * .22, 0)); root.add(c); } });
    const t = label(M.name, { size: 32, scale: .5 }); t.position.set(0, 2.1, 0); root.add(t); };
  build(); ctx.buttons = [['Next molecule ▶', () => { k = (k + 1) % keys.length; build(); say(MOLS[keys[k]].name); }]];
  ctx.camera.position.set(0, 1, 7.5); ctx.caption = 'Spin the molecule · each ball is an atom';
};

/* ---- Place-value blocks ---- */
S.blocks = (ctx, p) => {
  const { scene } = ctx; let n = Math.max(1, Math.min(999, p.n || 234)); const root = new THREE.Group(); scene.add(root); const u = .22;
  const cube = (x, y, z, c) => { const m = new THREE.Mesh(new THREE.BoxGeometry(u * .96, u * .96, u * .96), mat(c)); m.position.set(x, y, z); return m; };
  const build = () => { root.clear(); const H = Math.floor(n / 100), T = Math.floor(n / 10) % 10, O = n % 10; let x = -3.2;
    for (let h = 0; h < H; h++) { const g = new THREE.Group(); for (let i = 0; i < 10; i++) for (let j = 0; j < 10; j++) g.add(cube(i * u, j * u, 0, 0xff9f43)); g.position.set(x, 0, -h * .35); info(g, 'One hundred = 10 tens = 100 ones'); root.add(g); }
    if (H) x += 10 * u + .4; for (let t = 0; t < T; t++) { const g = new THREE.Group(); for (let j = 0; j < 10; j++) g.add(cube(0, j * u, 0, 0x3b82f6)); g.position.set(x + t * (u + .08), 0, 0); info(g, 'One ten = 10 ones'); root.add(g); }
    if (T) x += T * (u + .08) + .4; for (let o = 0; o < O; o++) { const c = cube(x + (o % 3) * (u + .05), Math.floor(o / 3) * (u + .05), 0, 0x2ed3a5); info(c, 'One'); root.add(c); }
    root.position.x = -x / 2 + 1.2;
    const l = label(`${n} = ${H} hundred${H !== 1 ? 's' : ''} + ${T} ten${T !== 1 ? 's' : ''} + ${O} one${O !== 1 ? 's' : ''}`, { size: 30, scale: .5 }); l.position.set(-root.position.x + .3, 2.75, 0); root.add(l); };
  build(); ctx.buttons = [['−10', () => { n = Math.max(1, n - 10); build(); say(String(n)); }], ['+1', () => { n = Math.min(999, n + 1); build(); say(String(n)); }], ['+10', () => { n = Math.min(999, n + 10); build(); say(String(n)); }], ['+100', () => { n = Math.min(999, n + 100); build(); say(String(n)); }]];
  ctx.camera.position.set(0, 1.5, 8.5); ctx.caption = 'Build numbers with blocks · try the buttons';
};

/* ---- Fraction pie: tap slices to colour them ---- */
S.fraction = (ctx, p) => {
  const { scene } = ctx; let den = Math.max(2, Math.min(12, p.den || 4)); let on = new Set([...Array(Math.min(p.num ?? 1, den)).keys()]); const root = new THREE.Group(); scene.add(root);
  let lbl;
  const build = () => { root.clear(); const step = Math.PI * 2 / den;
    for (let i = 0; i < den; i++) { const m = new THREE.Mesh(new THREE.CylinderGeometry(2, 2, .5, 48, 1, false, i * step + .01, step - .02), mat(on.has(i) ? 0x8b5cf6 : 0xeeeeee)); if (on.has(i)) m.position.y = .15; m.userData.slice = i; info(m, `1 of ${den} equal parts`); root.add(m); }
    lbl = label(`${on.size}/${den} coloured`, { size: 34, scale: .55 }); lbl.position.set(0, 1.6, 0); root.add(lbl); };
  build();
  ctx.onPick = o => { if (o.userData.slice === undefined) return false; const i = o.userData.slice; on.has(i) ? on.delete(i) : on.add(i); build(); say(`${on.size} out of ${den}`); return true; };
  ctx.buttons = [['Fewer parts', () => { den = Math.max(2, den - 1); on = new Set([...on].filter(i => i < den)); build(); }], ['More parts', () => { den = Math.min(12, den + 1); build(); }]];
  ctx.camera.position.set(0, 4.5, 5); ctx.caption = 'Tap slices to colour them · watch the fraction change';
};

/* ---- Bar magnet with field lines ---- */
S.magnet = (ctx) => {
  const { scene } = ctx;
  const n = new THREE.Mesh(new THREE.BoxGeometry(1.6, .6, .6), mat(0xff3b3b)); n.position.x = .8; const s = new THREE.Mesh(new THREE.BoxGeometry(1.6, .6, .6), mat(0x3b82f6)); s.position.x = -.8; scene.add(n, s);
  info(n, 'North pole (N). Field lines come out of the north pole.'); info(s, 'South pole (S). Field lines go into the south pole.');
  const ln = label('N', { size: 40, scale: .4, bg: null, color: '#fff' }); ln.position.set(1.2, 0, .32); const ls = label('S', { size: 40, scale: .4, bg: null, color: '#fff' }); ls.position.set(-1.2, 0, .32); scene.add(ln, ls);
  const parts = [];
  for (let plane = 0; plane < 4; plane++) for (const k of [1.6, 2.4, 3.4, 4.6]) {
    const pts = []; for (let i = 0; i <= 80; i++) { const th = .25 + i / 80 * (Math.PI - .5), r = k * Math.sin(th) ** 2; pts.push(new THREE.Vector3(r * Math.cos(th), r * Math.sin(th), 0)); }
    const curve = new THREE.CatmullRomCurve3(pts); const l = line(curve.getPoints(80), 0x8b5cf6, .6); l.rotation.x = plane * Math.PI / 2; scene.add(l);
    const dot = new THREE.Mesh(new THREE.SphereGeometry(.06, 8, 6), new THREE.MeshBasicMaterial({ color: 0xffc93c })); scene.add(dot); parts.push([curve, dot, plane, Math.random()]);
  }
  ctx.tick = (t) => parts.forEach(([c, d, pl, off]) => { const u = 1 - ((t * .15 + off) % 1); const pnt = c.getPoint(u); pnt.applyAxisAngle(new THREE.Vector3(1, 0, 0), pl * Math.PI / 2); d.position.copy(pnt); });
  ctx.camera.position.set(0, 3, 9); ctx.caption = 'Field lines go from N to S outside the magnet';
};

/* ---- Cells ---- */
S.cell = (ctx, p) => {
  const { scene } = ctx; const plant = p.type !== 'animal'; const root = new THREE.Group(); scene.add(root);
  const add = (geo, c, pos, t, o = {}) => { const m = new THREE.Mesh(geo, mat(c, o)); m.position.set(...pos); info(m, t); root.add(m); return m; };
  if (plant) {
    add(new THREE.BoxGeometry(4.4, 3, 2.4), 0x2e7d32, [0, 0, 0], 'Cell wall: a stiff outer wall that gives the plant cell its shape.', { transparent: true, opacity: .18 });
    add(new THREE.BoxGeometry(4.2, 2.8, 2.2), 0x81c784, [0, 0, 0], 'Cell membrane: a thin layer that controls what goes in and out.', { transparent: true, opacity: .2 });
    add(new THREE.SphereGeometry(1, 32, 24), 0xb3e5fc, [.5, 0, 0], 'Vacuole: a big sac that stores water and keeps the cell firm.', { transparent: true, opacity: .7 }).scale.set(1.4, 1, .8);
    for (let i = 0; i < 7; i++) add(new THREE.CapsuleGeometry(.12, .25, 6, 12), 0x1b8f3a, [-1.7 + i * .55, (i % 2 ? .9 : -.9), (i % 3 - 1) * .5], 'Chloroplast: makes food using sunlight (photosynthesis).');
  } else {
    add(new THREE.SphereGeometry(2, 48, 32), 0xffcdd2, [0, 0, 0], 'Cell membrane: a thin, flexible outer layer. Animal cells have no cell wall.', { transparent: true, opacity: .25 });
    for (let i = 0; i < 5; i++) add(new THREE.CapsuleGeometry(.14, .35, 6, 12), 0xff7043, [Math.cos(i * 1.3) * 1.2, Math.sin(i * 1.7) * .8, Math.sin(i) * .7], 'Mitochondrion: the powerhouse that releases energy from food.');
  }
  add(new THREE.SphereGeometry(.6, 32, 24), 0x7e57c2, plant ? [-1.2, .2, .3] : [0, 0, 0], 'Nucleus: the control centre. It holds the genetic material.');
  for (let i = 0; i < 4; i++) add(new THREE.SphereGeometry(.08, 12, 8), 0x5d4037, [Math.cos(i * 2) * .9, -.6 + i * .3, .6], 'Ribosome: makes proteins.');
  const l = label(plant ? 'Plant cell' : 'Animal cell', { size: 34, scale: .5 }); l.position.set(0, 2.2, 0); root.add(l);
  ctx.buttons = [[plant ? 'Show animal cell' : 'Show plant cell', () => ctx.remount({ kind: 'cell', type: plant ? 'animal' : 'plant' })]];
  ctx.camera.position.set(0, 2, 8); ctx.caption = 'Tap each part of the cell to learn its job';
};

/* ---- Water cycle ---- */
S.watercycle = (ctx) => {
  const { scene } = ctx;
  const sea = new THREE.Mesh(new THREE.BoxGeometry(4, .2, 4), mat(0x2b8fd6)); sea.position.set(-2, -1, 0); scene.add(sea); info(sea, 'Collection: water gathers in seas, rivers and lakes.');
  const land = new THREE.Mesh(new THREE.BoxGeometry(4, .4, 4), mat(0x7cc576)); land.position.set(2, -.9, 0); scene.add(land);
  const mtn = new THREE.Mesh(new THREE.ConeGeometry(1.4, 2.4, 6), mat(0x8d6e63, { flatShading: true })); mtn.position.set(2.5, .5, -.5); scene.add(mtn);
  const snow = new THREE.Mesh(new THREE.ConeGeometry(.5, .8, 6), mat(0xffffff, { flatShading: true })); snow.position.set(2.5, 1.35, -.5); scene.add(snow);
  const river = line([new THREE.Vector3(2.3, -.65, .5), new THREE.Vector3(1, -.66, .8), new THREE.Vector3(-.2, -.8, .5)], 0x2b8fd6); scene.add(river);
  const sun = new THREE.Mesh(new THREE.SphereGeometry(.5, 32, 24), new THREE.MeshBasicMaterial({ color: 0xffc93c })); sun.position.set(-3.5, 3, -1); scene.add(sun); info(sun, 'The Sun heats the water so it evaporates.');
  const cloud = new THREE.Group(); [[0, 0], [.5, .15], [-.5, .1], [.25, -.15], [-.25, .25]].forEach(([x, y]) => { const c = new THREE.Mesh(new THREE.SphereGeometry(.55, 24, 16), mat(0xf5f5f5)); c.position.set(x, y, 0); cloud.add(c); });
  cloud.position.set(.8, 2.6, 0); scene.add(cloud); info(cloud, 'Condensation: water vapour cools and forms tiny drops that make clouds.');
  const vap = [], rain = [];
  for (let i = 0; i < 30; i++) { const v = new THREE.Mesh(new THREE.SphereGeometry(.04, 8, 6), new THREE.MeshBasicMaterial({ color: 0xbbdefb })); v.userData.o = Math.random(); scene.add(v); vap.push(v); }
  for (let i = 0; i < 40; i++) { const r = new THREE.Mesh(new THREE.CylinderGeometry(.015, .015, .18, 6), new THREE.MeshBasicMaterial({ color: 0x64b5f6 })); r.userData.o = Math.random(); scene.add(r); rain.push(r); }
  [['Evaporation', -2, 1.2], ['Condensation', .8, 3.5], ['Precipitation', 1.9, 1.3], ['Collection', -2, -.4]].forEach(([t, x, y]) => { const l = label(t, { size: 28, scale: .38 }); l.position.set(x, y, 1.2); info(l, t); scene.add(l); });
  ctx.tick = (t) => { vap.forEach((v, i) => { const u = (t * .25 + v.userData.o) % 1; v.position.set(-3 + (i % 6) * .4, -.8 + u * 3, (i % 5) * .4 - .8); v.material.opacity = 1 - u; v.material.transparent = true; });
    rain.forEach((r, i) => { const u = (t * .8 + r.userData.o) % 1; r.position.set(.2 + (i % 8) * .22, 2.2 - u * 2.8, (i % 5) * .3 - .6); }); };
  ctx.camera.position.set(0, 2.5, 8); ctx.caption = 'Watch water travel in a never-ending cycle';
};

/* ---- Parts of a plant ---- */
S.plant = (ctx) => {
  const { scene } = ctx;
  const soil = new THREE.Mesh(new THREE.CylinderGeometry(2.4, 2.4, .2, 48), mat(0x8d6e63)); soil.position.y = -1.5; scene.add(soil);
  const stem = new THREE.Mesh(new THREE.CylinderGeometry(.08, .12, 3, 12), mat(0x4caf50)); stem.position.y = 0; scene.add(stem); info(stem, 'Stem: holds the plant up and carries water and food.');
  for (let i = 0; i < 4; i++) { const lf = new THREE.Mesh(new THREE.SphereGeometry(.5, 24, 12), mat(0x43a047)); lf.scale.set(1, .15, .45); lf.position.set(i % 2 ? .5 : -.5, -.6 + i * .5, 0); lf.rotation.z = i % 2 ? -.4 : .4; scene.add(lf); info(lf, 'Leaf: makes food for the plant using sunlight, air and water.'); }
  const fl = new THREE.Group(); fl.position.y = 1.6; scene.add(fl);
  for (let i = 0; i < 6; i++) { const pt = new THREE.Mesh(new THREE.SphereGeometry(.3, 16, 12), mat(0xf06292)); pt.scale.set(1, .3, .5); const a = i / 6 * Math.PI * 2; pt.position.set(Math.cos(a) * .35, 0, Math.sin(a) * .35); pt.rotation.y = -a; fl.add(pt); }
  const ctr = new THREE.Mesh(new THREE.SphereGeometry(.15, 16, 12), mat(0xffc93c)); fl.add(ctr); info(fl, 'Flower: makes seeds so new plants can grow.');
  for (let i = 0; i < 7; i++) { const a = i / 7 * Math.PI * 2; const r = line([new THREE.Vector3(0, -1.5, 0), new THREE.Vector3(Math.cos(a) * .4, -2.1, Math.sin(a) * .4), new THREE.Vector3(Math.cos(a) * .7, -2.6, Math.sin(a) * .7)], 0xd7b98e); scene.add(r); }
  const rootHit = new THREE.Mesh(new THREE.SphereGeometry(.6, 8, 6), new THREE.MeshBasicMaterial({ visible: false })); rootHit.position.y = -2.1; info(rootHit, 'Roots: hold the plant in the soil and take in water and minerals.'); scene.add(rootHit);
  [['Flower', 1.2, 1.8], ['Leaf', -1.3, 0], ['Stem', .7, .4], ['Roots', 1.2, -2.2]].forEach(([t, x, y]) => { const l = label(t, { size: 28, scale: .36 }); l.position.set(x, y, .3); scene.add(l); });
  ctx.camera.position.set(0, .5, 6.5); ctx.caption = 'Tap each part of the plant';
};

/* ---- 3D timeline for history ---- */
S.timeline = (ctx, p) => {
  const { scene } = ctx; const ev = (p.events || []).slice(0, 8); if (ev.length < 2) return S.orbit(ctx, p);
  const ys = ev.map(e => e[0]), lo = Math.min(...ys), hi = Math.max(...ys);
  const pts = []; ev.forEach((e, i) => { const a = i / ev.length * Math.PI * 1.6 - Math.PI * .8, y = hi === lo ? 0 : (e[0] - lo) / (hi - lo) * 3 - 1.5; const v = new THREE.Vector3(Math.sin(a) * 3, y, Math.cos(a) * 3); pts.push(v);
    const pil = new THREE.Mesh(new THREE.CylinderGeometry(.12, .12, .5, 12), mat(COLORS[i % COLORS.length])); pil.position.copy(v); info(pil, `${e[0] < 0 ? -e[0] + ' BCE' : e[0]}: ${e[1]}`); scene.add(pil);
    const l = label(`${e[0] < 0 ? -e[0] + ' BCE' : e[0]} · ${e[1]}`, { size: 26, scale: .34, maxW: 420 }); l.position.copy(v).add(new THREE.Vector3(0, .55, 0)); scene.add(l); });
  scene.add(line(new THREE.CatmullRomCurve3(pts).getPoints(100), 0x8b5cf6));
  ctx.camera.position.set(0, 2.5, 8); ctx.caption = 'Spin through time · tap an event';
};

/* ---- Word blocks for early language ---- */
S.word = (ctx, p) => {
  const { scene } = ctx; const w = Array.from(p.word || 'cat').slice(0, 8); const g = new THREE.Group(); scene.add(g);
  w.forEach((ch, i) => { const c = document.createElement('canvas'); c.width = c.height = 256; const x = c.getContext('2d'); x.fillStyle = '#' + COLORS[i % COLORS.length].toString(16).padStart(6, '0'); x.fillRect(0, 0, 256, 256); x.fillStyle = '#fff'; x.font = '800 170px Nunito, "Noto Sans Devanagari", sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(ch, 128, 140);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; const m = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshStandardMaterial({ map: t })); m.position.x = (i - (w.length - 1) / 2) * 1.15; info(m, ch); m.userData.say = ch; g.add(m); });
  ctx.onPick = o => { if (o.userData.say) { say(o.userData.say); o.rotation.y += Math.PI / 2; return true; } return false; };
  ctx.buttons = [['🔊 Say the word', () => say(p.word)]];
  ctx.camera.position.set(0, 1.5, Math.max(5, w.length * 1.3)); ctx.caption = 'Tap a block to hear it · spin the word';
};

/* ================= picking a scene for any topic ================= */
export function pickScene(topic, subject, grade, chapter) {
  if (topic.scene) return topic.scene;
  const txt = [topic.title, chapter?.title, ...(topic.learn?.points || []), topic.learn?.hook].join(' ').toLowerCase();
  const has = (...w) => w.some(x => txt.includes(x));
  const base = { title: topic.title, emoji: chapter?.emoji || '💡', points: topic.learn?.points || [] };
  if (subject === 'maths') {
    if (has('fraction', 'half', 'quarter', 'numerator')) return { kind: 'fraction', num: 1, den: has('quarter') ? 4 : has('third') ? 3 : 2 };
    if (has('place value', 'hundreds', 'tens and ones', 'tens', 'thousand') && grade <= 5) return { kind: 'blocks', n: grade <= 2 ? 34 : 345 };
    for (const s of ['cuboid', 'cube', 'cylinder', 'cone', 'sphere', 'hemisphere', 'pyramid', 'prism']) if (has(s)) return { kind: 'solid', shape: s };
    if (has('3d shape', 'solid', 'faces', 'edges', 'vertices', 'net of')) return { kind: 'solid', shape: 'cube' };
  }
  if (['science', 'evs', 'geography', 'social'].includes(subject)) {
    if (has('atom', 'electron', 'proton', 'valency', 'shell')) return { kind: 'atom', z: has('sodium') ? 11 : has('oxygen') ? 8 : has('carbon') ? 6 : 6 };
    if (has('molecule', 'h2o', 'h₂o', 'carbon dioxide', 'methane', 'ammonia')) return { kind: 'molecule', name: has('carbon dioxide') ? 'co2' : has('methane') ? 'methane' : has('ammonia') ? 'ammonia' : 'water' };
    if (has('magnet', 'magnetic')) return { kind: 'magnet' };
    if (has(' cell', 'cells', 'nucleus', 'chloroplast', 'mitochondri')) return { kind: 'cell', type: has('animal cell') ? 'animal' : 'plant' };
    if (has('water cycle', 'evaporation', 'condensation', 'precipitation')) return { kind: 'watercycle' };
    if (has('crust', 'mantle', 'core', 'layers of the earth', 'interior of the earth')) return { kind: 'earthlayers' };
    if (has('moon', 'phases', 'eclipse', 'day and night')) return { kind: 'moon' };
    if (has('planet', 'solar system', 'jupiter', 'mars')) return { kind: 'solar' };
    if (has('globe', 'latitude', 'longitude', 'equator', 'continent', 'meridian', 'hemisphere', 'tropic', 'earth', 'map', 'ocean')) return { kind: 'globe' };
    if (has('root', 'stem', 'leaf', 'leaves', 'flower', 'parts of a plant', 'photosynthesis')) return { kind: 'plant' };
  }
  if (['history', 'social', 'civics'].includes(subject)) {
    const all = [topic.title, ...(topic.learn?.points || []), ...(topic.quiz || []).map(q => q.q + ' ' + q.explain)].join(' . ');
    const ev = []; const seen = new Set();
    for (const s of all.split(/(?<=[.!?])\s+/)) { const m = s.match(/\b(1[0-9]{3}|20[0-2][0-9])\b/); if (m && !seen.has(m[1]) && s.length < 160) { seen.add(m[1]); ev.push([+m[1], s.replace(/\s+/g, ' ').slice(0, 70)]); } }
    if (ev.length >= 3) return { kind: 'timeline', events: ev.sort((a, b) => a[0] - b[0]).slice(0, 7), ...base };
  }
  if (['english', 'hindi'].includes(subject) && grade <= 3) {
    const pair = (topic.games || []).find(g => g.type === 'match')?.pairs?.[0]?.[0];
    if (pair && Array.from(pair).length <= 7 && !/\s/.test(pair)) return { kind: 'word', word: pair };
  }
  return { kind: 'orbit', ...base };
}

/* ================= mounting ================= */
let active = null;
export function mount(host, spec) {
  unmount();
  host.innerHTML = `<div class="s3d"><canvas></canvas><div class="s3d-cap"></div><div class="s3d-info"></div><div class="s3d-btns"></div><button class="s3d-full" title="Full screen">⤢</button></div>`;
  const wrap = host.querySelector('.s3d'), canvas = wrap.querySelector('canvas');
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true }); renderer.setPixelRatio(Math.min(2, devicePixelRatio));
  const scene = new THREE.Scene(); const camera = new THREE.PerspectiveCamera(45, 1, .1, 200);
  const ambient = new THREE.AmbientLight(0xffffff, .75); const light = new THREE.DirectionalLight(0xffffff, 1.6); light.position.set(5, 8, 6); scene.add(ambient, light);
  const controls = new OrbitControls(camera, canvas); controls.enableDamping = true; controls.enablePan = false; controls.autoRotate = false; controls.minDistance = 2; controls.maxDistance = 30;
  const ctx = { scene, camera, light, ambient, controls, buttons: [], caption: '', tick: null, onPick: null, remount: s => mount(host, s) };
  try { (S[spec.kind] || S.orbit)(ctx, spec); } catch (e) { console.error(e); scene.clear(); scene.add(ambient, light); S.orbit(ctx, spec); }
  controls.target.set(0, 0, 0); controls.update();
  wrap.querySelector('.s3d-cap').textContent = '👆 ' + (ctx.caption || 'Drag to spin · pinch to zoom');
  const bw = wrap.querySelector('.s3d-btns');
  ctx.buttons.forEach(([t, f]) => { const b = document.createElement('button'); b.textContent = t; b.onclick = () => { f(b); window.sfx && sfx('tap'); }; bw.appendChild(b); });
  const infoEl = wrap.querySelector('.s3d-info');
  const ray = new THREE.Raycaster(), ptr = new THREE.Vector2(); let down = null;
  canvas.addEventListener('pointerdown', e => { down = [e.clientX, e.clientY]; });
  canvas.addEventListener('pointerup', e => {
    if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 6) return; const r = canvas.getBoundingClientRect();
    ptr.set((e.clientX - r.left) / r.width * 2 - 1, -(e.clientY - r.top) / r.height * 2 + 1); ray.setFromCamera(ptr, camera);
    const hit = ray.intersectObjects(scene.children, true).find(h => h.object.userData.info || h.object.userData.slice !== undefined || h.object.userData.say);
    if (!hit) return;
    if (ctx.onPick && ctx.onPick(hit.object)) return;
    if (hit.object.userData.info) { infoEl.textContent = hit.object.userData.info; infoEl.classList.add('show'); say(hit.object.userData.info); window.sfx && sfx('coin'); clearTimeout(infoEl.t); infoEl.t = setTimeout(() => infoEl.classList.remove('show'), 4500); }
  });
  wrap.querySelector('.s3d-full').onclick = () => { wrap.classList.toggle('full'); resize(); };
  const resize = () => { const w = wrap.clientWidth, h = wrap.clientHeight; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); };
  const ro = new ResizeObserver(resize); ro.observe(wrap); resize();
  const clock = new THREE.Clock(); let visible = true;
  const io = new IntersectionObserver(es => { visible = es[0].isIntersecting; }); io.observe(wrap);
  let idle = 0; controls.addEventListener('start', () => { idle = -9999; }); controls.addEventListener('end', () => { idle = 0; });
  renderer.setAnimationLoop(() => {
    if (!visible || document.hidden) return; const dt = Math.min(.05, clock.getDelta()), t = clock.elapsedTime;
    idle += dt; controls.autoRotate = idle > 4 && spec.kind !== 'solar' && spec.kind !== 'moon'; controls.autoRotateSpeed = .8;
    ctx.tick && ctx.tick(t, dt); controls.update(); renderer.render(scene, camera);
  });
  active = { renderer, ro, io, scene };
  return ctx;
}
export function unmount() {
  if (!active) return; const { renderer, ro, io, scene } = active; renderer.setAnimationLoop(null); ro.disconnect(); io.disconnect();
  scene.traverse(o => { o.geometry && o.geometry.dispose(); if (o.material) { (Array.isArray(o.material) ? o.material : [o.material]).forEach(m => { m.map && m.map.dispose(); m.dispose(); }); } });
  renderer.dispose(); active = null;
}
export const KINDS = Object.keys(S);
