/* Knowtopia tiny Supabase Realtime client (no supabase-js).
   Phoenix channel protocol vsn 1.0.0 (JSON objects) over one WebSocket:
     wss://<project>.supabase.co/realtime/v1/websocket?apikey=<publishable key>&vsn=1.0.0
   - join a topic ("realtime:room-ABCDEF") with { config: { broadcast: { self: true }, presence: { key: userId }, private: false }, access_token }
   - heartbeat on topic "phoenix" every 25 s; no reply within the next beat = dead socket → reconnect
   - broadcast:  send(event, payload)  → every member gets { event, payload } (self included)
   - presence:   track(meta)           → onPresence(map of key → [metas]) on every change
   - reconnects with backoff (1, 2, 4, 8 … 30 s) and re-joins + re-tracks; refreshes the user token on re-join
   Used by js/live.js (Game Rooms). Needs window.Cloud (js/cloud.js) for the project URL, key and the user's token. */
(function () {
  'use strict';
  const HEART = 25000;
  const wsURL = () => (window.Cloud ? Cloud.api : '').replace(/^http/, 'ws') + '/realtime/v1/websocket?apikey=' + encodeURIComponent(window.Cloud ? Cloud.key : '') + '&vsn=1.0.0';
  async function token() {
    let a = null; try { a = JSON.parse(localStorage.getItem('sv_auth') || 'null'); } catch (e) {}
    if (a && a.exp && a.exp - 90 < Date.now() / 1000 && window.Cloud) { try { await Cloud.call('/auth/v1/user'); a = JSON.parse(localStorage.getItem('sv_auth') || 'null'); } catch (e) {} }  // Cloud.call refreshes an old token first
    return (a && a.at) || (window.Cloud ? Cloud.key : '');
  }

  /* open(topic, opts) → channel. opts: { key, onBroadcast(event, payload), onPresence(state), onStatus('joining'|'joined'|'closed'|'error') } */
  function open(topic, opts) {
    opts = opts || {};
    const full = 'realtime:' + topic;
    let ws = null, ref = 0, joinRef = null, joined = false, closed = false, beat = 0, pendingBeat = null, retry = 0, retryT = 0, tokT = 0, meta = null;
    const queue = [];                 // broadcasts sent while not joined (kept short)
    let presence = {};
    const status = s => { ch.status = s; try { opts.onStatus && opts.onStatus(s); } catch (e) {} };
    const raw = m => { try { if (ws && ws.readyState === 1) { ws.send(JSON.stringify(m)); return true; } } catch (e) {} return false; };
    const push = (event, payload, topicName) => { const r = String(++ref); raw({ topic: topicName || full, event, payload, ref: r, join_ref: topicName ? undefined : joinRef }); return r; };
    function sync(st) { presence = st; try { opts.onPresence && opts.onPresence(presence); } catch (e) {} }
    function diff(d) {
      const st = Object.assign({}, presence);
      Object.entries(d.leaves || {}).forEach(([k, v]) => { const gone = new Set((v.metas || []).map(m => m.phx_ref)); const left = (st[k] || []).filter(m => !gone.has(m.phx_ref)); if (left.length) st[k] = left; else delete st[k]; });
      Object.entries(d.joins || {}).forEach(([k, v]) => { st[k] = (st[k] || []).concat(v.metas || []); });
      sync(st);
    }
    function connect() {
      if (closed) return;
      clearTimeout(retryT); status('joining');
      try { ws = new WebSocket(wsURL()); } catch (e) { return later(); }
      const me = ws;
      ws.onopen = async () => {
        if (me !== ws) return;
        const at = await token(); if (me !== ws || closed) return;
        joinRef = String(++ref);
        raw({ topic: full, event: 'phx_join', ref: joinRef, join_ref: joinRef,
          payload: { config: { broadcast: { ack: false, self: true }, presence: { key: opts.key || '' }, postgres_changes: [], private: false }, access_token: at } });
        clearInterval(beat);
        beat = setInterval(() => {
          if (pendingBeat) { try { ws.close(1000, 'timeout'); } catch (e) {} return; }          // no reply to the last beat: reconnect
          pendingBeat = push('heartbeat', {}, 'phoenix');
        }, HEART);
      };
      ws.onmessage = e => {
        if (me !== ws) return;
        let m; try { m = JSON.parse(e.data); } catch (x) { return; }
        if (m.topic === 'phoenix') { if (m.ref === pendingBeat) pendingBeat = null; return; }
        if (m.topic !== full) return;
        if (m.event === 'phx_reply' && m.ref === joinRef) {
          if (m.payload && m.payload.status === 'ok') {
            joined = true; retry = 0; status('joined');
            if (meta) push('presence', { type: 'presence', event: 'track', payload: meta });
            while (queue.length) { const q = queue.shift(); push('broadcast', { type: 'broadcast', event: q[0], payload: q[1] }); }
            clearInterval(tokT); tokT = setInterval(async () => { const at = await token(); push('access_token', { access_token: at }); }, 10 * 60000);
          } else { status('error'); try { ws.close(1000); } catch (x) {} }
          return;
        }
        if (m.event === 'broadcast' && m.payload) { try { opts.onBroadcast && opts.onBroadcast(m.payload.event, m.payload.payload || {}); } catch (x) { console.warn(x); } return; }
        if (m.event === 'presence_state') return sync(Object.fromEntries(Object.entries(m.payload || {}).map(([k, v]) => [k, v.metas || []])));
        if (m.event === 'presence_diff') return diff(m.payload || {});
        if (m.event === 'phx_error' || m.event === 'phx_close') { try { ws.close(1000); } catch (x) {} }
      };
      ws.onclose = () => { if (me !== ws) return; joined = false; clearInterval(beat); clearInterval(tokT); pendingBeat = null; sync({}); status('closed'); later(); };
      ws.onerror = () => { if (me !== ws) return; status('error'); };
    }
    function later() {
      if (closed) return;
      const wait = Math.min(30000, 1000 * Math.pow(2, retry++)) * (0.8 + Math.random() * 0.4);
      clearTimeout(retryT); retryT = setTimeout(connect, wait);
    }
    const ch = {
      status: 'joining', topic,
      get joined() { return joined; },
      get presence() { return presence; },
      send(event, payload) { if (joined) push('broadcast', { type: 'broadcast', event, payload: payload || {} }); else { queue.push([event, payload || {}]); if (queue.length > 10) queue.shift(); } },
      track(m) { meta = m; if (joined) push('presence', { type: 'presence', event: 'track', payload: m }); },
      reconnect() { if (closed) return; retry = 0; if (ws && ws.readyState <= 1) { try { ws.close(1000, 'reconnect'); } catch (e) {} } else connect(); },
      close() {
        closed = true; clearTimeout(retryT); clearInterval(beat); clearInterval(tokT);
        if (ws) { try { if (joined) push('phx_leave', {}); ws.close(1000, 'leave'); } catch (e) {} }
        ws = null; joined = false; status('closed');
      }
    };
    addEventListener('online', ch.reconnect);
    const oldClose = ch.close; ch.close = () => { removeEventListener('online', ch.reconnect); oldClose(); };
    connect();
    return ch;
  }
  window.RT = { open, _url: wsURL };
})();
