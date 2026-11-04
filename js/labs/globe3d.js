/* 3D lab wrapper around js/scenes.js kind 'globe'. Params are passed to the scene (see scenes.js). */
Labs.register('globe3d', {
  title: '3D globe', subjects: ['maths', 'science', 'evs', 'geography', 'social'],
  async render(host, p, api) {
    const m = await import('../scenes.js?v=' + (window.LAB_V || 1));
    host.innerHTML = '<div class="lb3d-ch">🎯 ' + String(p.challenge || 'Spin the Earth and tap the Tropic of Cancer').replace(/[<>&]/g, '') + '</div><div class="lb3d"></div>';
    m.mount(host.querySelector('.lb3d'), Object.assign({ kind: 'globe' }, p));
    return () => m.unmount();
  },
  example: {}, examples: []
});
