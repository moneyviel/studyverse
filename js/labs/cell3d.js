/* 3D lab wrapper around js/scenes.js kind 'cell'. Params are passed to the scene (see scenes.js). */
Labs.register('cell3d', {
  title: '3D cell', subjects: ['maths', 'science', 'evs', 'geography', 'social'],
  async render(host, p, api) {
    const m = await import('../scenes.js?v=' + (window.LAB_V || 1));
    host.innerHTML = '<div class="lb3d-ch">🎯 ' + String(p.challenge || 'Tap every part of the cell').replace(/[<>&]/g, '') + '</div><div class="lb3d"></div>';
    m.mount(host.querySelector('.lb3d'), Object.assign({ kind: 'cell' }, p));
    return () => m.unmount();
  },
  example: {type:'plant'}, examples: [{type:'animal'}]
});
