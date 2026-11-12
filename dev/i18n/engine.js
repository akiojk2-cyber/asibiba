
/* ========== ことば（多言語） ==========
   にほんごの もじを そのまま キーにして、がめんの もじ・canvasの もじを ほんやくする */
const LANGS=[['ja','🇯🇵 にほんご'],['en','🇬🇧 English'],['uk','🇺🇦 Українська'],['zh','🇨🇳 中文'],['ko','🇰🇷 한국어'],['es','🇪🇸 Español'],['pt','🇧🇷 Português']];
/*@@I18N@@*/
let LANG='ja';
const JP_RE=/[぀-ヿ一-鿿]/,TR_SKIP='.kttile,.ktslot,.ktwords,script,style,[translate="no"],.langbtn';
let TRC=new Map(),TRP=[];
const TR_MISS=new Set();
function trBuild(){TRC=new Map();TRP=[];const d=I18N[LANG]||{};
  for(const k in d){if(!/\{\d+\}/.test(k))continue;
    const src='^'+k.replace(/[.*+?^$()|[\]\\]/g,'\\$&').replace(/\{\d+\}/g,'([\\s\\S]*?)')+'$';
    TRP.push({re:new RegExp(src),v:d[k],lit:k.replace(/\{\d+\}/g,'').length});}
  TRP.sort((a,b)=>b.lit-a.lit);}
function trPart(g){return g&&JP_RE.test(g)?tr(g):(g||'');}
function trCore(k){const d=I18N[LANG];if(Object.prototype.hasOwnProperty.call(d,k))return d[k];
  for(const p of TRP){const m=k.match(p.re);if(m)return p.v.replace(/\{(\d+)\}/g,(x,n)=>trPart(m[+n+1]));}
  const pm=k.match(/^([^\u3040-\u30ff\u4e00-\u9fff]+?) (.+)$/);if(pm&&JP_RE.test(pm[2])){const t=tr(pm[2]);if(t!==pm[2])return pm[1]+' '+t;}
  for(const sep of['・','、']){if(k.includes(sep)){const ps=k.split(sep);if(ps.length>1){const out=ps.map(x=>tr(x));if(out.every((x,i)=>x!==ps[i]||!JP_RE.test(ps[i])))return out.join(sep==='・'?' · ':', ');}}}
  TR_MISS.add(k);return k;}
function tr(s){if(LANG==='ja'||typeof s!=='string'||!JP_RE.test(s))return s;
  const m=s.match(/^(\s*)([\s\S]*?)(\s*)$/),core=m[2].replace(/\s+/g,' ');
  let r=TRC.get(core);if(r===undefined){r=trCore(core);TRC.set(core,r);}
  return m[1]+r+m[3];}
// がめんの もじ
const TR_ORIG=new WeakMap(),TR_DONE=new WeakMap();
function trText(n,force){const p=n.parentElement;if(!p||p.closest(TR_SKIP))return;
  let base=n.data;if(TR_DONE.get(n)===base){if(!force)return;base=TR_ORIG.get(n);}
  TR_ORIG.set(n,base);const t=tr(base);if(t!==n.data){TR_DONE.set(n,t);n.data=t;}else TR_DONE.set(n,t);}
function trTree(root,force){if(root.nodeType===3){trText(root,force);return;}if(root.nodeType!==1||(root.matches&&root.matches(TR_SKIP)))return;
  const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let x;while((x=w.nextNode()))trText(x,force);}
const trObs=new MutationObserver(rs=>{if(LANG==='ja')return;for(const r of rs){if(r.type==='characterData')trText(r.target);else r.addedNodes.forEach(n=>trTree(n));}});
// canvasの もじ
['fillText','strokeText','measureText'].forEach(fn=>{const o=CanvasRenderingContext2D.prototype[fn];
  CanvasRenderingContext2D.prototype[fn]=function(t,...a){return o.call(this,LANG==='ja'?t:tr(String(t)),...a);};});
// あそびかた
const HOWTO_JA=document.querySelector('#howto .howbody').innerHTML;
function setLang(l){if(!I18N[l]&&l!=='ja')l='ja';LANG=l;try{localStorage.setItem('asobiba-lang',l);}catch(e){}
  document.documentElement.lang=l==='zh'?'zh-Hans':l;trBuild();
  document.querySelector('#howto .howbody').innerHTML=l==='ja'?HOWTO_JA:(HOWTO_L[l]||HOWTO_JA);
  trTree(document.body,true);document.title=l==='ja'?'あそびば ゲーム':tr('あそびば ゲーム');
  const b=$('langBtn');if(b)b.textContent='🌐 '+LANGS.find(x=>x[0]===l)[1].replace(/^\S+\s/,'');
  trObs.disconnect();if(l!=='ja')trObs.observe(document.body,{childList:true,subtree:true,characterData:true});}
function pickLang(){modal('🌐',LANGS.map(([k,nm])=>({label:nm,cls:k===LANG?'':'gray',fn:()=>setLang(k)})));
  document.querySelectorAll('#modal .mbtns').forEach(r=>{r.classList.add('langrow');r.setAttribute('translate','no');});}
(function(){let l=null;try{l=localStorage.getItem('asobiba-lang');}catch(e){}
  if(!l){const n=(navigator.language||'ja').toLowerCase().slice(0,2);l=LANGS.some(x=>x[0]===n)?n:'ja';}
  setLang(l);})();
