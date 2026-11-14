/* ================= ⚡ Quick Games (js/quick-games.js) — OWNER PREVIEW until the owner makes them live =================
   Three original quick-maths games, each with its own animated scene:
     🪙 Chillar Champ — you run a shop counter. Bills, change, discounts, GST, profit — before the customer's patience runs out.
     🏏 Sixer Sums    — night-match chase under floodlights: fast right answers hit 1/2/4/6, a wrong answer is a wicket.
     🔎 Galti Pakdo   — a detective desk: one line in the bill / tax invoice / bank statement has a slip. Catch it, fix it.
   Every question is generated and calculated by code. A game is driven by a SEED, so the same code = the same questions:
     🙋 Alone   — a fresh game; the end screen gives a challenge code for this exact game.
     👫 Friends — "challenge code": a friend types the code and plays the same questions on their phone; compare scores.
     👨‍👩‍👧 Family — one phone, take turns: every player gets the same questions, then a family scoreboard.
                  own phones: the challenge code, the same way as friends.
   Difficulty bands: j = Class 1–3, m = Class 4–6, s = Class 7–12, p = CA (from the profile; the owner can switch).
   Visibility: QuickGames.visible() — owner only for now (set LIVE = true to open them to every student).
   Best scores: localStorage 'sv_qg' = { game: { band: best } }.
   window.QuickGames = { visible, live: LIVE, GAMES, open(id, {mode, back}), family(id, back), challenge(id, back) } */
(function () {
  'use strict';
  const LIVE = false;                                   // owner decides; false = only the owner sees these games
  const D = document, $1 = (s, r) => (r || D).querySelector(s);
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const S = k => { try { if (window.sfx) sfx(k); } catch (e) {} };
  const T = m => { try { toast(m); } catch (e) {} };
  const XP = (n, m) => { try { if (typeof addXP === 'function') addXP(n, m); } catch (e) {} };
  /* ---- seeded randomness: same seed → same questions (cosmetic choices use cos(), never the seed) ---- */
  let rnd = Math.random;
  const mulberry = a => () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const R = (a, b) => a + Math.floor(rnd() * (b - a + 1));
  const pick = a => a[Math.floor(rnd() * a.length)];
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const cos = a => a[Math.floor(Math.random() * a.length)];
  const inr = n => '₹' + Number(n).toLocaleString('en-IN');
  const num = n => Number(n).toLocaleString('en-IN');
  const isOwner = () => { try { return localStorage.getItem('sv_owner') === '1' || !!(window.Cloud && Cloud.admin && Cloud.admin()); } catch (e) { return false; } };
  const visible = () => LIVE || isOwner();
  const STx = () => { try { return ST; } catch (e) { return null; } };
  const autoBand = () => { const s = STx(); if (!s || !s.profile) return 's'; if (s.profile.course === 'ca') return 'p'; const g = +s.profile.grade || 8; return g <= 3 ? 'j' : g <= 6 ? 'm' : 's'; };
  const myName = () => { const s = STx(); return (s && s.profile && s.profile.name) || 'Me'; };
  const BANDS = [['j', 'Class 1–3'], ['m', 'Class 4–6'], ['s', 'Class 7–12'], ['p', 'CA']];
  let band = null, timer = null;
  const stop = () => { if (timer) { clearInterval(timer); timer = null; } };
  const best = (g, v) => { let o = {}; try { o = JSON.parse(localStorage.getItem('sv_qg') || '{}'); } catch (e) {} o[g] = o[g] || {};
    if (v != null && v > 0 && (o[g][band] == null || v > o[g][band])) { o[g][band] = v; try { localStorage.setItem('sv_qg', JSON.stringify(o)); } catch (e) {} return true; } return v == null ? o[g][band] : false; };

  /* ---- challenge codes: game letter + band letter + 4 seed characters, e.g. SPK9QZ ---- */
  const AL = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789', GL = { chillar: 'C', sixer: 'S', galti: 'G' }, BL = { j: 'J', m: 'M', s: 'S', p: 'P' };
  const newSeed = () => Array.from({ length: 4 }, () => AL[Math.floor(Math.random() * AL.length)]).join('');
  const codeOf = (g, b, seed) => GL[g] + BL[b] + seed;
  const seedInt = s => [...s].reduce((h, c) => Math.imul(h ^ c.charCodeAt(0), 2654435761) >>> 0, 2166136261);
  function parseCode(c) {
    c = String(c || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
    if (c.length !== 6) return null;
    const g = Object.keys(GL).find(k => GL[k] === c[0]), b = Object.keys(BL).find(k => BL[k] === c[1]);
    if (!g || !b || ![...c.slice(2)].every(x => AL.includes(x))) return null;
    return { game: g, band: b, seed: c.slice(2) };
  }
  const reseed = seed => { rnd = mulberry(seedInt(seed)); };

  /* ---------- screen + shared look ---------- */
  function screen() {
    let s = D.getElementById('s-play');
    if (!s) { $1('main').insertAdjacentHTML('beforeend', '<section class="screen" id="s-play"></section>'); s = D.getElementById('s-play'); }
    try { show('play', 'practice'); } catch (e) {}
    window.scrollTo(0, 0); return s;
  }
  /* ================= CSS (original look: three scenes) ================= */
  function style() {
    if (D.getElementById('qgStyle')) return;
    D.head.insertAdjacentHTML('beforeend', `<style id="qgStyle">
.qg{max-width:640px;margin:0 auto;color:#1b1530;font-family:inherit}.qg *{box-sizing:border-box}
.qg-top{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:4px 0 8px}
.qg-pill{display:inline-flex;align-items:center;gap:4px;background:rgba(255,255,255,.14);color:#fff;border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:5px 11px;font-weight:800;font-size:14px;backdrop-filter:blur(4px)}
.qg-pill.combo{background:linear-gradient(90deg,#ff7a18,#ff3d77);border:0;animation:qgPulse .9s ease infinite alternate}
@keyframes qgPulse{to{transform:scale(1.08)}}
.qg-sp{flex:1}
.qg-btn{display:block;width:100%;border:0;border-radius:16px;padding:15px;font:inherit;font-size:18px;font-weight:900;cursor:pointer;color:#fff;margin-top:10px;letter-spacing:.3px}
.qg-btn:active{transform:translateY(3px)}
.qg-ghost{background:rgba(255,255,255,.12)!important;border:2px solid rgba(255,255,255,.5)!important;box-shadow:none!important}
.qg-card{border-radius:22px;padding:16px;margin:10px 0;position:relative;overflow:hidden}
.qg-h{font-size:28px;line-height:1.05;font-weight:900;margin:0;letter-spacing:.3px}
.qg-tag{font-size:14px;opacity:.9;margin:6px 0 0}
.qg-chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}
.qg-chip{border:2px solid rgba(255,255,255,.55);background:transparent;color:#fff;border-radius:999px;padding:7px 13px;font:inherit;font-size:14px;font-weight:700;cursor:pointer}
.qg-chip.on{background:#fff;color:#1b1530}
.qg-code{display:flex;gap:8px;margin-top:8px}.qg-code input{flex:1;min-width:0;border-radius:12px;border:2px solid rgba(255,255,255,.6);background:rgba(0,0,0,.2);color:#fff;font:inherit;font-size:18px;font-weight:800;letter-spacing:4px;text-transform:uppercase;padding:10px 12px}
.qg-code input::placeholder{color:rgba(255,255,255,.6);letter-spacing:1px;font-weight:600}
.qg-code button{border:0;border-radius:12px;padding:0 16px;font:inherit;font-weight:800;cursor:pointer}
/* keypad (themes: .k-till brass cash register, .k-led stadium, .k-ink detective) */
.qg-disp{border-radius:14px;padding:10px 14px;font-size:30px;font-weight:900;min-height:58px;display:flex;align-items:center;justify-content:flex-end;gap:6px;font-variant-numeric:tabular-nums}
.qg-disp .ph{opacity:.45;font-size:16px;font-weight:700}
.qg-disp .cur{width:3px;height:30px;background:currentColor;animation:qgBlink 1s step-end infinite}@keyframes qgBlink{50%{opacity:0}}
.qg-keys{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:10px}
.qg-k{border:0;border-radius:14px;padding:14px 0;font:inherit;font-size:24px;font-weight:900;cursor:pointer;touch-action:manipulation}
.qg-k:active{transform:translateY(3px)}
.k-till .qg-disp{background:#0f2a1a;color:#7dff9b;font-family:ui-monospace,Menlo,Consolas,monospace;box-shadow:inset 0 0 0 3px #2b5c3a,inset 0 4px 12px rgba(0,0,0,.6);text-shadow:0 0 8px rgba(125,255,155,.6)}
.k-till .qg-k{background:linear-gradient(#fdf3d7,#e8d3a0);color:#4a3412;box-shadow:0 4px 0 #a4824a}.k-till .qg-k.ok{background:linear-gradient(#5fd38a,#2f9e5c);color:#fff;box-shadow:0 4px 0 #1f6b3e}.k-till .qg-k.del{background:linear-gradient(#ffd0c2,#f5a48c);box-shadow:0 4px 0 #b9654c}
.k-led .qg-disp{background:#05070d;color:#ffb21e;font-family:ui-monospace,Menlo,Consolas,monospace;box-shadow:inset 0 0 0 2px #2a3352;text-shadow:0 0 10px rgba(255,178,30,.8)}
.k-led .qg-k{background:#1d2742;color:#fff;box-shadow:0 4px 0 #0b1122}.k-led .qg-k.ok{background:linear-gradient(#36d17a,#1a9a52);box-shadow:0 4px 0 #0f6334}.k-led .qg-k.del{background:#4a2338}
.k-ink .qg-disp{background:#fffdf6;color:#1b1530;font-family:'Courier New',monospace;box-shadow:inset 0 0 0 2px #c9b98f}
.k-ink .qg-k{background:#f7efdc;color:#3b2d16;box-shadow:0 4px 0 #b9a473}.k-ink .qg-k.ok{background:#c0392b;color:#fff;box-shadow:0 4px 0 #7d2219}.k-ink .qg-k.del{background:#e9dcc0}
.qg-fb{min-height:24px;font-weight:900;margin-top:8px;font-size:16px}
.qg-how{border-radius:12px;padding:10px 12px;margin-top:8px;font-size:14.5px;line-height:1.5}
.qg-float{position:absolute;font-weight:900;font-size:26px;pointer-events:none;animation:qgUp 1.1s ease-out forwards;z-index:5}
@keyframes qgUp{from{opacity:1;transform:translateY(0) scale(.8)}to{opacity:0;transform:translateY(-70px) scale(1.25)}}
.qg-coin{position:absolute;font-size:20px;pointer-events:none;animation:qgCoin .9s ease-in forwards;z-index:5}
@keyframes qgCoin{to{transform:translate(var(--dx),var(--dy)) rotate(540deg);opacity:0}}
.qg-podium{display:grid;gap:8px;margin:10px 0}.qg-pl{display:flex;align-items:center;gap:10px;border-radius:14px;padding:10px 12px;background:rgba(255,255,255,.14);color:#fff;font-weight:800}
.qg-pl b{flex:1}.qg-pl .s{font-size:22px}
.qg-pl.w{background:linear-gradient(90deg,#ffd447,#ffb21e);color:#2b1a00}
.qg-sharebox{border:2px dashed rgba(255,255,255,.6);border-radius:16px;padding:12px;text-align:center;color:#fff;margin-top:10px}
.qg-sharebox .c{font-size:30px;font-weight:900;letter-spacing:6px;font-family:ui-monospace,Menlo,Consolas,monospace}
/* ===== 🪙 CHILLAR CHAMP: market lane at golden hour ===== */
.cc-wrap{background:linear-gradient(180deg,#ff9a3c 0%,#ffcf6e 38%,#ffe7b0 60%);border-radius:24px;padding:12px;position:relative;overflow:hidden}
.cc-awn{height:46px;margin:-12px -12px 6px;background:repeating-linear-gradient(90deg,#e8364f 0 34px,#fff7e8 34px 68px);position:relative;box-shadow:0 6px 10px rgba(120,40,0,.25)}
.cc-awn:after{content:"";position:absolute;left:0;right:0;bottom:-14px;height:16px;background:radial-gradient(circle at 17px 0,#e8364f 16px,transparent 17px) 0 0/68px 16px repeat-x,radial-gradient(circle at 51px 0,#fff7e8 16px,transparent 17px) 0 0/68px 16px repeat-x}
.cc-sign{position:absolute;left:50%;top:6px;transform:translateX(-50%) rotate(-2deg);background:#3b1d0e;color:#ffd447;font-weight:900;font-size:15px;padding:4px 14px;border-radius:8px;letter-spacing:2px;border:2px solid #ffd447;z-index:2;white-space:nowrap}
.cc-shelf{display:flex;justify-content:space-around;font-size:24px;background:linear-gradient(#8a5a2b,#6b4220);border-radius:8px;padding:4px 0 6px;margin:12px 0 10px;box-shadow:0 4px 0 #4a2c12}
.cc-stage{display:flex;gap:12px;align-items:flex-end;min-height:120px}
.cc-cust{position:relative;width:96px;height:96px;flex:none;animation:ccIn .55s cubic-bezier(.2,1.4,.4,1)}
@keyframes ccIn{from{transform:translateX(160px) rotate(12deg);opacity:0}}
.cc-ring{position:absolute;inset:0;border-radius:50%;background:conic-gradient(var(--c,#2fbf71) calc(var(--p,1)*360deg),rgba(0,0,0,.12) 0)}
.cc-face{position:absolute;inset:7px;border-radius:50%;background:#fff3d6;display:grid;place-items:center;font-size:52px}
.cc-mood{position:absolute;right:-6px;top:-6px;font-size:28px;filter:drop-shadow(0 2px 2px rgba(0,0,0,.3))}
.cc-say{flex:1;background:#fff;border-radius:18px 18px 18px 4px;padding:10px 13px;font-size:16.5px;line-height:1.45;box-shadow:0 4px 0 rgba(120,60,0,.18);animation:ccPop .4s .25s both}
@keyframes ccPop{from{transform:scale(.6);opacity:0}}
.cc-say small{display:block;font-weight:800;color:#b5471b;font-size:12.5px;letter-spacing:.5px;text-transform:uppercase}
.cc-say b{color:#c2185b}
.cc-counter{background:linear-gradient(#6b4220,#4a2c12);border-radius:18px;padding:12px;margin-top:10px;color:#ffe9b5;box-shadow:inset 0 2px 0 rgba(255,255,255,.15)}
.cc-q{font-size:17px;font-weight:900;margin:0 0 8px}
.cc-jar{position:absolute;right:12px;top:58px;font-size:12px;font-weight:900;text-align:center;color:#3b1d0e}
.cc-jar span{display:block;font-size:30px;line-height:1}.cc-jar.bump span{animation:ccBump .5s}
@keyframes ccBump{40%{transform:scale(1.4) rotate(-10deg)}}
.cc-wrap .qg-how{background:#fff7e2;color:#3b1d0e}.cc-wrap .qg-fb.good{color:#0f7a3c}.cc-wrap .qg-fb.bad{color:#c62828}
.cc-btn{background:linear-gradient(#ff5a7a,#d81b60);box-shadow:0 5px 0 #8e0f3d}
.cc-hero{background:linear-gradient(160deg,#ff7a18,#d81b60 70%);color:#fff}
/* ===== 🏏 SIXER SUMS: floodlit night stadium ===== */
.ss-wrap{background:radial-gradient(ellipse at 15% -10%,rgba(255,255,220,.55),transparent 35%),radial-gradient(ellipse at 85% -10%,rgba(255,255,220,.55),transparent 35%),linear-gradient(#0a1238,#132a6b 55%,#0a1238);border-radius:24px;padding:12px;color:#fff;position:relative;overflow:hidden}
.ss-crowd{height:34px;margin:0 -12px;background:radial-gradient(circle,#ffd447 1.6px,transparent 2px) 0 0/12px 10px,radial-gradient(circle,#ff6b9a 1.6px,transparent 2px) 6px 5px/12px 10px,linear-gradient(#1b2a5c,#24377a);opacity:.9}
.ss-wrap.wave .ss-crowd{animation:ssWave .5s ease 3}@keyframes ssWave{50%{transform:translateY(-6px)}}
.ss-board{background:#020409;border:3px solid #2a3352;border-radius:12px;padding:8px 10px;font-family:ui-monospace,Menlo,Consolas,monospace;color:#ffb21e;text-shadow:0 0 8px rgba(255,178,30,.85);display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:4px;text-align:center;margin:8px 0}
.ss-board small{display:block;color:#7f8bb8;text-shadow:none;font-size:10.5px;letter-spacing:1px}.ss-board b{font-size:24px}
.ss-field{position:relative;height:150px;border-radius:50%/42%;background:repeating-linear-gradient(90deg,#2f9a4c 0 22px,#38ad57 22px 44px);border:4px solid #fff;margin:8px 0;overflow:hidden}
.ss-pitch{position:absolute;left:50%;top:22%;width:30px;height:56%;margin-left:-15px;background:#d6bf86;border-radius:3px}
.ss-stumps{position:absolute;left:50%;top:20%;margin-left:-9px;display:flex;gap:3px}.ss-stumps i{width:4px;height:16px;background:#fff;border-radius:2px;transition:transform .6s}
.ss-field.out .ss-stumps i:nth-child(1){transform:translate(-14px,-10px) rotate(-60deg)}.ss-field.out .ss-stumps i:nth-child(3){transform:translate(14px,-10px) rotate(60deg)}.ss-field.out .ss-stumps i:nth-child(2){transform:translateY(-14px) rotate(20deg)}
.ss-bat{position:absolute;left:50%;top:70%;font-size:28px;margin-left:-14px}
.ss-ball{position:absolute;left:50%;top:66%;width:12px;height:12px;margin-left:-6px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#ff8a8a,#c0001a);box-shadow:0 0 6px rgba(255,0,0,.7);opacity:0}
.ss-field.hit6 .ss-ball{animation:ss6 1s ease-out forwards}.ss-field.hit4 .ss-ball{animation:ss4 .9s ease-out forwards}.ss-field.hit2 .ss-ball{animation:ss2 .8s ease-out forwards}
@keyframes ss6{0%{opacity:1;transform:translate(0,0) scale(1)}50%{transform:translate(70px,-110px) scale(2.4)}100%{opacity:0;transform:translate(150px,-180px) scale(.6)}}
@keyframes ss4{0%{opacity:1;transform:translate(0,0)}100%{opacity:.9;transform:translate(-150px,-40px)}}
@keyframes ss2{0%{opacity:1;transform:translate(0,0)}100%{opacity:.9;transform:translate(60px,-30px)}}
.ss-stamp{position:absolute;left:0;right:0;top:34%;text-align:center;font-size:54px;font-weight:900;letter-spacing:4px;pointer-events:none;opacity:0;z-index:6;-webkit-text-stroke:2px #1b1530;text-shadow:0 6px 0 rgba(0,0,0,.35)}
.ss-stamp.go{animation:ssStamp 1.2s cubic-bezier(.2,1.6,.4,1) forwards}@keyframes ssStamp{0%{opacity:0;transform:scale(3) rotate(-12deg)}25%{opacity:1;transform:scale(1) rotate(-6deg)}80%{opacity:1}100%{opacity:0;transform:scale(1.1) rotate(-6deg)}}
.ss-stamp.six{color:#ffd447}.ss-stamp.four{color:#5ef2a4}.ss-stamp.out{color:#ff4d6d}
.ss-dots{display:flex;gap:5px;flex-wrap:wrap;justify-content:center;margin:6px 0}
.ss-dot{width:28px;height:28px;border-radius:50%;display:grid;place-items:center;font-size:13px;font-weight:900;background:rgba(255,255,255,.12);border:2px solid rgba(255,255,255,.25)}
.ss-dot.r6{background:#ffd447;color:#2b1a00;border-color:#ffd447}.ss-dot.r4{background:#5ef2a4;color:#063;border-color:#5ef2a4}.ss-dot.w{background:#ff4d6d;border-color:#ff4d6d}.ss-dot.now{border-color:#fff;box-shadow:0 0 0 3px rgba(255,255,255,.3)}
.ss-q{background:rgba(255,255,255,.08);border-radius:18px;padding:12px;border:1px solid rgba(255,255,255,.18)}
.ss-qt{font-size:28px;font-weight:900;text-align:center;margin:0 0 8px;animation:ccPop .35s both}
.ss-tick{height:8px;border-radius:6px;background:rgba(255,255,255,.15);overflow:hidden;margin-bottom:8px}.ss-tick i{display:block;height:100%;background:linear-gradient(90deg,#5ef2a4,#ffd447 60%,#ff4d6d);transition:width .1s linear}
.ss-comm{font-style:italic;min-height:22px;margin:6px 0;color:#cfe0ff}
.ss-wrap .qg-how{background:rgba(255,255,255,.12)}.ss-btn{background:linear-gradient(#36d17a,#1a9a52);box-shadow:0 5px 0 #0f6334}
.ss-hero{background:linear-gradient(160deg,#0a1238,#1d4bbf);color:#fff}
/* ===== 🔎 GALTI PAKDO: detective desk ===== */
.gp-wrap{background:repeating-linear-gradient(92deg,#5a3a22 0 18px,#633f25 18px 36px,#56371f 36px 50px);border-radius:24px;padding:12px;position:relative;overflow:hidden;color:#fff}
.gp-lamp{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 0,rgba(255,236,170,.35),transparent 60%);pointer-events:none}
.gp-file{position:relative;background:#e9c27a;border-radius:4px 14px 14px 14px;padding:10px;margin-top:14px;box-shadow:0 8px 18px rgba(0,0,0,.4)}
.gp-file:before{content:attr(data-tab);position:absolute;top:-22px;left:0;background:#e9c27a;color:#4a2c12;font-weight:900;font-size:12.5px;letter-spacing:1.5px;padding:3px 12px;border-radius:8px 8px 0 0}
.gp-doc{background:#fffdf4;color:#1f1a14;border-radius:3px;padding:12px 12px 8px;font-family:'Courier New',ui-monospace,monospace;font-size:13.5px;transform:rotate(-.6deg);position:relative;background-image:radial-gradient(circle at 88% 12%,transparent 18px,rgba(140,90,40,.18) 19px,rgba(140,90,40,.18) 21px,transparent 22px)}
.gp-doc h4{margin:0;text-align:center;font-size:16px;letter-spacing:3px}.gp-doc .m{text-align:center;font-size:11.5px;opacity:.7;margin:2px 0 8px}
.gp-row{display:grid;grid-template-columns:1fr auto;gap:8px;width:100%;border:0;background:none;font:inherit;color:inherit;text-align:left;padding:8px 6px;border-bottom:1px dashed #cbbf9f;cursor:pointer;position:relative;border-radius:4px}
.gp-row:hover{background:rgba(255,213,79,.18)}.gp-row .v{text-align:right;white-space:nowrap;font-weight:700}
.gp-row.tot{font-weight:900;border-bottom:0;border-top:2px solid #1f1a14}
.gp-row.circ:after{content:"";position:absolute;inset:-3px -6px;border:3px solid #d32f2f;border-radius:50%;animation:gpCirc .45s ease-out both}
@keyframes gpCirc{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
.gp-row.miss{animation:gpShake .35s}@keyframes gpShake{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
.gp-row.fix .v{color:#1a7f37}.gp-row.fix .v:before{content:attr(data-was);text-decoration:line-through;color:#d32f2f;margin-right:8px;font-weight:400}
.gp-stamp{position:absolute;left:50%;top:40%;transform:translate(-50%,-50%) rotate(-14deg) scale(2.5);border:5px solid #c62828;color:#c62828;font-weight:900;font-size:30px;letter-spacing:3px;padding:4px 14px;border-radius:10px;opacity:0;pointer-events:none;z-index:6;background:rgba(255,253,244,.6);white-space:nowrap}
.gp-stamp.go{animation:gpStamp .5s cubic-bezier(.2,1.5,.4,1) forwards}@keyframes gpStamp{to{opacity:.92;transform:translate(-50%,-50%) rotate(-14deg) scale(1)}}
.gp-sand{height:10px;border-radius:6px;background:rgba(0,0,0,.35);overflow:hidden;margin:6px 0}.gp-sand i{display:block;height:100%;background:linear-gradient(90deg,#ffd447,#ff9800);transition:width .1s linear}.gp-sand.low i{background:#ff4d4d}
.gp-hint{font-weight:800;margin:8px 2px 0;min-height:22px}
.gp-fix{background:#fffdf4;border-radius:14px;padding:10px;margin-top:10px;color:#1f1a14}
.gp-wrap .qg-how{background:#fff7e2;color:#3b2d16}.gp-btn{background:linear-gradient(#e53935,#b71c1c);box-shadow:0 5px 0 #7f1212}
.gp-hero{background:linear-gradient(160deg,#3e2716,#7a4a24);color:#fff}
.qg-chip:focus-visible,.qg-k:focus-visible,.qg-btn:focus-visible,.gp-row:focus-visible,.qg-code input:focus-visible{outline:3px solid #ffd447;outline-offset:2px}
@media (prefers-reduced-motion:reduce){.qg *,.qg *:before,.qg *:after{animation:none!important;transition:none!important}}
</style>`);
  }

  /* ---------- keypad (screen keys + physical keyboard) ---------- */
  function keypad(host, theme, onOK) {
    let v = '';
    host.classList.add(theme);
    const disp = $1('.qg-disp', host), keys = $1('.qg-keys', host);
    const draw = () => { disp.innerHTML = `${v ? (theme === 'k-till' ? '₹ ' : '') + E(num(+v)) : '<span class="ph">type your answer</span>'}<span class="cur" aria-hidden="true"></span>`; disp.setAttribute('aria-label', 'Your answer: ' + (v || 'empty')); };
    const press = k => { if (k === 'del') v = v.slice(0, -1); else if (k === 'ok') { if (v) onOK(+v); return; } else if (v.length < 9) v = (v === '0' ? '' : v) + k; S('tap'); draw(); };
    keys.innerHTML = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'del', '0', 'ok'].map(k => `<button type="button" class="qg-k${k === 'ok' ? ' ok' : k === 'del' ? ' del' : ''}" data-k="${k}" aria-label="${k === 'del' ? 'Delete' : k === 'ok' ? 'Check answer' : k}">${k === 'del' ? '⌫' : k === 'ok' ? '✔' : k}</button>`).join('');
    keys.querySelectorAll('[data-k]').forEach(b => b.onclick = () => press(b.dataset.k));
    const kb = e => { if (!D.body.contains(disp)) { D.removeEventListener('keydown', kb); return; } if (e.target && e.target.tagName === 'INPUT') return; if (/^\d$/.test(e.key)) press(e.key); else if (e.key === 'Backspace') press('del'); else if (e.key === 'Enter') press('ok'); };
    D.addEventListener('keydown', kb); draw();
    return { clear() { v = ''; draw(); }, off() { D.removeEventListener('keydown', kb); keys.innerHTML = ''; } };
  }
  const floatAt = (host, text, color) => { const f = D.createElement('div'); f.className = 'qg-float'; f.textContent = text; f.style.cssText = `left:50%;top:40%;color:${color}`; host.appendChild(f); setTimeout(() => f.remove(), 1200); };
  const coins = (host, n) => { for (let i = 0; i < n; i++) { const c = D.createElement('span'); c.className = 'qg-coin'; c.textContent = '🪙'; c.style.cssText = `left:${40 + Math.random() * 20}%;top:45%;--dx:${(Math.random() - .5) * 220}px;--dy:${-60 - Math.random() * 120}px;animation-delay:${i * 40}ms`; host.appendChild(c); setTimeout(() => c.remove(), 1200); } };

  /* ================= content generators (every answer computed) ================= */
  const SHOP = [['🍌', 'bananas (dozen)', 40, 80, 's'], ['🥭', 'mangoes (kg)', 80, 200, 's'], ['🍅', 'tomatoes (kg)', 20, 60, 's'], ['🧅', 'onions (kg)', 30, 60, 's'],
    ['🥛', 'milk packet', 25, 35, 's'], ['🍪', 'biscuit pack', 10, 40, 's'], ['📒', 'notebook', 30, 80, 's'], ['✏️', 'pencil box', 60, 150, 'b'], ['🪔', 'diya set', 50, 150, 'b'],
    ['🧴', 'shampoo bottle', 120, 250, 'b'], ['👕', 'T-shirt', 250, 600, 'b'], ['🎒', 'school bag', 450, 1200, 'b'], ['👟', 'pair of shoes', 600, 1800, 'b'], ['📱', 'phone cover', 150, 400, 'b']];
  const PEOPLE = [['👵', 'Meena Aunty'], ['🧔', 'Raju Bhaiya'], ['👩', 'Fatima Didi'], ['👳', 'Gurpreet Ji'], ['👨‍🦳', 'Mr. Iyer'], ['👧', 'Kavya'], ['👴', 'Joseph Uncle'], ['🧑', 'Tenzin'], ['👩‍🦱', 'Ananya'], ['👦', 'Arjun'], ['🧕', 'Zoya'], ['👨', 'Vikram Sir']];
  const price = (it, step) => { const s = step || (it[3] > 200 ? 10 : 5); return Math.max(s, Math.round(R(it[2], it[3]) / s) * s); };
  const small = () => SHOP.filter(x => x[4] === 's'), bigItems = () => SHOP.filter(x => x[4] === 'b');
  const TASKS = {
    total() { const a = pick(small()), b = pick(small().filter(x => x !== a)), pa = band === 'j' ? R(5, 45) : price(a), pb = band === 'j' ? R(5, 45) : price(b);
      return { say: `One <b>${a[1]}</b> for ${inr(pa)} and one <b>${b[1]}</b> for ${inr(pb)}, please.`, q: 'How much is the total?', a: pa + pb, w: `${inr(pa)} + ${inr(pb)} = ${inr(pa + pb)}`, e: a[0] + b[0] }; },
    change() { const bill = band === 'j' ? R(11, 49) : band === 'm' ? R(12, 95) * 5 : R(12, 49) * 10 - pick([0, 5]), n = band === 'j' ? 50 : [100, 200, 500].find(x => x > bill);
      return { say: `My bill is <b>${inr(bill)}</b>. Here is a <b>${inr(n)}</b> note.`, q: 'How much change do you give back?', a: n - bill, w: `${inr(n)} − ${inr(bill)} = ${inr(n - bill)}`, e: '💵' }; },
    qty() { const it = pick(small()), p = price(it), q = R(3, band === 'm' ? 9 : 12);
      return { say: `I need <b>${q}</b> × ${it[1]} at <b>${inr(p)}</b> each.`, q: 'What do I pay?', a: p * q, w: `${q} × ${inr(p)} = ${inr(p * q)}`, e: it[0] }; },
    disc() { const it = pick(bigItems()), pct = pick(band === 'm' ? [10, 50] : [10, 20, 25, 50]), p = R(Math.ceil(it[2] / 20), Math.floor(it[3] / 20)) * 20, off = p * pct / 100;
      return { say: `This <b>${it[1]}</b> says <b>${inr(p)}</b>. Your board says <b>${pct}% off</b>!`, q: 'What is the price after the discount?', a: p - off, w: `${pct}% of ${inr(p)} = ${inr(off)}; ${inr(p)} − ${inr(off)} = ${inr(p - off)}`, e: it[0] }; },
    gst() { const it = pick(bigItems()), r = pick([5, 18]), p = R(Math.max(1, Math.ceil(it[2] / 100)), Math.floor(it[3] / 100)) * 100, g = p * r / 100;
      return { say: `The <b>${it[1]}</b> is <b>${inr(p)}</b> plus <b>${r}% GST</b>. Add it up for me.`, q: 'What is the total with GST?', a: p + g, w: `${r}% of ${inr(p)} = ${inr(g)}; ${inr(p)} + ${inr(g)} = ${inr(p + g)}`, e: it[0] }; },
    discgst() { const p = R(2, 9) * 1000, after = p * 9 / 10, g = after * 18 / 100;
      return { say: `Bulk order: list price <b>${inr(p)}</b>, <b>10% trade discount</b>, then <b>18% GST</b>.`, q: 'What is the invoice total?', a: after + g, w: `Discount: ${inr(p)} − 10% = ${inr(after)}; GST 18% of ${inr(after)} = ${inr(g)}; total ${inr(after + g)}. GST is charged on the price after the discount.`, e: '📦' }; },
    cgst() { const p = R(3, 40) * 100, c = p * 9 / 100;
      return { say: `Sale inside our own state: <b>${inr(p)}</b> at <b>18% GST</b>.`, q: 'How much is the CGST on this bill?', a: c, w: `Inside one state, 18% splits into CGST 9% + SGST 9%. 9% of ${inr(p)} = ${inr(c)}.`, e: '🧾' }; },
    profit() { const c = R(5, 40) * 20, p = pick([5, 10, 20, 25]), s = c * (100 + p) / 100;
      return { say: `I bought these for <b>${inr(c)}</b> and sold them for <b>${inr(s)}</b>.`, q: 'What was my profit percentage? (just the number)', a: p, w: `Profit = ${inr(s)} − ${inr(c)} = ${inr(s - c)}; ${inr(s - c)} ÷ ${inr(c)} × 100 = ${p}%`, e: '📈' }; }
  };

  const CQ = {
    j: [() => { const a = R(2, 12), b = R(1, 9); return { q: `${a} + ${b}`, a: a + b, tip: `Count on from ${a}: ${b} more.` }; },
      () => { const a = R(8, 19), b = R(1, a - 1 > 9 ? 9 : a - 1); return { q: `${a} − ${b}`, a: a - b, tip: `Count back ${b} from ${a}.` }; },
      () => { const t = pick([2, 5, 10]), n = R(1, 10); return { q: `${n} × ${t}`, a: n * t, tip: t === 10 ? 'Times 10: put a 0 at the end.' : t === 5 ? 'Times 5: half of times 10.' : 'Times 2: just double it.' }; }],
    m: [() => { const a = R(21, 89), b = R(11, 79); return { q: `${a} + ${b}`, a: a + b, tip: `Add tens first (${a - a % 10} + ${b - b % 10}), then ones (${a % 10} + ${b % 10}).` }; },
      () => { const a = R(50, 99), b = R(11, a - 10); return { q: `${a} − ${b}`, a: a - b, tip: `Take away the tens, then the ones.` }; },
      () => { const a = R(3, 12), b = R(3, 12); return { q: `${a} × ${b}`, a: a * b, tip: `Tables: ${a} × ${b}.` }; },
      () => { const a = R(12, 45); return { q: `${a} × 11`, a: a * 11, tip: `×11 trick: write ${String(a)[0]}, then ${String(a)[0]}+${String(a)[1]}, then ${String(a)[1]} (carry if the middle is 10 or more).` }; },
      () => { const a = R(6, 49) * 2; return { q: `Half of ${a}`, a: a / 2, tip: 'Half the tens, half the ones.' }; }],
    s: [() => { const a = pick([15, 25, 35, 45, 55, 65, 75, 85, 95]), t = Math.floor(a / 10); return { q: `${a}²`, a: a * a, tip: `Ends in 5: ${t} × ${t + 1} = ${t * (t + 1)}, then write 25 → ${a * a}.` }; },
      () => { const a = R(12, 99); return { q: `${a} × 11`, a: a * 11, tip: `×11 trick: first digit, sum of digits in the middle, last digit (carry if needed).` }; },
      () => { const a = R(13, 49), b = R(3, 9); return { q: `${a} × ${b}`, a: a * b, tip: `Split: ${a - a % 10} × ${b} + ${a % 10} × ${b} = ${(a - a % 10) * b} + ${(a % 10) * b}.` }; },
      () => { const p = pick([10, 20, 25, 50]), n = R(2, 40) * 20; return { q: `${p}% of ${n}`, a: n * p / 100, tip: p === 25 ? 'Quarter it: halve, then halve again.' : p === 50 ? 'Just halve it.' : p === 10 ? 'Move the decimal one place left.' : 'Find 10%, then double it.' }; },
      () => { const a = R(91, 99), b = R(91, 99); return { q: `${a} × ${b}`, a: a * b, tip: `Near-100 trick: ${a} is ${100 - a} below, ${b} is ${100 - b} below. ${a} − ${100 - b} = ${a - (100 - b)}, then ${100 - a} × ${100 - b} = ${String((100 - a) * (100 - b)).padStart(2, '0')} → ${a * b}.` }; }],
    p: [() => { const r = pick([5, 18]), n = R(5, 90) * 100; return { q: `${r}% GST on ${inr(n)}`, a: n * r / 100, tip: r === 18 ? `18% = 10% + 8%: ${num(n / 10)} + ${num(n * 8 / 100)}.` : `5% = half of 10%: ${num(n / 20)}.` }; },
      () => { const n = R(2, 30) * 1000; return { q: `${inr(n)} after 10% TDS`, a: n * 9 / 10, tip: `10% of ${num(n)} = ${num(n / 10)}; take it away.` }; },
      () => { const p = R(1, 12) * 10000, r = pick([6, 9, 12]), m = pick([6, 12]); return { q: `Simple interest: ${inr(p)} at ${r}% for ${m} months`, a: p * r / 100 * m / 12, tip: `P × R × T = ${num(p)} × ${r}% × ${m}/12.` }; },
      () => { const a = pick([15, 25, 35, 45, 55, 65, 75, 85, 95]), t = Math.floor(a / 10); return { q: `${a}²`, a: a * a, tip: `${t} × ${t + 1} = ${t * (t + 1)}, then 25.` }; },
      () => { const n = R(2, 50) * 100, r = pick([18]), g = n * r / 100; return { q: `Price incl. 18% GST is ${inr(n + g)}. Price before GST?`, a: n, tip: `Divide by 1.18: ${num(n + g)} ÷ 1.18 = ${num(n)}.` }; }]
  };

  const swapDigits = n => { const s = String(n); const idx = []; for (let i = 0; i < s.length - 1; i++) if (s[i] !== s[i + 1]) idx.push(i); if (!idx.length) return n + 10; const i = pick(idx); return +(s.slice(0, i) + s[i + 1] + s[i] + s.slice(i + 2)); };
  const nudge = n => { const d = pick([10, 100, 9, 1]); const m = Math.max(d, Math.round(n * 0.04 / d) * d); return n + (rnd() < .5 ? m : -Math.min(m, n - 1)); };
  const DOCS = {
    /* Rule for every document: exactly ONE line has a slip. Lines below it are worked out from the figures as shown,
       so every other line checks out against the lines above it — the slip is the only line that fails its own check. */
    bill() { // shopping bill / cash memo
      const shop = pick(['Sharma General Store', 'Lakshmi Stationers', 'Green Leaf Fruits', 'New Star Kirana']);
      const items = shuffle(SHOP).slice(0, band === 'j' ? 3 : 4).map(it => { const q = R(1, band === 'j' ? 3 : 5), r = band === 'j' ? R(5, 40) : price(it); return { l: `${it[0]} ${it[1]}  ${q} × ${r}`, v: q * r, name: `${q} × ${r}` }; });
      const ei = R(0, items.length), rows = items.map(x => ({ l: x.l, v: x.v }));
      let correct, why;
      if (ei < items.length) { correct = rows[ei].v; rows[ei].v = band === 'j' ? correct + pick([10, -10, 1, -1].filter(d => correct + d > 0)) : swapDigits(correct);
        why = `${items[ei].name} = ${inr(correct)}, but the bill shows ${inr(rows[ei].v)}. ${band === 'j' ? 'The multiplication slipped.' : 'Two digits were swapped while writing.'} The total was added from the wrong figure, so it changes too.`; }
      const tot = rows.reduce((s, r) => s + r.v, 0); rows.push({ l: 'TOTAL', v: tot, tot: 1 });
      if (ei === items.length) { correct = tot; rows[ei].v = nudge(tot); why = `The items add up to ${inr(correct)}, not ${inr(rows[ei].v)} — the total was added wrongly.`; }
      return { title: shop.toUpperCase(), meta: 'Cash memo · check every line', rows, ei, correct, why };
    },
    tax() { // tax invoice, intra-state: CGST 9% + SGST 9%
      const its = [['Printer paper (box)', R(2, 9), R(4, 9) * 100], ['Toner cartridge', R(1, 4), R(18, 45) * 100], ['Office chair', R(1, 3), R(35, 90) * 100]];
      const rows = its.map(([n, q, r]) => ({ l: `${n}  ${q} × ${num(r)}`, v: q * r, f: `${q} × ${num(r)}` }));
      const kind = pick(['item', 'cgst', 'sgst', 'total']); let ei, correct;
      if (kind === 'item') { ei = R(0, 2); correct = rows[ei].v; rows[ei].v = swapDigits(correct); }
      const tv = rows.reduce((s, r) => s + r.v, 0), c = Math.round(tv * 9) / 100;
      rows.push({ l: 'Taxable value', v: tv, tot: 1 }, { l: 'CGST @ 9%', v: c }, { l: 'SGST @ 9%', v: c });
      if (kind === 'cgst' || kind === 'sgst') { ei = kind === 'cgst' ? 4 : 5; correct = c; rows[ei].v = pick([Math.round(tv * 18) / 100, swapDigits(c)]); }
      const total = rows[3].v + rows[4].v + rows[5].v; rows.push({ l: 'INVOICE TOTAL', v: total, tot: 1 });
      if (kind === 'total') { ei = 6; correct = total; rows[6].v = nudge(total); }
      const shown = rows[ei].v, half = Math.round(tv * 18) / 100;
      const why = { item: `${rows[ei].f} = ${inr(correct)}; the digits were swapped to ${inr(shown)}. The taxable value and the taxes below were worked out from the wrong figure, so they change too.`,
        cgst: shown === half ? `CGST was charged at the full 18%. Inside one state, 18% splits into CGST 9% + SGST 9%: 9% of ${inr(tv)} = ${inr(correct)}.` : `9% of ${inr(tv)} = ${inr(correct)}, not ${inr(shown)}. CGST and SGST must be equal.`,
        sgst: shown === half ? `SGST was charged at the full 18%. It should be 9% of ${inr(tv)} = ${inr(correct)}.` : `9% of ${inr(tv)} = ${inr(correct)}, not ${inr(shown)}. CGST and SGST must be equal.`,
        total: `${inr(tv)} + ${inr(c)} + ${inr(c)} = ${inr(correct)}; the invoice total was added wrongly.` }[kind];
      return { title: 'TAX INVOICE', meta: 'Indigo Office Supplies Pvt Ltd · intra-state supply', rows, ei, correct, why };
    },
    bank() { // running balance, checked from the top
      let bal = R(20, 80) * 1000; const tx = [], rows = [{ l: 'Opening balance', v: bal, tot: 1 }];
      shuffle([['Salary credit', 1], ['Rent paid', -1], ['Electricity bill', -1], ['UPI from client', 1], ['Insurance premium', -1]]).slice(0, 4)
        .forEach(([n, sg]) => { const a = R(2, 40) * 500 * (sg > 0 ? 2 : 1), amt = sg > 0 ? a : Math.min(a, Math.max(500, bal - 5000)); bal += sg * amt; tx.push([n, sg * amt]); });
      const ei = R(1, tx.length); let correct = 0, run = rows[0].v;
      tx.forEach(([n, d], k) => { let v = run + d; if (k + 1 === ei) { correct = v; const sw = swapDigits(v); v = pick([v + 1000, v + 100].concat(sw > v ? [sw] : [])); } run = v; rows.push({ l: `${n}  ${d > 0 ? '+' : '−'}${num(Math.abs(d))}  → balance`, v }); });
      return { title: 'BANK STATEMENT', meta: 'Savings account · check each balance against the line above', rows, ei, correct,
        why: `Line above + this entry = ${inr(correct)}, but the statement shows ${inr(rows[ei].v)}. The balances below were carried forward from the slip, so they also need correcting.` };
    }
  };


  /* ================= game definitions ================= */
  const GAMES = [
    { id: 'chillar', e: '🪙', n: 'Chillar Champ', d: 'Run the shop counter: bills, change, discounts, GST — before the customer’s patience runs out.', hero: 'cc-hero', btn: 'cc-btn' },
    { id: 'sixer', e: '🏏', n: 'Sixer Sums', d: 'Night-match chase: answer fast to hit sixes. A wrong answer is a wicket!', hero: 'ss-hero', btn: 'ss-btn' },
    { id: 'galti', e: '🔎', n: 'Galti Pakdo', d: 'One line in the document is wrong. Catch the slip, fix it, close the case.', hero: 'gp-hero', btn: 'gp-btn' }];
  const G = id => GAMES.find(g => g.id === id);

  /* ---------- session: who plays, which seed ---------- */
  let SES = null;   // { game, seed, mode: 'solo'|'family'|'challenge', players: [{n,e,score,detail}], pi, back }
  const back = () => { stop(); const b = SES && SES.back; SES = null; try { (b || (() => PlayHub.open()))(); } catch (e) {} };

  /* intro: start alone, type a challenge code, pick level (owner) */
  function intro(id, o) {
    o = o || {}; stop(); style(); band = band || autoBand();
    const g = G(id), el = screen();
    const bandRow = isOwner() ? `<p class="qg-tag" style="margin-top:10px"><b>Level</b> (owner preview — students get theirs automatically)</p><div class="qg-chips" role="radiogroup" aria-label="Level">${BANDS.map(([k, n]) => `<button type="button" role="radio" class="qg-chip${k === band ? ' on' : ''}" aria-checked="${k === band}" data-band="${k}">${n}</button>`).join('')}</div>` : '';
    const b = best(id);
    el.innerHTML = `<div class="qg"><button class="back" type="button" id="qgB">← Play</button>
      <div class="qg-card ${g.hero}"><div style="font-size:54px;line-height:1" aria-hidden="true">${g.e}</div>
        <h1 class="qg-h">${E(g.n)}</h1><p class="qg-tag">${E(g.d)}</p>${b != null ? `<p class="qg-tag">🏆 Your best: <b>${num(b)}</b></p>` : ''}
        ${RULES[id]}${bandRow}
        <button class="qg-btn ${g.btn}" id="qgGo" type="button">${o.cta || 'Play ▶'}</button>
        <p class="qg-tag" style="margin-top:14px"><b>Got a challenge code?</b> Play the exact same questions as your friend.</p>
        <div class="qg-code"><input id="qgCode" maxlength="6" autocomplete="off" placeholder="e.g. SPK9QZ" aria-label="Challenge code"><button type="button" id="qgCodeGo">Play it</button></div></div></div>`;
    $1('#qgB').onclick = () => { S('tap'); back(); };
    el.querySelectorAll('[data-band]').forEach(x => x.onclick = () => { S('tap'); band = x.dataset.band; intro(id, o); });
    $1('#qgGo').onclick = () => { S('open'); begin({ game: id, seed: newSeed(), mode: 'solo', players: [{ n: myName(), e: '🙋' }], back: o.back }); };
    const go = () => { const c = parseCode($1('#qgCode').value); if (!c) { T('That code does not look right — it has 6 letters/numbers, like SPK9QZ.'); return; }
      band = c.band; S('open'); begin({ game: c.game, seed: c.seed, mode: 'challenge', players: [{ n: myName(), e: '🙋' }], back: o.back }); };
    $1('#qgCodeGo').onclick = go; $1('#qgCode').onkeydown = e => { if (e.key === 'Enter') go(); };
  }
  const RULES = {
    chillar: `<ul class="qg-tag" style="padding-left:18px;margin:8px 0 0"><li>8 customers · 10 coins + a bonus coin for every second left</li><li>3 right in a row = 🔥 combo bonus</li><li>Wrong or slow? The customer leaves, and you see how to work it out</li></ul>`,
    sixer: `<ul class="qg-tag" style="padding-left:18px;margin:8px 0 0"><li>2 overs, 3 wickets, chase the target</li><li>Right in under 3 s = SIX · under 5 s = FOUR · under 8 s = 2 · slower = 1</li><li>Wrong = OUT, then you learn the trick for that sum</li></ul>`,
    galti: `<ul class="qg-tag" style="padding-left:18px;margin:8px 0 0"><li>5 cases · exactly one line in each has a slip</li><li>Tap it, type the right figure · a wrong tap costs 10 seconds</li><li>Every case ends with the detective’s note</li></ul>`
  };

  function begin(ses) { SES = Object.assign({ pi: 0 }, ses); SES.players.forEach(p => { p.score = null; }); playTurn(); }
  function playTurn() { reseed(SES.seed + ':' + band); ({ chillar: Chillar, sixer: Sixer, galti: Galti })[SES.game].start(); }
  /* called by a game when one player's turn is over */
  function done(score, detail) {
    stop(); rnd = Math.random;
    const p = SES.players[SES.pi]; p.score = score; p.detail = detail;
    const nb = best(SES.game, score);
    XP(Math.max(5, Math.round(score / 20)), `${G(SES.game).n} done!`);
    if (SES.mode === 'family' && SES.pi < SES.players.length - 1) return handoff(detail, nb);
    finale(detail, nb);
  }
  function handoff(detail, nb) {
    const p = SES.players[SES.pi], nx = SES.players[SES.pi + 1], g = G(SES.game), el = screen();
    el.innerHTML = `<div class="qg"><div class="qg-card ${g.hero}" style="text-align:center"><div style="font-size:46px" aria-hidden="true">${p.e}</div>
      <h1 class="qg-h">${E(p.n)}: ${num(p.score)}</h1><p class="qg-tag">${E(detail)}${nb ? ' · 🏆 new best!' : ''}</p>
      <div style="font-size:64px;margin:16px 0 4px" aria-hidden="true">📱➡️${nx.e}</div><p class="qg-tag" style="font-size:18px"><b>Pass the phone to ${E(nx.n)}!</b><br>Same questions, no peeking 🙈</p>
      <button class="qg-btn ${g.btn}" id="qgNext" type="button">I’m ${E(nx.n)} — start ▶</button></div></div>`;
    $1('#qgNext').onclick = () => { S('open'); SES.pi++; playTurn(); }; $1('#qgNext').focus();
  }
  function finale(detail, nb) {
    const g = G(SES.game), el = screen(), code = codeOf(SES.game, band, SES.seed);
    const fam = SES.mode === 'family', sorted = SES.players.slice().sort((a, b) => b.score - a.score), top = sorted[0].score;
    const me = SES.players[0];
    el.innerHTML = `<div class="qg"><div class="qg-card ${g.hero}" style="text-align:center"><div style="font-size:54px" aria-hidden="true">${fam ? '🏆' : g.e}</div>
      ${fam ? `<h1 class="qg-h">Family scoreboard</h1><div class="qg-podium">${sorted.map((p, i) => `<div class="qg-pl${p.score === top ? ' w' : ''}"><span class="s">${p.score === top ? '👑' : ['🥈', '🥉', '🎖️', '🎖️', '🎖️'][i - 1] || '🎖️'}</span><span>${p.e}</span><b style="text-align:left">${E(p.n)}</b><span>${num(p.score)}</span></div>`).join('')}</div>`
        : `<h1 class="qg-h">${num(me.score)}</h1><p class="qg-tag">${E(detail)}${nb ? ' · 🏆 New best!' : ''}</p>`}
      ${LEARN.length ? `<div style="text-align:left;margin-top:10px"><p class="qg-tag"><b>Learn from the missed ones</b></p>${LEARN.slice(0, 6).map(x => `<div class="qg-how" style="background:rgba(255,255,255,.14)">${E(x)}</div>`).join('')}</div>` : ''}
      <div class="qg-sharebox"><div class="qg-tag">${SES.mode === 'challenge' ? 'You played challenge' : 'Challenge a friend with this exact game'}</div><div class="c">${code}</div>
        <div class="qg-tag">They tap ${E(g.n)} → type this code. Same questions — compare scores!</div>
        <button class="qg-btn qg-ghost" id="qgShare" type="button">📤 Send the code</button></div>
      <button class="qg-btn ${g.btn}" id="qgAgain" type="button">Play again ▶</button><button class="qg-btn qg-ghost" id="qgHome" type="button">← Play</button></div></div>`;
    $1('#qgShare').onclick = async () => { const msg = `Beat my ${num(me.score)} in ${g.n} on Knowtopia! Open Play → ${g.n} → type code ${code}`;
      try { if (navigator.share) { await navigator.share({ text: msg }); return; } } catch (e) { return; }
      try { await navigator.clipboard.writeText(msg); T('Code copied — paste it to your friend'); } catch (e) { T('Your code: ' + code); } };
    $1('#qgAgain').onclick = () => { S('open'); const s = { game: SES.game, seed: newSeed(), mode: SES.mode === 'challenge' ? 'solo' : SES.mode, players: SES.players.map(p => ({ n: p.n, e: p.e })), back: SES.back }; begin(s); };
    $1('#qgHome').onclick = () => { S('tap'); back(); };
    S('win');
  }
  let LEARN = [];

  /* ---- family setup: who is playing (one phone) ---- */
  function family(id, bk) {
    stop(); style(); band = band || autoBand();
    const g = G(id), el = screen(), PEOPLE_F = [['🙋', myName()], ['👩', 'Mum'], ['👨', 'Dad'], ['👵', 'Nani'], ['👴', 'Dadu'], ['🧒', 'Sibling']];
    const on = new Set([0, 1]);
    const draw = () => {
      el.innerHTML = `<div class="qg"><button class="back" type="button" id="qgB">← Play</button>
        <div class="qg-card ${g.hero}"><div style="font-size:46px" aria-hidden="true">👨‍👩‍👧 ${g.e}</div><h1 class="qg-h">${E(g.n)} · family</h1>
          <p class="qg-tag">Everyone gets <b>the same questions</b>, one after another on this phone. Highest score wins!</p>
          <p class="qg-tag" style="margin-top:10px"><b>Who is playing?</b></p>
          <div class="qg-chips" role="group" aria-label="Players">${PEOPLE_F.map(([e, n], i) => `<button type="button" class="qg-chip${on.has(i) ? ' on' : ''}" aria-pressed="${on.has(i)}" data-p="${i}" ${i === 0 ? 'disabled' : ''}>${e} ${E(n)}</button>`).join('')}</div>
          <button class="qg-btn ${g.btn}" id="qgGo" type="button">Start · ${on.size} players ▶</button></div></div>`;
      $1('#qgB').onclick = () => { S('tap'); try { (bk || PlayHub.open)(); } catch (e) {} };
      el.querySelectorAll('[data-p]').forEach(x => x.onclick = () => { S('tap'); const i = +x.dataset.p; if (on.has(i)) on.delete(i); else if (on.size < 6) on.add(i); draw(); });
      $1('#qgGo').onclick = () => { if (on.size < 2) { T('Pick at least one more player'); return; } S('open'); begin({ game: id, seed: newSeed(), mode: 'family', players: [...on].sort().map(i => ({ e: PEOPLE_F[i][0], n: PEOPLE_F[i][1] })), back: bk }); };
    };
    draw();
  }
  /* own phones = challenge code (same as friends): make a code now, then play it */
  function challenge(id, bk) {
    stop(); style(); band = band || autoBand();
    const g = G(id), el = screen(), seed = newSeed(), code = codeOf(id, band, seed);
    el.innerHTML = `<div class="qg"><button class="back" type="button" id="qgB">← Play</button>
      <div class="qg-card ${g.hero}" style="text-align:center"><div style="font-size:46px" aria-hidden="true">📲 ${g.e}</div><h1 class="qg-h">Same game, own phones</h1>
        <p class="qg-tag">Share this code. Everyone opens <b>${E(g.n)}</b> on their own phone and types it — same questions for all. Then compare scores!</p>
        <div class="qg-sharebox"><div class="c">${code}</div><button class="qg-btn qg-ghost" id="qgShare" type="button">📤 Send the code</button></div>
        <button class="qg-btn ${g.btn}" id="qgGo" type="button">Play my turn ▶</button>
        <p class="qg-tag" style="margin-top:14px"><b>Got a code from someone?</b></p>
        <div class="qg-code"><input id="qgCode" maxlength="6" autocomplete="off" placeholder="Type their code" aria-label="Challenge code"><button type="button" id="qgCodeGo">Play it</button></div></div></div>`;
    $1('#qgB').onclick = () => { S('tap'); try { (bk || PlayHub.open)(); } catch (e) {} };
    $1('#qgShare').onclick = async () => { const msg = `Let’s play ${g.n} on Knowtopia! Open Play → ${g.n} → type code ${code}`; try { if (navigator.share) { await navigator.share({ text: msg }); return; } } catch (e) { return; } try { await navigator.clipboard.writeText(msg); T('Code copied'); } catch (e) { T('Code: ' + code); } };
    $1('#qgGo').onclick = () => { S('open'); begin({ game: id, seed, mode: 'challenge', players: [{ n: myName(), e: '🙋' }], back: bk }); };
    const go = () => { const c = parseCode($1('#qgCode').value); if (!c) { T('That code does not look right — 6 letters/numbers, like SPK9QZ.'); return; } band = c.band; S('open'); begin({ game: c.game, seed: c.seed, mode: 'challenge', players: [{ n: myName(), e: '🙋' }], back: bk }); };
    $1('#qgCodeGo').onclick = go; $1('#qgCode').onkeydown = e => { if (e.key === 'Enter') go(); };
  }
  const who = () => SES.mode === 'family' ? `<span class="qg-pill">${SES.players[SES.pi].e} ${E(SES.players[SES.pi].n)}</span>` : '';
  const leave = () => `<button class="back" type="button" id="qgB">← Leave</button>`;
  const wireLeave = () => { $1('#qgB').onclick = () => { stop(); S('tap'); back(); }; };

  /* =================================================================
     🪙 CHILLAR CHAMP
     ================================================================= */
  const BZ_MIX = { j: ['total', 'change', 'total', 'change'], m: ['total', 'qty', 'change', 'disc'], s: ['qty', 'change', 'disc', 'gst', 'profit'], p: ['gst', 'discgst', 'cgst', 'profit', 'disc'] };
  const BZ_TIME = { j: 30, m: 28, s: 25, p: 30 }, BZ_N = 8;
  const MOOD = p => p > .66 ? ['😀', '#2fbf71'] : p > .4 ? ['🙂', '#9ccc3d'] : p > .2 ? ['😐', '#ffb21e'] : ['😤', '#e53935'];
  const Chillar = {
    start() {
      LEARN = []; this.i = 0; this.coins = 0; this.right = 0; this.combo = 0; this.used = [];
      this.plan = Array.from({ length: BZ_N }, (_, i) => { const t = TASKS[BZ_MIX[band][i % BZ_MIX[band].length]](); const w = pick(PEOPLE.filter(p => !this.used.includes(p[1]))); this.used.push(w[1]); return { t, w }; });
      this.next();
    },
    next() {
      stop(); if (this.i >= BZ_N) return done(this.coins, `${this.right} of ${BZ_N} customers served right`);
      const { t, w } = this.plan[this.i], lim = BZ_TIME[band] * 10; let left = lim, fin = false;
      const el = screen();
      el.innerHTML = `<div class="qg">${leave()}<div class="cc-wrap" id="ccW"><div class="cc-awn" aria-hidden="true"></div><div class="cc-sign">🪙 CHILLAR CHAMP</div>
        <div class="qg-top">${who()}<span class="qg-pill">👤 ${this.i + 1}/${BZ_N}</span>${this.combo >= 3 ? `<span class="qg-pill combo">🔥 combo ×${this.combo}</span>` : ''}<span class="qg-sp"></span></div>
        <div class="cc-jar" id="ccJar"><span aria-hidden="true">🫙</span>${num(this.coins)}</div>
        <div class="cc-shelf" aria-hidden="true">${shuffle(SHOP).slice(0, 6).map(x => x[0]).join('')}</div>
        <div class="cc-stage"><div class="cc-cust" aria-hidden="true"><div class="cc-ring" id="ccRing"></div><div class="cc-face">${w[0]}</div><div class="cc-mood" id="ccMood">😀</div></div>
          <div class="cc-say"><small>${E(w[1])} ${t.e}</small>${t.say}</div></div>
        <div class="cc-counter"><p class="cc-q">${E(t.q)}</p><div class="qg-disp" aria-live="polite"></div><div class="qg-fb" id="ccFb" aria-live="assertive"></div><div id="ccHow"></div><div class="qg-keys"></div></div></div></div>`;
      wireLeave();
      const wrap = $1('#ccW'), cnt = $1('.cc-counter', el);
      const fb = (ok, given) => { if (fin) return; fin = true; stop(); kp.off();
        const secs = Math.ceil(left / 10); let gain = 0;
        if (ok) { this.right++; this.combo++; gain = 10 + secs + (this.combo >= 3 ? 5 : 0); this.coins += gain; coins(wrap, 8); floatAt(wrap, `+${gain}`, '#0f7a3c'); const j = $1('#ccJar'); j.innerHTML = `<span aria-hidden="true">🫙</span>${num(this.coins)}`; j.classList.add('bump'); $1('#ccMood').textContent = '🤩'; }
        else { this.combo = 0; LEARN.push(`${t.q} → ${num(t.a)}. ${t.w}`); $1('#ccMood').textContent = '😠'; $1('.cc-cust', el).style.transform = 'translateX(140px) rotate(10deg)'; $1('.cc-cust', el).style.transition = 'transform .6s ease-in'; }
        const f = $1('#ccFb'); f.className = 'qg-fb ' + (ok ? 'good' : 'bad');
        f.textContent = ok ? `✅ ${cos(['Happy customer!', 'Shabash!', 'Paisa vasool!', 'Lightning fast!', 'Perfect change!'])} +${gain}${this.combo >= 3 ? ' (🔥 combo +5)' : ''}` : given == null ? `⏰ Too slow — answer: ${num(t.a)}` : `❌ Oops — answer: ${num(t.a)}`;
        $1('#ccHow').innerHTML = `<div class="qg-how"><b>How:</b> ${E(t.w)}</div><button class="qg-btn cc-btn" id="ccN" type="button">${this.i + 1 >= BZ_N ? 'Close the shop ▶' : 'Next customer ▶'}</button>`;
        S(ok ? 'good' : 'bad'); this.i++; const n = $1('#ccN'); n.onclick = () => { S('tap'); this.next(); }; n.focus(); };
      const kp = keypad(cnt, 'k-till', v => fb(v === t.a, v));
      timer = setInterval(() => { left--; const r = $1('#ccRing'); if (!r) { stop(); return; } const p = left / lim, [m, c] = MOOD(p); r.style.setProperty('--p', p); r.style.setProperty('--c', c); const mo = $1('#ccMood'); if (mo && mo.textContent !== m) mo.textContent = m; if (left <= 0) fb(false, null); }, 100);
    }
  };

  /* =================================================================
     🏏 SIXER SUMS
     ================================================================= */
  const COMM = { 6: ['Into the stands! SIX!', 'Out of the stadium!', 'That ball is still flying!'], 4: ['Cracking shot — FOUR!', 'Races away to the boundary!', 'Threaded the gap!'],
    2: ['Good running — two runs.', 'They come back for the second!'], 1: ['Quick single.', 'Nudged for one.'], 0: ['Dot ball — too slow!', 'Beaten for pace.'], w: ['OUT! Clean bowled!', 'Caught at mid-off!', 'Stumped! Gone!'] };
  const Sixer = {
    start() { LEARN = []; this.target = R(32, 46) + (band === 'p' ? -4 : 0); this.qs = Array.from({ length: 12 }, () => pick(CQ[band])()); this.runs = 0; this.wk = 0; this.ball = 0; this.dots = []; this.next(); },
    next() {
      stop();
      if (this.runs >= this.target || this.wk >= 3 || this.ball >= 12) return this.end();
      const g = this.qs[this.ball], lim = 150; let left = lim, fin = false; const t0 = Date.now();
      const need = this.target - this.runs, bl = 12 - this.ball, el = screen();
      el.innerHTML = `<div class="qg">${leave()}<div class="ss-wrap" id="ssW"><div class="ss-crowd" aria-hidden="true"></div>
        <div class="qg-top" style="margin-top:6px">${who()}<span class="qg-sp"></span><span class="qg-pill">🎯 Target ${this.target}</span></div>
        <div class="ss-board" role="group" aria-label="Scoreboard"><div><small>RUNS/WKTS</small><b>${this.runs}/${this.wk}</b></div><div><small>OVERS</small><b>${Math.floor(this.ball / 6)}.${this.ball % 6}</b></div><div><small>NEED</small><b>${need}</b><small>off ${bl}</small></div></div>
        <div class="ss-field" id="ssF" aria-hidden="true"><div class="ss-pitch"></div><div class="ss-stumps"><i></i><i></i><i></i></div><div class="ss-bat">🏏</div><div class="ss-ball"></div></div>
        <div class="ss-stamp" id="ssStamp" aria-hidden="true"></div>
        <div class="ss-dots" aria-label="Ball by ball">${Array.from({ length: 12 }, (_, i) => { const d = this.dots[i]; return `<span class="ss-dot${d === 'W' ? ' w' : d === 6 ? ' r6' : d === 4 ? ' r4' : ''}${i === this.ball ? ' now' : ''}">${d == null ? '' : d === 0 ? '•' : d}</span>`; }).join('')}</div>
        <div class="ss-q"><div class="ss-tick"><i id="ssT" style="width:100%"></i></div><p class="ss-qt">${E(g.q)} = ?</p><div class="qg-disp" aria-live="polite"></div>
          <div class="ss-comm" id="ssC" aria-live="assertive"></div><div id="ssHow"></div><div class="qg-keys"></div></div></div></div>`;
      wireLeave();
      const wrap = $1('#ssW'), fld = $1('#ssF'), st = $1('#ssStamp');
      const fb = v => { if (fin) return; fin = true; stop(); kp.off();
        const s = (Date.now() - t0) / 1000; let r;
        if (v == null) r = 0; else if (v !== g.a) r = 'W'; else r = s < 3 ? 6 : s < 5 ? 4 : s < 8 ? 2 : 1;
        this.dots.push(r); this.ball++;
        if (r === 'W') { this.wk++; LEARN.push(`${g.q} = ${num(g.a)}. ${g.tip}`); fld.classList.add('out'); st.textContent = 'OUT!'; st.className = 'ss-stamp out go'; S('bad'); }
        else { this.runs += r; if (r) fld.classList.add('hit' + (r === 6 ? 6 : r === 4 ? 4 : 2)); if (r >= 4) { st.textContent = r === 6 ? 'SIX!' : 'FOUR!'; st.className = 'ss-stamp go ' + (r === 6 ? 'six' : 'four'); wrap.classList.add('wave'); } S(r ? 'good' : 'tap'); }
        $1('#ssC').textContent = cos(COMM[r === 'W' ? 'w' : r]) + (r === 'W' ? ` The answer was ${num(g.a)}.` : '');
        const over = this.runs >= this.target || this.wk >= 3 || this.ball >= 12;
        $1('#ssHow').innerHTML = `${r === 'W' || r === 0 ? `<div class="qg-how"><b>Quick trick:</b> ${E(g.tip)}</div>` : ''}<button class="qg-btn ss-btn" id="ssN" type="button">${over ? 'See the result ▶' : 'Next ball ▶'}</button>`;
        const n = $1('#ssN'); n.onclick = () => { S('tap'); this.next(); }; n.focus();
        if (r !== 'W' && r !== 0 && !over) setTimeout(() => { if (n.isConnected) this.next(); }, 1500);
      };
      const kp = keypad($1('.ss-q', el), 'k-led', v => fb(v));
      timer = setInterval(() => { left--; const b = $1('#ssT'); if (!b) { stop(); return; } b.style.width = (left / lim * 100) + '%'; if (left <= 0) fb(null); }, 100);
    },
    end() { const won = this.runs >= this.target, score = this.runs * 10 + (won ? (3 - this.wk) * 20 + (12 - this.ball) * 10 : 0);
      const res = won ? `Won by ${3 - this.wk} wicket${3 - this.wk === 1 ? '' : 's'} with ${12 - this.ball} ball${12 - this.ball === 1 ? '' : 's'} to spare 🏆` : this.target - this.runs - 1 === 0 ? 'Match tied 🤝' : `Lost by ${this.target - this.runs - 1} run${this.target - this.runs - 1 === 1 ? '' : 's'}`;
      done(score, `${this.runs}/${this.wk} chasing ${this.target} · ${res}`); }
  };

  /* =================================================================
     🔎 GALTI PAKDO
     ================================================================= */
  const AD_N = 5, AD_T = { j: 90, m: 75, s: 60, p: 60 };
  const Galti = {
    start() { LEARN = []; const kinds = band === 'p' ? ['tax', 'bank', 'tax', 'bank', 'tax'] : band === 's' ? ['bill', 'bank', 'tax', 'bill', 'bank'] : ['bill'];
      this.docs = Array.from({ length: AD_N }, (_, i) => DOCS[kinds[i % kinds.length]]()); this.i = 0; this.stars = 0; this.solved = 0; this.next(); },
    next() {
      stop(); if (this.i >= AD_N) { const rank = this.stars >= 13 ? 'Chief Detective 🕵️' : this.stars >= 9 ? 'Inspector 🔎' : this.stars >= 5 ? 'Sub-Inspector 📋' : 'Cadet 📎';
        return done(this.stars * 20 + this.solved * 10, `${this.solved} of ${AD_N} cases solved · ⭐ ${this.stars}/${AD_N * 3} · Rank: ${rank}`); }
      const doc = this.docs[this.i], lim = AD_T[band] * 10; let left = lim, fin = false, sel = -1, kp = null;
      const el = screen();
      el.innerHTML = `<div class="qg">${leave()}<div class="gp-wrap" id="gpW"><div class="gp-lamp" aria-hidden="true"></div>
        <div class="qg-top">${who()}<span class="qg-pill">📁 Case ${this.i + 1}/${AD_N}</span><span class="qg-pill">⭐ ${this.stars}</span><span class="qg-sp"></span><span class="qg-pill" id="gpS">⏳ ${AD_T[band]}s</span></div>
        <div class="gp-sand" id="gpSand" aria-hidden="true"><i style="width:100%"></i></div>
        <div class="gp-file" data-tab="CASE FILE #${this.i + 1}"><div class="gp-doc"><h4>${E(doc.title)}</h4><div class="m">${E(doc.meta)}</div>
          ${doc.rows.map((r, i) => `<button type="button" class="gp-row${r.tot ? ' tot' : ''}" data-r="${i}" aria-label="${E(r.l.trim())}: ${E(num(r.v))}"><span>${E(r.l)}</span><span class="v">${E(num(r.v))}</span></button>`).join('')}
          <div class="gp-stamp" id="gpStamp" aria-hidden="true">CASE CLOSED</div></div></div>
        <p class="gp-hint" id="gpH" aria-live="polite">🔎 Tap the line with the slip.</p>
        <div class="gp-fix" id="gpFix" hidden><b>What should it be?</b><div class="qg-disp" aria-live="polite"></div><div class="qg-keys"></div></div>
        <div class="qg-fb" id="gpFb" aria-live="assertive"></div><div id="gpOut"></div></div></div>`;
      wireLeave();
      const close = ok => { if (fin) return; fin = true; stop(); if (kp) kp.off();
        const fr = left / lim, st = ok ? (fr > .5 ? 3 : fr > .2 ? 2 : 1) : 0; this.stars += st; if (ok) this.solved++; else LEARN.push(doc.why);
        el.querySelectorAll('.gp-row').forEach(b => b.disabled = true);
        const er = $1(`[data-r="${doc.ei}"]`, el); er.classList.add('circ', 'fix'); $1('.v', er).setAttribute('data-was', num(doc.rows[doc.ei].v)); $1('.v', er).textContent = num(doc.correct);
        $1('#gpFix').hidden = true; const sp = $1('#gpStamp'); sp.textContent = ok ? 'CASE CLOSED' : 'CASE MISSED'; sp.classList.add('go');
        const f = $1('#gpFb'); f.style.color = ok ? '#b9f6ca' : '#ffcdd2'; f.textContent = ok ? `✅ Solved! ${'⭐'.repeat(st)}` : left <= 0 ? '⏳ Time up — here is the slip.' : '❌ Here is the slip.';
        $1('#gpOut').innerHTML = `<div class="qg-how"><b>🕵️ Detective’s note:</b> ${E(doc.why)}</div><button class="qg-btn gp-btn" id="gpN" type="button">${this.i + 1 >= AD_N ? 'File the report ▶' : 'Next case ▶'}</button>`;
        S(ok ? 'good' : 'bad'); this.i++; const n = $1('#gpN'); n.onclick = () => { S('tap'); this.next(); }; n.focus(); };
      el.querySelectorAll('.gp-row').forEach(b => b.onclick = () => { if (fin) return; const i = +b.dataset.r;
        if (i !== doc.ei) { S('bad'); b.classList.remove('miss'); void b.offsetWidth; b.classList.add('miss'); left = Math.max(0, left - 100); $1('#gpH').textContent = '🙅 That line checks out. −10 seconds.'; return; }
        if (sel === i) return; sel = i; S('good'); b.classList.add('circ'); $1('#gpH').textContent = '🎯 Caught it! Now type the correct figure.'; $1('#gpFix').hidden = false;
        kp = keypad($1('#gpFix'), 'k-ink', v => { if (v === doc.correct) close(true); else { S('bad'); const f = $1('#gpFb'); f.style.color = '#ffcdd2'; f.textContent = 'Not that figure — check the working. −5 seconds.'; left = Math.max(0, left - 50); kp.clear(); } }); });
      timer = setInterval(() => { left--; const b = $1('#gpSand'); if (!b) { stop(); return; } b.firstChild.style.width = (left / lim * 100) + '%'; b.classList.toggle('low', left < lim * .25); $1('#gpS').textContent = '⏳ ' + Math.ceil(left / 10) + 's'; if (left <= 0) close(false); }, 100);
    }
  };

  function open(id, o) { if (!visible()) { T('Coming soon!'); return; } intro(id, o); }
  window.QuickGames = { visible, live: LIVE, GAMES, open, family: (id, b) => visible() && family(id, b), challenge: (id, b) => visible() && challenge(id, b), parseCode,
    _test: { TASKS, CQ, DOCS, setBand: b => { band = b; }, reseed, codeOf } };
})();
