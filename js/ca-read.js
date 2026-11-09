/* CA photo answers: read the handwriting so the answer can be marked.
   Photos (already compressed on the phone, ≤1600 px JPEG) are sent to the server function "studyverse-read", which asks
   Google Gemini (free tier) for an exact transcription — it does not correct or mark anything. The student then checks
   and corrects the text, and the app's own checker (js/ca-check.js) marks it like a typed answer.
   Adults only, checked ON THE SERVER: when the student has answered "I'm 18 or older" in the "Read my handwriting?" prompt
   (js/ca.js stores sv_adult = 'y'), rpc confirm_adult records it once per account (profiles.adult_confirmed_at); the
   server function refuses anyone not confirmed and any student in a school class (migration 20261113_play_ready.sql).
   Needs js/cloud.js (window.Cloud). */
(function () {
  const AK = 'sv_adult_srv';                                     // account ids already confirmed on the server (this phone)
  async function confirmAdult() {
    let adult = null; try { adult = localStorage.getItem('sv_adult'); } catch (e) {}
    if (adult !== 'y') throw new Error('Photo reading is only for students aged 18 or older.');
    const u = Cloud.user && Cloud.user(), id = u && u.id; if (!id) return;
    let done = []; try { done = JSON.parse(localStorage.getItem(AK) || '[]') || []; } catch (e) {}
    if (done.includes(id)) return;
    const r = await Cloud.rest('rpc/confirm_adult', { method: 'POST', body: {} });
    const j = Array.isArray(r) ? r[0] : r;
    if (j && j.ok === false) { try { localStorage.setItem('sv_adult', 'n'); } catch (e) {} throw new Error(j.msg || 'Photo reading is only for adult CA students.'); }
    try { localStorage.setItem(AK, JSON.stringify(done.concat(id).slice(-5))); } catch (e) {}
  }
  const toB64 = blob => new Promise((res, rej) => { const r = new FileReader(); r.onload = () => res(String(r.result).split(',')[1] || ''); r.onerror = () => rej(new Error('Could not open the photo.')); r.readAsDataURL(blob); });
  async function read(blobs, question) {
    if (!window.Cloud || !Cloud.signedIn()) throw new Error('Please sign in first.');
    if (navigator.onLine === false) throw new Error('No internet connection. Connect and try again, or type your key points.');
    await confirmAdult();
    const images = []; for (const b of blobs.slice(0, 4)) images.push(await toB64(b));
    const r = await Cloud.call('/functions/v1/studyverse-read', { method: 'POST', body: { images, question: String(question || '').slice(0, 1500) } });
    if (r && r.error && /^(adult|school)$/.test(r.code || '')) { try { const d = JSON.parse(localStorage.getItem(AK) || '[]').filter(x => x !== (Cloud.user() || {}).id); localStorage.setItem(AK, JSON.stringify(d)); } catch (e) {} }
    if (!r || r.error) throw new Error((r && r.error) || 'Could not read the photo.');
    return r.text;
  }
  window.CaRead = { read, confirmAdult };
})();
