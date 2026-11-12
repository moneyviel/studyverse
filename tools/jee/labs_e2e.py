"""End-to-end: every 'Try it yourself' mission must be completable with real taps / slider drags on a phone viewport."""
import asyncio, sys
from playwright.async_api import async_playwright
GATE = '''() => { const g=document.getElementById('svGate'); if(g) g.remove(); document.documentElement.classList.remove('sv-gated','sv-boot'); document.querySelectorAll('[data-sv-inert]').forEach(x=>{x.inert=false}); }'''
async def setr(pg, sel, v):   # move a range input the way a finger would (value + input event)
    await pg.locator(sel).first.fill(str(v)) if False else await pg.locator(sel).first.evaluate('(i,v)=>{i.value=v;i.dispatchEvent(new Event("input",{bubbles:true}));}', str(v))
async def tap(pg, sel, i=0): await pg.locator(sel).nth(i).scroll_into_view_if_needed(); await pg.locator(sel).nth(i).tap(); await pg.wait_for_timeout(120)
async def tapxy(pg, svg, x, y, W=320):   # tap at SVG user coords
    bb = await pg.locator(svg).bounding_box(); await pg.mouse.click(bb['x'] + x / W * bb['width'], bb['y'] + y / W * bb['height']); await pg.wait_for_timeout(120)
async def open_lab(pg, uid, lab):
    await pg.evaluate(f'() => Jee.unit("{uid}","lab")'); await pg.wait_for_timeout(400); await tap(pg, f'[data-lab="{lab}"]'); await pg.wait_for_timeout(300)
async def missions(pg):
    t = await pg.locator('#jxMis .jx-mis').all_inner_texts() if await pg.locator('#jxMis').count() else await pg.locator('.jx-mis').all_inner_texts(); return [x.startswith('✅') for x in t], t
S = {}
def lab(uid, name):
    def d(f): S[(uid, name)] = f; return f
    return d
@lab('chem-u02', 'bohr')
async def _(pg):
    for a, b in [(3, 2), (2, 1), (4, 1), (4, 2), (4, 3), (3, 1)]:   # tap ON the drawn orbit in the picture
        for n in (a, b): await tapxy(pg, '#jxAtom', 160 + 16 + n * 23, 160)
    await tap(pg, '[data-z="2"]'); await tapxy(pg, '#jxAtom', 160, 160 - (16 + 4 * 23)); await tapxy(pg, '#jxAtom', 160, 160 - (16 + 2 * 23))
    await tap(pg, '[data-z="1"]'); await tap(pg, '#jxIon')

@lab('phy-u17', 'photo')
async def _(pg):
    await tap(pg, '[data-m="2"]'); await setr(pg, '[data-k="lam"]', 450)
    await setr(pg, '[data-k="lam"]', 400); await setr(pg, '[data-k="V"]', 0.35)
    await setr(pg, '[data-k="V"]', 0); await setr(pg, '[data-k="lam"]', 600); await setr(pg, '[data-k="I"]', 100)
    await setr(pg, '[data-k="lam"]', 260)
    await tap(pg, '[data-m="3"]'); await setr(pg, '[data-k="lam"]', 250)
@lab('phy-u17', 'wave')
async def _(pg):
    await setr(pg, '[data-k="V"]', 150); await setr(pg, '[data-k="V"]', 54)
    await tap(pg, '[data-p="1"]'); await setr(pg, '[data-k="V"]', 100)
    await tap(pg, '[data-p="4"]'); await setr(pg, '[data-k="v"]', 45)
@lab('phy-u12', 'circuit')
async def _(pg):
    await tap(pg, '[data-top="par"]')
    for k, v in [('R1', 6), ('R2', 6), ('R3', 6), ('r', 2)]: await setr(pg, f'[data-k="{k}"]', v)
    await tap(pg, '[data-top="mix"]')
    for k, v in [('r', 0), ('E', 12), ('R1', 4), ('R2', 4), ('R3', 4)]: await setr(pg, f'[data-k="{k}"]', v)
    await tap(pg, '[data-top="series"]'); await setr(pg, '[data-k="R1"]', 10)
@lab('chem-u02', 'orbital')
async def _(pg):
    await pg.select_option('#qn', '3'); await pg.wait_for_timeout(100); await pg.select_option('#ql', '0'); await pg.wait_for_timeout(100); await pg.select_option('#qm', '0')
    for _ in range(7): await tap(pg, '#jxAdd')
    for _ in range(3): await tap(pg, '#jxAdd')
    await tap(pg, '#jxAdd5'); await tap(pg, '#jxAdd5')
    for _ in range(4): await tap(pg, '#jxAdd')
    await tap(pg, '[data-o="4s"]'); await tap(pg, '[data-o="3d"]')
async def run_react(pg):
    await tap(pg, '#jxGo'); await pg.wait_for_timeout(9800)
@lab('chem-u08', 'react')
async def _(pg):
    await tap(pg, '[data-n="1"]'); await run_react(pg); await tap(pg, '[data-p="ln"]')
    await tap(pg, '[data-n="0"]'); await run_react(pg)
    await tap(pg, '[data-n="2"]'); await run_react(pg); await tap(pg, '[data-p="inv"]')
    await tap(pg, '#jxMy')
    for _ in range(3):
        await run_react(pg)
        for o in range(3):
            before = await pg.inner_text('#jxGuess'); await tap(pg, f'[data-g="{o}"]')
            if await pg.inner_text('#jxGuess') != before: break
@lab('chem-u08', 'arrh')
async def _(pg):
    await setr(pg, '[data-k="T"]', 298); await setr(pg, '[data-k="Ea"]', 53)
    await setr(pg, '[data-k="T"]', 300); await setr(pg, '[data-k="Ea"]', 70); await setr(pg, '[data-k="Ea"]', 118.5)
    await setr(pg, '[data-k="Ea"]', 80); await setr(pg, '[data-k="T"]', 360); await setr(pg, '[data-k="T"]', 300)
    await tap(pg, '#jxCat')
@lab('chem-u01', 'molemach')
async def _(pg):
    await tap(pg, '[data-q="1"]'); await tap(pg, '[data-s="3"]'); await tap(pg, '[data-q="1"]'); await tap(pg, '[data-s="1"]'); await tap(pg, '[data-q="1"]')
@lab('chem-u01', 'limit')
async def _(pg):
    for r, a, b in [(0, 6, 3), (1, 3, 9), (2, 4, 2), (2, 2, 4), (3, 8, 6)]:
        await tap(pg, f'[data-r="{r}"]'); await setr(pg, '[data-k="a"]', a); await setr(pg, '[data-k="b"]', b); await tap(pg, '#jxFire')
@lab('math-u06', 'pattern')
async def _(pg):
    for k, v in [('a', 5), ('d', 5), ('n', 10)]: await setr(pg, f'[data-v="{k}"]', v)
    for k, v in [('d', -1), ('n', 11)]: await setr(pg, f'[data-v="{k}"]', v)
    for k, v in [('a', 1), ('d', 2), ('n', 6)]: await setr(pg, f'[data-v="{k}"]', v)
    await tap(pg, '[data-k="gp"]'); await setr(pg, '[data-v="r"]', 0.5); await setr(pg, '[data-v="r"]', -0.5)
@lab('math-u06', 'tele')
async def _(pg):
    await setr(pg, '#jxN', 10)
    for sname, n in [('t1', 9), ('t2', 8), ('t4', 10)]:
        await tap(pg, f'[data-s="{sname}"]'); await setr(pg, '#jxN', n); await tap(pg, '#jxAll')
@lab('math-u03', 'transform')
async def _(pg):
    for vals in [(1, 1, 1, 1), (0, -1, 1, 0), (-1, 0, 0, 1), (2, 0, 0, 2), (1, 1, 0, 1)]:
        for k, v in zip('abcd', vals): await setr(pg, f'[data-k="{k}"]', v)
@lab('math-u03', 'planes')
async def _(pg):
    for k, v in [('a2', 1), ('b2', 1), ('c2', 0)]: await setr(pg, f'[data-k="{k}"]', v)
    await setr(pg, '[data-k="c2"]', 4)
    for k, v in [('c1', 5), ('a2', 1), ('b2', -1), ('c2', -1)]: await setr(pg, f'[data-k="{k}"]', v)
@lab('phy-u12', 'bridge')
async def _(pg):
    for l in [x / 2 for x in range(2, 199)]:
        await pg.locator('#jxL').evaluate('(i,v)=>{i.value=v;i.dispatchEvent(new Event("input",{bubbles:true}));}', str(l))
        if 'reads ZERO' in await pg.inner_text('.jx-card'): print('    bridge null found at', l); return
    raise SystemExit('bridge: null point not reachable')
async def main(only=None):
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)
        pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.route(lambda u: 'localhost' not in u, lambda r: r.abort())
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.evaluate('''() => { Object.assign(ST,{profile:{name:'T',avatar:'🦊',grade:12,board:'cbse',stream:'science',subjects:['physics'],course:null}, jee:{track:'full',home:true,units:{},mist:[]}}); save(); }''')
        await pg.reload(); await pg.wait_for_timeout(2500); await pg.evaluate(GATE)
        bad = 0
        for (uid, name), f in S.items():
            if only and name not in only: continue
            await open_lab(pg, uid, name); await f(pg); await pg.wait_for_timeout(200)
            ok, txt = await missions(pg)
            print(('PASS ' if all(ok) else 'FAIL ') + f'{uid}/{name}: {sum(ok)}/{len(ok)}')
            for o, t in zip(ok, txt):
                if not o: print('    ✗', t[:90]); bad += 1
        print('page errors:', errs); await b.close(); sys.exit(1 if bad or errs else 0)
asyncio.run(main(sys.argv[1:] or None))
