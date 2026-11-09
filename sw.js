/* Knowtopia service worker: makes the app installable and work offline.
   Pages: always try the internet first (so updates show up), fall back to saved copy. */
const CACHE = 'studyverse-v61';
const CORE = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png',
  './css/base.css?v=61', './css/app.css?v=61', './js/worlds.js?v=61', './js/visuals.js?v=61', './js/games.js?v=61', './js/app.js?v=61', './js/audio.js?v=61', './js/labs/core.js?v=61', './js/demo.js?v=61', './js/fields.js?v=61', './js/cloud.js?v=61', './js/plans.js?v=61', './js/parent.js?v=61', './js/teach.js?v=61', './js/inst.js?v=61', './js/rt.js?v=61', './js/live.js?v=61', './js/puzzles-core.js?v=61', './js/puzzles.js?v=61', './js/puzzles-worker.js?v=61', './js/playhub.js?v=61', './js/rewards.js?v=61', './js/squad.js?v=61', './js/story.js?v=61', './js/exam.js?v=61', './js/practice.js?v=61', './js/tests.js?v=61', './js/ux.js?v=61', './js/nav.js?v=61', './js/arcade.js?v=61', './js/gen.js?v=61', './js/ask.js?v=61', './js/look.js?v=61', './js/legal.js?v=61', './js/dashboard.js?v=61', './js/insights.js?v=61', './js/gk.js?v=61', './content/gk/daily.json', './content/gk/index.json', './js/ca-gen.js?v=61', './js/ca.js?v=61', './js/ca-pad.js?v=61', './js/ca-tools.js?v=61', './js/ca-speed.js?v=61', './js/ca-check.js?v=61', './js/ca-read.js?v=61', './js/ca-keys-data.js?v=61', './js/ca-keys.js?v=61', './content/ca/foundation/mocks/fnd-p1-m1.json', './content/ca/foundation/structure.json', './content/ca/foundation/weightage.json', './content/ca/inter/structure.json', './content/ca/final/structure.json', './content/ca/motivation.json', './content/ca/foundation/p1/ch02/u01.json', './content/ca/foundation/p1/ch02/u02.json', './content/ca/foundation/p1/ch02/u03.json', './content/ca/foundation/p1/ch02/u04.json', './content/ca/foundation/p1/ch02/u05.json', './content/ca/foundation/p1/ch02/u06.json', './content/ca/foundation/p2/ch02/u01.json', './js/calc.js?v=61', './js/calc-acad-data.js?v=61', './js/calc-acad.js?v=61', './js/stars.js?v=61', './js/sheets.js?v=61', './js/a11y.js?v=61', './js/owner.js?v=61', './js/playready.js?v=61', './legal/delete-account.html', './css/desktop.css?v=61', './js/desktop.js?v=61', './js/scenes.js?v=61', './js/vendor/three.module.min.js', './js/vendor/OrbitControls.js', './content/curriculum.json',
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
    fetch(req).then(res => {
      if (res.ok && (new URL(req.url).origin === location.origin || req.url.includes('fonts.g'))) {
        const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy));
      }
      return res;
    }).catch(() => caches.match(req).then(r => r || caches.match('./index.html')))
  );
});
