/* 3D lab wrapper around js/scenes.js kind 'molecule'. Params are passed to the scene (see scenes.js). */
Labs.register('molecule3d', {
  title: '3D molecule', subjects: ['maths', 'science', 'evs', 'geography', 'social'],
  async render(host, p, api) {
    const m = await import('../scenes.js?v=' + (window.LAB_V || 1));
    host.innerHTML = '<div class="lb3d-ch">🎯 ' + String(p.challenge || 'Spin the molecule and count its atoms').replace(/[<>&]/g, '') + '</div><div class="lb3d"></div>';
    m.mount(host.querySelector('.lb3d'), Object.assign({ kind: 'molecule' }, p));
    return () => m.unmount();
  },
  example: {name:'water'}, examples: [{name:'co2'}]
});
