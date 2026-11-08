/* CA photo answers: read the handwriting so the answer can be marked.
   Photos (already compressed on the phone, ≤1600 px JPEG) are sent to the server function "studyverse-read", which asks
   Google Gemini (free tier) for an exact transcription — it does not correct or mark anything. The student then checks
   and corrects the text, and the app's own checker (js/ca-check.js) marks it like a typed answer.
   Needs js/cloud.js (window.Cloud). */
(function () {
  const toB64 = blob => new Promise((res, rej) => { const r = new FileReader(); r.onload = () => res(String(r.result).split(',')[1] || ''); r.onerror = () => rej(new Error('Could not open the photo.')); r.readAsDataURL(blob); });
  async function read(blobs, question) {
    if (!window.Cloud || !Cloud.signedIn()) throw new Error('Please sign in first.');
    if (navigator.onLine === false) throw new Error('No internet connection. Connect and try again, or type your key points.');
    const images = []; for (const b of blobs.slice(0, 4)) images.push(await toB64(b));
    const r = await Cloud.call('/functions/v1/studyverse-read', { method: 'POST', body: { images, question: String(question || '').slice(0, 1500) } });
    if (!r || r.error) throw new Error((r && r.error) || 'Could not read the photo.');
    return r.text;
  }
  window.CaRead = { read };
})();
