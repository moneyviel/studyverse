/* StudyVerse service worker: makes the app installable and work offline.
   Pages: always try the internet first (so updates show up), fall back to saved copy. */
const CACHE = 'studyverse-v32';
const CORE = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png',
  './css/base.css?v=32', './css/app.css?v=32', './js/worlds.js?v=32', './js/visuals.js?v=32', './js/games.js?v=32', './js/app.js?v=32', './js/audio.js?v=32', './js/labs/core.js?v=32', './js/demo.js?v=32', './js/cloud.js?v=32', './js/practice.js?v=32', './js/tests.js?v=32', './js/ux.js?v=32', './js/nav.js?v=32', './js/arcade.js?v=32', './js/gen.js?v=32', './js/ask.js?v=32', './js/look.js?v=32', './js/legal.js?v=32', './js/dashboard.js?v=32', './js/insights.js?v=32', './js/gk.js?v=32', './content/gk/daily.json', './content/gk/index.json', './js/ca-gen.js?v=32', './js/ca.js?v=32', './js/ca-pad.js?v=32', './js/ca-tools.js?v=32', './js/ca-check.js?v=32', './content/ca/foundation/mocks/fnd-p1-m1.json', './content/ca/foundation/structure.json', './content/ca/foundation/weightage.json', './content/ca/inter/structure.json', './content/ca/final/structure.json', './content/ca/motivation.json', './content/ca/foundation/p1/ch02/u01.json', './content/ca/foundation/p1/ch02/u02.json', './content/ca/foundation/p1/ch02/u03.json', './content/ca/foundation/p1/ch02/u04.json', './content/ca/foundation/p1/ch02/u05.json', './content/ca/foundation/p1/ch02/u06.json', './content/ca/foundation/p2/ch02/u01.json', './js/calc.js?v=32', './js/a11y.js?v=32', './js/scenes.js?v=32', './js/vendor/three.module.min.js', './js/vendor/OrbitControls.js', './content/curriculum.json',
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
