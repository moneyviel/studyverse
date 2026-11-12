# JEE course content

Each unit is two files:

- `phy/u01.json` holds the concept cards, formula vault, traps, step path and the **real JEE Main questions** (`pyq`). Each real question carries `src` = year, session, date and shift.
- `phy/u01-practice.json` holds **our own practice questions**. There are 12 for every real question, and each is linked to it by `like`.

Build from `tools/jee/` with `python3 build_u01.py`. The build runs these checks and stops on any failure:

1. **Official NTA answer key.** `u01_pyq.py` stores the key for every real question.
2. **Our own code re-computation.** Each real question has a `chk` function that solves it again and must give the same answer as the key.
3. **Independent cross-check.**
   - For the real questions, the same computations are re-run on a dimension table built only from defining equations (`dims.py` → `DEFS`).
   - For the practice questions, `check2.py` re-solves every one by a different method: simulation, numeric perturbation, `Decimal` arithmetic or the definition-built dimension table.
4. **Option integrity.**
   - Every question has 4 distinct options with exactly one marked correct.
   - Numerical answers are integers.
   - We never generate rounding-tie cases.
5. **App check.** Run `python3 tools/jee/app_check.py phy-u01` with `python3 -m http.server 8765` running in the repo root. It answers every question in the real app UI, once right and once wrong. It also checks that no raw markup is left in the rendered text.

Text markup in questions and solutions:

| Markup | Renders as |
| --- | --- |
| `^{x}` | superscript |
| `_{x}` | subscript |
| `\f{a}{b}` | fraction |
| `√{x}` | square root |

To add a unit, copy the three source files (`u01_pyq.py`, `u01_learn.py`, `build_u01.py`), write the generators the unit needs, and add the unit id to `READY` in `js/jee.js`.
