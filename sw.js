const C='kidbodhi-v16',F=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png','./landing-1280.webp','./landing-720.webp'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(F)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||!r.url.startsWith(self.location.origin))return;
 const page=r.mode==='navigate'||r.destination==='document';
 if(page){/* pages: always try the network first so updates show immediately; cache only for offline */
  e.respondWith(fetch(r).then(n=>{const cp=n.clone();caches.open(C).then(c=>c.put('./index.html',cp));return n}).catch(()=>caches.match('./index.html')));return}
 /* images/icons: cache first, refresh in background */
 e.respondWith(caches.match(r).then(m=>{const net=fetch(r).then(n=>{if(n.ok){const cp=n.clone();caches.open(C).then(c=>c.put(r,cp))}return n}).catch(()=>m);return m||net}))});
