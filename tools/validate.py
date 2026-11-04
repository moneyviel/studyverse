#!/usr/bin/env python3
"""StudyVerse strict content checker.

Usage:  python3 tools/validate.py content/g6/maths.json [more files...]
        python3 tools/validate.py --all

Exits with code 1 if any ERROR is found. Warnings are printed but do not fail.
Checks: file shape, ids, coverage against content/curriculum.json, every answer key,
maths answers re-computed from `check`, wrong options must not also be correct, games,
duplicates, language level, Gappu rubric, visuals.
"""
import json, re, sys, os, glob
from fractions import Fraction
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME_TYPES = {"match", "sort", "order", "truefalse", "fill", "speed"}
VIS = {"count", "fraction", "numberline", "angle", "clock", "bars", "shape", "compare"}
SHAPES = {"circle", "triangle", "square", "rectangle", "pentagon", "hexagon", "cube", "cylinder", "cone", "sphere"}
BANNED_OPTS = re.compile(r"\b(all|none|both) of (the )?(above|these)\b", re.I)


class Report:
    def __init__(self, path):
        self.path, self.errors, self.warnings = path, [], []
    def err(self, where, msg): self.errors.append(f"ERROR   {where}: {msg}")
    def warn(self, where, msg): self.warnings.append(f"warning {where}: {msg}")


def to_number(s):
    """Turn an option like '12', '₹45.50', '3/4', '1 1/2', '60°', '12 cm', '-7', '2,500' into a Fraction."""
    if isinstance(s, (int, float)):
        return Fraction(str(s))
    t = str(s).strip()
    t = t.replace("₹", "").replace("Rs.", "").replace("Rs", "").replace(",", "").replace("−", "-").strip()
    t = re.sub(r"\s*(°|degrees?|cm²|m²|km²|cm³|m³|sq\.?\s*\w+|cu\.?\s*\w+|cm|mm|km|kg|mg|g|ml|l|m|units?|hours?|hrs?|minutes?|mins?|seconds?|secs?|days?|years?|%|paise|rupees|litres?|metres?|grams?)\.?$", "", t, flags=re.I).strip()
    m = re.fullmatch(r"(-?\d+)\s+(\d+)/(\d+)", t)  # mixed number
    if m:
        whole, n, d = int(m[1]), int(m[2]), int(m[3])
        return Fraction(whole) + (Fraction(n, d) if whole >= 0 else -Fraction(n, d))
    m = re.fullmatch(r"(-?\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)", t)
    if m:
        return Fraction(m[1]) / Fraction(m[2])
    m = re.fullmatch(r"-?\d+(?:\.\d+)?", t)
    if m:
        return Fraction(t)
    return None


SAFE_EXPR = re.compile(r"^[\d\s\.\+\-\*/\(\),]*$")

def eval_check(expr):
    e = expr.replace("Fraction", "F")
    stripped = e.replace("F(", "(")
    if not SAFE_EXPR.match(stripped):
        raise ValueError(f"unsafe characters in check '{expr}'")
    # treat every number literal as an exact Fraction so 1/3 stays exact
    e = re.sub(r"(?<![\w.])(\d+(?:\.\d+)?)", lambda m: f"Fr('{m[1]}')", e)
    val = eval(e, {"__builtins__": {}}, {"Fr": Fraction, "F": lambda a, b=1: Fraction(a) / Fraction(b)})
    return Fraction(val)


def approx_equal(a, b):
    if a == b:
        return True
    return abs(float(a) - float(b)) <= 1e-9 + 0.005 * max(1.0, abs(float(b))) and _same_rounding(a, b)

def _same_rounding(a, b):
    # allow options rounded to 2 decimals, e.g. check 22/7*7 vs "22"
    return round(float(a), 2) == round(float(b), 2)


def load_curriculum():
    p = os.path.join(ROOT, "content", "curriculum.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return None


def max_len(grade):
    return 120 if grade <= 2 else 200 if grade <= 5 else 320


def nonempty_str(x):
    return isinstance(x, str) and x.strip() != ""


def check_question(r, where, q, subject, grade, seen_q):
    if not isinstance(q, dict):
        return r.err(where, "question must be an object")
    for k in ("q", "options", "answer", "explain", "mistake"):
        if k not in q:
            r.err(where, f"missing '{k}'")
    if not nonempty_str(q.get("q")):
        return r.err(where, "empty question text")
    text = q["q"].strip()
    key = re.sub(r"\W+", " ", text.lower()).strip()
    if key in seen_q:
        r.err(where, f"duplicate question text (also at {seen_q[key]})")
    seen_q[key] = where
    if len(text) > max_len(grade):
        r.warn(where, f"question is long for Grade {grade} ({len(text)} chars)")
    opts = q.get("options")
    if not isinstance(opts, list) or not (2 <= len(opts) <= 4):
        return r.err(where, "options must be a list of 2-4 items")
    if not all(nonempty_str(o) for o in opts):
        return r.err(where, "every option must be non-empty text")
    norm = [re.sub(r"\s+", " ", o.strip().lower()) for o in opts]
    if len(set(norm)) != len(norm):
        r.err(where, f"options are not unique: {opts}")
    for o in opts:
        if BANNED_OPTS.search(o):
            r.err(where, f"option '{o}' not allowed (options are shuffled)")
    a = q.get("answer")
    if not isinstance(a, int) or not (0 <= a < len(opts)):
        return r.err(where, f"answer index {a!r} is out of range")
    if not nonempty_str(q.get("explain")):
        r.err(where, "explain is empty")
    if not nonempty_str(q.get("mistake")):
        r.err(where, "mistake is empty")
    if "steps" in q and (not isinstance(q["steps"], list) or not all(nonempty_str(s) for s in q["steps"])):
        r.err(where, "steps must be a list of text")
    # numbers in options must be distinct values too (e.g. "0.5" vs "1/2")
    nums = [to_number(o) for o in opts]
    numeric_vals = [n for n in nums if n is not None]
    if len(numeric_vals) == len(opts) and len(set(numeric_vals)) != len(numeric_vals):
        r.err(where, f"two options have the same numeric value: {opts}")
    correct_num = nums[a]
    if "check" in q:
        try:
            val = eval_check(str(q["check"]))
        except Exception as e:
            r.err(where, f"check '{q['check']}' could not be evaluated: {e}")
        else:
            if correct_num is None:
                r.err(where, f"check given but correct option '{opts[a]}' is not a number")
            elif not approx_equal(val, correct_num):
                r.err(where, f"ANSWER KEY WRONG: check {q['check']} = {float(val):g}, but marked answer is '{opts[a]}'")
            for i, n in enumerate(nums):
                if i != a and n is not None and approx_equal(val, n):
                    r.err(where, f"wrong option '{opts[i]}' also equals the checked answer {float(val):g}")
    elif subject == "maths" and correct_num is not None and len(numeric_vals) >= 2:
        r.err(where, f"maths question with numeric answer '{opts[a]}' has no 'check' expression")
    if "visual" in q:
        check_visual(r, where, q["visual"])


def check_visual(r, where, v):
    if not isinstance(v, dict) or v.get("kind") not in VIS:
        return r.err(where, f"visual kind must be one of {sorted(VIS)}")
    k = v["kind"]
    try:
        if k == "count":
            assert isinstance(v["n"], int) and 1 <= v["n"] <= 40 and nonempty_str(v.get("emoji"))
            if "groups" in v:
                assert isinstance(v["groups"], int) and 1 <= v["groups"] <= v["n"]
        elif k == "fraction":
            assert isinstance(v["num"], int) and isinstance(v["den"], int) and 1 <= v["den"] <= 12 and 0 <= v["num"] <= v["den"] * 3
        elif k == "numberline":
            assert isinstance(v["from"], (int, float)) and isinstance(v["to"], (int, float)) and 0 < v["to"] - v["from"] <= 40
            for m in v.get("marks", []):
                assert v["from"] <= m <= v["to"]
            for j in v.get("jumps", []):
                assert len(j) == 2 and all(v["from"] <= x <= v["to"] for x in j)
        elif k == "angle":
            assert 0 <= v["deg"] <= 360
        elif k == "clock":
            assert 1 <= v["h"] <= 12 and 0 <= v["m"] < 60
        elif k == "bars":
            assert 1 <= len(v["items"]) <= 8 and all(nonempty_str(i[0]) and isinstance(i[1], (int, float)) and i[1] >= 0 for i in v["items"])
        elif k == "shape":
            assert v["name"] in SHAPES
        elif k == "compare":
            assert nonempty_str(v["a"][0]) and nonempty_str(v["b"][0]) and v["a"][1] >= 0 and v["b"][1] >= 0
    except (AssertionError, KeyError, TypeError, IndexError):
        r.err(where, f"visual '{k}' has missing or invalid fields: {json.dumps(v, ensure_ascii=False)}")


def check_game(r, where, g, subject):
    if not isinstance(g, dict) or g.get("type") not in GAME_TYPES:
        return r.err(where, f"game type must be one of {sorted(GAME_TYPES)}")
    t = g["type"]
    if not nonempty_str(g.get("title")):
        r.err(where, "game needs a title")
    try:
        if t == "match":
            p = g["pairs"]; assert 3 <= len(p) <= 6
            assert all(len(x) == 2 and nonempty_str(x[0]) and nonempty_str(x[1]) for x in p)
            if len({x[0].strip().lower() for x in p}) != len(p) or len({x[1].strip().lower() for x in p}) != len(p):
                r.err(where, "match: left or right side has duplicates (ambiguous)")
        elif t == "sort":
            b, it = g["buckets"], g["items"]
            assert 2 <= len(b) <= 3 and 4 <= len(it) <= 10
            assert all(len(x) == 2 and nonempty_str(x[0]) and isinstance(x[1], int) and 0 <= x[1] < len(b) for x in it)
            if len({x[0].strip().lower() for x in it}) != len(it):
                r.err(where, "sort: duplicate items")
            if len({x[1] for x in it}) < 2:
                r.err(where, "sort: all items in one bucket")
        elif t == "order":
            it = g["items"]; assert 3 <= len(it) <= 6 and all(nonempty_str(x) for x in it) and nonempty_str(g.get("prompt"))
            if len({x.strip().lower() for x in it}) != len(it):
                r.err(where, "order: duplicate items")
        elif t == "truefalse":
            it = g["items"]; assert 4 <= len(it) <= 8
            assert all(len(x) == 3 and nonempty_str(x[0]) and isinstance(x[1], bool) and nonempty_str(x[2]) for x in it)
            vals = [x[1] for x in it]
            if all(vals) or not any(vals):
                r.warn(where, "truefalse: all answers are the same")
        elif t == "fill":
            it = g["items"]; assert 3 <= len(it) <= 6
            for x in it:
                assert x["text"].count("___") == 1 and nonempty_str(x["answer"])
                assert 2 <= len(x["options"]) <= 4 and x["answer"] in x["options"]
                if len(set(o.strip().lower() for o in x["options"])) != len(x["options"]):
                    r.err(where, f"fill: duplicate options in '{x['text']}'")
        elif t == "speed":
            it = g["items"]; assert 5 <= len(it) <= 10
            for x in it:
                assert nonempty_str(x["q"]) and nonempty_str(str(x["a"]))
                if "check" in x:
                    val = eval_check(str(x["check"])); n = to_number(x["a"])
                    if n is None or not approx_equal(val, n):
                        r.err(where, f"ANSWER KEY WRONG in speed round: '{x['q']}' check={float(val):g} but a='{x['a']}'")
                elif subject == "maths" and to_number(x["a"]) is not None:
                    r.err(where, f"speed item '{x['q']}' has a numeric answer but no check")
    except (AssertionError, KeyError, TypeError, IndexError, AttributeError) as e:
        r.err(where, f"{t}: missing or invalid fields ({type(e).__name__})")
    except ValueError as e:
        r.err(where, f"{t}: {e}")


def check_file(path, curriculum):
    r = Report(path)
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        r.err("file", f"not valid JSON: {e}")
        return r
    grade, subject = d.get("grade"), d.get("subject")
    if not isinstance(grade, int) or not (1 <= grade <= 12):
        r.err("file", "grade must be a number 1-12"); return r
    if not nonempty_str(subject):
        r.err("file", "subject missing"); return r
    exp = f"g{grade}/{subject}.json"
    if not path.replace("\\", "/").endswith(exp):
        r.err("file", f"file should be named content/{exp}")
    chapters = d.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        r.err("file", "no chapters"); return r

    # coverage against the official syllabus map
    cur = None
    if curriculum:
        subs = curriculum.get("grades", {}).get(str(grade), {}).get("subjects", [])
        cur = next((s for s in subs if s.get("id") == subject), None)
        if cur is None:
            r.err("file", f"subject '{subject}' is not in curriculum.json for Grade {grade}")
        else:
            want = [c["n"] for c in cur["chapters"]]
            have = [c.get("n") for c in chapters]
            missing = [n for n in want if n not in have]
            extra = [n for n in have if n not in want]
            if missing: r.err("coverage", f"chapters missing: {missing}")
            if extra: r.err("coverage", f"chapters not in syllabus: {extra}")
            if have != sorted(have): r.err("coverage", "chapters are not in order")

    ids, seen_q, answer_pos, nq = set(), {}, Counter(), 0
    for ci, ch in enumerate(chapters):
        cw = f"ch{ch.get('n', ci+1)}"
        if not nonempty_str(ch.get("title")): r.err(cw, "chapter title missing")
        if cur:
            cc = next((c for c in cur["chapters"] if c["n"] == ch.get("n")), None)
            if cc and cc["title"].strip().lower() != str(ch.get("title", "")).strip().lower():
                r.warn(cw, f"title '{ch.get('title')}' differs from syllabus '{cc['title']}'")
        topics = ch.get("topics")
        if not isinstance(topics, list) or not (2 <= len(topics) <= 5):
            r.err(cw, "each chapter needs 2-5 topics"); continue
        for ti, tp in enumerate(topics):
            tw = f"{cw}/t{ti+1}"
            tid = tp.get("id", "")
            if not re.fullmatch(rf"g{grade}-{re.escape(subject)}-\d{{2}}-\d{{2}}", tid):
                r.err(tw, f"bad id '{tid}' (expected g{grade}-{subject}-NN-NN)")
            if tid in ids: r.err(tw, f"duplicate id {tid}")
            ids.add(tid)
            if not nonempty_str(tp.get("title")): r.err(tw, "topic title missing")
            L = tp.get("learn", {})
            if not nonempty_str(L.get("hook")): r.err(tw, "learn.hook missing")
            if not isinstance(L.get("points"), list) or not (2 <= len(L.get("points", [])) <= 6):
                r.err(tw, "learn.points needs 2-6 items")
            ex = L.get("example")
            if not (isinstance(ex, dict) and nonempty_str(ex.get("q")) and nonempty_str(ex.get("answer"))):
                r.err(tw, "learn.example needs q and answer")
            if not nonempty_str(L.get("reallife")): r.warn(tw, "learn.reallife missing")
            games = tp.get("games", [])
            if not isinstance(games, list) or not (1 <= len(games) <= 3):
                r.err(tw, "needs 1-3 games")
            for gi, g in enumerate(games or []):
                check_game(r, f"{tw}/game{gi+1}", g, subject)
            quiz = tp.get("quiz", [])
            lo = 5 if grade <= 2 else 6
            if not isinstance(quiz, list) or not (lo <= len(quiz) <= 10):
                r.err(tw, f"needs {lo}-10 quiz questions (has {len(quiz) if isinstance(quiz, list) else 0})")
            for qi, q in enumerate(quiz or []):
                check_question(r, f"{tw}/q{qi+1}", q, subject, grade, seen_q)
                if isinstance(q, dict) and isinstance(q.get("answer"), int): answer_pos[q["answer"]] += 1
                nq += 1
            T = tp.get("teach", {})
            if not nonempty_str(T.get("ask")): r.err(tw, "teach.ask missing")
            must = T.get("must")
            if not isinstance(must, list) or not (2 <= len(must) <= 4) or not all(isinstance(m, list) and m and all(nonempty_str(w) for w in m) for m in must):
                r.err(tw, "teach.must needs 2-4 non-empty word groups")
            for k in ("praise", "nudge"):
                if not nonempty_str(T.get(k)): r.err(tw, f"teach.{k} missing")
    r.stats = {"chapters": len(chapters), "topics": len(ids), "questions": nq, "answer_positions": dict(answer_pos)}
    return r


def main(argv):
    if not argv:
        print(__doc__); return 2
    files = sorted(glob.glob(os.path.join(ROOT, "content", "g*", "*.json"))) if argv == ["--all"] else argv
    curriculum = load_curriculum()
    if curriculum is None:
        print("warning: content/curriculum.json not found - coverage not checked")
    total_err = 0
    for p in files:
        r = check_file(p, curriculum)
        for line in r.errors + r.warnings:
            print(f"{os.path.relpath(p, ROOT)}  {line}")
        st = getattr(r, "stats", None)
        status = "PASS" if not r.errors else f"FAIL ({len(r.errors)} errors)"
        print(f"== {os.path.relpath(p, ROOT)}: {status}  {st if st else ''}  warnings={len(r.warnings)}")
        total_err += len(r.errors)
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
