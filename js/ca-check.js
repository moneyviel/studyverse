/* ================= CA answer checker (js/ca-check.js) — loaded after js/ca-tools.js =================
   Students no longer mark their own written answers. This file marks them automatically, offline, against the
   question's marking scheme, and is built so that paid AI examiners can replace or augment it later.

   CA.checkAnswer(attempt) → result      (synchronous, offline; the single entry point for every screen)
     attempt = { question: <unit question with scheme[]>, answer: { text, table }, photos?: [..] | n, unit?, qid? }
       table = the writing pad's value ({schema:'ca-pad/1', sheets:[{tpl, name, flat:{kind, cols, rows, account?}}]})
               or a legacy {cols, rows}
     result  = { schema:'ca-check/1', provider:'offline', status:'checked'|'partial'|'pending'|'waiting',
                 total, max (marks checked now), full (question marks), pendingMarks,
                 points:[{id, pt, m, skill, status:'correct'|'partial'|'wrong'|'missing'|'pending', marks, found[], expected[], remark}],
                 extras:[{kind:'row'|'sentence', text}], remarks:[…triggered `wrong` remarks], pending:[point ids], tips:[{kind, text}] }
   CA.provider = 'offline' | 'ai'   CA.checkAnswerAI(attempt) → Promise(result)   (AI path stubbed — see content/ca/README.md)
   CA.tfReason(item, text)          mock-paper true/false reason check
   CA.reportHTML(result, q, opts)   the examiner-style report used by the Write tab, the question bank and mock papers

   The core below is the twin of check_answer() in tools/ca_vivamatch.py: both must return the same result
   (tools/ca_validate.py proves it on every model answer through tools/ca_vivaparity.js). The award rule is documented there
   and in content/ca/README.md. */
(function () {
  'use strict';

  /* ================= checker core (keep identical to check_answer in tools/ca_vivamatch.py) ================= */
  function makeChecker(M) {
    const { pairs, tokens, clauses, phraseIn, same, kwSame, pointHit, isNum } = M;
    const SIDEW = { dr: 'debited', cr: 'credited', add: 'added', less: 'deducted', '': 'shown' };
    const sideW = s => (Object.prototype.hasOwnProperty.call(SIDEW, s) ? SIDEW[s] : s);
    const RE_NUM = /([0-9]+(?:,[0-9]{2,3}(?![0-9]))*)(\.[0-9]+)?(\s*(?:lakhs?|lacs?|crores?)(?![a-z]))?/gi;
    const RE_AMT = /[0-9]+(?:,[0-9]{2,3}(?![0-9]))*(?:\.[0-9]+)?/g;
    const RE_NEG = /(?:^|[^a-z0-9.])[\u2212\-](?:₹|rs\.?\s*)?$|(?:^|[^a-z])minus\s*(?:₹|rs\.?)?\s*$/i, RE_BRO = /\(\s*(?:₹|rs\.?)?\s*$/i;
    const MON = '(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\\.?';
    const RE_DATE = new RegExp('^(?:[0-9]{1,2}[-/. ]' + MON + '(?:[-/.][0-9a-z]{2,4}| [0-9]{2,4})?|' + MON + ' [0-9]{1,2}(?![0-9,])|[0-9]{1,2}[-/.][0-9]{1,2}[-/.][0-9]{2,4}|\\([0-9a-z]{1,4}\\)|[0-9]{1,2}[.)](?![0-9]))\\s*', 'i');
    const RE_SENT = /[;!?\n]|(?<![0-9])\.|\.(?![0-9])/;
    const RE_SEC = /^(add|less)(?![a-z])\s*:?\s*(.*)$/i;
    const RE_PART = /particular|account|name|basis|ledger|supplier|customer|party|drawer|item|head/i;
    const STD = ['dr', 'cr', 'add', 'less', ''];
    const PENDING_AI = 'Will be checked by AI examiners (coming soon)';
    const PENDING_NOKEY = 'Not auto-checkable yet — will be checked by AI examiners (coming soon)';
    const WAITING_PHOTO = 'Photo answer — waiting for AI examiners';
    const r2 = x => Math.floor(x * 100 + 0.5) / 100;
    const near = (x, n) => Math.abs(x - n) <= Math.max(Math.min(0.5, Math.max(Math.abs(n) * 0.005, 0.01)), Math.abs(n) * 0.0005);   // sign included; small figures within 0.5% (52.5 ≠ 53), large within 0.05%
    const _str = x => (x == null ? '' : typeof x === 'string' ? x : String(x));
    const uniq = a => [...new Set(a)];
    function fmtN(v) {
      v = Math.floor(Math.abs(v) * 10000 + 0.5) / 10000;
      const ip = Math.floor(v), fr = v - ip; let s = String(ip);
      if (s.length > 3) { let head = s.slice(0, -3); const parts = []; while (head.length > 2) { parts.unshift(head.slice(-2)); head = head.slice(0, -2); } if (head) parts.unshift(head); s = parts.concat([s.slice(-3)]).join(','); }
      if (fr > 1e-9) { const d = fr.toFixed(4).slice(1).replace(/0+$/, ''); if (d !== '.') s += d; }
      return s;
    }
    function numsIn(text, cellsMode) {   // signed; (30) counts as 30 and −30; '₹5,690 crore' gives 5690 and the scaled figure
      const out = [], t = _str(text); RE_NUM.lastIndex = 0; let m;
      while ((m = RE_NUM.exec(t))) {
        const v = parseFloat(m[1].replace(/,/g, '') + (m[2] || '')), end = m.index + m[0].length, pre = t.slice(Math.max(0, m.index - 8), m.index);
        const neg = RE_NEG.test(pre), br = !neg && RE_BRO.test(pre) && t.slice(end, end + 1) === ')';
        const u = (m[3] || '').trim().toLowerCase(), vals = u ? [v, v * (u.startsWith('cr') ? 10000000 : 100000)] : [v];
        for (const x of vals) { out.push(neg ? -x : x); if (br || (cellsMode && neg)) out.push(br ? -x : x); }   // in table cells a minus (or brackets) is presentation: both signs count
      }
      return out;
    }
    function cellAmt(x) {
      if (typeof x === 'boolean') return null;
      if (typeof x === 'number') return Math.abs(x);
      let t = _str(x).trim().toLowerCase().split('₹').join('').split(' ').join('').split('−').join('-');
      t = t.replace(/^\(|\)$/g, ''); t = t.replace(/^-/, ''); t = t.replace(/^(rs\.?|inr)/, ''); t = t.replace(/(dr|cr)\.?$/, ''); t = t.replace(/^\(|\)$/g, '');
      return /^[0-9]+(,[0-9]{2,3})*(\.[0-9]+)?$/.test(t) ? parseFloat(t.replace(/,/g, '')) : null;
    }
    function cleanAc(s) {
      s = _str(s).replace(/\s+/g, ' ').trim();
      s = s.replace(/^(?:to|by)\s+/i, '');
      s = s.replace(/(?:^|\s)(?:dr|cr)\.?\s*$/i, '');
      if (s.startsWith('(') && s.endsWith(')')) s = s.replace(/^[(\s]+|[)\s]+$/g, '');
      return s.trim();
    }
    const acToks = s => tokens(s).filter(w => w !== 'account');
    const title = s => _str(s).split('|')[0].trim().split(/\s+/).filter(Boolean).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    function acMatch(acc, rt, ct) {
      if (!_str(acc).trim()) return true;
      for (const alt of _str(acc).split('|')) {
        const ps = pairs(alt).filter(p => p[1] !== 'account'); if (!ps.length) continue;
        if (ps.every(p => rt.some(w => kwSame(p, w)))) return true;
        if (ct && ct.length && ps.length >= 2 && ps.some(p => rt.some(w => kwSame(p, w))) && ps.every(p => rt.concat(ct).some(w => kwSame(p, w)))) return true;
      }
      return false;
    }
    function sheetsOf(table) {
      if (!table || typeof table !== 'object') return [];
      if (table.sheets != null) return table.sheets.filter(s => s && typeof s === 'object' && s.flat && Object.keys(s.flat).length).map(s => Object.assign({}, s.flat, { name: s.name || s.tpl || 'Table', title: _str(s.title), ok: !!(s.check && typeof s.check === 'object' && s.check.ok === true) }));
      if (table.cols != null) return [{ cols: table.cols || [], rows: table.rows || [], name: 'Table' }];
      return [];
    }
    function sheetKind(s) {
      if (s.kind) return s.kind;
      const cols = (s.cols || []).map(_str);
      if (cols.length === 5 && cols[0] === 'Date' && cols[1] === 'Particulars' && cols[3].includes('Dr')) return 'journal';
      if ('account' in s) return 'tacc';
      return 'grid';
    }
    function sideOf(h) {
      if (/(^|[^a-z])(dr|debit)(?![a-z])/i.test(h)) return 'dr';
      if (/(^|[^a-z])(cr|credit)(?![a-z])/i.test(h)) return 'cr';
      return '';
    }
    function mkRow(part, side, amt, ctx, src, col) { const ac = cleanAc(part); return { ac, side, amt, ctx: _str(ctx), src, col: _str(col), t: acToks(ac), ct: ctx ? acToks(ctx) : [] }; }
    const pad = (r, n) => (Array.isArray(r) ? r : []).concat(Array(n).fill(''));
    function rowsOfSheet(s) {
      const kind = sheetKind(s), cols = (s.cols || []).map(_str), rows = s.rows || [], ctx = _str(s.account), out = [], n = cols.length;
      if (kind === 'journal') {
        for (let r of rows) {
          r = pad(r, 5); const d = cellAmt(r[3]), c = cellAmt(r[4]);
          if (d == null && c == null) continue;
          const [side, amt] = d != null ? ['dr', d] : ['cr', c];
          if (amt && cleanAc(r[1])) out.push(mkRow(r[1], side, amt, ctx, 'table', side === 'dr' && cols.length > 3 ? cols[3] : (cols.length > 4 ? cols[4] : '')));
        }
        return out;
      }
      if (kind === 'tacc') {
        const h = Math.floor(n / 2);
        for (const k of [0, 1]) {
          const cs = cols.slice(k * h, (k + 1) * h);
          let pi = cs.findIndex(c => /particular/i.test(c));
          if (pi < 0) { pi = cs.findIndex(c => !/date|₹|j\.?f|l\.?f/i.test(c)); if (pi < 0) pi = 0; }
          const am = []; cs.forEach((c, i) => { if (c.includes('₹') && i !== pi) am.push(i); });
          for (const r of rows) {
            const seg = pad(r, n).slice(k * h, (k + 1) * h);
            for (const i of am) { const v = cellAmt(seg[i]); if (v && cleanAc(seg[pi])) out.push(mkRow(seg[pi], k === 0 ? 'dr' : 'cr', v, ctx, 'table', cs[i])); }
          }
        }
        return out;
      }
      let pi = s.part;
      if (pi == null) { pi = cols.findIndex(c => RE_PART.test(c)); if (pi < 0) pi = 0; }
      let am = s.amt;
      if (am == null) {
        am = []; cols.forEach((c, i) => { if (c.includes('₹') && i !== pi) am.push(i); });
        if (!am.length) for (let i = 0; i < n; i++) { if (i === pi) continue; const filled = rows.map(r => (i < (r || []).length ? _str(r[i]).trim() : '')).filter(Boolean); if (filled.length && filled.every(x => cellAmt(x) != null)) am.push(i); }
      }
      /* column segments: a text column after an amount column starts a new segment (two-sided statements:
         Expenditure | ₹ | Income | ₹ or columnar capital accounts); each segment's amounts belong to its particulars column */
      const segs = []; let cur = [], seen = false;
      for (let i = 0; i < n; i++) { if (!am.includes(i) && seen) { segs.push(cur); cur = []; seen = false; } cur.push(i); if (am.includes(i)) seen = true; }
      if (cur.length) segs.push(cur);
      const pj = {};
      for (const sg of segs) {
        const tc = sg.filter(j => !am.includes(j));
        let pc = sg.includes(pi) ? pi : tc.find(j => RE_PART.test(cols[j])); if (pc === undefined) pc = tc.length ? tc[0] : pi;
        for (const i of sg) if (am.includes(i)) pj[i] = pc;
      }
      const pv = Object.values(pj), two = segs.length === 2 && new Set(pv).size === 2, first = pv.length ? Math.min(...pv) : pi;
      let sec = '';
      for (let r of rows) {
        r = pad(r, n); let p = _str(r[pi]).trim();
        const m = RE_SEC.exec(p);
        if (m) { sec = m[1].toLowerCase(); p = m[2].trim(); }
        if (!p && !m) sec = '';
        for (const i of am) {
          const v = cellAmt(r[i]); if (!v) continue;
          const part = pj[i] === pi ? p : _str(r[pj[i]]).trim(); if (!part) continue;
          const sd = sideOf(i < n ? cols[i] : '') || (two ? (pj[i] === first ? 'dr' : 'cr') : sec);
          out.push(mkRow(part, sd, v, ctx, 'table', i < n ? cols[i] : ''));
        }
      }
      return out;
    }
    function textRows(text) {
      const out = []; let sec = '', drSeen = false;
      for (const line of _str(text).split('\n')) {
        let L = line.replace(/\s+/g, ' ').trim(); if (!L) continue;
        const m = RE_SEC.exec(L);
        if (m) { sec = m[1].toLowerCase(); L = m[2].trim(); }
        if (!L) continue;
        L = L.replace(RE_DATE, '');
        const ns = [...L.matchAll(RE_AMT)]; if (!ns.length) continue;
        const md = /(?:^|[^a-z])(dr|cr)\.?(?![a-z])/i.exec(L);
        let side, ac, am;
        if (md) {
          const end = md.index + md[0].length, st1 = end - md[1].length - (md[0].endsWith('.') ? 1 : 0);
          side = md[1].toLowerCase(); ac = L.slice(0, st1);
          const after = ns.filter(x => x.index >= end); am = after.length ? after[0] : ns[ns.length - 1];
          if (side === 'dr') drSeen = true;
        } else if (/^by\s/i.test(L)) { side = 'cr'; am = ns[ns.length - 1]; ac = L.slice(0, am.index); }
        else if (/^to\s/i.test(L)) { side = drSeen ? 'cr' : 'dr'; am = ns[ns.length - 1]; ac = L.slice(0, am.index); }
        else if (sec) { side = sec; am = ns[ns.length - 1]; ac = L.slice(0, am.index); }
        else continue;
        ac = ac.replace(/[\s₹:=\-–—]+$/, ''); ac = ac.replace(/(?:^|\s)(?:rs\.?|inr)$/i, '');
        const amt = parseFloat(am[0].replace(/,/g, ''));
        if (amt && cleanAc(ac)) out.push(mkRow(ac, side, amt, '', 'text'));
      }
      return out;
    }
    function tableText(sheets) {
      const lines = [];
      for (const s of sheets) {
        const cols = (s.cols || []).map(_str), kind = sheetKind(s);
        if (_str(s.title).trim()) lines.push(_str(s.title).trim());
        if (kind === 'grid' && cols.some(c => c.trim())) lines.push(cols.filter(c => c.trim()).join(', '));
        for (const r of s.rows || []) {
          const cells = (r || []).map(x => _str(x).trim().replace(/^[\u2212\-](?=[0-9])/, ''));   // a minus in a statement cell is presentation
          if (!cells.some(Boolean)) continue;
          lines.push(cells.filter(Boolean).join(', '));
          if (kind === 'grid' && cells.length >= 3 && cells[0] && cellAmt(cells[0]) == null)
            for (let i = 1; i < cells.length; i++) if (cells[i] && cellAmt(cells[i]) == null && i < cols.length && cols[i]) lines.push(cols[i] + ' — ' + cells[i]);
        }
      }
      return lines.join('\n');
    }
    function modelAttempt(q) {
      const text = [], sheets = [];
      for (const b of q.model || []) {
        const t = b.t;
        if (t === 'p' || t === 'note') text.push(_str(b.text));
        else if (t === 'wn') text.push((b.title || 'Working note') + ': ' + _str(b.text));
        else if (t === 'list') (b.items || []).forEach(x => text.push(_str(x)));
        else if (t === 'legal') [['provision', 'Provision'], ['facts', 'Facts'], ['analysis', 'Analysis'], ['conclusion', 'Conclusion']].forEach(([k, n]) => text.push(n + ': ' + _str(b[k])));
        else if (t === 'journal') {
          const rows = [];
          for (const e of b.entries || []) {
            (e.lines || []).forEach((l, i) => { if (l.dr != null) rows.push([i === 0 ? _str(e.date) : '', _str(l.ac) + ' Dr.', '', l.dr, '']); else rows.push(['', 'To ' + _str(l.ac), '', '', l.cr]); });
            if (e.narr) rows.push(['', '(' + _str(e.narr) + ')', '', '', '']);
          }
          sheets.push({ ok: true, kind: 'journal', name: b.title || 'Journal', title: _str(b.title), cols: ['Date', 'Particulars', 'L.F.', 'Dr. Amount (₹)', 'Cr. Amount (₹)'], rows });
        } else if (t === 'ledger') {
          const dr = b.dr || [], cr = b.cr || [], rows = [];
          for (let i = 0; i < Math.max(dr.length, cr.length); i++) {
            const a = i < dr.length ? dr[i] : null, c = i < cr.length ? cr[i] : null;
            rows.push((a ? [_str(a.date), _str(a.part), '', a.amt] : ['', '', '', '']).concat(c ? [_str(c.date), _str(c.part), '', c.amt] : ['', '', '', '']));
          }
          if (!b.open) rows.push(['', 'Total', '', dr.reduce((a, x) => a + (x.amt || 0), 0), '', 'Total', '', cr.reduce((a, x) => a + (x.amt || 0), 0)]);
          const nx = b.next;
          if (nx && typeof nx === 'object' && nx.amt) { const bd = [_str(nx.date), (nx.side === 'dr' ? 'To' : 'By') + ' Balance b/d', '', nx.amt]; rows.push(nx.side === 'dr' ? bd.concat(['', '', '', '']) : ['', '', '', ''].concat(bd)); }
          sheets.push({ ok: true, kind: 'tacc', name: b.ac || 'Ledger', title: _str(b.title || b.ac), account: _str(b.ac), cols: ['Dr. Date', 'Dr. Particulars', 'Dr. J.F.', 'Dr. Amount (₹)', 'Cr. Date', 'Cr. Particulars', 'Cr. J.F.', 'Cr. Amount (₹)'], rows });
        } else if (t === 'tb') {
          const tr = b.rows || [];
          sheets.push({ ok: !b.diff, kind: 'grid', name: 'Trial Balance', title: _str(b.title) || ('Trial Balance as at ' + _str(b.date)).trim(), cols: ['Particulars', 'Dr. Amount (₹)', 'Cr. Amount (₹)'],
            rows: tr.map(r => [_str(r.ac), r.dr == null ? '' : r.dr, r.cr == null ? '' : r.cr]).concat([['Total', tr.reduce((a, r) => a + (r.dr || 0), 0), tr.reduce((a, r) => a + (r.cr || 0), 0)]]) });
        } else if (t === 'cashbook') {
          const cols = b.cols || [], dr = b.dr || [], cr = b.cr || [];
          const hd = p => [p + ' Date', p + ' Particulars', p + ' L.F.'].concat(cols.map(c => p + ' ' + _str(c) + ' (₹)'));
          const side = a => (a ? [_str(a.date), _str(a.part), _str(a.lf)].concat((a.v || []).concat(Array(cols.length).fill('')).slice(0, cols.length).map(x => (x ? x : ''))) : Array(3 + cols.length).fill(''));
          const rows = []; for (let i = 0; i < Math.max(dr.length, cr.length); i++) rows.push(side(i < dr.length ? dr[i] : null).concat(side(i < cr.length ? cr[i] : null)));
          const tot = L => ['', 'Total', ''].concat(cols.map((c, k) => L.reduce((a, x) => a + ((x.v || []).concat(Array(cols.length).fill(0))[k] || 0), 0)));
          rows.push(tot(dr).concat(tot(cr)));
          sheets.push({ ok: true, kind: 'tacc', name: 'Cash Book', title: _str(b.title) || 'Cash Book', account: 'Cash Book', cols: hd('Dr.').concat(hd('Cr.')), rows });
        } else if (t === 'table') {
          const sh = { ok: true, kind: 'grid', name: b.title || 'Table', title: _str(b.title), cols: b.head || [], rows: b.rows || [] };
          if (b.num && b.num.length) sh.amt = b.num.slice();
          sheets.push(sh);
        }
      }
      return { text: text.join('\n'), sheets };
    }
    function hits(groups, toks, raws, cl) {
      const hit = [], neg = [], found = [];
      for (const g of groups) {
        const alts = _str(g).split('|').filter(a => a.trim());
        const h = alts.find(a => phraseIn(pairs(a), toks, raws, cl));
        if (h !== undefined) { hit.push(true); neg.push(''); found.push(h.trim()); continue; }
        const n = alts.find(a => phraseIn(pairs(a), toks, null, cl));
        hit.push(false); neg.push(n !== undefined ? n.trim() : '');
      }
      return { hit, neg, found };
    }
    const colName = c => _str(c).replace(/\s*\(₹\)\s*/g, ' ').trim() || 'another column';
    const frac = (got, need) => (got >= need ? 1 : need >= 2 && 2 * got >= need ? 0.5 : 0);
    function desc(acc, side, amt) { const parts = [acc || 'Entry']; if (side) parts.push(sideW(side)); if (amt != null) parts.push('₹' + fmtN(amt)); return parts.join(' '); }
    function tier(e, r) {
      const [acc, side, amt] = e;
      const a = acMatch(acc, r.t, r.ct), sd = STD.includes(side) ? (side === '' || r.side === '' || r.side === side) : acMatch(side, acToks(r.col)), am = amt == null || near(r.amt, amt);
      if (a && sd && am) return 4;
      if (a && am) return 3;
      if (a && sd && amt != null) return 2;
      if (sd && am && side !== '' && acc.trim() && amt != null) return 1;
      return -1;
    }
    const expRows = p => (p.rows || []).map(x => { const e = (Array.isArray(x) ? x : []).concat(['', '', null]), amt = e[2]; return [_str(e[0]), _str(e[1]).toLowerCase(), amt == null || amt === '' ? null : Math.abs(+amt)]; });
    function matchRows(E, rows) {
      const best = E.map(() => [-1, -1]), used = new Set();
      E.forEach((e, i) => { for (let j = 0; j < rows.length; j++) if (!used.has(j) && tier(e, rows[j]) === 4) { best[i] = [4, j]; used.add(j); break; } });
      for (const want of [[3, 2], [1, 0]]) {
        E.forEach((e, i) => {
          if (best[i][0] >= 2) return;
          let bt = -1, bj = -1;
          for (let j = 0; j < rows.length; j++) { if (used.has(j)) continue; const t = tier(e, rows[j]); if (want.includes(t) && t > bt) { bt = t; bj = j; } }
          if (bj >= 0) { best[i] = [bt, bj]; if (bt >= 2) used.add(bj); }
        });
      }
      return best;
    }
    function wrongRules(w, say) {
      if (!w || (Array.isArray(w) && !w.length)) return [];
      if (!Array.isArray(w)) w = [w];
      if (w.every(x => typeof x === 'string')) return [{ kw: w, say }];
      return w.filter(x => x && typeof x === 'object' && x.kw && (!Array.isArray(x.kw) || x.kw.length));
    }
    function ruleHit(rule, toks, raws, cl) {
      const kw = Array.isArray(rule.kw) ? rule.kw : [rule.kw];
      const got = kw.filter(g => _str(g).split('|').some(a => a.trim() && phraseIn(pairs(a), toks, raws, cl))).length;
      return got >= (rule.min || kw.length);
    }
    let IGN = null;
    function maskCopied(toks, qt, lim, n = 6) {   // words copied from the question into the text (6+ words in order; figures and 'rupees' skipped) earn no keyword credit; tables never masked
      const W = w => !isNum(w) && w !== 'rupe', qw = qt.filter(W), idx = [];
      for (let i = 0; i < Math.min(lim, toks.length); i++) if (W(toks[i])) idx.push(i);
      if (qw.length < n || idx.length < n) return toks;
      const grams = new Set(); for (let i = 0; i + n <= qw.length; i++) grams.add(qw.slice(i, i + n).join('\u0001'));
      const mask = toks.map(() => false);
      for (let i = 0; i + n <= idx.length; i++) if (grams.has(idx.slice(i, i + n).map(j => toks[j]).join('\u0001'))) idx.slice(i, i + n).forEach(j => { mask[j] = true; });
      return toks.map((t, i) => (mask[i] ? '~' : t));
    }
    function checkAnswer(q, ans) {
      if (!IGN) IGN = new Set(tokens('total totals balance c/d b/d grand subtotal carried brought forward down'));
      ans = ans || {};
      const text = _str(ans.text);
      const sheets = ans.sheets != null ? ans.sheets : sheetsOf(ans.table);
      const ph = ans.photos || 0, nph = typeof ph === 'number' ? ph : ph.length;
      const typed = !!text.trim() || sheets.some(s => (s.rows || []).length);
      const scheme = q.scheme || [];
      const full = r2(scheme.reduce((a, p) => a + (p.m != null ? p.m : 0), 0));
      const base = p => ({ id: p.id, pt: _str(p.pt), m: p.m != null ? p.m : 0, skill: _str(p.skill) });
      if (nph && !typed) {
        const pts = scheme.map(p => Object.assign(base(p), { status: 'pending', marks: 0, found: [], expected: [], remark: WAITING_PHOTO }));
        return { schema: 'ca-check/1', provider: 'offline', status: 'waiting', total: 0, max: 0, full, pendingMarks: full, points: pts, extras: [], remarks: [], pending: pts.map(p => p.id), tips: [] };
      }
      const rows = [];
      sheets.forEach(s => rows.push(...rowsOfSheet(s)));
      rows.push(...textRows(text));
      const cells = sheets.flatMap(s => (s.rows || []).flatMap(r => (r || []).map(_str))).join('\n');
      const c0 = clauses(text + '\n' + tableText(sheets)), raws = c0.raws, cl = c0.cl, toks = maskCopied(c0.toks, tokens(_str(q.q)), clauses(text).toks.length);
      const pool = numsIn(text).concat(numsIn(cells, true));
      const points = [], remarks = [];
      for (const p of scheme) {
        const o = base(p), kw = p.kw || [], nums = p.nums || [], er = p.rows || [], pok = !!p.pad_ok;
        if (p.ai_only || !(kw.length || nums.length || er.length || pok)) { Object.assign(o, { status: 'pending', marks: 0, found: [], expected: [], remark: p.ai_only ? PENDING_AI : PENDING_NOKEY }); points.push(o); continue; }
        const comps = [], found = [], expected = [], notes = []; let evid = false;
        if (kw.length) {
          const { hit, neg, found: fk } = hits(kw, toks, raws, cl), g = hit.filter(Boolean).length;
          let f = frac(g, p.min || kw.length);
          if (f === 0.5 && scheme.some(o => o !== p && JSON.stringify(o.kw || []) === JSON.stringify(kw))) f = 0;   // "any N points": points sharing the same groups are all-or-nothing
          comps.push(f); found.push(...fk);
          if (f < 1) {
            kw.forEach((x, i) => { if (!hit[i]) expected.push(_str(x).split('|')[0].trim()); });
            neg.forEach(x => { if (x) { notes.push('Stated in the negative: "' + x + '"'); evid = true; } });
          }
        }
        if (nums.length) {
          const fn = [], mn = [];
          for (let n of nums) {
            n = parseFloat(n);
            if (pool.some(x => near(x, n))) { fn.push(n); continue; }
            mn.push(n); let cand = null;
            for (const x of pool) { const d = Math.abs(x - n); if (!near(x, n) && d <= 0.25 * Math.abs(n) && (cand === null || d < Math.abs(cand - n))) cand = x; }
            if (cand !== null) { notes.push(fmtN(cand) + ' found — expected ' + fmtN(n)); evid = true; }
          }
          comps.push(fn.length === nums.length ? 1 : nums.length >= 2 && 2 * fn.length >= nums.length ? 0.5 : 0);
          found.push(...fn.map(fmtN)); expected.push(...mn.map(fmtN));
        }
        if (er.length) {
          const E = expRows(p), best = matchRows(E, rows), sc = [];
          E.forEach(([acc, side, amt], i) => {
            const [t, j] = best[i], r = j >= 0 ? rows[j] : null;
            if (t === 4) { sc.push(1); found.push(desc(r.ac, r.side, r.amt)); return; }
            sc.push(t === 3 || t === 2 ? 0.5 : 0);
            if (t === 3) { found.push(desc(r.ac, r.side, r.amt)); notes.push(r.ac + ': ' + (STD.includes(side) ? sideW(r.side) + ' instead of ' + sideW(side) : 'under "' + colName(r.col) + '" instead of "' + side + '"')); evid = true; }
            else if (t === 2) { found.push(desc(r.ac, r.side, r.amt)); notes.push(r.ac + ': ₹' + fmtN(r.amt) + ' found — expected ₹' + fmtN(amt)); evid = true; }
            else if (t === 1) { expected.push(desc(title(acc), side, amt)); notes.push('₹' + fmtN(amt) + ' ' + sideW(side) + ' to ' + r.ac + ' — expected ' + title(acc)); evid = true; }
            else if (t === 0) { expected.push(desc(title(acc), side, amt)); notes.push(r.ac + ': ' + sideW(r.side) + ' ₹' + fmtN(r.amt) + ' — expected ' + desc(title(acc), side, amt)); evid = true; }
            else expected.push(desc(title(acc), side, amt));
          });
          const avg = sc.reduce((a, b) => a + b, 0) / sc.length;
          comps.push(sc.every(x => x === 1) ? 1 : avg >= 0.5 ? 0.5 : 0);
        }
        if (pok) {
          const good = sheets.some(s => s.ok === true && (s.rows || []).length);
          comps.push(good ? 1 : 0);
          if (good) found.push('Your table checks out (totals agree)'); else expected.push('Totals that agree in the exam-format table');
        }
        let f = comps.every(c => c === 1) ? 1 : comps.every(c => c === 0) ? 0 : 0.5;
        for (const w of wrongRules(p.wrong, _str(p.say))) {
          if (ruleHit(w, toks, raws, cl)) { const say = _str(w.say) || 'This statement is not correct here.'; notes.push(say); evid = true; f = Math.min(f, 0.5); if (!remarks.includes(say)) remarks.push(say); }
        }
        const st = f === 1 ? 'correct' : f === 0.5 ? 'partial' : evid ? 'wrong' : 'missing';
        Object.assign(o, { status: st, marks: r2(f * o.m), found, expected, remark: notes.join('; ') });
        points.push(o);
      }
      for (const w of wrongRules(q.wrong, _str(q.say))) if (ruleHit(w, toks, raws, cl)) { const say = _str(w.say) || 'This statement is not correct here.'; if (!remarks.includes(say)) remarks.push(say); }
      /* extras: table rows / sentences that match nothing in the model (listed, never deducted) */
      let extras = [];
      const ma = modelAttempt(q), mrows = ma.sheets.flatMap(rowsOfSheet), allE = scheme.flatMap(expRows);
      if ((mrows.length || allE.length) && rows.some(r => r.src === 'table')) {
        for (const r of rows) {
          if (r.src !== 'table' || !r.t.length || r.t.every(w => IGN.has(w))) continue;
          const ok = allE.some(([acc, side, amt]) => acMatch(acc, r.t, r.ct) && (amt == null || near(r.amt, amt))) ||
            mrows.some(m => near(r.amt, m.amt) && r.t.some(a => m.t.some(b => same(a, b))));
          if (!ok) extras.push({ kind: 'row', text: desc(r.ac, r.side, r.amt) });
        }
      }
      const vtext = [ma.text, tableText(ma.sheets), _str(q.q)].concat(scheme.map(p => _str(p.pt)), scheme.flatMap(p => (p.kw || []).flatMap(g => _str(g).split('|').map(_str)))).join('\n');
      const vocab = new Set(tokens(vtext)), vlist = [...vocab];
      for (const sent of text.split(RE_SENT)) {
        const st = tokens(sent).filter(w => !isNum(w)); if (st.length < 4) continue;
        const h = st.filter(w => vocab.has(w) || vlist.some(v => same(w, v))).length;
        if (h * 4 < st.length) extras.push({ kind: 'sentence', text: sent.trim().slice(0, 160) });
      }
      extras = extras.slice(0, 8);
      /* how to avoid this next time: the common mistakes / examiner remarks / tips that share words with the points lost */
      const lost = points.filter(p => ['partial', 'wrong', 'missing'].includes(p.status));
      const poolt = (q.mistakes || []).map(x => ['mistake', _str(x)]).concat((q.remarks || []).map(x => ['remark', _str(x)]), (q.tips || []).map(x => ['tip', _str(x)]));
      const ptok = poolt.map(([, x]) => uniq(tokens(x).filter(w => w.length >= 4 && !isNum(w))));
      const chosen = [];
      for (const p of lost) {
        const pt = tokens(p.pt).filter(w => w.length >= 4 && !isNum(w)); let bi = -1, bs = 1;
        ptok.forEach((xt, i) => { const s = xt.filter(w => pt.some(y => same(w, y))).length; if (s > bs) { bi = i; bs = s; } });
        if (bi >= 0 && !chosen.includes(bi)) chosen.push(bi);
        if (chosen.length >= 4) break;
      }
      if (lost.length && !chosen.length) for (const kind of ['mistake', 'tip']) { const i = poolt.findIndex(x => x[0] === kind); if (i >= 0) chosen.push(i); }
      const tips = chosen.map(i => ({ kind: poolt[i][0], text: poolt[i][1] }));
      const chk = points.filter(p => p.status !== 'pending'), pend = points.filter(p => p.status === 'pending');
      return { schema: 'ca-check/1', provider: 'offline', status: !pend.length ? 'checked' : !chk.length ? 'pending' : 'partial',
        total: r2(chk.reduce((a, p) => a + p.marks, 0)), max: r2(chk.reduce((a, p) => a + p.m, 0)), full, pendingMarks: r2(pend.reduce((a, p) => a + p.m, 0)),
        points, extras, remarks, pending: pend.map(p => p.id), tips };
    }
    function tfReason(item, text) {
      text = _str(text);
      if (!text.trim()) return { ok: false, how: 'none', hits: [], key: [] };
      if (item.kw && item.kw.length) { const { toks, raws, cl } = clauses(text); return { ok: pointHit({ kw: item.kw, min: item.min || item.kw.length }, toks, raws, cl), how: 'kw', hits: [], key: [] }; }
      const reason = _str(item.reason).replace(/^\s*(true|false)(?![a-z])\.?\s*/i, '');
      const st = new Set(tokens(_str(item.s)));
      const key = uniq(tokens(reason).filter(w => w.length >= 4 && !isNum(w) && !st.has(w)));
      const at = tokens(text), hit = key.filter(w => at.some(y => same(w, y)));
      return { ok: hit.length >= Math.min(2, key.length) && hit.length * 100 >= 35 * key.length, how: 'overlap', hits: hit, key };
    }
    return { checkAnswer, modelAttempt, tfReason, fmtN, sheetsOf, rowsOfSheet, textRows, numsIn, cellAmt, tableText };
  }
  /* ================= checker end ================= */

  if (typeof window === 'undefined' || !window.CaTools || !CaTools._m) return;
  const D = document, K = makeChecker(CaTools._m);
  const fmt = n => (n == null || n === '' ? '' : (typeof n === 'number' ? n.toLocaleString('en-IN', { maximumFractionDigits: 2 }) : String(n)));
  const mk = n => `${fmt(n)} mark${n === 1 ? '' : 's'}`;
  const H = s => (typeof esc === 'function' ? esc(s) : String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]));

  /* ---------- provider switch: 'offline' now; 'ai' = the future Supabase Edge Function (3 AI examiners + consensus) ---------- */
  let provider = 'offline';
  try { const v = localStorage.getItem('sv_ca_checker'); if (v === 'ai' || v === 'offline') provider = v; } catch (e) {}
  const AI = { endpoint: null, timeoutMs: 45000 };   // set AI.endpoint (e.g. https://<project>.functions.supabase.co/ca-check) when the backend exists

  function checkAnswer(attempt) {
    attempt = attempt || {}; const q = attempt.question || {}, a = attempt.answer || {};
    const res = K.checkAnswer(q, { text: a.text || '', table: a.table || null, photos: attempt.photos || [] });
    res.question = attempt.qid || q.id || null; if (attempt.unit) res.unit = attempt.unit;
    return res;
  }
  /* request body for the AI examiners (documented in content/ca/README.md, "AI examiners") */
  function aiRequest(attempt, offline) {
    const q = attempt.question || {};
    return { schema: 'ca-ai-check/1', unit: attempt.unit || null, question: attempt.qid || q.id || null, marks: q.marks,
      q: q.q, scheme: (q.scheme || []).map(p => ({ id: p.id, pt: p.pt, m: p.m, skill: p.skill, ai_only: !!p.ai_only })), model: q.model || [],
      answer: { text: (attempt.answer || {}).text || '', table: (attempt.answer || {}).table || null, photos: (attempt.photos || []).map(x => ({ id: x.id, w: x.w, h: x.h })) },
      offline: offline ? { total: offline.total, max: offline.max, points: offline.points.map(p => ({ id: p.id, status: p.status, marks: p.marks })) } : null,
      examiners: 3, consensus: 'median-per-point', transcribe: !!(attempt.photos || []).length };
  }
  /* AI path (stub). Today it resolves to the offline result with ai.status 'unavailable'. With AI.endpoint set it POSTs aiRequest()
     and expects a ca-ai-result/1 body; its points replace the offline ones (pending points get marks), anything missing stays offline. */
  async function checkAnswerAI(attempt) {
    const off = checkAnswer(attempt);
    if (provider !== 'ai' || !AI.endpoint) return Object.assign(off, { ai: { status: 'unavailable', note: 'AI examiners are coming soon — this is the offline check.' } });
    try {
      const ctl = typeof AbortController === 'function' ? new AbortController() : null; const tm = ctl ? setTimeout(() => ctl.abort(), AI.timeoutMs) : 0;
      const r = await fetch(AI.endpoint, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(aiRequest(attempt, off)), signal: ctl ? ctl.signal : undefined });
      clearTimeout(tm); if (!r.ok) throw new Error('HTTP ' + r.status);
      const ai = await r.json(); if (!ai || ai.schema !== 'ca-ai-result/1') throw new Error('bad response');
      const byId = {}; (ai.points || []).forEach(p => { byId[p.id] = p; });
      off.points = off.points.map(p => byId[p.id] ? Object.assign({}, p, byId[p.id], { by: 'ai' }) : p);
      const pend = off.points.filter(p => p.status === 'pending');
      Object.assign(off, { provider: 'ai', status: ai.status || (pend.length ? 'partial' : 'checked'), total: Math.round(off.points.filter(p => p.status !== 'pending').reduce((s, p) => s + (+p.marks || 0), 0) * 100) / 100,
        max: off.points.filter(p => p.status !== 'pending').reduce((s, p) => s + p.m, 0), pendingMarks: pend.reduce((s, p) => s + p.m, 0), pending: pend.map(p => p.id),
        remarks: off.remarks.concat(ai.remarks || []), transcript: ai.transcript || null, ai: { status: 'ok', examiners: ai.examiners || [], agreement: ai.agreement } });
      return off;
    } catch (e) { return Object.assign(off, { ai: { status: 'error', note: String(e && e.message || e) } }); }
  }

  /* ---------- compact record for storage (the full report is re-computed from the saved answer) ---------- */
  const CODE = { correct: 'c', partial: 'h', wrong: 'w', missing: 'm', pending: 'p' };
  function record(res) {
    return { status: res.status === 'waiting' ? 'waiting' : 'auto', score: res.status === 'waiting' ? null : res.total, max: res.max, full: res.full, pend: res.pendingMarks,
      pts: res.points.map(p => [p.id, CODE[p.status] || 'p', p.marks]), skills: res.points.filter(p => p.status !== 'pending').map(p => [p.skill, p.m, p.marks]), nx: res.extras.length, by: res.provider };
  }

  /* ---------- the examiner-style report ---------- */
  const ST = { correct: ['✅', 'Correct', 'ok'], partial: ['½', 'Half marks', 'half'], wrong: ['❌', 'Wrong', 'bad'], missing: ['⚠️', 'Missing', 'miss'], pending: ['🧑‍🏫', 'Not auto-marked', 'pend'] };
  const TIPK = { mistake: 'Common mistake', remark: 'Examiner', tip: 'Tip' };
  function scoreLine(res) {
    if (res.status === 'waiting') return 'Not marked — photo only. Type your key points to get marks';
    if (res.status === 'pending') return `This answer is judged by an examiner (${mk(res.full)}) — not marked automatically`;
    return `${res.pendingMarks ? `${fmt(res.total)} / ${mk(res.max)} marked · ${mk(res.pendingMarks)} for presentation / judgement not auto-marked` : `${fmt(res.total)} / ${mk(res.max)}`}`;
  }
  function pointHTML(p) {
    const [ic, lab, cl] = ST[p.status] || ST.pending;
    const bits = [];
    if (p.status !== 'pending' && p.found.length) bits.push(`<p class="ca-rp-f"><b>Found:</b> ${p.found.map(H).join(' · ')}</p>`);
    if (p.status !== 'pending' && p.status !== 'correct' && p.expected.length) bits.push(`<p class="ca-rp-e"><b>Expected:</b> ${p.expected.map(H).join(' · ')}</p>`);
    if (p.remark) bits.push(`<p class="ca-rp-r">${H(/AI examiners/.test(p.remark) ? 'Not marked automatically — ' + (SKILLTIP[p.skill] || 'present it the way the model answer does to earn it in the exam.') : p.remark)}</p>`);
    return `<li class="ca-rp ${cl}"><span class="ca-rp-i" aria-hidden="true">${ic}</span><div class="ca-rp-b"><div class="ca-rp-h"><span class="ca-rp-t">${H(p.pt)}</span><em class="ca-rp-m">${p.status === 'pending' ? `${fmt(p.m)} pending` : `${fmt(p.marks)} / ${fmt(p.m)}`}</em></div><span class="ca-rp-st">${lab}</span>${bits.join('')}</div></li>`;
  }
  /* what earns each kind of mark in the exam (shown in "How to get more marks") */
  const SKILLTIP = {
    computation: 'Show a working note for every figure — examiners give step marks even when the final answer is wrong.',
    concept: 'Start with the rule or definition in the exact words of the study material.',
    provision: 'Quote the section / standard number first, then the provision in brief.',
    analysis: 'Apply the provision to the facts of the question, one fact at a time.',
    application: 'Use the names, dates and figures given in the question, not general statements.',
    conclusion: 'End with a clear one-line conclusion that answers exactly what was asked.',
    presentation: 'Use the proper format: headings, dates, Dr / Cr columns and narrations, neatly ruled.',
    posting: 'Post each item to the correct account and the correct side (Dr / Cr).',
    classification: 'Classify each item correctly (capital / revenue, asset / liability…) before computing.',
    balancing: 'Total both sides, show the balance c/d and b/d with dates.',
    rectification: 'Show the wrong entry, the correct entry and then the rectifying entry.'
  };
  const SKN = { computation: 'Computation', concept: 'Concept', provision: 'Quoting provisions', analysis: 'Analysis', application: 'Application', conclusion: 'Conclusion', presentation: 'Presentation', posting: 'Posting', classification: 'Classification', balancing: 'Balancing', rectification: 'Rectification' };
  function moreMarks(res) {
    const gains = res.points.filter(p => p.status !== 'correct').map(p => ({ p, g: p.status === 'pending' ? p.m : Math.max(0, p.m - (p.marks || 0)) })).filter(x => x.g > 0).sort((a, b) => b.g - a.g);
    if (!gains.length) return '';
    const weak = [...new Set(gains.filter(x => x.p.status !== 'pending').map(x => SKN[x.p.skill] || x.p.skill).filter(Boolean))];
    return `<div class="ca-rep-av"><h3 class="ca-h3">📈 How to get more marks</h3><ol class="ca-ul">${gains.map(({ p, g }) => `<li><b>+${fmt(g)} mark${g === 1 ? '' : 's'}</b> — ${H(p.pt)}. <span class="ca-note">${H(SKILLTIP[p.skill] || '')}</span></li>`).join('')}</ol>
      ${weak.length ? `<p class="ca-p">🎯 Added to your weak points: <b>${weak.map(H).join(', ')}</b>.</p><button class="btn ghost" type="button" data-caweak>Practise my weak points</button>` : ''}</div>`;
  }
  function reportHTML(res, q, opts = {}) {
    const h = opts.h || 'h2';
    if (res.status === 'waiting') {
      return `<section class="card ca-rep ca-rep-wait" aria-label="Photo answer not marked"><div class="ca-rep-top"><span class="ca-rep-big" aria-hidden="true">📷</span><div><${h} class="ca-h2s">Not marked — photo only</${h}><p class="sub">Handwriting can't be read automatically, so this attempt has no marks.</p></div></div>
        <ul class="ca-ul"><li>To get marks, type the key figures, entries and points from your page in the answer box (or say them with 🎤), keep the photo if you like, and tap “Check my answer”.</li><li>Your typed points are then marked against this question's ${mk(res.full)} scheme, with “How to get more marks”.</li></ul></section>`;
    }
    const pct = res.max ? res.total / res.max : 0;
    const lost = res.points.filter(p => ['partial', 'wrong', 'missing'].includes(p.status));
    return `<section class="card ca-rep" aria-label="Examiner's report">
      <div class="ca-rep-top"><div class="ca-rep-sc ${res.max ? (pct >= .8 ? 's' : pct < .5 ? 'w' : 'm') : ''}" aria-hidden="true"><b>${res.max ? fmt(res.total) : '–'}</b><span>/ ${fmt(res.max || res.full)}</span></div>
        <div><${h} class="ca-h2s">Examiner's report</${h}><p class="ca-rep-line" role="status">${H(scoreLine(res))}</p></div></div>
      <ol class="ca-rep-pts">${res.points.map(pointHTML).join('')}</ol>
      ${res.extras.length ? `<details class="ca-rep-x" open><summary><span aria-hidden="true">➖</span> Extra / not required (${res.extras.length})</summary><ul class="ca-ul">${res.extras.map(x => `<li>${x.kind === 'row' ? '<span class="ca-rep-k">Table row</span> ' : ''}${H(x.text)}</li>`).join('')}</ul><p class="ca-note">${q && q.extra_ok ? 'This question can also give credit for other relevant points in the exam. ' : ''}No marks are deducted for these — but in the exam they cost time.</p></details>` : ''}
      ${res.remarks.length ? `<div class="ca-rep-rm"><h3 class="ca-h3">Examiner's remarks on your answer</h3><ul class="ca-ul ca-miss">${res.remarks.map(x => `<li>${H(x)}</li>`).join('')}</ul></div>` : ''}
      ${moreMarks(res)}
      ${lost.length || res.tips.length ? `<div class="ca-rep-av"><h3 class="ca-h3">How to avoid this next time</h3>${res.tips.length ? `<ul class="ca-ul">${res.tips.map(t => `<li><span class="ca-rep-k">${TIPK[t.kind] || 'Tip'}</span> ${H(t.text)}</li>`).join('')}</ul>` : '<p class="ca-p">Compare your answer with the model below, point by point.</p>'}</div>` : (res.max ? '<p class="ca-rep-ok">Every point checked so far is correct — well done.</p>' : '')}
      <details class="ca-rep-how"><summary>How was this checked?</summary><p class="ca-note">On this phone, against the ICAI-style marking scheme: key words and phrases (with synonyms, word forms and “not” / “never” detection), the figures in your text and tables (₹1,50,000, 150000 or 1.5 lakh all count; ±0.5 rounding), and every table line — account, Dr / Cr side and amount. A point gets full marks when everything it needs is there, half when part is right (for example the right figure on the wrong side). It cannot read handwriting or judge presentation quality — points marked “Not auto-marked” are shown with what earns them in the exam.</p></details>
      </section>`;
  }

  window.CA = {
    checkAnswer, checkAnswerAI, aiRequest, record, reportHTML, scoreLine,
    tfReason: (item, text) => K.tfReason(item, text),
    modelAttempt: q => K.modelAttempt(q), fmtN: K.fmtN,
    get provider() { return provider; }, set provider(v) { if (v === 'ai' || v === 'offline') { provider = v; try { localStorage.setItem('sv_ca_checker', v); } catch (e) {} } },
    ai: AI, _core: K
  };
})();
