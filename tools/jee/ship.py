"""After a unit build: register it as ready, add its files to the service-worker cache and bump the app version.
python3 tools/jee/ship.py phy-u11      (reads counts from the built JSON)"""
import json, re, sys, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'); uid = sys.argv[1]; s, n = uid.split('-')
d = json.load(open(f'{R}/content/jee/{s}/{n}.json')); pr = json.load(open(f'{R}/content/jee/{s}/{n}-practice.json'))
npyq, nprac = len(d['pyq']), len(pr['items'] if isinstance(pr, dict) and 'items' in pr else pr if isinstance(pr, list) else pr.get('q', []))
j = open(f'{R}/js/jee.js').read(); m = re.search(r"const READY = \{(.*?)\};", j)
body = re.sub(rf"\s*'{uid}': \{{[^}}]*\}},?", '', m[1]).rstrip(', ')
j = j.replace(m[0], "const READY = {" + body + f", '{uid}': {{ pyq: {npyq}, prac: {nprac} }} }};"); open(f'{R}/js/jee.js', 'w').write(j)
sw = open(f'{R}/sw.js').read(); v = int(re.search(r"studyverse-v(\d+)", sw)[1]); nv = v + 1
f1, f2 = f"'./content/jee/{s}/{n}.json'", f"'./content/jee/{s}/{n}-practice.json'"
if f1 not in sw: sw = sw.replace("'./js/ca-pad.js?v=", f"{f1}, {f2}, './js/ca-pad.js?v=", 1)
sw = sw.replace(f'studyverse-v{v}', f'studyverse-v{nv}').replace(f'?v={v}', f'?v={nv}'); open(f'{R}/sw.js', 'w').write(sw)
ix = open(f'{R}/index.html').read().replace(f'?v={v}', f'?v={nv}'); open(f'{R}/index.html', 'w').write(ix)
print(uid, 'ready:', npyq, 'real,', nprac, 'practice · version', v, '→', nv)
