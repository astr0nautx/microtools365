/* ==========================================================================
   microtools365 — Offline Service Worker
   Cache version: 2.1
   ========================================================================== */

const CACHE_NAME = 'mt365-cache-v2.1';
const OFFLINE_URL = '/offline.html';

const PRECACHE_ASSETS = [
  '/',
  '/offline.html',
  '/css/style.css?v=2.1',
  '/js/main.js?v=2.1',
  '/favicon.ico',
  '/logo.svg',
  '/icon-192.png',
  '/icon-512.png',
  '/manifest.json'
];

// Install: Cache critical static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// Activate: Clean up older cache versions and take control
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Strategy depending on request type
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Only handle GET requests
  if (req.method !== 'GET') return;

  // Bypass third-party analytics and comments
  if (
    url.hostname.includes('google-analytics.com') ||
    url.hostname.includes('googletagmanager.com') ||
    url.hostname.includes('cusdis.com')
  ) {
    return;
  }

  // 1. Navigation requests (HTML pages): Network-first with offline fallback
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then((networkRes) => {
          if (networkRes && networkRes.status === 200) {
            const resClone = networkRes.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, resClone));
          }
          return networkRes;
        })
        .catch(async () => {
          const cachedRes = await caches.match(req);
          if (cachedRes) return cachedRes;
          const fallback = await caches.match(OFFLINE_URL);
          return fallback || new Response('Offline', { status: 503, headers: { 'Content-Type': 'text/plain' } });
        })
    );
    return;
  }

  // 2. Static assets (CSS, JS, Fonts, Images): Stale-while-revalidate / Cache-first
  const isStaticAsset = (
    url.origin === self.location.origin ||
    url.hostname.includes('fonts.googleapis.com') ||
    url.hostname.includes('fonts.gstatic.com') ||
    url.hostname.includes('cdnjs.cloudflare.com')
  );

  if (isStaticAsset) {
    event.respondWith(
      caches.match(req).then((cachedRes) => {
        const fetchPromise = fetch(req)
          .then((networkRes) => {
            if (networkRes && networkRes.status === 200) {
              const resClone = networkRes.clone();
              caches.open(CACHE_NAME).then((cache) => cache.put(req, resClone));
            }
            return networkRes;
          })
          .catch(() => cachedRes);

        return cachedRes || fetchPromise;
      })
    );
  }
});
