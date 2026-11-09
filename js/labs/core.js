/* Knowtopia Concept Labs — registry and loader. Each lab lives in js/labs/<type>.js */
(function () {
  const REG = {}, loading = {};
  let current = null;
  function loadType(type) {
    if (REG[type]) return Promise.resolve(REG[type]);
    if (loading[type]) return loading[type];
    loading[type] = new Promise((res, rej) => {
      const s = document.createElement('script'); s.src = `js/labs/${type}.js?v=${window.LAB_V || 1}`;
      s.onload = () => REG[type] ? res(REG[type]) : rej(new Error('lab did not register: ' + type));
      s.onerror = () => rej(new Error('lab not found: ' + type));
      document.head.appendChild(s);
    });
    return loading[type];
  }
  function unmount() { if (current) { try { current(); } catch (e) {} current = null; } try { window.A11Y && A11Y.labUnmounted(); } catch (e) {} }
  async function mount(host, spec, opts = {}) {
    unmount();
    host.innerHTML = '<div class="lab-loading">Loading lab…</div>';
    let def;
    try { def = await loadType(spec.type); } catch (e) { host.innerHTML = ''; return false; }
    host.innerHTML = '';
    const box = document.createElement('div'); box.className = 'lab-box'; host.appendChild(box);
    const winEl = document.createElement('div'); winEl.className = 'lab-win'; host.appendChild(winEl);
    let won = false;
    const api = {
      speak: t => window.speak && window.speak(t),
      sfx: k => window.sfx && window.sfx(k),
      win: msg => { if (won) return; won = true; winEl.innerHTML = `🎉 ${String(msg || 'Challenge complete!').replace(/[<>&]/g, '')}`; winEl.classList.add('show'); api.sfx('unlock'); opts.onWin && opts.onWin(msg); },
      resetWin: () => { won = false; winEl.classList.remove('show'); }
    };
    try { const given = spec.p && Object.keys(spec.p).length ? spec.p : null; const p = given ? Object.assign({}, given) : Object.assign({}, def.example || {}); const c = await def.render(box, p, api); current = typeof c === 'function' ? c : null; }
    catch (e) { console.error('lab error', spec.type, e); host.innerHTML = ''; return false; }
    /* accessibility: spoken description, narration of changes and sonification for every lab type (js/a11y.js) */
    try { if (window.A11Y) A11Y.labMounted(host, box, spec, def); } catch (e) {}
    return true;
  }
  window.Labs = { register: (t, d) => { REG[t] = d; }, mount, unmount, loadType, registry: REG };
})();
