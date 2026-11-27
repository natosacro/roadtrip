// Road trip d'Avvento: funziona anche offline (in galleria o in montagna senza rete).
const CACHE = "roadtrip-v47";
const FILES = ["./", "./index.html", "./manifest.json", "./icona2-192.png", "./icona2-512.png", "./icona2-180.png", "./icona2-maskable-512.png", "./benzina.json", "./etzel.json", "./fonts/bitter-latin-600-normal.woff2", "./fonts/bitter-latin-700-italic.woff2", "./fonts/bitter-latin-700-normal.woff2", "./fonts/bitter-latin-ext-600-normal.woff2", "./fonts/bitter-latin-ext-700-italic.woff2", "./fonts/bitter-latin-ext-700-normal.woff2", "./fonts/courier-prime-latin-400-normal.woff2", "./fonts/courier-prime-latin-700-normal.woff2", "./fonts/courier-prime-latin-ext-400-normal.woff2", "./fonts/courier-prime-latin-ext-700-normal.woff2", "./fonts/overpass-latin-600-normal.woff2", "./fonts/overpass-latin-700-normal.woff2", "./fonts/overpass-latin-800-normal.woff2", "./fonts/overpass-latin-ext-600-normal.woff2", "./fonts/overpass-latin-ext-700-normal.woff2", "./fonts/overpass-latin-ext-800-normal.woff2", "./fonts/patrick-hand-latin-400-normal.woff2", "./fonts/patrick-hand-latin-ext-400-normal.woff2", "./fonts/source-sans-3-latin-400-italic.woff2", "./fonts/source-sans-3-latin-400-normal.woff2", "./fonts/source-sans-3-latin-600-normal.woff2", "./fonts/source-sans-3-latin-700-normal.woff2", "./fonts/source-sans-3-latin-ext-400-italic.woff2", "./fonts/source-sans-3-latin-ext-400-normal.woff2", "./fonts/source-sans-3-latin-ext-600-normal.woff2", "./fonts/source-sans-3-latin-ext-700-normal.woff2"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});
// Prima la rete (così le modifiche arrivano subito), poi la copia salvata se non c'è campo.
// Solo i file dell'app: niente cache per GitHub (dati privati, chiave), radio (flussi infiniti) o altri siti.
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  if (new URL(e.request.url).origin !== self.location.origin) return;
  e.respondWith(
    fetch(e.request)
      .then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copy)).catch(() => {});
        return res;
      })
      .catch(() => caches.match(e.request, { ignoreSearch: true }).then((r) => r || caches.match("./index.html")))
  );
});
