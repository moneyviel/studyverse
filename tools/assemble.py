#!/usr/bin/env python3
"""Join chapter part files into one subject file.

Usage: python3 tools/assemble.py <grade> <subject>
Reads   content/_parts/g<grade>-<subject>/ch01.json, ch02.json, ...  (each = one chapter object)
Writes  content/g<grade>/<subject>.json
"""
import json, os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main(grade, subject):
    part_dir = os.path.join(ROOT, "content", "_parts", f"g{grade}-{subject}")
    files = sorted(glob.glob(os.path.join(part_dir, "ch*.json")))
    if not files:
        sys.exit(f"no chapter files in {part_dir}")
    chapters = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            try:
                chapters.append(json.load(fh))
            except Exception as e:
                sys.exit(f"{os.path.relpath(f, ROOT)} is not valid JSON: {e}")
    chapters.sort(key=lambda c: c.get("n", 0))
    out_dir = os.path.join(ROOT, "content", f"g{grade}")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{subject}.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"board": "cbse", "grade": int(grade), "subject": subject, "chapters": chapters}, fh, ensure_ascii=False, indent=1)
    print(f"wrote {os.path.relpath(out, ROOT)} with {len(chapters)} chapters")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
