/* Knowtopia — "Leave the game?" pop-up for every puzzle and game (js/leave.js).
   A running game calls LeaveGuard.arm({ name, root, save, discard, leave, note }):
     save()    — keep the game so the student can come back and finish it (puzzles: saved on this device; arcade:
                 kept until the app is closed). Leave it out when a game cannot be saved (game rooms).
     discard() — throw the saved state away ("Leave without saving").
     leave()   — the game's own exit (what its ← button does).
   While armed, the phone's Back button, the game's ← button (LeaveGuard.ask()) and the main menu all show the pop-up:
     💾 Save & leave · 🚪 Leave without saving · ▶ Keep playing   (rooms: 🚪 Leave · ▶ Keep playing).
   LeaveGuard.disarm() when the game ends (results screen). Back works through one history entry of our own, so the
   app's own Back router (js/app.js Nav) never sees a Back press the pop-up has caught. */
(function () {
  'use strict';
  const D = document;
  let cur = null, pushed = false, ign = null, pop = null;
  const E = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const alive = () => !!(cur && (!cur.root || cur.root.isConnected));
  const pushMine = () => { try { history.pushState(Object.assign({}, history.state || {}, { svGame: 1 }), ''); pushed = true; } catch (e) {} };

  /* our Back entry is added a moment later, after the app's own navigation to the game has settled */
  let pt = 0;
  function arm(o) { cur = o; clearTimeout(pt); pt = setTimeout(() => { if (cur === o && alive() && !pushed) pushMine(); }, 400); }
  /* stop guarding; then() runs after our history entry is gone (so the next screen's history goes on top of it) */
  function disarm(then, soft) {
    cur = null; close(); clearTimeout(pt);
    if (soft) { if (pushed && history.state && history.state.svGame) { try { const s2 = Object.assign({}, history.state); delete s2.svGame; history.replaceState(s2, ''); } catch (e) {} } pushed = false; if (then) then(); return; }
    if (pushed && history.state && history.state.svGame) { pushed = false; ign = then || (() => {}); try { history.back(); } catch (e) { const f = ign; ign = null; f(); } return; }
    pushed = false; if (then) then();
  }
  function close() { if (pop) { const p = pop; pop = null; p.classList.remove('show'); setTimeout(() => p.remove(), 200); } }

  /* the pop-up; go = what "leave" does (the game's own exit, or the menu button that was tapped) */
  function ask(go) {
    if (!alive()) { const o = cur; cur = null; if (go) go(); else if (o && o.leave) o.leave(); return; }
    if (pop) return;
    const o = cur, canSave = typeof o.save === 'function';
    css();
    pop = D.createElement('div'); pop.className = 'lg-wrap show'; pop.setAttribute('role', 'alertdialog'); pop.setAttribute('aria-modal', 'true'); pop.setAttribute('aria-labelledby', 'lgT');
    pop.innerHTML = `<div class="lg-box"><div class="lg-e" aria-hidden="true">${canSave ? '💾' : '🚪'}</div><h3 id="lgT">Leave ${E(o.name || 'the game')}?</h3>
      <p class="lg-sub">${E(o.note || (canSave ? 'Save it and come back any time to finish — you can read your lessons in between.' : 'You will leave this game.'))}</p>
      ${canSave ? '<button class="btn mint" type="button" data-lg="save">💾 Save & leave</button>' : ''}
      <button class="btn ${canSave ? 'ghost' : 'mint'}" type="button" data-lg="drop">🚪 ${canSave ? 'Leave without saving' : 'Leave'}</button>
      <button class="btn ghost" type="button" data-lg="stay">▶ Keep playing</button></div>`;
    D.body.appendChild(pop);
    const exit = () => (go || o.leave || (() => {}));
    pop.querySelector('[data-lg="stay"]').onclick = () => close();
    pop.querySelector('[data-lg="drop"]').onclick = () => { try { o.discard && o.discard(); } catch (e) {} disarm(exit()); };
    const sv = pop.querySelector('[data-lg="save"]');
    if (sv) sv.onclick = () => { try { o.save(); } catch (e) { console.warn('save', e); } try { window.toast && toast('💾 Saved — come back any time to finish'); } catch (e) {} disarm(exit()); };
    pop.addEventListener('click', e => { if (e.target === pop) close(); });
    pop.addEventListener('keydown', e => { if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); close(); } });
    setTimeout(() => { const b = pop && pop.querySelector('[data-lg="stay"]'); if (b) try { b.focus(); } catch (e) {} }, 40);
  }

  /* the phone's Back button */
  window.addEventListener('popstate', e => {
    if (ign) { e.stopImmediatePropagation(); const f = ign; ign = null; try { f(); } catch (x) { console.warn(x); } return; }
    if (!pushed) return;
    if (e.state && e.state.svGame) return;                 // back from a sheet opened on top of the game: the app closes it
    pushed = false;
    if (!alive()) { cur = null; e.stopImmediatePropagation(); try { history.back(); } catch (x) {} return; }   // the game is already gone: one normal Back
    e.stopImmediatePropagation();
    pushMine();
    if (pop) { close(); return; }                          // Back while the pop-up is open = keep playing
    if (D.querySelector('.sheet.show,.asksheet.show')) return;
    ask();
  }, true);
  /* the main menu (bottom bar / sidebar) while a game is running */
  D.addEventListener('click', e => {
    if (!cur || pop) return;
    const b = e.target.closest && e.target.closest('nav button, .dsk-ql button, .dsk-rc, .dsk-brand, [data-s].nav-b');
    if (!b || (cur.root && cur.root.contains(b))) return;
    if (!alive()) { cur = null; return; }
    e.preventDefault(); e.stopImmediatePropagation();
    ask(() => b.click());
  }, true);

  function css() {
    if (D.getElementById('lgCss')) return;
    const c = D.createElement('style'); c.id = 'lgCss';
    c.textContent = `.lg-wrap{position:fixed;inset:0;z-index:9500;background:rgba(10,12,30,.55);display:flex;align-items:center;justify-content:center;padding:18px}
.lg-box{background:var(--card,#fff);color:var(--ink,#1d1f3a);border-radius:22px;padding:20px 18px 16px;max-width:360px;width:100%;text-align:center;box-shadow:0 18px 50px rgba(0,0,0,.35);animation:lgIn .18s ease-out}
.lg-box h3{margin:4px 0 6px;font-size:20px}.lg-e{font-size:40px;line-height:1}.lg-sub{margin:0 0 14px;font-size:14px;color:var(--muted,#5f6485);line-height:1.4}
.lg-box .btn{width:100%;margin-top:8px}
@keyframes lgIn{from{transform:scale(.92);opacity:0}to{transform:none;opacity:1}}
@media (prefers-reduced-motion:reduce){.lg-box{animation:none}}`;
    D.head.appendChild(c);
  }

  window.LeaveGuard = { arm, disarm, ask, get armed() { return !!cur; } };
})();
