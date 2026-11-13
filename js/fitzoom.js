/* FitZoom — any diagram (an <svg viewBox>) whose drawing spills past its frame gets, automatically:
   thin scroll bars to reach the hidden part, and three small buttons (− ⤢ +) to zoom in, fit everything, zoom out.
   The svg keeps its own viewBox and on-screen box, so taps inside labs still map to the right point.
   Opt out with data-nozoom on the svg. */
(function () {
  const MIN_W = 150, SLACK = 0.03, CAP = 1;   // ignore icons; tolerate 3% spill; extend at most one frame each side
  const st = new WeakMap(), SCOPE = '.jx, .lab-box';   // JEE labs and figures, school concept labs
  function vb(svg) { const v = svg.viewBox && svg.viewBox.baseVal; return v && v.width && v.height ? { x: v.x, y: v.y, w: v.width, h: v.height } : null; }
  function spill(svg, V) {
    let b; try { b = svg.getBBox(); } catch (e) { return null; }
    if (!b || !(b.width || b.height)) return null;
    const L = Math.min(Math.max(0, V.x - b.x), V.w * CAP), T = Math.min(Math.max(0, V.y - b.y), V.h * CAP);
    const R = Math.min(Math.max(0, b.x + b.width - V.x - V.w), V.w * CAP), B = Math.min(Math.max(0, b.y + b.height - V.y - V.h), V.h * CAP);
    const big = Math.max(L / V.w, R / V.w, T / V.h, B / V.h) > SLACK; return { L, T, R, B, big };
  }
  function wrap(svg, V) {
    const box = svg.getBoundingClientRect(), base = box.width, s0 = base / V.w;
    const w = document.createElement('div'); w.className = 'fz';
    w.innerHTML = '<div class="fz-sc"><div class="fz-in"></div></div><div class="fz-ctl" hidden><button type="button" data-z="-" aria-label="Zoom out">−</button><button type="button" data-z="fit" aria-label="Show everything">⤢</button><button type="button" data-z="+" aria-label="Zoom in">+</button></div>';
    const cs = getComputedStyle(svg); w.style.maxWidth = base + 'px'; w.style.margin = cs.margin === '0px' ? '' : cs.margin;
    svg.parentNode.insertBefore(w, svg); w.querySelector('.fz-in').appendChild(svg);
    const S = { w, sc: w.querySelector('.fz-sc'), inn: w.querySelector('.fz-in'), ctl: w.querySelector('.fz-ctl'), V, s0, z: 1, ext: { L: 0, T: 0, R: 0, B: 0 }, bg: cs.backgroundColor, rad: cs.borderRadius, orig: svg.getAttribute('style') || '' };
    S.sc.style.height = (V.h * s0) + 'px'; S.sc.style.borderRadius = S.rad; S.inn.style.background = S.bg;
    svg.style.position = 'absolute'; svg.style.overflow = 'visible'; svg.style.maxWidth = 'none'; svg.style.margin = '0'; svg.style.borderRadius = '0';
    S.ctl.addEventListener('click', e => { const k = e.target.closest('[data-z]'); if (!k) return; e.stopPropagation(); zoom(svg, S, k.dataset.z); });
    st.set(svg, S); return S;
  }
  function lay(svg, S, keepCentre) {
    const { V, ext } = S, s = S.s0 * S.z, sc = S.sc;
    const cx = keepCentre ? (sc.scrollLeft + sc.clientWidth / 2) / (sc.scrollWidth || 1) : null, cy = keepCentre ? (sc.scrollTop + sc.clientHeight / 2) / (sc.scrollHeight || 1) : null;
    S.inn.style.width = ((V.w + ext.L + ext.R) * s) + 'px'; S.inn.style.height = ((V.h + ext.T + ext.B) * s) + 'px';
    svg.style.left = (ext.L * s) + 'px'; svg.style.top = (ext.T * s) + 'px'; svg.style.width = (V.w * s) + 'px'; svg.style.height = (V.h * s) + 'px';
    if (keepCentre) { sc.scrollLeft = cx * sc.scrollWidth - sc.clientWidth / 2; sc.scrollTop = cy * sc.scrollHeight - sc.clientHeight / 2; }
  }
  function zoom(svg, S, how) {
    const { V, ext } = S;
    if (how === 'fit') { S.z = Math.min(V.w / (V.w + ext.L + ext.R), V.h / (V.h + ext.T + ext.B)); lay(svg, S); S.sc.scrollLeft = S.sc.scrollTop = 0; return; }
    const lo = Math.min(1, V.w / (V.w + ext.L + ext.R), V.h / (V.h + ext.T + ext.B)) * 0.999;
    S.z = Math.max(lo, Math.min(4, S.z * (how === '+' ? 1.25 : 0.8))); lay(svg, S, true);
  }
  function look(svg) {
    if (svg.hasAttribute('data-nozoom') || svg.closest('nav,button,.fz-ctl')) return;
    const V = vb(svg); if (!V) return;
    let S = st.get(svg);
    if (!S) { const w = svg.getBoundingClientRect().width; if (w < MIN_W) return; const sp = spill(svg, V); if (!sp || !sp.big) return; S = wrap(svg, V); }
    if (!S.w.isConnected) return;
    const sp = spill(svg, V) || { L: 0, T: 0, R: 0, B: 0, big: false }, old = S.ext;
    const grew = !old.L && !old.T && !old.R && !old.B && sp.big;
    S.ext = sp.big || S.z !== 1 ? { L: Math.max(sp.L, S.z !== 1 ? old.L : 0), T: Math.max(sp.T, S.z !== 1 ? old.T : 0), R: Math.max(sp.R, S.z !== 1 ? old.R : 0), B: Math.max(sp.B, S.z !== 1 ? old.B : 0) } : { L: 0, T: 0, R: 0, B: 0 };
    const sx = S.sc.scrollLeft - old.L * S.s0 * S.z, sy = S.sc.scrollTop - old.T * S.s0 * S.z;
    lay(svg, S);
    // keep the original frame where it was on screen; first time, open on the original frame
    S.sc.scrollLeft = (grew ? 0 : sx) + S.ext.L * S.s0 * S.z; S.sc.scrollTop = (grew ? 0 : sy) + S.ext.T * S.s0 * S.z;
    S.ctl.hidden = !(sp.big || S.z !== 1); S.w.classList.toggle('on', !S.ctl.hidden);
  }
  let queued = false; const pend = new Set();
  function queue(svg) { if (!svg.closest || !svg.closest(SCOPE)) return; pend.add(svg); if (queued) return; queued = true; requestAnimationFrame(() => { queued = false; const a = [...pend]; pend.clear(); a.forEach(s => { try { look(s); } catch (e) {} }); }); }
  function scan(root) { (root.matches && root.matches('svg[viewBox]') ? [root] : []).concat([...(root.querySelectorAll ? root.querySelectorAll('svg[viewBox]') : [])]).forEach(queue); }
  new MutationObserver(ms => {
    for (const m of ms) {
      const t = m.target; const own = t.closest ? t.closest('svg') : null;
      if (own) { let top = own; while (top.parentNode && top.parentNode.closest && top.parentNode.closest('svg')) top = top.parentNode.closest('svg'); queue(top); continue; }
      m.addedNodes.forEach(n => { if (n.nodeType === 1) scan(n); });
    }
  }).observe(document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ['d', 'cx', 'cy', 'x', 'y', 'x1', 'x2', 'y1', 'y2', 'points', 'transform', 'r', 'width', 'height'] });
  addEventListener('load', () => scan(document.body));
  window.FitZoom = { scan, look };
})();
