/* ================= Sheets: swipe down to close (js/sheets.js) =================
   Works for every bottom sheet in the app — .sheet with a .sheet-in panel (sound, Aa font size, ⭐ stars, 🔥 streak,
   plans, sign-in and other Cloud.sheet() popups, notes, install, 3D lab…) and .asksheet with an .ask-in panel.
   - Drag down on the top area (the grab handle, or the top 32 px of the panel) — or anywhere on the panel when its
     content is scrolled to the top. The panel follows the finger; past 80 px or a fast flick it closes, otherwise it
     springs back. Horizontal swipes and upward drags are ignored (they scroll as usual).
   - Tap on the dim backdrop closes the sheet (a tap that started inside the panel never does).
   - Escape closes the top sheet (js/a11y.js closeTop; handled here only if a11y.js is missing).
   - Forms are safe: while a text box inside the sheet is focused, only the grab handle drags, and a backdrop tap just
     closes the keyboard. Sliders, the 3D lab, canvases and [data-noswipe] areas never start a drag.
   - Sheets that must stay open ignore all of this: [data-pinned] (Parent Home), [data-noclose] (Cloud.sheet(…, false):
     new-password form, "which progress to keep"), the sign-in gate (#svGate is not a sheet), and full-screen
     sheets without a panel (Parent Hub page, photo viewer).
   Closing uses the sheet's own close / done / cancel button when it has one (so notes save, history entries go away),
   otherwise it removes .show. */
(function () {
  'use strict';
  const D = document;
  const OPEN = '.sheet.show,.asksheet.show', PANEL = '.sheet-in,.ask-in';
  const reduced = () => { try { return matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } };
  const isOpen = s => !!(s && s.isConnected && s.classList.contains('show'));
  const locked = s => s.hasAttribute('data-pinned') || s.hasAttribute('data-noclose') || s.id === 'svGate' || s.classList.contains('pv-hub') || s.classList.contains('ca-phview');
  const panelOf = s => s && [...s.children].find(c => c.matches && c.matches(PANEL));
  const typing = a => !!a && ((/^(input|textarea|select)$/i.test(a.tagName) && !/^(range|checkbox|radio|button|submit|reset|file|color)$/i.test(a.type || '')) || a.isContentEditable);
  const CLOSERS = '[data-close],.ask-x,#rvX,#uxDone,#clX,#caNoteX,#insHowX,[data-stx],#plX';
  const CLOSE_TXT = /^(✕|×|close|done|got it|cancel|no thanks|not now|maybe later|ok|okay)$/i;
  function closeSheet(s) {
    if (s.id === 'soundSheet' && typeof window.closeSound === 'function') return window.closeSound();
    if (s.id === 'sheet3d' && typeof window.close3D === 'function') return window.close3D();
    const btns = [...s.querySelectorAll('button')].filter(b => !b.disabled && b.offsetParent !== null);
    const b = btns.find(x => x.matches(CLOSERS)) || btns.find(x => CLOSE_TXT.test(x.textContent.trim()) || /^close\b/i.test(x.getAttribute('aria-label') || ''));
    if (b) b.click(); else s.classList.remove('show');
  }
  const reset = p => { p.style.transition = ''; p.style.transform = ''; };

  /* ---------- drag ---------- */
  let g = null, suppressUntil = 0;
  function canStart(s, p, target, y) {
    if (!isOpen(s) || locked(s) || !p.contains(target)) return false;
    const grab = !!target.closest('.sheet-grab') || y - p.getBoundingClientRect().top < 32;
    const a = D.activeElement;
    if (typing(a) && s.contains(a) && !grab) return false;                      // never close while typing
    if (target.closest('input,textarea,select,[contenteditable="true"],canvas,.s3dhost,.lab-box,[data-noswipe]') && !target.closest('.sheet-grab')) return false;
    if (!grab) for (let el = target; el && el !== s; el = el.parentElement) if (el.scrollTop > 0) return false;   // content not at the top: let it scroll
    return true;
  }
  function begin(s, x, y, kind) {
    const p = panelOf(s); g = { s, p, x0: x, y0: y, t0: Date.now(), dy: 0, mode: 'pending', kind, lastY: y, lastT: Date.now(), v: 0 };
  }
  function move(x, y, e) {
    if (!g) return;
    const dx = x - g.x0, dy = y - g.y0;
    if (g.mode === 'pending') {
      if (dy > 0 && dy >= Math.abs(dx) && e && e.cancelable) e.preventDefault();   // stop the page behind from scrolling
      if (Math.abs(dx) < 8 && Math.abs(dy) < 8) return;
      if (Math.abs(dx) > Math.abs(dy) || dy < 0) { g = null; return; }           // sideways or upward: not ours
      g.mode = 'drag'; g.p.style.transition = 'none'; g.s.classList.add('sv-dragging');
    }
    if (e && e.cancelable) e.preventDefault();
    const now = Date.now(), d = Math.max(0, y - g.y0);
    g.v = (y - g.lastY) / Math.max(1, now - g.lastT); g.lastY = y; g.lastT = now; g.dy = d;
    g.p.style.transform = `translateY(${d}px)`;
  }
  function end(cancel) {
    if (!g) return; const G = g; g = null;
    if (G.mode !== 'drag') return;
    G.s.classList.remove('sv-dragging'); suppressUntil = Date.now() + 400;
    const flick = G.dy > 24 && (G.v > 0.5 || (Date.now() - G.t0 < 300 && G.dy > 40));   // a quick short swipe also closes
    if (!cancel && (G.dy > 80 || flick)) dismiss(G.s, G.p); else spring(G.p);
  }
  function spring(p) {
    if (reduced()) return reset(p);
    p.style.transition = 'transform .26s cubic-bezier(.2,.9,.3,1.15)'; p.style.transform = 'translateY(0)';
    setTimeout(() => { if (!g || g.p !== p) reset(p); }, 300);
  }
  function dismiss(s, p) {
    const ms = reduced() ? 0 : 180;
    p.style.transition = ms ? `transform ${ms}ms ease-in` : 'none'; p.style.transform = `translateY(${p.offsetHeight + 40}px)`;
    setTimeout(() => {
      closeSheet(s);
      setTimeout(() => { if (isOpen(s)) spring(p); else reset(p); }, 700);   // a sheet that refused to close comes back
    }, ms);
    try { if (navigator.vibrate && navigator.userActivation && navigator.userActivation.hasBeenActive) navigator.vibrate(8); } catch (e) {}
  }
  const sheetAt = t => (t && t.closest ? t.closest(OPEN) : null);
  D.addEventListener('touchstart', e => {
    if (e.touches.length !== 1) { if (g) end(true); return; }
    const s = sheetAt(e.target), t = e.touches[0]; if (!s) return;
    const p = panelOf(s); if (!p || !canStart(s, p, e.target, t.clientY)) return;
    begin(s, t.clientX, t.clientY, 'touch');
  }, { passive: true, capture: true });
  D.addEventListener('touchmove', e => { if (g && g.kind === 'touch' && e.touches.length === 1) move(e.touches[0].clientX, e.touches[0].clientY, e); }, { passive: false, capture: true });
  D.addEventListener('touchend', () => { if (g && g.kind === 'touch') end(false); }, true);
  D.addEventListener('touchcancel', () => { if (g && g.kind === 'touch') end(true); }, true);
  /* mouse and pen (touch is handled by the touch events above) */
  D.addEventListener('pointerdown', e => {
    downOn = e.target; const a = D.activeElement; typedAtDown = typing(a) ? a : null;   // the tap moves focus away before 'click'
    if (e.pointerType === 'touch' || e.button !== 0) return;
    const s = sheetAt(e.target); if (!s) return; const p = panelOf(s); if (!p || !canStart(s, p, e.target, e.clientY)) return;
    begin(s, e.clientX, e.clientY, 'ptr');
  }, true);
  window.addEventListener('pointermove', e => { if (g && g.kind === 'ptr') move(e.clientX, e.clientY, e); }, true);
  window.addEventListener('pointerup', () => { if (g && g.kind === 'ptr') end(false); }, true);
  window.addEventListener('pointercancel', () => { if (g && g.kind === 'ptr') end(true); }, true);

  /* ---------- backdrop tap ---------- */
  let downOn = null, typedAtDown = null;
  D.addEventListener('click', e => {
    if (e.isTrusted && Date.now() < suppressUntil) { suppressUntil = 0; e.stopPropagation(); e.preventDefault(); return; }   // the real click that ends a drag (not our own close-button click)
    const s = e.target; if (!s || !s.matches || !s.matches(OPEN) || !panelOf(s)) return;
    if (downOn !== s) return;                                   // started inside the panel (text selection etc.)
    e.stopImmediatePropagation(); e.preventDefault();           // this module is the only backdrop handler: no double close
    if (locked(s)) return;
    const a = typedAtDown && typedAtDown.isConnected ? typedAtDown : D.activeElement; typedAtDown = null;
    if (typing(a) && s.contains(a)) { if (D.activeElement === a) a.blur(); return; }   // first tap just closes the keyboard
    closeSheet(s);
  }, true);

  /* ---------- Escape (js/a11y.js does this when it is loaded) ---------- */
  D.addEventListener('keydown', e => {
    if (e.key !== 'Escape' || window.A11Y || e.defaultPrevented) return;
    const l = [...D.querySelectorAll(OPEN)].filter(s => panelOf(s)); const s = l[l.length - 1];
    if (s && !locked(s)) { e.preventDefault(); closeSheet(s); }
  });

  /* ---------- a visible grab handle on every closable sheet ---------- */
  function grabs() {
    D.querySelectorAll(OPEN).forEach(s => { const p = panelOf(s); if (!p || locked(s) || p.querySelector(':scope > .sheet-grab')) return;
      const h = D.createElement('div'); h.className = 'sheet-grab sv-grabx'; h.setAttribute('aria-hidden', 'true'); p.insertBefore(h, p.firstChild); });
  }
  let gt = 0;
  new MutationObserver(() => { if (!gt) gt = requestAnimationFrame(() => { gt = 0; grabs(); }); }).observe(D.documentElement, { subtree: true, attributes: true, attributeFilter: ['class'], childList: true });

  const css = D.createElement('style'); css.id = 'svSheetsCss';
  css.textContent = `.sheet-grab{position:relative;cursor:grab;touch-action:none}
.sheet-grab::after{content:'';position:absolute;left:-40px;right:-40px;top:-12px;bottom:-12px}
.sv-dragging .sheet-grab{cursor:grabbing}.sv-dragging .sheet-in,.sv-dragging .ask-in{user-select:none;-webkit-user-select:none}
.sheet[data-noclose] .sheet-grab,.sheet[data-pinned] .sheet-grab{visibility:hidden}
.ask-in{position:relative}.ask-in>.sv-grabx{position:absolute;top:5px;left:50%;margin:0;transform:translateX(-50%);z-index:2}
.sheet-in,.ask-in{overscroll-behavior:contain}`;
  D.head.appendChild(css);
  window.SheetSwipe = { close: closeSheet, locked };
})();
