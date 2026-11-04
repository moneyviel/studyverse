/* 3D lab wrapper around js/scenes.js kind 'moon'. Params are passed to the scene (see scenes.js). */
Labs.register('moon3d', {
  title: '3D moon', subjects: ['maths', 'science', 'evs', 'geography', 'social'],
  async render(host, p, api) {
    const m = await import('../scenes.js?v=' + (window.LAB_V || 1));
    host.innerHTML = '<div class="lb3d-ch">🎯 ' + String(p.challenge || 'Watch for the full moon').replace(/[<>&]/g, '') + '</div><div class="lb3d"></div>';
    m.mount(host.querySelector('.lb3d'), Object.assign({ kind: 'moon' }, p));
    return () => m.unmount();
  },
  example: {}, examples: []
});
