"""Bump the app version (index.html ?v=, sw.js cache name and ?v=) after a change that is not a unit ship."""
import re
R = __file__.rsplit('/tools/', 1)[0]
sw = open(f'{R}/sw.js').read(); v = int(re.search(r"studyverse-v(\d+)", sw).group(1)); nv = v + 1
sw = sw.replace(f'studyverse-v{v}', f'studyverse-v{nv}').replace(f'?v={v}', f'?v={nv}'); open(f'{R}/sw.js', 'w').write(sw)
ix = open(f'{R}/index.html').read().replace(f'?v={v}', f'?v={nv}'); open(f'{R}/index.html', 'w').write(ix)
print('version', v, '→', nv)
