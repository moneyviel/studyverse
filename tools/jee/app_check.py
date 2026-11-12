"""Check 5: every JEE question answered through the real app UI (needs `python3 -m http.server 8765` in the repo root).
For each item the stored answer must be accepted as correct, one wrong option must be rejected, and the rendered
text must contain no raw markup (\\f{, ^{, _{, √{)."""
import asyncio, json, sys
from playwright.async_api import async_playwright
UID = sys.argv[1] if len(sys.argv) > 1 else 'phy-u01'
GATE = '''() => { const g=document.getElementById('svGate'); if(g) g.remove(); document.documentElement.classList.remove('sv-gated','sv-boot'); document.querySelectorAll('[data-sv-inert]').forEach(x=>{x.inert=false}); }'''
JS = r'''async ([uid, ids]) => {
  const d = await Jee.data(uid), bad = [], raw = /\\f\{|\^\{|_\{|√\{/;
  for (const id of ids) {
    const q = d.byId[id];
    for (const mode of ['right', 'wrong']) {
      Jee._run(uid, [id], { title: 't' });
      const card = document.querySelector('.jx-q');
      if (raw.test(card.innerText)) bad.push([id, 'raw markup in question/options']);
      if (q.n !== undefined) { const i = document.getElementById('jxN'); i.value = String(mode === 'right' ? q.n : q.n + 3); i.dispatchEvent(new Event('input')); }
      else { const k = mode === 'right' ? q.a : (q.a + 1) % q.o.length; document.querySelector('.jx-o[data-k="' + k + '"]').click(); }
      document.getElementById('jxCheck').click();
      const res = document.querySelector('.jx-res'); const ok = res && res.classList.contains('ok');
      if (mode === 'right' && !ok) bad.push([id, 'correct answer rejected']);
      if (mode === 'wrong' && ok) bad.push([id, 'wrong answer accepted']);
      while (document.getElementById('jxStep')) document.getElementById('jxStep').click();
      if (raw.test(document.querySelector('.jx-sol').innerText)) bad.push([id, 'raw markup in solution']);
    }
  }
  return bad;
}'''
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width': 400, 'height': 860}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.route(lambda u: 'localhost' not in u, lambda r: r.abort())
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.evaluate('''() => { Object.assign(ST, {profile:{name:'T',avatar:'🦊',grade:12,board:'cbse',stream:'science',subjects:['physics','chemistry','maths'],course:null}, jee:{track:'main',cls:12,home:true,units:{},mist:[]}}); save(); }''')
        await pg.reload(); await pg.wait_for_timeout(2000); await pg.evaluate(GATE)
        ids = await pg.evaluate('uid => Jee.data(uid).then(d => Object.keys(d.byId))', UID)
        bad = []
        for i in range(0, len(ids), 100):
            bad += await pg.evaluate(JS, [UID, ids[i:i + 100]])
        print(f'app check: {len(ids)} questions, right + wrong answer each, {len(bad)} problems'); [print(' ', x) for x in bad[:20]]
        if errs: print('page errors:', errs[:5])
        await b.close(); sys.exit(1 if bad or errs else 0)
asyncio.run(main())
