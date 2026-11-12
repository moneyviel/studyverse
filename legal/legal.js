/* Knowtopia legal pages.
   ONE PLACE for the app name and the owner's details: edit SV_LEGAL below and every legal page follows.
   (The pages also carry the same words as plain text, so they still read correctly without JavaScript and for
   search engines. After a rename, also run the one-line replace in docs/legal-implementation.md, section 7.)
   Anything that still starts with "[OWNER" is shown highlighted in yellow so it is easy to spot before launch.

   This file also: uses the app's reading-comfort settings (text size, high contrast, reduce motion) saved on this
   device, and makes "Back to Knowtopia" return to where you were. */
var SV_LEGAL = {
  brand: 'Knowtopia',                         // the app name, used in every page
  brandHTML: 'Know<span>topia</span>',         // the coloured logo text in the page header
  operator: 'Mukesh Jhedu',                     // the person who owns and runs the app
  tradeName: 'MoneyViel',                       // the business name the app is offered under
  legalForm: 'an individual (sole proprietor) in India, trading as MoneyViel',
  address: '[OWNER TO FILL: full postal address with PIN], Pune, Maharashtra, India',
  email: 'support@knowtopia.in',
  site: 'https://knowtopia.in',
  goName: 'Mukesh Jhedu',                               // Grievance Officer
  goPhone: '[OWNER TO FILL: phone number]',
  hours: 'Monday to Saturday, 10 am to 6 pm IST (not on public holidays)',
  gstin: '[OWNER TO FILL: GSTIN, or write "Not registered for GST"]',
  version: '2.1',                               // policy set version: change it with legal/changes.html
  effective: '12 November 2026',
  effectiveISO: '2026-11-12'
};

(function () {
  var C = SV_LEGAL;
  var SIZES = [0.95, 1.08, 1.2, 1.34, 1.5], NAMES = ['S', 'M', 'L', 'XL', 'XXL'];
  var ux = {};
  try { ux = JSON.parse(localStorage.getItem('sv_ux') || '{}') || {}; } catch (e) {}
  var root = document.documentElement;
  var i = typeof ux.size === 'number' && SIZES[ux.size] ? ux.size : 1;
  root.style.fontSize = Math.round(SIZES[i] / 1.08 * 100) + '%';
  root.setAttribute('data-ts', NAMES[i]);
  function mq(q) { try { return window.matchMedia(q).matches; } catch (e) { return false; } }
  var hc = ux.hc == null ? mq('(prefers-contrast: more)') : !!ux.hc;
  var rm = ux.rm == null ? mq('(prefers-reduced-motion: reduce)') : !!ux.rm;
  root.classList.toggle('sv-hc', hc);
  root.classList.toggle('sv-rm', rm);

  var DEFAULT_BRAND = 'Knowtopia';
  function isPh(v) { return /^\[OWNER/.test(String(v)); }

  /* fill every marked spot from SV_LEGAL */
  function fill() {
    var all = document.querySelectorAll('.bn');
    for (var a = 0; a < all.length; a++) all[a].textContent = C.brand;
    var els = document.querySelectorAll('[data-l]');
    for (var b = 0; b < els.length; b++) {
      var el = els[b], k = el.getAttribute('data-l'), v = C[k];
      if (v == null) continue;
      if (k === 'brandHTML') { el.innerHTML = v; continue; }
      el.textContent = v;
      if (el.tagName === 'A' && k === 'email') el.href = 'mailto:' + v;
      if (el.tagName === 'A' && k === 'site') el.href = v;
      if (el.tagName === 'TIME' && k === 'effective') el.setAttribute('dateTime', C.effectiveISO);
      el.classList.toggle('ph', isPh(v));
    }
    if (C.brand !== DEFAULT_BRAND) {
      document.title = document.title.split(DEFAULT_BRAND).join(C.brand);
      var labelled = document.querySelectorAll('[aria-label*="' + DEFAULT_BRAND + '"]');
      for (var c = 0; c < labelled.length; c++) labelled[c].setAttribute('aria-label', labelled[c].getAttribute('aria-label').split(DEFAULT_BRAND).join(C.brand));
    }
  }

  /* Google Play build (the app sets localStorage sv_play = '1', see js/plans.js): no links to the pricing page or a
     payment site inside the app — such links become plain text (Play payments policy). The website is unchanged. */
  function playUnlink() {
    var play = false; try { play = localStorage.getItem('sv_play') === '1'; } catch (e) {}
    if (!play) return;
    var as = document.querySelectorAll('a[href*="pricing"], a[href*="razorpay"]');
    for (var i = 0; i < as.length; i++) { var sp = document.createElement('span'); sp.textContent = as[i].textContent; as[i].parentNode.replaceChild(sp, as[i]); }
  }

  document.addEventListener('DOMContentLoaded', function () {
    fill();
    playUnlink();
    var back = document.getElementById('backApp');
    if (!back) return;
    back.addEventListener('click', function (e) {
      var fromApp = false;
      try { var r = new URL(document.referrer); fromApp = r.origin === location.origin && !/\/legal\//.test(r.pathname); } catch (err) {}
      if (fromApp && history.length > 1) { e.preventDefault(); history.back(); }
    });
  });
})();
