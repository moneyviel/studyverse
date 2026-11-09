/* ================= StudyVerse strict, friendly input fields — js/fields.js =================
   window.Fields — one shared helper for the app (index.html) and the pricing page.
   Mark an input with data-field="phone" | "pincode" | "email" | "digits" (and a <select data-field="board">);
   it is upgraded by itself (a MutationObserver watches the page) or by Fields.enhance(rootEl).
   - phone   : country button (🇮🇳 +91, searchable list of countries) + a digits-only box (letters / symbols are blocked
               on keydown, paste and input; numeric keyboard). India: exactly 10 digits starting 6–9; other countries:
               a per-country length (or 6–14). Fields.value(el) gives E.164, e.g. +919876543210.
   - pincode : Indian PIN, digits only, exactly 6, first digit 1–9.
   - email   : trimmed + lower-cased on blur; checked on blur / submit; the error clears as soon as the value is valid.
   - digits  : digits only (data-min / data-max optional, e.g. number of students).
   - text    : plain text that is required (data-minlen, data-label for the message).
   - board   : a <select>; Fields.boardOptions(current) gives its <option>s (CBSE, ICSE/ISC, state boards, IB, …).
   Fields.valid(rootEl) → { ok, first }: shows every error under its box (aria-invalid + aria-describedby) and focuses
   the first bad field. Empty fields are only an error when the input is required (required / data-required).
   Works on the light screens and on the dark CA look (colours follow the box's own background). */
(function () {
  'use strict';
  if (window.Fields) return;
  const D = document;

  /* ---------- countries: ISO:Name:dial code[:digits after the code, "n" or "min-max"] (no length = 6–14) ---------- */
  const RAW = 'IN:India:91:10;AF:Afghanistan:93:9;AL:Albania:355:8-9;DZ:Algeria:213:8-9;AS:American Samoa:1684:7;AD:Andorra:376:6-9;AO:Angola:244:9;' +
    'AI:Anguilla:1264:7;AG:Antigua and Barbuda:1268:7;AR:Argentina:54:10-11;AM:Armenia:374:8;AW:Aruba:297:7;AU:Australia:61:9;AT:Austria:43;' +
    'AZ:Azerbaijan:994:9;BS:Bahamas:1242:7;BH:Bahrain:973:8;BD:Bangladesh:880:10;BB:Barbados:1246:7;BY:Belarus:375:9;BE:Belgium:32:8-9;' +
    'BZ:Belize:501:7;BJ:Benin:229:8-10;BM:Bermuda:1441:7;BT:Bhutan:975:7-8;BO:Bolivia:591:8;BA:Bosnia and Herzegovina:387:8-9;BW:Botswana:267:7-8;' +
    'BR:Brazil:55:10-11;VG:British Virgin Islands:1284:7;BN:Brunei:673:7;BG:Bulgaria:359:8-9;BF:Burkina Faso:226:8;BI:Burundi:257:8;' +
    'KH:Cambodia:855:8-9;CM:Cameroon:237:9;CA:Canada:1:10;CV:Cape Verde:238:7;KY:Cayman Islands:1345:7;CF:Central African Republic:236:8;' +
    'TD:Chad:235:8;CL:Chile:56:9;CN:China:86:9-11;CO:Colombia:57:10;KM:Comoros:269:7;CG:Congo:242:9;CD:Congo (DRC):243:9;CK:Cook Islands:682:5;' +
    'CR:Costa Rica:506:8;CI:Côte d’Ivoire:225:10;HR:Croatia:385:8-9;CU:Cuba:53:8;CW:Curaçao:599:7;CY:Cyprus:357:8;CZ:Czechia:420:9;' +
    'DK:Denmark:45:8;DJ:Djibouti:253:8;DM:Dominica:1767:7;DO:Dominican Republic:1:10;EC:Ecuador:593:8-9;EG:Egypt:20:9-10;SV:El Salvador:503:8;' +
    'GQ:Equatorial Guinea:240:9;ER:Eritrea:291:7;EE:Estonia:372:7-8;SZ:Eswatini:268:8;ET:Ethiopia:251:9;FK:Falkland Islands:500:5;' +
    'FO:Faroe Islands:298:6;FJ:Fiji:679:7;FI:Finland:358;FR:France:33:9;GF:French Guiana:594:9;PF:French Polynesia:689:8;GA:Gabon:241:7-8;' +
    'GM:Gambia:220:7;GE:Georgia:995:9;DE:Germany:49;GH:Ghana:233:9;GI:Gibraltar:350:8;GR:Greece:30:10;GL:Greenland:299:6;GD:Grenada:1473:7;' +
    'GP:Guadeloupe:590:9;GU:Guam:1671:7;GT:Guatemala:502:8;GG:Guernsey:44:10;GN:Guinea:224:9;GW:Guinea-Bissau:245:7-9;GY:Guyana:592:7;' +
    'HT:Haiti:509:8;HN:Honduras:504:8;HK:Hong Kong:852:8;HU:Hungary:36:8-9;IS:Iceland:354:7;ID:Indonesia:62:9-12;IR:Iran:98:10;IQ:Iraq:964:8-10;' +
    'IE:Ireland:353:7-9;IM:Isle of Man:44:10;IL:Israel:972:8-9;IT:Italy:39:6-11;JM:Jamaica:1876:7;JP:Japan:81:9-10;JE:Jersey:44:10;' +
    'JO:Jordan:962:8-9;KZ:Kazakhstan:7:10;KE:Kenya:254:9;KI:Kiribati:686:5-8;XK:Kosovo:383:8-9;KW:Kuwait:965:8;KG:Kyrgyzstan:996:9;' +
    'LA:Laos:856:8-10;LV:Latvia:371:8;LB:Lebanon:961:7-8;LS:Lesotho:266:8;LR:Liberia:231:7-9;LY:Libya:218:9;LI:Liechtenstein:423:7;' +
    'LT:Lithuania:370:8;LU:Luxembourg:352;MO:Macao:853:8;MG:Madagascar:261:9;MW:Malawi:265:7-9;MY:Malaysia:60:9-10;MV:Maldives:960:7;' +
    'ML:Mali:223:8;MT:Malta:356:8;MH:Marshall Islands:692:7;MQ:Martinique:596:9;MR:Mauritania:222:8;MU:Mauritius:230:7-8;YT:Mayotte:262:9;' +
    'MX:Mexico:52:10;FM:Micronesia:691:7;MD:Moldova:373:8;MC:Monaco:377:8-9;MN:Mongolia:976:8;ME:Montenegro:382:8;MS:Montserrat:1664:7;' +
    'MA:Morocco:212:9;MZ:Mozambique:258:8-9;MM:Myanmar:95:7-10;NA:Namibia:264:8-9;NR:Nauru:674:7;NP:Nepal:977:8-10;NL:Netherlands:31:9;' +
    'NC:New Caledonia:687:6;NZ:New Zealand:64:8-10;NI:Nicaragua:505:8;NE:Niger:227:8;NG:Nigeria:234:8-10;KP:North Korea:850;' +
    'MK:North Macedonia:389:8;MP:Northern Mariana Islands:1670:7;NO:Norway:47:8;OM:Oman:968:8;PK:Pakistan:92:10;PW:Palau:680:7;' +
    'PS:Palestine:970:9;PA:Panama:507:7-8;PG:Papua New Guinea:675:7-8;PY:Paraguay:595:9;PE:Peru:51:8-9;PH:Philippines:63:8-10;PL:Poland:48:9;' +
    'PT:Portugal:351:9;PR:Puerto Rico:1:10;QA:Qatar:974:8;RE:Réunion:262:9;RO:Romania:40:9;RU:Russia:7:10;RW:Rwanda:250:9;' +
    'KN:Saint Kitts and Nevis:1869:7;LC:Saint Lucia:1758:7;VC:Saint Vincent and the Grenadines:1784:7;WS:Samoa:685:5-7;SM:San Marino:378;' +
    'ST:São Tomé and Príncipe:239:7;SA:Saudi Arabia:966:8-9;SN:Senegal:221:9;RS:Serbia:381;SC:Seychelles:248:7;SL:Sierra Leone:232:8;' +
    'SG:Singapore:65:8;SX:Sint Maarten:1721:7;SK:Slovakia:421:9;SI:Slovenia:386:8;SB:Solomon Islands:677:5-7;SO:Somalia:252;' +
    'ZA:South Africa:27:9;KR:South Korea:82:8-10;SS:South Sudan:211:9;ES:Spain:34:9;LK:Sri Lanka:94:9;SD:Sudan:249:9;SR:Suriname:597:6-7;' +
    'SE:Sweden:46;CH:Switzerland:41:9;SY:Syria:963:8-9;TW:Taiwan:886:8-9;TJ:Tajikistan:992:9;TZ:Tanzania:255:9;TH:Thailand:66:8-9;' +
    'TL:Timor-Leste:670:7-8;TG:Togo:228:8;TO:Tonga:676:5-7;TT:Trinidad and Tobago:1868:7;TN:Tunisia:216:8;TR:Türkiye:90:10;' +
    'TM:Turkmenistan:993:8;TC:Turks and Caicos Islands:1649:7;TV:Tuvalu:688:5-6;UG:Uganda:256:9;UA:Ukraine:380:9;' +
    'AE:United Arab Emirates:971:8-9;GB:United Kingdom:44:9-10;US:United States:1:10;UY:Uruguay:598:8;VI:US Virgin Islands:1340:7;' +
    'UZ:Uzbekistan:998:9;VU:Vanuatu:678:5-7;VA:Vatican City:39:6-11;VE:Venezuela:58:10;VN:Vietnam:84:9-10;YE:Yemen:967:7-9;ZM:Zambia:260:9;ZW:Zimbabwe:263';
  const flag = iso => String.fromCodePoint(...[...iso].map(c => 0x1F1E6 + c.charCodeAt(0) - 65));
  const COUNTRIES = RAW.split(';').map(s => {
    const [iso, name, dial, len] = s.split(':'); let min = 6, max = 14;
    if (len) { const p = len.split('-'); min = +p[0]; max = +(p[1] || p[0]); }
    // E.164: 7 to 15 digits in all (the server checks ^\+[1-9][0-9]{6,14}$)
    return { iso, name, dial, flag: flag(iso), min: Math.max(min, 7 - dial.length), max: Math.min(max, 15 - dial.length) };
  });
  // the picker lists India first, then A–Z
  const SORTED = [COUNTRIES[0]].concat(COUNTRIES.slice(1).sort((a, b) => a.name.localeCompare(b.name)));
  const byIso = iso => COUNTRIES.find(c => c.iso === iso) || COUNTRIES[0];

  /* ---------- boards (state boards = the states in content/boards.json) ---------- */
  const STATE_BOARDS = [['Andhra Pradesh', 'AP Board'], ['Assam', 'Assam Board'], ['Bihar', 'Bihar Board'], ['Chhattisgarh', 'CG Board'], ['Goa', 'Goa Board'],
    ['Gujarat', 'Gujarat Board'], ['Haryana', 'Haryana Board'], ['Himachal Pradesh', 'HP Board'], ['Jammu & Kashmir', 'JKBOSE'], ['Jharkhand', 'JAC Board'],
    ['Karnataka', 'Karnataka Board'], ['Kerala', 'Kerala Board'], ['Madhya Pradesh', 'MP Board'], ['Maharashtra', 'Maharashtra Board'], ['Manipur', 'Manipur Board'],
    ['Meghalaya', 'Meghalaya Board'], ['Mizoram', 'Mizoram Board'], ['Nagaland', 'Nagaland Board'], ['Odisha', 'Odisha Board'], ['Punjab', 'Punjab Board'],
    ['Rajasthan', 'Rajasthan Board'], ['Tamil Nadu', 'TN Board'], ['Telangana', 'Telangana Board'], ['Tripura', 'Tripura Board'], ['Uttar Pradesh', 'UP Board'],
    ['Uttarakhand', 'Uttarakhand Board'], ['West Bengal', 'WB Board']];
  const BOARDS = [['CBSE', 'CBSE'], ['ICSE/ISC', 'ICSE / ISC']].concat(
    STATE_BOARDS.map(([s, b]) => ['State board: ' + s, s + ' — ' + b]), [['State board: Other', 'Other state board']],
    [['IB', 'IB'], ['Cambridge/IGCSE', 'Cambridge / IGCSE'], ['NIOS', 'NIOS'], ['Other', 'Other']]);
  const escA = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  function boardOptions(cur, placeholder) {
    cur = cur == null ? '' : String(cur);
    const known = BOARDS.some(b => b[0] === cur), o = ([v, l]) => `<option value="${escA(v)}"${v === cur ? ' selected' : ''}>${escA(l)}</option>`;
    return `<option value="">${escA(placeholder || '— Choose board —')}</option>${cur && !known ? o([cur, cur]) : ''}`
      + BOARDS.slice(0, 2).map(o).join('') + `<optgroup label="State boards">${BOARDS.filter(b => b[0].startsWith('State board')).map(o).join('')}</optgroup>`
      + BOARDS.slice(-4).map(o).join('');
  }

  /* ---------- pure checks ('' = fine) ---------- */
  const EMAIL = /^[a-z0-9._%+'-]+@[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)*\.[a-z]{2,}$/;
  const normEmail = v => String(v == null ? '' : v).trim().toLowerCase();
  const emailOk = v => { v = normEmail(v); return v.length <= 254 && EMAIL.test(v) && !/\.\.|^\.|\.@/.test(v); };
  const pinOk = v => /^[1-9][0-9]{5}$/.test(String(v || ''));
  function phoneMsg(c, n) {
    if (c.iso === 'IN') return /^[6-9][0-9]{9}$/.test(n) ? '' : (/^[0-5]/.test(n) ? 'Indian mobile numbers start with 6, 7, 8 or 9.' : 'Please enter a 10-digit mobile number.');
    if (n.length < c.min || n.length > c.max) return `Please enter a valid ${c.name} number (${c.min === c.max ? c.min : c.min + '–' + c.max} digits after +${c.dial}).`;
    return '';
  }
  // any typed / pasted / stored phone → { c: country, n: national digits }
  function parsePhone(v, defIso) {
    const s = String(v == null ? '' : v).trim(); let d = s.replace(/\D/g, '');
    if (/^(\+|00)/.test(s)) {
      if (s.startsWith('00')) d = d.slice(2);
      let best = null;
      for (const c of COUNTRIES) if (d.startsWith(c.dial) && (!best || c.dial.length > best.dial.length)) best = c;
      if (best) return { c: best, n: d.slice(best.dial.length) };
    }
    const c = byIso(defIso || 'IN');
    if (c.iso === 'IN') { if (/^91[6-9][0-9]{9}$/.test(d)) d = d.slice(2); d = d.replace(/^0+/, ''); }
    else if (d.length > c.max && d.startsWith(c.dial)) d = d.slice(c.dial.length);
    else if (d.length > c.max && d.startsWith('0')) d = d.slice(1);
    return { c, n: d };
  }
  // E.164 check (same rule as the server): +[1-9] then 6–14 digits; +91 must be a mobile number
  const e164Ok = v => /^\+[1-9][0-9]{6,14}$/.test(v) && (!/^\+91/.test(v) || /^\+91[6-9][0-9]{9}$/.test(v));

  /* ---------- styles (once) ---------- */
  const CSS = `.fld-ph{position:relative;display:flex;align-items:stretch;gap:6px;width:100%;box-sizing:border-box}
.fld-ph>input{flex:1 1 auto;min-width:0;width:auto!important;margin:0!important}
.fld-ph>.fld-cc{flex:none;width:auto!important;min-width:0;margin:0!important;padding-left:10px!important;padding-right:8px!important;display:inline-flex!important;align-items:center;gap:4px;white-space:nowrap;cursor:pointer;font-weight:700;text-align:left}
.fld-cc .fld-fl{font-size:1.15em;line-height:1}.fld-cc .fld-car{font-size:.75em;opacity:.7}
.fld-err{display:block;color:#B71C2C;font-size:13px;font-weight:600;line-height:1.35;margin:4px 0 8px;text-align:left}.fld-err[hidden]{display:none}
.fld-err.fld-dk{color:#FFB4B4}
[data-field][aria-invalid=true],.fld-ph [aria-invalid=true]{border-color:#B71C2C!important;box-shadow:0 0 0 1px #B71C2C}
.fld-dk[aria-invalid=true],.fld-dkin[aria-invalid=true]{border-color:#FF8A8A!important;box-shadow:0 0 0 1px #FF8A8A}
.fld-pop{position:absolute;left:0;right:0;top:calc(100% + 4px);z-index:1200;background:#FFFDF8;color:#15161C;border:1.5px solid #cfc3aa;border-radius:12px;box-shadow:0 10px 28px rgba(0,0,0,.22);padding:8px;box-sizing:border-box}
.fld-pop.fld-dk{background:#1E2029;color:#F2EEE6;border-color:rgba(201,167,106,.45);color-scheme:dark}
.fld-pop .fld-q{display:block;width:100%;box-sizing:border-box;min-height:44px;padding:8px 10px;border:1.5px solid #cfc3aa;border-radius:10px;font:inherit;font-size:16px;background:#fff;color:#15161C;margin:0 0 6px}
.fld-pop.fld-dk .fld-q{background:#2A2D38;color:#fff;border-color:rgba(201,167,106,.45)}
.fld-list{list-style:none;margin:0;padding:0;max-height:240px;overflow:auto;overscroll-behavior:contain}
.fld-list li{display:flex;align-items:center;gap:8px;min-height:44px;padding:6px 8px;border-radius:8px;cursor:pointer;font-size:15px}
.fld-list li .fld-nm{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.fld-list li .fld-dc{font-weight:700;opacity:.8}
.fld-list li[aria-selected=true]{font-weight:800}.fld-list li.fld-act,.fld-list li:hover{background:#F4EAD8}
.fld-pop.fld-dk .fld-list li.fld-act,.fld-pop.fld-dk .fld-list li:hover{background:#343847}
.fld-list .fld-none{cursor:default;opacity:.75}
.fld-sr{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}`;
  function style() { if (D.getElementById('fldCss')) return; const s = D.createElement('style'); s.id = 'fldCss'; s.textContent = CSS; (D.head || D.documentElement).appendChild(s); }

  /* is this box on a dark background? (the CA look) */
  function dark(el) {
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const m = getComputedStyle(n).backgroundColor.match(/[\d.]+/g);
      if (m && (m.length < 4 || +m[3] > 0.5)) return (0.299 * m[0] + 0.587 * m[1] + 0.114 * m[2]) < 110;
    }
    return false;
  }

  /* ---------- per-field state ---------- */
  let uidN = 0;
  const S = new WeakMap();                 // input → { kind, err, c (country), wrap, btn }
  const kindOf = el => el && el.getAttribute && el.getAttribute('data-field');
  const required = el => el.required || el.hasAttribute('data-required');
  const digitsOnly = v => String(v || '').replace(/\D/g, '');
  const maxOf = (el, st) => st.kind === 'phone' ? st.c.max : st.kind === 'pincode' ? 6 : (+el.getAttribute('data-maxlen') || +el.getAttribute('maxlength') > 0 && +el.getAttribute('maxlength') || 12);

  function errEl(el) {
    const st = S.get(el); if (st.err) return st.err;
    const p = D.createElement('span'); p.className = 'fld-err'; p.id = (el.id || ('fld' + (++uidN))) + '-err'; p.hidden = true; p.setAttribute('aria-live', 'polite');
    const after = st.wrap || el; after.insertAdjacentElement('afterend', p);
    const mb = parseFloat(getComputedStyle(after).marginBottom) || 0; if (mb > 10) p.style.marginTop = (4 - mb) + 'px';
    const db = (el.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean); if (!db.includes(p.id)) db.push(p.id); el.setAttribute('aria-describedby', db.join(' '));
    st.err = p; return p;
  }
  function showErr(el, msg) {
    const st = S.get(el); if (!st) return;
    if (!msg) { if (st.err) { st.err.hidden = true; st.err.textContent = ''; } el.removeAttribute('aria-invalid'); return; }
    const p = errEl(el), dk = dark(el); p.classList.toggle('fld-dk', dk); el.classList.toggle('fld-dkin', dk);
    p.textContent = msg; p.hidden = false; el.setAttribute('aria-invalid', 'true');
  }
  const hasErr = el => el.getAttribute('aria-invalid') === 'true';

  // the message for a field's current value ('' = fine)
  function message(el) {
    const st = S.get(el); if (!st) return '';
    const v = st.kind === 'board' ? el.value : el.value.trim(), empty = !v;
    const lbl = el.getAttribute('data-label');
    if (empty) return required(el) ? (el.getAttribute('data-err-empty') || ({ phone: 'Please enter a mobile number.', email: 'Please enter an email address.', pincode: 'Please enter the 6-digit PIN code.', board: 'Please choose the board.' }[st.kind]) || (lbl ? 'Please enter ' + lbl + '.' : 'Please fill this in.')) : '';
    if (st.kind === 'text') return v.length < (+el.getAttribute('data-minlen') || 1) ? (el.getAttribute('data-err-empty') || (lbl ? 'Please enter ' + lbl + '.' : 'Please fill this in.')) : '';
    if (st.kind === 'email') return emailOk(v) ? '' : 'Please enter a valid email, like name@school.com';
    if (st.kind === 'pincode') return pinOk(v) ? '' : (/^0/.test(v) ? 'A PIN code does not start with 0.' : 'Please enter the 6-digit PIN code.');
    if (st.kind === 'phone') return phoneMsg(st.c, digitsOnly(v));
    if (st.kind === 'digits') {
      if (!/^[0-9]+$/.test(v)) return 'Please use digits only.';
      const n = +v, mn = el.getAttribute('data-min'), mx = el.getAttribute('data-max');
      if ((mn != null && n < +mn) || (mx != null && n > +mx)) return mn != null && mx != null ? `Please enter a number from ${(+mn).toLocaleString('en-IN')} to ${(+mx).toLocaleString('en-IN')}.` : mn != null ? `Please enter at least ${mn}.` : `Please enter at most ${(+mx).toLocaleString('en-IN')}.`;
    }
    return '';
  }

  /* ---------- typing rules for digit boxes ---------- */
  function setDigits(el, d, caretDigits) {
    const st = S.get(el), max = maxOf(el, st);
    if (st.kind === 'phone' && st.c.iso === 'IN') d = d.replace(/^0+/, '');      // 0 98765… → 98765…
    d = d.slice(0, max);
    if (el.value !== d) {
      el.value = d;
      if (caretDigits != null && D.activeElement === el) { const p = Math.min(caretDigits, d.length); try { el.setSelectionRange(p, p); } catch (e) {} }
    }
  }
  function digitBox(el) {
    const st = S.get(el);
    if (el.type === 'number' || el.type === 'email') el.type = 'text';
    if (st.kind !== 'phone') el.setAttribute('inputmode', 'numeric'); else { el.type = 'tel'; el.setAttribute('inputmode', 'numeric'); }
    el.setAttribute('pattern', '[0-9]*'); el.setAttribute('autocomplete', el.getAttribute('autocomplete') || (st.kind === 'pincode' ? 'postal-code' : st.kind === 'phone' ? 'tel-national' : 'off'));
    el.setAttribute('maxlength', maxOf(el, st));
    el.addEventListener('keydown', e => {
      if (e.ctrlKey || e.metaKey || e.altKey || e.isComposing || !e.key || e.key.length !== 1) return;   // Backspace, Tab, arrows, Ctrl+V…
      if (!/[0-9]/.test(e.key)) { e.preventDefault(); return; }
      const sel = (el.selectionEnd || 0) - (el.selectionStart || 0);
      if (!sel && el.value.length >= maxOf(el, st)) e.preventDefault();             // e.g. the 11th digit of an Indian number
    });
    el.addEventListener('beforeinput', e => {
      if (e.inputType === 'insertText' && e.data != null && /[^0-9]/.test(e.data)) e.preventDefault();
    });
    el.addEventListener('paste', e => {
      const t = (e.clipboardData || window.clipboardData) ? (e.clipboardData || window.clipboardData).getData('text') : null; if (t == null) return;
      e.preventDefault();
      const a = el.selectionStart || 0, b = el.selectionEnd || 0;
      if (st.kind === 'phone' && (!el.value || (a === 0 && b === el.value.length))) {   // a whole number pasted: +44 20…, 098765 43210, 91 98765…
        const p = parsePhone(t, st.c.iso); if (p.c !== st.c) setCountry(el, p.c, true); setDigits(el, p.n, p.n.length); after(); return;
      }
      const ins = digitsOnly(t), v = el.value, nv = v.slice(0, a) + ins + v.slice(b);
      setDigits(el, nv, a + ins.length); after();
      function after() { el.dispatchEvent(new Event('input', { bubbles: true })); }
    });
    el.addEventListener('input', () => {
      const v = el.value, c = el.selectionStart == null ? null : digitsOnly(v.slice(0, el.selectionStart)).length;
      if (/\D/.test(v) || v.length > maxOf(el, st) || (st.kind === 'phone' && st.c.iso === 'IN' && /^0/.test(v))) setDigits(el, digitsOnly(v), c);
    });
    if (el.value) setDigits(el, digitsOnly(el.value));
  }

  /* ---------- phone: country button + list ---------- */
  function ccHTML(c) { return `<span class="fld-fl" aria-hidden="true">${c.flag}</span><span>+${c.dial}</span><span class="fld-car" aria-hidden="true">▾</span>`; }
  function setCountry(el, c, quiet) {
    const st = S.get(el); st.c = c; el.setAttribute('data-country', c.iso);
    st.btn.innerHTML = ccHTML(c); st.btn.setAttribute('aria-label', `Country code: ${c.name} +${c.dial}. Change country`);
    el.setAttribute('maxlength', c.max); el.setAttribute('placeholder', c.iso === 'IN' ? '10-digit mobile number' : `${c.min === c.max ? c.min : c.min + '–' + c.max} digits`);
    if (el.value) setDigits(el, digitsOnly(el.value));
    if (!quiet && hasErr(el)) showErr(el, message(el));
  }
  function phone(el) {
    const st = S.get(el), init = parsePhone(el.value, el.getAttribute('data-country') || 'IN');
    const wrap = D.createElement('div'); wrap.className = 'fld-ph';
    const cs = getComputedStyle(el); wrap.style.marginTop = cs.marginTop; wrap.style.marginBottom = cs.marginBottom;
    el.parentNode.insertBefore(wrap, el); wrap.appendChild(el);
    const btn = D.createElement('button'); btn.type = 'button'; btn.className = (el.className + ' fld-cc').trim(); btn.setAttribute('aria-haspopup', 'listbox'); btn.setAttribute('aria-expanded', 'false');
    wrap.insertBefore(btn, el); st.wrap = wrap; st.btn = btn; st.c = init.c;
    el.value = init.n; digitBox(el); setCountry(el, init.c, true);
    btn.addEventListener('click', () => (st.pop ? closePop(el, true) : openPop(el)));
  }
  function openPop(el) {
    const st = S.get(el), id = 'fldL' + (++uidN);
    const pop = D.createElement('div'); pop.className = 'fld-pop' + (dark(st.wrap) ? ' fld-dk' : ''); pop.setAttribute('role', 'dialog'); pop.setAttribute('aria-label', 'Choose country');
    pop.innerHTML = `<input class="fld-q" type="search" role="combobox" aria-expanded="true" aria-autocomplete="list" aria-controls="${id}" aria-label="Search country or code" placeholder="Search country or code" autocomplete="off" autocapitalize="none" spellcheck="false">
      <ul class="fld-list" role="listbox" id="${id}" aria-label="Countries"></ul><span class="fld-sr" aria-live="polite"></span>`;
    st.wrap.appendChild(pop); st.pop = pop; st.btn.setAttribute('aria-expanded', 'true');
    const q = pop.querySelector('.fld-q'), ul = pop.querySelector('ul'), live = pop.querySelector('.fld-sr');
    let list = [], act = 0;
    const paint = () => {
      const t = q.value.trim().toLowerCase().replace(/^\+/, ''), tt = t.replace(/\s/g, '');
      list = !t ? SORTED : SORTED.filter(c => c.name.toLowerCase().includes(t) || c.iso.toLowerCase() === t || (tt && /^[0-9]+$/.test(tt) && c.dial.startsWith(tt)));
      act = Math.max(0, list.indexOf(st.c)); if (t) act = 0;
      ul.innerHTML = list.length ? list.map((c, i) => `<li role="option" id="${id}-${i}" data-i="${i}" aria-selected="${c === st.c}"${i === act ? ' class="fld-act"' : ''}><span aria-hidden="true">${c.flag}</span><span class="fld-nm">${escA(c.name)}</span><span class="fld-dc">+${c.dial}</span></li>`).join('') : '<li class="fld-none" aria-disabled="true">No country found</li>';
      if (list.length) q.setAttribute('aria-activedescendant', id + '-' + act); else q.removeAttribute('aria-activedescendant');
      live.textContent = t ? `${list.length} countr${list.length === 1 ? 'y' : 'ies'}` : '';
    };
    const move = n => { if (!list.length) return; act = (act + n + list.length) % list.length; ul.querySelectorAll('li').forEach((li, i) => li.classList.toggle('fld-act', i === act)); q.setAttribute('aria-activedescendant', id + '-' + act); const li = ul.children[act]; if (li && li.scrollIntoView) li.scrollIntoView({ block: 'nearest' }); };
    const pick = i => { const c = list[i]; if (!c) return; setCountry(el, c); closePop(el, false); el.focus(); };
    q.addEventListener('input', paint);
    q.addEventListener('keydown', e => {
      if (e.key === 'ArrowDown') { e.preventDefault(); move(1); } else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
      else if (e.key === 'Enter') { e.preventDefault(); pick(act); } else if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); closePop(el, true); }
      else if (e.key === 'Tab') closePop(el, false);
    });
    ul.addEventListener('mousedown', e => e.preventDefault());
    ul.addEventListener('click', e => { const li = e.target.closest('li[data-i]'); if (li) pick(+li.dataset.i); });
    st.outside = e => { if (!st.wrap.contains(e.target)) closePop(el, false); };
    setTimeout(() => D.addEventListener('pointerdown', st.outside, true), 0);
    paint(); const cur = ul.children[act]; if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: 'center' });
    q.focus();
  }
  function closePop(el, back) {
    const st = S.get(el); if (!st || !st.pop) return;
    st.pop.remove(); st.pop = null; st.btn.setAttribute('aria-expanded', 'false');
    D.removeEventListener('pointerdown', st.outside, true);
    if (back) st.btn.focus();
  }

  /* A blur error that appears while a finger / mouse is still down would push the Save button away before the tap
     ends (the tap then misses). So while a pointer is down, blur messages wait until it is released and the click ran. */
  let down = false, queue = [];
  const flush = () => { down = false; const q = queue; queue = []; if (q.length) setTimeout(() => q.forEach(f => f()), 0); };
  D.addEventListener('pointerdown', () => { down = true; }, true);
  D.addEventListener('pointerup', flush, true); D.addEventListener('pointercancel', flush, true);
  const later = f => { if (down) queue.push(f); else f(); };

  /* ---------- enhance ---------- */
  function enhanceOne(el) {
    const kind = kindOf(el); if (!kind || S.has(el) || !/^(phone|pincode|email|digits|board|text)$/.test(kind)) return;
    style(); S.set(el, { kind, err: null, c: COUNTRIES[0], wrap: null, btn: null, pop: null });
    if (kind === 'phone') phone(el);
    else if (kind === 'pincode' || kind === 'digits') digitBox(el);
    else if (kind === 'email') {
      el.setAttribute('autocapitalize', 'none'); el.setAttribute('spellcheck', 'false'); if (!el.getAttribute('inputmode')) el.setAttribute('inputmode', 'email');
      el.addEventListener('blur', () => { const n = normEmail(el.value); if (n !== el.value) el.value = n; });
    }
    if (kind === 'board' && el.tagName === 'SELECT' && !el.options.length) el.innerHTML = boardOptions(el.getAttribute('data-value') || '');
    // errors: shown on blur (when something was typed) / submit; cleared as soon as the value is fine
    el.addEventListener(kind === 'board' ? 'change' : 'input', () => {
      const m = message(el);
      if (!m) showErr(el, '');
      else if (hasErr(el)) showErr(el, m);
      else if (kind === 'phone' && S.get(el).c.iso === 'IN' && /^[0-5]/.test(el.value)) showErr(el, m);   // say it at once: Indian mobiles start 6–9
    });
    el.addEventListener('blur', () => later(() => {
      if (kind === 'phone' && S.get(el).pop) return;
      if (el.value.trim() || hasErr(el)) showErr(el, message(el));
    }));
  }
  function enhance(root) {
    root = root || D; const q = 'input[data-field],select[data-field],textarea[data-field]';
    if (root.matches && root.matches(q)) enhanceOne(root);
    if (root.querySelectorAll) root.querySelectorAll(q).forEach(enhanceOne);
    return root;
  }
  const visible = el => !el.disabled && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
  function valid(root, opt) {
    root = root || D; enhance(root); opt = opt || {};
    let first = null;
    root.querySelectorAll('[data-field]').forEach(el => {
      if (!S.has(el) || !visible(el)) return;
      if (S.get(el).kind === 'email') el.value = normEmail(el.value);
      const m = message(el); showErr(el, m); if (m && !first) first = el;
    });
    if (first && opt.focus !== false) { try { first.focus(); if (first.scrollIntoView) first.scrollIntoView({ block: 'center', behavior: 'smooth' }); } catch (e) {} }
    return { ok: !first, first };
  }
  // the value to send: phone → E.164 ('' when empty), email → lower case, digits → digits
  function value(el) {
    if (typeof el === 'string') el = D.getElementById(el);
    if (!el) return '';
    const st = S.get(el), v = String(el.value || '').trim();
    if (!st) return v;
    if (st.kind === 'phone') { const n = digitsOnly(v); return n ? '+' + st.c.dial + n : ''; }
    if (st.kind === 'email') return normEmail(v);
    if (st.kind === 'pincode' || st.kind === 'digits') return digitsOnly(v);
    return v;
  }
  function setValue(el, v) {
    if (typeof el === 'string') el = D.getElementById(el);
    const st = el && S.get(el); if (!st) { if (el) el.value = v == null ? '' : v; return; }
    if (st.kind === 'phone') { const p = parsePhone(v, st.c.iso); setCountry(el, p.c, true); el.value = ''; setDigits(el, p.n); }
    else el.value = v == null ? '' : v;
    showErr(el, '');
  }
  function reset(root) {
    (root || D).querySelectorAll('[data-field]').forEach(el => { const st = S.get(el); if (!st) return; showErr(el, ''); if (st.kind === 'phone') setCountry(el, byIso(el.getAttribute('data-default-country') || 'IN'), true); });
  }

  window.Fields = {
    enhance, valid, value, set: setValue, reset, showError: showErr, message,
    email: v => emailOk(v), emailMsg: v => emailOk(v) ? '' : 'Please enter a valid email, like name@school.com', normEmail,
    pincode: v => pinOk(String(v || '').trim()),
    phone: v => e164Ok(String(v || '')), parsePhone: (v, iso) => { const p = parsePhone(v, iso); return { iso: p.c.iso, dial: p.c.dial, national: p.n, e164: p.n ? '+' + p.c.dial + p.n : '' }; },
    boardOptions, BOARDS: BOARDS.map(b => ({ value: b[0], label: b[1] })), COUNTRIES: COUNTRIES.map(c => Object.assign({}, c))
  };

  /* upgrade marked inputs by themselves, also in sheets added later */
  const auto = () => { enhance(D); if (window.MutationObserver && D.body) { let t = 0; new MutationObserver(() => { if (!t) t = requestAnimationFrame(() => { t = 0; enhance(D); }); }).observe(D.body, { childList: true, subtree: true }); } };
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', auto); else auto();
})();
