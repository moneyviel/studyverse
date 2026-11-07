/* StudyVerse legal pages: use the app's own reading-comfort settings (text size, high contrast,
   reduce motion) saved on this device, and make "Back to StudyVerse" return to where you were. */
(function () {
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

  document.addEventListener('DOMContentLoaded', function () {
    var back = document.getElementById('backApp');
    if (!back) return;
    back.addEventListener('click', function (e) {
      var fromApp = false;
      try { var r = new URL(document.referrer); fromApp = r.origin === location.origin && !/\/legal\//.test(r.pathname); } catch (err) {}
      if (fromApp && history.length > 1) { e.preventDefault(); history.back(); }
    });
  });
})();
