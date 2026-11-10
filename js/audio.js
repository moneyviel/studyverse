
/* ================= SOUND ENGINE (all music generated in code) ================= */
const SND={ctx:null, master:null, music:null, sfx:null, delay:null, on:true, mv:75, sv:90, choice:'auto', grade:6, myGrade:6, playing:false, step:0, next:0, timer:null, theme:null, pat:null, loop:0};
try{ const p=JSON.parse(localStorage.getItem('sv_snd2')||'{}'); if(p.on!==undefined)SND.on=p.on; if(p.mv!==undefined)SND.mv=p.mv; if(p.sv!==undefined)SND.sv=p.sv; if(p.choice)SND.choice=p.choice; }catch(e){}
function saveSnd(){ try{ localStorage.setItem('sv_snd2',JSON.stringify({on:SND.on,mv:SND.mv,sv:SND.sv,choice:SND.choice})); }catch(e){} }

const MODES={major:[0,2,4,5,7,9,11],mixo:[0,2,4,5,7,9,10],dorian:[0,2,3,5,7,9,10],minor:[0,2,3,5,7,8,10],lydian:[0,2,4,6,7,9,11],bhairav:[0,1,4,5,7,8,11],penta:[0,2,4,7,9,12,14],raga:[0,2,4,5,7,9,10]};
/* One soundtrack per class. Young = bright toy sounds, fast & bouncy. Older = deeper, cooler, calmer. */
const THEMES={
 1:{name:'Toy Box Parade',      desc:'Toy xylophone, happy & bouncy', mode:'major', root:60, bpm:132, prog:[0,4,5,3], lead:'bell',   dens:.85, drums:'toy',   bass:'boing', pad:false, seven:false, swing:0, penta:true,  seed:11},
 2:{name:'Bubble Garden',       desc:'Music-box bubbles & claps',     mode:'major', root:62, bpm:128, prog:[0,3,4,0], lead:'musicbox',dens:.8, drums:'clap',  bass:'boing', pad:false, seven:false, swing:0, penta:true,  seed:23},
 3:{name:'Sunny Marimba',       desc:'Marimba & shakers',            mode:'major', root:65, bpm:124, prog:[0,5,3,4], lead:'marimba',dens:.75, drums:'shaker',bass:'simple',pad:false, seven:false, swing:0, penta:true,  seed:37},
 4:{name:'Island Steel Drums',  desc:'Steel drums, beach groove',    mode:'mixo',  root:62, bpm:120, prog:[0,6,3,0], lead:'steel',  dens:.7,  drums:'light', bass:'simple',pad:false, seven:false, swing:0, penta:true,  seed:41},
 5:{name:'Explorer March',      desc:'Plucky adventure march',       mode:'major', root:60, bpm:116, prog:[0,3,4,5], lead:'pluck',  dens:.65, drums:'light', bass:'simple',pad:true,  seven:false, swing:0, penta:false, seed:53},
 6:{name:'Angle Island Groove', desc:'Funky chiptune adventure',     mode:'mixo',  root:57, bpm:112, prog:[0,6,3,4], lead:'chip',   dens:.6,  drums:'pop',   bass:'bounce',pad:true,  seven:false, swing:0, penta:false, seed:67},
 7:{name:'Mountain Quest',      desc:'Heroic game soundtrack',       mode:'dorian',root:62, bpm:108, prog:[0,3,6,3], lead:'chip',   dens:.55, drums:'pop',   bass:'bounce',pad:true,  seven:false, swing:0, penta:false, seed:71},
 8:{name:'Neon Arcade',         desc:'Synth-pop energy',             mode:'minor', root:57, bpm:110, prog:[0,5,2,6], lead:'synth',  dens:.55, drums:'pop',   bass:'synth', pad:true,  seven:false, swing:0, penta:false, seed:83},
 9:{name:'Port City Nights',    desc:'Synthwave with echo',          mode:'minor', root:52, bpm:100, prog:[0,5,6,4], lead:'synth',  dens:.45, drums:'wave',  bass:'synth', pad:true,  seven:true,  swing:0, penta:false, seed:97},
 10:{name:'Focus Flow',         desc:'Chill electronic, steady beat', mode:'dorian',root:55, bpm:96,  prog:[0,3,0,4], lead:'synth',  dens:.4,  drums:'wave',  bass:'synth', pad:true,  seven:true,  swing:0, penta:false, seed:101},
 11:{name:'Lab After Dark',     desc:'Deep house, calm & cool',      mode:'minor', root:53, bpm:92,  prog:[0,6,5,4], lead:'epiano', dens:.35, drums:'house', bass:'deep',  pad:true,  seven:true,  swing:.08,penta:false, seed:113},
 12:{name:'Board Exam Lo-fi',   desc:'Lo-fi beats to study to',      mode:'dorian',root:50, bpm:84,  prog:[0,3,6,4], lead:'epiano', dens:.3,  drums:'lofi',  bass:'deep',  pad:true,  seven:true,  swing:.14,penta:false, seed:127},
 13:{name:'Galaxy Gate Jazz',   desc:'Smooth jazz-hop',     mode:'lydian',root:53, bpm:80,  prog:[1,4,0,5], lead:'epiano', dens:.28, drums:'lofi',  bass:'walk',  pad:true,  seven:true,  swing:.16,penta:false, seed:139},
 14:{name:'Desi Dhol Dhamaka',  desc:'Dhol beats & bright melody',  mode:'raga',  root:62, bpm:118, prog:[0,3,4,0], lead:'shehnai',dens:.7,  drums:'dhol',  bass:'simple',pad:false, seven:false, swing:0, penta:false, seed:151},
 15:{name:'Sitar Sunrise',      desc:'Calm sitar & tabla feel',     mode:'bhairav',root:57,bpm:92,  prog:[0,0,3,4], lead:'sitar',  dens:.45, drums:'tabla', bass:'drone', pad:false, seven:false, swing:0, penta:false, seed:163},
 16:{name:'Rainbow Bounce',     desc:'Super happy, jumpy fun',      mode:'major', root:64, bpm:140, prog:[0,3,4,3], lead:'chip',   dens:.85, drums:'pop',   bass:'bounce',pad:false, seven:false, swing:0, penta:true,  seed:173},
 17:{name:'Retro Racer',        desc:'Fast arcade racing',          mode:'minor', root:57, bpm:150, prog:[0,6,5,6], lead:'chip',   dens:.7,  drums:'race',  bass:'synth', pad:false, seven:false, swing:0, penta:false, seed:181},
 18:{name:'Space Cadet',        desc:'Twinkly outer-space adventure', mode:'lydian',root:60,bpm:104, prog:[0,1,0,4], lead:'musicbox',dens:.5, drums:'wave',  bass:'synth', pad:true,  seven:true,  swing:0, penta:false, seed:191},
 19:{name:'Jungle Drums',       desc:'Tribal drums & marimba',      mode:'dorian',root:57, bpm:112, prog:[0,3,0,6], lead:'marimba',dens:.6,  drums:'jungle',bass:'simple',pad:false, seven:false, swing:0, penta:true,  seed:197},
 20:{name:'Calm Ocean',         desc:'Gentle waves, no drums',      mode:'major', root:55, bpm:72,  prog:[0,5,3,4], lead:'bell',   dens:.25, drums:'none',  bass:'drone', pad:true,  seven:true,  swing:0, penta:true,  seed:211},
 21:{name:'Chai & Chill',       desc:'Cozy lo-fi for homework',     mode:'dorian',root:53, bpm:78,  prog:[0,3,1,4], lead:'epiano', dens:.3,  drums:'lofi',  bass:'deep',  pad:true,  seven:true,  swing:.15,penta:false, seed:223},
 22:{name:'Victory Parade',     desc:'Big brass-style celebration', mode:'major', root:60, bpm:120, prog:[0,4,3,4], lead:'brass',  dens:.6,  drums:'march', bass:'simple',pad:true,  seven:false, swing:0, penta:false, seed:229},
 23:{name:'Midnight Focus',     desc:'Deep, steady concentration',  mode:'minor', root:50, bpm:88,  prog:[0,5,3,4], lead:'synth',  dens:.25, drums:'house', bass:'deep',  pad:true,  seven:true,  swing:0, penta:false, seed:233}
};
const GENRE={1:'Playful',2:'Playful',3:'Playful',4:'Playful',16:'Playful',14:'Desi',15:'Desi',5:'Adventure',6:'Adventure',7:'Adventure',18:'Adventure',19:'Adventure',22:'Adventure',8:'Energy',9:'Energy',17:'Energy',10:'Focus',11:'Focus',12:'Focus',13:'Focus',21:'Focus',23:'Focus',20:'Relax'};
const GENRES=['Playful','Desi','Adventure','Energy','Focus','Relax'];
const midiHz=m=>440*Math.pow(2,(m-69)/12);

function initAudio(){
  if(SND.ctx) { if(SND.ctx.state==='suspended') SND.ctx.resume(); return; }
  try{
    const C=new (window.AudioContext||window.webkitAudioContext)(); SND.ctx=C;
    SND.master=C.createGain(); SND.master.gain.value=1.4;
    const comp=C.createDynamicsCompressor(); comp.threshold.value=-10; comp.ratio.value=3; comp.attack.value=.003; comp.release.value=.2;
    const lim=C.createDynamicsCompressor(); lim.threshold.value=-2; lim.knee.value=0; lim.ratio.value=20; lim.attack.value=.001; lim.release.value=.1;
    SND.master.connect(comp); comp.connect(lim); lim.connect(C.destination);
    SND.music=C.createGain(); SND.music.connect(SND.master);
    SND.sfx=C.createGain(); SND.sfx.connect(SND.master);
    // echo for older soundtracks
    SND.delay=C.createDelay(1); const fb=C.createGain(); fb.gain.value=.32; const dl=C.createGain(); dl.gain.value=.35; SND.delayOut=dl;
    SND.delay.connect(fb); fb.connect(SND.delay); SND.delay.connect(dl); dl.connect(SND.music);
    // noise buffer for drums
    const nb=C.createBuffer(1,C.sampleRate,C.sampleRate), d=nb.getChannelData(0); for(let i=0;i<d.length;i++) d[i]=Math.random()*2-1; SND.noise=nb;
    applyVol();
  }catch(e){ SND.ctx=null; }
}
function applyVol(){
  if(!SND.ctx) return; const t=SND.ctx.currentTime;
  SND.music.gain.setTargetAtTime(SND.on? Math.pow(SND.mv/100,1.5)*1.6 : 0, t, .1);
  SND.sfx.gain.setTargetAtTime(Math.pow(SND.sv/100,1.5)*2.2, t, .05);
}
/* ---- instruments ---- */
function tone(t,f,dur,o={}){
  const C=SND.ctx, g=C.createGain(), dest=o.dest||SND.music, peak=o.gain??.2, a=o.attack??.005;
  const osc=C.createOscillator(); osc.type=o.type||'sine'; osc.frequency.setValueAtTime(f,t);
  if(o.slide) osc.frequency.exponentialRampToValueAtTime(o.slide,t+dur);
  if(o.detune) osc.detune.value=o.detune;
  let node=osc;
  if(o.lp){ const fl=C.createBiquadFilter(); fl.type='lowpass'; fl.frequency.setValueAtTime(o.lp,t); if(o.lpEnd) fl.frequency.exponentialRampToValueAtTime(o.lpEnd,t+dur); fl.Q.value=o.q||1; osc.connect(fl); node=fl; }
  node.connect(g); g.connect(dest); if(o.echo&&SND.delay) g.connect(SND.delay);
  g.gain.setValueAtTime(0,t); g.gain.linearRampToValueAtTime(peak,t+a);
  if(o.sustain){ g.gain.setValueAtTime(peak,t+dur-.15); g.gain.linearRampToValueAtTime(0,t+dur); }
  else g.gain.exponentialRampToValueAtTime(.0001,t+dur);
  osc.start(t); osc.stop(t+dur+.05);
}
function noise(t,dur,o={}){
  const C=SND.ctx, s=C.createBufferSource(); s.buffer=SND.noise;
  const f=C.createBiquadFilter(); f.type=o.ft||'highpass'; f.frequency.value=o.f||7000; f.Q.value=o.q||1;
  const g=C.createGain(); g.gain.setValueAtTime(o.gain??.1,t); g.gain.exponentialRampToValueAtTime(.0001,t+dur);
  s.connect(f); f.connect(g); g.connect(o.dest||SND.music); s.start(t,Math.random()*.5); s.stop(t+dur+.02);
}
const INST={
  bell:(t,f,d)=>{ tone(t,f,.5,{type:'triangle',gain:.16}); tone(t,f*4,.18,{type:'sine',gain:.05}); },
  musicbox:(t,f,d)=>{ tone(t,f*2,.6,{type:'sine',gain:.12}); tone(t,f*4.01,.25,{type:'sine',gain:.04}); },
  marimba:(t,f,d)=>{ tone(t,f,.35,{type:'sine',gain:.2}); tone(t,f*4,.06,{type:'sine',gain:.06}); },
  steel:(t,f,d)=>{ tone(t,f,.5,{type:'sine',gain:.15}); tone(t,f*2.02,.4,{type:'sine',gain:.07}); tone(t,f*3.98,.2,{type:'triangle',gain:.03}); },
  pluck:(t,f,d)=>tone(t,f,.3,{type:'square',gain:.07,lp:2600,lpEnd:500}),
  chip:(t,f,d)=>{ tone(t,f,Math.min(d,.22),{type:'square',gain:.06,lp:3500}); },
  synth:(t,f,d)=>{ tone(t,f,.4,{type:'sawtooth',gain:.07,lp:2200,lpEnd:400,echo:true}); tone(t,f,.4,{type:'sawtooth',gain:.04,detune:9,lp:1800,lpEnd:400}); },
  sitar:(t,f,d)=>{ tone(t,f*.97,.9,{type:'sawtooth',gain:.07,lp:3000,lpEnd:600,slide:f,q:4,echo:true}); tone(t,f*2,.4,{type:'triangle',gain:.03}); },
  shehnai:(t,f,d)=>{ tone(t,f*.985,Math.max(d,.25),{type:'sawtooth',gain:.07,lp:2600,q:3,attack:.03,slide:f}); tone(t,f,Math.max(d,.25),{type:'square',gain:.03,lp:1800,attack:.03}); },
  brass:(t,f,d)=>{ tone(t,f,Math.max(d,.3),{type:'sawtooth',gain:.09,lp:900,lpEnd:2400,attack:.03}); tone(t,f*1.005,Math.max(d,.3),{type:'sawtooth',gain:.05,lp:1200,attack:.03}); },
  epiano:(t,f,d)=>{ tone(t,f,1.2,{type:'sine',gain:.12,echo:true}); tone(t,f*2,.5,{type:'sine',gain:.03,detune:6}); tone(t,f*7,.08,{type:'sine',gain:.012}); }
};
function kick(t,g=.5){ tone(t,140,.28,{type:'sine',slide:42,gain:g}); }
function snare(t,g=.12){ noise(t,.16,{ft:'bandpass',f:1800,gain:g}); tone(t,190,.08,{type:'triangle',gain:g*.8}); }
function hat(t,g=.04){ noise(t,.04,{f:8000,gain:g}); }
function shaker(t,g=.035){ noise(t,.06,{f:6000,gain:g}); }
function clap(t,g=.09){ [0,.012,.024].forEach(o=>noise(t+o,.08,{ft:'bandpass',f:1500,gain:g})); }
function tick(t,g=.06){ tone(t,1900,.05,{type:'sine',gain:g}); }
function rim(t,g=.06){ tone(t,1700,.03,{type:'square',gain:g*.5,lp:3000}); }

/* ---- composition ---- */
function noteAt(th,deg,oct=0){ const sc=MODES[th.mode], n=sc.length; const o=Math.floor(deg/n); return th.root+12*(o+oct)+sc[((deg%n)+n)%n]; }
function chordNotes(th,deg){ const ns=[0,2,4].map(k=>noteAt(th,deg+k)); if(th.seven) ns.push(noteAt(th,deg+6)); return ns; }
function makePattern(th){
  // catchy 4-bar melody: random walk on chord tones & scale, seeded so each class always has "its" tune
  let s=th.seed; const r=()=>{ s=(s*9301+49297)%233280; return s/233280; };
  const pent=[0,1,2,4,5]; const mel=[]; let deg=th.prog[0]+2;
  for(let bar=0;bar<4;bar++){
    const ch=th.prog[bar];
    for(let e=0;e<8;e++){
      const strong=e%2===0, play = e===0 || r()<th.dens*(strong?1.1:.7);
      if(!play){ mel.push(null); continue; }
      if(e===0 || r()<.4){ deg=ch+[0,2,4][Math.floor(r()*3)]; }
      else deg+= [-2,-1,1,1,2][Math.floor(r()*5)];
      if(th.penta){ const n=7, base=Math.floor(deg/n)*n, rr=((deg%n)+n)%n; const nearest=pent.reduce((a,b)=>Math.abs(b-rr)<Math.abs(a-rr)?b:a); deg=base+nearest; }
      deg=Math.max(-1,Math.min(9,deg));
      mel.push({deg, len: r()<.25?2:1});
    }
  }
  // make bar 4 end on the home note so it loops sweetly
  mel[24]={deg:th.prog[3]+2,len:1}; mel[28]={deg:7,len:4}; for(let k=29;k<32;k++) mel[k]=null;
  return mel;
}
function scheduleStep(st,t){
  const th=SND.theme, bar=Math.floor(st/16)%4, s16=st%16, eighth=Math.floor(s16/2), spb=60/th.bpm;
  const chordDeg=th.prog[bar], dur16=spb/4;
  // swing on off-beat 8ths
  if(th.swing && s16%4===2) t+=th.swing*spb;
  // pad: whole bar chord
  if(s16===0 && th.pad){ chordNotes(th,chordDeg).forEach((m,i)=>{ tone(t,midiHz(m),spb*4,{type:th.seven?'triangle':'sawtooth',gain:th.seven?.035:.018,lp:th.seven?1400:900,attack:.25,sustain:true,detune:i%2?6:-6}); }); }
  // young classes: light chord stabs instead of pads
  if(!th.pad && (s16===0||s16===8)){ chordNotes(th,chordDeg).forEach(m=>tone(t,midiHz(m),.25,{type:'triangle',gain:.035})); }
  // bass
  const b=midiHz(noteAt(th,chordDeg,-1));
  switch(th.bass){
    case 'boing': if(s16===0||s16===8) tone(t,b,.22,{type:'sine',gain:.22,slide:b*1.5}); break;
    case 'simple': if(s16===0||s16===8) tone(t,b,.35,{type:'triangle',gain:.22}); break;
    case 'bounce': if([0,6,8,11,14].includes(s16)) tone(t,s16===11?b*1.5:b,.18,{type:'square',gain:.06,lp:700}); break;
    case 'synth': if(s16%2===0) tone(t,b/ (s16%4?1:2)*(s16%4?1:2),.2,{type:'sawtooth',gain:.07,lp:600,lpEnd:150}); break;
    case 'deep': if([0,3,10].includes(s16)) tone(t,b/2,.5,{type:'sine',gain:.32}); break;
    case 'drone': if(s16===0) { tone(t,midiHz(th.root-12),spb*4,{type:'sawtooth',gain:.05,lp:500,attack:.3,sustain:true}); tone(t,midiHz(th.root-5),spb*4,{type:'sawtooth',gain:.03,lp:500,attack:.3,sustain:true}); } break;
    case 'walk': if(s16%4===0){ const w=[0,2,4,5][s16/4]; tone(t,midiHz(noteAt(th,chordDeg+w,-2)),spb*.9,{type:'sine',gain:.3}); } break;
  }
  // drums
  const k4=s16%4===0;
  switch(th.drums){
    case 'toy': if(k4) tick(t,s16===0?.08:.05); break;
    case 'clap': if(s16===4||s16===12) clap(t,.06); if(k4) tick(t,.04); break;
    case 'shaker': if(s16%2===0) shaker(t,s16%4?.02:.035); if(s16===0) kick(t,.3); break;
    case 'light': if(s16===0||s16===8) kick(t,.35); if(s16%2===0) shaker(t,.025); if(s16===12) clap(t,.05); break;
    case 'pop': if(s16===0||s16===8||s16===10) kick(t,.45); if(s16===4||s16===12) snare(t,.1); if(s16%2===0) hat(t,.03); break;
    case 'wave': if(k4) kick(t,.42); if(s16===4||s16===12) snare(t,.11); hat(t,s16%2?.015:.03); break;
    case 'house': if(k4) kick(t,.45); if(s16%4===2) hat(t,.05); if(s16===4||s16===12) clap(t,.05); break;
    case 'dhol': if([0,3,6,10].includes(s16)) kick(t,.5); if([4,12].includes(s16)) tone(t,320,.12,{type:'triangle',gain:.22,slide:260}); if([2,7,9,14,15].includes(s16)) tone(t,520,.06,{type:'triangle',gain:.1}); if(s16%2===0) shaker(t,.03); break;
    case 'tabla': if([0,6,10].includes(s16)) tone(t,110,.4,{type:'sine',gain:.35,slide:70}); if([3,8,13].includes(s16)) tone(t,680,.09,{type:'sine',gain:.14,slide:600}); if([4,12,15].includes(s16)) tone(t,900,.05,{type:'triangle',gain:.07}); break;
    case 'race': if(s16%2===0) kick(t,.4); if(s16===4||s16===12) snare(t,.12); hat(t,.03); break;
    case 'jungle': if([0,3,8,11].includes(s16)) tone(t,95,.3,{type:'sine',gain:.4,slide:60}); if([6,14].includes(s16)) tone(t,210,.15,{type:'sine',gain:.2,slide:160}); if(s16%2===1) shaker(t,.025); break;
    case 'march': if(s16===0||s16===8) kick(t,.45); if(s16===4||s16===12) snare(t,.14); if(s16===14||s16===15) snare(t,.06); break;
    case 'lofi': if(s16===0||s16===10) kick(t,.4); if(s16===4||s16===12) rim(t,.09); if(s16%2===0) hat(t,.018); break;
  }
  // melody (on 8th notes); every 2nd loop, older themes rest for a bar to breathe
  if(s16%2===0){
    const idx=bar*8+eighth, n=SND.pat[idx];
    const rest = SND.loop%2===1 && bar===2 && th.dens<.5;
    if(n && !rest){ const oct = th.lead==='musicbox'||th.lead==='bell'?1:(th.lead==='epiano'?0:1); INST[th.lead](t, midiHz(noteAt(th,n.deg,oct)), dur16*2*n.len); }
  }
  if(st%64===63) SND.loop++;
}
function scheduler(){
  if(!SND.ctx||!SND.playing) return;
  const spb=60/SND.theme.bpm;
  while(SND.next < SND.ctx.currentTime+.12){ scheduleStep(SND.step,SND.next); SND.next+=spb/4; SND.step++; }
}
function myTrack(){ return SND.choice==='auto' ? SND.myGrade : +SND.choice; }
const parentMode=()=>document.documentElement.classList.contains('sv-parent');   // parent accounts (js/cloud.js): no music
function startMusic(grade){
  if(parentMode()) return;
  initAudio(); if(!SND.ctx) return;
  SND.grade = grade || myTrack();
  SND.theme=THEMES[SND.grade]; SND.pat=makePattern(SND.theme); SND.step=0; SND.loop=0;
  if(SND.delay) SND.delay.delayTime.value=(60/SND.theme.bpm)*.75;
  SND.next=SND.ctx.currentTime+.1; SND.playing=true;
  clearInterval(SND.timer); SND.timer=setInterval(scheduler,25);
  renderSoundPanel();
}
function duck(){ if(!SND.ctx||!SND.on) return; const g=SND.music.gain, t=SND.ctx.currentTime, v=Math.pow(SND.mv/100,1.5)*1.6; g.cancelScheduledValues(t); g.setValueAtTime(g.value,t); g.linearRampToValueAtTime(v*.3,t+.05); g.linearRampToValueAtTime(v,t+1.1); }

/* ---- sound effects ---- */
function sfx(kind){
  initAudio(); if(!SND.ctx) return; const t=SND.ctx.currentTime+.01, d=SND.sfx;
  switch(kind){
    case 'correct': duck(); [72,76,79,84].forEach((m,i)=>{ tone(t+i*.07,midiHz(m),.4,{type:'triangle',gain:.22,dest:d}); tone(t+i*.07,midiHz(m+12),.25,{type:'sine',gain:.06,dest:d}); });
      for(let i=0;i<6;i++) tone(t+.3+i*.04,midiHz(96+(i%3)*4),.12,{type:'sine',gain:.05,dest:d}); break;
    case 'wrong': duck();
      // "uh-oh" buzzer: two falling buzzy notes + a little wobble at the end
      tone(t,     midiHz(67),.2, {type:'square',  gain:.16,lp:2400,dest:d});
      tone(t,     midiHz(67)*1.01,.2,{type:'sawtooth',gain:.08,lp:2000,dest:d});
      tone(t+.22, midiHz(61),.55,{type:'square',  gain:.18,lp:2200,slide:midiHz(56),dest:d});
      tone(t+.22, midiHz(61)*1.01,.55,{type:'sawtooth',gain:.09,lp:1800,slide:midiHz(56),dest:d});
      noise(t+.22,.12,{ft:'lowpass',f:500,gain:.25,dest:d});
      break;
    case 'coin': tone(t,midiHz(83),.08,{type:'square',gain:.06,dest:d,lp:4000}); tone(t+.07,midiHz(88),.25,{type:'square',gain:.06,dest:d,lp:4000}); break;
    case 'unlock': duck(); [60,64,67,72].forEach((m,i)=>tone(t+i*.09,midiHz(m),.3,{type:'square',gain:.06,lp:3000,dest:d})); tone(t+.36,midiHz(76),.7,{type:'triangle',gain:.2,dest:d}); tone(t+.36,midiHz(79),.7,{type:'triangle',gain:.12,dest:d}); break;
    case 'hmm': tone(t,midiHz(67),.18,{type:'sine',gain:.15,dest:d}); tone(t+.15,midiHz(70),.3,{type:'sine',gain:.15,slide:midiHz(72),dest:d}); break;
    case 'tap': tone(t,midiHz(88),.05,{type:'sine',gain:.06,dest:d}); break;
    case 'open': tone(t,midiHz(72),.12,{type:'sine',gain:.1,dest:d,slide:midiHz(79)}); break;
  }
}

/* ---- panel ---- */
function openSound(){ initAudio(); renderSoundPanel(); try{ renderVoicePicker(); }catch(e){} document.getElementById('soundSheet').classList.add('show'); }
function closeSound(){ document.getElementById('soundSheet').classList.remove('show'); }
document.getElementById('soundSheet').addEventListener('click',e=>{ if(e.target.id==='soundSheet') closeSound(); });
function toggleMusic(){ SND.on=!SND.on; saveSnd(); if(SND.on && !SND.playing) startMusic(); applyVol(); renderSoundPanel(); updateSndBtn(); }
function setVol(which,v){ if(which==='music') SND.mv=+v; else { SND.sv=+v; sfx('coin'); } saveSnd(); applyVol(); updateSndBtn(); }
function chooseTrack(k){ SND.choice=k; saveSnd(); if(!SND.on){ SND.on=true; applyVol(); updateSndBtn(); } startMusic(); }
function previewGrade(g){ if(!SND.on){ SND.on=true; saveSnd(); applyVol(); updateSndBtn(); } startMusic(g); }
function renderSoundPanel(){
  document.getElementById('musicTgl').classList.toggle('on',SND.on);
  document.getElementById('musVol').value=SND.mv; document.getElementById('sfxVol').value=SND.sv;
  let h=`<div class="glabel">✨ Smart</div><button class="${SND.choice==='auto'?'on':''}" onclick="chooseTrack('auto')">🪄 Auto · grows with me</button>`;
  GENRES.forEach(gn=>{ h+=`<div class="glabel">${{Playful:'🎈',Desi:'🪘',Adventure:'🗺️',Energy:'⚡',Focus:'🎧',Relax:'🌊'}[gn]} ${gn}</div>`;
    Object.keys(THEMES).filter(k=>GENRE[k]===gn).forEach(k=>{ h+=`<button class="${SND.choice!=='auto'&&+SND.choice===+k?'on':''}" onclick="chooseTrack(${k})">${THEMES[k].name}</button>`; }); });
  document.getElementById('gradeChips').innerHTML=h;
  const th=THEMES[SND.grade];
  document.getElementById('nowPlay').innerHTML=`<div class="eq ${SND.on&&SND.playing?'':'off'}"><i></i><i></i><i></i><i></i></div><div>Now playing: ${th.name}<br><span style="color:#6b7090;font-weight:600;font-size:12px">${th.desc}</span></div>`;
}
function updateSndBtn(){ document.getElementById('sndIcon').textContent = !SND.on||SND.mv==0 ? '🔇' : SND.mv<40 ? '🔉' : '🔊'; }
updateSndBtn();

/* start music on the first tap (browsers block sound until the user touches the page) */
let firstTap=true;
document.addEventListener('pointerdown',()=>{ if(!firstTap) return; firstTap=false; initAudio(); if(SND.on) startMusic(); },{capture:true});
setTimeout(()=>{ if(firstTap && !parentMode() && !/^(pro|senior)$/.test(document.documentElement.dataset.age||'')) toast('🎵 Tap anywhere to start the music'); },1200);
/* stop sound when the phone locks, the app goes to background, or the page closes */
function pauseAll(){ if(SND.ctx && SND.ctx.state==='running') SND.ctx.suspend(); }
function resumeAll(){ if(SND.ctx && SND.on && document.visibilityState==='visible' && SND.ctx.state==='suspended') SND.ctx.resume(); }
document.addEventListener('visibilitychange',()=>{ document.hidden ? pauseAll() : resumeAll(); });
window.addEventListener('pagehide',pauseAll);
window.addEventListener('blur',pauseAll);
window.addEventListener('focus',resumeAll);
document.addEventListener('freeze',pauseAll);
document.addEventListener('pointerdown',resumeAll);

/* ---------- floating music control: small round button; tap it to show a volume slider, tap again to mute ---------- */
(function(){
  const css=`#mDock{position:fixed;left:max(10px,calc(50% - 210px));bottom:calc(138px + env(safe-area-inset-bottom));z-index:985;display:none;align-items:center;gap:2px;background:rgba(1,13,51,.88);border:1.5px solid rgba(255,255,255,.7);border-radius:999px;padding:2px;box-shadow:0 4px 12px rgba(0,0,0,.25);touch-action:manipulation}
#mDock.show{display:flex}
#mDock button{border:0;background:transparent;color:#fff;cursor:pointer;width:32px;height:32px;border-radius:999px;display:grid;place-items:center;font-size:16px;padding:0;line-height:1}
#mDock button:focus-visible{outline:2px solid #ffc93c;outline-offset:1px}
#mDock input[type=range]{display:none;width:96px;accent-color:#ffc93c;height:22px;margin:0 8px 0 2px}
#mDock.open input[type=range]{display:block}
html.sv-parent #mDock{display:none!important}
html.sv-gated #mDock{bottom:calc(18px + env(safe-area-inset-bottom))}
html.dsk #mDock{left:calc(var(--dsk-side) + 16px);bottom:78px}
@media print{#mDock{display:none!important}}`;
  const st=document.createElement('style'); st.textContent=css; document.head.appendChild(st);
  const d=document.createElement('div'); d.id='mDock'; d.setAttribute('role','group'); d.setAttribute('aria-label','Music');
  d.innerHTML=`<button type="button" aria-label="Music volume">🔊</button><input type="range" min="0" max="100" step="5" aria-label="Music volume">`;
  document.body.appendChild(d);
  const btn=d.querySelector('button'), rng=d.querySelector('input');
  let closeT=0;
  const off=()=>!SND.on||SND.mv==0;
  function sync(){
    btn.textContent=off()?'🔇':SND.mv<40?'🔉':'🔊';
    btn.setAttribute('aria-label', d.classList.contains('open') ? (off()?'Unmute music':'Mute music') : 'Music volume');
    rng.value=SND.on?SND.mv:0;
  }
  function open(on){ d.classList.toggle('open',on); clearTimeout(closeT); if(on) closeT=setTimeout(()=>open(false),4000); sync(); }
  function show(){ if(parentMode()||d.classList.contains('show')) return; d.classList.add('show'); sync(); }
  btn.addEventListener('click',e=>{ e.stopPropagation();
    if(!d.classList.contains('open')) return open(true);
    if(SND.on && SND.mv==0){ SND.mv=40; saveSnd(); applyVol(); updateSndBtn(); } else toggleMusic();
    open(true); });
  rng.addEventListener('input',e=>{ e.stopPropagation(); const v=+rng.value;
    if(!SND.on && v>0){ SND.on=true; if(!SND.playing) startMusic(); }
    setVol('music',v); try{ const m=document.getElementById('musVol'); if(m) m.value=v; }catch(_){}
    open(true); });
  const _u=updateSndBtn; updateSndBtn=function(){ _u(); sync(); };
  const _s=startMusic; startMusic=function(g){ _s(g); if(SND.playing) show(); };
  const _t=toggleMusic; toggleMusic=function(){ _t(); sync(); };
  if(SND.playing) show();
})();
