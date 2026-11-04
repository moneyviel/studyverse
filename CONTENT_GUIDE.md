# StudyVerse content guide

Every subject for a grade lives in one file: `content/g<grade>/<subject>.json`
(for example `content/g6/maths.json`). The app reads these files; no code changes are
needed to add content. Every file must pass `python3 tools/validate.py content/g6/maths.json`
with **zero errors** before it is published.

## Golden rules
1. **Accuracy first.** Every answer must be correct. Solve each question yourself before writing it.
   For maths, add a `check` expression so the checker re-computes the answer (see below).
2. **Own words only.** Follow the official CBSE/NCERT syllabus, but never copy textbook sentences,
   exercises or stories. Write fresh questions, examples and explanations.
3. **Fun and Indian.** Use names, food, festivals, sports, money (₹), places and situations Indian
   children know. Light humour is welcome. Never scary, mean, political, religious-preachy or brand-promoting.
4. **Age-right language.** Grades 1–2: very short sentences, simple words, numbers within the grade's range.
   Grades 3–5: short sentences. Grades 6–10: clear and precise, still friendly.
5. **Explain, don't just mark.** Every question has an `explain` that says *why* the right answer is right
   in 1–3 short sentences, and `steps` for any calculation.
6. **Name the mistake.** `mistake` says what a child who picks a wrong option probably misunderstood
   (e.g. "Adds the denominators when adding fractions"). This powers the Mistake DNA.
7. **Coverage.** Every chapter in `content/curriculum.json` for that grade and subject must appear, in order,
   with the same chapter number. Every topic phrase listed there must be taught somewhere in that chapter.

## File shape
```json
{
  "board": "cbse",
  "grade": 6,
  "subject": "maths",
  "chapters": [
    {
      "n": 1,
      "title": "Patterns in Mathematics",
      "emoji": "🔢",
      "topics": [
        {
          "id": "g6-maths-01-01",
          "title": "Number patterns",
          "learn": {
            "hook": "One fun line that makes the child curious.",
            "points": ["Short key idea 1", "Short key idea 2", "Short key idea 3"],
            "example": { "q": "A worked example question", "steps": ["step 1", "step 2"], "answer": "final answer" },
            "reallife": "Where the child sees this in real life."
          },
          "games": [ ...1 to 3 game objects, see below... ],
          "quiz": [ ...6 to 10 question objects, see below... ],
          "teach": {
            "ask": "Gappu (a confused baby bird) asks the child to explain the idea.",
            "must": [["word", "synonym"], ["another idea", "its synonym"]],
            "praise": "What Gappu says when the explanation is good.",
            "nudge": "What Gappu asks when something important is missing."
          }
        }
      ]
    }
  ]
}
```
* `lab` (optional on a topic): `"angle"` adds the interactive angle lab to the Learn step. Use it for topics about measuring/classifying angles.
* `emoji` on each chapter: one emoji that represents the chapter on the map.
* `id` format: `g<grade>-<subject>-<chapter 2 digits>-<topic 2 digits>`, unique.
* 2–14 topics per chapter. When a depth outline exists (`content/outlines/g<grade>-<subject>.json`), every concept id in it must be listed in some topic's `covers` array (e.g. `"covers": ["c3.2.1", "c3.2.2"]`), and the checker fails the file until all are covered. Each topic: 6–10 quiz questions (Grades 1–2: 5–8), 1–3 games.
* `teach.must`: 2–4 groups; each group is a list of words/phrases (lowercase, any one of which counts).
  For Hindi/Sanskrit use Devanagari words.

## Quiz question
```json
{ "q": "Riya has 3 rows of 4 laddoos. How many laddoos?",
  "options": ["7", "12", "34", "1"],
  "answer": 1,
  "explain": "3 rows of 4 is 4 + 4 + 4 = 12. That is 3 × 4.",
  "steps": ["3 rows × 4 in each row", "3 × 4 = 12"],
  "mistake": "Adds the numbers instead of multiplying",
  "check": "3*4",
  "visual": { "kind": "count", "emoji": "🟡", "n": 12, "groups": 3 } }
```
* `options`: 2–4 unique strings. `answer`: 0-based index of the correct option.
* `steps`: optional list (use it for every calculation).
* `check` (**required for every maths question whose correct option is a number**): a Python
  expression using only numbers, + - * / ** ( ), and `Fraction(a,b)`. The checker evaluates it and it
  must equal the correct option (numbers like "12", "2.5", "3/4", "₹45", "60°", "12 cm" are understood)
  and must NOT equal any other option.
* `visual` (optional, strongly encouraged in maths): an animated picture shown after answering. Kinds:
  * `{"kind":"count","emoji":"🍎","n":12,"groups":3}` – objects, optionally in groups (n ≤ 40)
  * `{"kind":"fraction","num":3,"den":4}` – shaded bar (den ≤ 12)
  * `{"kind":"numberline","from":0,"to":20,"marks":[3,8],"jumps":[[3,8]]}` – hops on a number line (≤ 40 units)
  * `{"kind":"angle","deg":120}` – angle opening (0–360)
  * `{"kind":"clock","h":3,"m":0}` – clock face
  * `{"kind":"bars","items":[["Mon",4],["Tue",7]]}` – bar chart (≤ 8 bars)
  * `{"kind":"shape","name":"triangle"}` – one of circle, triangle, square, rectangle, pentagon, hexagon, cube, cylinder, cone, sphere
  * `{"kind":"compare","a":["Ravi",45],"b":["Meena",62]}` – two bars compared

## Games
* `{"type":"match","title":"Match the pairs","pairs":[["3 × 4","12"],["5 × 2","10"]]}` – 3–6 pairs, left and right sides unique
* `{"type":"sort","title":"Sort them","buckets":["Even","Odd"],"items":[["4",0],["7",1]]}` – 2–3 buckets, 4–10 items, `[text, bucketIndex]`
* `{"type":"order","title":"Put in order","prompt":"Smallest to largest","items":["2","5","9","14"]}` – 3–6 items written in the CORRECT order (the app shuffles)
* `{"type":"truefalse","title":"True or false?","items":[["Every square is a rectangle",true,"A square has 4 right angles and opposite sides equal."]]}` – 4–8 items
* `{"type":"fill","title":"Fill the gap","items":[{"text":"7 + ___ = 10","answer":"3","options":["3","4","2"]}]}` – 3–6 items, `___` appears exactly once, answer is one of options
* `{"type":"speed","title":"Speed round","items":[{"q":"6 × 7","a":"42","check":"6*7"}]}` – 5–10 quick questions with short answers; maths items need `check`

## Hindi / Sanskrit / English
Language files teach reading, vocabulary, grammar and comprehension in the target language with
original short passages (2–6 lines) written by you. Questions about a passage put the passage in
`learn.example.q` or in the question text itself. Never reproduce textbook poems or stories.
