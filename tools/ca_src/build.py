"""Builds every CA unit JSON from its Python source, adds the viva and case-study blocks, and writes the mock papers.
   python3 tools/ca_src/build.py"""
import importlib, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import write_unit
from ca_viva import VIVA
from ca_cases import cases
CASES = cases()
HERE = os.path.dirname(os.path.abspath(__file__))
for f in sorted(glob.glob(os.path.join(HERE, 'fnd_*.py'))):
    m = importlib.import_module(os.path.basename(f)[:-3])
    u = m.build()
    u['viva'] = VIVA.get(u['id'], [])
    u['cases'] = CASES.get(u['id'], [])
    print('wrote', os.path.relpath(write_unit(u)))
for f in sorted(glob.glob(os.path.join(HERE, 'mock_*.py'))):
    m = importlib.import_module(os.path.basename(f)[:-3])
    print('wrote', os.path.relpath(m.write()))
