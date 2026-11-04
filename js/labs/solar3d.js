/* 3D lab wrapper around js/scenes.js kind 'solar'. Params are passed to the scene (see scenes.js). */
Labs.register('solar3d', {
  title: '3D solar', subjects: ['maths', 'science', 'evs', 'geography', 'social'],
  async render(host, p, api) {
    const m = await import('../scenes.js?v=' + (window.LAB_V || 1));
    host.innerHTML = '<div class="lb3d-ch">🎯 ' + String(p.challenge || 'Tap each planet from the Sun outward').replace(/[<>&]/g, '') + '</div><div class="lb3d"></div>';
    m.mount(host.querySelector('.lb3d'), Object.assign({ kind: 'solar' }, p));
    return () => m.unmount();
  },
  example: {}, examples: []
});
