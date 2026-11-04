/* 3D lab wrapper around js/scenes.js kind 'atom'. Params are passed to the scene (see scenes.js). */
Labs.register('atom3d', {
  title: '3D atom', subjects: ['maths', 'science', 'evs', 'geography', 'social'],
  async render(host, p, api) {
    const m = await import('../scenes.js?v=' + (window.LAB_V || 1));
    host.innerHTML = '<div class="lb3d-ch">🎯 ' + String(p.challenge || 'Change elements and count the electrons in each shell').replace(/[<>&]/g, '') + '</div><div class="lb3d"></div>';
    m.mount(host.querySelector('.lb3d'), Object.assign({ kind: 'atom' }, p));
    return () => m.unmount();
  },
  example: {z:6}, examples: [{z:11}]
});
