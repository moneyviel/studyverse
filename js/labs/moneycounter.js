/* StudyVerse Concept Lab: moneycounter — "Money counter" (Indian rupees)
 * The child taps Indian coins and notes onto the counter to pay an exact amount, give change, or shop.
 *
 * PARAMS (all optional)
 *  name        type            meaning                                                               default
 *  mode        string          'pay'    : pay exactly `amount`                                         'pay'
 *                              'change' : something costs `price`, customer paid `paid` — give the change
 *                              'shop'   : tap items to buy (with prices), then act on `ask`
 *  amount      number          pay mode: amount in rupees (12.5 = ₹12.50 when paise is on)             37
 *  price       number          change mode: cost of the item                                           63
 *  paid        number          change mode: money given by the customer                                100
 *  itemName    string          change mode: what was bought (any language)                             'a toy'
 *  items       array           shop mode: [{name, price, icon?}] (icon = optional emoji)               4 snack items
 *  ask         string          shop mode: 'pay' (pay for the basket), 'total' (fill a basket worth exactly
 *                              `target`), 'cheapest' | 'costliest' (tap that item)                      'pay'
 *  buy         array           shop+pay: names of items that must be in the basket (else any basket)     none
 *  target      number          shop+total: basket total to reach                                       auto
 *  coins       array           coin values available (₹)                                               [1, 2, 5, 10]
 *  notes       array           note values available (₹)                                               [20, 50, 100, 200, 500]
 *  paise       boolean         adds the 50 paise coin and shows amounts as ₹12.50                       false
 *  fewest      boolean         the challenge also needs the fewest coins/notes possible                 false
 *  newChallenge boolean        show the "New" button                                                    true
 *  challenge   string          challenge text (any language); default generated                         auto
 */
(function () {
  const T = 'moneycounter';
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  // note colours (stylised, not copies of real notes)
  const NOTE = { 5: ['#8fbf6a', '#5e8d3d'], 10: ['#d4894a', '#9a5523'], 20: ['#c4d257', '#7f8d1e'], 50: ['#5cc8de', '#2a8ea3'], 100: ['#b29ae0', '#7354b3'], 200: ['#f5b83d', '#b97d06'], 500: ['#a3ab9b', '#646d5c'], 2000: ['#e07bb5', '#a63c7c'] };
  function coinSVG(v, s) { // v in paise
    const r = v < 100 ? 0.8 : v === 100 ? 0.86 : v === 200 ? 0.92 : v === 500 ? 0.96 : 1;
    const R = 11.5 * r;
    let body;
    if (v === 1000 || v === 2000) body = `<circle cx="12" cy="12" r="${R}" fill="#f2c94c" stroke="#b8901c" stroke-width="1.2"/><circle cx="12" cy="12" r="${R * .66}" fill="#d9dde6" stroke="#9aa0ad" stroke-width=".8"/>`;
    else if (v === 500) body = `<circle cx="12" cy="12" r="${R}" fill="#f3cd5a" stroke="#c39a1d" stroke-width="1.2"/><circle cx="12" cy="12" r="${R * .8}" fill="none" stroke="#c39a1d" stroke-width=".6"/>`;
    else body = `<circle cx="12" cy="12" r="${R}" fill="#dfe3ea" stroke="#9aa0ad" stroke-width="1.2"/><circle cx="12" cy="12" r="${R * .8}" fill="none" stroke="#aab0bd" stroke-width=".6"/>`;
    const lab = v < 100 ? v + 'p' : '₹' + v / 100;
    const fs = lab.length > 3 ? 6.2 : 7.4;
    return `<svg width="${s}" height="${s}" viewBox="0 0 24 24" aria-hidden="true">${body}<circle cx="8.5" cy="8" r="2.2" fill="#fff" opacity=".5"/><text x="12" y="${12 + fs * .36}" text-anchor="middle" font-size="${fs}" font-weight="800" fill="#3d4250">${lab}</text></svg>`;
  }
  function noteSVG(v, w) { // v in paise
    const r = v / 100, c = NOTE[r] || ['#9ad0a0', '#4f8a57'];
    const h = Math.round(w * .5);
    return `<svg width="${w}" height="${h}" viewBox="0 0 60 30" aria-hidden="true"><rect x=".7" y=".7" width="58.6" height="28.6" rx="3.5" fill="${c[0]}" stroke="${c[1]}" stroke-width="1.4"/><rect x="4" y="4" width="52" height="22" rx="2" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1"/><circle cx="46" cy="15" r="8" fill="#fff" opacity=".4"/><rect x="34" y="4" width="2" height="22" fill="#fff" opacity=".45"/><text x="18" y="20" text-anchor="middle" font-size="13" font-weight="800" fill="#1b1f3a" opacity=".82">₹${r}</text></svg>`;
  }

  const CSS = `
  .lb-moneycounter-w{user-select:none;-webkit-user-select:none}
  .lb-moneycounter-ch{font-weight:800;font-size:14.5px;line-height:1.3;color:#1b1f3a;background:#f4f0ff;border-radius:14px;padding:9px 12px;margin-bottom:8px}
  .lb-moneycounter-shop{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:7px;margin-bottom:8px}
  .lb-moneycounter-it{border:2px solid #e3e6f6;border-radius:14px;background:#fff;padding:6px 4px;text-align:center;cursor:pointer;font-family:inherit;color:#1b1f3a;min-height:58px;transition:transform .12s,border-color .2s,background .2s}
  .lb-moneycounter-it:active{transform:scale(.95)}
  .lb-moneycounter-it .ic{font-size:22px;line-height:1.1;display:block}
  .lb-moneycounter-it .nm{font-weight:800;font-size:13px;display:block;line-height:1.2;overflow-wrap:anywhere}
  .lb-moneycounter-it .pr{display:inline-block;margin-top:3px;background:#ffc93c;border-radius:8px;padding:1px 8px;font-weight:800;font-size:13px}
  .lb-moneycounter-it.on{border-color:#8b5cf6;background:#f4f0ff}
  .lb-moneycounter-it.on .pr{background:#8b5cf6;color:#fff}
  .lb-moneycounter-counter{background:linear-gradient(180deg,#eaf7ef,#dff3e7);border-radius:18px;box-shadow:inset 0 0 0 2px #c7ead5;padding:8px 8px 6px;min-height:118px}
  .lb-moneycounter-top{display:flex;justify-content:space-between;align-items:baseline;gap:6px;flex-wrap:wrap}
  .lb-moneycounter-top .l{font-weight:800;font-size:12px;color:#3c8a5e;text-transform:uppercase;letter-spacing:.4px}
  .lb-moneycounter-tot{font-weight:800;font-size:26px;color:#1b1f3a}
  .lb-moneycounter-tot small{font-size:14px;color:#6b7090}
  .lb-moneycounter-tray{display:flex;flex-wrap:wrap;gap:3px;align-items:center;min-height:52px;padding:4px 0}
  .lb-moneycounter-tray .pc{cursor:pointer;animation:lbmcIn .25s ease;display:block;line-height:0}
  .lb-moneycounter-tray .empty{color:#7fae92;font-weight:700;font-size:13px;width:100%;text-align:center}
  @keyframes lbmcIn{from{transform:translateY(-14px) scale(.7);opacity:0}}
  .lb-moneycounter-bar{height:10px;border-radius:999px;background:#fff;overflow:hidden;box-shadow:inset 0 0 0 1px #c7ead5}
  .lb-moneycounter-bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,#2ed3a5,#3b82f6);border-radius:999px;transition:width .25s,background .25s}
  .lb-moneycounter-bar i.over{background:#ff6b6b}
  .lb-moneycounter-msg{text-align:center;font-weight:800;font-size:14px;color:#7c4ddb;min-height:20px;margin:6px 0 4px}
  .lb-moneycounter-wallet{display:flex;flex-wrap:wrap;gap:5px;justify-content:center;background:#fff8e6;border-radius:16px;padding:7px 4px;box-shadow:inset 0 0 0 2px #ffe6a6}
  .lb-moneycounter-d{border:none;background:none;padding:2px;cursor:pointer;line-height:0;border-radius:10px;transition:transform .08s;min-width:44px;min-height:44px;display:flex;align-items:center;justify-content:center}
  .lb-moneycounter-d:active{transform:scale(.88)}
  .lb-moneycounter-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:8px}
  .lb-moneycounter-s{height:42px;min-width:44px;border:none;border-radius:14px;font-family:inherit;font-weight:800;font-size:14px;cursor:pointer;background:#eef0fb;color:#1b1f3a;box-shadow:0 4px 0 #d3d7ef;padding:0 13px}
  .lb-moneycounter-s:active{transform:translateY(3px);box-shadow:0 1px 0 #d3d7ef}
  `;

  Labs.register(T, {
    title: 'Money counter',
    subjects: ['maths'],
    render(host, p, api) {
      const mode = ['pay', 'change', 'shop'].includes(p.mode) ? p.mode : 'pay';
      const P = v => { const x = Math.round(parseFloat(String(v == null ? '' : v).replace(/[₹,\s]/g, '')) * 100); return isFinite(x) ? x : NaN; };
      const okList = (a, d) => Array.isArray(a) && a.length ? a.map(P).filter(x => x > 0) : d;
      let coins = okList(p.coins, [100, 200, 500, 1000]);
      const notes = okList(p.notes, [2000, 5000, 10000, 20000, 50000]);
      if (p.paise && !coins.includes(50)) coins = [50].concat(coins);
      const usePaise = !!p.paise || coins.some(c => c % 100) ;
      const denoms = coins.map(v => ({ v, k: 'c' })).concat(notes.map(v => ({ v, k: 'n' }))).sort((a, b) => a.v - b.v);
      const allV = [...new Set(denoms.map(d => d.v))].sort((a, b) => a - b);
      const rs = v => { const neg = v < 0; v = Math.abs(v); const r = Math.floor(v / 100), ps = v % 100; const s = r.toLocaleString('en-IN'); return (neg ? '−' : '') + '₹' + (usePaise || ps ? s + '.' + String(ps).padStart(2, '0') : s); };
      const unit = Math.min(...allV);
      const round = v => Math.round(v / unit) * unit;
      // minimum pieces (DP, works for any denominations)
      function minPieces(t) {
        if (t <= 0) return 0; const u = unit; const n = Math.round(t / u); if (n > 20000) return Infinity;
        const dp = new Array(n + 1).fill(Infinity); dp[0] = 0;
        const vs = allV.map(v => Math.round(v / u));
        for (let i = 1; i <= n; i++) for (const v of vs) if (v <= i && dp[i - v] + 1 < dp[i]) dp[i] = dp[i - v] + 1;
        return dp[n];
      }

      // ---------- challenge state ----------
      let amount = 0, price = 0, paid = 0, target = 0;
      let items = Array.isArray(p.items) && p.items.length ? p.items.map(it => ({ name: String(it.name == null ? '' : it.name), price: P(it.price), icon: it.icon || '' })).filter(it => it.price > 0) : [];
      if (!items.length) items = [{ name: 'Pencil', price: 500 }, { name: 'Eraser', price: 300 }, { name: 'Notebook', price: 3500 }, { name: 'Pen', price: 1000 }];
      const ask = ['pay', 'total', 'cheapest', 'costliest'].includes(p.ask) ? p.ask : 'pay';
      let mustBuy = Array.isArray(p.buy) ? p.buy.map(String) : [];
      function setup() {
        amount = round(P(p.amount)); if (!(amount > 0)) amount = 3700;
        price = round(P(p.price)); paid = round(P(p.paid));
        if (!(price > 0)) price = 6300; if (!(paid > price)) paid = Math.ceil((price + 1) / 10000) * 10000;
        target = round(P(p.target));
        if (!(target > 0)) { const s = items.slice(0, 2).reduce((a, b) => a + b.price, 0); target = s; }
      }
      setup();
      let tray = [], basket = new Set(), customText = p.challenge ? String(p.challenge) : '';
      const goal = () => mode === 'pay' ? amount : mode === 'change' ? paid - price : basketTotal();
      const basketTotal = () => [...basket].reduce((s, i) => s + items[i].price, 0);
      const trayTotal = () => tray.reduce((s, v) => s + v, 0);
      const itemName = p.itemName || 'a toy';

      function defaultText() {
        if (mode === 'pay') return `Pay exactly ${rs(amount)}${p.fewest ? ' using the fewest coins and notes' : ''}`;
        if (mode === 'change') return `${itemName} costs ${rs(price)}. The customer pays ${rs(paid)}. Give the right change${p.fewest ? ' with the fewest pieces' : ''}.`;
        if (ask === 'total') return `Choose things that cost exactly ${rs(target)} in all`;
        if (ask === 'cheapest') return 'Tap the cheapest thing';
        if (ask === 'costliest') return 'Tap the costliest thing';
        return mustBuy.length ? `Buy ${mustBuy.join(' and ')}. Pay the exact total.` : 'Pick things to buy, then pay the exact total';
      }

      host.innerHTML = `<style>${CSS}</style><div class="lb-moneycounter-w">
        <div class="lb-moneycounter-ch"></div>
        <div class="lb-moneycounter-shop"></div>
        <div class="lb-moneycounter-counter">
          <div class="lb-moneycounter-top"><span class="l"></span><span class="lb-moneycounter-tot"></span></div>
          <div class="lb-moneycounter-tray"></div>
          <div class="lb-moneycounter-bar"><i></i></div>
        </div>
        <div class="lb-moneycounter-msg"></div>
        <div class="lb-moneycounter-wallet"></div>
        <div class="lb-moneycounter-row"></div></div>`;
      const $ = s => host.querySelector(s);
      const chEl = $('.lb-moneycounter-ch'), shopEl = $('.lb-moneycounter-shop'), counterEl = $('.lb-moneycounter-counter'), labEl = $('.lb-moneycounter-top .l'), totEl = $('.lb-moneycounter-tot'), trayEl = $('.lb-moneycounter-tray'), barEl = $('.lb-moneycounter-bar i'), msgEl = $('.lb-moneycounter-msg'), walletEl = $('.lb-moneycounter-wallet'), rowEl = $('.lb-moneycounter-row');
      const msg = t => { msgEl.textContent = t || ''; };
      const pieceHTML = (v, k, big) => k === 'n' ? noteSVG(v, big ? 70 : 56) : coinSVG(v, big ? (v >= 1000 ? 46 : v >= 500 ? 44 : v >= 200 ? 42 : 40) : (v >= 1000 ? 36 : 32));
      const kindOf = v => (notes.includes(v) && !coins.includes(v)) ? 'n' : 'c';
      const trayKinds = [];
      const needMoney = !(mode === 'shop' && (ask === 'total' || ask === 'cheapest' || ask === 'costliest'));

      function drawShop() {
        if (mode !== 'shop') { shopEl.style.display = 'none'; return; }
        shopEl.innerHTML = items.map((it, i) => `<button class="lb-moneycounter-it${basket.has(i) ? ' on' : ''}" data-i="${i}">${it.icon ? `<span class="ic">${esc(it.icon)}</span>` : ''}<span class="nm">${esc(it.name)}</span><span class="pr">${rs(it.price)}</span></button>`).join('');
      }
      function drawWallet() {
        walletEl.innerHTML = denoms.map(d => `<button class="lb-moneycounter-d" data-v="${d.v}" data-k="${d.k}" aria-label="${rs(d.v)}">${pieceHTML(d.v, d.k, true)}</button>`).join('');
        walletEl.style.display = needMoney ? '' : 'none';
        counterEl.style.display = needMoney ? '' : 'none';
      }
      function drawTray() {
        const g = goal(), t = trayTotal();
        trayEl.innerHTML = tray.length ? tray.map((v, i) => `<span class="pc" data-i="${i}" title="tap to take back">${pieceHTML(v, trayKinds[i])}</span>`).join('') : `<span class="empty">Tap coins and notes below to put them here</span>`;
        labEl.textContent = mode === 'change' ? 'Change you give' : 'On the counter';
        totEl.innerHTML = `${rs(t)} <small>/ ${g ? rs(g) : '—'}</small>`;
        const pct = g ? Math.min(100, t / g * 100) : 0;
        barEl.style.width = pct + '%'; barEl.classList.toggle('over', g > 0 && t > g);
      }
      function status() {
        const g = goal(), t = trayTotal();
        if (!needMoney) {
          if (ask === 'total') { const b = basketTotal(); msg(basket.size ? `Basket: ${[...basket].map(i => rs(items[i].price)).join(' + ')} = ${rs(b)}` + (b < target ? ` · need ${rs(target - b)} more` : b > target ? ` · ${rs(b - target)} too much` : '') : 'Tap items to add them to your basket'); }
          return;
        }
        if (mode === 'shop' && !basket.size) { msg('First tap the things you want to buy'); return; }
        if (!tray.length) { msg(mode === 'change' ? `Count up from ${rs(price)} to ${rs(paid)}` : ''); return; }
        if (t < g) msg(`${rs(g - t)} more needed`);
        else if (t > g) msg(`Too much by ${rs(t - g)} — tap a coin to take it back`);
        else msg(mode === 'change' ? `${rs(price)} + ${rs(t)} = ${rs(paid)} ✔` : 'Exact amount! ✔');
      }
      function buildRow() {
        rowEl.innerHTML = (needMoney ? `<button class="lb-moneycounter-s" data-act="undo">↩ Undo</button>` : '') + `<button class="lb-moneycounter-s" data-act="clear">↺ Clear</button>` + (p.newChallenge !== false ? `<button class="lb-moneycounter-s" data-act="new">✨ New</button>` : '');
      }
      const setText = () => { chEl.textContent = '🎯 Challenge: ' + (customText || defaultText()); };
      function refresh() { drawShop(); drawTray(); status(); }

      // ---------- win ----------
      let won = false;
      function win(m) { if (won) return; won = true; api.sfx('correct'); api.win(m); }
      function check() {
        if (won) return;
        if (mode === 'shop' && ask === 'total') {
          const b = basketTotal();
          if (b === target) win(`${[...basket].map(i => items[i].name).join(' + ')} = ${rs(b)}`);
          return;
        }
        if (mode === 'shop' && (ask === 'cheapest' || ask === 'costliest')) return;
        const g = goal(), t = trayTotal();
        if (!g || t !== g) return;
        if (mode === 'shop' && mustBuy.length) {
          const names = [...basket].map(i => items[i].name.toLowerCase());
          if (!mustBuy.every(n => names.includes(n.toLowerCase())) || names.length !== mustBuy.length) { msg(`Exact! But the basket should have only: ${mustBuy.join(', ')}`); return; }
        }
        const mp = minPieces(g);
        if (p.fewest && tray.length > mp) { api.sfx('hmm'); msg(`Right amount with ${tray.length} pieces. Can you do it with ${mp}?`); return; }
        const fewNote = !p.fewest && tray.length > mp ? ` (smallest way: ${mp} pieces)` : '';
        if (mode === 'pay') win(`You paid ${rs(g)} with ${tray.length} piece${tray.length > 1 ? 's' : ''}${fewNote}`);
        else if (mode === 'change') win(`${rs(paid)} − ${rs(price)} = ${rs(g)} change${fewNote}`);
        else win(`Basket total ${rs(g)} paid exactly!${fewNote}`);
      }

      // ---------- events ----------
      walletEl.addEventListener('click', e => {
        const b = e.target.closest('button'); if (!b) return;
        if (mode === 'shop' && !basket.size) { api.sfx('hmm'); msg('First tap the things you want to buy'); return; }
        if (tray.length >= 40) { api.sfx('wrong'); msg('The counter is full!'); return; }
        tray.push(+b.dataset.v); trayKinds.push(b.dataset.k); api.sfx('coin'); drawTray(); status(); check();
      });
      trayEl.addEventListener('click', e => {
        const pc = e.target.closest('.pc'); if (!pc) return;
        const i = +pc.dataset.i; tray.splice(i, 1); trayKinds.splice(i, 1); api.sfx('tap'); drawTray(); status(); check();
      });
      shopEl.addEventListener('click', e => {
        const b = e.target.closest('button'); if (!b) return; const i = +b.dataset.i;
        if (ask === 'cheapest' || ask === 'costliest') {
          basket = new Set([i]); drawShop();
          const prices = items.map(x => x.price); const best = ask === 'cheapest' ? Math.min(...prices) : Math.max(...prices);
          const sorted = items.slice().sort((a, b2) => a.price - b2.price).map(x => `${x.name} ${rs(x.price)}`).join(' < ');
          if (items[i].price === best) { msg(sorted); win(`${items[i].name} at ${rs(best)} is the ${ask}!`); }
          else { api.sfx('wrong'); const o = items.find(x => x.price === best); msg(`${items[i].name} costs ${rs(items[i].price)}. Compare — is anything ${ask === 'cheapest' ? 'cheaper' : 'costlier'}?`); }
          return;
        }
        basket.has(i) ? basket.delete(i) : basket.add(i); api.sfx('tap'); refresh(); check();
      });
      rowEl.addEventListener('click', e => {
        const b = e.target.closest('button'); if (!b) return; const a = b.dataset.act;
        if (a === 'undo') { tray.pop(); trayKinds.pop(); api.sfx('tap'); drawTray(); status(); }
        else if (a === 'clear') { tray = []; trayKinds.length = 0; basket = new Set(); api.sfx('tap'); refresh(); }
        else if (a === 'new') newChallenge();
      });
      function newChallenge() {
        const r = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
        const bigV = Math.max(...allV);
        if (mode === 'pay') { let a; do { a = round(r(3, Math.min(bigV / 100 * 2, 300)) * 100 + (usePaise && Math.random() < .5 ? 50 : 0)); } while (a === amount); amount = a; }
        else if (mode === 'change') { const pv = [1000, 2000, 5000, 10000, 20000, 50000].filter(v => v <= bigV * 2); paid = pv[r(Math.min(1, pv.length - 1), pv.length - 1)] || 10000; price = round(r(1, Math.max(1, paid / 100 - 1)) * 100 - (usePaise && Math.random() < .5 ? 50 : 0)); if (price <= 0) price = paid / 2; }
        else if (ask === 'total') { const idx = items.map((_, i) => i).sort(() => Math.random() - .5).slice(0, r(2, Math.min(3, items.length))); target = idx.reduce((s, i) => s + items[i].price, 0); }
        else if (ask === 'pay') { mustBuy = items.map(x => x.name).sort(() => Math.random() - .5).slice(0, r(1, Math.min(2, items.length))); }
        else if (ask === 'cheapest' || ask === 'costliest') { items.sort(() => Math.random() - .5); }
        tray = []; trayKinds.length = 0; basket = new Set(); customText = '';
        if (won) { won = false; api.resetWin && api.resetWin(); }
        setText(); refresh(); api.sfx('tap');
      }

      setText(); drawWallet(); buildRow(); refresh();
      return () => { };
    },
    example: { mode: 'pay', amount: 37 },
    examples: [
      { mode: 'change', price: 63, paid: 100, itemName: 'A cricket ball', fewest: true, challenge: 'A cricket ball costs ₹63. Aman pays with a ₹100 note. Give him the change using the fewest coins and notes.' },
      { mode: 'shop', ask: 'pay', items: [{ name: 'Samosa', price: 15 }, { name: 'Lassi', price: 30 }, { name: 'Jalebi', price: 25 }, { name: 'Chai', price: 10 }], buy: ['Samosa', 'Lassi'], challenge: 'Buy a samosa and a lassi. Pay the exact total.' },
      { mode: 'pay', amount: 12.5, paise: true, coins: [1, 2, 5, 10], notes: [10, 20, 50], challenge: 'A pencil box costs ₹12.50. Pay the exact amount — you will need a 50 paise coin!' }
    ]
  });
})();
