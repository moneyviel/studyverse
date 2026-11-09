/* StudyVerse service worker: makes the app installable and work offline.
   Pages: always try the internet first (so updates show up), fall back to saved copy. */
const CACHE = 'studyverse-v51';
const CORE = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png',
  './css/base.css?v=51', './css/app.css?v=51', './js/worlds.js?v=51', './js/visuals.js?v=51', './js/games.js?v=51', './js/app.js?v=51', './js/audio.js?v=51', './js/labs/core.js?v=51', './js/demo.js?v=51', './js/cloud.js?v=51', './js/plans.js?v=51', './js/parent.js?v=51', './js/rt.js?v=51', './js/live.js?v=51', './js/puzzles-core.js?v=51', './js/puzzles.js?v=51', './js/puzzles-worker.js?v=51', './js/practice.js?v=51', './js/tests.js?v=51', './js/ux.js?v=51', './js/nav.js?v=51', './js/arcade.js?v=51', './js/gen.js?v=51', './js/ask.js?v=51', './js/look.js?v=51', './js/legal.js?v=51', './js/dashboard.js?v=51', './js/insights.js?v=51', './js/gk.js?v=51', './content/gk/daily.json', './content/gk/index.json', './js/ca-gen.js?v=51', './js/ca.js?v=51', './js/ca-pad.js?v=51', './js/ca-tools.js?v=51', './js/ca-speed.js?v=51', './js/ca-check.js?v=51', './js/ca-read.js?v=51', './js/ca-keys-data.js?v=51', './js/ca-keys.js?v=51', './content/ca/foundation/mocks/fnd-p1-m1.json', './content/ca/foundation/structure.json', './content/ca/foundation/weightage.json', './content/ca/inter/structure.json', './content/ca/final/structure.json', './content/ca/motivation.json', './content/ca/foundation/p1/ch02/u01.json', './content/ca/foundation/p1/ch02/u02.json', './content/ca/foundation/p1/ch02/u03.json', './content/ca/foundation/p1/ch02/u04.json', './content/ca/foundation/p1/ch02/u05.json', './content/ca/foundation/p1/ch02/u06.json', './content/ca/foundation/p2/ch02/u01.json', './js/calc.js?v=51', './js/calc-acad-data.js?v=51', './js/calc-acad.js?v=51', './js/stars.js?v=51', './js/sheets.js?v=51', './js/a11y.js?v=51', './js/scenes.js?v=51', './js/vendor/three.module.min.js', './js/vendor/OrbitControls.js', './content/curriculum.json',
  './legal/index.html', './legal/terms.html', './legal/privacy.html', './legal/disclaimer.html', './legal/liability.html', './legal/copyright.html', './legal/refunds.html', './legal/community.html', './legal/accessibility.html', './legal/contact.html', './legal/legal.css', './legal/legal.js'];
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
    fetch(req).then(res => {
      if (res.ok && (new URL(req.url).origin === location.origin || req.url.includes('fonts.g'))) {
        const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy));
      }
      return res;
    }).catch(() => caches.match(req).then(r => r || caches.match('./index.html')))
  );
});
