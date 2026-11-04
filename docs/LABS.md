# StudyVerse Concept Labs — builder contract

A **Concept Lab** is a small, hands-on interactive for ONE concept. The child changes something
(drag, tap, slide) and immediately sees the effect, then completes a **challenge**.
Labs must NOT just display text from the lesson.

## Files
* One file per lab type: `js/labs/<type>.js` (plain JavaScript, no build step, no external libraries
  except Three.js for true-3D labs, imported from `../vendor/three.module.min.js`).
* Each file registers itself:

```js
Labs.register('numberline', {
  title: 'Number line jumper',          // short name
  subjects: ['maths'],                   // where it fits
  render(host, p, api) {                 // host = empty <div>, p = params from content data
    host.innerHTML = `...`;              // build UI with SVG / canvas / HTML
    // when the child completes the challenge:
    api.win('You landed on 8! 3 + 5 = 8');
    // optional helpers:
    api.speak('text');                   // read aloud (English or Hindi auto)
    api.sfx('tap'|'coin'|'correct'|'wrong'|'unlock'|'hmm');
    return () => { /* cleanup: stop timers/animation, remove listeners on window */ };
  },
  example: { /* a complete, realistic params object used by the test page */ },
  examples: [ /* 1-3 more params objects showing different uses */ ]
});
```

* For 3D labs (Three.js) use a dynamic import inside render:
  `const THREE = await import('../vendor/three.module.min.js')` (render may be async) and
  `import('../vendor/OrbitControls.js')`.

## Rules (all labs)
1. **Mobile first**: works at 340–400 px wide; height ≤ 440 px; big touch targets (≥ 40 px);
   pointer events (`pointerdown/move/up`) so touch and mouse both work; `touch-action:none` only on
   the draggable area (page must still scroll elsewhere).
2. **Looks great**: bright, friendly colours on white/very light cards; rounded shapes; smooth
   CSS/SVG animation; use the app palette: violet #8b5cf6, mint #2ed3a5, sun #ffc93c, coral #ff6b6b,
   blue #3b82f6, ink #1b1f3a, muted #6b7090. Font is inherited (Nunito / Noto Sans Devanagari).
   Put lab-specific CSS in a `<style>` inside the host, with class names prefixed `lb-<type>-`.
3. **Live feedback**: every change updates numbers/labels/visuals instantly.
4. **Challenge**: show one line "🎯 Challenge: …" from `p.challenge` (or a sensible default you
   generate from p). When achieved, call `api.win(message)` once. Offer a "New challenge" or
   "Reset" button where it makes sense.
5. **Accurate**: all maths/science shown must be correct; label units.
6. **Language**: any text that comes from `p` may be English or Hindi/Sanskrit (Devanagari); never
   assume English. Your own UI words stay short and simple (English).
7. **Self-contained & safe**: no network calls, no alert/confirm, no localStorage, clean up
   everything in the returned cleanup function.
8. **Params validation**: be tolerant — if a param is missing use a sensible built-in default (the app passes ONLY the topic's params; `example` is used only when a topic gives no params at all).

## Test page
`labs-test.html?type=<type>` renders every example of that lab type at phone width.
Open it to check your lab. All labs must render with **zero console errors**.

## Data (how topics use labs)
Lab assignments live in `content/labs/g<grade>-<subject>.json`:
```json
{ "g6-maths-02-01": { "type": "anglemaker", "p": { "challenge": "Make an obtuse angle of 120°", "target": 120 } } }
```
Each topic id maps to one lab. The app shows it in the Learn step under "🧪 Try it".
