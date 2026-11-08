"""Writes the extra MCQ banks (content/ca/foundation/<paper>/bank/<unit-id>.json) from tools/ca_src/bank_fnd_*.py.
   python3 tools/ca_src/bank_build.py            then   python3 tools/ca_bank_check.py --paper p2 --paper p4
Each bank_fnd_*.py module defines BANK = {unit_id: [Q(...), ...]} and optionally DROP = {unit_id: {'bk03', ...}}
(questions removed after the independent re-answer pass; ids of the remaining questions never change)."""
import glob, importlib, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ca_bank import write

for f in sorted(glob.glob(os.path.join(HERE, 'bank_fnd_*.py'))):
    m = importlib.import_module(os.path.basename(f)[:-3])
    drop = getattr(m, 'DROP', {})
    for uid, items in m.BANK.items():
        path, n = write(uid, items, drop.get(uid, ()))
        print(f'wrote {os.path.relpath(path, os.path.dirname(os.path.dirname(HERE)))}  ({n} MCQs)')
