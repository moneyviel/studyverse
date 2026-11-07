// Runs the JS viva matcher from js/ca-tools.js on [vivaQuestion, answer] pairs read from stdin (used by tools/ca_validate.py to prove JS == Python).
const fs=require('fs');const src=fs.readFileSync(process.argv[2],'utf8');
const a=src.indexOf('/* ================= offline matcher'), b=src.indexOf('/* ================= content helpers');
eval(src.slice(a,b)+';global.vivaScore=vivaScore;global.tokens=tokens;');
const cases=JSON.parse(fs.readFileSync(0,'utf8'));
const out=cases.map(([v,ans])=>{const r=vivaScore(v,ans);return [r.pct,r.hit,tokens(ans)]});
console.log(JSON.stringify(out));
