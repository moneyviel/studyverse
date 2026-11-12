/* Knowtopia service worker: makes the app installable and work offline.
   Pages: always try the internet first (so updates show up), fall back to saved copy. */
const CACHE = 'studyverse-v100';
const CORE = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './icons/emblem-128.webp', './icons/logo-full.webp',
  './css/base.css?v=100', './css/app.css?v=100', './js/worlds.js?v=100', './js/visuals.js?v=100', './js/games.js?v=100', './js/app.js?v=100', './js/audio.js?v=100', './js/labs/core.js?v=100', './js/demo.js?v=100', './js/fields.js?v=100', './js/cloud.js?v=100', './js/plans.js?v=100', './js/parent.js?v=100', './js/teach.js?v=100', './js/inst.js?v=100', './js/rt.js?v=100', './js/live.js?v=100', './js/puzzles-core.js?v=100', './js/puzzles.js?v=100', './js/puzzles-worker.js?v=100', './js/playhub.js?v=100', './js/mindpics.js?v=100', './js/guard.js?v=100', './js/voice.js?v=100', './js/suites-gen.js?v=100', './js/suites.js?v=100', './js/mindpool.js?v=100', './js/family.js?v=100', './js/melayout.js?v=100', './js/nextup.js?v=100', './js/mindgym.js?v=100', './js/mindplay-gen.js?v=100', './js/mindplay.js?v=100', './js/heartplay-gen.js?v=100', './js/heartplay.js?v=100', './js/rewards.js?v=100', './js/squad.js?v=100', './js/story.js?v=100', './js/exam.js?v=100', './js/practice.js?v=100', './js/tests.js?v=100', './js/ux.js?v=100', './js/nav.js?v=100', './js/review.js?v=100', './js/leave.js?v=100', './js/scope.js?v=100', './js/pz-words.js?v=100', './js/arcade.js?v=100', './js/gen.js?v=100', './js/ask.js?v=100', './js/look.js?v=100', './js/legal.js?v=100', './js/dashboard.js?v=100', './js/insights.js?v=100', './js/gk.js?v=100', './content/gk/daily.json', './content/gk/index.json', './js/ca-gen.js?v=100', './js/ca.js?v=100', './js/jee.js?v=100', './content/jee/phy/u01.json', './content/jee/phy/u01-practice.json', './js/ca-pad.js?v=100', './js/ca-tools.js?v=100', './js/ca-speed.js?v=100', './js/ca-check.js?v=100', './js/ca-read.js?v=100', './js/ca-keys-data.js?v=100', './js/ca-keys.js?v=100', './content/ca/foundation/mocks/fnd-p1-m1.json', './content/ca/foundation/structure.json', './content/ca/foundation/weightage.json', './content/ca/inter/structure.json', './content/ca/final/structure.json', './content/ca/motivation.json', './content/ca/foundation/p1/ch02/u01.json', './content/ca/foundation/p1/ch02/u02.json', './content/ca/foundation/p1/ch02/u03.json', './content/ca/foundation/p1/ch02/u04.json', './content/ca/foundation/p1/ch02/u05.json', './content/ca/foundation/p1/ch02/u06.json', './content/ca/foundation/p2/ch02/u01.json', './js/calc.js?v=100', './js/calc-acad-data.js?v=100', './js/calc-acad.js?v=100', './js/stars.js?v=100', './js/sheets.js?v=100', './js/a11y.js?v=100', './js/owner.js?v=100', './js/playready.js?v=100', './legal/delete-account.html', './css/desktop.css?v=100', './js/desktop.js?v=100', './js/scenes.js?v=100', './js/vendor/three.module.min.js', './js/vendor/OrbitControls.js', './content/curriculum.json',
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
