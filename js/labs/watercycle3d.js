/* 3D lab wrapper around js/scenes.js kind 'watercycle'. Params are passed to the scene (see scenes.js). */
Labs.register('watercycle3d', {
  title: '3D watercycle', subjects: ['maths', 'science', 'evs', 'geography', 'social'],
  async render(host, p, api) {
    const m = await import('../scenes.js?v=' + (window.LAB_V || 1));
    host.innerHTML = '<div class="lb3d-ch">🎯 ' + String(p.challenge || 'Tap each stage of the water cycle').replace(/[<>&]/g, '') + '</div><div class="lb3d"></div>';
    m.mount(host.querySelector('.lb3d'), Object.assign({ kind: 'watercycle' }, p));
    return () => m.unmount();
  },
  example: {}, examples: []
});
