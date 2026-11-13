#!/usr/bin/env python3
"""Builds content/ca/<level>/structure.json from ICAI's own contents pages.

Source: the ICAI Board of Studies study-material index pages converted to text
("<Level>__<Paper>__...__ICAI - The Institute of Chartered Accountants of India.txt").
Only the STRUCTURE is taken (levels, papers, modules/parts, chapter and unit titles and
their order) -- no text of the study material is copied.

Usage:  python3 tools/ca_build_structure.py /tmp/ca/txt
Built (pilot) units are listed in BUILT below; the app shows every other unit as "coming soon".
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'content', 'ca')

# unit ids that have full content files (content/ca/<level>/<paper>/<chapter>/<unit>.json)
BUILT = {
    'fnd-p1-ch02-u01', 'fnd-p1-ch02-u02', 'fnd-p1-ch02-u03', 'fnd-p1-ch02-u04', 'fnd-p1-ch02-u05', 'fnd-p1-ch02-u06',
    'fnd-p2-ch02-u01',
}

ROMAN = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}
SKIP = re.compile(r'^(Initial [Pp]ages?|Annexure|Appendix|Glossary|Accounting Terminology Glossary|IPR Notice|Quick Links|Crossword|Practice Questions|'
                  r'Questions for Practice|Comprehensive Illustrations|Test Your Knowledge|ANSWERS|Answers to|Overview, Scenario|Section I+V? - Scenario|'
                  r'Section [IV]+ - Scenario|About Notifications|All Intellectual|Institute of Chartered|reproduced or|otherwise, or)', re.I)

# exam pattern per paper (from ICAI model test papers / initial pages provided)
FOUNDATION_PATTERN = {
    'p1': {'mode': 'descriptive', 'marks': 100, 'hours': 3, 'note': 'Question 1 is compulsory; answer any four of the remaining five. Working notes form part of the answer.'},
    'p2': {'mode': 'descriptive', 'marks': 100, 'hours': 3, 'note': 'Written answers. Legal answers are expected with the provision, the facts, the analysis and a conclusion.'},
    'p3': {'mode': 'objective', 'marks': 100, 'hours': 2, 'negative': 0.25, 'note': '100 multiple-choice questions of 1 mark each; one-fourth mark deducted for each wrong answer.'},
    'p4': {'mode': 'objective', 'marks': 100, 'hours': 2, 'negative': 0.25, 'note': 'Multiple-choice questions; one-fourth mark deducted for each wrong answer.'},
}


def clean_text(s):
    s = re.sub(r'\(https?://[^)]*\)', ' ', s, flags=re.S)          # links, even when they wrap lines
    lines = []
    for l in s.split('\n'):
        l = re.sub(r'\s+', ' ', l).strip()
        if not l or re.match(r'^\d+/\d+/\d+, \d+:\d+', l) or l.startswith('https://www.icai.org') or l.startswith('ICAI - The Institute'):
            continue
        lines.append(l)
    return lines


def parse_index(path):
    """Returns header line + list of items in order: ('group', name) | ('chapter', n, title) | ('unit', n, title)"""
    lines = clean_text(open(path, encoding='utf-8', errors='ignore').read())
    head = lines[0] if lines else ''
    items = []
    last = None   # item that a wrapped line may continue
    for l in lines[1:]:
        if l.startswith('IPR Notice'):
            break
        if re.search(r'(Relevant for|Applicable for|New Scheme of|Study Material - |Course - Paper)', l) or re.match(r'^\(?(Section [AB]:.*\)|Applicable|Relevant)', l) or l in ('Paper-5: Indirect Tax Laws',):
            last = None; continue
        m = re.match(r'^(MODULE|Module)[\s-]*(\d+|[IVX]+)$', l)
        if m:
            items.append(['module', m.group(2)]); last = None; continue
        m = re.match(r'^(PART[\s-]*[A-Z]+|PART [IV]+|Part-[IV]+)\s*[:\-–]\s*(.+)$', l)
        if m:
            items.append(['part', re.sub(r'\s+', ' ', l)]); last = None; continue
        m = re.match(r'^SECTION ([IV]+)$', l)
        if m:
            items.append(['section', m.group(1)]); last = None; continue
        m = re.match(r'^Chapter[\s-]*(\d+)\s*:?\s*(.*)$', l)
        if m:
            it = ['chapter', int(m.group(1)), m.group(2).strip()]; items.append(it); last = it; continue
        m = re.match(r'^Unit[\s-]*(\d+|[IVX]+)\s*:?\s*(.*)$', l)
        if m:
            n = m.group(1); n = ROMAN.get(n, None) or int(n)
            it = ['unit', n, m.group(2).strip()]; items.append(it); last = it; continue
        if SKIP.match(l):
            last = None; continue
        if last is not None and l[0].isalnum() or (last is not None and l[0] in '("“'):
            last[2] = (last[2] + ' ' + l).strip()          # wrapped title
    for it in items:
        if it[0] in ('chapter', 'unit'):
            it[2] = re.sub(r'\s+', ' ', it[2]).strip().rstrip(':').strip()
    return head, items


SMALL = {'and', 'of', 'the', 'in', '&'}
def pretty_part(t):
    m = re.match(r'^PART[\s-]*([A-Z]+|[IV]+)\s*[:\-–]\s*(.+)$', t, re.I)
    if not m: return t
    name = m.group(2).strip()
    if name.isupper():
        name = ' '.join(w if w in ('FTP', 'GST') else (w.lower() if w.lower() in SMALL and i else w.capitalize()) for i, w in enumerate(name.split()))
    return f'Part {m.group(1).upper()}: {name}'


def edition_of(path):
    head = ' '.join(clean_text(open(path, encoding='utf-8', errors='ignore').read())[:8])
    m = re.search(r'(Applicable|Relevant) for (.+?(Examinations?|Exams?)(\s+Onwards)?|.+?Onwards)', head)
    return (m.group(1) + ' for ' + m.group(2)).strip() if m else ''


def title_case_fix(t):
    return t.replace(' ,', ',').replace('( ', '(').replace(' )', ')')


def slug(n):
    return f'{n:02d}'


def build_paper(level_key, paper_key, paper_name, sources, pattern=None, group=None, extra=None):
    """sources: list of (section_label or None, index_path)"""
    chapters = []
    multi = len(sources) > 1
    for sec_i, (sec_label, path) in enumerate(sources):
        head, items = parse_index(path)
        cur_group = None; cur_part = None; ch = None; part_i = 0; max_n = 0; restarts = 0
        for it in items:
            if it[0] == 'module':
                cur_group = f'Module {it[1]}'
            elif it[0] == 'part':
                cur_part = pretty_part(it[1]); part_i += 1; cur_group = None
            elif it[0] == 'section':
                cur_group = f'Section {it[1]}'
            elif it[0] == 'chapter':
                n = it[1]
                if n <= max_n:               # numbering restarts in a new part (Part II Other Laws, Part II Customs & FTP)
                    restarts += 1
                max_n = max(max_n, n) if restarts == 0 else n
                sec = sec_label or ('I' * (restarts + 1) if restarts else None)
                cid_sec = (sec.lower() + '-') if sec else ''
                ch = {'id': f'{level_key}-{paper_key}-{cid_sec}ch{slug(n)}', 'n': n, 'title': title_case_fix(it[2]), 'units': []}
                if sec: ch['sec'] = sec
                if cur_group: ch['module'] = cur_group
                if cur_part: ch['part'] = cur_part
                chapters.append(ch)
            elif it[0] == 'unit' and ch is not None:
                u = {'id': f"{ch['id']}-u{slug(it[1])}", 'n': it[1], 'title': title_case_fix(it[2])}
                ch['units'].append(u)
    # fixes for items ICAI lists without a title
    for ch in chapters:
        if not ch['title']:
            ch['title'] = '; '.join(u['title'] for u in ch['units'])
            ch['title_derived'] = True
        for u in ch['units']:
            if not u['title']:
                u['title_derived'] = True
        if not ch['units']:
            ch['units'] = [{'id': f"{ch['id']}-u01", 'n': 1, 'title': ch['title'], 'implicit': True}]
        for u in ch['units']:
            u['status'] = 'built' if (u['id'] in BUILT or os.path.exists(os.path.join(ROOT, unit_file(u['id'])))) else 'soon'  # any unit with a content file is live
            if u['status'] == 'built':
                u['file'] = unit_file(u['id'])
    paper = {'id': f'{level_key}-{paper_key}', 'key': paper_key, 'name': paper_name, 'chapters': chapters}
    if group: paper['group'] = group
    if pattern: paper['pattern'] = pattern
    if extra: paper.update(extra)
    if multi: paper['sections'] = [s for s, _ in sources]
    return paper


def unit_file(uid):
    parts = uid.split('-')                         # section papers: int-p3-a-ch01-u01 -> inter/p3-a/ch01/u01.json
    lv, u, ch = parts[0], parts[-1], parts[-2]; p = '-'.join(parts[1:-2])
    folder = {'fnd': 'foundation', 'int': 'inter', 'fin': 'final'}[lv]
    return f'content/ca/{folder}/{p}/{ch}/{u}.json'


def count(level):
    ch = sum(len(p['chapters']) for p in level['papers'])
    un = sum(len(c['units']) for p in level['papers'] for c in p['chapters'])
    built = sum(1 for p in level['papers'] for c in p['chapters'] for u in c['units'] if u['status'] == 'built')
    return {'papers': len(level['papers']), 'chapters': ch, 'units': un, 'built': built}



# ---------- ICAI topic headings (section titles only, e.g. "1.3 TYPES OF CONTRACTS") for Foundation units ----------
TH=re.compile(r"^\s{0,20}(\d{1,2})\.(\d{1,2})\s+(.{3,90})$")
BAD=re.compile(r'(BUSINESS MATHEMATICS|BUSINESS LAWS|BUSINESS ECONOMICS|STATISTICS|LOGICAL REASONING|ACCOUNTING|QUANTITATIVE APTITUDE)\s*$')
def upratio(t):
    L=[c for c in t if c.isalpha()]; return sum(c.isupper() for c in L)/max(1,len(L))
def heads(path):
    L=open(path,encoding='utf-8',errors='ignore').read().split('\n'); out=[]; seen=set()
    for i,l in enumerate(L):
        m=TH.match(l.rstrip())
        if not m: continue
        t=re.sub(r'\s+',' ',m.group(3)).strip()
        if upratio(t)<0.9 or BAD.search(t) or len(re.sub('[^A-Za-z]','',t))<4 or re.search(r'\d{2,}',t): continue
        nx=L[i+1].strip() if i+1<len(L) else ''
        if nx and upratio(nx)>0.9 and len(nx)<60 and not TH.match(L[i+1]) and re.sub('[^A-Za-z]','',nx) and not BAD.search(nx): t+=' '+re.sub(r'\s+',' ',nx)
        k=(int(m.group(1)),int(m.group(2)))
        if k in seen: continue
        seen.add(k); out.append(t)
    return out
def tc(t):
    small={'and','of','the','in','a','an','to','for','on','by','or','with','through','between','under','as','at','is','be','vs'}
    keep={'GST','IGST','CGST','SGST','LLP','GDP','GNP','NNP','RBI','WTO','II','I','III','IV','AP','GP','MRP','AR','MR','AC','MC','TC','UTGST','NI'}
    ws=t.split(); r=[]
    for i,w in enumerate(ws):
        core=re.sub(r'[^A-Za-z]','',w)
        if core in keep: r.append(w)
        elif core.lower() in small and i: r.append(w.lower())
        else: r.append(w[:1].upper()+w[1:].lower() if w[:1].isalpha() else w[:2]+w[2:].lower())
    s=' '.join(r); s=re.sub(r'Section (\d+)\((\w)\)',lambda m:f'Section {m.group(1)}({m.group(2).lower()})',s)
    return s

FIX = {'Ntms': 'NTMs', 'Fdi': 'FDI', 'Fpi': 'FPI', 'Rtas': 'RTAs', 'Gatt': 'GATT', 'Tu & Mu': 'TU & MU', 'Ofdemand': 'of Demand', '64a': '64A', 'Right of Lien Right of Lien': 'Right of Lien', 'Credit/debit': 'Credit/Debit', 'Calls- In-advance': 'Calls-in-advance', 'Niti Aayog': 'NITI Aayog', 'Post-keynesian': 'Post-Keynesian'}
def foundation_topics(src):
    out = {}
    for f in sorted(glob.glob(os.path.join(src, 'CA - Foundation__Paper-*'))):
        b = os.path.basename(f)
        m = re.search(r'Paper-(\d).*?-(?:p\d-)?ch(\d+)(?:u(\d+))?\.txt$', b)
        if not m: continue
        uid = f'fnd-p{m.group(1)}-ch{int(m.group(2)):02d}-u{int(m.group(3) or 1):02d}'
        ts = []
        for t in (tc(x) for x in heads(f)):
            for a, b2 in FIX.items(): t = t.replace(a, b2)
            if re.search(r'\d+\.\d+', t) or re.search(r'\b(and|between|of|the|Divisible)$', t) or t.endswith(':'): continue
            if t not in ts: ts.append(t)
        if len(ts) >= 3: out[uid] = ts
    return out

def main(src):
    F = lambda *parts: glob.glob(os.path.join(src, '__'.join(parts) + '__ICAI - The Institute*'))[0]
    edition = {}
    levels = {}

    # ---------- Foundation ----------
    names = {'p1': 'Accounting', 'p2': 'Business Laws', 'p3': 'Quantitative Aptitude', 'p4': 'Business Economics'}
    papers = []
    for k, nm in names.items():
        path = F('CA - Foundation', f'Paper-{k[1]} {nm}')
        papers.append(build_paper('fnd', k, nm, [(None, path)], FOUNDATION_PATTERN[k]))
        edition[f'fnd-{k}'] = edition_of(path)
    # Paper 3 chapter 13 is listed by ICAI without a title; mark it.
    tops = foundation_topics(src)
    for p in papers:
        for c in p['chapters']:
            for u in c['units']:
                if u['id'] in tops: u['topics'] = tops[u['id']]
    levels['foundation'] = {'level': 'foundation', 'name': 'CA Foundation', 'papers': papers}

    # ---------- Intermediate ----------
    I = 'CA - Inter'
    inter = [
        ('p1', 'Advanced Accounting', 'Group I', [(None, F(I, 'GROUP I', 'Paper-1 Advanced Accounting'))]),
        ('p2', 'Corporate and Other Laws', 'Group I', [(None, F(I, 'GROUP I', 'Paper-2 Corporate and Other Laws'))]),
        ('p3', 'Taxation', 'Group I', [('A', F(I, 'GROUP I', 'Paper-3 Taxation', 'Section A Income-tax Law')), ('B', F(I, 'GROUP I', 'Paper-3 Taxation', 'Section B Goods and Services Tax'))]),
        ('p4', 'Cost and Management Accounting', 'Group II', [(None, F(I, 'GROUP II', 'Paper-4 Cost and Management Accounting'))]),
        ('p5', 'Auditing and Ethics', 'Group II', [(None, F(I, 'GROUP II', 'Paper-5 Auditing and Ethics'))]),
        ('p6', 'Financial Management and Strategic Management', 'Group II', [('A', F(I, 'GROUP II', 'Paper-6 Financial Management and Strategic Management', 'Section A Financial Management')), ('B', F(I, 'GROUP II', 'Paper-6 Financial Management and Strategic Management', 'Section B Strategic Management'))]),
    ]
    sec_names = {('p3', 'A'): 'Income-tax Law', ('p3', 'B'): 'Goods and Services Tax', ('p6', 'A'): 'Financial Management', ('p6', 'B'): 'Strategic Management'}
    papers = []
    for k, nm, grp, srcs in inter:
        p = build_paper('int', k, nm, srcs, group=grp)
        if 'sections' in p:
            p['sections'] = [{'key': s, 'name': sec_names[(k, s)]} for s in p['sections']]
        for s, path in srcs:
            edition[f'int-{k}' + (f'-{s}' if s else '')] = edition_of(path)
        papers.append(p)
    levels['inter'] = {'level': 'inter', 'name': 'CA Intermediate', 'papers': papers}

    # ---------- Final ----------
    final = [
        ('p1', 'Financial Reporting', 'Group I', 'GROUP I', 'Paper-1 Financial Reporting'),
        ('p2', 'Advanced Financial Management', 'Group I', 'GROUP I', 'Paper-2 Advanced Financial Management'),
        ('p3', 'Advanced Auditing, Assurance and Professional Ethics', 'Group I', 'GROUP I', 'Paper-3 Advanced Auditing, Assurance and Professional Ethics'),
        ('p4', 'Direct Tax Laws & International Taxation', 'Group II', 'GROUP II', 'Paper-4 Direct Tax Laws & International Taxation'),
        ('p5', 'Indirect Tax Laws', 'Group II', 'GROUP II', 'Paper-5 Indirect Tax Laws'),
    ]
    papers = []
    for k, nm, grp, gdir, pdir in final:
        path = F(gdir, pdir)
        p = build_paper('fin', k, nm, [(None, path)], group=grp)
        edition[f'fin-{k}'] = edition_of(path)
        papers.append(p)
    # Final Paper 3, Chapter 14: ICAI's index shows "Unit-1 / Unit-2" without titles; titles are on the units themselves.
    p3 = papers[2]
    for ch in p3['chapters']:
        if ch['n'] == 14:
            names14 = {1: 'Special Features of Audit of Banks', 2: 'Special Features of Audit of Non-Banking Financial Companies (NBFCs)'}
            for u in ch['units']:
                if u.get('title_derived') or not u['title']:
                    u['title'] = names14.get(u['n'], u['title']); u.pop('title_derived', None)
    # Final Paper 5: Part II (Customs & FTP) restarts chapter numbers
    # Final Paper 6 is a case-study paper with no chapters in ICAI's material.
    papers.append({'id': 'fin-p6', 'key': 'p6', 'name': 'Integrated Business Solutions (Multidisciplinary Case Study with Strategic Management)', 'group': 'Group II',
                   'case_study': True, 'chapters': [
                       {'id': 'fin-p6-ch01', 'n': 1, 'title': 'IBS Case Study Digest', 'units': [{'id': 'fin-p6-ch01-u01', 'n': 1, 'title': 'IBS Case Study Digest', 'implicit': True, 'status': 'soon'}]},
                       {'id': 'fin-p6-ch02', 'n': 2, 'title': 'IBS Case Study Digest Volume-II', 'units': [{'id': 'fin-p6-ch02-u01', 'n': 1, 'title': 'IBS Case Study Digest Volume-II', 'implicit': True, 'status': 'soon'}]},
                       {'id': 'fin-p6-ch03', 'n': 3, 'title': "Case Studies Published in Students' Journal", 'units': [{'id': 'fin-p6-ch03-u01', 'n': 1, 'title': "Case Studies Published in Students' Journal", 'implicit': True, 'status': 'soon'}]},
                   ], 'note': 'Open-book style multidisciplinary case studies; ICAI publishes case-study digests rather than chapters.'})
    levels['final'] = {'level': 'final', 'name': 'CA Final', 'papers': papers}

    summary = {}
    for key, lv in levels.items():
        lv['source'] = 'Structure (titles and order) from the ICAI Board of Studies study-material contents pages. Explanations in this app are original.'
        pre = {'foundation': 'fnd', 'inter': 'int', 'final': 'fin'}[key]
        lv['editions'] = {k: v for k, v in edition.items() if k.startswith(pre)}
        lv['counts'] = count(lv)
        summary[key] = lv['counts']
        os.makedirs(os.path.join(OUT, key), exist_ok=True)
        with open(os.path.join(OUT, key, 'structure.json'), 'w', encoding='utf-8') as f:
            json.dump(lv, f, ensure_ascii=False, indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '/tmp/ca/txt')
