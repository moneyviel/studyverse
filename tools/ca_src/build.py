"""Builds every CA unit JSON from its Python source.   python3 tools/ca_src/build.py"""
import importlib, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import write_unit
for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fnd_*.py'))):
    m = importlib.import_module(os.path.basename(f)[:-3])
    print('wrote', os.path.relpath(write_unit(m.build())))
