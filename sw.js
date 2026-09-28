// Offline cache: app shell + data are precached; fonts and anything else are cached on first use.
const VERSION = 'adsp-v5';
const SHELL = [
  './', 'index.html', 'og.png', 'css/style.css', 'js/app.js', 'manifest.webmanifest',
  'icons/icon-192.png', 'icons/icon-512.png',
  'data/exam.json', 'data/mock/index.json',
  'data/questions/s1.json', 'data/questions/s2.json', 'data/questions/s3.json',
  'data/notes/s1.html', 'data/notes/s2.html', 'data/notes/s3.html',
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => Promise.all(SHELL.map((u) => c.add(u).catch(() => {})))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== VERSION).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
// network first for our own files (so fixes show up), cache first for fonts/CDN
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const same = new URL(req.url).origin === self.location.origin;
  if (same) {
    e.respondWith(fetch(req).then((res) => { const copy = res.clone(); caches.open(VERSION).then((c) => c.put(req, copy)); return res; })
      .catch(() => caches.match(req, { ignoreSearch: true }).then((r) => r || caches.match('index.html'))));
  } else {
    e.respondWith(caches.match(req).then((r) => r || fetch(req).then((res) => { const copy = res.clone(); caches.open(VERSION).then((c) => c.put(req, copy)); return res; })));
  }
});
