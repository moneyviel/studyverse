#!/usr/bin/env python3
"""Marks every unit that has a content file as built in content/ca/<level>/structure.json (status, file), copies the
unit's ICAI topic headings (`topics` in the unit file, navigation labels only) and recounts. Use it when the ICAI
contents-page text needed by tools/ca_build_structure.py is not at hand:  python3 tools/ca_mark_built.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ca_build_structure import unit_file, ROOT
for lv in ('foundation', 'inter', 'final'):
    p = os.path.join(ROOT, 'content', 'ca', lv, 'structure.json'); s = json.load(open(p, encoding='utf-8')); n = 0
    for pp in s['papers']:
        for c in pp['chapters']:
            for u in c['units']:
                f = unit_file(u['id'])
                if os.path.exists(os.path.join(ROOT, f)):
                    u['status'], u['file'] = 'built', f; n += 1
                    t = json.load(open(os.path.join(ROOT, f), encoding='utf-8')).get('topics')
                    if t and not u.get('topics'): u['topics'] = t
                else: u['status'] = 'soon'; u.pop('file', None)
    s.setdefault('counts', {})['built'] = n
    json.dump(s, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(lv, 'built', n)
