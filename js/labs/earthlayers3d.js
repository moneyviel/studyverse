/* 3D lab wrapper around js/scenes.js kind 'earthlayers'. Params are passed to the scene (see scenes.js). */
Labs.register('earthlayers3d', {
  title: '3D earthlayers', subjects: ['maths', 'science', 'evs', 'geography', 'social'],
  async render(host, p, api) {
    const m = await import('../scenes.js?v=' + (window.LAB_V || 1));
    host.innerHTML = '<div class="lb3d-ch">🎯 ' + String(p.challenge || 'Tap all four layers').replace(/[<>&]/g, '') + '</div><div class="lb3d"></div>';
    m.mount(host.querySelector('.lb3d'), Object.assign({ kind: 'earthlayers' }, p));
    return () => m.unmount();
  },
  example: {}, examples: []
});
