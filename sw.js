// あそびば ゲーム：オフライン用（ファイルを更新したら VERSION を変える）
const VERSION='asobiba-v14';
const FILES=['./','./index.html','./manifest.webmanifest','./icon-180.png','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(VERSION).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==VERSION).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{if(e.request.method!=='GET'||new URL(e.request.url).origin!==location.origin)return;
  e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||fetch(e.request).then(res=>{
    if(res.ok&&res.type==='basic'&&new URL(e.request.url).origin===location.origin){const cp=res.clone();caches.open(VERSION).then(c=>c.put(e.request,cp));}
    return res;}).catch(()=>caches.match('./index.html'))));});
