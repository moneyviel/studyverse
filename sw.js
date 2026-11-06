/* StudyVerse service worker: makes the app installable and work offline.
   Pages: always try the internet first (so updates show up), fall back to saved copy. */
const CACHE = 'studyverse-v12';
const CORE = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png',
  './css/base.css?v=12', './css/app.css?v=12', './js/worlds.js?v=12', './js/visuals.js?v=12', './js/games.js?v=12', './js/app.js?v=12', './js/audio.js?v=12', './js/labs/core.js?v=12', './js/practice.js?v=12', './js/tests.js?v=12', './js/ux.js?v=12', './js/nav.js?v=12', './js/ask.js?v=12', './js/scenes.js?v=12', './js/vendor/three.module.min.js', './js/vendor/OrbitControls.js', './content/curriculum.json'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => Promise.all(CORE.map(u => c.add(u).catch(() => {}))))); self.skipWaiting(); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  e.respondWith(
    fetch(req).then(res => {
      if (res.ok && (new URL(req.url).origin === location.origin || req.url.includes('fonts.g'))) {
        const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy));
      }
      return res;
    }).catch(() => caches.match(req).then(r => r || caches.match('./index.html')))
  );
});
