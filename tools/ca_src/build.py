"""Builds every CA unit JSON from its Python source, adds the viva and case-study blocks, and writes the mock papers.
   python3 tools/ca_src/build.py"""
import importlib, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import write_unit
from ca_viva import VIVA
from ca_cases import cases
CASES = cases()
HERE = os.path.dirname(os.path.abspath(__file__))
ONLY = [a for a in sys.argv[1:] if not a.startswith('-')]   # optional filters, e.g. build.py fnd_p3_ch01 fnd_p3_ch02
FAILED = []
for f in sorted(glob.glob(os.path.join(HERE, 'fnd_*.py')) + glob.glob(os.path.join(HERE, 'int_*.py')) + glob.glob(os.path.join(HERE, 'fin_*.py'))):
    name = os.path.basename(f)[:-3]
    if ONLY and not any(name.startswith(o) for o in ONLY): continue
    try:
        m = importlib.import_module(name)
        u = m.build()
    except Exception as e:   # one unfinished unit must not stop the others (several writers work in parallel)
        FAILED.append(name); print('SKIPPED (error)', name, '-', type(e).__name__, str(e)[:200]); continue
    u['viva'] = u.get('viva') or VIVA.get(u['id'], [])     # new units carry their own viva/cases inside build()
    u['cases'] = u.get('cases') or CASES.get(u['id'], [])
    print('wrote', os.path.relpath(write_unit(u)))
for f in ([] if ONLY else sorted(glob.glob(os.path.join(HERE, 'mock_*.py')))):
    m = importlib.import_module(os.path.basename(f)[:-3])
    print('wrote', os.path.relpath(m.write()))

if FAILED: print('BUILD ERRORS in:', ', '.join(FAILED))
