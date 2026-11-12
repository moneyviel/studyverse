/* Knowtopia service worker: makes the app installable and work offline.
   Pages: always try the internet first (so updates show up), fall back to saved copy. */
const CACHE = 'studyverse-v87';
const CORE = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './icons/emblem-128.webp', './icons/logo-full.webp',
  './css/base.css?v=87', './css/app.css?v=87', './js/worlds.js?v=87', './js/visuals.js?v=87', './js/games.js?v=87', './js/app.js?v=87', './js/audio.js?v=87', './js/labs/core.js?v=87', './js/demo.js?v=87', './js/fields.js?v=87', './js/cloud.js?v=87', './js/plans.js?v=87', './js/parent.js?v=87', './js/teach.js?v=87', './js/inst.js?v=87', './js/rt.js?v=87', './js/live.js?v=87', './js/puzzles-core.js?v=87', './js/puzzles.js?v=87', './js/puzzles-worker.js?v=87', './js/playhub.js?v=87', './js/mindpics.js?v=87', './js/guard.js?v=87', './js/voice.js?v=87', './js/suites-gen.js?v=87', './js/suites.js?v=87', './js/mindpool.js?v=87', './js/mindgym.js?v=87', './js/mindplay-gen.js?v=87', './js/mindplay.js?v=87', './js/heartplay-gen.js?v=87', './js/heartplay.js?v=87', './js/rewards.js?v=87', './js/squad.js?v=87', './js/story.js?v=87', './js/exam.js?v=87', './js/practice.js?v=87', './js/tests.js?v=87', './js/ux.js?v=87', './js/nav.js?v=87', './js/review.js?v=87', './js/leave.js?v=87', './js/scope.js?v=87', './js/pz-words.js?v=87', './js/arcade.js?v=87', './js/gen.js?v=87', './js/ask.js?v=87', './js/look.js?v=87', './js/legal.js?v=87', './js/dashboard.js?v=87', './js/insights.js?v=87', './js/gk.js?v=87', './content/gk/daily.json', './content/gk/index.json', './js/ca-gen.js?v=87', './js/ca.js?v=87', './js/ca-pad.js?v=87', './js/ca-tools.js?v=87', './js/ca-speed.js?v=87', './js/ca-check.js?v=87', './js/ca-read.js?v=87', './js/ca-keys-data.js?v=87', './js/ca-keys.js?v=87', './content/ca/foundation/mocks/fnd-p1-m1.json', './content/ca/foundation/structure.json', './content/ca/foundation/weightage.json', './content/ca/inter/structure.json', './content/ca/final/structure.json', './content/ca/motivation.json', './content/ca/foundation/p1/ch02/u01.json', './content/ca/foundation/p1/ch02/u02.json', './content/ca/foundation/p1/ch02/u03.json', './content/ca/foundation/p1/ch02/u04.json', './content/ca/foundation/p1/ch02/u05.json', './content/ca/foundation/p1/ch02/u06.json', './content/ca/foundation/p2/ch02/u01.json', './js/calc.js?v=87', './js/calc-acad-data.js?v=87', './js/calc-acad.js?v=87', './js/stars.js?v=87', './js/sheets.js?v=87', './js/a11y.js?v=87', './js/owner.js?v=87', './js/playready.js?v=87', './legal/delete-account.html', './css/desktop.css?v=87', './js/desktop.js?v=87', './js/scenes.js?v=87', './js/vendor/three.module.min.js', './js/vendor/OrbitControls.js', './content/curriculum.json',
  './legal/index.html', './legal/terms.html', './legal/children.html', './legal/parents.html', './legal/schools.html', './legal/changes.html', './legal/privacy.html', './legal/disclaimer.html', './legal/liability.html', './legal/copyright.html', './legal/refunds.html', './legal/community.html', './legal/accessibility.html', './legal/contact.html', './legal/legal.css', './legal/legal.js'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => Promise.all(CORE.map(u => c.add(u).catch(() => {}))))); self.skipWaiting(); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const u = new URL(req.url);
  if (u.origin !== location.origin && !req.url.includes('fonts.g')) return;   // never answer server (Supabase) calls from the cache
  e.respondWith(
    // pages and app files always check for a newer copy (no 10-minute browser cache), so updates show on the next open
    fetch(req, u.origin === location.origin ? { cache: 'no-cache' } : undefined).then(res => {
      if (res.ok && (new URL(req.url).origin === location.origin || req.url.includes('fonts.g'))) {
        const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy));
      }
      return res;
    }).catch(() => caches.match(req).then(r => r || caches.match('./index.html')))
  );
});
