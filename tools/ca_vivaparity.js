// Runs the JS matcher from js/ca-tools.js on stdin cases (used by tools/ca_validate.py to prove JS == Python):
//   node tools/ca_vivaparity.js js/ca-tools.js                 stdin [[vivaQuestion, answer], …]   → [[pct, hit, tokens], …]
//   node tools/ca_vivaparity.js js/ca-tools.js js/ca-check.js  stdin [[question, answer], …]       → [checkResult, …]   (answer checker)
const fs=require('fs');const src=fs.readFileSync(process.argv[2],'utf8');
const a=src.indexOf('/* ================= offline matcher'), b=src.indexOf('/* ================= content helpers');
let code=src.slice(a,b)+';global.vivaScore=vivaScore;global.tokens=tokens;';
if(process.argv[3]){const cs=fs.readFileSync(process.argv[3],'utf8');const c0=cs.indexOf('/* ================= checker core'),c1=cs.indexOf('/* ================= checker end');
  code+=cs.slice(c0,c1)+';global.CK=makeChecker({pairs,tokens,clauses,phraseIn,same,kwSame,pointHit,isNum});';}
eval(code);
const cases=JSON.parse(fs.readFileSync(0,'utf8'));
const out=process.argv[3]?cases.map(([q,ans])=>CK.checkAnswer(q,ans)):cases.map(([v,ans])=>{const r=vivaScore(v,ans);return [r.pct,r.hit,tokens(ans)]});
console.log(JSON.stringify(out));
