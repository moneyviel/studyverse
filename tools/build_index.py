#!/usr/bin/env python3
"""Build compact per-grade search indexes for "Ask Gappu".

Every entry is copied verbatim from reviewed course content (no new text is created),
so answers are exactly as accurate as the validated, reviewed courses.

Usage: python3 tools/build_index.py            # all grades
Writes content/index/gN-<subject>.json
"""
import json, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build(grade):
    cur = json.load(open(os.path.join(ROOT, "content", "curriculum.json")))
    names = {s["id"]: s["name"] for s in cur["grades"].get(str(grade), {}).get("subjects", [])}
    topics, qa = [], []
    for f in sorted(glob.glob(os.path.join(ROOT, "content", f"g{grade}", "*.json"))):
        sid = os.path.basename(f)[:-5]
        d = json.load(open(f))
        for ci, c in enumerate(d["chapters"]):
            for ti, t in enumerate(c["topics"]):
                L = t.get("learn", {})
                ex = L.get("example") or {}
                topics.append({
                    "id": t["id"], "s": sid, "sn": names.get(sid, sid), "ci": ci, "ti": ti,
                    "ch": c["title"], "t": t["title"], "h": L.get("hook", ""), "p": L.get("points", []),
                    "ex": {"q": ex.get("q", ""), "st": ex.get("steps", []), "a": ex.get("answer", "")},
                    "rl": L.get("reallife", ""), "rv": t.get("revise"),
                })
                for qi, q in enumerate(t.get("quiz", [])):
                    try:
                        ans = q["options"][q["answer"]]
                    except Exception:
                        continue
                    qa.append({"id": t["id"], "qi": qi, "q": q.get("q", ""), "a": ans, "e": q.get("explain", "")})
    return {"grade": grade, "topics": topics, "qa": qa}


def main():
    out = os.path.join(ROOT, "content", "index")
    os.makedirs(out, exist_ok=True)
    for g in range(1, 13):
        if not glob.glob(os.path.join(ROOT, "content", f"g{g}", "*.json")):
            continue
        idx = build(g)
        for sid in sorted({t["s"] for t in idx["topics"]}):
            part = {"grade": g, "subject": sid, "topics": [t for t in idx["topics"] if t["s"] == sid],
                    "qa": [q for q in idx["qa"] if q["id"].split("-")[1] == sid]}
            p = os.path.join(out, f"g{g}-{sid}.json")
            with open(p, "w") as fh:
                json.dump(part, fh, ensure_ascii=False, separators=(",", ":"))
        print(f"g{g}: {len(idx['topics'])} topics, {len(idx['qa'])} Q&A")


if __name__ == "__main__":
    main()
