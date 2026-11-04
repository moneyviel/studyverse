/* 3D lab wrapper around js/scenes.js kind 'plant'. Params are passed to the scene (see scenes.js). */
Labs.register('plant3d', {
  title: '3D plant', subjects: ['maths', 'science', 'evs', 'geography', 'social'],
  async render(host, p, api) {
    const m = await import('../scenes.js?v=' + (window.LAB_V || 1));
    host.innerHTML = '<div class="lb3d-ch">🎯 ' + String(p.challenge || 'Tap all the parts of the plant').replace(/[<>&]/g, '') + '</div><div class="lb3d"></div>';
    m.mount(host.querySelector('.lb3d'), Object.assign({ kind: 'plant' }, p));
    return () => m.unmount();
  },
  example: {}, examples: []
});
