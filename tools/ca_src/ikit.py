"""Small helpers for CA Intermediate unit sources (tools/ca_src/int_*.py). Same JSON schema as Foundation
(content/ca/README.md); MCQs carry their topic (a concept-card title) and a full teaching explanation inline,
and scheme points carry their offline auto-check keywords inline."""
from lib import *                       # noqa: F401,F403  (table, p, ul, note, legal, wn, minutes, Checks, R, inr …)
from ca_viva import P, ALT, V           # noqa: F401
from ca_cases import M                  # noqa: F401


def Q(mid, q, options, answer, explain, concept, topic, difficulty='core', check=None):
    d = {'id': mid, 'q': q, 'options': options, 'answer': answer, 'explain': explain, 'concept': concept, 'topic': topic, 'difficulty': difficulty}
    if check is not None: d['check'] = check
    return d


def S(sid, pt, m, skill, *kw, n=None, nums=None, wrong=None, ai_only=False):
    """scheme point; kw = keyword groups ('a|b' = synonyms), n = groups needed (default all), nums = figures that must appear"""
    d = {'id': sid, 'pt': pt, 'm': m, 'skill': skill}
    if kw: d['kw'] = list(kw); d['min'] = len(kw) if n is None else n
    if nums: d['nums'] = list(nums)
    if wrong: d['wrong'] = wrong
    if ai_only: d['ai_only'] = True
    return d


def W(qid, marks, q, model, scheme, remarks, mistakes, tips, pad='text', difficulty='core', given=None, checks=None, extra_ok=True):
    d = {'id': qid, 'marks': marks, 'minutes': minutes(marks), 'difficulty': difficulty, 'pad': pad, 'q': q, 'model': model, 'scheme': scheme,
         'remarks': remarks, 'mistakes': mistakes, 'tips': tips, 'extra_ok': extra_ok}
    if given: d['given'] = given
    if checks: d['checks'] = checks
    assert abs(sum(s['m'] for s in scheme) - marks) < 1e-9, (qid, 'scheme marks', sum(s['m'] for s in scheme), marks)
    return d


def C(cid, title, body, analogy, work, blocks=None):
    d = {'id': cid, 'title': title, 'body': body, 'analogy': analogy, 'work': work}
    if blocks: d['blocks'] = blocks
    return d


def unit(uid, paper, chapter, n, title, outcomes, meta, concepts, illustrations, jobs, mcqs, questions, revision, quickref, viva, cases, topics=None):
    d = {'schema': 'ca-unit/1', 'id': uid, 'level': 'inter', 'paper': paper, 'chapter': chapter, 'n': n, 'title': title, 'outcomes': outcomes, 'meta': meta,
         'concepts': concepts, 'illustrations': illustrations, 'jobs': jobs, 'mcqs': mcqs, 'questions': questions, 'revision': revision,
         'quickref': [{'k': k, 'v': v} for k, v in quickref], 'viva': viva, 'cases': cases}
    if topics: d['topics'] = topics
    titles = {c['title'] for c in concepts}
    for q in mcqs + [m for cs in cases for m in cs['mcqs']]:
        assert q.get('topic') in titles, (uid, q['id'], 'topic must be a concept title', q.get('topic'))
    return d
